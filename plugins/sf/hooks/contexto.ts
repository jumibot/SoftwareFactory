import { atom, read, update } from 'claude-code'
import type { PromptComposeResult } from 'claude-code'
import { configuracion, convenciones } from './configuracion'
import { MARCA_SF, PROYECTO } from './constantes'
import { normal } from './control'
import { importaCopia, leerJson, raizSesion } from './lectura'
import type { $ } from './lectura'
import { detectarPython, lineaPython } from './python'
import { ORDEN_EMPEZAR } from './bienvenida'

// ── Lo que pinta la SF y lo global no son del proyecto (decisión 167) ──
// En los proyectos incorporados a la SF (con .sf/proyecto.json), nunca en la propia SF, el mod añade al final del prompt de sistema una regla corta: lo que el plugin pinta en el proyecto
// es de la SF y ~/.claude es de todos los proyectos. Va en el prompt de sistema y no como contexto de un evento: llega
// en cada petición, también tras un /clear o una compactación, y aunque el proyecto se incorporara con una versión de
// la SF que aún no traía la regla. Es la parte variable (`session`) de la caché, siempre con el mismo texto.
export const ID_REGLA = 'sf:lo-que-es-de-la-sf'
export const REGLA_SF =
  'Software Factory: lo que el plugin sf pinta aquí (panel, caja sobre el prompt con su línea gris «SF x.y.z · fase», avisos) y sus skills y hooks son de la SF, no de este proyecto: una petición sobre ello no se cambia aquí ni se anota en el proyecto, ni en su cola ni en sus propuestas: se dice en una línea que es de la SF; llevarla a la SF es cosa del propietario, en una sesión de la SF. ' +
  'Lo global (~/.claude: ajustes, línea de estado, plugins) afecta a todos los proyectos: no se toca sin que el propietario lo pida y lo confirme.'

// Si la carpeta de la sesión es un proyecto incorporado a la SF que no es la propia SF, por carpeta. Solo se guarda el
// sí, que dura lo que la carga del mod: el no se vuelve a mirar cada vez, porque la carpeta puede incorporarse en esta
// misma conversación (decisión 242).
const conRegla = new Set<string>()

export async function llevaRegla($: $): Promise<boolean> {
  const raiz = await raizSesion($)
  const clave = raiz.toLowerCase()
  if (conRegla.has(clave)) return true
  const si = (await $.fs.exists(`${raiz}/${PROYECTO}`)) && !(await $.fs.exists(`${raiz}/${MARCA_SF}`))
  if (si) conRegla.add(clave)
  return si
}

// Una carpeta sin SF: ni proyecto incorporado ni la propia SF. Sin guardar: puede incorporarse en la conversación.
export async function sinSf($: $): Promise<boolean> {
  const raiz = await raizSesion($)
  return !(await $.fs.exists(`${raiz}/${PROYECTO}`)) && !(await $.fs.exists(`${raiz}/${MARCA_SF}`))
}

// Añade la regla al final de las secciones en un proyecto incorporado (decisión 167): no en la SF, donde lo del plugin
// sí es del proyecto, ni en una carpeta sin SF. Si algo falla, el prompt sigue como estaba.
export async function anadirRegla($: $, r: PromptComposeResult): Promise<PromptComposeResult> {
  if (r.sections.some(s => s.id === ID_REGLA)) return r
  if (!(await llevaRegla($).catch(() => false))) return r
  return { sections: [...r.sections, { id: ID_REGLA, text: REGLA_SF, scope: 'session' }] }
}

// ── Las reglas de la SF y la orquestación, del plugin instalado (decisión 187) ──
// En los proyectos incorporados, no en la SF, el mod las entrega como contexto de SessionStart al empezar la sesión,
// tras /clear y tras compactar: las reglas comunes de templates/claude-sf.md (tareas, repositorio y decisiones), las
// del método de templates/claude-sf-metodologia.md si el proyecto sigue la metodología, la línea de sus convenciones
// (idioma, commits, remoto y rama de publicación, de .sf/proyecto.json) y el texto entero de sf:orquestacion. No en
// resume ni fork, donde la conversación ya las tiene. Así el CLAUDE.md del proyecto no lleva ninguna línea de la SF y
// cargar la orquestación no depende de que Claude se acuerde.
export const PLANTILLA_REGLAS = 'templates/claude-sf.md'
export const PLANTILLA_METODOLOGIA = 'templates/claude-sf-metodologia.md'
export const SKILL_ORQUESTACION = 'skills/orquestacion/SKILL.md'
export const FUENTES_REGLAS = new Set(['startup', 'clear', 'compact'])
// Interruptor de .sf/proyecto.json (decisión 171): `automatizaciones.orquestacion`, encendido salvo que valga false.
export async function entregaOrquestacion($: $, raiz: string): Promise<boolean> {
  try {
    const a = (await leerJson($, `${raiz}/${PROYECTO}`)).automatizaciones as Record<string, unknown> | undefined
    return a?.orquestacion !== false
  } catch {
    return true
  }
}

