import { atom, read, update } from 'claude-code'
import type { AvisosSubagentes, Peticion, SubagenteVisto } from '../types'
import { PROYECTO } from './constantes'
import { ordenColaClaude } from './python'
import { leerJson, leerPeticiones, leerSubagentes, raizSesion, recuperarVistos } from './lectura'
import { guardarSesion, recordarSesion } from './memoria'
import type { $ } from './lectura'

// ── Avisos de subagentes (tarea 249) ──
// Con cada mensaje del propietario, al volver un subagente (su notificación o el final del Agent en primer plano), el
// mod añade al contexto de Claude las tareas en curso sin subagente vivo y los subagentes que han terminado sin
// recoger. Solo avisa. Cada situación se avisa una vez, cuando aparece: se repite si se resuelve y vuelve, tras un
// /clear o una compactación (Claude ya no la tiene en el contexto) y en una sesión nueva. Si el motor no da la lista de
// subagentes, no se sabe quién vive: no se avisa de los que faltan. La sesión se reconoce por su id, no por la carga
// del módulo: /reload-plugins, aunque cambie de plugin y vacíe el estado, no la hace nueva (tarea 277).

// Las claves ya avisadas, si aún no se ha avisado nada en una sesión nueva y el id de la sesión.
const avisados = atom({ plugin: 'sf', key: 'avisosSubagentes' } as const, { claves: [], nueva: true } as AvisosSubagentes)

export type AvisoSubagente = { clave: string; texto: string }

// El último informe anotado de la tarea (ms), o null.
function ultimoInforme(p: Peticion): number | null {
  for (let i = p.historial.length - 1; i >= 0; i--) if (p.historial[i]!.evento === 'informe') return p.historial[i]!.fecha
  return null
}

// Lo que hay que avisar ahora, por tarea en curso: sin subagente vivo (ni trabajando ni esperando), si se tiene la
// lista; o con uno que dejó de trabajar después del último informe anotado («cola.py informe» es recogerlo).
export function avisosSubagentes(peticiones: Peticion[], vistos: Record<string, SubagenteVisto>, conLista: boolean): AvisoSubagente[] {
  const avisos: AvisoSubagente[] = []
  const lista = Object.values(vistos)
  for (const p of peticiones) {
    if (p.estado !== 'en-curso') continue
    const n = String(p.id)
    const suyos = lista.filter(v => v.tarea === p.id)
    if (suyos.some(v => v.estado === 'trabajando')) continue
    const esperan = suyos.filter(v => v.estado === 'esperando')
    if (!esperan.length) {
      if (conLista) avisos.push({ clave: `sin:${n}`, texto: `la ${n} está en curso sin subagente: lánzalo («Tarea ${n}: …»)` })
      continue
    }
    const informe = ultimoInforme(p) ?? -Infinity
    // Por segundos enteros, como las fechas de cola.py.
    if (esperan.some(v => v.visto !== undefined && Math.floor(v.visto / 1000) * 1000 > informe))
      avisos.push({ clave: `fin:${n}`, texto: `el subagente de la ${n} ha terminado: recógelo (revisar el diff, merge --ff-only, \`${ordenColaClaude()} informe ${n}\`, pasos, listo)` })
  }
  return avisos
}

// Las que no se habían avisado, y las claves que quedan avisadas: las de ahora (las resueltas salen y vuelven a contar).
export function nuevos(avisos: AvisoSubagente[], claves: string[]): { nuevos: AvisoSubagente[]; claves: string[] } {
  const ya = new Set(claves)
  return { nuevos: avisos.filter(a => !ya.has(a.clave)), claves: avisos.map(a => a.clave) }
}

// El texto del aviso, o null sin nada nuevo. En una sesión recién abierta, recuerda que los de la anterior ya no viven.
export function textoAviso(nuevosAvisos: AvisoSubagente[], nueva: boolean): string | null {
  if (!nuevosAvisos.length) return null
  const inicio = nueva && nuevosAvisos.some(a => a.clave.startsWith('sin:')) ? 'Sesión nueva: los subagentes de la anterior ya no viven. ' : ''
  return `${inicio}Subagentes: ${nuevosAvisos.map(a => a.texto).join('; ')}.`
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

// Lee la cola y los subagentes y devuelve el aviso de lo nuevo, apuntándolo como avisado; null sin nada nuevo.
export async function leerAvisoSubagentes($: $): Promise<string | null> {
  const raiz = await raizSesion($)
  if (!(await encendidos($, raiz))) return null
  const { peticiones } = await leerPeticiones($, raiz)
  const { vistos, conLista } = await leerSubagentes($)
  const antes = await read($, avisados)
  const r = nuevos(avisosSubagentes(peticiones, vistos, conLista), antes.claves)
  await update($, avisados, a => ({ ...a, claves: r.claves, nueva: false }))
  await guardarSesion($, raiz, { claves: r.claves })
  return textoAviso(r.nuevos, antes.nueva)
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
