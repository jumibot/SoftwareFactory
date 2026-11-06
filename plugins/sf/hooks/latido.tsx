import { atom, read, update } from 'claude-code'
import { CARPETA_COPIAS, PANEL } from './constantes'
import { entregaReglas, sinSf, textoReglas } from './contexto'
import { carpetaClaude, claveIncorporacion, leerJson, raizSesion } from './lectura'
import type { $ } from './lectura'
import { emergente } from './emergentes'

// ── Una sola sesión con la SF por proyecto (decisión 193) ──
// Solo una sesión de cada proyecto lleva la SF: la cola, los subagentes, sus avisos, las órdenes /sf_* y el panel. La
// que la tiene deja un latido cada minuto en ~/.claude/sf/latido-<clave de la carpeta>.json (fuera del proyecto: no
// hay que ignorarlo en git), con el id de la sesión y la hora. Al arrancar (y tras un /clear), una sesión toma la SF si
// no hay latido, si es suyo o si tiene más de CADUCA; si no, arranca con la SF apagada y lo avisa. /sf_forzar_activa
// la toma aunque otra la tenga: esa otra lo ve en su siguiente latido y se apaga. /sf_forzar_inactiva la apaga en la
// sesión donde se escribe, que suelta el latido y deja de darlo. Sin SF en la carpeta, nada de esto aplica.
// Una sesión apagada no toma la SF sola aunque la otra deje de latir, tampoco tras un /clear o un /reload-plugins: lo
// avisa y propone /sf_forzar_activa (decisión 295). Apagada (por otra o con /sf_forzar_inactiva) es Claude Code sin
// más: sin panel ni caja, sin control de proyecto, sin regla en el prompt de sistema y sin contexto de la SF; solo el
// latido y sus avisos (decisiones 296 y 297). Que se trabaja sin la SF se avisa una vez, al apagarse.

export const CADA_LATIDO = 60_000
export const CADUCA = 3 * 60_000
export const PREFIJO_LATIDO = 'latido-'

// 'activa': la lleva esta sesión; 'apagada': la tiene otra; 'inactiva': apagada aquí con /sf_forzar_inactiva; null:
// sin decidir o sin SF (se trata como activa: todo sigue como antes de la decisión 193).
export type SesionSf = 'activa' | 'apagada' | 'inactiva'
type Latido = { carpeta: string; sesion: string; latido: number }

const sesionSf = atom({ plugin: 'sf', key: 'sesionSf' } as const, null as SesionSf | null)
// Los ids de sesión que esta sesión ha escrito en el latido: tras un /clear el motor puede darle otro id, y el latido
// con el de antes sigue siendo suyo.
const idsPropios = atom({ plugin: 'sf', key: 'latidoIds' } as const, [] as string[])
// Lo que hay que decir a Claude con el siguiente mensaje del propietario: que la SF se ha apagado o activado aquí.
const avisoClaude = atom({ plugin: 'sf', key: 'avisoSesionSf' } as const, null as string | null)
// Ya se dijo, en esta sesión apagada, que la que tenía la SF dejó de dar latido.
const caducadaDicha = atom({ plugin: 'sf', key: 'latidoCaducadoDicho' } as const, false)
// El mismo valor que en contexto.ts: las reglas y la orquestación ya están en la conversación.
const reglasDadas = atom({ plugin: 'sf', key: 'reglasDadas' } as const, false)
// Las sesiones apagadas con /sf_forzar_inactiva, por id y con su fecha: en $.store, que sobrevive a un cambio de
// plugin (/reload-plugins con otra versión o el modo prueba), donde $.state empieza de cero.
const CLAVE_INACTIVAS = 'sesionesInactivas'
// Las sesiones apagadas porque otra tiene la SF, igual: tras un cambio de plugin siguen apagadas y no la toman solas.
const CLAVE_APAGADAS = 'sesionesApagadas'
const SEMANA = 7 * 24 * 3600_000

