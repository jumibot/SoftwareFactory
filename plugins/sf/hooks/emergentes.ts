import { MARCA_AVISO_EMERGENTE, MARCA_ERROR_EMERGENTE } from './estilo'
import type { $ } from './lectura'

// ── Avisos emergentes del panel (tarea 257) ──
// Todo lo que el panel dice en un toast pasa por aquí: se lee a primera vista qué tarea y qué ha pasado. Las rutas
// absolutas, por su último tramo («wt-256» en vez de «D:/proyectos/SoftwareFactory-wt-256»); el mensaje entero de
// cola.py, que también ve Claude, no cambia. El toast no admite fondo: avisos y errores se distinguen por la marca de
// color del principio (estilo.ts) y los errores duran más.

// Una ruta absoluta (D:/…, D:\…, /…) con al menos una carpeta, no pegada a otra palabra: «/sf_split 12» no lo es, y
// «plugins/sf/x.json», relativa, se queda como está.
const RUTA = /(?<![\w.\-/\\])(?:[A-Za-z]:[\\/]|\/)(?:[^\s,;:()«»"'\\/]+[\\/])+([^\s,;:()«»"'\\/]+)/g

// Las rutas, abreviadas: la carpeta de un worktree de subagente («Proyecto-wt-256»), «wt-256»; las demás, su último
// tramo.
export const abreviarRutas = (t: string) => t.replace(RUTA, (_, fin: string) => /-(wt-[\w-]+)$/.exec(fin)?.[1] ?? fin)

// Un fallo de una orden del panel: el convenio es anteponer la orden («C: …», «/sf_split: …», «→: …») solo cuando no sale.
export const pareceError = (t: string) => /^(?:[A-Z]|→|\/[\w-]+):\s/.test(t)

// El texto del toast: la marca, avisos o errores, y las rutas abreviadas.
export const textoEmergente = (t: string, error: boolean) =>
  `${error ? MARCA_ERROR_EMERGENTE : MARCA_AVISO_EMERGENTE} ${abreviarRutas(t.trim())}`

// Lo que dura: 4 s los cortos, algo más los largos, para leerlos; los errores, al menos 8 s. Un clic lo quita.
export const duracionEmergente = (t: string, error: boolean) =>
  Math.min(15_000, Math.max(error ? 8_000 : 4_000, 60 * t.length))

// Muestra un aviso emergente; `error` sin decir, se deduce del texto (pareceError).
export function emergente($: $, t: string, error = pareceError(t)): void {
  const texto = textoEmergente(t, error)
  $.ui.toast(texto, { timeoutMs: duracionEmergente(texto, error) })
}
export function emergenteError($: $, t: string): void {
  emergente($, t, true)
}
// La respuesta de una orden ({ ok, mensaje }), como aviso o como error.
export function emergenteRespuesta($: $, r: { ok: boolean; mensaje: string }): void {
  emergente($, r.mensaje, !r.ok)
}
