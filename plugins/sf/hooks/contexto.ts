import { atom, read, update } from 'claude-code'
import type { PromptComposeResult } from 'claude-code'
import { configuracion, convenciones } from './configuracion'
import { MARCA_SF, PROYECTO } from './constantes'
import { normal } from './control'
import { importaCopia, leerIncorporacion, leerJson, raizSesion, rutaIncorporacion } from './lectura'
import type { $ } from './lectura'
import { detectarPython, lineaPython } from './python'
import { ORDEN_EMPEZAR } from './bienvenida'
import { lanzar } from './identidad'
import { encargarAClaude } from './avisos'

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

// Si el mod entrega las reglas y sf:orquestacion: en un proyecto incorporado y en la propia SF (decisión 298), que no
// tiene .sf/proyecto.json y se reconoce por su marca; su configuración sale de ella (configuracion.ts). La regla del
// prompt de sistema, en cambio, solo en los proyectos (llevaRegla).
export async function entregaReglas($: $): Promise<boolean> {
  return !(await sinSf($))
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
// En los proyectos incorporados y en la propia SF (decisión 298), el mod las entrega como contexto de SessionStart al empezar la sesión,
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
  const lleva = await entregaReglas($)
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
  // Solo un proyecto se incorpora en la conversación: la SF las recibe en SessionStart.
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

// ── La incorporación en pausa (tarea 333, decisión 258) ──
// Un turno del principal que acaba (también interrumpido con Esc, en un menú o mientras Claude trabaja) con una
// incorporación a medias la pone en pausa: no se borra lo respondido. El mod añade "pausa": true al progreso, y
// incorporacion.py la quita en cuanto Claude anota algo. En pausa, el panel atenúa la lista y ofrece Continuar (pasa a
// Claude ORDEN_CONTINUAR) y Abandonar (borra el progreso, sin Claude). Al cargar el mod (sesión nueva o reanudada,
// /reload-plugins, el modo prueba, /clear), lo mismo: en pausa, no se borra (tarea 333, a petición del propietario).
// Se borra solo con Abandonar, con «Hecho» en la lista terminada, al salir el panel operativo y con «Ahora no» o «No,
// y no vuelvas a preguntar» en un menú. Borrar es dejar el archivo sin pasos, que el panel y incorporacion.py leen
// como sin progreso.
export const ORDEN_CONTINUAR = 'continúa la incorporación a la SF'
async function hayIncorporacion($: $): Promise<string | null> {
  const ruta = await rutaIncorporacion($)
  if (!ruta) return null
  return (await leerIncorporacion($, await raizSesion($)).catch(() => null)) ? ruta : null
}
// Borrar una incorporación a medias no pierde lo respondido (tarea 366): antes se copia a su .guardada.json, que
// `incorporacion.py ver` menciona y `recuperar` trae. Una terminada no se guarda, y Abandonar lo borra todo, también
// lo guardado antes (`guardar: false`): es una decisión expresa del propietario (decisión 286).
export const guardadaIncorporacion = (ruta: string) => ruta.replace(/\.json$/, '.guardada.json')
export async function borrarIncorporacion($: $, { guardar = true }: { guardar?: boolean } = {}): Promise<void> {
  const ruta = await hayIncorporacion($)
  if (!ruta) return
  const inc = await leerIncorporacion($, await raizSesion($)).catch(() => null)
  if (!guardar) {
    if (await $.fs.exists(guardadaIncorporacion(ruta))) await $.fs.write(guardadaIncorporacion(ruta), '{}\n')
  } else if (inc && !terminada(inc) && inc.pasos.some(p => p.respuesta)) {
    const { pausa: _p, recargar: _r, retomar: _t, ...d } = await leerJson($, ruta)
    await $.fs.write(guardadaIncorporacion(ruta), JSON.stringify(d, null, 2) + '\n')
  }
  await $.fs.write(ruta, '{}\n')
}
export async function pausarIncorporacion($: $): Promise<void> {
  const ruta = await hayIncorporacion($)
  if (!ruta) return
  const d = await leerJson($, ruta)
  // Con una recarga pedida o en marcha, no es una pausa: la incorporación sigue sola tras recargar (tarea 366).
  if (d.pausa === true || d.recargar === true || typeof d.retomar === 'number' || !(typeof d.actual === 'number' && d.actual > 0)) return
  await $.fs.write(ruta, JSON.stringify({ ...d, pausa: true }, null, 2) + '\n')
}
// Mientras corre un turno del principal, la incorporación no está en pausa: el menú que espera respuesta es parte del
// turno (tarea 366: el panel decía «En pausa» con un menú abierto). Se quita al empezar el turno.
export async function reanudarIncorporacion($: $): Promise<boolean> {
  const ruta = await hayIncorporacion($)
  if (!ruta) return false
  const d = await leerJson($, ruta)
  if (d.pausa !== true) return false
  const { pausa: _p, ...resto } = d
  await $.fs.write(ruta, JSON.stringify(resto, null, 2) + '\n')
  return true
}

// ── Recargar los plugins sin que el propietario escriba la orden (tarea 366) ──
// Cuando la incorporación necesita la versión instalada de la SF (está instalada una más nueva que la que corre),
// Claude lo pide con `incorporacion.py recargar` ("recargar": true). Al acabar ese turno, el mod lanza /reload-plugins
// (Claude Code lo hace en cuanto la sesión queda libre) y deja "retomar" con la hora. Quien lo vea primero pasa a
// Claude «continúa la incorporación a la SF» y lo quita: el propietario no escribe nada.
// - El mod recargado, al cargarse (session.start), si la recarga cambió su código.
// - Si no lo cambió, el mismo mod, RESPALDO_RECARGA_MS después de ejecutarse /reload-plugins: Claude Code solo vuelve a
//   cargar (y a lanzar session.start) los módulos que han cambiado, y la incorporación se quedaba parada (tarea 371:
//   en la app de escritorio, con el código del mod ya al día y solo las skills y herramientas por recargar). Si la
//   recarga lo cambió, el mod viejo ya no está y su temporizador no salta; si saltara, "retomar" ya no está.
export const RETOMAR_HASTA_MS = 10 * 60_000
export const RESPALDO_RECARGA_MS = 3000
// `alRedibujar`: redibuja el panel cuando cambia lo que enseña (retomada, o en pausa si no se pudo recargar).
export async function recargarSiPedido($: $, alRedibujar?: () => void): Promise<boolean> {
  const ruta = await hayIncorporacion($)
  if (!ruta) return false
  const d = await leerJson($, ruta)
  if (d.recargar !== true) return false
  const { recargar: _r, pausa: _p, ...resto } = d
  await $.fs.write(ruta, JSON.stringify({ ...resto, retomar: await $.clock.now() }, null, 2) + '\n')
  void lanzar($, 'reload-plugins', '').then(async hecha => {
    // Sin recarga, en pausa, con Continuar: el aviso de que no se pudo lanzar ya lo da `lanzar`.
    if (!hecha) {
      const { retomar: _t, ...sin } = await leerJson($, ruta)
      await $.fs.write(ruta, JSON.stringify(sin, null, 2) + '\n')
      await pausarIncorporacion($)
      alRedibujar?.()
      return
    }
    $.clock.after(RESPALDO_RECARGA_MS, () => {
      void retomarIncorporacion($, 0)
        .then(r => {
          if (r) alRedibujar?.()
        })
        .catch(err => $.ui.log(`retomar la incorporación tras recargar: ${String(err)}`, { to: 'debug' }))
    })
  })
  return true
}
// Con "retomar" reciente (hace menos de RETOMAR_HASTA_MS), lo quita y, `espera` ms después, pasa a Claude
// ORDEN_CONTINUAR. Sin él, o pasado el plazo, no hace nada (lo de hace mucho lo quita) y devuelve false.
async function retomarIncorporacion($: $, espera: number): Promise<boolean> {
  const ruta = await hayIncorporacion($)
  if (!ruta) return false
  const d = await leerJson($, ruta)
  if (typeof d.retomar !== 'number') return false
  const { retomar, pausa: _p, recargar: _r, ...resto } = d
  await $.fs.write(ruta, JSON.stringify(resto, null, 2) + '\n')
  if ((await $.clock.now()) - (retomar as number) > RETOMAR_HASTA_MS) return false
  const pasar = () => void encargarAClaude($, ORDEN_CONTINUAR).catch(err => $.ui.log(`retomar la incorporación: ${String(err)}`, { to: 'debug' }))
  if (espera > 0) $.clock.after(espera, pasar)
  else pasar()
  return true
}
// Al cargarse el mod: tras una recarga pedida (hace menos de RETOMAR_HASTA_MS), la incorporación sigue sola; si no,
// queda en pausa, como siempre (decisión 258).
export async function alCargarIncorporacion($: $): Promise<'retomada' | 'pausa' | null> {
  if (!(await hayIncorporacion($))) return null
  if (await retomarIncorporacion($, 1500)) return 'retomada'
  await pausarIncorporacion($)
  return 'pausa'
}
// Una incorporación terminada (todos sus pasos anotados, ninguno en curso) se queda en el panel hasta que el proyecto
// tiene su panel operativo (`conSf`: .sf/proyecto.json válido); entonces, al empezar el siguiente turno del principal,
// la borra el mod: así el propietario ve Aplicar y Comprobación marcados y repasa la lista junto al panel nuevo. La
// skill ya no la borra al terminar. Sin panel operativo (simulada, o diagnosticar sin SF), sigue hasta Abandonar
// (tarea 333, norma del propietario).
export const terminada = (inc: { actual: number; pasos: { respuesta: string | null }[] }) => inc.actual === 0 && inc.pasos.every(p => !!p.respuesta)
export async function cerrarIncorporacionTerminada($: $, conSf: boolean): Promise<boolean> {
  if (!conSf) return false
  const inc = await leerIncorporacion($, await raizSesion($)).catch(() => null)
  if (!inc || !terminada(inc)) return false
  await borrarIncorporacion($)
  return true
}
// Las respuestas de un menú del principal: con un no a incorporar, se borra el progreso.
export async function menuEnIncorporacion($: $, respuestas: unknown): Promise<void> {
  if (!respuestas || typeof respuestas !== 'object') return
  const no = Object.values(respuestas as Record<string, unknown>).some(v => typeof v === 'string' && (v.trim().startsWith(AHORA_NO) || v.trim().startsWith(NUNCA_AQUI)))
  if (no) await borrarIncorporacion($)
}

// Las reglas y la orquestación del proyecto de la sesión, con el momento en que se entregan.
export async function textoReglas($: $, momento: string): Promise<string | null> {
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
