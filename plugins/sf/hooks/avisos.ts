import { atom, read, update } from 'claude-code'
import type { Evento } from '../types'
import { leerPeticiones, leerSalidas, raizSesion } from './lectura'
import type { $ } from './lectura'
import { emergente } from './emergentes'

// ── Avisos del panel (tarea 228) ──
// Con cada mensaje del propietario, el mod añade al contexto lo que él ha cambiado en la cola desde el panel desde el
// mensaje anterior: Claude no depende de acordarse de consultar la cola. Sale del historial de cada tarea (los eventos
// con via «panel»), en la cola y en .sf/historial.jsonl. Sin cambios, nada.

type Tarea = { id: number; historial: Evento[] }
export type CambioPanel = { id: number; evento: string; detalle: string | null; fecha: number }

// Lo que no se avisa: lo que el panel ya pasa a Claude por su cuenta (el cierre fallido) o no cambia nada que Claude
// use (limpiar Cerradas), o ya dice otro evento (absorbida, en la fusión; nacida, en la separación; la recogida del
// subagente, en el cierre o el descarte).
const CALLADOS = new Set(['cierre-fallido', 'limpiada', 'absorbida', 'nacida', 'recogida', 'recogida-con-avisos'])

// Los cambios del panel con fecha en [desde, hasta), por orden de fecha y sin repetir (una tarea reabierta puede estar
// en la cola y en historial.jsonl).
export function cambiosDelPanel(tareas: Tarea[], desde: number, hasta: number): CambioPanel[] {
  const vistos = new Set<string>()
  const cambios: CambioPanel[] = []
  for (const t of tareas)
    for (const e of t.historial) {
      if (e.via !== 'panel' || e.fecha === null || e.fecha < desde || e.fecha >= hasta || CALLADOS.has(e.evento)) continue
      const clave = `${String(t.id)}|${e.evento}|${String(e.fecha)}|${e.detalle ?? ''}`
      if (vistos.has(clave)) continue
      vistos.add(clave)
      cambios.push({ id: t.id, evento: e.evento, detalle: e.detalle, fecha: e.fecha })
    }
  return cambios.sort((a, b) => a.fecha - b.fecha || a.id - b.id)
}

// Cada evento, como frase corta; el detalle, solo donde se lee bien (el texto de un paso, el tipo, los números).
const FRASES: Record<string, (n: string, d: string) => string> = {
  creada: n => `nueva la ${n}`,
  'en-curso': n => `la ${n}, en curso`,
  'en-cola': n => `la ${n}, en cola`,
  rama: n => `la ${n}, con rama`,
  paso: (n, d) => `la ${n}, ${frasePaso(d)}`,
  renombrada: n => `renombrada la ${n}`,
  tipo: (n, d) => `la ${n}, de tipo ${d.split(' ')[0] || '?'}`,
  redescrita: n => `redescrita la ${n}`,
  subagente: n => `la ${n}, con subagente`,
  informe: n => `informe del subagente de la ${n}`,
  listo: n => `la ${n}, lista para probar`,
  comprobado: n => `la ${n}, comprobada por Claude`,
  probar: n => `la ${n}, en prueba`,
  observando: n => `la ${n}, en observación: la estás mirando`,
  seguir: n => `la ${n}, sigue en observación`,
  cerrada: n => `cerrada la ${n}`,
  'push-fallido': n => `la ${n}, sin push de develop`,
  'a-observacion': n => `la ${n}, a observación`,
  reobservada: n => `la ${n}, de nuevo en observación`,
  descartada: n => `descartada la ${n}`,
  revertida: n => `revertida la ${n}`,
  reabierta: n => `reabierta la ${n}`,
  eliminada: n => `eliminada la ${n}`,
  'a-propuesta': (n, d) => `la ${n}, a propuesta${d ? ` (${d.split(' ')[0]!})` : ''}`,
  restaurada: n => `restaurada la ${n}`,
  fusion: (n, d) => (d.startsWith('absorbe ') ? `la ${n} absorbe la ${d.slice(8)}` : `fusionada la ${n}`),
  separada: (n, d) => (d ? `separados de la ${n} los ${d}` : `separados pasos de la ${n}`),
}

// «añadido 3: texto», «2 hecho: texto», «quitado 3: texto» → «paso añadido: «texto»», «paso 2 hecho», «paso 3 quitado».
function frasePaso(d: string): string {
  const m = /^(añadido|quitado) \d+: (.*)$/s.exec(d)
  if (m) return m[1] === 'añadido' ? `paso añadido: «${m[2]!}»` : `paso quitado: «${m[2]!}»`
  const e = /^(\d+) ([\w-]+):/.exec(d)
  return e ? `paso ${e[1]!} ${e[2]!.replace('-', ' ')}` : 'pasos cambiados'
}

