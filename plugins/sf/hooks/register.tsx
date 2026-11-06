import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'
import type { Paso, Peticion, Sesion } from '../types'
import { CADA_COMPROBACION, arrancar, comprobarActualizacion, copiarCola, elegirPasos, enCursoRecientes, etiqueta, fusionable, motivoFusion, motivoSplit, numerosDe, olvidarTitulosInicio, ordenCola, pedirConfiguracion, pedirFusion, pedirRedescripcion, pedirSplit, refrescar, refrescarSubagentes, separable } from './cola'
import { CLAVE_PLEGADO, PANEL, migrarPlegado } from './constantes'
import { escribir } from './control'
import { cargarAvisosPanel, encargarAClaude, tomarAvisoPanel } from './avisos'
import { alCargarIncorporacion, anadirRegla, anotarRespuestaIncorporar, cerrarIncorporacionTerminada, contextoInicial, contextoPython, menuEnIncorporacion, pausarIncorporacion, ofrecerIncorporar, recargarSiPedido, reanudarIncorporacion, reglasAlIncorporar, reiniciarIncorporar, sugerirIncorporar } from './contexto'
import { detectarPython } from './python'
import { marcarSubagente } from './lectura'
import type { $ } from './lectura'
import { emergente, emergenteError } from './emergentes'
import { ofrecerPantalla, reiniciarOferta } from './pantalla'
import { CATALOGO_PRUEBA, apagarAlCerrar, apagarAlEntrar, cambiarPrueba, desdeCopia, leerAjustes, marcarTurno } from './prueba'
import { registrarPanel, turnarAvisos } from './panel'
import { leerAvisoSubagentes, rearmarAvisosSubagentes, recuperarSubagentes, SIN_AVISO } from './subagentes'
import { asegurarSesion, decidirSesion, forzarActiva, forzarInactiva, latirSesion, sesionSfActual, sfApagada, soltarAlCerrar, tomarAvisoSesion } from './latido'

// Valores de estado del mod: el motor exige declararlos en el archivo que los usa; con el mismo
// plugin y clave, son el mismo valor en todos los archivos.
// Cambiar la etiqueta si cambian los campos de Estado.
const estado = atom({ plugin: 'sf', key: 'estado' } as const, null, {
  shape: 'estado-17',
})
// Propuestas añadidas en esta sesión de la SF: títulos nuevos respecto a los del inicio.
// Prompts enviados por el propietario en esta sesión.
const prompts = atom({ plugin: 'sf', key: 'prompts' } as const, 0)
// Los mensajes que son del propietario: los que escribe en la terminal o por Remote Control.
const DEL_PROPIETARIO = new Set(['composer', 'bridge'])
// Inicio de la sesión (ms) y último minuto contado: la duración de la cabecera. Viven en $.state: sobreviven a
// /reload-plugins y acaban con la sesión.
const inicioSesion = atom({ plugin: 'sf', key: 'inicioSesion' } as const, 0)
const minuto = atom({ plugin: 'sf', key: 'minuto' } as const, 0)
// La hora de la última comprobación del latido en la red (la del latido, /sf o RELEASE; al empezar, la del arranque): la escriben register.tsx y cola.ts, y la lee
// el panel para decir, al pulsar la etiqueta de la versión, cuánto falta para la próxima (tarea 238).
const comprobadaEn = atom({ plugin: 'sf', key: 'comprobadaEn' } as const, null as number | null)
// Las Cerradas que el propietario ha quitado de la lista en esta sesión: tras un /clear vuelven a contar.
const sesion = atom({ plugin: 'sf', key: 'sesion' } as const, { limpiadas: {} } as Sesion)
// El propietario cerró el panel a mano: vuelve la caja sobre el prompt hasta que lo reabra con /sf.
const panelCerrado = atom({ plugin: 'sf', key: 'panelCerrado' } as const, false)
// El panel se abre solo una vez por carga del módulo; después manda lo que haga el propietario.
// Secciones del panel plegadas (true) o abiertas (false) por el propietario; las que no ha tocado siguen
// PLEGADAS_DE_INICIO. Se recuerdan entre sesiones en $.store.
const plegado = atom({ plugin: 'sf', key: 'plegado' } as const, {} as Record<string, boolean>)

// Añade el paso, pendiente, a la tarea `id` con «cola.py paso añadir» (antes de los pasos de cierre, si los tiene) y
// avisa a Claude para que se ponga con él sin esperar a un «continúa»: si está trabajando, al acabar el turno; si no,
// en el momento (decisión del propietario, 2026-10-28). El aviso sale de un temporizador: el motor no deja enviarlo
// desde el hook del comando.
async function escribirPaso($: $, id: number, texto: string): Promise<string> {
  const r = await ordenCola($, ['paso', 'añadir', String(id), texto])
  await refrescar($)
  if (!r.ok) return `/sf_paso: ${r.mensaje}`
  const aviso = `Paso añadido con /sf_paso a la ${String(id)}: «${texto}». Hazlo ahora, dentro de esa tarea: márcalo en curso y, al acabar, hecho; sigue hasta terminar o hasta necesitar mi feedback.`
  $.clock.after(50, () => {
    void encargarAClaude($, aviso).catch(err => emergenteError($, `/sf_paso: no se pudo avisar a Claude: ${String(err)}`))
  })
  return `Paso añadido a la ${String(id)}: ${texto}`
}

