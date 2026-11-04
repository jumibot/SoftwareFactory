import { atom, read, update } from 'claude-code'
import type { Actualizacion, Estado, FuenteVersion, Paso, Peticion, Realimentacion, Sesion } from '../types'
import { normal, raicesConocidas } from './control'
import { lanzar, ponerIdentidad } from './identidad'
import { CARPETA_COPIAS, CLI_COLA, CLI_LANZADOR, MARCA_SF, PETICIONES, PROYECTO } from './constantes'
import { CANDIDATOS_PYTHON, detectarPython, ordenColaClaude, recordarPython } from './python'
import { configuracion, formatoManifiesto } from './configuracion'
import { carpetaClaude, carpetaGit, commitsDe, leerEstado, leerJson, leerMergeadas, leerPasos, raizSesion, subagentesDeTareas, texto } from './lectura'
import type { $ } from './lectura'
import { emergente, emergenteError } from './emergentes'
import { encargarAClaude } from './avisos'
import { desdeCopia } from './prueba'
import { revisarPublicacion } from './revision'

// Valores de estado del mod: el motor exige declararlos en el archivo que los usa; con el mismo
// plugin y clave, son el mismo valor en todos los archivos.
// Cambiar la etiqueta si cambian los campos de Estado.
const estado = atom({ plugin: 'sf', key: 'estado' } as const, null, {
  shape: 'estado-17',
})
const nuevasEnSf = atom({ plugin: 'sf', key: 'nuevasEnSf' } as const, 0)
const sesion = atom({ plugin: 'sf', key: 'sesion' } as const, { limpiadas: {} } as Sesion)
// Inicio de la sesión (ms): lo que el historial dice que ha pasado desde entonces es de la sesión.
const inicioSesion = atom({ plugin: 'sf', key: 'inicioSesion' } as const, 0)

export let titulosInicio: Set<string> | null = null
// Una sesión nueva tras un /clear (decisión 165): las propuestas nuevas se cuentan desde ahí.
export function olvidarTitulosInicio(): void {
  titulosInicio = null
}
// La tarea en la que se trabaja: la primera petición en curso o, si no hay, la devslice.
// Peticiones en curso, la última que ha cambiado primero: es en la que se está trabajando.
export function enCursoRecientes(e: Estado): Peticion[] {
  return porCambio(e.peticiones.filter(enCursoOObservando))
}

// Orden por defecto de las listas de tareas: la última que ha cambiado arriba (petición 166). El cambio es la
// fecha más reciente de su historial; las que no tienen historial, anteriores al CLI, van detrás de las que sí,
// de la de número más alto a la más baja, el orden que tenían arriba.
export function porCambio<T extends { id: number; cambio?: number | null }>(lista: T[]): T[] {
  return [...lista].sort((a, b) => (b.cambio ?? -Infinity) - (a.cambio ?? -Infinity) || b.id - a.id)
}

// Una tarea en observación que el propietario está mirando («La miro ahora») se trata como en curso: se trabaja en
// ella. Su estado, y su letra, siguen siendo los de En observación (petición 67).
export function enCursoOObservando(p: Peticion): boolean {
  return p.estado === 'en-curso' || (p.estado === 'en-observacion' && p.observando)
}
export function tareaPrincipal(e: Estado): string | null {
  return enCursoRecientes(e)[0]?.texto ?? e.devslice
}

// ── La cola, con el CLI (tarea 145) ──
// Toda escritura de la cola pasa por cola.py (skill sf:flujo_tareas): el panel lo lanza con la orden y la respuesta
// en JSON, como el propietario y por el panel. Así cada cambio queda en el historial de la tarea y, si sale de la
// cola, en .sf/historial.jsonl. El panel solo lee la cola: para comprobar, antes de pedir el cambio, que la tarea
// sigue siendo la que vio el propietario.
export type Respuesta = { ok: boolean; mensaje: string; id?: number; fallo?: string; motivo?: string }

// La copia de cola.py que ejecuta el panel (decisión 136): al cargar el mod (al empezar la sesión y con
// /reload-plugins) copia el cola.py de su plugin fuera del repositorio, en ~/.claude/sf/cola-<sesión>.py, y lanza
// siempre esa copia. Así el panel cargado y el CLI van a juego aunque la C, la R o Activar rama cambien de rama la carpeta del
// plugin. La copia lleva en su primera línea la raíz del plugin, para sus módulos (tarea 322). Sin copia (falla al copiar), el del disco, con un aviso. Copia también el lanzador de Claude (tarea 252) a
// ~/.claude/sf/cola.py, si ha cambiado: Claude lanza siempre ordenColaClaude(), que pasa la orden a esta copia.
let copiaCola: string | null = null
const DIAS_COPIA = 7
export async function copiarCola($: $): Promise<void> {
  copiaCola = null
  const origen = `${$.plugin.root}/${CLI_COLA}`
  let carpeta = ''
  try {
    const claude = await carpetaClaude($)
    if (!claude) throw new Error('sin carpeta de Claude Code')
    if (!(await $.fs.exists(origen))) throw new Error(`no está ${origen}`)
    carpeta = `${claude}/${CARPETA_COPIAS}`
    const id = (await $.session.id()).replace(/[^A-Za-z0-9_-]/g, '_')
    const destino = `${carpeta}/cola-${id}.py`
    // Con la raíz del plugin en la primera línea: la copia busca allí lo que necesita del plugin, como
    // indice_decisiones.py y el generador de los .html (tarea 322; MARCA_PLUGIN de cola.py).
    await $.fs.write(destino, `# sf-plugin: ${$.plugin.root}\n${await $.fs.read(origen)}`)
    copiaCola = destino
    void borrarCopiasViejas($, carpeta, `cola-${id}.py`).catch(() => undefined)
  } catch (err) {
    emergenteError($, `sf: no se pudo copiar cola.py (${String(err)}); el panel usa el del disco, que puede no ir a juego si cambia la rama.`)
    return
  }
  try {
    const fuente = `${$.plugin.root}/${CLI_LANZADOR}`
    if (!(await $.fs.exists(fuente))) throw new Error(`no está ${fuente}`)
    const lanzador = await $.fs.read(fuente)
    const destino = `${carpeta}/cola.py`
    const actual = (await $.fs.exists(destino)) ? await $.fs.read(destino) : null
    if (actual !== lanzador) await $.fs.write(destino, lanzador)
  } catch (err) {
    emergenteError($, `sf: no se pudo copiar el lanzador de cola.py para Claude (${String(err)}).`)
  }
}

// Las copias de otras sesiones de más de DIAS_COPIA días: el motor no borra archivos, lo hace Python.
async function borrarCopiasViejas($: $, carpeta: string, propia: string): Promise<void> {
  const ahora = await $.clock.now()
  const viejas = (await $.fs.list(carpeta))
    .filter(x => /^cola-.+\.py$/.test(x.name) && x.name !== propia && typeof x.mtimeMs === 'number' && x.mtimeMs > 0 && ahora - x.mtimeMs > DIAS_COPIA * 86_400_000)
    .map(x => `${carpeta}/${x.name}`)
  if (!viejas.length) return
  const codigo = 'import os,sys\nfor p in sys.argv[1:]:\n    try: os.remove(p)\n    except OSError: pass'
  const python = await detectarPython($)
  for (const exe of python ? [python] : CANDIDATOS_PYTHON) {
    const r = await $.process.run([exe, '-I', '-c', codigo, ...viejas], { timeoutMs: 30_000 }).catch(() => null)
    if (r && r.exitCode === 0) return
  }
}

