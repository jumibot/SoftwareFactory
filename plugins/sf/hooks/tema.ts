import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'
import { modoDeTema } from './logo'
import type { ModoLogo } from './logo'
import type { $ } from './lectura'

// ── El tema de Claude Code, para el logo «/SF» del terminal (tarea 395) ──
// El mod no sabe el fondo de la superficie: lee el ajuste «theme» de /config. Con un tema claro (light…), el logo
// claro; con cualquier otro, sin ajuste o «auto», el oscuro. En el escritorio y el móvil, el SVG del logo sigue el
// modo de la app por sí solo (prefers-color-scheme).
const temaClaro = atom({ plugin: 'sf', key: 'temaClaro' } as const, false)

export async function modoLogo($: $): Promise<ModoLogo> {
  return (await read($, temaClaro).catch(() => false)) ? 'claro' : 'oscuro'
}

async function anotarTema($: $, tema: unknown): Promise<void> {
  const claro = modoDeTema(tema) === 'claro'
  if ((await read($, temaClaro)) !== claro) await update($, temaClaro, () => claro)
}

// Al empezar la sesión (lo llama el session.start de register.tsx), el tema que hay.
export async function leerTema($: $): Promise<void> {
  const fila = (await $.config.list().catch(() => [])).find(x => x.key === 'theme')
  await anotarTema($, fila?.value).catch(() => undefined)
}

export function registrarTema(on: Parameters<Register>[0]): void {
  // Al cambiar el tema en /config, el logo cambia con él.
  on('config.set', { key: 'theme' }, async ($, e, next) => {
    const r = await next(e)
    if (r.deny === undefined) await anotarTema($, r.value).catch(() => undefined)
    return r
  }).catch(($, e, next) => next(e))
}