// Un cambio en pocas palabras; un evento sin frase, solo su nombre.
const frase = (c: CambioPanel) => FRASES[c.evento]?.(String(c.id), c.detalle ?? '') ?? `la ${String(c.id)}, ${c.evento}`

// El worktree y la rama del último subagente de la tarea, de su evento «subagente» («worktree · rama»); null sin él.
export function subagenteDe(h: Evento[]): string | null {
  for (let i = h.length - 1; i >= 0; i--) if (h[i]!.evento === 'subagente') return h[i]!.detalle ?? ''
  return null
}

// La recogida del último subagente que anotó cola.py al cerrar o descartar (tarea 246): «recogida», todo quitado;
// «recogida-con-avisos», con lo que queda o se perdió en el detalle. null sin ella (un cola.py anterior).
export function recogidaDe(h: Evento[]): Evento | null {
  for (let i = h.length - 1; i >= 0; i--) {
    const e = h[i]!
    if (e.evento === 'recogida' || e.evento === 'recogida-con-avisos') return e
    if (e.evento === 'subagente') return null
  }
  return null
}

// El texto del aviso, o null sin cambios. Tras un cierre con la C o un descarte de una tarea que tuvo subagente, pide
// pararlo: el panel no puede. Su worktree y su rama auxiliar ya los quitó cola.py; si algo quedó, lo dice, y sin
// recogida anotada (un cola.py anterior) pide quitarlos también.
export function avisoPanel(cambios: CambioPanel[], tareas: Tarea[]): string | null {
  if (!cambios.length) return null
  let aviso = `Desde el panel: ${cambios.map(frase).join('; ')}.`
  const cerradas = [...new Set(cambios.filter(c => c.evento === 'cerrada' || c.evento === 'descartada').map(c => c.id))]
  for (const id of cerradas) {
    const h = tareas.find(t => t.id === id)?.historial ?? []
    const sub = subagenteDe(h)
    if (sub === null) continue
    const n = String(id)
    const r = recogidaDe(h)
    if (r?.evento === 'recogida') aviso += ` Detén el subagente de la ${n}: cola.py ya quitó su worktree y su rama auxiliar.`
    else if (r) aviso += ` Detén el subagente de la ${n}; al recogerlo, cola.py avisó: ${r.detalle ?? '?'}.`
    else aviso += ` Recoge el subagente de la ${n}${sub ? ` (${sub})` : ''}: páralo, quita su worktree y borra su rama auxiliar.`
  }
  return aviso
}

// Lee la cola y historial.jsonl y devuelve el aviso de lo cambiado desde el panel en [desde, hasta). Si no puede
// leer alguno de los dos (la cola a medio escribir, por ejemplo), falla: el aviso no se da por dado (tarea 285).
export async function leerAvisoPanel($: $, desde: number, hasta: number): Promise<string | null> {
  const raiz = await raizSesion($)
  const cola = await leerPeticiones($, raiz)
  if (cola.error) throw new Error(cola.error)
  const tareas: Tarea[] = [...cola.peticiones, ...(await leerSalidas($, raiz, desde))]
  return avisoPanel(cambiosDelPanel(tareas, desde, hasta), tareas)
}

// Hasta dónde (ms) se ha avisado a Claude de los cambios del panel: el último mensaje que lo llevó (del propietario o
// un encargo del panel) o, si no hay ninguno en esta sesión, su inicio o el último /clear. /reload-plugins no lo
// reinicia, para no perder lo cambiado antes de recargar y aún sin avisar (tarea 285).
export const avisadoPanel = atom({ plugin: 'sf', key: 'avisadoPanel' } as const, 0)
// También en $.store, con el id de la sesión: $.state se vacía al cambiar de plugin (otra versión, el modo prueba), y
// una versión anterior del mod, cargada entre medias con el modo prueba, pone el atom en la hora de su carga y reescribe
// .sf/subagentes.json sin los campos que no conoce; su clave de $.store no la toca (tarea 285, reabierta).
export const CLAVE_AVISADO = 'avisadoPanel'
type Avisado = { sesion: string; avisado: number }

// Por segundos enteros, como las fechas de cola.py: un cambio del mismo segundo que el mensaje va en el siguiente.
const segundo = (ms: number) => Math.floor(ms / 1000) * 1000

async function fijarAvisado($: $, cambio: (v: number) => number): Promise<void> {
  const antes = await read($, avisadoPanel)
  const v = cambio(antes)
  if (v === antes) return
  await update($, avisadoPanel, () => v)
  const valor: Avisado = { sesion: await $.session.id(), avisado: v }
  await $.store.set(CLAVE_AVISADO, valor).catch(() => undefined)
}

