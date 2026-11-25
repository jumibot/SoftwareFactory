

// Fases del ciclo de la metodología (skills/metodologia/references/desarrollo-de-proyectos.md, 3.1–3.7).
export const FASES = [
  { clave: 'vision', nombre: 'Visión' },
  { clave: 'especificacion', nombre: 'Especificación e interfaz' },
  { clave: 'tecnica', nombre: 'Definición técnica' },
  { clave: 'planificacion', nombre: 'Planificación de devslices' },
  { clave: 'preparacion', nombre: 'Preparación de la devslice' },
  { clave: 'desarrollo', nombre: 'Desarrollo y verificación' },
  { clave: 'cierre', nombre: 'Cierre' },
] as const

// Carpeta .sf/ en la raíz del proyecto (metodología, 2 y 6): proyecto.json, versionado, dice que el proyecto está
// bajo la SF; estado.json, fuera de git, guarda el estado (o su última copia cuando el estado venga de JKanban).
export const PROYECTO = '.sf/proyecto.json'
export const ESTADO = '.sf/estado.json'
// Cola de peticiones del propietario (metodología, 2): fuera de git, la mantiene Claude.
export const PETICIONES = '.sf/peticiones.json'
// Las tareas que salen de la cola, una línea JSON cada una, con su historial; lo escribe cola.py.
export const HISTORIAL = '.sf/historial.jsonl'
// Lo que el mod sabe de los subagentes de cada sesión (tarea 277), fuera de git: sobrevive a un cambio de plugin.
export const MEMORIA_SUBAGENTES = '.sf/subagentes.json'
// El CLI de la cola, en el plugin: toda escritura de la cola pasa por él.
export const CLI_COLA = 'tools/cola.py'
// Dónde copia el panel su cola.py al cargar (decisión 136), relativo a la carpeta de Claude Code (carpetaClaude).
export const CARPETA_COPIAS = 'sf'
// El progreso de una incorporación (tarea 333), que escribe tools/incorporacion.py: en la misma carpeta que las copias,
// un archivo por proyecto, <CARPETA_COPIAS>/<PREFIJO_INCORPORACION><clave de la carpeta>.json, con la carpeta dentro.
export const PREFIJO_INCORPORACION = 'incorporacion-'
// El lanzador de la cola para Claude (tarea 252): el panel lo copia al cargar a ~/.claude/sf/cola.py, que pasa cada
// orden a la copia de cola.py de la sesión (CLAUDE_CODE_SESSION_ID), la misma que lanza el panel.
export const CLI_LANZADOR = 'tools/cola_sesion.py'
// La revisión de lo que sale al publicar en un repositorio público (decisión 252), que lanza RELEASE.
export const CLI_REVISION = 'tools/revision_publica.py'
// La orden con que Claude lanza la cola, en cualquier proyecto y en bash, zsh o PowerShell, tras el intérprete que
// detecta el mod (python.ts, ordenColaClaude; decisión 236): nunca el cola.py del disco.
export const ARGS_COLA = '-I -X utf8 "$HOME/.claude/sf/cola.py"'
export const ESTADOS_PETICION = ['en-curso', 'en-cola', 'en-observacion', 'descartada'] as const
// Los nombres de antes de «En observación» (decisión 215) no son alias: el panel los convierte al leer la cola, el
// historial y el plegado guardado, igual que cola.py al cargarlos. Las líneas con «migración 215» son las únicas que
// los nombran.
export const ESTADOS_VIEJOS: Record<string, string> = { 'sin-probar': 'en-observacion' } // migración 215
export const CAMPO_VIEJO = 'probando' // migración 215
export const EVENTOS_VIEJOS: Record<string, string> = { 'a-testing': 'a-observacion', probada: 'cerrada', probando: 'observando', pendiente: 'seguir' } // migración 215
export const EVENTO_CERRADA_VIEJO = 'probada' // migración 215
const SECCION_VIEJA = 'probar' // migración 215
// El plegado guardado con la sección de antes (también en las claves de sus tareas, «pet:<sección>:12») pasa a la de
// ahora, «observacion». Devuelve null si no hay nada que cambiar.
export function migrarPlegado(v: Record<string, boolean>): Record<string, boolean> | null {
  let cambio = false
  const nuevo: Record<string, boolean> = {}
  for (const [k, x] of Object.entries(v)) {
    const partes = k.split(':')
    const i = partes.length === 1 ? 0 : 1
    if (partes[i] === SECCION_VIEJA) {
      partes[i] = 'observacion'
      cambio = true
    }
    nuevo[partes.join(':')] = x
  }
  return cambio ? nuevo : null
}
// Ubicación anterior a sf 0.7.0: se sigue leyendo, con aviso para moverla.
export const ANTIGUO = 'docs/sf.json'
// El repositorio fuente de la SF, por la fuente del plugin: solo para lo que hace falta en él (el modo prueba y la regla
// del prompt de sistema, decisión 345); su configuración sale de su .sf/proyecto.json (299).
export const MARCA_SF = 'plugins/sf/.claude-plugin/plugin.json'
export const PANEL = 'sf-estado'
// Colores que acepta /color. COLOR_SF es el de la sesión de la SF si le faltara su estilo: el amarillo (decisión 304).
export const COLORES = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan'] as const
export const COLOR_SF = 'yellow'
// Cada color de /color en RGB, para pintar el nombre del proyecto como la etiqueta de la sesión.
// El morado está medido en la etiqueta de Claude Code (tema oscuro); los demás, aproximados.
export const RGB: Record<(typeof COLORES)[number], string> = {
  red: '#dc2626',
  blue: '#2563eb',
  green: '#16a34a',
  yellow: '#ca8a04',
  purple: '#827dbd',
  orange: '#ea580c',
  pink: '#db2777',
  cyan: '#0891b2',
}
// El estilo del proyecto (decisión 316): su colores.primario da el color de sesión (decisión 310).
export const ESTILO = 'docs/identidad/estilo.json'
// El tono OKLCH (grados) de un color #rrggbb y su croma, o null si no es un hex.
export function tonoOklch(hex: string): { tono: number; croma: number } | null {
  const m = /^#?([0-9a-f]{6}|[0-9a-f]{3})$/i.exec(hex.trim())
  if (!m) return null
  const h = m[1].length === 3 ? [...m[1]].map(c => c + c).join('') : m[1]
  const lin = (i: number) => {
    const c = parseInt(h.slice(i, i + 2), 16) / 255
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4
  }
  const [r, g, b] = [lin(0), lin(2), lin(4)]
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
  const mm = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
  const A = 1.9779984951 * l - 2.428592205 * mm + 0.4505937099 * s
  const B = 0.0259040371 * l + 0.7827717662 * mm - 0.808675766 * s
  return { tono: ((Math.atan2(B, A) * 180) / Math.PI + 360) % 360, croma: Math.hypot(A, B) }
}
// El color de /color de tono más cercano a un primario, sin reservar el de la SF (decisión 311). Un primario gris
// (croma por debajo de 0,03) no tiene tono: null, y la sesión conserva el color del proyecto.
export function colorDeSesion(primario: string): (typeof COLORES)[number] | null {
  const p = tonoOklch(primario)
  if (!p || p.croma < 0.03) return null
  const dist = (c: (typeof COLORES)[number]) => {
    const d = Math.abs(tonoOklch(RGB[c])!.tono - p.tono) % 360
    return Math.min(d, 360 - d)
  }
  return COLORES.reduce((mejor, c) => (dist(c) < dist(mejor) ? c : mejor))
}
export const CLAVE_PLEGADO = 'plegado'
export const PLEGADAS_DE_INICIO = ['observacion', 'propuestas']
// Fondo de los bloques del panel, algo más claro que el del panel (#262626 en tema oscuro): la fila entre
// bloques queda con el fondo del panel y hace de separador.
export const FONDO_BLOQUE = '#3a3a3a'
