import { atom, read } from 'claude-code'
import type { Estado } from '../types'
import { enCursoRecientes } from './cola'
import { focoGuardado, leerPeticiones, raizSesion } from './lectura'
import type { $ } from './lectura'
import { sfApagada } from './latido'
import { lineaFoco, numeroTarea, recordatorioFoco } from './recordatorio'

// No interrumpir al propietario (tarea 372). El mod pone la sugerencia tras un rato sin escribir (decisión 332), el
// freno a los menús con texto a medio escribir (333) y, con el foco guardado en la cola («cola.py foco N», tarea 436),
// el recordatorio de que lo que traen sus avisos de otras tareas va como off-topic (decisión 357, 9 y 10).

const estado = atom({ plugin: 'sf', key: 'estado' } as const, null, {
  shape: 'estado-17',
})

// A los 10 minutos sin ningún prompt desde el último turno del principal (decisión 332).
export const ESPERA_SUGERENCIA = 10 * 60_000

// Cada turno que empieza o acaba y cada prompt del propietario abren una vuelta nueva: el temporizador de una vuelta
// pasada ya no sugiere nada.
let vuelta = 0

// Lo pendiente, como pregunta: la tarea de la rama activa si está en curso; si no, la en curso que cambió la última.
// Sin ninguna en curso, nada.
// Con el foco guardado en la cola y en curso, el foco (tarea 436).
export function textoSugerencia(est: Estado | null): string | null {
  if (!est || est.tipo === 'sin-sf') return null
  const enCurso = enCursoRecientes(est)
  const rama = est.rama && !est.rama.separada ? est.rama.nombre : null
  const p = enCurso.find(x => x.id === est.foco) ?? enCurso.find(x => rama !== null && x.rama === rama) ?? enCurso[0]
  return p ? `¿Seguimos con «${p.texto}» (${numeroTarea(p.id)})?` : null
}

// El número de una tarea en el chat (tarea 417), la línea del foco y el recordatorio, en recordatorio.ts (tarea 436).
export { lineaFoco, numeroTarea, recordatorioFoco }

// Al empezar la sesión (también al reanudarla), tras /clear y tras compactar, la línea del foco guardado en la cola,
// para que Claude lo tenga aunque la conversación lo haya perdido (decisión 382); sin foco, o en un subagente, null.
const FUENTES_FOCO = new Set(['startup', 'resume', 'clear', 'compact'])
export function textoFocoInicial(foco: { id: number; texto: string } | null): string | null {
  return foco ? `Foco guardado en la cola: ${lineaFoco(foco)}. Es el foco hasta que el propietario lo cambie (cola.py foco).` : null
}
export async function contextoFoco($: $, e: { source: string; agent_id?: string }): Promise<string | null> {
  if (!FUENTES_FOCO.has(e.source) || e.agent_id) return null
  const { peticiones, foco } = await leerPeticiones($, await raizSesion($))
  return textoFocoInicial(focoGuardado(peticiones, foco))
}

// Un turno del principal empieza o el propietario escribe: la sugerencia pendiente ya no va.
export function cancelarSugerencia(): void {
  vuelta++
}

// Al acabar un turno del principal: si en ESPERA_SUGERENCIA no llega ningún prompt, la sugerencia en la caja del prompt,
// en gris y sin enviarla (Tab para tomarla), y solo con la caja vacía: no pisa lo que esté escribiendo.
export function armarSugerencia($: $): void {
  const mia = ++vuelta
  $.clock.after(ESPERA_SUGERENCIA, () => void sugerirPendiente($, mia).catch(() => undefined))
}

async function sugerirPendiente($: $, mia: number): Promise<boolean> {
  if (mia !== vuelta) return false
  if (await sfApagada($).catch(() => true)) return false
  const texto = textoSugerencia(await read($, estado))
  if (!texto || (await borrador($))) return false
  return (await $.prompt.suggest({ text: texto })).isShown
}

async function borrador($: $): Promise<boolean> {
  const b = await $.prompt.read().catch(() => null)
  return !!b && typeof b.text === 'string' && b.text.trim() !== ''
}

export const MENU_CON_BORRADOR =
  'El propietario tiene un mensaje a medio escribir en la caja del prompt: un menú ahora lo cortaría (decisión 333). ' +
  'No abras el menú: deja la pregunta en una línea al final de tu respuesta.'

// El principal no abre un menú con texto a medio escribir en la caja del prompt (decisión 333): el motivo, o null.
export async function frenarMenu($: $): Promise<string | null> {
  return (await borrador($)) ? MENU_CON_BORRADOR : null
}