// Abre un archivo o una carpeta con el programa del sistema (un .html, en el navegador), sin Claude: el motor no
// tiene otro modo. La usa Activar rama. En Windows (ruta con letra de unidad), rundll32 con el
// manejador de archivos de url.dll, que sale con 0 si lo lanza; explorer.exe sale con 1 aunque abra, y no deja ver
// un fallo. En los demás, xdg-open (Linux) y, si no está, open (macOS): en Linux, open puede ser otra orden.
// Devuelve el error, o null si lo ha lanzado.
export async function abrirArchivo($: $, ruta: string): Promise<string | null> {
  const windows = /^[a-zA-Z]:[\\/]/.test(ruta) || (await $.env.get('OS')) === 'Windows_NT'
  const intentos = windows ? [['rundll32', 'url.dll,FileProtocolHandler', ruta.replace(/\//g, '\\')]] : [['xdg-open', ruta], ['open', ruta]]
  let error = 'no hay con qué abrirlo'
  for (const argv of intentos) {
    const r = await $.process.run(argv, { timeoutMs: 15_000 }).catch((err: unknown) => {
      error = String(err)
      return null
    })
    if (r === null) continue
    if (r.exitCode === 0) return null
    error = r.stderr.trim() || `${argv[0]!} terminó con ${String(r.exitCode)}`
  }
  return error
}

export async function ordenCola($: $, args: string[]): Promise<Respuesta> {
  const raiz = await raizSesion($)
  const cli = copiaCola ?? `${$.plugin.root}/${CLI_COLA}`
  const resto = ['-I', '-X', 'utf8', cli, '--raiz', raiz, '--json', '--quien', 'propietario', '--via', 'panel', ...args]
  let error = 'no se encuentra Python'
  const python = await detectarPython($)
  for (const exe of python ? [python] : CANDIDATOS_PYTHON) {
    // Un cierre hace merge, commit y push: más que los 30 s por defecto.
    const r = await $.process.run([exe, ...resto], { cwd: raiz, timeoutMs: 180_000 }).catch((err: unknown) => {
      error = String(err)
      return null
    })
    if (r === null) continue
    const linea = r.stdout.trim().split(/\r?\n/).at(-1) ?? ''
    try {
      const j = JSON.parse(linea) as Respuesta
      if (typeof j.ok === 'boolean' && typeof j.mensaje === 'string') {
        if (!python) recordarPython(exe)
        return j
      }
    } catch {
      // Sin JSON: no es cola.py quien responde (o Python no está), se prueba el siguiente.
    }
    error = (r.stderr.trim() || r.stdout.trim() || `sale con ${String(r.exitCode)}`).split(/\r?\n/).at(-1)!
  }
  return { ok: false, mensaje: `cola.py no responde (${error}).` }
}

// La orden y, después, la relectura del panel.
async function cambiarCola($: $, args: string[]): Promise<Respuesta> {
  const r = await ordenCola($, args)
  await refrescar($)
  return r
}

// La etiqueta de develop en la cabecera, confirmada (tarea 355): sube develop a su remoto sin Claude, con «cola.py
// subir», que con el remoto público revisa antes lo que sale, como el push de un cierre y RELEASE (decisión 259). Si
// la revisión pide permiso, se da volviendo a pulsar la etiqueta. Después, la relectura, que pone al día su cifra.
export const REPETIR_SUBIDA = 'vuelve a pulsar la etiqueta de develop del panel y confírmalo'
export async function subirDevelop($: $): Promise<Respuesta> {
  return cambiarCola($, ['subir', '--repetir', REPETIR_SUBIDA])
}

// Lo que se dice al propietario cuando la orden de un botón no sale: el mensaje de cola.py, tras la letra del botón.
const conLetra = (letra: string, r: Respuesta) => (r.ok ? r.mensaje : `${letra}: ${r.mensaje}`)

// Pasos que quedan al acabar una tarea: los que hace la C al cerrarla. El de prueba es «Activar rama para poder
// probar», que se llamaba «Probar la tarea» (decisión 172): cola.py lo renombra al escribir la cola; hasta entonces, el
// panel acepta los dos.
const PROBAR = 'Activar rama para poder probar'
const PROBAR_ANTES = 'Probar la tarea'
const CERRAR = 'Cerrar la tarea'
const PASOS_DE_CIERRE = [PROBAR, PROBAR_ANTES, CERRAR]

// Se quita un paso pendiente, salvo los de cierre, que la tarea lleva desde que entra en curso (decisión 174).
export function pasoQuitable(x: { texto?: unknown; estado?: unknown }): boolean {
  return x.estado === 'pendiente' && !PASOS_DE_CIERRE.includes(String(x.texto))
}

// Quita un paso pendiente de una tarea (la E del panel, confirmada; decisión del propietario, 2026-10-29), con
// «cola.py paso quitar». Solo si en ese sitio sigue el mismo paso, sin empezar y no es de cierre: Claude
// puede haber cambiado la cola entretanto; entonces no hace nada, sin avisar. Devuelve el aviso si cola.py no lo quita.
export async function quitarPaso($: $, id: number, indice: number, textoPaso: string): Promise<string | null> {
  const tarea = await tareaVigente($, id, null, t => {
    const paso = (Array.isArray(t.pasos) ? (t.pasos as { texto?: unknown; estado?: unknown }[]) : [])[indice]
    return paso?.texto === textoPaso && pasoQuitable(paso)
  })
  if (!tarea) return null
  const r = await cambiarCola($, ['paso', 'quitar', String(id), String(indice + 1)])
  return r.ok ? null : conLetra('E', r)
}

// Se puede eliminar una tarea en cola o en curso sin rama: aún no ha cambiado ningún activo (decisión del
// propietario, 2026-10-29). Con rama, o en observación, ya tiene trabajo efectivo: se descarta o se revierte.
export function eliminable(p: { estado?: unknown; rama?: unknown }): boolean {
  return (p.estado === 'en-cola' || p.estado === 'en-curso') && texto(p.rama) === null
}

// Se descarta una tarea con rama que aún no ha entrado en develop: en cola o en curso (decisión del propietario,
// 2026-10-29). Una en observación ya entró en develop al cerrarla: no se descarta, se revierte con la R (decisión 115, 4).
export function descartable(p: { estado?: unknown; rama?: unknown }): boolean {
  return (p.estado === 'en-cola' || p.estado === 'en-curso') && texto(p.rama) !== null
}

// La R en observación: una tarea en observación con commits en develop, según su historial o la historia de develop.
export function revertibleEnObservacion(p: Peticion, mergeadas: Record<string, string[]>): boolean {
  return p.estado === 'en-observacion' && (commitsDe(p.historial).length > 0 || (mergeadas[String(p.id)]?.length ?? 0) > 0)
}

type Resultado = { ok: boolean; mensaje: string }
type Git = (args: string[], stdin?: string) => Promise<{ exitCode: number; stdout: string; stderr: string }>

// La tarea `id` de la cola, si sigue siendo la que vio el propietario (con el mismo texto, si se da) y cumple `vale`:
// Claude puede haber cambiado la cola entretanto. Solo lee: el cambio lo hace cola.py.
async function tareaVigente(
  $: $,
  id: number,
  textoTarea: string | null,
  vale: (t: Record<string, unknown>) => boolean,
): Promise<Record<string, unknown> | null> {
  let datos: Record<string, unknown>
  try {
    datos = await leerJson($, `${await raizSesion($)}/${PETICIONES}`)
  } catch {
    return null
  }
  const lista = Array.isArray(datos.peticiones) ? (datos.peticiones as Record<string, unknown>[]) : []
  const tarea = lista.find(x => x.id === id)
  return tarea && (textoTarea === null || texto(tarea.texto) === textoTarea) && vale(tarea) ? tarea : null
}

// Declarada como función: el motor solo sigue $ fuera del archivo del hook a través de declaraciones.
function gitEn($: $, raiz: string): Git {
  return (args, stdin) => $.process.run(['git', ...args], stdin === undefined ? { cwd: raiz } : { cwd: raiz, stdin })
}
function motivoGit(r: { stderr: string }): string {
  return r.stderr.trim() || 'git no responde'
}

// La D del panel, confirmada: descarta la tarea sin Claude (decisión del propietario, 2026-10-29, precisada por
// «Comandos antes que inferencia»), con «cola.py descartar»: si la rama está en el worktree de otro agente, o es la
// activa con cambios sin commit, no hace nada y dice por qué; si es la activa, pasa antes a develop; borra la rama y
// pasa la tarea a `descartada`, sin sacarla: sale al limpiar Cerradas. Si git falla, no toca la cola.
export async function descartarTarea($: $, id: number, textoTarea: string): Promise<Resultado> {
  if (!(await tareaVigente($, id, textoTarea, descartable)))
    return { ok: false, mensaje: `La ${String(id)} ya no se puede descartar: ha cambiado en la cola.` }
  const r = await cambiarCola($, ['descartar', String(id)])
  return { ok: r.ok, mensaje: conLetra('D', r) }
}

// A propuesta (tarea 243): una tarea en cola y sin rama vuelve a sf/propuestas.md (o al docs/propuestas.md de antes), lo contrario de «A Pendientes» en Propuestas.
// Solo en los proyectos que llevan propuestas: sin propuestas.md, el panel no la ofrece y cola.py no crea el archivo.
export function devolvible(p: { estado?: unknown; rama?: unknown }): boolean {
  return p.estado === 'en-cola' && texto(p.rama) === null
}

// «A propuesta», confirmada, sin Claude, con «cola.py a-propuesta»: si salió de una propuesta, la devuelve a
// «propuesta, pendiente de aprobación»; si no, crea una con su título, su descripción y su tipo. Sale de la cola.
export async function aPropuestaTarea($: $, id: number, textoTarea: string): Promise<Resultado> {
  if (!(await tareaVigente($, id, textoTarea, devolvible)))
    return { ok: false, mensaje: `La ${String(id)} ya no se puede pasar a propuesta: ha cambiado en la cola.` }
  const r = await cambiarCola($, ['a-propuesta', String(id)])
  return { ok: r.ok, mensaje: r.ok ? r.mensaje : `A propuesta: ${r.mensaje}` }
}

// Se cierra con la C una tarea en curso que tiene «Cerrar la tarea» y ningún otro paso sin hacer, salvo el de prueba,
// que la C marca hecho, y las ayudas de prueba, que no se exigen; sin pasos, no hay C (decisiones del propietario,
// 2026-10-29, 172 y 184). Con rama, la rama debe existir; sin rama, también, sin squash ni commit (188).
export function cerrable(p: Peticion, ramas: Record<string, boolean>): boolean {
  return (
    p.estado === 'en-curso' &&
    (p.rama === null || ramas[p.rama] === true) &&
    p.pasos.some(x => x.texto === CERRAR) &&
    p.pasos.every(x => x.estado === 'hecho' || x.ayuda === true || PASOS_DE_CIERRE.includes(x.texto))
  )
}

// Las deliberativas (investigar, deliberar y diseñar) no se prueban ni pasan por observación: se cierran con la C
// (218, 278). Como DELIBERATIVAS de cola.py.
const DELIBERATIVAS = ['investigar', 'deliberar', 'diseñar']
export function observable(p: { tipo?: string | null }): boolean {
  return !DELIBERATIVAS.includes(p.tipo ?? '')
}

// La C del panel, confirmada: cierra la tarea sin Claude (decisión del propietario, 2026-10-29: pulsarla es el OK
// «ciérrala»), con «cola.py cerrar»: si la rama está en otro worktree o hay cambios sin commit, no hace nada y
// dice por qué; pasa la rama a develop por squash, con un commit «<tarea> (N)» y sus pasos hechos, hace push de
// develop (si falla, cierra igual, lo anota y lo dice), borra la rama y saca la tarea de la cola: entra en Cerradas
// con C y su commit. Si hay choques o falla el commit, cola.py lo deshace y vuelve a la rama de antes, y el panel le
// pasa a Claude el cierre para que lo resuelva (decisión del propietario, 2026-10-29: «si falla un cierre pasa al
// agente principal el prompt para resolverlo»).
// «A observación» (241) hace lo mismo con «cola.py a-observacion»: cierra con el mismo squash y la deja en observación.
// Sin rama (188), las dos sacan la tarea sin squash ni commit.
export async function cerrarTarea($: $, id: number, textoTarea: string, rama: string | null, orden: 'cerrar' | 'a-observacion' = 'cerrar'): Promise<Resultado> {
  const vale = (t: Record<string, unknown>) => t.estado === 'en-curso' && texto(t.rama) === rama
  if (!(await tareaVigente($, id, textoTarea, vale)))
    return { ok: false, mensaje: `La ${String(id)} ya no se puede cerrar: ha cambiado en la cola.` }
  const letra = orden === 'cerrar' ? 'C' : 'A observación'
  const r = await cambiarCola($, [orden, String(id)])
  if (r.ok || !r.fallo) return { ok: r.ok, mensaje: conLetra(letra, r) }
  // El cierre que no sale se lo pasa a Claude, con lo que necesita. Desde un temporizador, como la R: el motor no deja
  // enviar un prompt desde el hook que atiende el panel.
  const pedido =
    `${orden === 'cerrar' ? 'Cierra' : 'Pasa a observación'} la ${String(id)} («${textoTarea}»): ${orden === 'cerrar' ? 'la C' : 'A observación'} del panel no pudo, ${r.motivo ?? r.mensaje}. Está deshecho y estás en la rama de antes. ` +
    `Resuélvelo en \`${rama ?? 'develop'}\` (por ejemplo, integrando develop) y repite el cierre con \`${ordenColaClaude()} ${orden} ${String(id)}\`.`
  $.clock.after(50, () => {
    void encargarAClaude($, pedido).catch(err => emergenteError($, `${letra}: no se pudo avisar a Claude (${String(err)}).`))
  })
  return {
    ok: false,
    mensaje:
      r.fallo === 'choques'
        ? `Choques al pasar la ${String(id)} a develop: se lo paso a Claude.`
        : `${letra}: no se pudo hacer el commit de la ${String(id)} en develop: se lo paso a Claude.`,
  }
}

// Cerrar en observación (241, 204): la tarea va bien. Con «cola.py cerrar», sin Claude y sin git: ya entró en develop
// al pasarla a observación; sale de la cola y entra en Cerradas.
export async function cerrarObservada($: $, id: number, textoTarea: string): Promise<Resultado> {
  if (!(await tareaVigente($, id, textoTarea, t => t.estado === 'en-observacion')))
    return { ok: false, mensaje: `La ${String(id)} ya no se puede cerrar: ha cambiado en la cola.` }
  const r = await cambiarCola($, ['cerrar', String(id)])
  return { ok: r.ok, mensaje: conLetra('Cerrar', r) }
}

// «A observación», en las cerradas (296): la cerrada por error vuelve a observación («en-observacion» en la cola) con su commit
// de develop, para seguir vigilándola y poder revertirla. Con «cola.py reobservar», sin Claude y sin git. Solo si sigue
// fuera de la cola; cola.py comprueba además que salió cerrada.
export async function reobservarTarea($: $, id: number): Promise<Resultado> {
  let datos: Record<string, unknown> = {}
  try {
    datos = await leerJson($, `${await raizSesion($)}/${PETICIONES}`)
  } catch {
    // Sin cola legible, decide cola.py.
  }
  const lista = Array.isArray(datos.peticiones) ? (datos.peticiones as Record<string, unknown>[]) : []
  if (lista.some(x => x.id === id)) return { ok: false, mensaje: `La ${String(id)} ya está en la cola.` }
  const r = await cambiarCola($, ['reobservar', String(id)])
  return { ok: r.ok, mensaje: conLetra('A observación', r) }
}

/// RELEASE (decisión del propietario, 2026-10-29): la versión actual, la del último tag vX.Y.Z del repositorio, también
// en la SF («La versión forma parte del manejo del repositorio», 226); sin ninguno, null: se pregunta la primera. Con
// ella, los manifiestos de la configuración a los que se sube (en la SF, el de su plugin).
const SEMVER = /^\d+\.\d+\.\d+$/
export async function versionActual($: $): Promise<FuenteVersion> {
  const raiz = await raizSesion($)
  const conf = await configuracion($, raiz)
  const sf = await $.fs.exists(`${raiz}/${MARCA_SF}`)
  const tags = await gitEn($, raiz)(['tag', '--list', 'v*', '--sort=-v:refname'])
  const ultimo = tags.exitCode === 0 ? tags.stdout.split(/\r?\n/).map(t => t.trim().slice(1)).find(t => SEMVER.test(t)) : undefined
  return { actual: ultimo ?? null, manifiestos: conf.manifiesto, sf }
}

// Las versiones que se ofrecen: las tres que siguen a la actual (patch, minor y major) o, sin ninguna, la primera.
export function siguientesVersiones(v: string | null): string[] {
  if (v === null) return ['0.1.0', '1.0.0']
  const [a, b, c] = v.split('.').map(Number) as [number, number, number]
  return [`${a}.${b}.${c + 1}`, `${a}.${b + 1}.0`, `${a + 1}.0.0`]
}

// La versión nueva en un manifiesto: el texto con ella y la que tenía (null si no tenía, y entonces se escribe), o
// null si no se puede escribir. Solo cambia (o añade) el valor de version: el resto, con su formato, queda igual.
// .json: su clave version (package.json, plugin.json). pyproject.toml: version en [project] o en [tool.poetry].
export function subirManifiesto(original: string, ruta: string, nueva: string): { texto: string; antes: string | null } | null {
  const formato = formatoManifiesto(ruta)
  if (formato === 'json') {
    const m = /("version"\s*:\s*")([^"]*)"/.exec(original)
    if (m) return { texto: original.replace(m[0], `${m[1]!}${nueva}"`), antes: m[2]! }
    const abre = /^(﻿?\s*\{)(\s*)/.exec(original)
    if (!abre) return null
    const sangria = abre[2] || ' '
    return { texto: original.replace(abre[0], `${abre[1]!}${sangria}"version": "${nueva}",${sangria}`), antes: null }
  }
  if (formato === 'pyproject') {
    const seccion = /^\[(project|tool\.poetry)\][ \t]*\r?\n/m.exec(original)
    if (!seccion) return null
    const desde = seccion.index + seccion[0].length
    const resto = original.slice(desde)
    const fin = /^\[/m.exec(resto)?.index ?? resto.length
    const cuerpo = resto.slice(0, fin)
    const v = /^(version\s*=\s*")([^"]*)"/m.exec(cuerpo)
    const nl = seccion[0].endsWith('\r\n') ? '\r\n' : '\n'
    const nuevoCuerpo = v ? cuerpo.replace(v[0], `${v[1]!}${nueva}"`) : `version = "${nueva}"${nl}${cuerpo}`
    return { texto: original.slice(0, desde) + nuevoCuerpo + resto.slice(fin), antes: v ? v[2]! : null }
  }
  return null
}

// RELEASE confirmado: publica `nueva` con git y sin Claude. Antes comprueba que existen la rama que hace de main
// (rama_main de la configuración, 213) y develop, que se está en develop, sin cambios sin commit, que main es
// antecesor de develop (fast-forward posible), que el tag no existe y que la versión no ha cambiado; si algo falla, no
// hace nada y dice cómo arreglarlo. Sube la versión de cada manifiesto de la configuración en un commit «vX.Y.Z» (en
// la SF, «sf X.Y.Z») en develop; un manifiesto sin versión o con otra que la del tag se avisa sin bloquear, y se
// escribe (226). Después pasa develop a main sin cambiar de rama (git fetch . develop:<main>), crea el tag anotado y
// hace push de develop, main y el tag al remoto de la configuración. Si el push falla, lo local queda hecho y lo dice.
// Antes de tocar nada, si el remoto es público, revisa lo que sale (revision.ts, decisión 252).
export async function publicarVersion($: $, fuente: FuenteVersion, nueva: string): Promise<Resultado> {
  const raiz = await raizSesion($)
  const git = gitEn($, raiz)
  const conf = await configuracion($, raiz)
  const main = conf.ramaMain
  const remoto = conf.remoto
  const tag = `v${nueva}`
  for (const r of [main, 'develop']) {
    const hay = await git(['rev-parse', '-q', '--verify', `refs/heads/${r}`])
    if (hay.exitCode !== 0) return { ok: false, mensaje: `RELEASE: el proyecto no tiene la rama ${r}. Créala (se desarrolla en develop y se publica en ${main}) y vuelve a pulsar.` }
  }
  const cabeza = await git(['symbolic-ref', '--short', '-q', 'HEAD'])
  const activa = cabeza.exitCode === 0 ? cabeza.stdout.trim() : null
  if (activa !== 'develop')
    return { ok: false, mensaje: `RELEASE: la rama activa es ${activa ?? 'una cabeza separada'}, no develop. Pasa a develop (git switch develop) y vuelve a pulsar.` }
  const cambios = await git(['status', '--porcelain', '--untracked-files=no'])
  if (cambios.exitCode !== 0) return { ok: false, mensaje: `RELEASE: git no responde (${motivoGit(cambios)}).` }
  if (cambios.stdout.trim()) return { ok: false, mensaje: 'RELEASE: hay cambios sin commit en develop. Haz commit antes (o pídeselo a Claude) y vuelve a pulsar.' }
  const antecesor = await git(['merge-base', '--is-ancestor', main, 'develop'])
  if (antecesor.exitCode === 1)
    return { ok: false, mensaje: `RELEASE: ${main} tiene commits que no están en develop y no se puede pasar por fast-forward. Intégralos en develop (git merge ${main}) y vuelve a pulsar.` }
  if (antecesor.exitCode !== 0) return { ok: false, mensaje: `RELEASE: no se pudo comparar ${main} con develop (${motivoGit(antecesor)}). Comprueba que existe ${main}.` }
  const existe = await git(['rev-parse', '-q', '--verify', `refs/tags/${tag}`])
  if (existe.exitCode === 0) return { ok: false, mensaje: `RELEASE: el tag ${tag} ya existe. Elige otra versión.` }
  const ahora = await versionActual($)
  if (ahora.actual !== fuente.actual || ahora.manifiestos.join('\n') !== fuente.manifiestos.join('\n'))
    return { ok: false, mensaje: `RELEASE: la versión ha cambiado (ahora, ${ahora.actual ?? 'ninguna'}). Vuelve a pulsar RELEASE.` }
  // Lo que sale en esta versión, revisado (decisiones 252 y 259): para, o pide permiso, si encuentra algo.
  const revision = await revisarPublicacion($, raiz, remoto, fuente.actual === null ? null : `v${fuente.actual}`, nueva)
  if (revision) return { ok: false, mensaje: revision }
  // Los manifiestos, con la versión nueva; lo que no cuadra se avisa sin bloquear.
  const avisos: string[] = []
  const escritos: { ruta: string; original: string }[] = []
  for (const rel of fuente.manifiestos) {
    const ruta = `${raiz}/${rel}`
    if (!(await $.fs.exists(ruta))) {
      avisos.push(`no existe ${rel}`)
      continue
    }
    const original = await $.fs.read(ruta)
    const sube = subirManifiesto(original, rel, nueva)
    if (!sube) {
      avisos.push(`${rel} no tiene dónde llevar la versión`)
      continue
    }
    if (sube.antes === null) avisos.push(`${rel} no tenía versión`)
    else if (fuente.actual !== null && sube.antes !== fuente.actual) avisos.push(`${rel} decía ${sube.antes}, no ${fuente.actual}`)
    if (sube.texto === original) continue
    await $.fs.write(ruta, sube.texto)
    escritos.push({ ruta: rel, original })
  }
  const titulo = fuente.sf ? `sf ${nueva}` : tag
  if (escritos.length) {
    const anadido = await git(['add', ...escritos.map(x => x.ruta)])
    const commit = anadido.exitCode === 0 ? await git(['commit', '-q', '-F', '-'], `${titulo}\n${conf.coautor ? `\n${conf.coautor}\n` : ''}`) : anadido
    if (commit.exitCode !== 0) {
      await git(['reset', '-q', '--', ...escritos.map(x => x.ruta)])
      for (const x of escritos) await $.fs.write(`${raiz}/${x.ruta}`, x.original)
      return { ok: false, mensaje: `RELEASE: no se pudo hacer el commit de ${titulo} (${motivoGit(commit)}). No ha cambiado nada.` }
    }
  }
  const avance = await git(['fetch', '.', `develop:${main}`])
  if (avance.exitCode !== 0) {
    if (escritos.length) await git(['reset', '-q', '--keep', 'HEAD~1'])
    await refrescar($)
    return { ok: false, mensaje: `RELEASE: no se pudo pasar develop a ${main} (${motivoGit(avance)}).${escritos.length ? ' Deshecho el commit de la versión.' : ''}` }
  }
  const etiqueta = await git(['tag', '-a', tag, '-m', titulo, main])
  if (etiqueta.exitCode !== 0) {
    await refrescar($)
    return { ok: false, mensaje: `RELEASE: develop está en ${main}, pero no se pudo crear el tag ${tag} (${motivoGit(etiqueta)}). Créalo a mano y haz push.` }
  }
  const push = await git(['push', remoto, 'develop', main, tag])
  await refrescar($)
  const aviso = avisos.length ? ` Aviso: ${avisos.join('; ')}.` : ''
  if (push.exitCode !== 0)
    return { ok: false, mensaje: `Publicada ${tag} en local; falta el push (${motivoGit(push)}). Repite: git push ${remoto} develop ${main} ${tag}.${aviso}` }
  return { ok: true, mensaje: `Publicada ${tag}${aviso ? `.${aviso}` : ''}` }
}

// ACTUALIZAR (decisión del propietario, 2026-10-29): la versión publicada más alta del plugin sf y los scopes que el
// proyecto usa con una instalada más vieja; null si no hay versión nueva o no se puede saber. Sin scopes, es REFRESCAR
// (decisión 177): la sesión corre un plugin más viejo que el instalado, porque otra sesión lo actualizó y esta no lo ha
// recargado (tarea 229). La publicada se consulta en la red al empezar la sesión, cada 5 minutos, con /sf y tras
// publicar con RELEASE; lo instalado y lo que corre, que son archivos locales, cada minuto con el latido, con la última
// publicada conocida (tarea 229, reabierta: otra sesión instala y esta lo ve al minuto, no a los 5). Nunca al pintar.
const actualizacion = atom({ plugin: 'sf', key: 'actualizacion' } as const, null as Actualizacion | null)
const publicadaConocida = atom({ plugin: 'sf', key: 'publicadaConocida' } as const, null as string | null)
const PLUGIN_SF = 'sf@softwarefactory'
const CATALOGO = 'softwarefactory'
export const CADA_COMPROBACION = 5 * 60_000
// La próxima comprobación: el primer latido, que va en minutos exactos, a 5 minutos o más de la última.
export function proximaComprobacion(ultima: number): number {
  return Math.ceil((ultima + CADA_COMPROBACION) / 60_000) * 60_000
}

// El aviso de la etiqueta de la versión: cuánto falta para la próxima comprobación y la hora de la última.
export function avisoComprobacion(ultima: number | null, ahora: number): string {
  if (ultima === null) return 'Versión: aún sin comprobar si hay una nueva'
  const min = Math.ceil((proximaComprobacion(ultima) - ahora) / 60_000)
  const d = new Date(ultima)
  const hora = `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
  return `Próxima comprobación de versión ${min > 0 ? `en ${String(min)} min` : 'en menos de 1 min'} (última, a las ${hora})`
}

// a > b, las dos X.Y.Z.
function mayor(a: string, b: string): boolean {
  const x = a.split('.').map(Number)
  const y = b.split('.').map(Number)
  for (let i = 0; i < 3; i++) if (x[i] !== y[i]) return x[i]! > y[i]!
  return false
}

// Rutas comparables: barras normales, sin la final y, con unidad de Windows, en minúsculas.
function mismaRuta(a: string, b: string): boolean {
  const n = (r: string) => (/^[a-zA-Z]:/.test(normal(r)) ? normal(r).toLowerCase() : normal(r))
  return n(a) === n(b)
}

// La versión del plugin que corre en la sesión; null si no se lee o si corre la copia de trabajo de la SF (la carpeta
// del plugin está en un repositorio, dos niveles por debajo de su raíz), que no se compara con lo instalado.
async function versionQueCorre($: $): Promise<string | null> {
  const raiz = normal($.plugin.root)
  if (await desdeCopia($)) return null
  try {
    const v = texto((await leerJson($, `${raiz}/.claude-plugin/plugin.json`)).version)
    return v !== null && SEMVER.test(v) ? v : null
  } catch {
    return null
  }
}

// La carpeta de los plugins de Claude Code: la de CLAUDE_CONFIG_DIR si está puesta, si no ~/.claude (sin rutas fijas
// de esta máquina, decisión 171).
async function carpetaPlugins($: $): Promise<string | null> {
  const claude = await carpetaClaude($)
  return claude ? `${claude}/plugins` : null
}

// Si sf@softwarefactory está activo en este proyecto, según `enabledPlugins` de los ajustes: manda el local del
// proyecto, luego el del proyecto y luego el del usuario; sin valor en ninguno, activo. Desactivado (en la SF, con el
// plugin de desarrollo en su lugar), sus instalaciones no corren y no cuentan (tarea 229, reabierta).
async function sfActivo($: $, plugins: string, raiz: string): Promise<boolean> {
  const archivos = [`${raiz}/.claude/settings.local.json`, `${raiz}/.claude/settings.json`, `${plugins.replace(/\/plugins$/, '')}/settings.json`]
  for (const a of archivos) {
    try {
      const v = ((await leerJson($, a)).enabledPlugins as Record<string, unknown> | undefined)?.[PLUGIN_SF]
      if (typeof v === 'boolean') return v
    } catch {}
  }
  return true
}

async function buscarActualizacion($: $, red: boolean): Promise<Actualizacion | null> {
  const plugins = await carpetaPlugins($)
  if (!plugins) return null
  const raiz = await raizSesion($)
  if (!(await sfActivo($, plugins, raiz))) return null
  let instaladas: Record<string, unknown>[]
  try {
    const p = (await leerJson($, `${plugins}/installed_plugins.json`)).plugins as Record<string, unknown> | undefined
    instaladas = Array.isArray(p?.[PLUGIN_SF]) ? (p[PLUGIN_SF] as Record<string, unknown>[]) : []
  } catch {
    return null
  }
  // El scope de usuario y los locales o de proyecto de esta carpeta.
  const usadas = instaladas.filter(
    x => x.scope === 'user' || ((x.scope === 'local' || x.scope === 'project') && typeof x.projectPath === 'string' && mismaRuta(x.projectPath, raiz)),
  )
  if (usadas.length === 0) return null
  let publicada: string | null
  if (red) {
    publicada = await versionPublicada($, plugins, raiz)
    await update($, publicadaConocida, () => publicada)
  } else publicada = await read($, publicadaConocida)
  if (publicada !== null) {
    const viejas = usadas.filter(x => typeof x.version === 'string' && SEMVER.test(x.version) && mayor(publicada, x.version))
    if (viejas.length) return { version: publicada, scopes: [...new Set(viejas.map(x => String(x.scope)))] }
  }
  // Lo instalado está al día (o no se sabe la publicada), pero la sesión corre una versión más vieja: REFRESCAR, que
  // recarga el plugin (decisión 177).
  const corre = await versionQueCorre($)
  const instalada = usadas
    .map(x => x.version)
    .filter((v): v is string => typeof v === 'string' && SEMVER.test(v))
    .reduce<string | null>((m, v) => (m === null || mayor(v, m) ? v : m), null)
  return corre !== null && instalada !== null && mayor(instalada, corre) ? { version: instalada, scopes: [], corre } : null
}

// REFRESCAR (decisión 177): la versión ya está instalada y solo hay que recargar el plugin; ACTUALIZAR, hay scopes que
// actualizar.
export const esRefresco = (a: Actualizacion): boolean => a.scopes.length === 0

// El aviso del panel cuando hay que refrescar (decisión 177); null si no.
export function avisoRefresco(a: Actualizacion | null): string | null {
  if (!a || !esRefresco(a)) return null
  return `Esta sesión usa la SF ${a.corre ?? '?'} y está instalada la ${a.version}: pulsa REFRESCAR`
}

// La versión publicada más alta del plugin sf, de los tags vX.Y.Z del catálogo; null si no se puede saber.
async function versionPublicada($: $, plugins: string, raiz: string): Promise<string | null> {
  let url: string | null = null
  try {
    const s = ((await leerJson($, `${plugins}/known_marketplaces.json`))[CATALOGO] as { source?: Record<string, unknown> } | undefined)?.source
    if (s?.source === 'github' && typeof s.repo === 'string') url = `https://github.com/${s.repo}.git`
    else if (s?.source === 'git' && typeof s.url === 'string') url = s.url
  } catch {
    return null
  }
  if (!url) return null
  const r = await $.process.run(['git', 'ls-remote', '--tags', url], { cwd: raiz })
  if (r.exitCode !== 0) return null
  return r.stdout
    .split(/\r?\n/)
    .map(l => /\trefs\/tags\/v(\d+\.\d+\.\d+)$/.exec(l.trim())?.[1])
    .filter((v): v is string => v !== undefined)
    .reduce<string | null>((m, v) => (m === null || mayor(v, m) ? v : m), null)
}

// La hora de la última comprobación en la red: la del latido, /sf o RELEASE, que reinician la cuenta de 5 minutos
// (decisión del propietario, tarea 238); al empezar, la del arranque. La lee el panel al pulsar la etiqueta de la versión.
const comprobadaEn = atom({ plugin: 'sf', key: 'comprobadaEn' } as const, null as number | null)

// Comprueba y guarda el resultado; si algo falla, no hay botón y no se avisa. Sin red, con la última publicada conocida.
// Con red, anota la hora salvo con `anotar: false` (la del arranque, ya anotada con la hora de inicio).
export async function comprobarActualizacion($: $, { red = true, anotar = red }: { red?: boolean; anotar?: boolean } = {}): Promise<void> {
  if (anotar) {
    const t = await $.clock.now()
    await update($, comprobadaEn, () => t)
  }
  const a = await buscarActualizacion($, red).catch(() => null)
  await update($, actualizacion, () => a)
}

// La primera línea del error de una orden.
const errorDe = (r: { stdout: string; stderr: string }) => (r.stderr.trim() || r.stdout.trim() || 'claude no responde').split(/\r?\n/)[0]!

// ACTUALIZAR confirmado: con comandos y sin Claude, primero refresca el catálogo (el clon local puede no tener aún la
// versión que da GitHub) y luego `claude plugin update` en cada scope desactualizado, desde la carpeta del proyecto
// (la de los scopes local y de proyecto). Si el refresco falla, no actualiza; los scopes que fallan siguen en el botón.
// Sin scopes por actualizar (lo instalado ya está al día y la sesión va por detrás), es REFRESCAR (decisión 177): instala
// las dependencias que falten y lanza /reload-plugins.
export async function actualizarPlugin($: $, a: Actualizacion): Promise<Resultado> {
  const raiz = await raizSesion($)
  // Las dependencias instaladas: con alguna nueva, hay que reiniciar; si no, basta recargar (decisión 286).
  let nuevas = 0
  const correr = async (argv: string[]) => {
    const r = await $.process.run(argv, { cwd: raiz }).catch((err: unknown) => ({ exitCode: 1, stdout: '', stderr: String(err) }))
    if (argv[1] === 'plugin' && argv[2] === 'install' && r.exitCode === 0) nuevas++
    return r
  }
  if (a.scopes.length === 0) {
    // Antes de recargar, las dependencias de la versión instalada: sin ellas, sf no carga (decisión 176).
    const falta = await instalarDependencias($, raiz, null, correr, 'REFRESCAR')
    if (falta) return { ok: false, mensaje: falta }
    await update($, actualizacion, () => null)
    lanzar($, 'reload-plugins', '')
    return { ok: true, mensaje: `REFRESCAR: sf v${a.version} ya instalada, recargando los plugins` }
  }
  const c = await correr(['claude', 'plugin', 'marketplace', 'update', CATALOGO])
  if (c.exitCode !== 0) return { ok: false, mensaje: `ACTUALIZAR: no se pudo refrescar el catálogo ${CATALOGO} (${errorDe(c)}).` }
  const fallos: [string, string][] = []
  const alDia: string[] = []
  for (const scope of a.scopes) {
    const r = await correr(['claude', 'plugin', 'update', PLUGIN_SF, '--scope', scope])
    if (r.exitCode !== 0) fallos.push([scope, errorDe(r)])
    else if (/already at the latest version \(([^)]+)\)/.exec(r.stdout)?.[1] === a.version) alDia.push(scope)
  }
  // Las dependencias de la versión nueva que falten, en los scopes actualizados, antes de pedir reiniciar (decisión 176).
  const hechos = a.scopes.filter(s => !fallos.some(([f]) => f === s))
  const falta = hechos.length ? await instalarDependencias($, raiz, hechos, correr) : null
  // Claude Code ya tenía la versión pedida y no ha tocado nada: se anota igualmente en el registro (decisión 124).
  const sinAnotar = alDia.length ? await anotarVersion($, raiz, alDia, a.version).then(() => null, (err: unknown) => String(err)) : null
  const quedan = fallos.map(([s]) => s)
  await update($, actualizacion, () => (quedan.length ? { ...a, scopes: quedan } : null))
  if (fallos.length) return { ok: false, mensaje: `ACTUALIZAR: no se pudo actualizar a v${a.version} (${fallos.map(([s, m]) => `${s}: ${m}`).join('; ')}).` }
  if (falta) return { ok: false, mensaje: falta }
  if (sinAnotar) return { ok: false, mensaje: `ACTUALIZAR: sf ya estaba en v${a.version}, pero no se pudo anotar en el registro (${sinAnotar}).` }
  if (alDia.length === a.scopes.length) return { ok: true, mensaje: `sf ya estaba en v${a.version}: anotado en el registro` }
  if (nuevas > 0) return { ok: true, mensaje: `Actualizado a v${a.version}, con dependencias nuevas: reinicia Claude Code` }
  // Sin dependencias nuevas basta recargar (decisión 286): el botón pasa a REFRESCAR, que recarga con un clic del
  // propietario. El mod no recarga por su cuenta fuera de la incorporación (decisión 103).
  if (a.corre === a.version) return { ok: true, mensaje: `Actualizado a v${a.version}` }
  await update($, actualizacion, () => ({ ...a, scopes: [] }))
  return { ok: true, mensaje: `Actualizado a v${a.version}: pulsa REFRESCAR para cargarla, sin reiniciar` }
}

type Orden = (argv: string[]) => Promise<{ exitCode: number; stdout: string; stderr: string }>

// Interruptor de .sf/proyecto.json (decisión 171): `automatizaciones.dependencias_al_actualizar`, encendido salvo que
// valga false. Sin el archivo o sin la clave, encendido.
async function instalaDependencias($: $, raiz: string): Promise<boolean> {
  try {
    const a = (await leerJson($, `${raiz}/${PROYECTO}`)).automatizaciones as Record<string, unknown> | undefined
    return a?.dependencias_al_actualizar !== false
  } catch {
    return true
  }
}

// «nombre», «nombre@catálogo» o { name, marketplace }: el identificador nombre@catálogo; sin catálogo, el de sf.
function idDependencia(d: unknown): string | null {
  if (typeof d === 'string') return d.includes('@') ? d : `${d}@${CATALOGO}`
  if (d && typeof d === 'object' && typeof (d as { name?: unknown }).name === 'string') {
    const { name, marketplace } = d as { name: string; marketplace?: unknown }
    return `${name}@${typeof marketplace === 'string' ? marketplace : CATALOGO}`
  }
  return null
}

// ACTUALIZAR, medida 2 (decisión 176): `claude plugin update` no instala las dependencias nuevas, y sin una de ellas sf
// no carga, ni su panel. Mientras aún corre la versión vieja, lee las `dependencies` del plugin.json de la versión
// instalada de sf (la que cargará el reinicio o /reload-plugins) en cada scope (null: los del proyecto) e instala con
// `claude plugin install` las que falten, una orden por dependencia (la orden instala solo la primera que se le da).
// Devuelve null si todo está, o el aviso con una orden por línea para las que quedan; con el interruptor apagado, no
// instala nada y avisa de las que faltan (tarea 259).
async function instalarDependencias($: $, raiz: string, scopes: string[] | null, correr: Orden, boton = 'ACTUALIZAR'): Promise<string | null> {
  const instalar = await instalaDependencias($, raiz)
  const plugins = await carpetaPlugins($)
  if (!plugins) return null
  let instaladas: Record<string, Record<string, unknown>[]>
  try {
    instaladas = ((await leerJson($, `${plugins}/installed_plugins.json`)).plugins ?? {}) as Record<string, Record<string, unknown>[]>
  } catch {
    return null
  }
  const delProyecto = (x: Record<string, unknown>) =>
    x.scope === 'user' || ((x.scope === 'local' || x.scope === 'project') && typeof x.projectPath === 'string' && mismaRuta(x.projectPath, raiz))
  const sf = (Array.isArray(instaladas[PLUGIN_SF]) ? instaladas[PLUGIN_SF] : []).filter(
    x => delProyecto(x) && (scopes === null || scopes.includes(String(x.scope))),
  )
  const pendientes: [string, string][] = []
  for (const x of sf) {
    const scope = String(x.scope)
    const carpeta = typeof x.installPath === 'string' ? normal(x.installPath) : `${plugins}/cache/${CATALOGO}/sf/${String(x.version)}`
    let deps: unknown[]
    try {
      const d = (await leerJson($, `${carpeta}/.claude-plugin/plugin.json`)).dependencies
      deps = Array.isArray(d) ? d : []
    } catch {
      continue
    }
    for (const id of deps.map(idDependencia).filter((v): v is string => v !== null)) {
      // Vale la del mismo scope (la local o de proyecto, de esta carpeta) o la de usuario, que alcanza a todos.
      const hay = (Array.isArray(instaladas[id]) ? instaladas[id] : []).some(
        y => y.scope === 'user' || (y.scope === scope && typeof y.projectPath === 'string' && mismaRuta(y.projectPath, raiz)),
      )
      if (!hay && !pendientes.some(([i, s]) => i === id && s === scope)) pendientes.push([id, scope])
    }
  }
  // La de usuario alcanza a todos los scopes: si hay que instalarla en el de usuario, no se repite en los demás.
  const aInstalar = pendientes.filter(([id, s]) => s === 'user' || !pendientes.some(([i, t]) => i === id && t === 'user'))
  if (!instalar) return avisoDependencias(boton, 'no están instaladas', aInstalar)
  const fallidas: [string, string][] = []
  let motivo = ''
  for (const [id, scope] of aInstalar) {
    const r = await correr(['claude', 'plugin', 'install', id, '--scope', scope])
    if (r.exitCode !== 0) {
      fallidas.push([id, scope])
      motivo ||= errorDe(r)
    }
  }
  return avisoDependencias(boton, `no se pudieron instalar (${motivo})`, fallidas)
}

// El aviso de las dependencias que quedan por instalar, con una orden por línea; null si no queda ninguna.
export function avisoDependencias(boton: string, porque: string, quedan: [string, string][]): string | null {
  if (quedan.length === 0) return null
  const ordenes = quedan.map(([id, scope]) => `claude plugin install ${id} --scope ${scope}`).join('\n')
  return `${boton}: sf necesita ${[...new Set(quedan.map(([id]) => id))].join(', ')} y ${porque}. Sin ellas, sf no carga: no recargues ni reinicies hasta instalarlas a mano, una orden por línea:\n${ordenes}`
}

// Pone la versión de sf@softwarefactory en installed_plugins.json para esos scopes (los locales y de proyecto, solo
// los de esta carpeta).
async function anotarVersion($: $, raiz: string, scopes: string[], version: string): Promise<void> {
  const plugins = await carpetaPlugins($)
  if (!plugins) throw new Error('sin carpeta de usuario')
  const ruta = `${plugins}/installed_plugins.json`
  const datos = await leerJson($, ruta)
  const lista = (datos.plugins as Record<string, unknown> | undefined)?.[PLUGIN_SF]
  if (!Array.isArray(lista)) throw new Error(`${PLUGIN_SF} no está en ${ruta}`)
  const ahora = new Date(await $.clock.now()).toISOString()
  let anotadas = 0
  for (const x of lista as Record<string, unknown>[]) {
    const nuestra = x.scope === 'user' || (typeof x.projectPath === 'string' && mismaRuta(x.projectPath, raiz))
    if (typeof x.scope === 'string' && scopes.includes(x.scope) && nuestra) {
      Object.assign(x, { version, lastUpdated: ahora })
      anotadas++
    }
  }
  if (anotadas === 0) throw new Error(`ningún scope ${scopes.join(', ')} de este proyecto en ${ruta}`)
  await $.fs.write(ruta, JSON.stringify(datos, null, 2) + '\n')
  // Comprueba que se ha escrito: el motor puede no dejar escribir ahí.
  const leida = ((await leerJson($, ruta)).plugins as Record<string, Record<string, unknown>[]>)[PLUGIN_SF] ?? []
  if (!leida.some(x => scopes.includes(String(x.scope)) && x.version === version)) throw new Error(`${ruta} no ha cambiado`)
}

// La R del panel, confirmada: revierte en develop una tarea cerrada o en observación, sin Claude (decisión del
// propietario, 2026-10-29), con «cola.py revertir», que lee sus commits del historial (o, sin él, de develop): con
// cambios sin commit o con develop en otro worktree, no hace nada y dice por qué; si la rama activa no es develop, pasa
// a develop y se queda en ella; `git revert --no-edit` de sus commits, el más reciente primero, sin push: el push es
// del cierre. Después, según `destino` (decisión 134), la tarea sale de la cola sin rastro, como con la E
// («eliminar»), o vuelve a Pendientes, en cola y reabierta, sin rama («pendiente»); nunca queda en Cerradas con R. Si
// hay choques, cola.py lo deshace y vuelve a la rama de antes, sin tocar la cola, y el panel se lo pasa a Claude.
// `hashes`: los commits de develop con los que se pintó el botón; si develop ha cambiado desde entonces, no hace nada.
export type DestinoRevertir = 'eliminar' | 'pendiente'
export async function revertirTarea($: $, id: number, textoTarea: string, hashes: string[], destino: DestinoRevertir): Promise<Resultado> {
  const raiz = await raizSesion($)
  if (hashes.length > 0) {
    const carpeta = await carpetaGit($, raiz)
    const ahora = carpeta ? (await leerMergeadas($, raiz, carpeta, true))[String(id)] ?? [] : []
    if (ahora.join(' ') !== hashes.join(' ')) return { ok: false, mensaje: `La ${String(id)} ya no se puede revertir: ha cambiado en develop.` }
  }
  const r = await cambiarCola($, ['revertir', String(id), `--${destino}`])
  if (r.ok || !r.fallo) return { ok: r.ok, mensaje: conLetra('R', r) }
  const despues = destino === 'eliminar' ? `y elimínala con \`${ordenColaClaude()} revertir ${String(id)} --eliminar\`` : `y déjala en Pendientes con \`${ordenColaClaude()} revertir ${String(id)} --pendiente\``
  const pedido = `La R del panel no ha podido revertir la ${String(id)} («${textoTarea}») en develop: ${r.motivo ?? r.mensaje}. Ha hecho git revert --abort y ha vuelto a la rama de antes. Revierte la tarea en develop resolviendo los choques, sin push, ${despues} (o, ya revertida a mano, con --commit).`
  $.clock.after(50, () => {
    void encargarAClaude($, pedido).catch(err => emergenteError($, `R: no se pudo pasar a Claude: ${String(err)}`))
  })
  return { ok: false, mensaje: `Choques al revertir la ${String(id)}: se lo paso a Claude.` }
}

// Se prueba en su rama una tarea con rama, en cola, en curso o en observación, si la rama existe y no es la activa
// (decisión del propietario, 2026-10-29).
export function probable(p: { estado?: unknown; rama?: unknown }, ramas: Record<string, boolean>, activa: Estado['rama']): boolean {
  const rama = texto(p.rama)
  return (
    (p.estado === 'en-cola' || p.estado === 'en-curso' || p.estado === 'en-observacion') &&
    rama !== null &&
    ramas[rama] === true &&
    !(activa !== null && !activa.separada && activa.nombre === rama)
  )
}

// Activar rama (antes la letra T): pone la tarea en prueba activando su rama, sin darla por buena y sin pasar por
// Claude: lo que se puede hacer con un comando se hace sin inferencia (decisión del propietario, 2026-10-29). Un clic,
// sin confirmar, con «cola.py probar»: no cambia de rama si hay cambios sin commit o si la rama está en otro worktree,
// y devuelve el motivo. Una tarea en cola pasa a en curso; no recarga el plugin, que queda a cargo del propietario.
// Activada la rama, abre en el navegador los .html que cambia respecto a develop (tarea 206).
// Antes de activarla, cola.py integra develop en ella (270). Si choca, o si la rama auxiliar del subagente tiene
// commits sin traer, no la activa y da «fallo»: el panel se lo pasa a Claude, como el cierre fallido, para que lo
// resuelva el subagente de la tarea («Activar rama integra develop…», 191).
export async function probarTarea($: $, id: number, rama: string): Promise<Resultado> {
  if (!(await tareaVigente($, id, null, t => texto(t.rama) === rama)))
    return { ok: false, mensaje: `La ${String(id)} ya no tiene la rama ${rama}: ha cambiado en la cola.` }
  const r = await cambiarCola($, ['probar', String(id)])
  if (!r.ok && r.fallo) {
    const sinTraer = r.fallo === 'sin-traer'
    const pedido =
      `Activa la rama de la ${String(id)}: «Activar rama» del panel no pudo, ${r.motivo ?? r.mensaje}. No se ha activado y \`${rama}\` está como estaba. ` +
      (sinTraer
        ? 'Que su subagente termine y trae sus commits con `git merge --ff-only`; '
        : `Que su subagente lo resuelva integrando develop en su rama y tráelo a \`${rama}\`; `) +
      `luego repite con \`${ordenColaClaude()} probar ${String(id)}\`.`
    $.clock.after(50, () => {
      void encargarAClaude($, pedido).catch(err => emergenteError($, `Activar rama: no se pudo avisar a Claude (${String(err)}).`))
    })
    return {
      ok: false,
      mensaje: sinTraer
        ? `La ${String(id)} tiene trabajo del subagente sin traer: se lo paso a Claude.`
        : `Choques al integrar develop en la ${String(id)}: se lo paso a Claude.`,
    }
  }
  if (!r.ok) return { ok: false, mensaje: conLetra('Activar rama', r) }
  const abiertos = await abrirDocumentos($, await raizSesion($), rama)
  return { ok: true, mensaje: r.mensaje + abiertos }
}

// Con la rama ya activa, Activar rama abre en el navegador los .html que la rama cambia respecto a develop, todos, sin
// Claude (tarea 206). Los saca git; los borrados no. Los abre abrirArchivo. Devuelve lo que se añade al aviso de Activar rama: nada si no hay ninguno.
export async function abrirDocumentos($: $, raiz: string, rama: string): Promise<string> {
  const r = await gitEn($, raiz)(['diff', '-z', '--name-only', '--diff-filter=d', `develop...${rama}`, '--', '*.html']).catch(() => null)
  if (!r || r.exitCode !== 0) return ''
  const rutas = r.stdout.split('\0').filter(Boolean)
  if (!rutas.length) return ''
  const fallidos: string[] = []
  for (const ruta of rutas) if ((await abrirArchivo($, `${raiz}/${ruta}`)) !== null) fallidos.push(ruta)
  const abiertos = rutas.length - fallidos.length
  const dicho = abiertos ? ` Abiertos en el navegador: ${rutas.filter(x => !fallidos.includes(x)).join(', ')}.` : ''
  return dicho + (fallidos.length ? ` No se ha podido abrir: ${fallidos.join(', ')}.` : '')
}

// El botón de Cerradas: quita de la lista las cerradas (C), las descartadas (D) y las revertidas (R, de antes de la
// decisión 134), y saca de la cola las descartadas, con «cola.py limpiar». Cada una se apunta con la fecha de su último cierre: si vuelve a
// cerrarse (o se reabre), vuelve a la lista.
export async function limpiarCerradas($: $, quitar: { id: number; fecha: number }[], conDescartadas: boolean): Promise<string | null> {
  await update($, sesion, v => ({ limpiadas: { ...(v.limpiadas ?? {}), ...Object.fromEntries(quitar.map(c => [String(c.id), c.fecha])) } }))
  if (!conDescartadas) return null
  const r = await cambiarCola($, ['limpiar'])
  return r.ok ? null : `limpiar: ${r.mensaje}`
}

// La E del panel, confirmada: saca la tarea de la cola con «cola.py eliminar», sin pasar por Cerradas (decisión del
// propietario, 2026-10-29); su historial queda en .sf/historial.jsonl, de donde se restaura. Solo si sigue siendo la
// misma y eliminable: Claude puede haber cambiado la cola entretanto. Devuelve el aviso si no la elimina.
export async function eliminarTarea($: $, id: number, textoTarea: string): Promise<string | null> {
  if (!(await tareaVigente($, id, textoTarea, eliminable))) return `La ${String(id)} ya no se puede eliminar: ha cambiado en la cola.`
  const r = await cambiarCola($, ['eliminar', String(id)])
  return r.ok ? null : conLetra('E', r)
}

// El «?» de los pasos de cierre enseña el flujo de tareas a quien no conoce la SF (tarea 253): dónde está el paso,
// del trabajo en la rama a develop, y qué hacer ahora con la tarea.
function explicacionCierre(id: number, texto: string, estado: string): string {
  const n = String(id)
  const centro =
    texto === CERRAR
      ? `Céntrate en «Cerrar la tarea»: lleva la rama a develop en un solo commit (squash), recoge al subagente que la trabajó y saca la tarea de la cola; además, pulsarlo es el OK del propietario al resultado. Cuenta también qué hace antes «Activar rama para poder probar»`
      : `Céntrate en «Activar rama para poder probar»: deja esa rama activa en la sesión para probar el resultado, recargando el plugin si hace falta, y con eso el paso queda hecho; activarla no es dar la tarea por buena. Cuenta también qué hace después «Cerrar la tarea»: lleva la rama a develop en un solo commit (squash), recoge al subagente y saca la tarea de la cola, y es el OK del propietario`
  return (
    `Explícame el paso «${texto}» de la ${n} (${estado}) para alguien que no conoce la Software Factory, en sencillo y sin dar nada por sabido: dónde está este paso dentro del flujo de una tarea. ` +
    `La tarea se trabaja en su propia rama, feature/${n}-…, que sale de develop. ${centro}. ` +
    `Explica para qué sirve En observación (la tarea ya está en develop y se vigila cómo funciona con el uso, para cerrarla si va bien o revertirla si va mal) y qué pasa si se cierra sin probarla en su rama. ` +
    `Acaba con qué conviene hacer ahora con la ${n}, según cómo está. Solo explicarlo; no lo hagas ni cambies nada.`
  )
}

// El «?» de un paso: pide a Claude que lo explique, sin tocar la cola (decisión del propietario, 2026-10-28). Los de
// cierre, con el flujo de tareas (253).
export function preguntarPaso($: $, id: number, paso: Paso): void {
  const estado = { hecho: 'hecho', 'en-curso': 'en curso', pendiente: 'pendiente' }[paso.estado]
  const texto =
    paso.texto === PROBAR || paso.texto === PROBAR_ANTES || paso.texto === CERRAR
      ? explicacionCierre(id, paso.texto === CERRAR ? CERRAR : PROBAR, estado)
      : `Explícame el paso «${paso.texto}» de la ${String(id)} (${estado}): qué es, qué se ha hecho y qué falta. Solo explicarlo; no lo hagas ni cambies nada.`
  $.clock.after(50, () => {
    void encargarAClaude($, texto).catch(err => emergenteError($, `«?»: no se pudo preguntar a Claude: ${String(err)}`))
  })
}

// El «?» del menú de una tarea (254): pide a Claude que explique la tarea al propietario, breve y sencillo, sin tocar
// la cola; como el «?» de los pasos. Devuelve lo que se dice al propietario.
export function explicarTarea($: $, id: number, textoTarea: string): string {
  const texto =
    `Explícame la ${String(id)} («${textoTarea}») de forma breve y sencilla, para alguien que no ha seguido los detalles: ` +
    'qué es, en qué punto está y qué espera de mí. Solo explicarla; no hagas ni cambies nada.'
  $.clock.after(50, () => {
    void encargarAClaude($, texto).catch(err => emergenteError($, `«?»: no se pudo preguntar a Claude: ${String(err)}`))
  })
  return `«?»: le pido a Claude que explique la ${String(id)}.`
}

// /sf_redescribir N (decisión del propietario, 2026-10-30): pide a Claude que vuelva a redactar la descripción de la N
// para que se lea fácilmente, y la guarde con cola.py redescribir. Devuelve lo que se dice al propietario.
export function pedirRedescripcion($: $, peticiones: Peticion[], args: string): string {
  const id = Number(/^\s*(\d+)\s*$/.exec(args)?.[1])
  if (!id) return 'Uso: /sf_redescribir 162'
  const p = peticiones.find(x => x.id === id)
  if (!p) return `La ${String(id)} no está en la cola.`
  if (!p.descripcion) return `La ${String(id)} no tiene descripción.`
  const texto =
    `Redacta de nuevo la descripción de la ${String(id)} («${p.texto}») para que se lea fácilmente: frases claras y cortas, ` +
    'sin quitar ni añadir nada de lo que dice, cada idea en su párrafo, separados por una línea en blanco. ' +
    `Enséñame la propuesta y espera mi OK; solo entonces guárdala con \`${ordenColaClaude()} redescribir ${String(id)}\`.`
  $.clock.after(50, () => {
    void encargarAClaude($, texto).catch(err => emergenteError($, `/sf_redescribir: no se pudo pasar a Claude (${String(err)}).`))
  })
  return `/sf_redescribir: se lo paso a Claude.`
}

// /sf_config (tarea 299; «La configuración se cambia pidiéndoselo a Claude, con menús», 228, corregida el mismo día):
// pasa a Claude cambiar la configuración del proyecto con la skill sf:configurar_proyecto, sin tarea y fuera del panel.
// Lo que siga a la orden («/sf_config idioma») es lo que el propietario quiere cambiar. Fuera de un proyecto
// incorporado, o en la propia SF, lo dice y no pide nada.
export async function pedirConfiguracion($: $, args: string): Promise<string> {
  const raiz = await raizSesion($)
  if (await $.fs.exists(`${raiz}/${MARCA_SF}`))
    return '/sf_config: la SF no tiene .sf/proyecto.json; su configuración sale de su marca.'
  if (!(await $.fs.exists(`${raiz}/${PROYECTO}`)))
    return '/sf_config: este proyecto no está incorporado a la SF. Pide a Claude «incorpora el proyecto a la SF».'
  const pedido = args.trim()
  const texto =
    'Cambia la configuración del proyecto con la skill sf:configurar_proyecto: enséñame lo que hay, pregúntame qué cambiar con menús, ' +
    'pide mi OK y aplícalo en develop con su commit, sin tarea.' +
    (pedido ? ` Quiero cambiar: «${pedido}».` : '')
  $.clock.after(50, () => {
    void encargarAClaude($, texto).catch(err => emergenteError($, `/sf_config: no se pudo pasar a Claude (${String(err)}).`))
  })
  return '/sf_config: se lo paso a Claude.'
}

// TURBO, en la cabecera («TURBO pone en curso las tareas que no necesitan al propietario», 160): pide a Claude que
// ponga en curso, cada una con su subagente, las tareas de la cola que no necesitan al propietario, y que lance el
// de las en curso que aún no lo tienen. Desde un temporizador: el motor no deja enviar un prompt desde el hook que
// atiende el panel.
export const PROMPT_TURBO =
  'TURBO: pon en curso, cada una con su subagente, las tareas de la cola que se pueden hacer sin interactuar con el propietario; lanza también el subagente de las tareas en curso que aún no lo tienen, y avísame de cuáles.'
export function pedirTurbo($: $): void {
  $.clock.after(50, () => {
    void encargarAClaude($, PROMPT_TURBO).catch(err => emergenteError($, `TURBO: no se pudo pasar a Claude: ${String(err)}`))
  })
  emergente($, 'TURBO: se lo paso a Claude.')
}

// La pastilla de la bienvenida, un botón (decisión 248): pasa a Claude «incorpora este proyecto a la SF» como si lo
// escribiera el propietario. Desde un temporizador, como TURBO: el motor no deja enviar un prompt desde el hook que
// atiende el panel.
export function pedirIncorporar($: $, texto: string): void {
  $.clock.after(50, () => {
    void encargarAClaude($, texto).catch(err => emergenteError($, `No se pudo pasar a Claude «${texto}»: ${String(err)}`))
  })
  emergente($, `Se lo paso a Claude: «${texto}».`)
}

// /sf_split (decisión del propietario, 2026-10-29): se separan pasos de una tarea en curso o en cola en una tarea
// nueva. Hacen falta dos pasos o más: separarlos todos es renombrarla.
export function separable(p: Peticion): boolean {
  return (p.estado === 'en-curso' || p.estado === 'en-cola') && p.pasos.length >= 2
}

// La S del panel (decisión del propietario, 2026-10-29): en las tareas en cola o en curso con dos pasos pendientes o
// más. Los de cierre no cuentan: no se separan (decisión del propietario, 2026-10-29).
const separablePaso = (x: Paso) => !PASOS_DE_CIERRE.includes(x.texto) && x.ayuda !== true
export function separablePendientes(p: Peticion): boolean {
  return (
    (p.estado === 'en-curso' || p.estado === 'en-cola') &&
    p.pasos.filter(x => x.estado === 'pendiente' && separablePaso(x)).length >= 2
  )
}

// Números de paso: «2,3», «2 3» o, de la respuesta de varios elegidos, «2 Texto, 3 Texto» (cada etiqueta empieza
// por su número).
export function numerosDe(t: string): number[] {
  const trozos = /^[\d\s,]+$/.test(t) ? t.split(/[\s,]+/) : t.split(',').map(x => /^\s*(\d+)/.exec(x)?.[1] ?? '')
  return trozos.filter(x => x !== '').map(Number)
}

// Etiqueta de una opción del diálogo: sin comas, que separan las elegidas en la respuesta.
export const etiqueta = (n: number, t: string) => `${String(n)} ${t}`.replace(/,/g, ' ').slice(0, 60)

// /sf_split con la tarea ya elegida: pregunta qué pasos, con varios a la vez; con `soloPendientes` (la S del panel),
// solo los pendientes, cada uno con su número en la tarea. El diálogo admite cuatro opciones como mucho: con más
// pasos, en vez de preguntar, se listan y se pide la forma corta. Devuelve la línea para el propietario; null si
// pregunta.
export function elegirPasos($: $, p: Peticion, soloPendientes = false): string | null {
  const opciones = p.pasos
    .map((x, i) => ({ n: i + 1, x }))
    .filter(({ x }) => separablePaso(x) && (!soloPendientes || x.estado === 'pendiente'))
  if (opciones.length > 4) {
    const lista = opciones.map(({ n, x }) => `${String(n)} ${x.texto}`).join(' · ')
    // La orden primero: el aviso emergente se corta por el final (tarea 257).
    return `/sf_split ${String(p.id)} 2,3 con los pasos que separas. ${soloPendientes ? 'Pendientes' : 'Pasos'}: ${lista}`
  }
  $.clock.after(50, () => {
    void $.ui
      .ask(`¿Qué pasos de la ${String(p.id)} separas en una tarea nueva?`, {
        header: '/sf_split',
        options: opciones.map(({ n, x }) => etiqueta(n, x.texto)),
        multiSelect: true,
      })
      .then(async r => {
        const nums = numerosDe(r)
        const motivo = motivoSplit(p, p.id, nums)
        if (motivo) emergenteError($, motivo)
        else emergente($, await pedirSplit($, p, nums))
      })
      .catch(() => undefined)
  })
  return null
}

// El motivo por el que no se puede pedir el /sf_split, o null si se puede. Los números de paso empiezan en 1, en el
// orden en que salen al desplegar la tarea. Sin números, solo se mira la tarea.
export function motivoSplit(p: Peticion | undefined, id: number, numeros?: number[]): string | null {
  if (!p || (p.estado !== 'en-curso' && p.estado !== 'en-cola')) return `La ${String(id)} no está en curso ni en cola.`
  if (p.pasos.length === 0) return `La ${String(id)} no tiene pasos que separar.`
  if (p.pasos.length === 1) return `La ${String(id)} solo tiene un paso: separarlo es renombrarla.`
  if (!numeros) return null
  if (numeros.length === 0) return `Di qué pasos de la ${String(id)} separas: /sf_split ${String(id)} 2,3`
  const fuera = numeros.find(n => n < 1 || n > p.pasos.length)
  if (fuera !== undefined) return `La ${String(id)} no tiene paso ${String(fuera)}: tiene ${String(p.pasos.length)}.`
  if (new Set(numeros).size === p.pasos.length)
    return `No se pueden separar todos los pasos de la ${String(id)}: eso es renombrarla.`
  return null
}

// «2 y 3», «2, 3 y 4».
const enumerar = (l: string[]) => (l.length < 2 ? l.join('') : `${l.slice(0, -1).join(', ')} y ${l.at(-1)!}`)

// /sf_split, sin Claude: separar pasos es mover datos de la cola (decisión del propietario, 2026-10-29: lo que se
// pueda hacer con un comando, sin inferencia), con «cola.py split». Antes se relee: si la tarea o sus pasos ya no son
// los que vio el propietario (`vista`), avisa y no cambia nada. La nueva va en cola, sin rama, con los pasos y su
// estado, y se llama como su primer paso; su número, el siguiente al último dado. Devuelve la línea que lo resume.
export async function pedirSplit($: $, vista: Peticion, numeros: number[]): Promise<string> {
  const id = vista.id
  const igual = await tareaVigente($, id, vista.texto, t => {
    const pasos = leerPasos(t.pasos)
    return (
      (t.estado === 'en-curso' || t.estado === 'en-cola') &&
      pasos.length === vista.pasos.length &&
      pasos.every((x, i) => x.texto === vista.pasos[i]!.texto)
    )
  })
  if (!igual) return `/sf_split: la ${String(id)} ha cambiado; mírala y vuelve a pedirlo.`
  const nums = [...new Set(numeros)].sort((a, b) => a - b)
  const r = await cambiarCola($, ['split', String(id), nums.join(',')])
  return r.ok ? r.mensaje : `/sf_split: ${r.mensaje}`
}

// /sf_fusionar (decisión del propietario, 2026-10-29): junta en una tareas en cola o en curso. Las en observación, las
// descartadas y las que no están en la cola no se fusionan.
export function fusionable(p: Peticion): boolean {
  return p.estado === 'en-curso' || p.estado === 'en-cola'
}

// El motivo por el que no se pueden fusionar las tareas `ids`, o null si se puede. Las ramas las mira cola.py, que ve
// git: con varias, fusiona si las que sobran ya no existen o están integradas en la de destino.
export function motivoFusion(peticiones: Peticion[], ids: number[]): string | null {
  const unicos = [...new Set(ids)]
  if (unicos.length < 2) return 'Hacen falta dos tareas o más: /sf_fusionar 104 105'
  for (const id of unicos) {
    const p = peticiones.find(x => x.id === id)
    if (!p) return `La ${String(id)} no está en la cola.`
    if (p.estado === 'en-observacion') return `La ${String(id)} está en observación: no se fusiona.`
    if (!fusionable(p)) return `La ${String(id)} está descartada: no se fusiona.`
  }
  return null
}

// /sf_fusionar, sin Claude, como /sf_split, con «cola.py fusionar». Queda la de número más alto, con su número y su nombre:
// el hueco queda en el histórico. Reúne los pasos de todas por orden de tarea, cada uno con su estado; una sin pasos
// aporta uno con su nombre. Pasa a en curso si alguna lo estaba. Las demás salen de la cola sin cerrarse, absorbidas.
// Antes se relee: si alguna ya no es la que vio el propietario (`vistas`), avisa y no cambia nada. Devuelve la línea
// que lo resume.
export async function pedirFusion($: $, vistas: Peticion[]): Promise<string> {
  const orden = [...vistas].sort((a, b) => a.id - b.id)
  for (const v of orden) {
    const igual = await tareaVigente($, v.id, v.texto, c => {
      const pasos = leerPasos(c.pasos)
      return (
        (c.estado === 'en-curso' || c.estado === 'en-cola') &&
        texto(c.rama) === v.rama &&
        pasos.length === v.pasos.length &&
        pasos.every((x, j) => x.texto === v.pasos[j]!.texto)
      )
    })
    if (!igual) return `/sf_fusionar: la ${String(v.id)} ha cambiado; mírala y vuelve a pedirlo.`
  }
  const r = await cambiarCola($, ['fusionar', ...orden.map(v => String(v.id))])
  return r.ok ? r.mensaje : `/sf_fusionar: ${r.mensaje}`
}

// «A Pendientes» en una propuesta (sf/propuestas.md del proyecto, por decidir; antes, la «→»): pasa a tarea en su cola, con su título como
// texto, su resumen como descripción y su «Tipo», si lo tiene, como tipo, con «cola.py de-propuesta», sin Claude.
// cola.py cambia su «Estado» por «pasada a la tarea N de la cola el <fecha>», que ya no dice «pendiente de…», así que
// sale de la lista y no se pasa dos veces, con su propio commit en develop, aunque la rama activa sea otra (tarea 273);
// si la propuesta ya no está por decidir en develop, o no puede hacer el commit, no crea la tarea y lo dice.
export async function convertirPropuesta($: $, pr: Realimentacion['porRevisar'][number]): Promise<string> {
  const args = ['de-propuesta', pr.titulo, ...(pr.numero ? ['--numero', pr.numero] : []),
    ...(pr.resumen ? ['--descripcion', pr.resumen] : []), ...(pr.tipo ? ['--tipo', pr.tipo] : [])]
  const c = await ordenCola($, args)
  await refrescar($)
  return c.ok ? `Tarea ${String(c.id ?? '?')} en cola: ${pr.titulo}` : `A Pendientes: ${c.mensaje}`
}

export async function refrescar($: $): Promise<Estado> {
  raicesConocidas.clear()
  // Sin inicio de la sesión (el estado se acaba de vaciar al cambiar de plugin y aún no ha pasado cargar), desde
  // ahora: con 0, Cerradas contaría todo lo cerrado desde el principio del historial (tarea 350).
  const nuevo = await leerEstado($, (await read($, inicioSesion)) || (await $.clock.now()))
  await update($, estado, () => nuevo)
  await ponerIdentidad($, nuevo).catch(() => undefined)
  const rf = nuevo.realimentacion
  if (rf) {
    if (titulosInicio === null) titulosInicio = new Set(rf.titulos)
    const inicio = titulosInicio
    const n = rf.titulos.filter(t => !inicio.has(t)).length
    await update($, nuevasEnSf, () => n)
  }
  return nuevo
}

// Solo los subagentes, para el latido: si cambian, el panel quita o pone la ⚙ sin releer todo el estado.
export async function refrescarSubagentes($: $): Promise<void> {
  const ahora = await subagentesDeTareas($)
  const actual = await read($, estado)
  if (!actual) return
  const antes = { subagentes: actual.subagentes, subagentesEsperando: actual.subagentesEsperando ?? {} }
  if (JSON.stringify(antes) === JSON.stringify(ahora)) return
  await update($, estado, e => (e ? { ...e, ...ahora } : e))
}

// Arranque: primero termina el de Claude Code (next) y después se lee. Si no sale ni la SF ni un proyecto, se
// vuelve a mirar a los 2 s. Lo visto queda en el registro de depuración (claude --debug).
// Al empezar la sesión (`primera`; no al recargar el plugin), las descartadas que quedaron de otra salen de la cola con
// «cola.py limpiar» (decisión del propietario, 2026-10-29): su descarte es de antes de la sesión, así que no entran en
// Cerradas.
export async function arrancar($: $, primera = false): Promise<void> {
  let est = await refrescar($)
  $.ui.log(
    `arranque: root «${await $.session.root()}», cwd «${await $.session.cwd()}», raíz «${await raizSesion($)}» → ${est.tipo}`,
    { to: 'debug' },
  )
  if (primera && est.peticiones.some(p => p.estado === 'descartada')) {
    const r = await cambiarCola($, ['limpiar']).catch(() => null)
    if (r && !r.ok) $.ui.log(`arranque, limpiar: ${r.mensaje}`, { to: 'debug' })
    est = (await read($, estado)) ?? est
  }
  if (est.tipo === 'sin-sf') {
    $.clock.after(2000, async () => {
      const otra = await refrescar($)
      $.ui.log(`arranque, a los 2 s → ${otra.tipo}`, { to: 'debug' })
    })
  }
}
