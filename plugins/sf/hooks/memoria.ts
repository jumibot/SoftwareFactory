import type { EngineInterface } from 'claude-code'
import type { SubagenteVisto } from '../types'
import { MEMORIA_SUBAGENTES, PETICIONES } from './constantes'

// ── Lo que el mod sabe de los subagentes de cada sesión, en disco (tarea 277) ──
// $.state no sobrevive a un cambio de plugin (/reload-plugins al entrar o salir del modo prueba, o con otra versión):
// el mod empezaría de cero, creería la sesión nueva y pediría lanzar los subagentes que ya viven. Por eso lo apuntado
// (los subagentes vistos y los avisos dados) se guarda también en .sf/subagentes.json, fuera de git, por el id de la
// sesión: al cargarse con el estado vacío, el mod lo recupera si es de la misma sesión. Solo con cola de peticiones.
// Se guardan las sesiones de la última semana, hasta diez.

export type MemoriaSesion = { fecha: number; claves?: string[]; vistos?: Record<string, SubagenteVisto> }
type Memoria = { sesiones: Record<string, MemoriaSesion> }

const SEMANA = 7 * 24 * 3600_000
const MAXIMO = 10

async function leer($: EngineInterface, raiz: string): Promise<Memoria> {
  try {
    const m = JSON.parse(await $.fs.read(`${raiz}/${MEMORIA_SUBAGENTES}`)) as Memoria
    return m && typeof m.sesiones === 'object' && m.sesiones ? m : { sesiones: {} }
  } catch {
    return { sesiones: {} }
  }
}

// Lo guardado de esta sesión, o null.
export async function recordarSesion($: EngineInterface, raiz: string): Promise<MemoriaSesion | null> {
  return (await leer($, raiz)).sesiones[await $.session.id()] ?? null
}

// Apunta lo de esta sesión: los vistos se suman a los guardados (un subagente no deja de haber existido) y las claves
// se sustituyen.
export async function guardarSesion($: EngineInterface, raiz: string, cambio: { claves?: string[]; vistos?: Record<string, SubagenteVisto> }): Promise<void> {
  try {
    if (!(await $.fs.exists(`${raiz}/${PETICIONES}`))) return
    const id = await $.session.id()
    const ahora = await $.clock.now()
    const m = await leer($, raiz)
    const antes = m.sesiones[id]
    const sesion: MemoriaSesion = {
      fecha: ahora,
      claves: cambio.claves ?? antes?.claves ?? [],
      vistos: { ...(antes?.vistos ?? {}), ...(cambio.vistos ?? {}) },
    }
    const sesiones = Object.entries({ ...m.sesiones, [id]: sesion })
      .filter(([, s]) => ahora - s.fecha < SEMANA)
      .sort((a, b) => b[1].fecha - a[1].fecha)
      .slice(0, MAXIMO)
    const texto = JSON.stringify({ sesiones: Object.fromEntries(sesiones) }, null, 2) + '\n'
    await $.fs.write(`${raiz}/${MEMORIA_SUBAGENTES}`, texto)
  } catch {
    // Sin memoria en disco, el mod sigue con la de la sesión.
  }
}
