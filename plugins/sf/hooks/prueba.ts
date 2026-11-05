import { atom, read, update } from 'claude-code'
import type { EngineInterface } from 'claude-code'
import type { Prueba } from '../types'
import { emergente } from './emergentes'
import { normal } from './control'
import { lanzar } from './identidad'
import { MARCA_SF } from './constantes'
import { raizSesion } from './lectura'

// Valores de estado del mod: el motor exige declararlos en el archivo que los usa; con el mismo
// plugin y clave, son el mismo valor en todos los archivos.
// disponible: el catálogo local está registrado en este proyecto; pedido: los ajustes piden la copia de trabajo.
const prueba = atom({ plugin: 'sf', key: 'prueba' } as const, { disponible: false, pedido: false } as Prueba)

// Modo prueba (solo en la SF): este proyecto carga la copia de trabajo de plugins/sf, desde el catálogo local
// softwarefactory-dev (.claude-plugin/marketplace.json en la carpeta que contiene el repositorio de la SF), en lugar
// del plugin publicado.
// Se cambia en .claude/settings.local.json y se aplica con /reload-plugins. Al entrar y al cerrar la sesión,
// siempre desactivado (decisión del propietario, 2026-10-28).
export const AJUSTES_LOCALES = '.claude/settings.local.json'
export const CATALOGO_PRUEBA = 'softwarefactory-dev'
export const SF_PRUEBA = `sf@${CATALOGO_PRUEBA}`
export const SF_PUBLICADO = 'sf@softwarefactory'
export const COLOR_PRUEBA = '#f97316'

export async function leerAjustes($: EngineInterface): Promise<Record<string, any> | null> {
  try {
    return JSON.parse(await $.fs.read(AJUSTES_LOCALES)) as Record<string, any>
  } catch {
    return null
  }
}

export async function leerPrueba($: EngineInterface): Promise<void> {
  const a = await leerAjustes($)
  const disponible = Boolean(a?.extraKnownMarketplaces?.[CATALOGO_PRUEBA])
  const pedido = disponible && a?.enabledPlugins?.[SF_PRUEBA] === true
  await update($, prueba, () => ({ disponible, pedido }))
}

// La sesión está en el repositorio fuente de la SF. Fuera de él (una carpeta de prueba con el catálogo local, o un
// proyecto), el mod no apaga el modo prueba ni escribe en .sf/: manda lo que diga .claude/settings.local.json (tarea 338).
export async function enLaFuente($: EngineInterface): Promise<boolean> {
  return $.fs.exists(`${await raizSesion($)}/${MARCA_SF}`).catch(() => false)
}

// Registro de diagnóstico (tarea 183): quién cambia el modo prueba y cuándo, en .sf/prueba.log, fuera de git.
// Solo en la SF, con el catálogo local registrado: en otra carpeta no escribe nada.
export const REGISTRO_PRUEBA = '.sf/prueba.log'
export async function anotarPrueba($: EngineInterface, texto: string): Promise<void> {
  try {
    if (!(await leerAjustes($))?.extraKnownMarketplaces?.[CATALOGO_PRUEBA] || !(await enLaFuente($))) return
    let antes = ''
    try {
      antes = await $.fs.read(REGISTRO_PRUEBA)
    } catch {}
    const linea = `${new Date(await $.clock.now()).toISOString()} ${texto} · sesión ${await $.session.id()} · ${$.plugin.root}\n`
    await $.fs.write(REGISTRO_PRUEBA, (antes + linea).split('\n').slice(-200).join('\n'))
  } catch {}
}

// Pide la copia de trabajo (o la publicada) en los ajustes locales; solo si el catálogo local está registrado.
export async function ponerPrueba($: EngineInterface, activar: boolean, motivo = 'sin motivo'): Promise<void> {
  const a = await leerAjustes($)
  if (!a?.extraKnownMarketplaces?.[CATALOGO_PRUEBA]) return
  if (a.enabledPlugins?.[SF_PRUEBA] !== activar || a.enabledPlugins?.[SF_PUBLICADO] !== !activar) {
    a.enabledPlugins = { ...(a.enabledPlugins ?? {}), [SF_PRUEBA]: activar, [SF_PUBLICADO]: !activar }
    await $.fs.write(AJUSTES_LOCALES, JSON.stringify(a, null, 2) + '\n')
    await anotarPrueba($, `modo prueba ${activar ? 'encendido' : 'apagado'} por ${motivo}`)
  }
  await leerPrueba($)
}

