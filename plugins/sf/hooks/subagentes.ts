import { atom, read, update } from 'claude-code'
import type { AvisosSubagentes, Peticion, SubagenteVisto } from '../types'
import { PROYECTO } from './constantes'
import { ordenColaClaude } from './python'
import { absorbidas, esperaAbierta, focoGuardado, leerJson, leerPeticiones, leerSubagentes, raizSesion, recuperarVistos } from './lectura'
import type { FocoGuardado } from './lectura'
import { guardarSesion, recordarSesion } from './memoria'
import { recordatorioFoco } from './recordatorio'
import type { $ } from './lectura'
import { emergente } from './emergentes'

// ── Avisos de subagentes (tarea 249) ──
// Con cada mensaje del propietario, al volver un subagente (su notificación o el final del Agent en primer plano), el
// mod añade al contexto de Claude las tareas en curso sin subagente vivo y los subagentes que han terminado sin
// recoger. Solo avisa. Las que no tienen subagente, en cada mensaje mientras falten, en un aviso aparte que va el
// primero y manda lanzarlos antes de nada (tarea 351: al reanudar, un aviso al final de otros no bastó). Los
// terminados, una vez, cuando aparecen: se repite si se resuelve y vuelve, tras un /clear o una compactación (Claude
// ya no lo tiene en el contexto) y en una sesión nueva. Si el motor no da la lista de
// subagentes, no se sabe quién vive: no se avisa de los que faltan. La sesión se reconoce por su id, no por la carga
// del módulo: /reload-plugins, aunque cambie de plugin y vacíe el estado, no la hace nueva (tarea 277).

// Las claves ya avisadas, si aún no se ha avisado nada en una sesión nueva y el id de la sesión.
const avisados = atom({ plugin: 'sf', key: 'avisosSubagentes' } as const, { claves: [], nueva: true } as AvisosSubagentes)

export type AvisoSubagente = { clave: string; texto: string; tarea?: number }

// El último informe anotado de la tarea (ms), o null.
function ultimoInforme(p: Peticion): number | null {
  for (let i = p.historial.length - 1; i >= 0; i--) if (p.historial[i]!.evento === 'informe') return p.historial[i]!.fecha
  return null
}

// Lo que hay que avisar ahora, por tarea en curso: sin subagente vivo (ni trabajando ni esperando), si se tiene la
// lista; o con uno que dejó de trabajar después del último informe anotado («cola.py informe» es recogerlo). Los de
// las tareas que absorbió al fusionarse cuentan como suyos (tarea 426). La que espera a otra aún abierta
// («cola.py espera M N») no pide su subagente hasta que la otra se cierre o pase a observación (tarea 436).
export function avisosSubagentes(peticiones: Peticion[], vistos: Record<string, SubagenteVisto>, conLista: boolean): AvisoSubagente[] {
  const avisos: AvisoSubagente[] = []
  const lista = Object.values(vistos)
  for (const p of peticiones) {
    if (p.estado !== 'en-curso') continue
    const n = String(p.id)
    const tareas = new Set([p.id, ...absorbidas(p)])
    const suyos = lista.filter(v => tareas.has(v.tarea))
    if (suyos.some(v => v.estado === 'trabajando')) continue
    const esperan = suyos.filter(v => v.estado === 'esperando')
    if (!esperan.length) {
      if (conLista && esperaAbierta(p, peticiones) === null) avisos.push({ clave: `sin:${n}`, texto: `la ${n} («Tarea ${n}: …»)`, tarea: p.id })
      continue
    }
    const informe = ultimoInforme(p) ?? -Infinity
    // Por segundos enteros, como las fechas de cola.py.
    if (esperan.some(v => v.visto !== undefined && Math.floor(v.visto / 1000) * 1000 > informe))
      avisos.push({ clave: `fin:${n}`, texto: `el subagente de la ${n} ha terminado: recógelo (revisar el diff, merge --ff-only, \`${ordenColaClaude()} informe ${n}\`, pasos, listo)`, tarea: p.id })
  }
  return avisos
}

// Las que hay que avisar ahora: las que no se habían avisado y, siempre, las que faltan por lanzar (tarea 351); y las
// claves que quedan avisadas: las de ahora (las resueltas salen y vuelven a contar).
export function nuevos(avisos: AvisoSubagente[], claves: string[]): { nuevos: AvisoSubagente[]; claves: string[] } {
  const ya = new Set(claves)
  return { nuevos: avisos.filter(a => a.clave.startsWith('sin:') || !ya.has(a.clave)), claves: avisos.map(a => a.clave) }
}