const USO_SPLIT = 'Uso: /sf_split, /sf_split 89 o /sf_split 89 2,3 (la tarea y los números de sus pasos, en su orden)'
// /sf_split con la tarea ya elegida: pregunta los pasos o, con más de cuatro, devuelve la forma corta.
const elegir = ($: $, p: Peticion) => elegirPasos($, p) ?? `Elige qué pasos de la ${String(p.id)} separas.`

const USO_FUSIONAR = 'Uso: /sf_fusionar o /sf_fusionar 104 105 (dos tareas o más, en cola o en curso)'

// Lo que hace el mod al cargarse, en session.start y tras un /clear: lee el estado y lo que depende de la sesión.
// Devuelve el momento de la carga. `nueva`: tras un /clear, que empieza una sesión nueva en el panel (decisión 165):
// la duración, los prompts, las Cerradas y las mejoras nuevas cuentan desde ahí, y salen las descartadas de antes,
// aunque el motor no haya vaciado $.state. /reload-plugins no la reinicia.
async function cargar($: $, nueva = false): Promise<number> {
  let guardado = (await $.store.get(CLAVE_PLEGADO).catch(() => undefined)) as Record<string, boolean> | undefined
  // El plegado de antes de «En observación» se convierte una vez y se guarda así (decisión 215).
  const convertido = guardado && typeof guardado === 'object' ? migrarPlegado(guardado) : null
  if (convertido) {
    guardado = convertido
    await $.store.set(CLAVE_PLEGADO, convertido).catch(() => undefined)
  }
  if (guardado && typeof guardado === 'object') await update($, plegado, () => guardado)
  // El inicio de la sesión, solo la primera vez (/reload-plugins no lo reinicia): antes de leer, porque el historial
  // de las tareas se lee desde ahí.
  const ahora = await $.clock.now()
  const primera = nueva || (await read($, inicioSesion)) === 0
  if (primera) await update($, inicioSesion, () => ahora)
  if (nueva) {
    await update($, minuto, () => ahora)
    await update($, prompts, () => 0)
    await update($, sesion, () => ({ limpiadas: {} }))
    await reiniciarOferta($)
    await reiniciarIncorporar($)
    olvidarTitulosInicio()
    await rearmarAvisosSubagentes($)
  }
  // Lo que se sabía de los subagentes de esta sesión, si el estado acaba de empezar (tarea 277): antes de leerlos.
  await recuperarSubagentes($).catch(() => undefined)
  // El intérprete de Python de la máquina (236), antes de lanzar nada con él.
  await detectarPython($, true)
  // El cola.py que lanza el panel: una copia del de este plugin, hecha ahora (decisión 136).
  await copiarCola($)
  await arrancar($, primera)
  // Una sola sesión con la SF por proyecto (decisión 193): si otra la tiene, esta arranca con ella apagada. Antes del
  // modo prueba: una sesión apagada no lo toca, que es de la que tiene la SF.
  await decidirSesion($).catch(() => undefined)
  if (!(await sfApagada($))) await apagarAlEntrar($).catch(() => undefined)
  // Los avisos del panel cuentan desde el inicio de la sesión o el /clear; /reload-plugins sigue desde el último dado,
  // sin repetirlo ni perder lo cambiado antes de recargar, aunque cambie de plugin (tarea 285).
  await cargarAvisosPanel($, ahora, nueva).catch(() => undefined)
  return ahora
}

// Una conversación reanudada (--continue, --resume o /resume; el SessionStart con source «resume»): la duración, los
// prompts, las Cerradas y el aviso de lo cambiado desde el panel cuentan desde aquí, no desde que empezó la
// conversación, aunque el $.store de su sesión guarde un aviso de hace días (tarea 350). /reload-plugins no lo lanza.
// Con /resume, y según cómo arranque --resume, el mod sigue en la sesión reanudada con su $.state vacío y sin
// session.start, como tras un /clear: sin inicio ni estado leído, se carga entera, como sesión nueva; si no, el panel
// se queda en «Leyendo el estado…» hasta un /reload-plugins.
async function reanudar($: $): Promise<void> {
  if ((await read($, inicioSesion)) === 0 || (await read($, estado)) === null) {
    await cargar($, true)
    return
  }
  const ahora = await $.clock.now()
  await update($, inicioSesion, () => ahora)
  await update($, minuto, () => ahora)
  await update($, prompts, () => 0)
  // La relectura, aunque falle la carga de los avisos: sin ella, Cerradas seguiría contando desde antes.
  await cargarAvisosPanel($, ahora, true).catch(err => $.ui.log(`al reanudar, avisos: ${String(err)}`, { to: 'debug' }))
  await refrescar($)
}