export const AVISO_APAGADA = 'SF apagada en esta sesión: otra sesión de este proyecto la tiene activa, y aquí se trabaja sin la SF. Para traerla aquí, /sf_forzar_activa.'
export const AVISO_PERDIDA = 'SF apagada en esta sesión: otra sesión de este proyecto la ha tomado con /sf_forzar_activa, y aquí se trabaja sin la SF.'
export const AVISO_CADUCADA = 'La sesión que tenía la SF ya no da latido: /sf_forzar_activa para tomarla en esta.'
// Al apagarse en mitad de la conversación, Claude aún tiene las reglas y la orquestación: que las deje, una vez.
const DEJALA =
  'Desde ahora deja las reglas y la orquestación de la SF que se te dieron: no lleves la cola (.sf/peticiones.json), ni tareas, ni subagentes de la SF. Esta sesión es Claude Code sin más.'
const CONTEXTO_PERDIDA = `Software Factory apagada en esta sesión: otra sesión de este proyecto la ha tomado con /sf_forzar_activa. ${DEJALA}`
const CONTEXTO_INACTIVA = `Software Factory apagada en esta sesión con /sf_forzar_inactiva. ${DEJALA}`
const CONTEXTO_CADUCADA =
  'La sesión que tenía la Software Factory ha dejado de dar latido; esta sigue sin la SF (decisión 295). Di al propietario en una línea que puede traerla aquí con /sf_forzar_activa.'
const CONTEXTO_ACTIVADA = 'Software Factory activa en esta sesión con /sf_forzar_activa: la otra sesión del proyecto que la tuviera se apaga en su siguiente latido (un minuto como mucho).'

// Una petición en curso de decidir: session.start y el SessionStart de los ajustes pueden llegar a la vez.
let decidiendo: Promise<SesionSf | null> | null = null

async function rutaLatido($: $): Promise<string | null> {
  const claude = await carpetaClaude($)
  if (!claude) return null
  return `${claude}/${CARPETA_COPIAS}/${PREFIJO_LATIDO}${claveIncorporacion(await raizSesion($))}.json`
}

async function leerLatido($: $, ruta: string): Promise<Latido | null> {
  try {
    if (!(await $.fs.exists(ruta))) return null
    const d = await leerJson($, ruta)
    return typeof d.sesion === 'string' && typeof d.latido === 'number' ? { carpeta: String(d.carpeta ?? ''), sesion: d.sesion, latido: d.latido } : null
  } catch {
    return null
  }
}

async function escribirLatido($: $, ruta: string, latido: number): Promise<void> {
  const id = await $.session.id()
  await $.fs.write(ruta, JSON.stringify({ carpeta: await raizSesion($), sesion: id, latido }) + '\n')
  if (!(await read($, idsPropios)).includes(id)) await update($, idsPropios, v => [...v, id].slice(-10))
}

async function esPropio($: $, l: Latido): Promise<boolean> {
  return l.sesion === (await $.session.id()) || (await read($, idsPropios)).includes(l.sesion)
}

async function marcadas($: $, clave: string): Promise<Record<string, number>> {
  const g = (await $.store.get(clave).catch(() => undefined)) as Record<string, number> | undefined
  return g && typeof g === 'object' ? g : {}
}
async function marcar($: $, clave: string, si: boolean): Promise<void> {
  const id = await $.session.id()
  const antes = await marcadas($, clave)
  if (!si && antes[id] === undefined) return
  const ahora = await $.clock.now()
  const nuevas = Object.fromEntries(Object.entries(antes).filter(([k, f]) => k !== id && ahora - f < SEMANA))
  if (si) nuevas[id] = ahora
  await $.store.set(clave, nuevas).catch(() => undefined)
}
async function inactivas($: $): Promise<Record<string, number>> {
  return marcadas($, CLAVE_INACTIVAS)
}
async function marcarInactiva($: $, si: boolean): Promise<void> {
  await marcar($, CLAVE_INACTIVAS, si)
}

