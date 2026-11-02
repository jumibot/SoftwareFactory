import { atom, read, update } from 'claude-code'
import type { $ } from './lectura'
import { sinSf } from './contexto'

// ── Sin pantalla completa, los clics no llegan (tarea 264) ──
// Fuera de la pantalla completa de Claude Code (ajuste «tui»), el panel y la caja se pintan en la conversación y no
// reciben clics: ni ACTUALIZAR ni las secciones responden. El motor dice en cada dibujo de la terminal si está en
// pantalla completa (e.viewport.isFullscreen, fijo en la sesión): es la fuente fiable, porque cuenta también lo que
// los ajustes no dicen (variables de entorno, un arranque fallido, el lector de pantalla). Con false, el panel lo dice
// en texto y, con el primer mensaje del propietario de la conversación, Claude recibe el contexto para ofrecer
// activarla: el motor no lo sabe antes de dibujar, y antes de ese mensaje Claude no habla.

export const AVISO_PANTALLA = 'Los botones necesitan la pantalla completa: pide a Claude que la active.'

type Dibujo = { surface?: string; viewport?: { isFullscreen?: boolean } }

// Solo la terminal: el móvil también dice false, pero allí los toques sí llegan.
export const sinPantallaCompleta = (e: Dibujo): boolean => e.surface === 'terminal' && e.viewport?.isFullscreen === false

// Lo último que dijo la terminal al dibujar: undefined hasta el primer dibujo (tras recargar el mod, hasta el siguiente).
let vista: boolean | undefined
export function anotarPantalla(e: Dibujo): void {
  if (e.surface === 'terminal' && typeof e.viewport?.isFullscreen === 'boolean') vista = e.viewport.isFullscreen
}

// Si ya se ofreció en esta conversación: en $.state, para no repetirlo tras /reload-plugins; un /clear lo reinicia.
const ofrecida = atom({ plugin: 'sf', key: 'pantallaOfrecida' } as const, false)
export async function reiniciarOferta($: $): Promise<void> {
  await update($, ofrecida, () => false)
}

// El contexto para Claude, con la causa que se puede leer: una variable de entorno, el ajuste ya puesto (un arranque
// fallido la deja en la clásica hasta /tui fullscreen) o nada. Activarla, en el proyecto; ~/.claude, solo con OK expreso.
export async function textoPantalla($: $): Promise<string> {
  const base =
    'Software Factory: Claude Code no está en pantalla completa, así que el panel de la SF se pinta en la conversación y sus botones no reciben clics. Ofrece al propietario, en una línea, activarla, y hazlo solo con su OK. '
  const noFlicker = await $.env.get('CLAUDE_CODE_NO_FLICKER').catch(() => undefined)
  const sinAlterna = await $.env.get('CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN').catch(() => undefined)
  if (noFlicker === '0' || (sinAlterna !== undefined && sinAlterna !== '' && sinAlterna !== '0')) {
    const v = noFlicker === '0' ? 'CLAUDE_CODE_NO_FLICKER=0' : `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=${sinAlterna}`
    return `${base}La quita la variable de entorno ${v}: que la retire antes de abrir Claude Code; los ajustes no bastan.`
  }
  const tui = await $.settings.read({ key: 'tui' }).catch(() => undefined)
  if (tui === 'fullscreen')
    return `${base}El ajuste «tui» ya la pide (Claude Code vuelve a la clásica tras un arranque fallido): que ejecute /tui fullscreen, que la activa al momento sin perder la conversación.`
  return `${base}Con su OK, añade "tui": "fullscreen" a .claude/settings.local.json del proyecto (nunca a ~/.claude sin su OK expreso) y dile que la tome con /exit y claude --continue. Alternativa suya: /tui fullscreen, que cambia al momento pero la guarda en ~/.claude, para todos sus proyectos.`
}

// El contexto del primer mensaje del propietario sin pantalla completa, una vez por conversación; si no, null. En una
// carpeta sin SF, todavía no: se ofrece con el primer mensaje tras incorporarla, junto a las reglas (decisión 245).
export async function ofrecerPantalla($: $): Promise<string | null> {
  if (vista !== false || (await read($, ofrecida))) return null
  if (await sinSf($)) return null
  await update($, ofrecida, () => true)
  return textoPantalla($)
}