// Las órdenes del mod que no pasan nada a Claude: tras ellas no hay turno ni sugerencia del motor (tarea 323).
// La orden fija del plugin, commands/panel.md: el motor la nombra con el plugin delante (tarea 337).
const ORDEN_FIJA = 'sf:panel'
const ORDENES_LOCALES = new Set(['sf', ORDEN_FIJA, 'sf_paso', 'sf_split', 'sf_fusionar', 'sf_prueba', 'sf_forzar_activa', 'sf_forzar_inactiva'])
// Las órdenes de la SF que no se atienden con la SF apagada en la sesión (decisión 193): /sf abre el panel, que lo dice.
// Tampoco /sf ni /sf:panel: sin la SF activa no hay panel (decisión 296).
const ORDENES_CON_SF = new Set(['sf', ORDEN_FIJA, 'sf_paso', 'sf_split', 'sf_fusionar', 'sf_redescribir', 'sf_config', 'sf_prueba'])

const ordenApagada = (orden: string) =>
  `/${orden}: la SF está apagada en esta sesión (la tiene otra sesión del proyecto, o se apagó con /sf_forzar_inactiva). Para traerla aquí, /sf_forzar_activa.`

// /sf abre el panel. La orden fija del plugin (commands/panel.md, decisiones 254 y 257) se llama /sf:panel: la app la lista antes
// del primer mensaje, cuando el mod aún no corre; con el mod en marcha, se atiende aquí igual que /sf y no sale en
// la lista, para que no se vea dos veces (tarea 337).
async function abrirPanel($: $) {
  await refrescar($)
  await update($, panelCerrado, () => false)
  // Un panel que ya está abierto se cierra y se abre de nuevo: así /sf repara uno que se ha quedado en blanco
  // (tarea 185).
  if ((await $.ui.panes()).some(p => p.id === PANEL)) await $.ui.close({ id: PANEL }).catch(() => undefined)
  await $.ui.open({ id: PANEL, title: 'Software Factory' })
  // Al abrir el panel, ACTUALIZAR vuelve a comprobar (tarea 229).
  await comprobarActualizacion($).catch(() => undefined)
  return { text: 'Panel de la SF abierto.' }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'sf',
      description: 'Panel de la Software Factory: tareas, propuestas y estado',
    })
    // El propietario añade un paso a la tarea en curso sin esperar a Claude, también a mitad de turno.
    await $.command.register({
      name: 'sf_paso',
      description: 'Añade un paso pendiente a la tarea en curso: /sf_paso texto',
      argumentHint: 'texto del paso',
      immediate: true,
    })
    // Separa pasos de una tarea en una tarea nueva, sin Claude, también a mitad de turno.
    await $.command.register({
      name: 'sf_split',
      description: 'Separa pasos de una tarea en una tarea nueva: /sf_split 89 2,3',
      argumentHint: '[tarea] [pasos]',
      immediate: true,
    })
    // Fusiona tareas en una, sin Claude, también a mitad de turno.
    await $.command.register({
      name: 'sf_fusionar',
      description: 'Fusiona tareas en una: /sf_fusionar 104 105',
      argumentHint: '[tareas]',
      immediate: true,
    })
    // Pide a Claude que vuelva a redactar la descripción de una tarea para que se lea fácilmente.
    await $.command.register({
      name: 'sf_redescribir',
      description: 'Claude vuelve a redactar la descripción de una tarea para que se lea fácilmente: /sf_redescribir 162',
      argumentHint: 'tarea',
      immediate: true,
    })
    // Pide a Claude cambiar la configuración del proyecto, con menús y su OK (tarea 299).
    await $.command.register({
      name: 'sf_config',
      description: 'Cambia la configuración del proyecto (.sf/proyecto.json) con Claude, con menús: /sf_config [qué]',
      argumentHint: '[qué cambiar]',
      immediate: true,
    })
    // Una sola sesión con la SF por proyecto (decisión 193): tomarla aquí o apagarla aquí.
    await $.command.register({
      name: 'sf_forzar_activa',
      description: 'Activa la SF en esta sesión y la apaga en la otra sesión del proyecto que la tenga',
      immediate: true,
    })
    await $.command.register({
      name: 'sf_forzar_inactiva',
      description: 'Apaga la SF en esta sesión, que deja de dar latido, para que otra la tome',
      immediate: true,
    })
    const r = await next(e)
    // Sin línea de estado: Claude Code la marca con «⚠ sf:» y repite lo que ya dice la caja sobre el prompt.
    // Se borra la que hubiera dejado una versión anterior.
    $.ui.status(undefined)
    // Al cargar el mod, una incorporación a medias queda en pausa, con Continuar y Abandonar: no se pierde (tarea 333).
    // Si se recarga porque la incorporación lo pidió (incorporacion.py recargar), sigue sola (tarea 366).
    await alCargarIncorporacion($).catch(() => undefined)
    const ahora = await cargar($)
    // /sf_prueba, solo en la SF con el catálogo local: cambia el modo prueba sin el panel (tarea 185).
    if ((await desdeCopia($)) || (await leerAjustes($))?.extraKnownMarketplaces?.[CATALOGO_PRUEBA]) {
      await $.command.register({
        name: 'sf_prueba',
        description: 'Modo prueba de la SF: cambia entre la copia de trabajo y el plugin publicado, sin el panel',
        immediate: true,
      })
    }
    // La duración de la sesión: un latido por minuto que redibuja el panel y relee los subagentes: cambia la ⚙ de uno
    // que entregó su informe o se paró sin que pase nada más.
    // ACTUALIZAR: si hay versión publicada nueva del plugin; al empezar, en un temporizador para no esperar a la red;
    // la publicada, cada 5 minutos con el latido (decisión del propietario, 2026-10-29; 5 y no 30, tarea 229), y lo
    // instalado frente a lo que corre, en cada latido, sin red (tarea 229, reabierta).
    // La última comprobación, en un atom para que el panel diga cuánto falta para la siguiente (tarea 238); la del
    // arranque cuenta desde el inicio, y las del latido, /sf y RELEASE la anotan en comprobarActualizacion.
    await update($, comprobadaEn, () => ahora)
    // Sin SF, la orden de incorporar como sugerencia del prompt (tarea 323).
    $.clock.after(500, () => void sugerirIncorporar($).catch(() => undefined))
    $.clock.after(1000, () => void comprobarActualizacion($, { anotar: false }).catch(() => undefined))
    // Si el reloj no avanza (un reloj simulado), el latido se para: sin esto, se repetiría sin fin. Un fallo en un
    // latido no lo para: el siguiente se programa siempre (tarea 229, reabierta).
    const latir = (antes: number) =>
      $.clock.after(60_000 - (antes % 60_000), () => {
        void (async () => {
          const t = await $.clock.now()
          if (t <= antes) return
          try {
            await update($, minuto, () => t)
            // El latido de la sesión con la SF (decisión 193); con ella apagada aquí, sin ACTUALIZAR ni REFRESCAR.
            const conSf = await latirSesion($).catch(() => true)
            // Si el estado sigue sin leer (se perdió con un /clear o falló la lectura), se lee ahora (tarea 239).
            if ((await read($, estado)) === null) await refrescar($).catch(() => undefined)
            await refrescarSubagentes($).catch(() => undefined)
            const red = t - ((await read($, comprobadaEn)) ?? ahora) >= CADA_COMPROBACION
            if (conSf) await comprobarActualizacion($, { red }).catch(() => undefined)
          } finally {
            latir(t)
          }
        })().catch(() => undefined)
      })
    latir(ahora)
    // Los avisos del panel se turnan con su cabecera (decisión 164).
    turnarAvisos($, ahora)
    return r
  })

  // Un /clear acaba la conversación sin cerrar el proceso: el motor no vuelve a lanzar session.start, y el estado del
  // panel puede quedar vacío («Leyendo el estado…»). El SessionStart de los ajustes sí llega, con source «clear»: ahí
  // se vuelve a cargar (tarea 239).
  // En los proyectos incorporados y en la propia SF, al empezar, tras /clear y tras compactar, las reglas de la SF y
  // sf:orquestacion como contexto (decisiones 187 y 298); con la SF apagada, nada (297). Si falla, la sesión sigue sin ellas.
  on('classic.SessionStart', async ($, e, next) => {
    const r = await next(e)
    if (e.source === 'clear') {
      await cargar($, true).catch(err => $.ui.log(`tras /clear: ${String(err)}`, { to: 'debug' }))
      await alCargarIncorporacion($).catch(() => undefined)
      // Sin SF, otra vez la sugerencia de incorporar (tarea 323).
      $.clock.after(500, () => void sugerirIncorporar($).catch(() => undefined))
    }
    // Tras compactar, Claude ya no tiene los avisos de subagentes dados: lo pendiente se vuelve a avisar (tarea 249).
    if (e.source === 'compact') await rearmarAvisosSubagentes($).catch(() => undefined)
    if (e.source === 'resume') await reanudar($).catch(err => $.ui.log(`al reanudar: ${String(err)}`, { to: 'debug' }))
    // Con la SF apagada en la sesión, sin contexto de la SF: Claude Code sin más (decisión 297).
    await asegurarSesion($).catch(() => null)
    const apagada = await sfApagada($)
    const textos = [
      apagada
        ? null
        : await contextoInicial($, e).catch(err => {
            $.ui.log(`reglas en SessionStart: ${String(err)}`, { to: 'debug' })
            return null
          }),
      // El intérprete de Python, en cualquier carpeta, si no es `python` (236), como en una carpeta sin SF.
      await contextoPython($, e).catch(() => null),
    ].filter((x): x is string => !!x)
    return textos.length ? { ...r, additionalContext: [...(r.additionalContext ?? []), ...textos] } : r
  }).catch(($, e, next) => next(e))

  // En los proyectos incorporados, no en la SF, la regla de lo que es de la SF y lo global, en el prompt de sistema (decisión 167).
  // Con la SF apagada en la sesión, sin ella (decisión 297).
  on('prompt.compose', async ($, e, next) => {
    const r = await next(e)
    return (await sfApagada($).catch(() => false)) ? r : anadirRegla($, r)
  }).catch(($, e, next) => next(e))

  // Al cerrar la sesión, en la SF, el modo prueba se desactiva: la siguiente entra con el plugin publicado.
  // Con la SF apagada, no: el modo prueba es de la sesión que la tiene. La que la tiene suelta su latido (decisión 193).
  on('session.end', async ($, e, next) => {
    if (!(await sfApagada($).catch(() => false))) await apagarAlCerrar($, String(e.reason)).catch(() => undefined)
    await soltarAlCerrar($).catch(() => undefined)
    return next(e)
  })

  // Un proyecto por sesión: las escrituras en otro proyecto se bloquean con el motivo.
  // Si el control falla, la escritura sigue: el control ayuda, la regla manda.
  // Con la SF apagada en la sesión, sin control: Claude Code sin más (decisión 297).
  on('tool.call', { tool: 'Write' }, async ($, e, next) => ((await sfApagada($).catch(() => false)) ? next(e) : escribir($, e.file_path, e, next))).catch(($, e, next) => next(e))
  on('tool.call', { tool: 'Edit' }, async ($, e, next) => ((await sfApagada($).catch(() => false)) ? next(e) : escribir($, e.file_path, e, next))).catch(($, e, next) => next(e))
  on('tool.call', { tool: 'NotebookEdit' }, async ($, e, next) =>
    (await sfApagada($).catch(() => false)) ? next(e) : escribir($, e.notebook_path, e, next),
  ).catch(($, e, next) => next(e))

  // La cola cambia a mitad de turno (Claude marca una petición en curso y trabaja en ella): tras cada herramienta
  // que puede escribir, se relee sin esperar, para que el panel muestre al momento la tarea en curso.
  // También tras el Agent: el de un subagente en primer plano acaba con él, y su ⚙ se va al momento.
  for (const tool of ['Bash', 'PowerShell', 'Write', 'Edit', 'Agent'] as const) {
    on('tool.call', { tool }, async ($, e, next) => {
      const r = await next(e)
      void refrescar($).catch(() => undefined)
      return r
    }).catch(($, e, next) => next(e))
  }

  // Al volver un Agent del principal (un subagente en primer plano acaba con él; uno en segundo plano, recién lanzado),
  // los avisos de subagentes nuevos, tras su resultado (tarea 249).
  on('tool.call', { tool: 'Agent' }, async ($, e, next) => {
    const r = await next(e)
    if (e.agentId || r.deny !== undefined) return r
    // Con la SF apagada en la sesión, sin avisos de subagentes: son de la sesión que la tiene (decisión 193).
    if (await sfApagada($).catch(() => false)) return r
    const { lanzar, recoger } = await leerAvisoSubagentes($).catch(() => SIN_AVISO)
    const aviso = [lanzar, recoger].filter((x): x is string => !!x)
    return aviso.length ? { ...r, context: [...(r.context ?? []), ...aviso] } : r
  }).catch(($, e, next) => next(e))

  // La respuesta al menú de incorporar (decisión 246): «No, y no vuelvas a preguntar en esta carpeta» se guarda por carpeta.
  on('tool.call', { tool: 'AskUserQuestion' }, async ($, e, next) => {
    const r = await next(e)
    if (e.agentId || r.deny !== undefined) return r
    const respuestas = r.isError === true ? undefined : (r.result as { answers?: unknown } | undefined)?.answers
    if (respuestas !== undefined) await anotarRespuestaIncorporar($, respuestas).catch(() => undefined)
    // Con un no a incorporar, se borra el progreso que hubiera (tarea 333, decisión 258).
    if (respuestas !== undefined) await menuEnIncorporacion($, respuestas).catch(() => undefined)
    return r
  }).catch(($, e, next) => next(e))

  // Un subagente parado con TaskStop: su ⚙ se va al momento, aunque el motor ya no lo liste (tarea 225). Si TaskStop
  // falla (ya había entregado su informe y no hay nada que parar), sigue esperando instrucciones.
  on('tool.call', { tool: 'TaskStop' }, async ($, e, next) => {
    const r = await next(e)
    const id = e.task_id ?? e.shell_id
    if (id && r.deny === undefined && r.isError !== true) await marcarSubagente($, id, 'parado').catch(() => undefined)
    await refrescarSubagentes($).catch(() => undefined)
    return r
  }).catch(($, e, next) => next(e))

  // Un subagente que empieza: su ⚙, al momento (decisión del propietario, 2026-10-29).
  on('agent.spawn', async ($, e, next) => {
    const r = await next(e)
    void refrescar($).catch(() => undefined)
    return r
  }).catch(($, e, next) => next(e))

  // El turno de Claude en curso: el /reload-plugins del modo prueba espera a que acabe (tarea 185).
  on('turn.start', async ($, e, next) => {
    if (e.agentId === undefined) {
      marcarTurno(e.turnId)
      // Con un turno en marcha, la incorporación no está en pausa, aunque espere la respuesta de un menú (tarea 366).
      if (await reanudarIncorporacion($).catch(() => false)) void refrescar($).catch(() => undefined)
      // Una incorporación terminada, con el panel operativo ya pintado, se quita al empezar el turno siguiente (tarea 333).
      const est = await read($, estado)
      if (est && (await cerrarIncorporacionTerminada($, est.tipo !== 'sin-sf').catch(() => false))) await refrescar($).catch(() => undefined)
    }
    return next(e)
  }).catch(($, e, next) => next(e))

  // Y al acabar cada turno.
  on('turn.complete', async ($, e, next) => {
    if (e.agentId === undefined) {
      marcarTurno(null)
      // Una incorporación a medias queda en pausa al acabar o interrumpirse el turno (tarea 333, decisión 258); si pidió
      // recargar los plugins, el mod los recarga y no la pausa: sigue sola tras recargar (tarea 366).
      if (!(await recargarSiPedido($, () => void refrescar($).catch(() => undefined)).catch(() => false))) await pausarIncorporacion($).catch(() => undefined)
    }
    await refrescar($)
    return next(e)
  })

  // Cuenta los prompts enviados (no los que el motor añade sin que se vean).
  // Y a cada mensaje del propietario le añade, como contexto para Claude, lo que él ha cambiado en la cola desde el
  // panel desde el último mensaje que lo llevó (tarea 228). Por segundos enteros, como las fechas de cola.py: un cambio
  // del mismo segundo que el mensaje va en el siguiente.
  // También le añade los avisos de subagentes nuevos (tarea 249), y a la notificación de un subagente que vuelve.
  on('prompt.submit', async ($, e, next) => {
    if (!e.isMeta) await update($, prompts, n => n + 1).catch(() => undefined)
    if (e.command) return next(e)
    const delPropietario = !e.isMeta && DEL_PROPIETARIO.has(e.origin.kind)
    if (!delPropietario && e.origin.kind !== 'task-notification') return next(e)
    // Una sola sesión con la SF por proyecto (decisión 193): que se ha apagado o activado aquí, una vez; con ella
    // apagada, ningún otro aviso de la SF.
    const avisoSesion = delPropietario ? await tomarAvisoSesion($).catch(() => null) : null
    if (await sfApagada($).catch(() => false)) return next(avisoSesion ? { ...e, context: [...(e.context ?? []), avisoSesion] } : e)
    // La carpeta se acaba de incorporar en esta conversación: las reglas y la orquestación, una vez (decisión 242). Sin
    // SF, el encargo de ofrecer la incorporación, una vez por conversación (decisión 243).
    const reglas = delPropietario ? await reglasAlIncorporar($).catch(() => null) : null
    const incorporar = delPropietario ? await ofrecerIncorporar($).catch(() => null) : null
    const tomado = delPropietario ? await tomarAvisoPanel($).catch(() => null) : null
    const panel = tomado?.aviso ?? null
    // Sin pantalla completa, la oferta de activarla, una vez por conversación (tarea 264).
    const pantalla = delPropietario ? await ofrecerPantalla($).catch(() => null) : null
    // El de lanzar los subagentes que faltan, el primero: es lo primero del turno (tarea 351).
    const { lanzar, recoger } = await leerAvisoSubagentes($).catch(() => SIN_AVISO)
    const avisos = [avisoSesion, lanzar, reglas, incorporar, panel, pantalla, recoger].filter((x): x is string => !!x)
    if (!avisos.length) return next(e)
    // Si el mensaje no llega a entrar (otro hook lo descarta), el aviso del panel queda pendiente para el siguiente.
    const r = await next({ ...e, context: [...(e.context ?? []), ...avisos] }).catch(async (err: unknown) => {
      await tomado?.devolver()
      throw err
    })
    if ('drop' in r) await tomado?.devolver()
    return r
  })


  // Tras una orden local del mod (no un turno de Claude, que deja su propia sugerencia), sin SF, vuelve la sugerencia de
  // incorporar: el prompt la pierde al escribir la orden (tarea 323). Va antes que las de cada orden, que contestan sin
  // next: así las envuelve.
  // Con la SF apagada en la sesión, sus órdenes no se atienden: lo dicen (decisión 193).
  on('command.run', async ($, e, next) => {
    if (ORDENES_CON_SF.has(e.command) && (await sfApagada($).catch(() => false))) return { text: ordenApagada(e.command) }
    const r = await next(e)
    if (ORDENES_LOCALES.has(e.command)) $.clock.after(300, () => void sugerirIncorporar($).catch(() => undefined))
    return r
  })

  // /sf_forzar_activa y /sf_forzar_inactiva (decisiones 193 y 198). Al activarla, el panel se relee y comprueba
  // ACTUALIZAR y REFRESCAR, que con ella apagada no se miraban.
  on('command.run', { command: 'sf_forzar_activa' }, async $ => {
    const antes = await sesionSfActual($)
    const text = await forzarActiva($)
    await refrescar($).catch(() => undefined)
    // Apagada no había panel (decisión 296): al traerla, se abre.
    if (antes === 'apagada' || antes === 'inactiva') {
      await update($, panelCerrado, () => false)
      await $.ui.open({ id: PANEL, title: 'Software Factory' }).catch(() => undefined)
      $.clock.after(0, () => void comprobarActualizacion($, { anotar: false }).catch(() => undefined))
    }
    return { text }
  })
  on('command.run', { command: 'sf_forzar_inactiva' }, async $ => {
    const text = await forzarInactiva($)
    await refrescar($).catch(() => undefined)
    return { text }
  })

  // /sf_paso texto: lo escribe en una tarea en curso de .sf/peticiones.json, como pendiente (decisión del
  // propietario, 2026-10-28). Con una sola en curso, va a esa; con varias, pregunta a cuál, salvo que el texto
  // empiece por su número («/sf_paso 64 texto»). El resto del archivo queda como estaba.
  on('command.run', { command: 'sf_paso' }, async ($, e) => {
    const args = e.args.trim()
    if (!args) return { text: 'Uso: /sf_paso texto del paso (o /sf_paso 64 texto, para la 64)' }
    const est = await read($, estado)
    const enCurso = est ? enCursoRecientes(est) : []
    if (enCurso.length === 0) return { text: 'No hay ninguna tarea en curso: díselo a Claude en el chat.' }
    const m = /^(\d+)\s+(.+)$/s.exec(args)
    const elegida = m ? enCurso.find(p => p.id === Number(m[1])) : undefined
    if (elegida) return { text: await escribirPaso($, elegida.id, m![2]!.trim()) }
    if (enCurso.length === 1) return { text: await escribirPaso($, enCurso[0]!.id, args) }
    // Varias en curso: se pregunta en el diálogo de Claude Code, desde un temporizador (el motor no deja
    // preguntar desde este hook, que retiene el turno).
    const opciones = enCurso.slice(0, 4).map(p => `${p.id} ${p.texto}`.slice(0, 60))
    $.clock.after(50, () => {
      void $.ui
        .ask(`¿A qué tarea va el paso «${args}»?`, { header: '/sf_paso', options: opciones.length > 1 ? opciones : [...opciones, 'Cancelar'] })
        .then(r => {
          const id = Number(/^\s*(\d+)/.exec(r)?.[1])
          if (!enCurso.some(p => p.id === id)) return
          return escribirPaso($, id, args).then(t => emergente($, t))
        })
        .catch(() => undefined)
    })
    return { text: `Varias tareas en curso (${enCurso.map(p => p.id).join(', ')}): elige a cuál va el paso.` }
  })

  // /sf_redescribir N: Claude vuelve a redactar la descripción de la N (decisión del propietario, 2026-10-30).
  on('command.run', { command: 'sf_redescribir' }, async ($, e) => {
    const est = await read($, estado)
    return { text: pedirRedescripcion($, est?.peticiones ?? [], e.args) }
  })

  // /sf_config [qué] (tarea 299): Claude cambia la configuración del proyecto con sf:configurar_proyecto.
  on('command.run', { command: 'sf_config' }, async ($, e) => ({ text: await pedirConfiguracion($, e.args) }))

  // /sf_split (decisión del propietario, 2026-10-29): separa pasos de una tarea en curso o en cola en una tarea nueva.
  // El mod lo pide a cola.py, sin Claude. «/sf_split 89 2,3» separa sin preguntar; «/sf_split 89» pregunta los
  // pasos; «/sf_split» a secas, antes, la tarea, entre las que tienen dos pasos o más.
  on('command.run', { command: 'sf_split' }, async ($, e) => {
    const args = e.args.trim()
    const m = /^(\d+)(?:\s+([\d\s,]+))?$/.exec(args)
    if (args && !m) return { text: USO_SPLIT }
    const est = await read($, estado)
    const peticiones = est?.peticiones ?? []
    if (m) {
      const id = Number(m[1])
      const p = peticiones.find(x => x.id === id)
      const nums = m[2] !== undefined ? numerosDe(m[2]) : undefined
      const motivo = motivoSplit(p, id, nums)
      if (motivo) return { text: motivo }
      return { text: nums ? await pedirSplit($, p!, nums) : elegir($, p!) }
    }
    const tareas = peticiones.filter(separable).sort((a, b) => b.id - a.id)
    if (tareas.length === 0) return { text: `Ninguna tarea en curso o en cola tiene pasos que separar. ${USO_SPLIT}` }
    if (tareas.length === 1) return { text: elegir($, tareas[0]!) }
    // Varias: se pregunta cuál, desde un temporizador (el motor no deja preguntar desde este hook). Caben cuatro, las
    // más recientes; otra se escribe por su número en «Other».
    $.clock.after(50, () => {
      void $.ui
        .ask('¿De qué tarea separas pasos?', { header: '/sf_split', options: tareas.slice(0, 4).map(p => etiqueta(p.id, p.texto)) })
        .then(r => {
          const id = Number(/^\s*(\d+)/.exec(r)?.[1])
          const p = tareas.find(x => x.id === id)
          if (!p) return emergenteError($, Number.isNaN(id) ? USO_SPLIT : (motivoSplit(peticiones.find(x => x.id === id), id) ?? USO_SPLIT))
          const t = elegirPasos($, p)
          if (t) emergente($, t, false)
        })
        .catch(() => undefined)
    })
    return { text: `Elige de qué tarea separas pasos (${tareas.map(p => p.id).join(', ')}).` }
  })

  // /sf_fusionar (decisión del propietario, 2026-10-29): junta en una tareas en cola o en curso; queda la de número más
  // alto. El mod lo pide a cola.py, sin Claude. «/sf_fusionar 104 105» fusiona sin preguntar; «/sf_fusionar» a
  // secas pregunta cuáles, con varias a la vez, entre las cuatro más recientes.
  on('command.run', { command: 'sf_fusionar' }, async ($, e) => {
    const args = e.args.trim()
    if (args && !/^[\d\s,]+$/.test(args)) return { text: USO_FUSIONAR }
    const est = await read($, estado)
    const peticiones = est?.peticiones ?? []
    const fusionar = async (ids: number[]) =>
      motivoFusion(peticiones, ids) ?? (await pedirFusion($, peticiones.filter(p => ids.includes(p.id))))
    if (args) return { text: await fusionar(numerosDe(args)) }
    const tareas = peticiones.filter(fusionable).sort((a, b) => b.id - a.id).slice(0, 4)
    if (tareas.length < 2) return { text: `No hay dos tareas en cola o en curso que fusionar. ${USO_FUSIONAR}` }
    // Desde un temporizador: el motor no deja preguntar desde este hook. Otra se escribe por su número en «Other».
    $.clock.after(50, () => {
      void $.ui
        .ask('¿Qué tareas fusionas en una?', {
          header: '/sf_fusionar',
          options: tareas.map(p => etiqueta(p.id, p.texto)),
          multiSelect: true,
        })
        .then(async r => {
          const ids = numerosDe(r)
          if (new Set(ids).size < 2) emergenteError($, 'Elige dos tareas o más: no se ha fusionado nada.')
          else emergente($, await fusionar(ids))
        })
        .catch(() => undefined)
    })
    return { text: `Elige qué tareas fusionas (${tareas.map(p => p.id).join(', ')}).` }
  })

  // /sf_prueba (tarea 185): la otra forma de cambiar el modo prueba, por si el panel no se ve o queda en blanco.
  on('command.run', { command: 'sf_prueba' }, async $ => {
    const copia = await desdeCopia($)
    if (!copia && !(await leerAjustes($))?.extraKnownMarketplaces?.[CATALOGO_PRUEBA])
      return { text: 'El modo prueba solo está en la SF, con el catálogo local softwarefactory-dev registrado.' }
    return { text: await cambiarPrueba($, !copia, 'la orden /sf_prueba', true) }
  })

  on('command.run', { command: 'sf' }, async $ => abrirPanel($))
  on('command.run', { command: 'sf:panel' }, async $ => abrirPanel($))
  on('command.describe', { command: 'sf:panel' }, async ($, e, next) => ({ ...(await next(e)), isHidden: true }))

  registrarPanel(on)
}
