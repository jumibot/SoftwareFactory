

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
// El lanzador de la cola para Claude (tarea 252): el panel lo copia al cargar a ~/.claude/sf/cola.py, que pasa cada
// orden a la copia de cola.py de la sesión (CLAUDE_CODE_SESSION_ID), la misma que lanza el panel.
export const CLI_LANZADOR = 'tools/cola_sesion.py'
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
// El repositorio de la SF se reconoce por la fuente del plugin.
export const MARCA_SF = 'plugins/sf/.claude-plugin/plugin.json'
export const PANEL = 'sf-estado'
// Colores que acepta /color; el de la propia SF es fijo.
export const COLORES = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan'] as const
export const COLOR_SF = 'purple'
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
export const CLAVE_PLEGADO = 'plegado'
export const PLEGADAS_DE_INICIO = ['observacion', 'propuestas']
// Fondo de los bloques del panel, algo más claro que el del panel (#262626 en tema oscuro): la fila entre
// bloques queda con el fondo del panel y hace de separador.
export const FONDO_BLOQUE = '#3a3a3a'