// Quita del texto el comentario inicial (la cabecera de la copia) o el frontmatter de la skill.
const sinCabecera = (t: string) =>
  t
    .replace(/^\uFEFF?/, '')
    .replace(/^<!--[\s\S]*?-->\s*/, '')
    .replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n\s*/, '')
    .trim()

// Lo que el mod dice del intérprete de Python (236) en SessionStart, en cualquier carpeta (también la SF y una sin
// incorporar), en las mismas fuentes que las reglas y nunca a un subagente; null si es `python`.
export async function contextoPython($: $, e: { source: string; agent_id?: string }): Promise<string | null> {
  if (!FUENTES_REGLAS.has(e.source) || e.agent_id) return null
  return lineaPython(await detectarPython($))
}

// Lo que el mod entrega en SessionStart, o null si no toca: fuera de un proyecto incorporado, en otra fuente, en un
// subagente (no deben recibir la orquestación; según la documentación SessionStart no les llega, pero por si acaso)
// o sin nada que entregar.
export async function contextoInicial($: $, e: { source: string; agent_id?: string }): Promise<string | null> {
  if (!FUENTES_REGLAS.has(e.source) || e.agent_id) return null
  // Lo que se entrega ahora queda dado en esta conversación: sin SF, no, y se entrega al incorporarse (decisión 242).
  const lleva = await llevaRegla($)
  await update($, reglasDadas, () => lleva)
  if (!lleva) return null
  return textoReglas($, e.source === 'compact' ? 'compactar' : e.source === 'clear' ? 'hacer /clear' : 'empezar la sesión')
}

// ── Tras incorporar, las reglas con el siguiente mensaje (decisión 242) ──
// Si la conversación empezó en una carpeta sin SF y la carpeta se incorpora en ella, el siguiente mensaje del
// propietario lleva las reglas y la orquestación, una vez: sin reiniciar ni /clear, que sigue valiendo de respaldo.
// En $.state: /reload-plugins no lo reinicia; cada SessionStart (empezar, /clear, compactar) lo vuelve a fijar.
const reglasDadas = atom({ plugin: 'sf', key: 'reglasDadas' } as const, false)
export async function reglasAlIncorporar($: $): Promise<string | null> {
  if (await read($, reglasDadas)) return null
  if (!(await llevaRegla($))) return null
  await update($, reglasDadas, () => true)
  return textoReglas($, 'incorporarse el proyecto en esta conversación')
}

// ── En una carpeta sin SF, ofrecer incorporarla (decisión 243) ──
// Con el primer mensaje del propietario de la conversación, Claude pregunta con un menú si quiere incorporar el
// proyecto. Una vez por conversación: tras /clear o en una sesión nueva, otra vez. En $.state, como la pantalla.
const incorporarOfrecido = atom({ plugin: 'sf', key: 'incorporarOfrecido' } as const, false)
// Las tres respuestas del menú (decisión 246). «Ahora no» no pregunta más en la conversación; «No, y no vuelvas a
// preguntar en esta carpeta» se guarda por carpeta en el almacén del mod, cuando el mod ve la respuesta del menú.
export const SI_INCORPORAR = 'Sí, incorporarlo'
export const AHORA_NO = 'Ahora no'
export const NUNCA_AQUI = 'No, y no vuelvas a preguntar en esta carpeta'
export const CLAVE_NO_INCORPORAR = 'noIncorporar'
export const TEXTO_INCORPORAR =
  'Software Factory: el plugin sf está instalado, pero esta carpeta no está incorporada a la SF (no tiene .sf/proyecto.json). ' +
  'Si este mensaje ya pide incorporarla, carga la skill sf:incorporar_proyecto_a_sf y síguela, sin preguntar. Si no, antes de atenderlo, ' +
  `pregunta al usuario con un menú (herramienta AskUserQuestion; sin menú, en una línea) si quiere incorporar este proyecto a la SF, con tres opciones, con estas etiquetas exactas: «${SI_INCORPORAR}», «${AHORA_NO}» y «${NUNCA_AQUI}». ` +
  `Con el sí, carga sf:incorporar_proyecto_a_sf y síguela. Con cualquiera de los dos no, añade una nota en una línea: el proyecto se puede incorporar cuando lo pida, escribiendo «incorpora este proyecto a la SF»; ` +
  'después atiende su mensaje y no vuelvas a preguntarlo en esta conversación (el mod recuerda el segundo no para esta carpeta). ' +
  'Si pregunta por el panel: se abre con /sf (a pantalla completa, solo), y sin incorporar solo da la bienvenida.'