// /reload-plugins vuelve a pasar por session.start: el modo prueba se apaga solo la primera vez en cada sesión.
// La sesión que ya lo apagó queda en .sf/prueba.json (fuera de git), que sobrevive al cambio de plugin.
export const MARCA_PRUEBA = '.sf/prueba.json'
export async function apagarAlEntrar($: EngineInterface): Promise<void> {
  if (!(await enLaFuente($))) return leerPrueba($)
  const id = await $.session.id()
  let anterior: string | null = null
  try {
    anterior = (JSON.parse(await $.fs.read(MARCA_PRUEBA)) as { sesion?: string }).sesion ?? null
  } catch {}
  await anotarPrueba($, `arranque: marca ${anterior ?? 'ninguna'}${anterior === id ? ', la misma sesión' : ''}`)
  if (anterior === id) return leerPrueba($)
  await ponerPrueba($, false, 'el arranque de una sesión nueva')
  if (!(await read($, prueba)).disponible) return
  await $.fs.write(MARCA_PRUEBA, JSON.stringify({ sesion: id }) + '\n')
  // La sesión arrancó con la copia de trabajo (la anterior se cerró sin apagarlo): vuelve al publicado.
  if (await desdeCopia($)) void lanzar($, 'reload-plugins', '')
}

// Al cerrar la sesión, el modo prueba se desactiva, solo en la SF: la siguiente entra con el plugin publicado.
export async function apagarAlCerrar($: EngineInterface, motivo: string): Promise<void> {
  if (!(await enLaFuente($))) return
  await anotarPrueba($, `session.end: ${motivo}`)
  await ponerPrueba($, false, `session.end (${motivo})`)
}

// El turno de Claude en curso (el del principal, no los de los subagentes). Claude Code guarda el /reload-plugins
// que lanza el mod hasta que la sesión queda libre (tarea 185): mientras, sigue cargado el plugin de antes.
let turno: string | null = null
export function marcarTurno(id: string | null): void {
  turno = id
}

// El clic en la etiqueta o /sf_prueba: cambia los ajustes y lanza /reload-plugins, que aplica el cambio. Desde /sf_prueba,
// con un temporizador: el motor no deja lanzar un comando desde el hook de una orden. Devuelve qué ha hecho y, con
// Claude trabajando, lo avisa: la recarga espera a que acabe su turno.
export async function cambiarPrueba($: EngineInterface, activar: boolean, motivo = 'la etiqueta PRUEBA', diferido = false): Promise<string> {
  await ponerPrueba($, activar, motivo)
  const texto = `Modo prueba ${activar ? 'encendido' : 'apagado'}: recargo ${turno ? 'al acabar el turno de Claude' : 'ahora'}.`
  if (turno) emergente($, `${texto} Mientras, sigue este panel.`, false)
  if (diferido) $.clock.after(0, () => void lanzar($, 'reload-plugins', ''))
  else void lanzar($, 'reload-plugins', '')
  return texto
}

// El mod se ejecuta desde la copia de trabajo: el catálogo local la carga en su sitio, sin copiarla a la caché. Se
// reconoce porque la carpeta del plugin está en un repositorio, dos niveles por debajo de su raíz (plugins/sf), y no
// por el nombre de la carpeta: se mira con $.fs, que una prueba simula, y vale en cualquier clon o worktree (tarea 307).
export async function desdeCopia($: EngineInterface): Promise<boolean> {
  const raiz = normal($.plugin.root)
  const repo = raiz.replace(/\/[^/]+\/[^/]+$/, '')
  return repo !== raiz && (await $.fs.exists(`${repo}/.git`).catch(() => false))
}