// Los textos del aviso: el de lanzar los que faltan, imperativo, y el de recoger los terminados; cada uno, null sin
// nada que avisar. En una sesión recién abierta, recuerda que los de la anterior ya no viven.
// tareas: las de los avisos; foco: el guardado en la cola, para el recordatorio del foco (tarea 436).
export type TextosAviso = { lanzar: string | null; recoger: string | null; tareas?: number[]; foco?: FocoGuardado | null }
export function textoAviso(nuevosAvisos: AvisoSubagente[], nueva: boolean): TextosAviso {
  const sin = nuevosAvisos.filter(a => a.clave.startsWith('sin:'))
  const fin = nuevosAvisos.filter(a => !a.clave.startsWith('sin:'))
  return {
    tareas: nuevosAvisos.flatMap(a => (a.tarea === undefined ? [] : [a.tarea])),
    lanzar: sin.length
      ? `ANTES DE NADA, en este turno y antes de contestar: lanza el subagente de cada tarea en curso que no lo tiene: ${sin.map(a => a.texto).join(', ')}.` +
        (nueva ? ' Sesión nueva: los de la anterior ya no viven.' : '')
      : null,
    recoger: fin.length ? `Subagentes: ${fin.map(a => a.texto).join('; ')}.` : null,
  }
}

// Interruptor de .sf/proyecto.json: `automatizaciones.avisos_subagentes`, encendido salvo que valga false. Sin el
// archivo o sin la clave, encendido.
async function encendidos($: $, raiz: string): Promise<boolean> {
  try {
    const a = (await leerJson($, `${raiz}/${PROYECTO}`)).automatizaciones as Record<string, unknown> | undefined
    return a?.avisos_subagentes !== false
  } catch {
    return true
  }
}

// Lee la cola y los subagentes y devuelve los textos del aviso, apuntándolo como avisado; null en lo que no hay nada.
export const SIN_AVISO: TextosAviso = { lanzar: null, recoger: null }
export async function leerAvisoSubagentes($: $): Promise<TextosAviso> {
  const raiz = await raizSesion($)
  if (!(await encendidos($, raiz))) return SIN_AVISO
  const { peticiones, foco } = await leerPeticiones($, raiz)
  const { vistos, conLista } = await leerSubagentes($)
  const antes = await read($, avisados)
  const r = nuevos(avisosSubagentes(peticiones, vistos, conLista), antes.claves)
  await update($, avisados, a => ({ ...a, claves: r.claves, nueva: false }))
  await guardarSesion($, raiz, { claves: r.claves })
  return { ...textoAviso(r.nuevos, antes.nueva), foco: focoGuardado(peticiones, foco) }
}

// Tras un /clear o una compactación, lo pendiente se vuelve a avisar.
export async function rearmarAvisosSubagentes($: $): Promise<void> {
  await update($, avisados, a => ({ ...a, claves: [] }))
  await guardarSesion($, await raizSesion($), { claves: [] })
}

// Al cargarse el mod (session.start, también tras /reload-plugins): con el estado recién empezado, lo guardado de esta
// misma sesión en .sf/subagentes.json (tarea 277). Si está, la sesión no es nueva: vuelven los vistos y los avisos
// dados. Si no, es nueva de verdad. Con el estado conservado, nada.
export async function recuperarSubagentes($: $): Promise<void> {
  const antes = await read($, avisados)
  if (antes.sesion) return
  const id = await $.session.id()
  const guardada = await recordarSesion($, await raizSesion($))
  if (guardada?.vistos) await recuperarVistos($, guardada.vistos)
  await update($, avisados, a =>
    a.sesion ? a : guardada ? { claves: guardada.claves ?? [], nueva: false, sesion: id } : { ...a, sesion: id },
  )
}