// Cambia el estado solo si es otro: cada cambio de un valor de estado vuelve a pintar el panel y la caja. Apagada por
// otra, queda anotado en $.store, para que un cambio de plugin no la encienda sola (decisión 295).
// Al apagarse, el panel se cierra: sin la SF activa no hay panel (decisión 296).
async function fijar($: $, s: SesionSf | null): Promise<void> {
  const antes = await read($, sesionSf)
  if (antes !== s) await update($, sesionSf, () => s)
  if (s !== null && (antes !== s || s === 'apagada')) await marcar($, CLAVE_APAGADAS, s === 'apagada')
  const apagadaAhora = s === 'apagada' || s === 'inactiva'
  if (apagadaAhora && antes !== 'apagada' && antes !== 'inactiva' && (await $.ui.panes()).some(p => p.id === PANEL))
    await $.ui.close({ id: PANEL }).catch(() => undefined)
}

// La que la tenía ha dejado de latir, vista desde la apagada: se dice una vez, en un aviso y a Claude con el siguiente
// mensaje; tomarla es cosa del propietario (decisiones 295 y 296).
async function decirCaducada($: $): Promise<void> {
  if (await read($, caducadaDicha)) return
  await update($, caducadaDicha, () => true)
  await update($, avisoClaude, () => CONTEXTO_CADUCADA)
  emergente($, AVISO_CADUCADA, false)
}

// El estado de la SF en esta sesión, sin decidir nada.
export async function sesionSfActual($: $): Promise<SesionSf | null> {
  return read($, sesionSf)
}
// La SF está apagada en esta sesión (por otra o con /sf_forzar_inactiva).
export async function sfApagada($: $): Promise<boolean> {
  const s = await read($, sesionSf)
  return s === 'apagada' || s === 'inactiva'
}

// Decide al arrancar (session.start, tras /clear) si esta sesión toma la SF. Devuelve el estado, o null sin SF.
export async function decidirSesion($: $): Promise<SesionSf | null> {
  if (!decidiendo)
    decidiendo = decidir($).finally(() => {
      decidiendo = null
    })
  return decidiendo
}
// Como decidirSesion, pero solo si aún no se ha decidido (el SessionStart de los ajustes, que puede llegar antes).
export async function asegurarSesion($: $): Promise<SesionSf | null> {
  return decidiendo ?? ((await read($, sesionSf)) ?? (await decidirSesion($)))
}

async function decidir($: $): Promise<SesionSf | null> {
  const ruta = await rutaLatido($)
  if (!ruta || (await sinSf($))) {
    await fijar($, null)
    return null
  }
  const id = await $.session.id()
  if ((await inactivas($))[id] !== undefined) {
    await fijar($, 'inactiva')
    return 'inactiva'
  }
  const ahora = await $.clock.now()
  const l = await leerLatido($, ruta)
  const antes = await read($, sesionSf)
  const propio = !!l && (await esPropio($, l))
  const caducado = !l || ahora - l.latido >= CADUCA
  // Ya apagada (antes de un /clear o de un cambio de plugin): no la toma sola aunque la otra no lata (decisión 295).
  const eraApagada = antes === 'apagada' || (await marcadas($, CLAVE_APAGADAS))[id] !== undefined
  if (propio || (caducado && !eraApagada)) {
    await escribirLatido($, ruta, ahora)
    await fijar($, 'activa')
    return 'activa'
  }
  await fijar($, 'apagada')
  if (caducado) {
    await decirCaducada($)
    return 'apagada'
  }
  if (await read($, caducadaDicha)) await update($, caducadaDicha, () => false)
  // Que se trabaja sin la SF, una vez: al apagarse, no tras un /clear ni un cambio de plugin (decisión 296).
  if (!eraApagada) emergente($, AVISO_APAGADA, false)
  return 'apagada'
}

