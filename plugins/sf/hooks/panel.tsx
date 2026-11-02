import { atom, read, update } from 'claude-code'
import type { Register, RenderChildren } from 'claude-code'
import type { Actualizacion, Cerrada, Estado, FuenteVersion, Paso, Peticion, Prueba, Sesion } from '../types'
import { actualizarPlugin, aPropuestaTarea, devolvible, avisoComprobacion, avisoRefresco, esRefresco, cerrable, cerrarTarea, cerrarObservada, reobservarTarea, comprobarActualizacion, convertirPropuesta, descartable, descartarTarea, elegirPasos, eliminable, eliminarTarea, enCursoOObservando, explicarTarea, enCursoRecientes, limpiarCerradas, porCambio, pasoQuitable, pedirRedescripcion, pedirTurbo, preguntarPaso, probable, probarTarea, publicarVersion, revertibleEnObservacion, siguientesVersiones, versionActual, quitarPaso, revertirTarea, separablePendientes, tareaPrincipal } from './cola'
import { CLAVE_PLEGADO, COLORES, EJEMPLO_ESTADO, ESTADO, FASES, FONDO_BLOQUE, PANEL, PLEGADAS_DE_INICIO, PROYECTO, RGB, ejemploProyecto } from './constantes'
import { COLOR_ACTUALIZAR, COLOR_AVISO, COLOR_ORDEN_DESTRUCTIVA, COLOR_RELEASE, FONDO_AVISO, FONDO_AVISO_ALTERNO, FONDO_ORDEN, MARCA_SUBAGENTE, COLOR_TURBO, COLOR_TAREA, FONDO_ETIQUETA, LETRA, anchoComun, centrar, huecos, TEXTO_PASO, TEXTO_TAREA, colorLetra, colorLetraApagada, hueco, puntosDe } from './estilo'
import { atrasada, commitsDe, creadaEn, cuentaPasos, texto, ultimoCierre } from './lectura'
import { AVISO_PANTALLA, anotarPantalla, sinPantallaCompleta } from './pantalla'
import { COLOR_PRUEBA, cambiarPrueba, desdeCopia } from './prueba'
import type { $ } from './lectura'
import { emergente, emergenteError, emergenteRespuesta } from './emergentes'

// Valores de estado del mod: el motor exige declararlos en el archivo que los usa; con el mismo
// plugin y clave, son el mismo valor en todos los archivos.
// Cambiar la etiqueta si cambian los campos de Estado.
const estado = atom({ plugin: 'sf', key: 'estado' } as const, null, {
  shape: 'estado-16',
})
// Propuestas añadidas en esta sesión de la SF: títulos nuevos respecto a los del inicio.
// Prompts enviados por el propietario en esta sesión.
const prompts = atom({ plugin: 'sf', key: 'prompts' } as const, 0)
// Inicio de la sesión (ms) y último minuto contado: la duración de la cabecera. Viven en $.state: sobreviven a
// /reload-plugins y acaban con la sesión.
const inicioSesion = atom({ plugin: 'sf', key: 'inicioSesion' } as const, 0)
const minuto = atom({ plugin: 'sf', key: 'minuto' } as const, 0)
// La hora de la última comprobación del latido en la red (la del latido, /sf o RELEASE; al empezar, la del arranque): la escriben register.tsx y cola.ts, y la lee
// el panel para decir, al pulsar la etiqueta de la versión, cuánto falta para la próxima (tarea 238).
const comprobadaEn = atom({ plugin: 'sf', key: 'comprobadaEn' } as const, null as number | null)
// disponible: el catálogo local está registrado en este proyecto; pedido: los ajustes piden la copia de trabajo.
const prueba = atom({ plugin: 'sf', key: 'prueba' } as const, { disponible: false, pedido: false } as Prueba)
const sesion = atom({ plugin: 'sf', key: 'sesion' } as const, { limpiadas: {} } as Sesion)
// El propietario cerró el panel a mano: vuelve la caja sobre el prompt hasta que lo reabra con /sf.
const panelCerrado = atom({ plugin: 'sf', key: 'panelCerrado' } as const, false)
// El panel se abre solo una vez por carga del módulo; después manda lo que haga el propietario.
// Secciones del panel plegadas (true) o abiertas (false) por el propietario; las que no ha tocado siguen
// PLEGADAS_DE_INICIO. Se recuerdan entre sesiones en $.store.
const plegado = atom({ plugin: 'sf', key: 'plegado' } as const, {} as Record<string, boolean>)
// Filas que el cuerpo del panel ha subido con el scroll: la cabecera queda fija encima.
const desplazamiento = atom({ plugin: 'sf', key: 'desplazamiento' } as const, 0)
// Turnos de la cabecera con avisos: par, la cabecera normal (también al abrir); impar, los avisos. Lo sube el reloj
// mientras el panel tiene avisos: la cabecera dura TURNO_CABECERA ms y los avisos, TURNO_AVISOS (decisión 164; los
// avisos, 10 s y no 5, tras probarlo el propietario, 2026-11-01).
const turnoAvisos = atom({ plugin: 'sf', key: 'turnoAvisos' } as const, 0)
const TURNO_CABECERA = 5000
const TURNO_AVISOS = 10_000
// Alto fijo de la cabecera: sus dos filas y la de relleno de abajo; con rama, una más, la tercera, para ella sola
// (petición del propietario, 2026-11-01, tarea 260). Los avisos ocupan dos, sin cambiarlo.
const ALTO_CABECERA = 3
// Filas del bloque blanco de los avisos, dentro de la cabecera (petición del propietario, 2026-11-01).
const ALTO_AVISOS = 2
// Si el último dibujo del panel tenía avisos: solo entonces el reloj cambia de turno y lo redibuja.
let conAvisos = false

// La cadena de temporizadores en marcha: un clic en los avisos empieza otra y la anterior se para.
let cadenaTurno = 0

// El turno entre avisos y cabecera, con el reloj del mod, como el latido: si el reloj no avanza (uno simulado), se
// para, para no repetirse sin fin. Se lanza al empezar la sesión.
export function turnarAvisos($: $, antes: number, cadena = cadenaTurno): void {
  void read($, turnoAvisos)
    .then(n => {
      $.clock.after(conAvisos && n % 2 === 1 ? TURNO_AVISOS : TURNO_CABECERA, () => {
        void (async () => {
          const t = await $.clock.now()
          if (t <= antes || cadena !== cadenaTurno) return
          if (conAvisos) await update($, turnoAvisos, k => k + 1)
          turnarAvisos($, t, cadena)
        })().catch(() => undefined)
      })
    })
    .catch(() => undefined)
}

// Un clic en los avisos los quita hasta su siguiente turno: vuelve la cabecera, con sus 5 s enteros (petición del
// propietario, 2026-11-01).
async function quitarAvisos($: $): Promise<void> {
  cadenaTurno++
  await update($, turnoAvisos, k => (k % 2 === 1 ? k + 1 : k))
  turnarAvisos($, await $.clock.now())
}

// El botón que espera el segundo clic: la E que elimina, la D que descarta o la E que quita un paso, «eliminar:7»,
// «descartar:8» o «paso:7:2»; null, ninguno (decisión del propietario, 2026-10-29).
const porConfirmar = atom({ plugin: 'sf', key: 'porConfirmar' } as const, null as string | null)
// Cada primer clic lleva su turno: el temporizador que devuelve el botón a E o D solo actúa si sigue siendo el último.
let turnoConfirmar = 0
// RELEASE: la versión de la que se parte, leída en el primer clic (decisión del propietario, 2026-10-29). Su botón
// espera en porConfirmar: «release», con las versiones a elegir; «release:X.Y.Z», con la elegida por confirmar.
const fuenteRelease = atom({ plugin: 'sf', key: 'fuenteRelease' } as const, null as FuenteVersion | null)
// ACTUALIZAR: la versión publicada nueva y los scopes por actualizar, o null. La comprueba cola.ts, nunca al pintar.
// Su botón espera en porConfirmar como «actualizar»; sin scopes es REFRESCAR (decisión 177) y espera como «refrescar».
const actualizacion = atom({ plugin: 'sf', key: 'actualizacion' } as const, null as Actualizacion | null)
const ESPERA_CONFIRMAR = 5000
// Los párrafos de una descripción, separados por una línea en blanco: cada uno se pinta aparte.
const parrafos = (d: string) => d.split(/\r?\n\s*\n/).map(x => x.trim()).filter(x => x !== '')
// Las órdenes con confirmación: el texto de su etiqueta, su color y el prefijo de la clave de su botón. Al confirmar,
// la etiqueta dice «¿Cerrar? sí», en su mismo color; la de Revertir se parte en dos, una por destino (decisiones 134 y
// 168). Las que destruyen, en rojo; Cerrar, en verde, como las demás órdenes de la tarea.
const ACCIONES = {
  eliminar: { nombre: 'Eliminar', color: COLOR_ORDEN_DESTRUCTIVA, clave: 'eliminar-tarea' },
  descartar: { nombre: 'Descartar', color: COLOR_ORDEN_DESTRUCTIVA, clave: 'descartar-tarea' },
  cerrar: { nombre: 'Cerrar', color: 'success', clave: 'cerrar-tarea' },
  // A observación, en la en curso que se cierra: cierra y la deja en observación; Cerrar en observación la saca: va
  // bien (241, 204).
  aObservacion: { nombre: 'A observación', color: 'success', clave: 'a-observacion-tarea' },
  cerrarObservada: { nombre: 'Cerrar', color: 'success', clave: 'cerrar-observada-tarea' },
  revertir: { nombre: 'Revertir', color: COLOR_ORDEN_DESTRUCTIVA, clave: 'revertir-tarea' },
  propuesta: { nombre: 'A propuesta', color: 'success', clave: 'propuesta-tarea' },
  // A observación, en las cerradas: la cerrada por error vuelve a observación con su commit de develop (296).
  reobservar: { nombre: 'A observación', color: 'success', clave: 'reobservar-tarea' },
} as const
const DESTINOS_REVERTIR = ['eliminar', 'pendiente'] as const
const TEXTO_DESTINO = { eliminar: 'eliminar', pendiente: 'a Pendientes' } as const
type Accion = keyof typeof ACCIONES

export let panelIntentado = false
export function recortar(t: string, n: number): string {
  return t.length > n ? `${t.slice(0, n - 1)}…` : t
}

// Un aviso, en las dos filas del bloque blanco de la cabecera, de w columnas cada una: partido por palabras; lo que
// no cabe, recortado con «…».
export function lineasAviso(aviso: string, w: number): string[] {
  const lineas: string[] = []
  for (const palabra of `⚠ ${aviso}`.split(' ')) {
    const ultima = lineas.at(-1)
    if (ultima !== undefined && (ultima + ' ' + palabra).length <= w) lineas[lineas.length - 1] = `${ultima} ${palabra}`
    else lineas.push(palabra)
  }
  if (lineas.length <= 2) return lineas.map(l => recortar(l, w))
  return [recortar(lineas[0]!, w), recortar(lineas.slice(1).join(' '), w)]
}

