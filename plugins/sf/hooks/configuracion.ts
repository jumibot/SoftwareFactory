import { MARCA_SF, PROYECTO } from './constantes'
import type { $, Git } from './lectura'

// ── La configuración del proyecto (.sf/proyecto.json; informe «Configuración inicial», tarea 263) ──
// Una sola lectura, con los valores por defecto donde falta un campo: lo de antes de la configuración, así los
// proyectos ya incorporados no cambian hasta ponerlos al día. Un valor que no se entiende vale como si faltara y se
// nombra en `desconocidos`, para que el panel avise sin bloquear (decisión 171). La propia SF no tiene
// .sf/proyecto.json: su configuración sale de su marca, con el manifiesto del plugin y lo demás por defecto. Es la
// misma que leer_configuracion de cola.py.
export type Kanban = { proveedor: 'jkanban'; proyecto: string }
export type FormatoCommit = 'libre' | 'conventional' | 'propio'
export type Configuracion = {
  proyecto: string | null
  metodologia: boolean
  kanban: Kanban | null
  idioma: string
  commits: FormatoCommit
  remoto: string
  ramaMain: string
  manifiesto: string[]
  // La línea de coautoría de los commits de la SF, o null: sin línea (238).
  coautor: string | null
  desconocidos: string[]
}
export const FORMATOS_COMMIT: readonly FormatoCommit[] = ['libre', 'conventional', 'propio']
export const TRAILER_TAREA = 'SF-Tarea'
// La línea de coautoría de la propia SF, que no tiene .sf/proyecto.json: su `coautor` por defecto (COAUTOR de
// cola.py). Un proyecto la configura en su `coautor`; sin él, sus commits van sin línea (238).
export const COAUTOR_SF = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>'

// La línea de un valor de `coautor`: con «Co-Authored-By: » delante si no lo lleva; null si está vacío; undefined si
// no vale (no es texto o tiene más de una línea). Como linea_coautor de cola.py.
export function lineaCoautor(v: unknown): string | null | undefined {
  if (v === null || (typeof v === 'string' && v.trim() === '')) return null
  if (typeof v !== 'string' || /[\r\n]/.test(v.trim())) return undefined
  const t = v.trim()
  return /^co-authored-by:/i.test(t) ? t : `Co-Authored-By: ${t}`
}