// ── Arranque solo (tarea 400) ──
// Al abrir la sesión (también al reanudarla), tras /clear y tras compactar, el mod no espera al primer mensaje del
// propietario: si hay tareas en curso sin subagente o subagentes terminados sin recoger, encarga a Claude un turno
// propio con $.prompt.submit, que empieza en cuanto la sesión está quieta. Va como mensaje del plugin, no como del
// propietario: quien abre la sesión ve por qué Claude se pone a trabajar solo. Solo en una sesión con alguien delante
// (no en -p ni en el SDK), con la SF activa y el interruptor `automatizaciones.avisos_subagentes` encendido.
export const FUENTES_ARRANQUE = new Set(['startup', 'resume', 'clear', 'compact'])
// Lo que espera el mod tras el SessionStart antes de encargarlo: que acabe de cargarse (session.start, decidir la sesión).
export const ESPERA_ARRANQUE = 1500
// Cuánto cuenta como «en marcha» un arranque cuyo turno no se ve acabar (si el motor no avisa del final).
export const DURACION_ARRANQUE = 10 * 60_000

// El encargo del arranque, o null sin nada que hacer.
export function textoArranque(t: TextosAviso): string | null {
  if (!t.lanzar && !t.recoger) return null
  const partes = ['Arranque de la SF, sin esperar a que el propietario escriba.']
  if (t.lanzar)
    partes.push(
      t.lanzar.replace(/^ANTES DE NADA, en este turno y antes de contestar: lanza/, 'Lanza') +
        ' Prepara sus encargos y lánzalos todos en segundo plano, a la vez en lo posible, sin otro trabajo antes.',
    )
  if (t.recoger) partes.push(t.recoger)
  const recordatorio = recordatorioFoco(t.foco, t.tareas ?? [])
  if (recordatorio) partes.push(recordatorio)
  partes.push(
    'Si el propietario escribe mientras, atiéndelo en cuanto lo veas y sigue después con lo que falte. Al acabar, di en una línea qué has lanzado o recogido y espera.',
  )
  return partes.join(' ')
}

// El arranque encargado y aún sin acabar: mientras, los mensajes del propietario no vuelven a mandar lanzar los
// subagentes (los lanzaría dos veces). Acaba con el primer final de turno del principal tras empezar el suyo.
let arranque: { hasta: number; empezado: boolean } | null = null
export async function arranqueEnMarcha($: $): Promise<boolean> {
  if (arranque && (await $.clock.now()) >= arranque.hasta) arranque = null
  return arranque !== null
}
export function arranqueTurnoAcabado(): void {
  if (arranque?.empezado) arranque = null
}
export const AVISO_ARRANQUE_EN_MARCHA =
  'El arranque de la SF ya está lanzando los subagentes de las tareas en curso: no los lances otra vez por este mensaje; atiéndelo y sigue con el arranque.'

// Encarga el arranque, si toca. Si el motor no lo admite, lo deja escrito en el prompt para enviarlo con Intro y lo
// dice, y lo avisado vuelve a contar para el siguiente mensaje.
export async function encargarArranque($: $): Promise<void> {
  if (!(await $.session.surfaces().catch(() => [] as const)).length) return
  const antes = await read($, avisados)
  const texto = textoArranque(await leerAvisoSubagentes($))
  if (!texto) return
  const hasta = (await $.clock.now()) + DURACION_ARRANQUE
  arranque = { hasta, empezado: false }
  const actual = arranque
  let r: Awaited<ReturnType<typeof $.prompt.submit>> | undefined
  try {
    r = await $.prompt.submit({ text: texto })
  } catch (err) {
    $.ui.log(`arranque: ${String(err)}`, { to: 'debug' })
  }
  if (r && !('drop' in r && r.drop !== undefined)) {
    actual.empezado = true
    return
  }
  if (arranque === actual) arranque = null
  // Lo avisado, como antes del arranque: el siguiente mensaje lo lleva, con «Sesión nueva» si lo era.
  await update($, avisados, a => ({ ...a, claves: antes.claves, nueva: antes.nueva }))
  await guardarSesion($, await raizSesion($), { claves: antes.claves }).catch(() => undefined)
  if (r) $.ui.log(`arranque no admitido: ${String(r.drop)}`, { to: 'debug' })
  const borrador = await $.prompt.read().catch(() => ({ text: '' }))
  const escrito = !borrador.text.trim() && (await $.prompt.fill({ text: texto }).catch(() => ({ isFilled: false }))).isFilled
  emergente(
    $,
    escrito
      ? 'Hay tareas en curso sin subagente: te dejo en el prompt el encargo de lanzarlos; pulsa Intro.'
      : 'Hay tareas en curso sin subagente: escribe cualquier cosa y Claude los lanzará.',
    false,
  )
}
