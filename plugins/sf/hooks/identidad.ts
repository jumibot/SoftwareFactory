import { atom, read, update } from 'claude-code'
import type { Estado } from '../types'
import type { $ } from './lectura'
import { emergenteError } from './emergentes'

// Valores de estado del mod: el motor exige declararlos en el archivo que los usa; con el mismo
// plugin y clave, son el mismo valor en todos los archivos.
// Identidad de la sesión: /color con el color del proyecto y /rename con su nombre, solo al entrar
// (norma del propietario, 2026-10-28). Lo puesto se guarda en $.state, que dura la sesión y sobrevive a
// /reload-plugins: recargar no repite los comandos. No se espera, porque se ejecutan cuando la sesión queda libre.
const identidadPuesta = atom({ plugin: 'sf', key: 'identidadPuesta' } as const, { color: null as string | null, nombre: null as string | null })

// Solo el nombre del proyecto: la tarea ya se ve en el panel.
export function nombreSesion(e: Estado): string | null {
  return e.tipo === 'sin-sf' ? null : e.proyecto
}

// Si Claude Code no deja lanzar /color o /rename, se avisa una vez y queda el motivo en el registro de depuración.
export let avisoIdentidad = false
export function lanzar($: $, command: string, args: string): void {
  $.command.run({ command, args }).catch(err => {
    $.ui.log(`/${command} ${args}: ${String(err)}`, { to: 'debug' })
    if (!avisoIdentidad) {
      avisoIdentidad = true
      emergenteError($, `El mod no pudo lanzar /${command}: ${String(err)}`)
    }
  })
}

export async function ponerIdentidad($: $, e: Estado): Promise<void> {
  const puesta = await read($, identidadPuesta)
  const nombre = nombreSesion(e)
  if (e.color && e.color !== puesta.color) lanzar($, 'color', e.color)
  if (nombre && nombre !== puesta.nombre) lanzar($, 'rename', nombre)
  await update($, identidadPuesta, () => ({ color: e.color ?? puesta.color, nombre: nombre ?? puesta.nombre }))
}