const nombreValido = (v: unknown): v is string => typeof v === 'string' && v.trim() !== '' && !/[\s~^:?*[\\]|\.\.|^-/.test(v.trim())

// «json» (clave version: package.json, plugin.json) o «pyproject» (pyproject.toml); null si no se soporta.
export function formatoManifiesto(ruta: string): 'json' | 'pyproject' | null {
  const nombre = (ruta.trim().replace(/\\/g, '/').split('/').at(-1) ?? '').toLowerCase()
  return nombre.endsWith('.json') ? 'json' : nombre === 'pyproject.toml' ? 'pyproject' : null
}

export function leerConfiguracion(datos: Record<string, unknown> | null, esSf = false): Configuracion {
  const d = datos ?? {}
  const raros: string[] = []
  const c: Configuracion = {
    proyecto: typeof d.proyecto === 'string' && d.proyecto.trim() ? d.proyecto.trim() : null,
    metodologia: true,
    kanban: null,
    idioma: 'es',
    commits: 'libre',
    remoto: 'origin',
    ramaMain: 'main',
    manifiesto: esSf ? [MARCA_SF] : [],
    coautor: esSf ? COAUTOR_SF : null,
    desconocidos: raros,
  }
  if ('idioma' in d) {
    if (typeof d.idioma === 'string' && /^[a-z]{2,3}(-[A-Za-z]{2,4})?$/.test(d.idioma.trim())) c.idioma = d.idioma.trim()
    else raros.push('idioma')
  }
  if ('commits' in d) {
    const f = FORMATOS_COMMIT.find(x => x === d.commits)
    if (f) c.commits = f
    else raros.push('commits')
  }
  if ('remoto' in d) {
    if (nombreValido(d.remoto)) c.remoto = d.remoto.trim()
    else raros.push('remoto')
  }
  if ('rama_main' in d) {
    if (nombreValido(d.rama_main)) c.ramaMain = d.rama_main.trim()
    else raros.push('rama_main')
  }
  if ('manifiesto' in d) {
    const m = d.manifiesto
    const lista: unknown[] | null = m === null ? [] : typeof m === 'string' ? [m] : Array.isArray(m) ? m : null
    const buenos = (lista ?? []).filter((x): x is string => typeof x === 'string' && formatoManifiesto(x) !== null)
    if (lista === null || buenos.length !== lista.length) raros.push('manifiesto')
    c.manifiesto = buenos.map(x => x.trim().replace(/\\/g, '/'))
  }
  if ('metodologia' in d) {
    if (typeof d.metodologia === 'boolean') c.metodologia = d.metodologia
    else raros.push('metodologia')
  }
  if ('kanban' in d && d.kanban !== null) {
    const k = d.kanban as Record<string, unknown> | string
    if (typeof k === 'string' && k.trim()) c.kanban = { proveedor: 'jkanban', proyecto: k.trim() }
    else if (typeof k === 'object' && k.proveedor === 'jkanban' && typeof k.proyecto === 'string' && k.proyecto.trim())
      c.kanban = { proveedor: 'jkanban', proyecto: k.proyecto.trim() }
    else raros.push('kanban')
  }
  if ('coautor' in d) {
    const linea = lineaCoautor(d.coautor)
    if (linea === undefined) {
      raros.push('coautor')
      c.coautor = null
    } else c.coautor = linea
  }
  return c
}

// La de la carpeta: su .sf/proyecto.json o, en la SF, su marca. Un archivo que no se lee, como si faltara.
export async function configuracion($: $, raiz: string): Promise<Configuracion> {
  let datos: Record<string, unknown> | null = null
  try {
    if (await $.fs.exists(`${raiz}/${PROYECTO}`)) {
      const leido = JSON.parse(await $.fs.read(`${raiz}/${PROYECTO}`)) as unknown
      datos = leido && typeof leido === 'object' && !Array.isArray(leido) ? (leido as Record<string, unknown>) : null
    }
  } catch {
    datos = null
  }
  return leerConfiguracion(datos, await $.fs.exists(`${raiz}/${MARCA_SF}`))
}

// La línea de convenciones que el mod entrega con las reglas (y cola.py encargo, en el encargo del subagente).
export function convenciones(c: Configuracion): string {
  const marca = c.commits === 'libre' ? '«(N)» al final del título' : `el trailer «${TRAILER_TAREA}: N» al pie`
  const formato = { libre: 'libres', conventional: 'conventional commits', propio: 'con la forma de los últimos del proyecto' }[c.commits]
  const partes = [`idioma ${c.idioma}`, `commits ${formato}, con el número de la tarea como ${marca}`, `remoto ${c.remoto}`]
  if (c.ramaMain !== 'main') partes.push(`se publica en ${c.ramaMain}, que hace de main`)
  return `Convenciones del proyecto: ${partes.join('; ')}.`
}

// Los remotos del repositorio y su url, del config de su carpeta común, sin ejecutar git; null si no se lee.
export async function remotos($: $, git: Git): Promise<Record<string, string> | null> {
  try {
    if (!(await $.fs.exists(`${git.comun}/config`))) return null
    const salida: Record<string, string> = {}
    let actual: string | null = null
    for (const linea of (await $.fs.read(`${git.comun}/config`)).split(/\r?\n/)) {
      const s = /^\s*\[\s*remote\s+"([^"]+)"\s*\]/.exec(linea)
      if (s) {
        actual = s[1]!
        continue
      }
      if (/^\s*\[/.test(linea)) actual = null
      const u = actual ? /^\s*url\s*=\s*(.+?)\s*$/.exec(linea) : null
      if (u && actual && !(actual in salida)) salida[actual] = u[1]!
    }
    return salida
  } catch {
    return null
  }
}

export const esDeGithub = (url: string) => /(^|[@/.])github\.com[:/]/i.test(url)

// Los avisos de la configuración: valores que no se entienden, y el remoto que no existe o no apunta a GitHub
// (decisión 230). Sin config de git que leer, no se avisa del remoto.
export function avisosConfiguracion(c: Configuracion, rem: Record<string, string> | null): string[] {
  const avisos: string[] = []
  if (c.desconocidos.length)
    avisos.push(`${PROYECTO}: no se entiende ${c.desconocidos.join(', ')}; vale lo de por defecto: pide a Claude «pon el proyecto al día con la SF»`)
  if (rem !== null) {
    const url = rem[c.remoto]
    if (url === undefined) avisos.push(`no existe el remoto ${c.remoto}: pide a Claude «pon el proyecto al día con la SF»`)
    else if (!esDeGithub(url)) avisos.push(`el remoto ${c.remoto} no apunta a GitHub (${url}): la SF solo trabaja con GitHub`)
  }
  return avisos
}