// Lo más atrás que llegan los avisos del panel al cargarse el mod: al reanudar una sesión de hace días, lo cambiado
// desde entonces ya está en la cola, y avisarlo entero (con «Recoge el subagente…» de tareas cerradas hace días) solo
// tapa lo que importa (tarea 351).
export const VENTANA_AVISOS = 12 * 3600_000

// Al cargarse el mod: tras /clear (nueva), los avisos cuentan desde ahora; si no, siguen desde el último dado en esta
// sesión, el de $.store (manda sobre el atom, que una versión anterior pudo reiniciar) o el del atom, con
// VENTANA_AVISOS como mucho; sin ninguno (la sesión empieza), desde ahora.
export async function cargarAvisosPanel($: $, ahora: number, nueva: boolean): Promise<void> {
  if (nueva) return fijarAvisado($, () => segundo(ahora))
  const g = (await $.store.get(CLAVE_AVISADO).catch(() => undefined)) as Partial<Avisado> | undefined
  const guardado = g && g.sesion === (await $.session.id()) && typeof g.avisado === 'number' && g.avisado > 0 ? g.avisado : 0
  const atomo = await read($, avisadoPanel)
  await update($, avisadoPanel, () => 0)
  const desde = guardado || atomo
  await fijarAvisado($, () => (desde && desde >= ahora - VENTANA_AVISOS ? desde : segundo(ahora)))
}

// Toma el aviso de lo cambiado desde el panel desde el último dado, y lo da por dado solo si lo ha podido leer; con
// devolver, si el mensaje que lo lleva no llega a enviarse, vuelve a quedar pendiente. null sin cambios o sin leer.
export async function tomarAvisoPanel($: $): Promise<{ aviso: string | null; devolver: () => Promise<void> }> {
  const hasta = segundo(await $.clock.now())
  // Con el atom a 0, el mod aún no lo ha cargado (el estado se acaba de vaciar al cambiar de plugin): se carga ahora,
  // del $.store de esta sesión o desde ahora; con 0 se avisaría de todo lo hecho desde el panel (tarea 350).
  if ((await read($, avisadoPanel)) === 0) await cargarAvisosPanel($, hasta, false)
  const desde = await read($, avisadoPanel)
  const aviso = await leerAvisoPanel($, desde, hasta).catch(() => undefined)
  if (aviso === undefined) return { aviso: null, devolver: async () => undefined }
  await fijarAvisado($, v => Math.max(v, hasta))
  return { aviso, devolver: () => fijarAvisado($, v => (v === hasta ? desde : v)) }
}

// Un encargo del panel a Claude, como si lo escribiera el propietario (R, T y C fallidas, «?», /sf_paso, TURBO…). El
// hook prompt.submit del mod no ve los prompts que envía el propio mod: el aviso de lo cambiado desde el panel va
// aquí, tras el encargo; si no, se quedaría sin dar hasta el siguiente mensaje del propietario (tarea 285).
// El motor puede no admitir el encargo sin lanzar error: responde { drop }. Pasa tras interrumpir a Claude con Esc (en
// un menú o mientras trabaja): hasta que el propietario escribe algo, Claude Code no deja que un plugin le pase
// mensajes. Entonces el encargo se deja escrito en el prompt (si está vacío), para enviarlo con Intro, y se dice; el
// aviso del panel queda para el siguiente mensaje (tarea 333: Continuar no hacía nada tras Esc).
export async function encargarAClaude($: $, text: string): Promise<void> {
  const { aviso, devolver } = await tomarAvisoPanel($)
  let r: Awaited<ReturnType<typeof $.prompt.submit>>
  try {
    r = await $.prompt.submit({ text: aviso ? `${text}\n\n${aviso}` : text, asUser: true })
  } catch (err) {
    await devolver()
    throw err
  }
  if (!r || !('drop' in r) || r.drop === undefined) return
  await devolver()
  $.ui.log(`encargo a Claude no admitido: ${r.drop}`, { to: 'debug' })
  const borrador = await $.prompt.read().catch(() => ({ text: '' }))
  const escrito = !borrador.text.trim() && (await $.prompt.fill({ text }).catch(() => ({ isFilled: false }))).isFilled
  emergente(
    $,
    escrito
      ? 'Claude Code no me deja pasárselo ahora (tras Esc espera tu mensaje): te lo dejo escrito en el prompt; pulsa Intro.'
      : `Claude Code no me deja pasárselo ahora (tras Esc espera tu mensaje): escríbele «${text}».`,
    false,
  )
}
