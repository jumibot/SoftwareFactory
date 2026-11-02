import { ARGS_COLA } from './constantes'
import type { $ } from './lectura'

// ── El intérprete de Python de esta máquina («La orden de Python sale del intérprete que se detecta», 236) ──
// La SF lanza cola.py y sus herramientas con Python: en Windows suele ser `python` (o `py`, el lanzador); en macOS y
// en muchas Linux solo hay `python3`. El mod prueba los tres, por este orden, y se queda con el primero que responde
// con Python 3.9 o posterior (el python3 de las herramientas de línea de órdenes de macOS es el 3.9). Con él lanza el
// panel cola.py y da a Claude sus órdenes. `python` en Windows puede ser el atajo de la Microsoft Store, que no es
// Python: no responde a la prueba y se pasa al siguiente.
export const CANDIDATOS_PYTHON = ['python', 'python3', 'py'] as const
export const PRUEBA_PYTHON = 'import sys;print("sf-python",*sys.version_info[:2])'
const MINIMO: readonly [number, number] = [3, 9]

let detectado: string | null = null
let deteccion: Promise<string | null> | null = null

// El intérprete detectado, o null si aún no se ha detectado o no hay ninguno.
export const pythonDetectado = () => detectado

// El que respondió a una orden (el panel lo apunta si la detección no lo encontró y la orden sí respondió).
export function recordarPython(exe: string): void {
  detectado = exe
}

// Detecta el intérprete una vez por carga del mod; `otraVez`, al cargar (session.start, /reload-plugins, /clear).
export function detectarPython($: $, otraVez = false): Promise<string | null> {
  if (otraVez || !deteccion)
    deteccion = (async () => {
      for (const exe of CANDIDATOS_PYTHON) {
        const r = await $.process.run([exe, '-I', '-c', PRUEBA_PYTHON], { timeoutMs: 20_000 }).catch(() => null)
        const m = r && r.exitCode === 0 ? /sf-python (\d+) (\d+)/.exec(r.stdout) : null
        if (!m) continue
        const [mayor, menor] = [Number(m[1]), Number(m[2])]
        if (mayor > MINIMO[0] || (mayor === MINIMO[0] && menor >= MINIMO[1])) {
          detectado = exe
          return exe
        }
      }
      detectado = null
      return null
    })()
  return deteccion
}

// La orden con que Claude lanza la cola, en cualquier proyecto y en bash, zsh o PowerShell: el lanzador que copia el
// panel (tarea 252), con el intérprete detectado; sin detectar, `python`.
export const ordenColaClaude = () => `${detectado ?? 'python'} ${ARGS_COLA}`

// Lo que el mod dice a Claude del intérprete al empezar la sesión, tras /clear y tras compactar, en cualquier carpeta
// (también antes de incorporar, cuando la incorporación ya lanza herramientas de Python): nada si es `python`, que es
// lo que escriben las skills; el que hay, si es otro; y, si no hay ninguno, que falta.
export function lineaPython(exe: string | null): string | null {
  if (exe === 'python') return null
  if (exe === null)
    return (
      `Software Factory: en esta máquina no responde Python ${MINIMO.join('.')} o posterior (se han probado ${CANDIDATOS_PYTHON.join(', ')}). ` +
      'La cola de la SF y sus herramientas lo necesitan: antes de usarlas, díselo al desarrollador en una línea, con cómo instalarlo ' +
      '(en macOS, `xcode-select --install` o `brew install python`; en Windows, desde python.org), y que reinicie Claude Code después.'
    )
  return (
    `Software Factory: en esta máquina Python se lanza con \`${exe}\`, no con \`python\`. En toda orden de Python de la SF (la cola, ` +
    `sus herramientas y los scripts de las skills, que escriben \`python -I -X utf8 …\`) se usa \`${exe}\`; la de la cola es ` +
    `\`${exe} ${ARGS_COLA}\`. Dilo así en el encargo de cada subagente que lance Python.`
  )
}