async function carpetasSinPreguntar($: $): Promise<Record<string, boolean>> {
  const g = (await $.store.get(CLAVE_NO_INCORPORAR).catch(() => undefined)) as Record<string, boolean> | undefined
  return g && typeof g === 'object' ? g : {}
}
export async function ofrecerIncorporar($: $): Promise<string | null> {
  if (await read($, incorporarOfrecido)) return null
  if (!(await sinSf($))) return null
  if ((await carpetasSinPreguntar($))[(await raizSesion($)).toLowerCase()]) return null
  await update($, incorporarOfrecido, () => true)
  return TEXTO_INCORPORAR
}
// Sin SF, la línea del prompt sugiere la orden de incorporar, en gris, Tab para tomarla (tarea 323): al empezar la
// sesión y tras /clear, mientras la carpeta no esté incorporada ni se haya dicho «no vuelvas a preguntar» (decisión 246).
// La sugerencia se va en cuanto se escribe algo o corre un turno; el motor la sustituye por la suya tras un turno.
export async function sugerirIncorporar($: $): Promise<boolean> {
  if (!(await sinSf($))) return false
  if ((await carpetasSinPreguntar($))[(await raizSesion($)).toLowerCase()]) return false
  return (await $.prompt.suggest({ text: ORDEN_EMPEZAR })).isShown
}
// La respuesta de un menú del principal: si eligió no volver a preguntar, se guarda la carpeta (decisión 246).
export async function anotarRespuestaIncorporar($: $, respuestas: unknown): Promise<void> {
  if (!respuestas || typeof respuestas !== 'object') return
  if (!Object.values(respuestas as Record<string, unknown>).some(v => typeof v === 'string' && v.trim().startsWith(NUNCA_AQUI))) return
  const g = await carpetasSinPreguntar($)
  await $.store.set(CLAVE_NO_INCORPORAR, { ...g, [(await raizSesion($)).toLowerCase()]: true })
}
export async function reiniciarIncorporar($: $): Promise<void> {
  await update($, incorporarOfrecido, () => false)
}

// Las reglas y la orquestación del proyecto de la sesión, con el momento en que se entregan.
async function textoReglas($: $, momento: string): Promise<string | null> {
  const raiz = await raizSesion($)
  const raizPlugin = normal($.plugin.root).replace(/\/$/, '')
  const partes: string[] = []
  if (!(await importaCopia($, raiz))) {
    const conf = await configuracion($, raiz)
    const leer = async (rel: string) => sinCabecera(await $.fs.read(`${raizPlugin}/${rel}`).catch(() => ''))
    const reglas = [await leer(PLANTILLA_REGLAS), conf.metodologia ? await leer(PLANTILLA_METODOLOGIA) : '', convenciones(conf)].filter(Boolean)
    partes.push(reglas.join('\n\n'))
  }
  if (await entregaOrquestacion($, raiz)) {
    const orq = sinCabecera(await $.fs.read(`${raizPlugin}/${SKILL_ORQUESTACION}`))
    if (orq)
      partes.push(
        `# sf:orquestacion, ya cargada\n\nEl mod de la SF entrega aquí la skill sf:orquestacion entera: el agente principal la aplica en cada mensaje sin cargarla con la herramienta Skill. Un subagente no la aplica: sigue su encargo. Carpeta de la skill, para sus referencias: ${raizPlugin}/skills/orquestacion\n\n${orq}`,
      )
  }
  if (partes.length === 0) return null
  return `Software Factory (plugin sf, entregado por su mod al ${momento}):\n\n${partes.join('\n\n---\n\n')}`
}
