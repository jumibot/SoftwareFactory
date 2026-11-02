import { MARCA_SF, PETICIONES, PROYECTO } from './constantes'
import { nombreCarpeta, raizSesion } from './lectura'
import type { $ } from './lectura'

// ── Un proyecto por sesión (metodología, 2 y 11) ──
// Antes de escribir un archivo (Write, Edit, NotebookEdit), si pertenece a otro proyecto (una carpeta con
// .sf/proyecto.json o la fuente de la SF), se bloquea con el motivo, también si es la SF: ningún proyecto escribe en
// ella (decisión 194). Un worktree
// de git cuenta como su repositorio, y también, por su ruta, cualquier carpeta de <raíz>/.claude/worktrees/<nombre>/
// (los de los subagentes), aunque no se lea su .git. La cola (.sf/peticiones.json) solo la escribe el principal, nunca un subagente.
// Las órdenes de terminal no se analizan: para ellas vale la regla escrita.
export const raicesConocidas = new Map<string, string | null>()

export const normal = (ruta: string) => ruta.replace(/\\/g, '/').replace(/\/+$/, '')
export const igual = (a: string, b: string) => a.toLowerCase() === b.toLowerCase()

// Carpeta del proyecto (con .sf/proyecto.json o la fuente de la SF) que contiene la ruta, o null.
export async function proyectoDe($: $, ruta: string): Promise<string | null> {
  const partes = normal(ruta).split('/')
  const vistas: string[] = []
  let hallada: string | null = null
  for (let n = partes.length; n > 1; n--) {
    const dir = partes.slice(0, n).join('/')
    const cache = raicesConocidas.get(dir.toLowerCase())
    if (cache !== undefined) { hallada = cache; break }
    vistas.push(dir)
    if ((await $.fs.exists(`${dir}/${PROYECTO}`)) || (await $.fs.exists(`${dir}/${MARCA_SF}`))) {
      hallada = raizDeWorktree(dir) ?? (await repoDeWorktree($, dir)) ?? dir
      break
    }
  }
  for (const d of vistas) raicesConocidas.set(d.toLowerCase(), hallada)
  return hallada
}

// Los worktrees de los subagentes viven en <raíz>/.claude/worktrees/<nombre>: son de <raíz>. Devuelve <raíz> si dir
// es uno de ellos o está dentro, o null.
export function raizDeWorktree(dir: string): string | null {
  const m = /^(.+?)\/\.claude\/worktrees\/[^/]+(?:\/|$)/i.exec(normal(dir))
  return m ? m[1]! : null
}

// Un worktree de git es el mismo proyecto que su repositorio: su .git es un archivo
// «gitdir: <repo>/.git/worktrees/<n>». Devuelve <repo>, o null si dir no es un worktree.
export async function repoDeWorktree($: $, dir: string): Promise<string | null> {
  const texto: unknown = await $.fs.read(`${dir}/.git`).catch(() => '')
  const m = /^gitdir:\s*(.+?)\s*$/m.exec(typeof texto === 'string' ? texto : '')
  const repo = m && /^(.+)\/\.git\/worktrees\/[^/]+$/.exec(normal(m[1]!))
  return repo ? repo[1]! : null
}

// La cola de peticiones la escribe solo el principal (metodología, 2): una llamada con agentId viene de un
// subagente.
export function motivoCola(ruta: string, agentId: string | undefined): string | null {
  if (!agentId || !normal(ruta).toLowerCase().endsWith(`/${PETICIONES}`)) return null
  return `Solo el principal escribe la cola (${normal(ruta)}). Pasa al principal lo que haya que anotar en ella.`
}

export async function controlarEscritura($: $, ruta: string | undefined, agentId?: string): Promise<string | null> {
  if (!ruta) return null
  const cola = motivoCola(ruta, agentId)
  if (cola) return cola
  const destino = await proyectoDe($, ruta)
  if (destino === null) return null // fuera de cualquier proyecto: borradores, memoria, temporales
  const raiz = await raizSesion($)
  const propio = (await proyectoDe($, raiz)) ?? raiz
  if (igual(destino, propio)) return null
  return `Un proyecto por sesión: ${normal(ruta)} es de ${nombreCarpeta(destino)} y esta sesión es de ${nombreCarpeta(propio)}. ` +
    `Hazlo en una sesión abierta en ${destino}.`
}

// Aplica el control: si la escritura es de otro proyecto, la bloquea con el motivo.
export async function escribir<E extends { agentId?: string }, R>(
  $: $,
  ruta: string | undefined,
  e: E,
  next: (e: E) => Promise<R>,
): Promise<R | { deny: string }> {
  const motivo = await controlarEscritura($, ruta, e.agentId)
  return motivo ? { deny: motivo } : next(e)
}
