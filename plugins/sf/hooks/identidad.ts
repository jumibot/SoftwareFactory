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
// Devuelve si se ha ejecutado (Claude Code lo ejecuta cuando la sesión queda libre); no hace falta esperarlo.
export function lanzar($: $, command: string, args: string): Promise<boolean> {
  return $.command.run({ command, args }).then(
    () => true,
    err => {
      $.ui.log(`/${command} ${args}: ${String(err)}`, { to: 'debug' })
      if (!avisoIdentidad) {
        avisoIdentidad = true
        emergenteError($, `El mod no pudo lanzar /${command}: ${String(err)}`)
      }
      return false
    },
  )
}

// La app de escritorio puede quitar de su cola una orden lanzada al arrancar la sesión («the command was removed from
// the queue before it ran»): no llega a correr. Entonces se lanza otra vez, una sola, a los REINTENTO ms, sin avisar;
// solo si ese segundo intento falla, el aviso de lanzar. Se lanza en un temporizador, fuera del hook que lo pide.
export const REINTENTO = 3000
const quitadaDeLaCola = (err: unknown) => /removed from the queue/i.test(String(err))
// El motor no deja lanzar una orden desde el hook de otra mientras la tiene en curso (al tomar la SF con
// /sf_forzar_activa, «called from a command.run hook … (host check)»), tampoco desde un temporizador que salta antes de
// que ese hook acabe. Esas quedan pendientes y salen después: DESPUES_DE_ORDEN ms tras acabar la orden y, si el motor
// aún las rechaza, al acabar el siguiente turno de Claude (turn.complete) o en el siguiente latido, sin avisar.
export const DESPUES_DE_ORDEN = 500
const desdeUnaOrden = (err: unknown) => /called from a command\.run hook|host check/i.test(String(err))
const pendientes = new Map<string, string>()
// Mientras corre el hook de una orden del mod (diferirIdentidad), /color y /rename quedan pendientes sin intentarlo.
let enOrden = 0

function lanzarIdentidad($: $, command: string, args: string): void {
  if (enOrden > 0) return void pendientes.set(command, args)
  $.clock.after(0, () => void intentar($, command, args))
}
function intentar($: $, command: string, args: string): Promise<void> {
  return $.command.run({ command, args }).then(
    () => undefined,
    (err: unknown) => {
      if (desdeUnaOrden(err)) {
        $.ui.log(`/${command} ${args}: ${String(err)}; pendiente para después del turno`, { to: 'debug' })
        if (!pendientes.has(command)) pendientes.set(command, args)
        return
      }
      if (!quitadaDeLaCola(err)) return void lanzar($, command, args)
      $.ui.log(`/${command} ${args}: ${String(err)}; otra vez en ${String(REINTENTO / 1000)} s`, { to: 'debug' })
      $.clock.after(REINTENTO, () => void lanzar($, command, args))
    },
  )
}

// /color y /rename pendientes, si los hay: se lanzan ya (desde turn.complete, el latido o tras una orden).
export function lanzarPendientes($: $): void {
  const todas = [...pendientes]
  pendientes.clear()
  for (const [command, args] of todas) void intentar($, command, args)
}

// Envuelve el hook de una orden del mod que puede poner la identidad (/sf_forzar_activa): lo que pida queda pendiente
// y sale DESPUES_DE_ORDEN ms después, con el hook ya acabado.
export async function diferirIdentidad<T>($: $, fn: () => Promise<T>): Promise<T> {
  enOrden++
  try {
    return await fn()
  } finally {
    enOrden--
    if (enOrden === 0 && pendientes.size) $.clock.after(DESPUES_DE_ORDEN, () => lanzarPendientes($))
  }
}

// La SF en esta sesión, el mismo valor que en latido.tsx. Apagada (otra sesión la tiene, o /sf_forzar_inactiva), la
// sesión es Claude Code sin más: ni /color ni /rename (decisión 297).
const sesionSf = atom({ plugin: 'sf', key: 'sesionSf' } as const, null as 'activa' | 'apagada' | 'inactiva' | null)

export async function ponerIdentidad($: $, e: Estado): Promise<void> {
  const s = await read($, sesionSf)
  if (s === 'apagada' || s === 'inactiva') return
  const puesta = await read($, identidadPuesta)
  const nombre = nombreSesion(e)
  if (e.color && e.color !== puesta.color) lanzarIdentidad($, 'color', e.color)
  if (nombre && nombre !== puesta.nombre) lanzarIdentidad($, 'rename', nombre)
  await update($, identidadPuesta, () => ({ color: e.color ?? puesta.color, nombre: nombre ?? puesta.nombre }))
}