export function lineaEstado(e: Estado): string {
  if (e.tipo === 'sin-sf') return 'Sin SF'
  if (e.tipo === 'sf') return 'SF · repositorio de la SF'
  const partes = [`SF${e.versionSf ? ' ' + e.versionSf : ''}${atrasada(e) ? ` → ${e.versionPlugin}` : ''}`, e.proyecto]
  // Sin metodología no hay fase: solo tareas, repositorio y decisiones (informe «Configuración inicial»).
  if (e.error) partes.push('⚠ revisar .sf/')
  else if (e.metodologia !== false) partes.push(e.fase !== null ? `${e.fase + 1}/${FASES.length} ${FASES[e.fase]?.nombre ?? ''}` : 'fase sin declarar')
  if (e.devslice) partes.push(`devslice ${e.devslice}`)
  if (e.aviso) partes.push('⚠ mover a .sf/')
  return partes.join(' · ')
}

export function registrarPanel(on: Parameters<Register>[0]): void {
  // Centro de control: en pantalla completa, el panel lateral (se abre solo); si no hay panel (pantalla normal,
  // terminal estrecho o panel cerrado a mano), una caja pequeña sobre el prompt con el estado y la cola.
  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    anotarPantalla(e)
    const est = await read($, estado)
    if (e.props.hasSurvey || est === null) return next(e)
    // La caja no sale mientras el panel se ve: colocado y al frente. Sale con el panel cerrado, detrás de otra
    // pestaña o sin colocar (decisión 164, corregida tras probarla: verse siempre la repetía junto al panel).
    if (e.viewport?.isFullscreen === true) {
      const cerrado = await read($, panelCerrado)
      const panel = (await $.ui.panes()).find(p => p.id === PANEL)
      if (panel?.isPlaced && panel.isShown) return next(e)
      if (!panel && !panelIntentado && !cerrado) {
        panelIntentado = true
        const r = await $.ui.open({ id: PANEL, title: 'Software Factory' })
        if (r.isPlaced) return next(e)
        $.ui.log(`panel sin colocar: ${r.reason}`, { to: 'debug' })
      }
    }
    const { Box, Text } = $.ui.resolve(e)
    const cola = est.peticiones
    const porRevisar = est.realimentacion?.porRevisar.length ?? 0
    const cuenta = (x: Peticion['estado']) => cola.filter(p => p.estado === x).length
    const curso = cola.filter(enCursoOObservando)

    const cuentas: string[] = []
    if (cuenta('en-cola')) cuentas.push(`en cola ${cuenta('en-cola')}`)
    if (cuenta('en-observacion')) cuentas.push(`observación ${cuenta('en-observacion')}`)
    if (porRevisar) cuentas.push(`propuestas ${porRevisar}`)
    // Sin pantalla completa, los clics no llegan: se dice en texto (tarea 264).
    const avisos = [sinPantallaCompleta(e) ? AVISO_PANTALLA : null, est.error || est.aviso || est.avisosConfiguracion?.length ? 'revisar .sf/' : null, est.errorPeticiones ? 'revisar .sf/peticiones.json' : null]
      .filter((x): x is string => x !== null)

    return (
      <Box flexDirection="column" alignSelf="flex-end" borderStyle="round" borderDimColor paddingX={1}>
        <Text weight="bold">{lineaEstado(est)}</Text>
        {curso.map(p => (
          <Text>▶ {recortar(p.texto, 56)}</Text>
        ))}
        {cuentas.length > 0 && <Text dimColor>{cuentas.join(' · ')}</Text>}
        {/* Los avisos, como en el panel: fondo blanco y letra oscura (decisión 164). */}
        {avisos.length > 0 && (
          <Box flexDirection="column" backgroundColor={FONDO_AVISO}>
            {avisos.map(t => (
              <Text color={COLOR_AVISO}>⚠ {t}</Text>
            ))}
          </Box>
        )}
        <Text dimColor>/sf abre el panel</Text>
      </Box>
    )
  })

  // Un clic en cualquier otro botón del panel deja la E o la D pendiente como estaba, sin eliminar ni descartar
  // (decisión del propietario, 2026-10-29).
  on('ui.press', async ($, e, next) => {
    if (e.plugin === 'sf' && !['eliminar-tarea:', 'descartar-tarea:', 'revertir-tarea:', 'quitar-paso:', 'release', 'actualizar', 'refrescar'].some(x => e.element.startsWith(x))) {
      turnoConfirmar++
      await update($, porConfirmar, v => (v === null ? v : null)).catch(() => undefined)
    }
    return next(e)
  })

  // Cerrado a mano: se recuerda para no volver a abrirlo solo y para enseñar la caja en su lugar.
  // La caja se vuelve a pintar al cerrarse el panel: la banda no se entera sola de que $.ui.panes() ha cambiado.
  on('ui.close', async ($, e, next) => {
    if (e.id !== PANEL) return next(e)
    $.ui.log(`panel cerrado: ${e.origin.kind}`, { to: 'debug' })
    if (e.origin.kind === 'person') await update($, panelCerrado, () => true).catch(() => undefined)
    const r = await next(e)
    $.ui.invalidate('ui.render')
    return r
  })

  // Cabecera fija: el panel no deja mover su ventana; sube el cuerpo bajo la cabecera, como pide el motor
  // para un árbol que se desplaza solo bajo una cabecera. El tope sale del alto del árbol, que el cuerpo
  // no cambia al subir (decisión del propietario, 2026-10-29).
  on('ui.scroll', { component: 'Pane', requestId: PANEL }, async ($, e) => {
    const k = await read($, desplazamiento)
    const nuevo = Math.min(Math.max(0, k + e.by), Math.max(0, e.contentRows - e.bodyRows))
    if (nuevo !== k) await update($, desplazamiento, () => nuevo)
    return {}
  })

  on('ui.render', { component: 'Pane', requestId: PANEL }, async ($, e) => {
    anotarPantalla(e)
    const { Box, Text, Button } = $.ui.resolve(e)
    const est = await read($, estado)

    if (est === null) return <Text dimColor>Leyendo el estado…</Text>

    const plegadas = await read($, plegado)
    // La letra es el estado de la tarea, la misma en todos los sitios (decisión del propietario, 2026-10-28):
    // A (actual): en cola o en curso, entró en esta sesión; H (histórico): en cola o en curso, ya estaba al abrirla
    // (una H no pasa a A); O: en observación; C: cerrada, ya fuera de la cola; D: descartada (decisión del
    // propietario, 2026-10-29), también si ya ha salido de la cola; R: revertida en develop, solo en las salidas
    // anteriores a la decisión 134 (ahora una revertida sale eliminada o vuelve a Pendientes). Salen del historial de cada tarea, que escribe cola.py (tarea 145): A si se creó (o nació de un
    // /sf_split) después del inicio de la sesión; H si no, si no tiene historial o si está reabierta. Fuera de la cola, el
    // estado con que salió, en .sf/historial.jsonl.
    const desde = await read($, inicioSesion)
    const enCola = new Map(est.peticiones.map(p => [p.id, p] as const))
    const fuera = new Map(est.salidas.map(t => [t.id, t] as const))
    const letra = (id: number) => {
      const p = enCola.get(id)
      if (p === undefined) {
        const e = fuera.get(id)?.estado
        return e === 'descartada' ? 'D' : e === 'revertida' ? 'R' : 'C'
      }
      if (p.estado === 'descartada') return 'D'
      if (p.estado === 'en-observacion') return 'O'
      return !p.reabierta && (creadaEn(p.historial) ?? -Infinity) >= desde ? 'A' : 'H'
    }
    // Sin letras tras los números (decisión del propietario, 2026-10-31): la letra solo da el color del número. El rojo,
    // solo en las reabiertas, como fondo del número, en todos los apartados; las de sesiones anteriores (H), en gris
    // (petición del propietario, 2026-10-31).
    const reabierta = (id: number) => enCola.get(id)?.reabierta === true
    const fondoNumero = (id: number) => (reabierta(id) ? 'error' : undefined)
    const colorNumero = (id: number, enCurso = false) =>
      enCurso ? COLOR_TAREA : reabierta(id) ? TEXTO_TAREA : (colorLetra(letra(id)) ?? TEXTO_TAREA)
    // Las peticiones (pet:<sección>:<id>), los commits (hecho:<hash>) y las propuestas (prop:<título>) empiezan plegados.
    const abierta = (clave: string) =>
      !(
        plegadas[clave] ??
        (PLEGADAS_DE_INICIO.includes(clave) || /^(pet|hecho|prop|pasos|desc|prueba|arriba):/.test(clave))
      )
    // `ahora`: si se ve abierta, cuando no lo dice solo su clave; `fijar`: otras claves que se guardan con su estado de
    // ahora, si el propietario aún no las ha tocado (la Descripción abierta por defecto, decisión del propietario,
    // 2026-11-01).
    const alternar = (clave: string, ahora = abierta(clave), fijar: Record<string, boolean> = {}) => () => {
      const plegar = ahora
      void update($, plegado, v => ({ ...fijar, ...v, [clave]: plegar }))
        .then(() => read($, plegado))
        .then(v => $.store.set(CLAVE_PLEGADO, v))
        .catch(() => undefined)
    }

    // Sección plegable: la cabecera es un botón (clic, o Tab y Enter con el panel enfocado) con su cuenta.
    // La cuenta, atenuada; una sección puede dar la suya ya dibujada (Cerradas, con el número en verde).
    // La cabecera, el nombre en mayúsculas y el icono de desplegar a su derecha, antes de la cuenta: «PENDIENTES ▸ 17»;
    // el cuerpo, sin sangría: el número de una tarea de sección, en la misma columna que el de las de arriba
    // (decisiones del propietario, 2026-10-31).
    const seccion = (clave: string, titulo: string, cuenta: RenderChildren, cuerpo: RenderChildren) => (
      <Box flexDirection="column">
        <Button key={`sec:${clave}`} plain onPress={alternar(clave)}>
          <Text weight="bold">{titulo.toUpperCase()}</Text>
          {abierta(clave) ? ' ▾' : ' ▸'}
          {cuenta === null || cuenta === undefined ? '' : typeof cuenta === 'string' ? <Text dimColor> {cuenta}</Text> : <Text> {cuenta}</Text>}
        </Button>
        {abierta(clave) && (
          <Box flexDirection="column">
            {cuerpo}
          </Box>
        )}
      </Box>
    )

    // Niveles: cabecera de sección y una línea por elemento, sin sangría; su detalle, con la suya.
    // Las líneas de nivel 1 no se parten: se recortan al ancho del panel y el texto entero va en el detalle. Los
    // títulos de las tareas, no: van enteros, partidos con sangría colgante (filaTitulo).
    // Una columna de margen a la derecha: lo último de cada línea no toca el borde (decisión del propietario, 2026-10-30).
    const ancho = e.props.bodyColumns - 1
    const enLinea = (t: string, ocupado: number) => recortar(t, Math.max(12, ancho - ocupado))

    // El paso en curso, sin amarillo, también arriba: el amarillo es solo para la tarea (decisión del propietario,
    // 2026-10-28).
    // El primer clic de un botón con confirmación: lo deja esperando el segundo; a los 5 s vuelve a ser el símbolo.
    const aConfirmar = await read($, porConfirmar)
    const pedirConfirmar = (marca: string) => {
      const turno = ++turnoConfirmar
      void update($, porConfirmar, () => marca).catch(() => undefined)
      $.clock.after(ESPERA_CONFIRMAR, () => {
        if (turno === turnoConfirmar) void update($, porConfirmar, v => (v === marca ? null : v)).catch(() => undefined)
      })
    }

    // Un paso pendiente lleva al final la «×» que lo quita de la tarea: roja y con dos clics, «¿Quitar? sí»
    // (decisiones del propietario, 2026-10-29, y 168; antes, una E). Los de cierre, «Activar rama para poder probar» y «Cerrar la tarea», no la llevan (174).
    // Cada paso lleva «?», que pide a Claude que lo explique (decisión del propietario, 2026-10-28).
    const botonQuitarPaso = (x: Paso, id: number, i: number, donde: string) => {
      const marca = `paso:${id}:${i}`
      const confirmando = aConfirmar === marca
      const pulsar = () => {
        if (!confirmando) return pedirConfirmar(marca)
        turnoConfirmar++
        void update($, porConfirmar, () => null)
          .then(() => quitarPaso($, id, i, x.texto))
          .then(aviso => {
            if (aviso) emergenteError($, aviso)
          })
          .catch(() => undefined)
      }
      return (
        <Button key={`quitar-paso:${donde}:${id}:${i}`} plain onPress={pulsar}>
          <Text color="error" weight={confirmando ? 'bold' : undefined}>
            {confirmando ? ' ¿Quitar? sí' : ' ×'}
          </Text>
        </Button>
      )
    }
    // El texto de un paso, partido por palabras en líneas de `w` columnas, con sus botones («?» y «×», de `botones`
    // columnas) como una palabra más al final: van tras la última palabra, en la última línea, y si no caben, en una
    // propia. El motor no deja un Button dentro de un Text, así que el partido lo hace el panel.
    const partirPaso = (texto: string, w: number, botones: number): string[] => {
      const lineas: string[] = []
      for (const palabra of texto.split(' ')) {
        const ultima = lineas.at(-1)
        if (ultima !== undefined && (ultima + ' ' + palabra).length <= w) lineas[lineas.length - 1] = `${ultima} ${palabra}`
        else lineas.push(palabra)
      }
      if (lineas.length === 0) lineas.push('')
      if (lineas.at(-1)!.length + botones > w && lineas.at(-1) !== '') lineas.push('')
      return lineas
    }
    const lineaPaso = (x: Paso, id: number, i: number, donde: string) => {
      const color = x.estado === 'hecho' ? LETRA.neutra : TEXTO_PASO
      const quitable = pasoQuitable(x)
      const botones = 2 + (quitable ? (aConfirmar === `paso:${id}:${i}` ? ' ¿Quitar? sí'.length : 2) : 0)
      // Una ayuda de prueba lleva «(opcional)» tras su texto: no se exige para cerrar (decisión 184).
      const lineas = partirPaso(x.ayuda ? `${x.texto} (opcional)` : x.texto, Math.max(12, ancho - 4), botones)
      return (
        <Box flexDirection="row">
          {/* Numerados en lugar de marcas (decisión del propietario, 2026-10-31): hecho, en gris; en curso, el número
              en negrita; pendiente, normal. El número, sin punto, en tres columnas alineado a su derecha, y un espacio;
              el texto, a su derecha y con sangría colgante, como los títulos: «  1 Elegir», « 12 Probar». */}
          <Box width={4} flexShrink={0}>
            <Text color={color} weight={x.estado === 'en-curso' ? 'bold' : 'regular'}>
              {String(i + 1).padStart(3)}
            </Text>
          </Box>
          {/* Los botones siguen a la última palabra, también si el paso ocupa varias líneas (petición del propietario,
              2026-11-01). */}
          <Box flexDirection="column" flexShrink={1}>
            {lineas.slice(0, -1).map(l => (
              <Text color={color} weight="regular">
                {l}
              </Text>
            ))}
            <Box flexDirection="row">
              {lineas.at(-1) !== '' && (
                <Text color={color} weight="regular">
                  {lineas.at(-1)}
                </Text>
              )}
              <Button key={`info-paso:${donde}:${id}:${i}`} plain onPress={() => preguntarPaso($, id, x)}>
                {/* En verde, como Activar rama y la C: así se ve que es un botón (decisión del propietario, 2026-10-30). */}
                <Text color="success">{lineas.at(-1) === '' ? '?' : ' ?'}</Text>
              </Button>
              {quitable && botonQuitarPaso(x, id, i, donde)}
            </Box>
          </Box>
        </Box>
      )
    }

    // El ● del subagente de una tarea, a la derecha de su línea plegada: la única marca que queda en ella (decisión
    // 168). Sale de los subagentes en marcha, no de los worktrees; su descripción, para el aviso. Verde mientras
    // trabaja y rojo mientras espera instrucciones, solo con la tarea en curso; parado, sin ● (decisión 162).
    const subagenteDe = (p: Peticion): { descripcion: string; esperando: boolean } | undefined => {
      const trabajando = est.subagentes[p.id]
      if (trabajando !== undefined) return { descripcion: trabajando, esperando: false }
      const esperando = p.estado === 'en-curso' ? est.subagentesEsperando?.[p.id] : undefined
      return esperando !== undefined ? { descripcion: esperando, esperando: true } : undefined
    }
    const marcaSubagente = (p: Peticion, donde: string) => {
      const subagente = subagenteDe(p)
      if (subagente === undefined) return null
      const aviso = subagente.esperando
        ? `⚙: el subagente de la ${String(p.id)} espera instrucciones (${subagente.descripcion})`
        : `⚙: un subagente trabaja en la ${String(p.id)} (${subagente.descripcion})`
      const avisar = () => emergente($, aviso, false)
      return (
        <Button key={`subagente-tarea:${donde}:${p.id}`} plain onPress={avisar}>
          <Text color={subagente.esperando ? 'error' : 'success'}>{` ${MARCA_SUBAGENTE} `}</Text>
        </Button>
      )
    }

    // Las órdenes de una tarea, en un menú de etiquetas en la primera fila de la tarea desplegada (decisión 168;
    // antes, letras a la derecha de la línea plegada). Cada una, con el estilo de las etiquetas de la cabecera: su
    // nombre, con mayúscula inicial, sin negrita (las de la cabecera, sí), sobre su fondo propio (FONDO_ORDEN); las de la tarea en verde, salvo las
    // que destruyen, en rojo. Si no caben en una fila, siguen en la siguiente. Primero las de la tarea: Activar rama,
    // Cerrar, A observación (o Cerrar en observación, 241), Redescribir, «?» (254), A propuesta (243) y la que destruye (Eliminar, Descartar o Revertir); después, las de sus pasos: Separar pasos
    // y Paso +, al final y con la letra atenuada, para distinguirlas de las de la tarea (decisión 168, precisada por el
    // propietario el 2026-11-01).
    type Tarea = { id: number; texto: string; rama?: string | null }
    const etiquetaOrden = (key: string, color: string | undefined, nombre: string, pulsar: () => void) => (
      <Box marginRight={1} flexShrink={0}>
        <Button key={key} plain onPress={pulsar}>
          <Text color={color} weight="regular" backgroundColor={FONDO_ORDEN}>
            {` ${nombre} `}
          </Text>
        </Button>
      </Box>
    )
    // Eliminar, en las eliminables: en cola o en curso y sin rama. Descartar, en las descartables: con rama, en cola o
    // en curso. En observación, Revertir en su lugar: ya entró en develop al cerrarla (decisión 115, 4). Nunca dos: una
    // tarea con rama no es eliminable.
    const accionDe = (p: Peticion, conEliminar: boolean): Accion | null =>
      conEliminar && eliminable(p)
        ? 'eliminar'
        : descartable(p)
          ? 'descartar'
          : revertibleEnObservacion(p, est.mergeadas)
            ? 'revertir'
            : null
    // Las de dos clics: el primero cambia la etiqueta por «¿Cerrar? sí» y el segundo actúa. A los 5 s, o con un clic
    // en otro botón del panel, vuelve a ser la etiqueta.
    const botonAccion = (p: Tarea, donde: string, accion: Accion) => {
      const { nombre, color, clave } = ACCIONES[accion]
      const marca = `${accion}:${p.id}`
      const confirmando = aConfirmar === marca
      const pulsar = () => {
        if (!confirmando) return pedirConfirmar(marca)
        turnoConfirmar++
        // Eliminar quita la tarea de la cola; descartar borra la rama y la pasa a descartada; cerrar la pasa a
        // develop por squash y la saca de la cola; A observación, igual, pero la deja en observación; Cerrar en observación
        // la saca, porque va bien; A propuesta la devuelve a sf/propuestas.md y la saca; A observación devuelve una cerrada a la cola, en observación. Todas, sin Claude («Comandos antes
        // que inferencia»).
        void update($, porConfirmar, () => null)
          .then(async () => {
            if (accion === 'eliminar') {
              const aviso = await eliminarTarea($, p.id, p.texto)
              if (aviso) emergenteError($, aviso)
              return
            }
            const r =
              accion === 'descartar'
                ? await descartarTarea($, p.id, p.texto)
                : accion === 'propuesta'
                  ? await aPropuestaTarea($, p.id, p.texto)
                  : accion === 'cerrarObservada'
                    ? await cerrarObservada($, p.id, p.texto)
                    : accion === 'reobservar'
                      ? await reobservarTarea($, p.id)
                      : await cerrarTarea($, p.id, p.texto, p.rama, accion === 'aObservacion' ? 'a-observacion' : 'cerrar')
            emergenteRespuesta($, r)
          })
          .catch(err => emergenteError($, `No se pudo ${accion === 'aObservacion' ? 'pasar a observación' : accion === 'cerrarObservada' ? 'cerrar' : accion === 'propuesta' ? 'pasar a propuesta' : accion === 'reobservar' ? 'devolver a observación' : accion} la ${String(p.id)}: ${String(err)}`))
      }
      // Revertir, confirmando, se parte en «¿Revertir?» y dos etiquetas, [eliminar] y [a Pendientes]: el segundo clic,
      // en una de ellas, revierte y deja la tarea en ese destino, eliminada sin rastro o de vuelta en Pendientes
      // (decisión 134).
      if (accion === 'revertir' && confirmando) {
        const revertirA = (destino: (typeof DESTINOS_REVERTIR)[number]) => () => {
          turnoConfirmar++
          void update($, porConfirmar, () => null)
            .then(() => revertirTarea($, p.id, p.texto, est.mergeadas[String(p.id)] ?? [], destino))
            .then(r => emergenteRespuesta($, r))
            .catch(err => emergenteError($, `No se pudo revertir la ${String(p.id)}: ${String(err)}`))
        }
        return (
          <Box flexDirection="row" flexShrink={0}>
            <Box marginRight={1} flexShrink={0}>
              <Text dimColor>¿Revertir?</Text>
            </Box>
            {DESTINOS_REVERTIR.map(d => etiquetaOrden(`${clave}:${donde}:${p.id}:${d}`, color, TEXTO_DESTINO[d], revertirA(d)))}
          </Box>
        )
      }
      return etiquetaOrden(`${clave}:${donde}:${p.id}`, color, confirmando ? `¿${nombre}? sí` : nombre, pulsar)
    }

    // Activar rama (antes Probar, y antes la letra T): activa la rama de la tarea con git para ponerla en prueba, sin darla por buena; con un clic (decisiones
    // del propietario, 2026-10-29). Solo si la rama existe y no es la activa; si lo es, la cabecera ya la muestra en
    // amarillo. Si la rama está en otro worktree, sale igual: al pulsarla, probarTarea lo comprueba y no cambia de rama.
    const conProbar = (p: Peticion) => probable(p, est.ramas, est.rama)
    // Cerrar y A observación, en las tareas en curso que solo esperan probarse y cerrarse, con rama o sin ella (decisiones
    // del propietario, 2026-10-29, y 188). Con dos clics.
    const conCerrar = (p: Peticion) => cerrable(p, est.ramas)
    // Separar, en las tareas en cola o en curso con dos pasos pendientes o más: abre el diálogo de /sf_split con solo los
    // pendientes y separa sin Claude; con más de cuatro, recuerda la forma corta (decisión del propietario, 2026-10-29).
    const conSplit = (p: Peticion) => separablePendientes(p)
    // A propuesta (tarea 243), en Pendientes: en cola y sin rama, si el sf/propuestas.md del proyecto tiene
    // «Propuestas pendientes» (realimentacion). Con dos clics, antes de la que destruye.
    const conPropuesta = (p: Peticion, donde: string) => donde === 'cola' && est.realimentacion !== null && devolvible(p)
    const botonSplit = (p: Peticion, donde: string) =>
      etiquetaOrden(`split-tarea:${donde}:${p.id}`, TEXTO_TAREA, 'Separar pasos', () => {
        const t = elegirPasos($, p, true)
        if (t) emergente($, t, false)
      })
    const botonProbar = (p: Peticion, donde: string) =>
      etiquetaOrden(`probar-tarea:${donde}:${p.id}`, 'success', 'Activar rama', () => {
        void probarTarea($, p.id, p.rama ?? '')
          .then(r => emergenteRespuesta($, r))
          .catch(err => emergenteError($, `No se pudo activar la rama de la ${String(p.id)}: ${String(err)}`))
      })
    // Redescribir y Paso +, las órdenes que antes solo eran comandos (decisión 168): las dos acaban en Claude. Redescribir, en las que tienen descripción: lo mismo que /sf_redescribir N. Paso +, en las en
    // curso o en prueba, las de arriba: deja «/sf_paso N » en el prompt para escribir el paso, como /sf_paso N texto.
    const botonRedescribir = (p: Peticion, donde: string) =>
      etiquetaOrden(`redescribir-tarea:${donde}:${p.id}`, 'success', 'Redescribir', () => {
        emergente($, pedirRedescripcion($, est.peticiones, String(p.id)).replace(/^\/sf_redescribir/, 'Redescribir'), false)
      })
    // «?», en todas las tareas desplegadas con menú (254): pide a Claude que explique la tarea al propietario, como el
    // «?» de los pasos; en verde, tras Redescribir y antes de la que destruye, que sigue al final.
    const botonExplicar = (p: Peticion, donde: string) =>
      etiquetaOrden(`explicar-tarea:${donde}:${p.id}`, 'success', '?', () => {
        emergente($, explicarTarea($, p.id, p.texto), false)
      })
    const botonPaso = (p: Peticion, donde: string) =>
      etiquetaOrden(`paso-tarea:${donde}:${p.id}`, TEXTO_TAREA, 'Paso +', () => {
        const orden = `/sf_paso ${String(p.id)} `
        const avisar = () => emergente($, `Paso +: escribe «${orden.trim()} texto del paso».`, false)
        // Desde un temporizador, como los prompts del panel: el motor no deja tocar el prompt desde su hook.
        $.clock.after(50, () => {
          void $.prompt
            .fill({ text: orden })
            .then(r => {
              if (!r.isFilled) avisar()
            })
            .catch(avisar)
        })
      })
    // Una fila de etiquetas de orden, a la izquierda y partida si no cabe; sin órdenes, no se pinta. La usan las
    // tareas y las propuestas (decisión 197).
    const filaOrdenes = (ordenes: RenderChildren[]) =>
      ordenes.length === 0 ? null : (
        <Box flexDirection="row" flexWrap="wrap">
          {ordenes}
        </Box>
      )
    // Las órdenes de una tarea de la cola, por sitio: arriba (en curso o en prueba), Pendientes (cola) y En observación
    // (observacion). Con «?» (254), toda tarea tiene al menos una; una fila sin órdenes no se pinta.
    const menuOrdenes = (p: Peticion, donde: string) => {
      const enCola = donde === 'cola' || donde === 'arriba'
      const accion = accionDe(p, enCola)
      // Dos filas: la de las órdenes de la tarea y, debajo, la de las de sus pasos (petición del propietario,
      // 2026-11-01). Una fila sin órdenes no se pinta.
      const deTarea = [
        conProbar(p) ? botonProbar(p, donde) : null,
        enCola && conCerrar(p) ? botonAccion(p, donde, 'cerrar') : null,
        enCola && conCerrar(p) ? botonAccion(p, donde, 'aObservacion') : null,
        p.estado === 'en-observacion' ? botonAccion(p, donde, 'cerrarObservada') : null,
        p.descripcion ? botonRedescribir(p, donde) : null,
        botonExplicar(p, donde),
        conPropuesta(p, donde) ? botonAccion(p, donde, 'propuesta') : null,
        accion !== null ? botonAccion(p, donde, accion) : null,
      ].filter(x => x !== null)
      const dePasos = [enCola && conSplit(p) ? botonSplit(p, donde) : null, donde === 'arriba' ? botonPaso(p, donde) : null].filter(x => x !== null)
      if (deTarea.length === 0 && dePasos.length === 0) return null
      return (
        <Box flexDirection="column">
          {filaOrdenes(deTarea)}
          {filaOrdenes(dePasos)}
        </Box>
      )
    }

    // Una línea del detalle, en la columna 0: sus partes, separadas por « · »; se parte si no cabe. Cada parte, hermana
    // de las demás: un color heredado no se puede anular dentro.
    const lineaDetalle = (partes: RenderChildren[]) => {
      const hay = partes.filter(x => x !== null && x !== undefined && x !== false && x !== '')
      if (hay.length === 0) return null
      if (hay.length === 1) return hay[0]
      return <Text>{hay.flatMap((x, i) => (i > 0 ? [<Text dimColor> · </Text>, x] : [x]))}</Text>
    }
    // La línea de la rama: «Rama: feature/NN-nombre», con « (no existe)» si no está en el repositorio (decisión del
    // propietario, 2026-10-29); tras ella, en la misma línea, «Commit: …» (tarea 237). Sin rama, la línea empieza por el commit. Igual
    // en todas las secciones: en observación o la que se mira, cómo probarla y el OK de Claude van aparte (tarea 237).
    const lineaRama = (p: Peticion) =>
      lineaDetalle([
        p.rama ? (
          <Text dimColor>
            Rama: {p.rama}
            {est.ramas[p.rama] === false ? ' (no existe)' : ''}
          </Text>
        ) : null,
        p.commit ? <Text dimColor>Commit: {p.commit}</Text> : null,
      ])
    // En observación o la que se mira, el OK de Claude y cómo probarla, en un desplegable propio, «Prueba», plegado al
    // empezar, con la cabecera subrayada como «Descripción» y «Pasos»; con «✓» en verde tras ella si Claude comprobó
    // algo (decisión 179 y peticiones del propietario en la tarea 237). Su clave, por sitio: prueba:<sitio>:<id>.
    // Desplegado, en la columna del título, dos apartados con su rótulo atenuado, «Comprobado por Claude» y «Qué
    // mirar»; debajo, un punto por línea, con guion y sangría colgante (puntosDe parte por «;»); el contexto del
    // principio («Tras publicar:»), antes de los puntos, atenuado.
    const apartadoPrueba = (rotulo: string, texto: string, color: string | undefined, columna: number) => {
      const { contexto, puntos } = puntosDe(texto)
      return (
        <Box flexDirection="column">
          <Box paddingLeft={columna}>
            <Text dimColor>{rotulo}</Text>
          </Box>
          {contexto !== null && (
            <Box paddingLeft={columna + 2}>
              <Text dimColor>{contexto}:</Text>
            </Box>
          )}
          {puntos.map(x => (
            <Box flexDirection="row" paddingLeft={columna + 2}>
              <Box width={2} flexShrink={0}>
                <Text dimColor>-</Text>
              </Box>
              <Box flexShrink={1}>
                <Text color={color ?? TEXTO_TAREA} weight="regular">{x}</Text>
              </Box>
            </Box>
          ))}
        </Box>
      )
    }
    const bloquePrueba = (p: Peticion, donde: string, columna: number, fijar: Record<string, boolean> = {}) => {
      if (p.comprobado === null && !p.prueba) return null
      const k = `prueba:${donde}:${p.id}`
      return (
        <Box flexDirection="column">
          <Button key={k} plain onPress={alternar(k, abierta(k), fijar)}>
            <Text dimColor underline>
              Prueba
            </Text>
            {p.comprobado !== null ? <Text color="success"> ✓</Text> : ''}
          </Button>
          {abierta(k) && p.comprobado !== null && apartadoPrueba('Comprobado por Claude', p.comprobado, 'success', columna)}
          {abierta(k) && p.prueba && apartadoPrueba('Qué mirar', p.prueba, undefined, columna)}
        </Box>
      )
    }
    // Los pasos, desplegable propio en la columna 0, plegado al empezar: su cabecera, «Pasos 3/5», el rótulo y los
    // hechos del total, sin el paso actual; desplegado, la lista, sin sangría (decisiones del propietario,
    // 2026-10-28 y 2026-10-31). Su clave, por sitio: pasos:<sitio>:<id>.
    const bloquePasos = (t: Peticion, donde: string, fijar: Record<string, boolean> = {}) => {
      const pasos = t.pasos
      if (pasos.length === 0) return null
      const k = `pasos:${donde}:${t.id}`
      return (
        <Box flexDirection="column">
          <Button key={k} plain onPress={alternar(k, abierta(k), fijar)}>
            {/* Con el brillo de la línea de la rama (decisión del propietario, 2026-10-31). */}
            <Text dimColor underline>
              Pasos
            </Text>
            <Text dimColor> {cuentaPasos(pasos)}</Text>
          </Button>
          {/* La lista, sin sangría: en la columna 0, como la rama (decisión del propietario, 2026-10-31). */}
          {abierta(k) && (
            <Box flexDirection="column">
              {pasos.map((x, i) => lineaPaso(x, t.id, i, donde))}
            </Box>
          )}
        </Box>
      )
    }

    // La descripción de una tarea desplegada empieza en la columna de su título (decisión del propietario,
    // 2026-10-31): tras el hueco, el número (tres columnas entre los dos) y un espacio.
    const columnaTitulo = (id: number) => hueco(id) + String(id).length + 1
    const bloqueDescripcion = (texto: string, columna: number) => (
      <Box flexDirection="column" paddingLeft={columna}>
        {parrafos(texto).map((x, i) => (
          <Box marginTop={i > 0 ? 1 : 0}>
            <Text color={TEXTO_TAREA} weight="regular">{x}</Text>
          </Box>
        ))}
      </Box>
    )
    // Desplegada, debajo del título y en este orden (decisión del propietario, 2026-10-31, con el orden precisado el
    // mismo día): la línea de la rama (rama y commit); en observación, «Prueba», desplegable propio plegado al empezar (prueba:<sitio>:<id>), con el OK de Claude y la prueba en la columna del título; «Descripción»,
    // desplegable propio plegado al empezar (desc:<sitio>:<id>), con el texto en la columna del título; y los pasos,
    // desplegable propio. Lo que la tarea no tiene, no sale.
    // Con órdenes, la primera fila es su menú (decisión 168): toda tarea con alguna orden se despliega.
    const hayDetalle = (p: Peticion, conPrueba: boolean, ordenes: RenderChildren = null) =>
      ordenes !== null || p.descripcion !== null || p.rama !== null || p.commit !== null || p.pasos.length > 0 || (conPrueba && (p.prueba !== null || p.comprobado !== null))
    const detalleTarea = (p: Peticion, donde: string, conPrueba: boolean, columna: number, ordenes: RenderChildren = null) => {
      const kDesc = `desc:${donde}:${p.id}`
      // Con todas sus partes sin tocar, la Descripción sale desplegada; en cuanto el propietario despliega o pliega
      // una, manda lo guardado (decisión del propietario, 2026-11-01). Al tocar Pasos, la Descripción se guarda abierta.
      const sinTocar = plegadas[kDesc] === undefined && plegadas[`pasos:${donde}:${p.id}`] === undefined && plegadas[`prueba:${donde}:${p.id}`] === undefined
      const descAbierta = p.descripcion !== null && (sinTocar || abierta(kDesc))
      const fijar: Record<string, boolean> = p.descripcion !== null && sinTocar ? { [kDesc]: false } : {}
      return (
        <Box flexDirection="column">
          {ordenes}
          {lineaRama(p)}
          {conPrueba && bloquePrueba(p, donde, columna, fijar)}
          {p.descripcion && (
            <Box flexDirection="column">
              <Button key={kDesc} plain onPress={alternar(kDesc, descAbierta)}>
                {/* Con el brillo de la línea de la rama, como «Pasos» (decisión del propietario, 2026-10-31). */}
                <Text dimColor underline>
                  Descripción
                </Text>
              </Button>
              {descAbierta && bloqueDescripcion(p.descripcion, columna)}
            </Box>
          )}
          {bloquePasos(p, donde, fijar)}
        </Box>
      )
    }

    // La fila del título (decisión del propietario, 2026-10-31): a la izquierda, en una columna de ancho fijo
    // (columnaTitulo), lo que va antes del título (hueco, número y espacio); a su derecha, el título, que al partirse
    // sigue en su columna (sangría colgante). Con algo que desplegar, las dos partes despliegan: el título, con la
    // clave de la tarea; la izquierda, con <clave>:num (Button solo admite Text de hijos). El subrayado, solo en el número.
    // El tipo de la tarea, tras su título, entre paréntesis, en minúsculas y en el color de su título, sin atenuar: « (deliberar)» (decisión del
    // propietario, 2026-10-31). Sin tipo, nada.
    const sufijoTipo = (tipo: string | null | undefined) => (tipo ? ` (${tipo})` : '')
    const conTipo = (texto: string, tipo: string | null | undefined): RenderChildren[] =>
      tipo ? [texto, <Text>{sufijoTipo(tipo)}</Text>] : [texto]
    // Con `delante`, un margen de ese ancho antes de la cabeza, fuera de su botón: alinea los números a la derecha.
    const filaTitulo = (cabeza: RenderChildren, ancho: number, cuerpo: RenderChildren, clave: string | null, delante = 0) => (
      <Box flexDirection="row">
        <Box width={ancho} flexShrink={0} paddingLeft={delante}>
          {clave ? (
            <Button key={`${clave}:num`} plain onPress={alternar(clave)}>
              {cabeza}
            </Button>
          ) : (
            cabeza
          )}
        </Box>
        <Box flexShrink={1}>
          {clave ? (
            <Button key={clave} plain onPress={alternar(clave)}>
              {cuerpo}
            </Button>
          ) : (
            cuerpo
          )}
        </Box>
      </Box>
    )

    const peticion = (p: Peticion, conPrueba: boolean, donde: string) => {
      const id = String(p.id)
      // Las órdenes, en el menú de la tarea desplegada; en la línea plegada, solo el ● del subagente (decisión 168).
      const ordenes = donde === 'cola' || donde === 'observacion' ? menuOrdenes(p, donde) : null
      const agente = donde === 'cola' || donde === 'observacion' ? marcaSubagente(p, donde) : null
      const conEliminar = (fila: RenderChildren) =>
        agente ? (
          <Box flexDirection="row">
            <Box flexGrow={1} flexShrink={1}>
              {fila}
            </Box>
            {agente}
          </Box>
        ) : (
          fila
        )
      // Plegada, como arriba (decisión del propietario, 2026-10-31): solo «número título (tipo)», con el título
      // entero y sangría colgante. El OK de Claude va en la línea de la rama y la cuenta de pasos, en «Pasos N/M».
      // Cada fila, con su propia clave de despliegue por sección (norma del propietario, 2026-10-28).
      const k = `pet:${donde}:${p.id}`
      const hayMas = hayDetalle(p, conPrueba, ordenes)
      // Sin ▸/▾: el código de una tarea que se despliega va subrayado (norma del propietario, 2026-10-28).
      // El código, con el color de su letra; el de una tarea en curso, en amarillo. Su texto, sin amarillo: la línea en amarillo solo va arriba (decisión del propietario,
      // 2026-10-28, precisada el 2026-10-29: se refería al texto). Subrayado si se despliega.
      const enCursoP = enCursoOObservando(p)
      const codigo = (
        <Text>
          <Text color={colorNumero(p.id, enCursoP)} backgroundColor={fondoNumero(p.id)} underline={hayMas}>
            {id}
          </Text>
        </Text>
      )
      const columna = columnaTitulo(p.id)
      const fila = filaTitulo(
        <Text>{codigo} </Text>,
        columna,
        <Text color={TEXTO_TAREA} weight="regular">{conTipo(p.texto, p.tipo)}</Text>,
        hayMas ? k : null,
        hueco(p.id),
      )
      if (!hayMas || !abierta(k)) return conEliminar(fila)
      // Desplegada: debajo del título, su detalle.
      return (
        <Box flexDirection="column">
          {conEliminar(fila)}
          {detalleTarea(p, donde, conPrueba, columna, ordenes)}
        </Box>
      )
    }

    const grupos: [Peticion['estado'], string, string, boolean][] = [
      ['en-curso', 'curso', 'En curso', true],
      ['en-cola', 'cola', 'Pendientes', false],
      ['en-observacion', 'observacion', 'En observación', true],
    ]
    const grupo = ([estadoP, clave, titulo, conPrueba]: (typeof grupos)[number], desde = 0) => {
      // Cada tarea, en una sola sección (decisión del propietario, 2026-10-31): las en curso y la que se está
      // mirando, solo arriba, ni en Pendientes ni en observación. La última que ha cambiado arriba (petición 166).
      const lista = porCambio(est.peticiones.filter(p => p.estado === estadoP && !enCursoOObservando(p))).slice(desde)
      // Pendientes y En observación se ven siempre, también con 0, como Cerradas (petición del propietario, 2026-10-31):
      // si desaparecen, parece un fallo.
      // La cuenta, sin reparto por letra (decisión del propietario, 2026-10-31).
      const cuenta = String(lista.length)
      return seccion(clave, titulo, cuenta, lista.map(p => peticion(p, conPrueba, clave)))
    }
    // Las en curso van arriba, en amarillo; aquí, la cola. En observación va después, en el mismo bloque.
    // El error de la cola va con los demás avisos, bajo la cabecera.
    const secPeticiones = grupo(grupos[1])
    const secObservacion = grupo(grupos[2])

    // Propuestas: las por decidir del sf/propuestas.md del proyecto, la última sección, tras Cerradas (decisiones 194 y 197).
    const rf = est.realimentacion
    // La columna de los números de las propuestas: el más largo y un espacio; sin números, ninguna.
    const anchoNumProp = Math.max(0, ...(rf?.porRevisar ?? []).map(x => x.numero?.length ?? 0))
    const columnaProp = anchoNumProp > 0 ? anchoNumProp + 1 : 0
    const secPropuestas =
      rf === null
        ? null
        : seccion(
            'propuestas',
            'Propuestas',
            String(rf.porRevisar.length),
            <Box flexDirection="column">
              {/* Sin rótulo ni cuentas encima: la sección empieza por las propuestas; las por decidir, en su cabecera
                  (decisión del propietario, 2026-10-31). */}
              {rf.porRevisar.map(pr => {
                // Como las tareas (decisión del propietario, 2026-10-31): a la izquierda, en una columna de ancho fijo
                // común a todas, el número alineado a la derecha y un espacio; a su derecha, el título entero, con
                // sangría colgante. Plegada, solo número y título; desplegada, como una tarea de Pendientes:
                // el resumen en la columna del título y, tras todo el texto, su fila de etiquetas, a la izquierda (decisión 197).
                const k = `prop:${pr.titulo}`
                // «A Pendientes»: la pasa a tarea en cola del proyecto, sin Claude, como etiqueta de orden y con dos clics,
                // «¿A Pendientes? sí», como las demás que mueven una tarea (decisión 197; antes, la «→»).
                const marcaPendientes = `a-pendientes:${pr.numero ?? pr.titulo}`
                const confirmandoPendientes = aConfirmar === marcaPendientes
                const aTarea = etiquetaOrden(marcaPendientes, 'success', confirmandoPendientes ? '¿A Pendientes? sí' : 'A Pendientes', () => {
                  if (!confirmandoPendientes) return pedirConfirmar(marcaPendientes)
                  turnoConfirmar++
                  void update($, porConfirmar, () => null)
                    .then(() => convertirPropuesta($, pr))
                    .then(m => emergente($, m))
                    .catch(err => emergenteError($, `A Pendientes: ${String(err)}`))
                })
                // Sin ▸/▾: el número de la propuesta, subrayado, dice que se despliega.
                // Mismo estilo que las tareas: sin negrita y un punto menos de brillo.
                const cabeza = (
                  <Text color={TEXTO_TAREA} weight="regular">
                    {' '.repeat(anchoNumProp - (pr.numero?.length ?? 0))}
                    {pr.numero ? <Text underline>{pr.numero}</Text> : ''}{' '}
                  </Text>
                )
                const cuerpo = <Text color={TEXTO_TAREA} weight="regular">{pr.titulo}</Text>
                // Sin números en ninguna, sin columna: el título, en la columna 0.
                const fila =
                  columnaProp > 0 ? (
                    filaTitulo(cabeza, columnaProp, cuerpo, k)
                  ) : (
                    <Button key={k} plain onPress={alternar(k)}>
                      {cuerpo}
                    </Button>
                  )
                if (!abierta(k)) return fila
                return (
                  <Box flexDirection="column">
                    {fila}
                    {pr.resumen !== '' && (
                      <Box paddingLeft={columnaProp}>
                        <Text color={TEXTO_TAREA} weight="regular">
                          {pr.resumen}
                        </Text>
                      </Box>
                    )}
                    {filaOrdenes([aTarea])}
                  </Box>
                )
              })}
            </Box>,
          )

    // Cerradas en esta sesión, la última arriba, con su código en verde si se probó.
    // Una línea por petición; un clic despliega el texto entero y el commit.
    // Salen del historial (tarea 145): las tareas con un evento de cierre en la sesión, por la fecha del último. Cada
    // tarea, en una sola sección (decisión del propietario, 2026-10-31): solo las que ya han salido de la cola y las
    // descartadas que siguen en ella; una en observación, reabierta o de vuelta en Pendientes sale en su sección, no
    // aquí. Las eliminadas y las absorbidas por /sf_fusionar no entran: salen sin cerrarse.
    const ms = await read($, sesion)
    const limpiadas = ms.limpiadas ?? {}
    const porId = new Map<number, Cerrada>()
    for (const t of [...est.salidas, ...est.peticiones]) {
      const enLaCola = enCola.get(t.id)
      if (enLaCola !== undefined && enLaCola.estado !== 'descartada') {
        porId.delete(t.id)
        continue
      }
      if (t.estado === 'eliminada' || t.estado === 'absorbida') {
        porId.delete(t.id)
        continue
      }
      const e = ultimoCierre(t.historial, desde)
      if (e === null) continue
      porId.set(t.id, { id: t.id, texto: t.texto, commit: t.commit ?? commitsDe(t.historial)[0] ?? null, fecha: e.fecha ?? 0, tipo: t.tipo ?? null })
    }
    // Las quitadas con «limpiar» no salen mientras sigan cerradas (C), descartadas (D) o revertidas (R, solo las de
    // antes de la decisión 134) y sin otro cierre después; si vuelven a cerrarse, vuelven. Una revertida ahora no
    // queda en Cerradas: eliminada, no entra; de vuelta en Pendientes, sale solo allí, como reabierta.
    const limpiable = (id: number) => ['C', 'D', 'R'].includes(letra(id))
    const visible = (c: Cerrada) => !(limpiadas[String(c.id)] === c.fecha && limpiable(c.id))
    // Lo último arriba: la fecha más reciente entre su último cierre y el último cambio de su historial (decisión 129).
    const tocada = new Map([...est.salidas, ...est.peticiones].map(t => [t.id, Math.max(0, ...t.historial.map(e => e.fecha ?? 0))] as const))
    const orden = (c: Cerrada) => Math.max(c.fecha, tocada.get(c.id) ?? 0)
    const cerradas: Cerrada[] = [...porId.values()].filter(visible).sort((x, y) => orden(y) - orden(x))
    const total = cerradas.length
    // Botón para limpiar Cerradas: quita de la lista las cerradas (C), las descartadas (D) y las revertidas (R), las
    // que ya no piden nada; las descartadas salen además de la cola, con cola.py. Se llama «limpiar» (decisiones del
    // propietario, 2026-10-29). Es una etiqueta de orden, con dos clics, «¿Limpiar? sí», en el color de las órdenes:
    // no destruye trabajo (282).
    const aQuitar = cerradas.filter(c => limpiable(c.id))
    const conDescartadas = aQuitar.some(c => enCola.get(c.id)?.estado === 'descartada')
    const confirmandoLimpiar = aConfirmar === 'limpiar'
    const quitarProbadas =
      aQuitar.length === 0
        ? null
        : etiquetaOrden('limpiar-cerradas', 'success', confirmandoLimpiar ? '¿Limpiar? sí' : `Limpiar (${aQuitar.length})`, () => {
            if (!confirmandoLimpiar) return pedirConfirmar('limpiar')
            turnoConfirmar++
            void update($, porConfirmar, () => null)
              .then(() => limpiarCerradas($, aQuitar, conDescartadas))
              .then(aviso => {
                if (aviso) emergenteError($, aviso)
              })
              .catch(() => undefined)
          })
    // El push de develop que falló al cerrar una tarea, hasta que origin/develop tenga su commit (decisión 115, 19).
    const sinPush = new Set(est.pushPendiente)
    const lineaPush =
      est.pushPendiente.length === 0 ? null : (
        <Text color="warning">{enLinea(`falta el push de develop (${[...est.pushPendiente].sort((a, b) => a - b).join(' ')})`, 0)}</Text>
      )
    // Cerradas se ve siempre, también con 0 al empezar la sesión (decisión del propietario, 2026-10-28).
    const idsCerradas = cerradas.map(c => c.id)
    const secHecho =
      seccion(
            'hecho',
            'Cerradas',
            <Text dimColor={total === 0}>{total}</Text>,
            // «Limpiar (N)», solo desplegada, en su fila de etiquetas, a la izquierda, encima de la lista (282).
            [quitarProbadas && filaOrdenes([quitarProbadas]), ...cerradas.map(c => {
              const k = `hecho:${c.id}`
              const id = String(c.id)
              // Sin led: el código de la tarea va en verde si está cerrada (T o C) y en rojo si se ha reabierto
              // en observación para corregirla (A o H), con su mismo número (norma del propietario, 2026-10-28).
              const L = letra(c.id)
              // Desplegada, Revertir en su menú, en las cerradas (C) que han entrado en develop: con su
              // commit «… (N)» en develop (decisión del propietario, 2026-10-29). El primer clic la parte en
              // «¿Revertir?» [eliminar] [a Pendientes]; el segundo, en uno de ellos, revierte (decisiones 134 y 168).
              const revertir = L === 'C' && (est.mergeadas[id]?.length ?? 0) > 0
              // A observación, en todas las cerradas (C), antes de Revertir: la cerrada por error vuelve a observación
              // con su commit de develop, con dos clics (296).
              const reobservar = L === 'C'
              // Plegada, como arriba: el título entero, con sangría colgante; se despliega si tiene commit u órdenes.
              const hayMas = c.commit !== null || revertir || reobservar
              const codigo = (
                <Text>
                  <Text color={colorNumero(c.id)} backgroundColor={fondoNumero(c.id)} underline={hayMas}>
                    {id}
                  </Text>
                </Text>
              )
              const fila = filaTitulo(<Text>{codigo} </Text>, columnaTitulo(c.id), <Text color={TEXTO_TAREA} weight="regular">{conTipo(c.texto, c.tipo)}</Text>, hayMas ? k : null, hueco(c.id))
              if (!hayMas || !abierta(k)) return fila
              return (
                <Box flexDirection="column">
                  {fila}
                  {(reobservar || revertir) && (
                    <Box flexDirection="row" flexWrap="wrap">
                      {reobservar && botonAccion(c, 'hecho', 'reobservar')}
                      {revertir && botonAccion(c, 'hecho', 'revertir')}
                    </Box>
                  )}
                  {/* Sin rama ni pasos: la línea empieza por el commit, en la columna 0. Sin commit ni push pendiente, no
                      sale: ni rótulos vacíos ni filas gastadas (decisión del propietario, 2026-10-31). */}
                  {lineaDetalle([
                    c.commit ? <Text dimColor>Commit: {c.commit}</Text> : null,
                    sinPush.has(c.id) ? <Text color="warning">falta el push</Text> : null,
                  ])}
                </Box>
              )
            }), lineaPush].filter(x => x !== null),
          )

    // Métricas de la sesión: los ceros, atenuados.
    const nPrompts = await read($, prompts)
    // Estilo marcador, compacto: solo los prompts (decisión del propietario, 2026-10-27), cada una con la cifra en negrita y en color
    // delante de su etiqueta; los ceros, atenuados. Las cerradas se cuentan en la cabecera de Cerradas.
    const metricas: [number, string, string][] = [
      [nPrompts, 'prompts', 'suggestion'],
    ]
    // Cada casilla, una etiqueta con fondo, como todo lo de la cabecera (decisión del propietario, 2026-10-29); con
    // el ancho común de la cabecera (tarea 260) y sin encogerse, para que la rama no la parta en líneas.
    // Con el ancho común, «N prompts» se come su relleno antes que ensanchar la etiqueta.
    const casilla = ([n, etiqueta, color]: [number, string, string]) => {
      const t = `${String(n)} ${etiqueta}`
      const w = anchoDe(t, 0)
      const [i, d] = huecos(t.length, w)
      return (
        <Box flexShrink={0} marginRight={1} width={w} backgroundColor={FONDO_ETIQUETA}>
          <Text backgroundColor={FONDO_ETIQUETA}>
            {' '.repeat(i)}
            <Text weight="bold" color={n === 0 ? undefined : color} dimColor={n === 0}>
              {String(n)}
            </Text>{' '}
            <Text dimColor>{etiqueta}</Text>
            {' '.repeat(d)}
          </Text>
        </Box>
      )
    }
    // El marcador va fijo en la segunda fila de la cabecera, tras la duración, sin sección: siempre a la vista. Pasó
    // de la primera a la segunda para dejar sitio a RELEASE en un panel estrecho (decisión del propietario, 2026-10-29).
    // La duración de la sesión, en horas y minutos, en una etiqueta a la izquierda de la segunda fila (decisión del
    // propietario, 2026-10-29): cuenta desde que se abrió; /reload-plugins no la reinicia.
    const inicio = await read($, inicioSesion)
    const ultimo = await read($, minuto)
    const transcurrido = inicio > 0 ? Math.max(0, Math.max(ultimo, await $.clock.now()) - inicio) : null
    const duracion =
      transcurrido === null ? null : (() => {
        const min = Math.floor(transcurrido / 60_000)
        const h = Math.floor(min / 60)
        return h > 0 ? `${String(h)}h ${String(min % 60).padStart(2, '0')}m` : `${String(min)}m`
      })()
    // El ancho común de las etiquetas de la cabecera, salvo la rama (tarea 260; ANCHO_ETIQUETA, en estilo.ts): cuántas
    // salen en cada fila y sus textos. ACTUALIZAR o REFRESCAR se cuenta como ACTUALIZAR, la más larga de las dos.
    const hayActualizar = est.tipo !== 'sin-sf' && (await read($, actualizacion)) !== null
    const hayPrueba = est.tipo === 'sf' && ((await read($, prueba)).disponible || (await desdeCopia($)))
    const textoSf = est.versionPlugin ? `SF ${est.versionPlugin}` : 'SF'
    // Lo que necesita cada una como mínimo: su texto; el relleno se sacrifica antes que el ancho común.
    const fila1 = [hayActualizar && 'ACTUALIZAR'.length, est.tipo !== 'sin-sf' && 'RELEASE'.length, est.tipo !== 'sin-sf' && 'TURBO'.length, hayPrueba && 'PRUEBA'.length, textoSf.length]
    const fila2 = [duracion !== null && duracion.length, `${String(nPrompts)} prompts`.length]
    const deFila = (f: (number | false)[]) => f.filter((n): n is number => typeof n === 'number')
    const comun = anchoComun(ancho, [
      { necesita: deFila(fila1), reserva: 0 },
      // La rama va sola en la tercera fila: no le quita sitio a la segunda.
      { necesita: deFila(fila2), reserva: 0 },
    ])
    // El ancho de una etiqueta de texto t: el común si su texto cabe en él (con el relleno que quepa); si no (las que
    // piden confirmar), el suyo con `relleno`; sin común, el suyo, con un espacio a cada lado.
    const anchoDe = (t: string, relleno = 2) => (comun === null ? t.length + 2 : t.length <= comun ? comun : t.length + relleno)
    const marcador = (
      <Box flexDirection="row" flexShrink={0}>
        {metricas.map(casilla)}
      </Box>
    )
    const etiquetaDuracion =
      duracion === null ? null : (
        <Box flexShrink={0} marginRight={1} width={anchoDe(duracion)} backgroundColor={FONDO_ETIQUETA}>
          <Text backgroundColor={FONDO_ETIQUETA} dimColor>
            {centrar(duracion, anchoDe(duracion))}
          </Text>
        </Box>
      )
    // TURBO, a la izquierda de la etiqueta del modo prueba, donde hay cola (decisión del propietario, 2026-10-29):
    // pide a Claude que ponga en curso las tareas que no necesitan al propietario (160). Fondo neutro y letra en
    // cian, en negrita: no se confunde con los fondos llenos de PRUEBA ni del nombre.
    const etiquetaTurbo =
      est.tipo !== 'sin-sf' ? (
        <Box marginRight={1} flexShrink={0} width={anchoDe('TURBO')} backgroundColor={FONDO_ETIQUETA}>
          <Button key="turbo" plain onPress={() => pedirTurbo($)}>
            <Text color={COLOR_TURBO} weight="bold" backgroundColor={FONDO_ETIQUETA}>
              {centrar('TURBO', anchoDe('TURBO'))}
            </Text>
          </Button>
        </Box>
      ) : null

    // RELEASE, a la izquierda de TURBO, en todos los proyectos con SF (decisión del propietario, 2026-10-29). El primer
    // clic lee la versión (el último tag vX.Y.Z, también en la SF: decisión 226) y en su lugar
    // salen las siguientes: patch, minor y major, o, sin ninguna, «¿Primera versión?» con v0.1.0 y v1.0.0. Al elegir
    // una, pide confirmarla con otro clic. A los 5 s, o con un clic en otro botón, vuelve a ser RELEASE. Confirmada,
    // publica con git y sin Claude.
    const fuente = await read($, fuenteRelease)
    const enObservacion = est.peticiones.filter(p => p.estado === 'en-observacion').map(p => p.id)
    const abrirRelease = () => {
      turnoConfirmar++
      void versionActual($)
        .then(async f => {
          await update($, fuenteRelease, () => f)
          pedirConfirmar('release')
        })
        .catch(err => emergenteError($, `RELEASE: no se pudo leer la versión (${String(err)}).`))
    }
    const elegirVersion = (v: string) => () => {
      const marca = `release:${v}`
      if (aConfirmar !== marca) return pedirConfirmar(marca)
      turnoConfirmar++
      void update($, porConfirmar, () => null)
        .then(async () => {
          emergente($, `RELEASE: publicando v${v}…`)
          const r = await publicarVersion($, fuente!, v)
          emergenteRespuesta($, r)
          // Recién publicada, ACTUALIZAR la ofrece si lo instalado se ha quedado atrás.
          if (r.ok) await comprobarActualizacion($)
        })
        .catch(err => emergenteError($, `RELEASE: no se pudo publicar v${v} (${String(err)}).`))
    }
    // Con `w`, centrado en ese ancho; sin él (las versiones a elegir), con un espacio a cada lado.
    const textoRelease = (t: string, w = t.length + 2) => (
      <Text color={COLOR_RELEASE} weight="bold" backgroundColor={FONDO_ETIQUETA}>
        {centrar(t, w)}
      </Text>
    )
    const elegida = aConfirmar?.startsWith('release:') && fuente ? aConfirmar.slice('release:'.length) : null
    const etiquetaRelease =
      est.tipo === 'sin-sf' ? null : elegida ? (
        <Box marginRight={1} flexShrink={0} width={anchoDe(`¿Publicar v${elegida}? sí`)} backgroundColor={FONDO_ETIQUETA}>
          <Button key={`release-v:${elegida}`} plain onPress={elegirVersion(elegida)}>
            {textoRelease(`¿Publicar v${elegida}? sí`, anchoDe(`¿Publicar v${elegida}? sí`))}
          </Button>
        </Box>
      ) : aConfirmar === 'release' && fuente ? (
        <Box flexDirection="row" marginRight={1} flexShrink={0}>
          {fuente.actual === null && <Text dimColor>{'¿Primera versión? '}</Text>}
          {siguientesVersiones(fuente.actual).map(v => (
            <Box marginRight={1} flexShrink={0}>
              <Button key={`release-v:${v}`} plain onPress={elegirVersion(v)}>
                {textoRelease(`v${v}`)}
              </Button>
            </Box>
          ))}
        </Box>
      ) : (
        <Box marginRight={1} flexShrink={0} width={anchoDe('RELEASE')} backgroundColor={FONDO_ETIQUETA}>
          <Button key="release" plain onPress={abrirRelease}>
            {textoRelease('RELEASE', anchoDe('RELEASE'))}
          </Button>
        </Box>
      )
    // ACTUALIZAR, a la izquierda de todo, solo con una versión publicada mayor que la instalada de sf@softwarefactory
    // en algún scope que use el proyecto (decisión del propietario, 2026-10-29). El primer clic pide confirmarla; a
    // los 5 s, o con un clic en otro botón, vuelve. Confirmada, `claude plugin update` en cada scope, sin Claude.
    // REFRESCAR, en su sitio, cuando lo instalado está al día y la sesión corre una versión más vieja: confirmado,
    // recarga el plugin (decisión 177).
    const nueva = await read($, actualizacion)
    const refresco = nueva !== null && esRefresco(nueva)
    const boton = refresco ? 'refrescar' : 'actualizar'
    const pulsarActualizar = () => {
      if (!nueva) return
      if (aConfirmar !== boton) return pedirConfirmar(boton)
      turnoConfirmar++
      void update($, porConfirmar, () => null)
        .then(async () => {
          emergente($, refresco ? `REFRESCAR: recargando sf v${nueva.version}…` : `ACTUALIZAR: actualizando a v${nueva.version}…`)
          emergenteRespuesta($, await actualizarPlugin($, nueva))
        })
        .catch(err =>
          emergenteError($, 
            refresco
              ? `REFRESCAR: no se pudo recargar sf v${nueva.version} (${String(err)}).`
              : `ACTUALIZAR: no se pudo actualizar a v${nueva.version} (${String(err)}).`,
          ),
        )
    }
    const textoBoton = refresco
      ? aConfirmar === boton ? `¿Refrescar a v${nueva.version}? sí` : 'REFRESCAR'
      : aConfirmar === boton ? `¿Actualizar a v${nueva?.version ?? ''}? sí` : 'ACTUALIZAR'
    const etiquetaActualizar =
      est.tipo === 'sin-sf' || !nueva ? null : (
        <Box marginRight={1} flexShrink={0} width={anchoDe(textoBoton)} backgroundColor={FONDO_ETIQUETA}>
          <Button key={boton} plain onPress={pulsarActualizar}>
            <Text color={COLOR_ACTUALIZAR} weight="bold" backgroundColor={FONDO_ETIQUETA}>
              {centrar(textoBoton, anchoDe(textoBoton))}
            </Text>
          </Button>
        </Box>
      )
    // Con una versión por confirmar, el aviso de las tareas que quedan en observación, sin bloquear.
    const avisoRelease =
      elegida && enObservacion.length > 0 ? `${String(enObservacion.length)} en observación: ${enObservacion.join(', ')}` : null

    // El proyecto se incorporó con una SF anterior: se dice y cómo ponerlo al día (decisión del propietario, 2026-10-28).
    // O, al día de versión, si su CLAUDE.md aún importa la copia .sf/claude-sf.md de las reglas, que ya entrega el mod
    // (decisión 187): el mismo remedio.
    const avisoVersion = atrasada(est)
      ? `incorporado con la SF ${est.versionSf}; va por la ${est.versionPlugin}: pide a Claude «pon el proyecto al día con la SF»`
      : est.tipo === 'proyecto' && est.importaCopia
        ? 'su CLAUDE.md importa la copia vieja de las reglas (.sf/claude-sf.md): pide a Claude «pon el proyecto al día con la SF»'
        : null
    // La sesión corre una SF más vieja que la instalada: se dice también en los avisos, que se ven aunque la cabecera,
    // con REFRESCAR, esté en su turno de avisos (decisión 177).
    const avisoRecarga = est.tipo === 'sin-sf' ? null : avisoRefresco(nueva)
    const avisos = [est.error, est.aviso, est.errorPeticiones, ...(est.avisosConfiguracion ?? []), avisoRecarga, avisoVersion].filter((x): x is string => x !== null)
    // Con avisos, se turnan con la cabecera en sus filas, unos 5 s cada uno (decisión 164). Mientras un botón de la
    // cabecera espera su segundo clic, la cabecera se queda: los botones no se mueven.
    conAvisos = avisos.length > 0
    const enBotonCabecera = aConfirmar === 'actualizar' || aConfirmar === 'refrescar' || (aConfirmar?.startsWith('release') ?? false)
    const turno = await read($, turnoAvisos)
    const verAvisos = conAvisos && !enBotonCabecera && turno % 2 === 1
    // Con varios, uno por turno blanco, en ciclo (petición del propietario, 2026-11-01).
    const avisoDelTurno = avisos[Math.floor(turno / 2) % Math.max(1, avisos.length)] ?? ''
    // Y el fondo, blanco y gris claro, un turno blanco cada uno: se nota que cambia; con uno solo, siempre blanco.
    const fondoAviso = avisos.length > 1 && Math.floor(turno / 2) % 2 === 1 ? FONDO_AVISO_ALTERNO : FONDO_AVISO
    // Modo prueba, solo en la SF y con el catálogo local registrado: «PRUEBA» en naranja si el panel viene de la
    // copia de trabajo; «prueba» atenuada si viene del publicado. Un clic cambia los ajustes; /reload-plugins aplica.
    const mp = await read($, prueba)
    const activo = await desdeCopia($)
    const etiquetaPrueba =
      est.tipo === 'sf' && (mp.disponible || activo) ? (
        <Box marginRight={1} flexShrink={0} width={anchoDe('PRUEBA')} backgroundColor={activo ? COLOR_PRUEBA : undefined}>
          <Button
            key="modo-prueba"
            plain
            onPress={() => void cambiarPrueba($, !activo).catch(() => undefined)}
          >
            {activo ? (
              <Text color="#000000" backgroundColor={COLOR_PRUEBA}>
                {centrar('PRUEBA', anchoDe('PRUEBA'))}
              </Text>
            ) : (
              <Text>
                {' '.repeat(huecos(6, anchoDe('prueba'))[0])}
                <Text dimColor underline>
                  prueba
                </Text>
                {' '.repeat(huecos(6, anchoDe('prueba'))[1])}
              </Text>
            )}
          </Button>
        </Box>
      ) : null
    const avisoPrueba =
      est.tipo === 'sf' && activo !== mp.pedido && (mp.disponible || activo) ? (
        <Text color={COLOR_PRUEBA}>
          /reload-plugins para {mp.pedido ? 'entrar en el' : 'salir del'} modo prueba
        </Text>
      ) : null
    // Arriba del todo, tras el proyecto, la tarea en la que se trabaja; con varias en curso, cuántas más hay.
    const enCurso = enCursoRecientes(est)
    const tarea = tareaPrincipal(est)
    // En amarillo en todos los proyectos: se lee bien en el panel (decisión del propietario, 2026-10-27).
    // El amarillo de la paleta (#ca8a04) se ve mostaza en el panel oscuro: uno claro, propio de la tarea.
    const colorTarea = COLOR_TAREA
    // Cada tarea en curso de arriba, en amarillo y entera, en varias líneas si hace falta (decisión del propietario,
    // 2026-10-29; antes, solo la primera). Plegada, solo su título; con algo que desplegar, su número va subrayado y
    // un clic la despliega: debajo, su detalle, como en las secciones (decisión del propietario, 2026-10-31).
    const tareaArriba = (p: Peticion) => {
      const k = `arriba:${p.id}`
      // Arriba, también el menú de órdenes al desplegarla (decisión 168).
      const ordenes = menuOrdenes(p, 'arriba')
      const titulo = p.texto
      // Arriba, «Prueba» (cómo probarla y el OK de Claude, tarea 237), como en observación: la que se está mirando y
      // también las en curso, que el propietario prueba en su rama sin pasarlas a observación (tarea 266).
      const conPrueba = true
      const hayMas = hayDetalle(p, conPrueba, ordenes)
      const abiertaT = hayMas && abierta(k)
      // El número y, a su derecha, el título, con sangría colgante (decisión del propietario, 2026-10-31).
      const linea = filaTitulo(
        <Text color={colorTarea} weight="regular">
          <Text backgroundColor={fondoNumero(p.id)} underline={hayMas}>
            {p.id}
          </Text>{' '}
        </Text>,
        columnaTitulo(p.id),
        <Text color={colorTarea} weight="regular">
          {conTipo(abiertaT ? p.texto : titulo, p.tipo)}
        </Text>,
        hayMas ? k : null,
        hueco(p.id),
      )
      return (
        <Box flexDirection="column">
          <Box flexDirection="row">
            <Box flexGrow={1} flexShrink={1}>
              {linea}
            </Box>
            {marcaSubagente(p, 'arriba')}
          </Box>
          {abiertaT && detalleTarea(p, 'arriba', conPrueba, columnaTitulo(p.id), ordenes)}
        </Box>
      )
    }
    const lineaTarea = tarea ? (
      <Box flexDirection="row" marginTop={1}>
        <Box flexDirection="column" flexShrink={1}>
          {/* Todo en amarillo, número incluido, y sin negrita; las demás en curso, debajo, una línea cada una. */}
          {enCurso.length > 0 ? (
            enCurso.map(p => tareaArriba(p))
          ) : (
            <Text color={colorTarea} weight="regular">
              devslice {tarea}
            </Text>
          )}
        </Box>
      </Box>
    ) : (
      <Box marginTop={1}>
        <Text dimColor>▷ ninguna tarea en curso</Text>
      </Box>
    )
    // Un solo bloque, con su fondo y sin rótulo (282), en el orden del ciclo de las tareas (decisión del propietario,
    // 2026-10-28): Pendientes, En observación y Cerradas; Propuestas, la última (decisión 197). Sin propuestas.md, sin
    // Propuestas.
    const bloqueTareas = (
      <Box flexDirection="column" backgroundColor={FONDO_BLOQUE} paddingBottom={1}>
        <Box flexDirection="column" gap={1}>
          {[secPeticiones, secObservacion, secHecho, secPropuestas]}
        </Box>
      </Box>
    )
    // La rama activa de la carpeta del proyecto, sola en la tercera fila de la cabecera, a la izquierda (tarea 260; antes,
    // a la derecha de la segunda): fondo neutro; en el
    // amarillo de la tarea si es la rama de una tarea en curso o en observación; en una cabeza separada, el commit corto
    // (decisión del propietario, 2026-10-29).
    const ramaCabecera = () => {
      const r = est.rama
      if (!r) return null
      const deTarea = !r.separada && est.peticiones.some(p => p.rama === r.nombre && (p.estado === 'en-curso' || p.estado === 'en-observacion'))
      // A la izquierda, bajo la duración (petición del propietario, 2026-11-01): se recorta solo si no cabe en la fila, contando el
      // espacio de cada lado de la etiqueta.
      const libre = ancho - 2
      const nombre = recortar(r.separada ? `(${r.nombre})` : r.nombre, Math.max(6, libre))
      return (
        <Box flexDirection="row" flexShrink={1}>
          {/* Etiqueta con el estilo de la de los prompts (decisión del propietario, 2026-10-29): fondo neutro; la letra,
              en el amarillo de la tarea si es la rama de una tarea, y si no, atenuada. */}
          <Text color={deTarea ? COLOR_TAREA : undefined} dimColor={!deTarea} backgroundColor={FONDO_ETIQUETA} wrap="truncate-end">
            {` ${nombre} `}
          </Text>
        </Box>
      )
    }
    // Bajo la cabecera, el cuerpo: sube las filas desplazadas sin cambiar su alto y recorta lo que queda encima.
    const k = await read($, desplazamiento)
    const cuerpo = (...hijos: RenderChildren[]) => (
      <Box flexDirection="column" overflow="hidden">
        <Box flexDirection="column" gap={1} position="relative" top={k > 0 ? -k : 0}>
          {hijos}
        </Box>
      </Box>
    )
    // La etiqueta de la derecha: «SF» y la versión del plugin que corre, en todos los proyectos, también sin SF
    // (decisión del propietario, 2026-10-30); sin versión legible, «SF» a secas.
    const etiquetaSf = est.versionPlugin ? `SF ${est.versionPlugin}` : 'SF'
    const avisarComprobacion = () =>
      void (async () => emergente($, avisoComprobacion(await read($, comprobadaEn), await $.clock.now()), false))().catch(() => undefined)
    // La cabecera, de alto fijo: sus dos filas, la de la rama si la hay y la de relleno de abajo. Con avisos, en su
    // turno, los avisos, en un bloque blanco de dos filas (decisión 164), con el mismo alto.
    const filaRama = ramaCabecera()
    const altoCabecera = ALTO_CABECERA + (filaRama ? 1 : 0)
    const cabecera = () =>
      verAvisos ? (
        // El bloque blanco, en las dos primeras filas; las demás, vacías, con el fondo del panel: la cabecera no cambia
        // de alto (petición del propietario, 2026-11-01). Un clic en un aviso los quita hasta su siguiente turno.
        <Box flexDirection="column" height={altoCabecera} flexShrink={0}>
          <Box flexDirection="column" height={ALTO_AVISOS} flexShrink={0} overflow="hidden" backgroundColor={fondoAviso} paddingX={1}>
            {lineasAviso(avisoDelTurno, Math.max(8, ancho - 3)).map((l, i) => (
              <Button key={`aviso:${String(i)}`} plain onPress={() => void quitarAvisos($).catch(() => undefined)}>
                <Text color={COLOR_AVISO} wrap="truncate-end">
                  {l}
                </Text>
              </Button>
            ))}
          </Box>
        </Box>
      ) : (
      <Box flexDirection="column" height={altoCabecera} flexShrink={0}>
        {/* Dos filas (decisión del propietario, 2026-10-29) y la de la rama (tarea 260). La primera: ACTUALIZAR, RELEASE, TURBO y el modo prueba a la
            izquierda y, a la derecha, la etiqueta de la SF con los colores de la etiqueta de la sesión (fondo del color
            de /color y letra negra); sin color, atenuada como los rótulos de los bloques. */}
        <Box flexDirection="row">
          {etiquetaActualizar}
          {etiquetaRelease}
          {etiquetaTurbo}
          {etiquetaPrueba}
          <Box flexGrow={1} />
          {/* Al pulsarla, cuánto falta para la próxima comprobación de versión (tarea 238). */}
          {est.color ? (
            <Box backgroundColor={RGB[est.color as (typeof COLORES)[number]]} width={anchoDe(etiquetaSf)} flexShrink={0}>
              <Button key="version-sf" plain onPress={avisarComprobacion}>
                <Text color="#000000">{centrar(etiquetaSf, anchoDe(etiquetaSf))}</Text>
              </Button>
            </Box>
          ) : (
            <Box flexShrink={0} width={anchoDe(etiquetaSf)}>
              <Button key="version-sf" plain onPress={avisarComprobacion}>
                <Text dimColor>{centrar(etiquetaSf, anchoDe(etiquetaSf))}</Text>
              </Button>
            </Box>
          )}
        </Box>
        {/* La segunda: la duración y los prompts, a la izquierda. */}
        <Box flexDirection="row">
          <Box flexDirection="row" flexGrow={1} flexShrink={0}>
            {etiquetaDuracion}
            {marcador}
          </Box>
        </Box>
        {/* La tercera, si hay rama: la rama sola, a la izquierda, bajo la duración. */}
        {filaRama && <Box flexDirection="row">{filaRama}</Box>}
        {/* En la fila de relleno, con una versión por confirmar, las tareas que quedan en observación, sin bloquear. */}
        {avisoRelease && (
          <Box backgroundColor={FONDO_AVISO} paddingX={1}>
            <Text color={COLOR_AVISO} wrap="truncate-end">
              ⚠ {avisoRelease}
            </Text>
          </Box>
        )}
      </Box>
      )
    // Lo que va bajo la cabecera y sube con el scroll: el aviso de prueba y la tarea en curso con sus pasos (decisión
    // del propietario, 2026-10-29). Los avisos van en la cabecera (decisión 164). La línea gris del proyecto (versión
    // de la SF, fase y devslice; «sin SF» sin SF), de momento, no sale aquí: solo en la caja sobre el prompt
    // (decisión 166).
    // Sin pantalla completa, arriba del todo: los botones no responden (tarea 264).
    const avisoPantalla = sinPantallaCompleta(e) ? (
      <Box backgroundColor={FONDO_AVISO} paddingX={1}>
        <Text color={COLOR_AVISO}>⚠ {AVISO_PANTALLA}</Text>
      </Box>
    ) : null
    const bajoCabecera = () =>
      avisoPantalla || avisoPrueba || lineaTarea ? (
        <Box flexDirection="column">
          {avisoPantalla}
          {avisoPrueba}
          {lineaTarea}
        </Box>
      ) : null

    // Una columna libre a la derecha: un espaciador de una columna junto al contenido, que no depende de que el motor
    // respete el ancho o el margen de la caja raíz (decisión del propietario, 2026-10-30).
    const conMargen = (contenido: RenderChildren) => (
      <Box flexDirection="row">
        <Box flexDirection="column" flexGrow={1} flexShrink={1}>
          {contenido}
        </Box>
        <Box width={1} flexShrink={0} />
      </Box>
    )
    if (est.tipo === 'sin-sf') {
      return conMargen(
        <Box flexDirection="column">
          {cabecera()}
          {cuerpo(
            bajoCabecera(),
            seccion(
              'incorporar',
              'Incorporarlo a la SF',
              null,
              <Box flexDirection="column">
                <Text>Pide a Claude «incorpora este proyecto a la SF» (skill sf:incorporar_proyecto_a_sf), o crea {PROYECTO}, por ejemplo:</Text>
                <Text dimColor>{ejemploProyecto(est.versionPlugin)}</Text>
                <Text>Y el estado, en {ESTADO} (fuera de git):</Text>
                <Text dimColor>{EJEMPLO_ESTADO}</Text>
              </Box>,
            ),
            bloqueTareas,
          )}
        </Box>,
      )
    }

    // El mismo panel en todos los proyectos, la SF incluida, sin adaptaciones (decisión del propietario,
    // 2026-10-28): un solo bloque, sin rótulo (decisión 197).
    return conMargen(
      <Box flexDirection="column">
        {cabecera()}
        {cuerpo(bajoCabecera(), bloqueTareas)}
      </Box>,
    )
  })
}