// El latido de cada minuto (lo lanza el de register.tsx, el mismo que comprueba REFRESCAR). Devuelve si la SF sigue
// activa en esta sesión: si no, ese latido no comprueba ACTUALIZAR ni REFRESCAR.
export async function latirSesion($: $): Promise<boolean> {
  const s = (await read($, sesionSf)) ?? (await decidirSesion($))
  if (s === null) return true
  if (s === 'inactiva') return false
  const ruta = await rutaLatido($)
  if (!ruta) return true
  const ahora = await $.clock.now()
  const l = await leerLatido($, ruta)
  if (s === 'apagada') {
    // La que la tenía ya no late: se dice una vez; tomarla es cosa del propietario, con /sf_forzar_activa (decisión
    // 295). Si vuelve a latir (solo estaba colgada), se podrá volver a avisar si deja de latir otra vez.
    if (!l || ahora - l.latido >= CADUCA) await decirCaducada($)
    else if (await read($, caducadaDicha)) await update($, caducadaDicha, () => false)
    return false
  }
  // Otra sesión la ha tomado (con /sf_forzar_activa, o arrancó cuando esta llevaba más de CADUCA sin latir): se apaga.
  if (l && !(await esPropio($, l)) && ahora - l.latido < CADUCA) {
    await fijar($, 'apagada')
    if (await read($, caducadaDicha)) await update($, caducadaDicha, () => false)
    await update($, avisoClaude, () => CONTEXTO_PERDIDA)
    emergente($, AVISO_PERDIDA, false)
    return false
  }
  await escribirLatido($, ruta, ahora)
  return true
}

// /sf_forzar_activa: la SF pasa a esta sesión; la otra se apaga en su siguiente latido.
export async function forzarActiva($: $): Promise<string> {
  const ruta = await rutaLatido($)
  if (!ruta || (await sinSf($))) return 'Esta carpeta no tiene la SF: no hay nada que activar.'
  const antes = await read($, sesionSf)
  await marcarInactiva($, false)
  await escribirLatido($, ruta, await $.clock.now())
  await fijar($, 'activa')
  if (antes === 'activa' || antes === null) return 'La SF ya estaba activa en esta sesión.'
  // Las reglas y la orquestación, si la sesión arrancó apagada y aún no las tiene (también en la SF, decisión 298).
  const reglas = !(await read($, reglasDadas)) && (await entregaReglas($)) ? await textoReglas($, 'activarse la SF en esta sesión con /sf_forzar_activa').catch(() => null) : null
  if (reglas) await update($, reglasDadas, () => true)
  await update($, avisoClaude, () => [CONTEXTO_ACTIVADA, reglas].filter(Boolean).join('\n\n'))
  return 'SF activa en esta sesión: la otra sesión del proyecto se apaga en su siguiente latido (un minuto como mucho).'
}

// /sf_forzar_inactiva: apaga la SF aquí y suelta el latido, para que otra sesión la tome al arrancar.
export async function forzarInactiva($: $): Promise<string> {
  const ruta = await rutaLatido($)
  if (!ruta || (await sinSf($))) return 'Esta carpeta no tiene la SF: no hay nada que apagar.'
  const antes = await read($, sesionSf)
  await marcarInactiva($, true)
  await fijar($, 'inactiva')
  if (antes === 'inactiva') return 'La SF ya estaba apagada en esta sesión con /sf_forzar_inactiva.'
  const l = await leerLatido($, ruta)
  if (l && (await esPropio($, l))) await escribirLatido($, ruta, 0)
  if (antes !== 'apagada') await update($, avisoClaude, () => CONTEXTO_INACTIVA)
  return 'SF apagada en esta sesión, que sigue como Claude Code sin más: deja de dar latido y otra sesión la toma al arrancar. Para volver: /sf_forzar_activa.'
}

// Al cerrar la sesión: si la tenía, suelta el latido, para que la siguiente que arranque la tome sin esperar.
export async function soltarAlCerrar($: $): Promise<void> {
  if ((await read($, sesionSf)) !== 'activa') return
  const ruta = await rutaLatido($)
  if (!ruta) return
  const l = await leerLatido($, ruta)
  if (l && (await esPropio($, l))) await escribirLatido($, ruta, 0)
}

// Lo que hay que decir a Claude de la SF de esta sesión con el siguiente mensaje del propietario, una vez.
export async function tomarAvisoSesion($: $): Promise<string | null> {
  const a = await read($, avisoClaude)
  if (a !== null) await update($, avisoClaude, () => null)
  return a
}

