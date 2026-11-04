import { CLI_REVISION } from './constantes'
import { CANDIDATOS_PYTHON, detectarPython } from './python'
import type { $ } from './lectura'

// La revisión de RELEASE («La SF se trabaja en el repositorio público, con revisión antes de publicar», 252, y 259),
// con tools/revision_publica.py --decidir y sin Claude: la misma decisión que el push de develop al cerrar una tarea
// (cola.py). Lo ya publicado en el último tag no cuenta; con el remoto público, algo nuevo sin subir para; lo ya
// subido, o cualquier cosa con el remoto privado, se enseña y se pide permiso: volver a pulsar RELEASE y elegir la
// misma versión en 10 minutos. Devuelve por qué no se publica, o null si se sigue.
export async function revisarPublicacion($: $, raiz: string, remoto: string, desde: string | null, nueva: string): Promise<string | null> {
  const argv = ['-I', '-X', 'utf8', `${$.plugin.root}/${CLI_REVISION}`, '--repo', raiz, '--remoto', remoto, '--hasta', 'develop', '--json', '--decidir',
    '--accion', 'release', '--repetir', `vuelve a pulsar RELEASE y elige v${nueva}`, ...(desde ? ['--desde', desde] : [])]
  let error = 'no se encuentra Python'
  const python = await detectarPython($)
  for (const exe of python ? [python] : CANDIDATOS_PYTHON) {
    const r = await $.process.run([exe, ...argv], { cwd: raiz, timeoutMs: 180_000 }).catch((err: unknown) => {
      error = String(err)
      return null
    })
    if (r === null) continue
    let j: { ok?: unknown; mensaje?: unknown; accion?: unknown } | null = null
    try {
      j = JSON.parse(r.stdout.trim().split(/\r?\n/).at(-1) ?? '') as typeof j
    } catch {
      error = (r.stderr.trim() || r.stdout.trim() || `sale con ${String(r.exitCode)}`).split(/\r?\n/).at(-1)!
      continue
    }
    const mensaje = typeof j?.mensaje === 'string' ? j.mensaje : 'sin respuesta'
    if (j?.ok !== true) return `RELEASE: no se pudo revisar lo que sale (${mensaje}). No se publica.`
    return j.accion === 'seguir' ? null : `RELEASE no publica: ${mensaje}`
  }
  return `RELEASE: no se pudo revisar lo que sale (${error}). No se publica.`
}
