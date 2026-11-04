import { expect, mock, test } from 'claude-code/testing'
import { ANCHO_ETIQUETA, FONDO_ORDEN, MARCA_AVISO_EMERGENTE, MARCA_ERROR_EMERGENTE, anchoComun, centrar, puntosDe } from '../hooks/estilo'
import { abreviarRutas, duracionEmergente, pareceError, textoEmergente } from '../hooks/emergentes'
import { avisoComprobacion, avisoDependencias, proximaComprobacion, subirManifiesto } from '../hooks/cola'
import { claveIncorporacion, tareasEnDevelop } from '../hooks/lectura'
import { PRUEBA_PYTHON } from '../hooks/python'
import { NOMBRE, NOMBRE_ANCHO, bienvenida, partir } from '../hooks/bienvenida'
import { BARRA, COLOR_BARRA, COLOR_LETRAS, LETRAS, logoSvg } from '../hooks/logo'

// Un repositorio de la SF de mentira: la marca del plugin, documentos y una cola de peticiones.
// Cada caso parte de su propia copia, para que un fallo señale un solo comportamiento.
const RAIZ = '/sf'
const AHORA = Date.parse('2026-10-27T12:00:00Z')
const COLA = '/sf/.sf/peticiones.json'
// Las tareas que han salido de la cola, con su historial: las escribe cola.py.
const HISTORIAL_JSONL = '/sf/.sf/historial.jsonl'
// El cola.py del plugin cargado y la copia que el panel hace de él al cargar (decisión 136).
const CLI_PLUGIN = '/plugin/tools/cola.py'
const COPIA_COLA = '/home/.claude/sf/cola-sesion-1.py'
// El lanzador de Claude (tarea 252), en el plugin y donde lo copia el panel: Claude lanza siempre ese.
const LANZADOR_PLUGIN = '/plugin/tools/cola_sesion.py'
const LANZADOR = '/home/.claude/sf/cola.py'
const AJUSTES = '/sf/.claude/settings.local.json'

type Pet = Record<string, unknown>
// La respuesta de cola.py --json.
type Respuesta = { ok: boolean; mensaje: string; id?: number; fallo?: string; motivo?: string }
const LARGA = 'Un proyecto por sesión: bloqueo en el mod de la SF'

// Un evento del historial de una tarea, como lo escribe cola.py: por omisión, de la sesión (AHORA, cuando empieza);
// con `segundos`, tantos después; con ANTES, de otra sesión.
const ANTES = -86400
const ev = (evento: string, detalle?: string, segundos = 0) => ({
  evento,
  fecha: new Date(AHORA + 1000 * segundos).toISOString(),
  quien: 'propietario',
  via: 'panel',
  ...(detalle ? { detalle } : {}),
})

// Al abrir la sesión: dos en curso (1 y 4) y dos en observación (2 y 3).
const INICIAL: Pet[] = [
  { id: 1, texto: 'Panel lateral', estado: 'en-curso' },
  { id: 4, texto: 'Fondos por bloque', estado: 'en-curso' },
  { id: 2, texto: 'Secciones plegables', estado: 'en-observacion', prueba: 'pulsar la cabecera' },
  { id: 3, texto: LARGA, estado: 'en-observacion', commit: 'sf 0.8.0' },
]

// Se cierran las dos en curso: la 1 con commit (pasa a observación) y la 4 sin commit (sale de la cola: CERRADA_4).
const CERRADAS: Pet[] = [
  { id: 1, texto: 'Panel lateral', estado: 'en-observacion', commit: 'sf 1.0', prueba: 'mirar', historial: [ev('a-observacion', 'sf 1.0')] },
  // Comprobada por Claude: sigue en observación, con «✓».
  { id: 2, texto: 'Secciones plegables', estado: 'en-observacion', prueba: 'pulsar la cabecera', comprobado: 'prueba del panel' },
  { id: 3, texto: LARGA, estado: 'en-observacion', commit: 'sf 0.8.0', observando: true },
  // Añadida y cerrada entre dos lecturas: también cuenta como cerrada.
  { id: 5, texto: 'Cerrada sin verla en curso', estado: 'en-observacion', commit: 'sf 1.1', historial: [ev('creada', 'en-cola'), ev('a-observacion', 'sf 1.1')] },
]
// La 4, cerrada sin rama en la sesión: ya en .sf/historial.jsonl.
const CERRADA_4: Pet = { id: 4, texto: 'Fondos por bloque', estado: 'cerrada', historial: [ev('cerrada', 'sin rama')] }

// La 2 cerrada (sale de la cola) y la 4 reabierta, con pasos.
const REABIERTA: Pet[] = [
  { id: 1, texto: 'Panel lateral', estado: 'en-observacion', commit: 'sf 1.0', prueba: 'mirar' },
  { id: 3, texto: LARGA, estado: 'en-observacion', commit: 'sf 0.8.0' },
  {
    id: 4,
    texto: 'Fondos por bloque',
    estado: 'en-curso',
    pasos: [
      { texto: 'Elegir el gris', estado: 'hecho' },
      { texto: 'Aplicarlo a los bloques', estado: 'en-curso' },
      { texto: 'Probarlo', estado: 'pendiente' },
    ],
  },
  { id: 5, texto: 'Cerrada sin verla en curso', estado: 'en-observacion', commit: 'sf 1.1' },
]

// En Windows, el motor completa /sf con la unidad y usa barras invertidas. Los ajustes locales y la marca del
// modo prueba se leen con ruta relativa, que en la prueba cae en la carpeta del plugin: se llevan a /sf.
// El manifiesto del plugin que se ejecuta (el de la copia de trabajo) se lleva a /plugin.
const ruta = (p: string) =>
  p
    .replace(/\\/g, '/')
    .replace(/^[a-zA-Z]:/, '')
    // Los del usuario (/home/.claude/settings.json) se quedan en /home.
    .replace(/^(?!\/home\/).*\/(\.claude\/settings|\.sf\/prueba)/, '/sf/$1')
    .replace(/^(?!\/sf\/).*\/plugins\/sf\/\.claude-plugin\/plugin\.json$/, '/plugin/plugin.json')
    // El cola.py del plugin que se ejecuta, como su manifiesto: en /plugin.
    .replace(/^(?!\/sf\/).*\/plugins\/sf\/tools\/cola\.py$/, CLI_PLUGIN)
    // La plantilla de las reglas y las skills del plugin que se ejecuta: en /plugin.
    .replace(/^(?!\/sf\/).*\/plugins\/sf\/(templates|skills)\//, '/plugin/$1/')
    // El cola.py del plugin que se ejecuta, como su manifiesto: en /plugin.
    .replace(/^(?!\/sf\/).*\/plugins\/sf\/tools\/cola\.py$/, '/plugin/tools/cola.py')
    // El lanzador de Claude (tarea 252), igual.
    .replace(/^(?!\/sf\/).*\/plugins\/sf\/tools\/cola_sesion\.py$/, '/plugin/tools/cola_sesion.py')

const PANEL = {
  plugin: 'sf',
  component: 'Pane',
  requestId: 'sf-estado',
  props: {
    title: 'Software Factory',
    isFocused: false,
    bodyColumns: 38,
    placement: 'dock',
    scroll: { offset: 0, bodyRows: 40 },
    view: {},
  },
} as const

type Motor = Parameters<Parameters<typeof test>[1]>
// sinMarca: un proyecto consumidor, no el repositorio de la SF.
// reloj: un reloj en memoria que solo avanza cuando el caso lo mueve (sin él, cada espera se cumple al momento).
// git: lo que responden status y worktree list, y si fallan el switch (Activar rama), el merge o el push (la C).
// log: lo que responde git log develop (la R); revertFalla: choques en el revert.
// tags: lo que responde git tag --list (RELEASE); noAncestro: main no es antecesor de develop.
// remoto: lo que responde git ls-remote --tags (ACTUALIZAR; null, falla); updateFalla: los scopes en que falla
// claude plugin update; catalogoFalla: falla claude plugin marketplace update; alDia: los scopes en que claude plugin
// update responde que ya está en la última versión, sin tocar el registro; installFalla: los plugins que
// claude plugin install no puede instalar. revision: lo que responde tools/revision_publica.py (RELEASE, decisiones 252 y 259;
// sin él, seguir; null, no responde).
type Git = { status?: string; worktrees?: string; switchFalla?: boolean; mergeFalla?: boolean; pushFalla?: boolean; log?: string; revertFalla?: boolean; tags?: string; noAncestro?: boolean; remoto?: string | null; updateFalla?: string[]; catalogoFalla?: boolean; alDia?: string[]; installFalla?: string[]; html?: string[]; sinAbridor?: string[]; propuestasDevelop?: string; rutaDevelop?: string; revision?: object | null }
// paneles: lo que responde $.ui.panes() en cada llamada (sin él, ningún panel abierto).
// agentes: lo que responde $.agent.list(), que el caso puede cambiar (sin él, la llamada falla).
type Agente = { description: string; status: string }
// raiz: la carpeta de la sesión (sin ella, /sf).
// salidas: las tareas que ya salieron de la cola (.sf/historial.jsonl); respuestas: lo que responde cola.py a una
// orden (por su nombre: «cerrar», «paso quitar»), sin cambiar nada. sinCola: el plugin sin tools/cola.py, que no se
// puede copiar. copia: el plugin que corre es la copia de trabajo de la SF, dentro de su repositorio (existe el .git
// de la carpeta dos niveles por encima de la del plugin, fuera de /sf). sinDecisiones: el proyecto sin docs/decisiones/.
// sinGenerador: indice_decisiones.py --html falla, como sin el paquete markdown. desplegadas: las tareas, desplegadas.
type Opciones = { sinDecisiones?: boolean; sinGenerador?: boolean; cola?: Pet[]; extra?: Record<string, string>; sinMarca?: boolean; reloj?: boolean; git?: Git; paneles?: () => unknown[]; agentes?: Agente[]; raiz?: string; salidas?: Pet[]; respuestas?: Record<string, Respuesta>; sinCola?: boolean; copia?: boolean; sinArranque?: boolean; desplegadas?: boolean; entorno?: Record<string, string>; ajustes?: Record<string, unknown>; contextoMotor?: string[]; plegado?: Record<string, boolean>; pythons?: Record<string, string | null> }

// Motor simulado: archivos, almacén, comandos y reloj. Devuelve lo que el caso quiere mirar.
async function preparar([$, on]: Motor, { sinDecisiones = false, sinGenerador = false, cola = INICIAL, extra = {}, sinMarca = false, reloj = false, git = {}, paneles = () => [], agentes, raiz = RAIZ, salidas = [], respuestas = {}, sinCola = false, copia = false, sinArranque = false, desplegadas = false, entorno = {}, ajustes = {}, contextoMotor, plegado, pythons = { python: '3 13' } }: Opciones = {}) {
  const archivos: Record<string, string> = {
    ...(sinMarca ? {} : { '/sf/plugins/sf/.claude-plugin/plugin.json': '{}' }),
    '/plugin/plugin.json': JSON.stringify({ name: 'sf', version: '0.32.3' }),
    // El cola.py del plugin: el panel lo copia al cargar y lanza la copia (decisión 136).
    ...(sinCola ? {} : { [CLI_PLUGIN]: '# cola.py v1', [LANZADOR_PLUGIN]: '# lanzador v1' }),
    '/sf/docs/specs/vision': '',
    ...(sinDecisiones ? {} : { '/sf/docs/decisiones': '' }),
    [COLA]: JSON.stringify({ peticiones: cola }),
    ...(salidas.length ? { [HISTORIAL_JSONL]: salidas.map(x => JSON.stringify(x) + '\n').join('') } : {}),
    ...extra,
  }
  // desplegadas: las tareas de la cola y las cerradas empiezan desplegadas, con su menú de órdenes a la vista
  // (decisión 168), como si el propietario ya las hubiera abierto.
  const guardado: Record<string, unknown> = desplegadas
    ? { plegado: Object.fromEntries([...cola, ...salidas].flatMap(t => ['pet:cola', 'pet:observacion', 'arriba', 'hecho'].map(k => [`${k}:${t.id}`, false]))) }
    : plegado ? { plegado } : {}
  const comandos: string[] = []
  const prompts: string[] = []
  // Lo que cada prompt lleva como contexto para Claude, en su orden (undefined: nada).
  const contextos: (readonly string[] | undefined)[] = []
  const ordenes: string[] = []
  // Las órdenes de cola.py, sin las opciones comunes: «descartar 12».
  const colas: string[] = []
  // Las líneas de órdenes completas de cola.py, para mirar las opciones comunes.
  const lineasCola: string[][] = []
  // Lo que recibe git por stdin (el mensaje del commit de la C).
  const entradas: string[] = []
  // Los avisos emergentes sin su marca de aviso o de error (tarea 257), para comparar el texto; enteros, en marcados.
  const toasts: string[] = []
  const marcados: { text: string; timeoutMs?: number }[] = []
  // Lo que el mod deja en el prompt con $.prompt.fill (Paso +).
  const rellenos: string[] = []
  // La carpeta desde la que se lanza cada claude plugin update.
  const cwds: string[] = []
  on('session.root', () => ({ value: raiz }))
  on('session.cwd', () => ({ value: raiz }))
  on('session.id', () => ({ value: 'sesion-1' }))
  // entorno y ajustes: las variables y los ajustes efectivos que lee el mod (tarea 264); el caso puede cambiarlos.
  on('env.get', (_, e) => ({ value: e.name === 'USERPROFILE' ? '/home' : entorno[e.name] }))
  on('settings.read', () => ({ value: { ...ajustes } }) as never)
  on('fs.exists', (_, e) => ({ value: ruta(e.path) in archivos || (copia && !ruta(e.path).startsWith('/sf') && ruta(e.path).endsWith('/.git')) }))
  on('fs.read', (_, e) => ({ value: archivos[ruta(e.path)] ?? '' }))
  on('fs.write', (_, e) => {
    archivos[ruta(e.path)] = e.text
    return { value: undefined }
  })
  on('fs.list', (_, e) => ({
    value: (
      ruta(e.path) === '/sf/docs/specs/vision'
        ? ['a.md', 'b.md', 'b.html', 'fundacional-a.md']
        : ruta(e.path) === '/sf/docs/decisiones'
          ? ['README.md', '2026-10-29-a.md', '2026-10-28-b.md']
          : // Los worktrees de .git/worktrees: las carpetas que tengan archivos en el caso.
            ruta(e.path).endsWith('/worktrees')
            ? [...new Set(Object.keys(archivos).filter(k => k.startsWith(`${ruta(e.path)}/`)).map(k => k.slice(ruta(e.path).length + 1).split('/')[0]!))]
            : []
    ).map(name => ({ name, kind: 'file', size: 1, isLink: false })),
  }))
  on('store.get', (_, e) => ({ value: guardado[e.key] }))
  on('store.set', (_, e) => {
    guardado[e.key] = e.value
    return { value: undefined }
  })
  on('command.register', () => ({ value: { command: 'sf' } }))
  on('command.run', (_, e) => {
    comandos.push(e.command)
    return { text: '' }
  })
  on('ui.open', () => ({ value: { isPlaced: true } }))
  // Los paneles que cierra el mod ($.ui.close), por su id.
  const cierres: string[] = []
  on('ui.close', (_, e) => {
    cierres.push(e.id)
    return { value: undefined }
  })
  on('turn.start', (_, e) => ({ turnId: e.turnId }))
  on('turn.complete', (_, e) => ({ text: e.answer }))
  on('prompt.submit', (_, e) => {
    prompts.push(e.text)
    contextos.push(e.context)
    return { text: e.text }
  })
  on('prompt.fill', (_, e) => {
    rellenos.push(e.text)
    return { isFilled: true }
  })
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  // El prompt de sistema del motor: una sección, para ver qué añade el mod.
  on('prompt.compose', () => ({ sections: [{ id: 'intro', text: 'motor', scope: 'shared' }] }))
  // Sin hooks SessionStart en los ajustes: nada que decir; con contextoMotor, lo que dirían.
  on('classic.SessionStart', () => (contextoMotor ? { additionalContext: contextoMotor } : {}))
  on('ui.status', () => ({ value: undefined }))
  on('ui.log', () => ({ value: undefined }))
  on('ui.toast', (_, e) => {
    toasts.push(e.text.replace(/^(?:🟦|🟥) /u, ''))
    marcados.push({ text: e.text, timeoutMs: e.timeoutMs })
    return { value: undefined }
  })
  on('ui.panes', () => ({ value: paneles() as never }))
  if (agentes) on('agent.list', () => ({ value: agentes.map((a, i) => ({ id: `a${String(i)}`, type: 'general-purpose', ...a })) as never }))
  // Lo que dibuja el motor en la banda sobre el prompt cuando el mod no pinta la caja.
  on('ui.render', { component: 'AbovePrompt' }, ($, e) => {
    const { Text } = $.ui.resolve(e)
    return <Text>motor</Text>
  })
  const relojEnMemoria = reloj ? mock.clock(on, { now: AHORA }) : null
  if (!relojEnMemoria) {
    on('clock.now', () => ({ value: AHORA }))
    on('clock.after', () => ({ value: undefined }))
  }
  on('tool.call', { tool: 'Bash' }, () => ({ result: 'ok' }))
  on('tool.call', { tool: 'Write' }, () => ({ result: 'ok' }))
  // git log: un commit corto y otro largo, de hace 5 min y 3 h. status, worktree y switch, para Activar rama.
  const salida = (stdout: string, exitCode = 0, stderr = '') => ({ value: { exitCode, stdout, stderr, isStdoutTruncated: false, isStderrTruncated: false } })
  // La rama activa y las que existen salen de los archivos de .git, como los lee el panel.
  const GIT_ORDENES = ['status', 'worktree', 'switch', 'symbolic-ref', 'show-ref', 'branch', 'merge', 'reset', 'commit', 'rev-parse', 'push', 'revert', 'diff', 'tag', 'merge-base', 'fetch', 'add', 'show']
  // La historia de develop: la lee el panel en cada relectura, si develop ha cambiado; no se apunta en `ordenes`.
  let logDevelop = git.log ?? ''
  // cola.py de mentira (tarea 145): el panel escribe la cola solo con él. Hace lo que hace el de verdad con la cola,
  // el historial y .sf/historial.jsonl, sin git: lo de git lo prueban las pruebas de Python (test_cola.py). Cada
  // orden se apunta en `colas` («descartar 12»); `respuestas` fija la de una orden (por su nombre), sin cambiar nada.
  // Las fechas avanzan un segundo por orden, desde AHORA: son de la sesión.
  let reloj145 = 0
  const colaFalsa = (args: string[]): Respuesta => {
    const orden = args[0] === 'paso' ? `paso ${args[1]!}` : args[0]!
    colas.push(args.join(' '))
    if (respuestas[orden]) return respuestas[orden]!
    const datos = JSON.parse(archivos[COLA] ?? '{"peticiones":[]}') as { ultimo?: number; peticiones: Pet[] }
    const lista = datos.peticiones
    const fuera = (archivos[HISTORIAL_JSONL] ?? '').split('\n').filter(Boolean).map(l => JSON.parse(l) as Pet)
    const fecha = new Date(AHORA + 1000 * ++reloj145).toISOString()
    const anotar = (t: Pet, evento: string, detalle?: string) => {
      t.historial = [...((t.historial as Pet[] | undefined) ?? []), { evento, fecha, quien: 'propietario', via: 'panel', ...(detalle ? { detalle } : {}) }]
    }
    const archivar = (t: Pet, estado: string) => {
      t.estado = estado
      archivos[HISTORIAL_JSONL] = (archivos[HISTORIAL_JSONL] ?? '') + JSON.stringify(t) + '\n'
    }
    const sacar = (t: Pet, estado: string) => {
      datos.peticiones = datos.peticiones.filter(x => x !== t)
      archivar(t, estado)
    }
    const siguiente = () => Math.max(datos.ultimo ?? 0, ...lista.map(x => x.id as number), ...fuera.map(x => x.id as number)) + 1
    const guardar = () => {
      archivos[COLA] = JSON.stringify(datos)
    }
    const n = Number(args[orden.startsWith('paso') ? 2 : 1])
    const t = lista.find(x => x.id === n)
    const no = (mensaje: string): Respuesta => ({ ok: false, mensaje })
    const pasos = (x: Pet) => (x.pasos as Pet[] | undefined) ?? []
    switch (orden) {
      case 'crear': {
        const id = siguiente()
        const nueva: Pet = { id, texto: args[1], estado: 'en-cola' }
        const d = args.indexOf('--descripcion')
        if (d > 0) nueva.descripcion = args[d + 1]
        const tp = args.indexOf('--tipo')
        if (tp > 0) nueva.tipo = args[tp + 1]
        anotar(nueva, 'creada', 'en-cola')
        lista.push(nueva)
        datos.ultimo = id
        guardar()
        return { ok: true, mensaje: `Creada la ${String(id)}, en cola: «${args[1]!}».`, id }
      }
      case 'paso añadir': {
        if (!t || !['en-cola', 'en-curso', 'en-observacion'].includes(t.estado as string)) return no(`La ${String(n)} no está en la cola.`)
        const p = pasos(t)
        const sitio = p.findIndex(x => ['Probar la tarea', 'Cerrar la tarea'].includes(x.texto as string))
        t.pasos = [...p.slice(0, sitio < 0 ? p.length : sitio), { texto: args[3], estado: 'pendiente' }, ...p.slice(sitio < 0 ? p.length : sitio)]
        anotar(t, 'paso', `añadido: ${args[3]!}`)
        guardar()
        return { ok: true, mensaje: `Paso de la ${String(n)}: «${args[3]!}».` }
      }
      case 'paso quitar': {
        const i = Number(args[3])
        t!.pasos = pasos(t!).filter((_, j) => j !== i - 1)
        anotar(t!, 'paso', `quitado ${String(i)}`)
        guardar()
        return { ok: true, mensaje: `Quitado el paso ${String(i)} de la ${String(n)}.` }
      }
      case 'eliminar':
        anotar(t!, 'eliminada', t!.estado as string)
        sacar(t!, 'eliminada')
        guardar()
        return { ok: true, mensaje: `Eliminada la ${String(n)}; su número no se reutiliza.` }
      // propuestas.md lo prueba test_cola.py: aquí solo sale de la cola.
      case 'a-propuesta':
        anotar(t!, 'a-propuesta', 'P09 nueva')
        sacar(t!, 'eliminada')
        guardar()
        return { ok: true, mensaje: `La ${String(n)}, a propuesta: nueva propuesta P09; sale de la cola.` }
      // El commit en develop lo prueba test_cola.py: aquí marca la propuesta en el archivo y crea la tarea.
      case 'de-propuesta': {
        const ruta = PROPUESTAS
        const num = args.indexOf('--numero')
        const lineas = (archivos[ruta] ?? '').split('\n')
        const ini = lineas.findIndex(l => l.trim() === `### ${num > 0 ? `${args[num + 1]!} ` : ''}${args[1]!}`)
        let fin = ini + 1
        while (ini >= 0 && fin < lineas.length && !lineas[fin]!.startsWith('##')) fin++
        const i = ini < 0 ? -1 : lineas.findIndex((l, j) => j >= ini && j < fin && l.startsWith('- **Estado:**'))
        if (i < 0 || !/pendiente de (aprobación|decisión)/i.test(lineas[i]!)) return no('La mejora ya no está por decidir.')
        const id = siguiente()
        lineas[i] = `- **Estado:** pasada a la tarea ${String(id)} de la cola el ${fecha.slice(0, 10)}.`
        archivos[ruta] = lineas.join('\n')
        const nueva: Pet = { id, texto: args[1], estado: 'en-cola' }
        const d = args.indexOf('--descripcion')
        if (d > 0) nueva.descripcion = args[d + 1]
        const tp = args.indexOf('--tipo')
        if (tp > 0) nueva.tipo = args[tp + 1]
        anotar(nueva, 'creada', 'en-cola')
        lista.push(nueva)
        datos.ultimo = id
        guardar()
        return { ok: true, mensaje: `Creada la ${String(id)}, en cola: «${args[1]!}». docs/propuestas.md, en develop (c0ffee1).`, id }
      }
      case 'descartar': {
        const rama = t!.rama as string
        delete archivos[`/sf/.git/refs/heads/${rama}`]
        t!.estado = 'descartada'
        anotar(t!, 'descartada', rama)
        guardar()
        return { ok: true, mensaje: `Descartada la ${String(n)}: rama ${rama} borrada.` }
      }
      case 'limpiar': {
        const salen = lista.filter(x => x.estado === 'descartada')
        if (salen.length === 0) return { ok: true, mensaje: 'No hay descartadas que limpiar.' }
        for (const x of salen) {
          anotar(x, 'limpiada')
          sacar(x, 'descartada')
        }
        guardar()
        return { ok: true, mensaje: `Limpiadas ${String(salen.length)}.` }
      }
      case 'probar': {
        const rama = t!.rama as string
        archivos['/sf/.git/HEAD'] = `ref: refs/heads/${rama}\n`
        if (t!.estado === 'en-cola') t!.estado = 'en-curso'
        anotar(t!, 'probar', rama)
        guardar()
        return { ok: true, mensaje: `La ${String(n)}, en prueba: rama ${rama} activa${t!.prueba ? `. Prueba: ${t!.prueba as string}` : '.'}` }
      }
      case 'cerrar': {
        if (t?.estado === 'en-observacion') {
          anotar(t, 'cerrada', 'en observación')
          sacar(t, 'cerrada')
          guardar()
          return { ok: true, mensaje: `Cerrada la ${String(n)}, en observación: sale de la cola.` }
        }
        const rama = t!.rama as string | undefined
        if (!rama) {
          // Sin rama (188): sale de la cola sin squash ni commit.
          anotar(t!, 'cerrada', 'sin rama')
          t!.pasos = pasos(t!).map(x => (['Activar rama para poder probar', 'Cerrar la tarea'].includes(x.texto as string) ? { ...x, estado: 'hecho' } : x))
          sacar(t!, 'cerrada')
          guardar()
          return { ok: true, mensaje: `Cerrada la ${String(n)}, sin rama.` }
        }
        delete archivos[`/sf/.git/refs/heads/${rama}`]
        archivos['/sf/.git/HEAD'] = 'ref: refs/heads/develop\n'
        logDevelop = `c0ffee1\t${t!.texto as string} (${String(n)})\n${logDevelop}`
        archivos['/sf/.git/refs/heads/develop'] = `${archivos['/sf/.git/refs/heads/develop'] ?? ''}-cerrada`
        anotar(t!, 'cerrada', 'develop c0ffee1')
        if (git.pushFalla) anotar(t!, 'push-fallido', 'fatal: sin red')
        delete t!.rama
        t!.commit = 'c0ffee1'
        t!.pasos = pasos(t!).map(x => (['Probar la tarea', 'Cerrar la tarea'].includes(x.texto as string) ? { ...x, estado: 'hecho' } : x))
        sacar(t!, 'cerrada')
        guardar()
        return { ok: true, mensaje: `Cerrada la ${String(n)} en develop (c0ffee1).${git.pushFalla ? ' Aviso: falta el push de develop (fatal: sin red).' : ''}` }
      }
      case 'a-observacion': {
        const rama = t!.rama as string | undefined
        if (!rama) {
          anotar(t!, 'a-observacion')
          t!.estado = 'en-observacion'
          t!.pasos = pasos(t!).map(x => (x.texto === 'Cerrar la tarea' ? { ...x, estado: 'hecho' } : x))
          guardar()
          return { ok: true, mensaje: `La ${String(n)}, en observación.` }
        }
        delete archivos[`/sf/.git/refs/heads/${rama}`]
        archivos['/sf/.git/HEAD'] = 'ref: refs/heads/develop\n'
        logDevelop = `c0ffee1\t${t!.texto as string} (${String(n)})\n${logDevelop}`
        anotar(t!, 'a-observacion', 'develop c0ffee1')
        delete t!.rama
        t!.commit = 'c0ffee1'
        t!.estado = 'en-observacion'
        t!.pasos = pasos(t!).map(x => (x.texto === 'Cerrar la tarea' ? { ...x, estado: 'hecho' } : x))
        guardar()
        return { ok: true, mensaje: `La ${String(n)}, en observación en develop (c0ffee1).` }
      }
      case 'reobservar': {
        const x = [...fuera].reverse().find(y => y.id === n)
        if (t || x?.estado !== 'cerrada') return no(`La ${String(n)} no es una cerrada.`)
        x.estado = 'en-observacion'
        anotar(x, 'reobservada', 'con develop aaa1111')
        lista.push(x)
        guardar()
        return { ok: true, mensaje: `La ${String(n)} vuelve a observación, con su commit de develop (aaa1111).` }
      }
      case 'revertir': {
        const x = t ?? [...fuera].reverse().find(y => y.id === n)
        if (!x) return no(`La ${String(n)} no está en la cola ni en el historial.`)
        logDevelop = `c0ffee1\tRevert "${x.texto as string} (${String(n)})"\n${logDevelop}`
        archivos['/sf/.git/refs/heads/develop'] = `${archivos['/sf/.git/refs/heads/develop'] ?? ''}-revert`
        delete x.observando
        delete x.commit
        anotar(x, 'revertida', 'develop c0ffee1 revierte …')
        if (args[2] === '--eliminar') {
          anotar(x, 'eliminada', 'en-cola')
          if (t) sacar(t, 'eliminada')
          else archivar(x, 'eliminada')
          guardar()
          return { ok: true, mensaje: `Revertida la ${String(n)} en develop (c0ffee1), sin push, y eliminada; su número no se reutiliza.` }
        }
        x.estado = 'en-cola'
        x.reabierta = true
        delete x.rama
        anotar(x, 'reabierta', 'revertida')
        if (!t) datos.peticiones.push(x)
        guardar()
        return { ok: true, mensaje: `Revertida la ${String(n)} en develop (c0ffee1), sin push; vuelve a Pendientes, en cola.` }
      }
      case 'split': {
        const nums = args[2]!.split(',').map(Number)
        const p = pasos(t!)
        const id = siguiente()
        const separados = nums.map(k => p[k - 1]!)
        t!.pasos = p.filter((_, j) => !nums.includes(j + 1))
        const nueva: Pet = { id, texto: separados[0]!.texto, estado: 'en-cola', pasos: separados }
        anotar(t!, 'separada', `pasos ${nums.join(', ')} a la ${String(id)}`)
        anotar(nueva, 'nacida', `de la ${String(n)}`)
        lista.push(nueva)
        datos.ultimo = id
        guardar()
        const hechos = nums.filter(k => p[k - 1]!.estado === 'hecho')
        const y = (l: number[]) => (l.length < 2 ? l.join('') : `${l.slice(0, -1).join(', ')} y ${String(l.at(-1))}`)
        const aviso = hechos.length ? ` El trabajo ${hechos.length === 1 ? 'del paso' : 'de los pasos'} ${y(hechos)}, ya hecho, sigue en la rama de la ${String(n)}.` : ''
        return { ok: true, mensaje: `Separado de la ${String(n)} ${nums.length === 1 ? 'el paso' : 'los pasos'} ${y(nums)}: tarea ${String(id)}, «${separados[0]!.texto as string}», en cola.${aviso}`, id }
      }
      case 'fusionar': {
        const ids = args.slice(1).map(Number).sort((a, b) => a - b)
        const todas = ids.map(id => lista.find(x => x.id === id)!)
        const queda = todas.at(-1)!
        const salen = todas.slice(0, -1)
        const nuevos = todas.flatMap(x => (pasos(x).length ? pasos(x) : [{ texto: x.texto, estado: x.estado === 'en-curso' ? 'en-curso' : 'pendiente' }]))
        const descripcion = [queda, ...salen].map(x => x.descripcion).filter(Boolean).join('\n\n')
        // Sin git de verdad: con dos ramas o más, como cola.py cuando alguna no está integrada en la de destino.
        const ramas = todas.filter(x => x.rama).map(x => x.rama as string)
        if (ramas.length > 1)
          return no(`La rama ${ramas[0]!} tiene commits que no están en ${ramas.at(-1)!}: intégrala en ${ramas.at(-1)!} antes de fusionar.`)
        const conRama = todas.find(x => x.rama)
        queda.estado = todas.some(x => x.estado === 'en-curso') ? 'en-curso' : 'en-cola'
        queda.pasos = nuevos
        if (descripcion) queda.descripcion = descripcion
        if (conRama) queda.rama = conRama.rama
        const prueba = [queda, ...salen].map(x => x.prueba).find(Boolean)
        if (prueba) queda.prueba = prueba
        anotar(queda, 'fusion', `absorbe ${salen.map(x => String(x.id)).join(', ')}`)
        for (const x of salen) {
          anotar(x, 'absorbida', `en ${String(queda.id)}`)
          sacar(x, 'absorbida')
        }
        guardar()
        const otras = salen.map(x => String(x.id))
        const y = (l: string[]) => (l.length < 2 ? l.join('') : `${l.slice(0, -1).join(', ')} y ${l.at(-1)!}`)
        const rama = conRama && conRama !== queda ? ` Rama: ${conRama.rama as string}.` : ''
        return { ok: true, mensaje: `Fusionadas en la ${String(queda.id)} ${otras.length === 1 ? 'la' : 'las'} ${y(otras)}: ${String(nuevos.length)} pasos.${rama}` }
      }
    }
    return no(`orden desconocida: ${orden}`)
  }
  on('process.run', (_, e) => {
    const { argv, init } = e as { argv: readonly string[]; init?: { stdin?: string; cwd?: string } }
    // La prueba del intérprete de Python (236): responde cada uno de `pythons` con su versión («3 13»), o como el
    // atajo de la Microsoft Store si vale null; los demás no existen.
    if (argv[2] === '-c' && argv[3] === PRUEBA_PYTHON) {
      const v = pythons[argv[0]!]
      if (v === undefined) throw new Error(`no existe ${argv[0]!}`)
      return v === null ? salida('', 9009, 'Python was not found') : salida(`sf-python ${v}
`)
    }
    // indice_decisiones.py --html: escribe README.html junto al README.md, o falla con sinGenerador.
    if (/^(python3?|py)$/.test(argv[0] ?? '') && argv.some(a => /tools\/indice_decisiones\.py$/.test(a.replace(/\\/g, '/')))) {
      const carpeta = ruta(argv.at(-2)!)
      ordenes.push(`indice_decisiones ${argv.slice(-2).join(' ')}`)
      if (sinGenerador) return salida('', 1, "ModuleNotFoundError: No module named 'markdown'")
      archivos[`${carpeta}/README.html`] = '<h1>Decisiones</h1>'
      return salida(`${carpeta}/README.html\n`)
    }
    // La revisión de lo que sale (RELEASE, decisiones 252 y 259): se apunta como «revision <argumentos>».
    if (/^(python3?|py)$/.test(argv[0] ?? '') && argv.some(a => /tools\/revision_publica\.py$/.test(a.replace(/\\/g, '/')))) {
      const i = argv.findIndex(a => /revision_publica\.py$/.test(a))
      ordenes.push(`revision ${argv.slice(i + 1).join(' ')}`)
      if (git.revision === null) return salida('', 1, 'Traceback: roto')
      return salida(JSON.stringify(git.revision ?? { ok: true, accion: 'seguir', mensaje: '', visibilidad: 'PUBLIC', hallazgos: [] }) + '\n')
    }
    // El del plugin (tools/cola.py) o su copia (~/.claude/sf/cola-<sesión>.py).
    if (/^(python3?|py)$/.test(argv[0] ?? '') && argv.some(a => /(tools\/cola|\/cola-[^/]+)\.py$/.test(a.replace(/\\/g, '/')))) {
      lineasCola.push([...argv])
      const i = argv.indexOf('panel')
      return salida(JSON.stringify(colaFalsa(argv.slice(i + 1))) + '\n')
    }
    if (argv[0] === 'git' && argv[1] === 'log' && argv[2] === 'develop') return salida(logDevelop)
    // El programa del sistema que abre archivos, para Activar rama y la línea de Decisiones: se apunta tal cual;
    // `sinAbridor` dice cuáles no existen.
    if (['rundll32', 'xdg-open', 'open'].includes(argv[0] ?? '')) {
      if (git.sinAbridor?.includes(argv[0]!)) throw new Error(`no existe ${argv[0]!}`)
      ordenes.push(argv.join(' '))
      return salida('')
    }
    if (argv[0] === 'git' && argv[1] === 'ls-remote') {
      ordenes.push(argv.join(' '))
      return git.remoto === null ? salida('', 128, 'fatal: unable to access') : salida(git.remoto ?? '')
    }
    // claude plugin update: si no falla, la instalada de ese scope pasa a la publicada más alta.
    if (argv[0] === 'claude') {
      ordenes.push(argv.join(' '))
      cwds.push(ruta(init?.cwd ?? ''))
      // claude plugin marketplace update: refresca el catálogo; falla si se pide.
      if (argv[2] === 'marketplace') return git.catalogoFalla ? salida('', 1, 'Failed to update marketplace') : salida('')
      // claude plugin install <id> --scope <scope>: lo apunta en el registro, salvo que falle.
      if (argv[2] === 'install') {
        const [id, , sc] = argv.slice(3)
        if (git.installFalla?.includes(id!)) return salida('', 1, `Plugin "${id!}" not found in any marketplace`)
        const d = JSON.parse(archivos[INSTALADAS] ?? '{}') as { plugins: Record<string, { scope: string; version: string; projectPath?: string }[]> }
        ;(d.plugins[id!] ??= []).push({ scope: sc!, version: '1', ...(sc === 'user' ? {} : { projectPath: RAIZ }) })
        archivos[INSTALADAS] = JSON.stringify(d)
        return salida('')
      }
      const scope = argv.at(-1)!
      if (git.updateFalla?.includes(scope)) return salida('', 1, `Failed to update plugin in ${scope} scope`)
      const datos = JSON.parse(archivos[INSTALADAS] ?? '{}') as { plugins: Record<string, { scope: string; version: string }[]> }
      const nueva = [...(git.remoto ?? '').matchAll(/refs\/tags\/v(\d+\.\d+\.\d+)$/gm)].map(x => x[1]!).sort().at(-1)!
      if (git.alDia?.includes(scope)) return salida(`Checking for updates…\n✔ sf is already at the latest version (${nueva}).\n`)
      for (const x of datos.plugins['sf@softwarefactory'] ?? []) if (x.scope === scope) x.version = nueva
      archivos[INSTALADAS] = JSON.stringify(datos)
      return salida('')
    }
    if (argv[0] === 'git' && GIT_ORDENES.includes(argv[1])) {
      ordenes.push(argv.join(' '))
      if (init?.stdin !== undefined) entradas.push(init.stdin)
      const ref = (r: string) => `/sf/.git/refs/heads/${r}`
      switch (argv[1]) {
        case 'status':
          return salida(git.status ?? '')
        case 'worktree':
          return salida(git.worktrees ?? `worktree ${RAIZ}\nHEAD abc\nbranch refs/heads/develop\n`)
        case 'symbolic-ref': {
          const m = /^ref: refs\/heads\/(.+)$/.exec((archivos['/sf/.git/HEAD'] ?? '').trim())
          return m ? salida(`${m[1]}\n`) : salida('', 1)
        }
        case 'show-ref':
          return ref(argv.at(-1)!.replace('refs/heads/', '')) in archivos ? salida('') : salida('', 1)
        case 'branch':
          delete archivos[ref(argv.at(-1)!)]
          return salida('')
        case 'merge':
          return git.mergeFalla ? salida('', 1, 'CONFLICT (content)') : salida('')
        case 'diff':
          // Los .html de la rama, para Activar rama (tarea 206), separados por NUL.
          if (argv.includes('-z')) return salida((git.html ?? []).map(x => `${x}\0`).join(''))
          return salida(git.mergeFalla ? 'docs/decisiones.md\n' : '')
        case 'rev-parse': {
          // --verify de una rama: existe si está en .git/refs/heads; de un tag, si está en la lista de tags.
          const r = argv.at(-1)!
          if (argv.includes('--verify') && r.startsWith('refs/heads/')) return ref(r.slice('refs/heads/'.length)) in archivos ? salida('abc\n') : salida('', 1)
          if (argv.includes('--verify') && r.startsWith('refs/tags/')) return (git.tags ?? '').split('\n').includes(r.slice('refs/tags/'.length)) ? salida('abc\n') : salida('', 1)
          return salida('c0ffee1\n')
        }
        case 'tag':
          return argv[2] === '--list' ? salida(git.tags ?? '') : salida('')
        case 'merge-base':
          return git.noAncestro ? salida('', 1) : salida('')
        case 'fetch':
        case 'add':
          return salida('')
        // git show develop:sf/propuestas.md (o la ruta del caso): el de develop, si el caso lo da (tarea 273).
        case 'show':
          return git.propuestasDevelop === undefined || argv[2] !== `develop:${git.rutaDevelop ?? 'sf/propuestas.md'}`
            ? salida('', 128, 'fatal: invalid object name')
            : salida(git.propuestasDevelop)
        case 'push':
          return git.pushFalla ? salida('', 1, 'fatal: sin red') : salida('')
        case 'revert': {
          if (argv[2] === '--abort') return salida('')
          if (git.revertFalla) return salida('', 1, 'CONFLICT (content)')
          // Un commit «Revert "…"» por cada uno, arriba de develop, que pasa a otro commit.
          const titulos = argv.slice(3).map(h => logDevelop.split('\n').find(l => l.startsWith(`${h}\t`))?.split('\t')[1] ?? h)
          logDevelop = titulos.map(t => `c0ffee1\tRevert "${t}"\n`).join('') + logDevelop
          archivos['/sf/.git/refs/heads/develop'] = `${archivos['/sf/.git/refs/heads/develop'] ?? ''}-revert`
          return salida('')
        }
        case 'reset':
        case 'commit':
          return salida('')
      }
      if (git.switchFalla) return salida('', 1, 'error: no se pudo')
      archivos['/sf/.git/HEAD'] = `ref: refs/heads/${argv[2]}\n`
      return salida('')
    }
    return ({
    value: {
      exitCode: 0,
      stdout: `abc1234	${(AHORA - 300000) / 1000}	Panel corto
def5678	${(AHORA - 3 * 3600000) / 1000}	Panel de la SF: un título de commit muy largo que no cabe en una línea
`,
      stderr: '',
      isStdoutTruncated: false,
      isStderrTruncated: false,
    },
  })
  })
  // sinArranque: el mod sin session.start, como tras un /clear que vacía su estado.
  if (!sinArranque) await $.session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })

  // Cambia la cola y la relee como tras una herramienta que puede escribir.
  // Con `fuera`, también las tareas que han salido de la cola entretanto (se añaden a .sf/historial.jsonl).
  const cambiarCola = async (nueva: Pet[], fuera: Pet[] = []) => {
    archivos[COLA] = JSON.stringify({ peticiones: nueva })
    if (fuera.length) archivos[HISTORIAL_JSONL] = (archivos[HISTORIAL_JSONL] ?? '') + fuera.map(x => JSON.stringify(x) + '\n').join('')
    await $.tool.call({ tool: 'Bash', command: 'true' })
  }
  return { archivos, guardado, comandos, prompts, contextos, ordenes, colas, lineasCola, entradas, toasts, marcados, rellenos, cwds, cierres, cambiarCola, reloj: relojEnMemoria }
}

// ACTUALIZAR: lo instalado del plugin sf y el catálogo de donde sale, en la carpeta del usuario (/home).
const INSTALADAS = '/home/.claude/plugins/installed_plugins.json'
const CATALOGOS = '/home/.claude/plugins/known_marketplaces.json'
type Instalada = { scope: string; version: string; projectPath?: string }
const instalado = (entradas: Instalada[]) => ({
  [INSTALADAS]: JSON.stringify({ version: 2, plugins: { 'sf@softwarefactory': entradas, 'sf@softwarefactory-dev': [{ scope: 'local', projectPath: RAIZ, version: '0.1.0' }] } }),
  [CATALOGOS]: JSON.stringify({ softwarefactory: { source: { source: 'github', repo: 'jumibot/SoftwareFactory' } } }),
})
// Lo que responde git ls-remote --tags: cada tag con su ^{} de tag anotado.
const remotos = (...v: string[]) => v.map(x => `abc\trefs/tags/v${x}\ndef\trefs/tags/v${x}^{}\n`).join('')

const hay = async (ui: { find: (q: object) => Promise<unknown> }, q: object) => (await ui.find(q)) !== undefined

// El número de una tarea, sin letra detrás (decisión del propietario, 2026-10-31): el Text que lo lleva solo, con su
// subrayado de desplegable, que no tienen las cuentas. El estado se lee en su color: rojo si ya estaba (o en Cerradas,
// si se reabrió), verde si se probó, gris en el resto; amarillo, la en curso; el fondo rojo, la reabierta.
const GRIS = '#717171'
type Nodo = { props: Record<string, unknown> }
const numeros = async (ui: { findAll: (q: object) => Promise<unknown[]> }, id: number) =>
  ((await ui.findAll({ type: 'Text', text: new RegExp(`^${id}$`) })) as Nodo[]).filter(x => 'underline' in x.props)
// Sus colores, uno por cada sitio donde sale: «error», «#717171 sobre error»; arriba, el color lo hereda de la línea.
const colores = async (ui: { findAll: (q: object) => Promise<unknown[]> }, id: number) =>
  (await numeros(ui, id)).map(x => [x.props.color ?? 'heredado', ...(x.props.backgroundColor === undefined ? [] : [x.props.backgroundColor])].join(' sobre '))
const conNumero = async (ui: { findAll: (q: object) => Promise<unknown[]> }, id: number) => (await numeros(ui, id)).length > 0
// Ningún número con una letra de estado detrás.
const SIN_LETRAS = /^ ?\d+[AHTCDR]( |$)/

for (const surface of ['terminal', 'desktop'] as const) {
  test(`${surface}: cabecera, marcador y bloques`, async (...m) => {
    await preparar(m)
    const ui = await m[0].ui.mount({ ...PANEL, surface })
    // El marcador, bajo el título y fuera de toda sección.
    expect(await ui.find({ type: 'Button', text: /Marcador/ })).toBe(undefined)
    expect(await hay(ui, { type: 'Text', text: /^prompts$/ })).toBe(true)
    expect(await ui.find({ type: 'Text', text: /^hechas$/ })).toBe(undefined)
    // Un solo bloque, sin rótulo (282); sin PROYECTO (decisiones 195 y 197).
    expect(await hay(ui, { type: 'Text', text: /^TAREAS$/ })).toBe(false)
    for (const fuera of [/^PROYECTO$/, /^SESIÓN$/, /^añadidas$/, /^propuestas$/]) expect(await ui.find({ type: 'Text', text: fuera })).toBe(undefined)
    expect(await ui.find({ type: 'Button', key: 'sec:documentos' })).toBe(undefined)
    await ui.unmount()
  })

  test(`${surface}: Cerradas se ve siempre, también con 0`, async (...m) => {
    await preparar(m)
    const ui = await m[0].ui.mount({ ...PANEL, surface })
    expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
    expect(await ui.find({ type: 'Button', text: /^limpiar \(/ })).toBe(undefined)
    await ui.unmount()
  })

  test(`${surface}: tareas en curso arriba, la más reciente primero`, async (...m) => {
    await preparar(m)
    const ui = await m[0].ui.mount({ ...PANEL, surface })
    // Sin marca delante: la tarea de arriba no se despliega.
    expect(await ui.find({ type: 'Text', text: /^▶ $/ })).toBe(undefined)
    expect((await ui.findAll({ type: 'Text', text: /Panel lateral/ })).length > 0).toBe(true)
    expect(await hay(ui, { type: 'Text', text: /Fondos por bloque/ })).toBe(true)
    const lineas = (await ui.findAll({ type: 'Text', text: /^ ?(1|4) / })).map(x => String(x.text ?? ''))
    expect(lineas[0]?.trimStart().startsWith('4')).toBe(true)
    // Sin sección En curso ni «y N más»; En observación, plegada.
    expect(await ui.find({ type: 'Button', text: /en curso/i })).toBe(undefined)
    expect(await ui.find({ type: 'Text', text: /más en curso/ })).toBe(undefined)
    expect(await ui.find({ type: 'Text', text: /Secciones plegables/ })).toBe(undefined)
    await ui.unmount()
  })

  test(`${surface}: Pendientes, solo con las en cola: cuenta sin reparto y números sin letras`, async (...m) => {
    await preparar(m, { cola: [...INICIAL, { id: 6, texto: 'En cola', estado: 'en-cola' }] })
    const ui = await m[0].ui.mount({ ...PANEL, surface })
    // Las dos en curso (1 y 4), solo arriba; en Pendientes, la 6, en gris aunque ya estaba: el rojo, solo para las reabiertas.
    expect(await hay(ui, { type: 'Button', text: /PENDIENTES [▸▾]\s+1$/ })).toBe(true)
    expect(await colores(ui, 6)).toEqual([GRIS])
    for (const id of [1, 4]) {
      expect(await colores(ui, id)).toEqual(['heredado'])
      expect(await ui.find({ type: 'Button', key: `pet:cola:${id}` })).toBe(undefined)
    }
    expect(await ui.find({ type: 'Text', text: SIN_LETRAS })).toBe(undefined)
    await ui.unmount()
  })

  test(`${surface}: En observación despliega cada petición por separado`, async (...m) => {
    const { guardado } = await preparar(m)
    const ui = await m[0].ui.mount({ ...PANEL, surface })
    await ui.press({ key: 'sec:observacion' })
    expect(await hay(ui, { type: 'Button', text: /EN OBSERVACIÓN/ })).toBe(true)
    expect(await hay(ui, { type: 'Button', text: /Secciones plegables/ })).toBe(true)
    // En observación, el número en gris, sin letra.
    expect(await colores(ui, 2)).toEqual([GRIS])
    expect(await ui.find({ type: 'Text', text: SIN_LETRAS })).toBe(undefined)
    // El detalle, plegado; se abre con un clic.
    expect(await ui.find({ type: 'Text', text: /^Pulsar la cabecera$/ })).toBe(undefined)
    await ui.press({ key: 'pet:observacion:2' })
    expect(await ui.find({ type: 'Text', text: /^Pulsar la cabecera$/ })).toBe(undefined)
    // Cómo probarla, en «Prueba», plegada al empezar (tarea 237).
    await ui.press({ key: 'prueba:observacion:2' })
    expect(await hay(ui, { type: 'Text', text: /^Pulsar la cabecera$/ })).toBe(true)
    // Lo plegado se recuerda en el almacén.
    expect(guardado.plegado).toEqual({ observacion: false, 'pet:observacion:2': false, 'prueba:observacion:2': false })
    await ui.unmount()
  })

  test(`${surface}: una petición larga sale entera, plegada y desplegada`, async (...m) => {
    await preparar(m)
    const ui = await m[0].ui.mount({ ...PANEL, surface })
    await ui.press({ key: 'sec:observacion' })
    expect(await hay(ui, { type: 'Button', text: /Un proyecto por sesión.*…/ })).toBe(false)
    expect(await hay(ui, { type: 'Button', text: /bloqueo en el mod de la SF/ })).toBe(true)
    await ui.press({ key: 'pet:observacion:3' })
    expect((await ui.findAll({ type: 'Button', text: /Un proyecto por sesión/ })).length).toBe(1)
    expect(await hay(ui, { type: 'Button', text: /bloqueo en el mod de la SF/ })).toBe(true)
    await ui.unmount()
  })
}

test('Cerradas: solo las que han salido de la cola, en verde si se probaron, y etiqueta «Limpiar»', async (...m) => {
  const { cambiarCola, colas } = await preparar(m, { reloj: true })
  await cambiarCola(CERRADAS, [{ ...CERRADA_4, commit: 'sf 0.9' }])
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // La 4 ya salió de la cola: en verde. La 1 y la 5, pasadas a observación en la sesión, solo en observación, en gris.
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+1$/ })).toBe(true)
  expect(await colores(ui, 4)).toEqual(['success'])
  for (const id of [1, 5]) expect(await conNumero(ui, id)).toBe(false)
  await ui.press({ key: 'sec:observacion' })
  for (const id of [1, 5]) expect(await colores(ui, id)).toEqual([GRIS])
  expect(await ui.find({ type: 'Text', text: SIN_LETRAS })).toBe(undefined)
  // Sin led y sin horas («ahora», «5 min», «3 h»).
  expect(await ui.find({ type: 'Text', text: /●|○/ })).toBe(undefined)
  expect(await ui.find({ type: 'Text', text: /\bahora\b|\d+ (min|h|d)\b|hace/ })).toBe(undefined)
  // Desplegada, su commit.
  await ui.press({ key: 'hecho:4' })
  expect(await hay(ui, { type: 'Text', text: /sf 0\.9/ })).toBe(true)
  // La etiqueta, con dos clics: el primero pide «¿Limpiar? sí» sin quitar nada; el segundo quita las cerradas (la 4),
  // también al releer la cola.
  expect(await hay(ui, { type: 'Text', text: /^ Limpiar \(1\) $/ })).toBe(true)
  await ui.press({ key: 'limpiar-cerradas' })
  expect(await hay(ui, { type: 'Text', text: /^ ¿Limpiar\? sí $/ })).toBe(true)
  expect(await conNumero(ui, 4)).toBe(true)
  await ui.press({ key: 'limpiar-cerradas' })
  expect(await conNumero(ui, 4)).toBe(false)
  expect(await ui.find({ type: 'Button', key: 'limpiar-cerradas' })).toBe(undefined)
  await m[0].tool.call({ tool: 'Bash', command: 'true' })
  expect(await conNumero(ui, 4)).toBe(false)
  // Sin descartadas en la cola, limpiar no llama a cola.py: solo quita de la lista.
  expect(colas).toEqual([])
  await ui.unmount()
})

// «Limpiar (N)», solo con Cerradas desplegada, en su fila de etiquetas, a la izquierda y encima de la lista (282);
// nunca en la cabecera.
test('Cerradas: «Limpiar» solo desplegada, en su fila, encima de la lista', async (...m) => {
  const { cambiarCola } = await preparar(m)
  await cambiarCola(CERRADAS, [CERRADA_4])
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  if (!(await hay(ui, { type: 'Button', key: 'limpiar-cerradas' }))) await ui.press({ key: 'sec:hecho' })
  expect(await hay(ui, { type: 'Button', key: 'limpiar-cerradas' })).toBe(true)
  // Encima de la cerrada: en el dibujo, el texto de la etiqueta va antes que el número de la 4.
  const dibujo = JSON.stringify(await ui.drawn())
  expect(dibujo.indexOf('Limpiar (1)')).toBeGreaterThan(-1)
  expect(dibujo.indexOf('Limpiar (1)')).toBeLessThan(dibujo.indexOf('Fondos por bloque'))
  expect(await hay(ui, { type: 'Button', key: 'sec:hecho', text: /Limpiar/ })).toBe(false)
  await ui.press({ key: 'sec:hecho' })
  expect(await hay(ui, { type: 'Button', key: 'limpiar-cerradas' })).toBe(false)
  expect(await hay(ui, { type: 'Text', text: /Limpiar/ })).toBe(false)
  await ui.unmount()
})

test('Cerradas: salen del historial; las cerradas en otra sesión, no', async (...m) => {
  const { cambiarCola } = await preparar(m)
  await cambiarCola(
    [{ id: 6, texto: 'En observación de antes', estado: 'en-observacion', historial: [ev('a-observacion', 'sf 0.9', ANTES)] }],
    [{ id: 7, texto: 'Cerrada ayer', estado: 'cerrada', historial: [ev('cerrada', 'develop abc1234', ANTES)] }, CERRADA_4],
  )
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await colores(ui, 4)).toEqual(['success'])
  expect(await conNumero(ui, 7)).toBe(false)
  expect(await hay(ui, { type: 'Button', text: /CERRADAS.*1/ })).toBe(true)
  await ui.unmount()
})

test('Cerradas: una cerrada en observación en otra sesión entra en verde; una reabierta sale de Cerradas y vuelve arriba, sobre rojo', async (...m) => {
  const { cambiarCola } = await preparar(m, { reloj: true })
  await cambiarCola(CERRADAS, [CERRADA_4])
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'limpiar-cerradas' })
  await ui.press({ key: 'limpiar-cerradas' })
  // La 2, de En observación (en observación en otra sesión), cerrada; la 4, reabierta después de cerrarse.
  const reabierta = { ...REABIERTA[2]!, reabierta: true, historial: [ev('cerrada', 'sin rama'), ev('reabierta', 'falla el gris', 1)] }
  await cambiarCola(
    [CERRADAS[0]!, REABIERTA[1]!, reabierta, CERRADAS[3]!],
    [{ id: 2, texto: 'Secciones plegables', estado: 'cerrada', historial: [ev('a-observacion', 'sf 0.8', ANTES), ev('cerrada', 'en observación', 2)] }],
  )
  expect(await colores(ui, 2)).toEqual(['success'])
  // La 4, reabierta y en curso: solo arriba, sobre rojo.
  expect(await colores(ui, 4)).toEqual(['heredado sobre error'])
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+1$/ })).toBe(true)
  await ui.unmount()
})

// Orden por defecto: la última que ha cambiado arriba, por la fecha más reciente de su historial (con su zona); sin
// historial, detrás, de la de número más alto a la más baja (petición 166).
const hist = (...fechas: string[]) => fechas.map(fecha => ({ evento: 'paso', fecha, quien: 'principal', via: 'cli' }))
const POR_CAMBIO: Pet[] = [
  // En curso: la 1, tocada la última (a las 11 UTC, escrita en +01:00); la 7, antes; la 9, sin historial.
  { id: 1, texto: 'Uno', estado: 'en-curso', historial: hist('2026-10-26T08:00:00Z', '2026-10-26T12:00:00+01:00') },
  { id: 9, texto: 'Nueve', estado: 'en-curso' },
  { id: 7, texto: 'Siete', estado: 'en-curso', historial: hist('2026-10-26T10:00:00Z') },
  // En cola: la 5 y la 6 sin historial; la 8, con historial: arriba aunque sea la más vieja de fecha.
  { id: 5, texto: 'Cinco', estado: 'en-cola' },
  { id: 8, texto: 'Ocho', estado: 'en-cola', historial: hist('2020-01-01T00:00:00Z') },
  { id: 6, texto: 'Seis', estado: 'en-cola', historial: [] },
  // En observación: la 2, tocada después que la 3, aunque su número sea menor.
  { id: 3, texto: 'Tres', estado: 'en-observacion', historial: hist('2026-10-26T09:00:00Z') },
  { id: 2, texto: 'Dos', estado: 'en-observacion', historial: hist('2026-10-26T09:30:00Z') },
]

// Una fila de POR_CAMBIO: su número y su título.
// El número y el título van en partes separadas (sangría colgante): las filas, por su título.
const ID_POR_CAMBIO: Record<string, string> = { Uno: '1', Dos: '2', Tres: '3', Cinco: '5', Seis: '6', Siete: '7', Ocho: '8', Nueve: '9' }
const FILA_POR_CAMBIO = /^(Uno|Dos|Tres|Cinco|Seis|Siete|Ocho|Nueve)$/
const idsPorCambio = (nodos: unknown[]) => (nodos as { text?: unknown }[]).map(x => ID_POR_CAMBIO[String(x.text)])

test('Orden: en cada lista, la última que ha cambiado arriba; sin historial, detrás y de mayor a menor', async (...m) => {
  await preparar(m, { cola: POR_CAMBIO })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // Arriba, las en curso; en Pendientes, solo la cola.
  const filas = async () => idsPorCambio(await ui.findAll({ type: 'Text', text: FILA_POR_CAMBIO }))
  expect(await filas()).toEqual(['1', '7', '9', '8', '6', '5'])
  // En observación, desplegada, después.
  await ui.press({ key: 'sec:observacion' })
  expect((await filas()).slice(6)).toEqual(['2', '3'])
  await ui.unmount()
})

test('Orden: la tarea principal es la en curso tocada la última', async (...m) => {
  const { cambiarCola } = await preparar(m, { cola: POR_CAMBIO })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // La 9 recibe un paso: pasa arriba.
  await cambiarCola(POR_CAMBIO.map(p => (p.id === 9 ? { ...p, historial: hist('2026-10-27T09:00:00Z') } : p)))
  const arriba = idsPorCambio(await ui.findAll({ type: 'Text', text: FILA_POR_CAMBIO }))
  expect(arriba.slice(0, 3)).toEqual(['9', '1', '7'])
  await ui.unmount()
})

test('Orden: en Cerradas, una tocada después de su cierre sube arriba', async (...m) => {
  const { cambiarCola } = await preparar(m)
  // La 1 se cierra después que la 5; la 5, tocada después de las dos: arriba.
  await cambiarCola(
    [],
    [
      { id: 1, texto: 'Panel lateral', estado: 'cerrada', historial: [ev('cerrada', 'sin rama', 10)] },
      { id: 5, texto: 'Cerrada sin verla en curso', estado: 'cerrada', historial: [ev('cerrada', 'sin rama'), ev('comprobado', undefined, 60)] },
    ],
  )
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // Las filas de Cerradas, por su título.
  const filas = ((await ui.findAll({ type: 'Text', text: /^(Panel lateral|Cerrada sin verla en curso)$/ })) as { text?: unknown }[]).map(x =>
    x.text === 'Panel lateral' ? '1' : '5',
  )
  expect(filas[0]).toBe('5')
  expect(filas.slice(1)).toEqual(['1'])
  await ui.unmount()
})

test('En prueba: solo arriba, ni en Pendientes ni en observación; desplegada, su commit y cómo probarla', async (...m) => {
  const { cambiarCola } = await preparar(m)
  await cambiarCola(CERRADAS.map(p => (p.id === 3 ? { ...p, prueba: 'abrir otra sesión', comprobado: 'el bloqueo' } : p)))
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Box', text: /^3 Un proyecto por sesión/ })).toBe(true)
  // Pendientes, vacía, se ve con 0.
  expect(await hay(ui, { type: 'Button', text: /^PENDIENTES [▸▾] 0$/ })).toBe(true)
  await ui.press({ key: 'sec:observacion' })
  expect(await hay(ui, { type: 'Button', text: /EN OBSERVACIÓN [▸▾]\s+3$/ })).toBe(true)
  expect(await ui.find({ type: 'Button', key: 'pet:observacion:3' })).toBe(undefined)
  // Arriba, desplegada: lo que en observación iba en su detalle.
  await ui.press({ key: 'arriba:3' })
  expect(await ui.findAll({ type: 'Text', text: /^Commit: sf 0\.8\.0$/ })).toHaveLength(1)
  await ui.press({ key: 'prueba:arriba:3' })
  expect(await hay(ui, { type: 'Text', text: /^El bloqueo$/ })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /^Abrir otra sesión$/ })).toBe(true)
  await ui.unmount()
})

test('En curso: arriba, desplegada, cómo probarla y el OK de Claude, como en observación (266)', async (...m) => {
  const cola: Pet[] = [
    { id: 18, texto: 'Lista en su rama', estado: 'en-curso', prueba: 'abrir el panel', comprobado: 'lo abrí',
      pasos: [{ texto: 'Mirar la C', estado: 'pendiente', ayuda: true }] },
  ]
  await preparar(m, { cola })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'arriba:18' })
  // En «Prueba», plegada al empezar, como en observación (tarea 237).
  expect(await hay(ui, { type: 'Button', key: 'prueba:arriba:18', text: /^Prueba ✓$/ })).toBe(true)
  await ui.press({ key: 'prueba:arriba:18' })
  expect(await hay(ui, { type: 'Text', text: /^Abrir el panel$/ })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /^Lo abrí$/ })).toBe(true)
  await ui.press({ key: 'pasos:arriba:18' })
  expect(await hay(ui, { type: 'Text', text: /^Mirar la C \(opcional\)$/ })).toBe(true)
  await ui.unmount()
})

test('En observación: la comprobada por Claude, plegada sin ✓; desplegada, con lo que comprobó', async (...m) => {
  const { cambiarCola } = await preparar(m)
  await cambiarCola(CERRADAS)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  if (!(await hay(ui, { type: 'Button', key: 'pet:observacion:2' }))) await ui.press({ key: 'sec:observacion' })
  expect(await hay(ui, { type: 'Text', text: /✓/ })).toBe(false)
  await ui.press({ key: 'pet:observacion:2' })
  await ui.press({ key: 'prueba:observacion:2' })
  expect(await hay(ui, { type: 'Text', text: /^Prueba del panel$/ })).toBe(true)
  await ui.unmount()
})

test('Pasos: arriba, plegada, solo el título; desplegada, «Pasos 1/3», plegado al empezar y desplegable', async (...m) => {
  await preparar(m, { cola: REABIERTA })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await ui.find({ type: 'Button', key: 'pasos:arriba:4' })).toBe(undefined)
  expect(await ui.find({ type: 'Text', text: /Aplicarlo a los bloques/ })).toBe(undefined)
  await ui.press({ key: 'arriba:4' })
  // La cabecera, el rótulo y la cuenta, sin el paso actual.
  expect(await hay(ui, { type: 'Button', key: 'pasos:arriba:4', text: /^Pasos 1\/3$/ })).toBe(true)
  expect(await ui.find({ type: 'Text', text: /Aplicarlo a los bloques/ })).toBe(undefined)
  await ui.press({ key: 'pasos:arriba:4' })
  expect(await hay(ui, { type: 'Text', text: /^Probarlo$/ })).toBe(true)
  await ui.press({ key: 'pasos:arriba:4' })
  expect(await ui.find({ type: 'Text', text: /^Probarlo$/ })).toBe(undefined)
  // Desplegados, numerados sin punto en tres columnas a la derecha; el texto, aparte: «  1» y «Elegir el gris».
  await ui.press({ key: 'pasos:arriba:4' })
  expect(await hay(ui, { type: 'Text', text: /^Elegir el gris$/ })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /^  1$/ })).toBe(true)
  // En curso, la tarea no sale en Pendientes.
  expect(await ui.find({ type: 'Button', key: 'pet:cola:4' })).toBe(undefined)
  await ui.unmount()
})

// Los pasos pendientes y el en curso, encendidos, en un gris más claro que el de las tareas (#a3a3a3); los hechos, atenuados, en gris
// oscuro (#4f4f4f). También el pendiente con su «×» y la primera vez que se despliegan (tarea 256).
test('Pasos: pendientes y en curso, encendidos; hechos, atenuados', async (...m) => {
  await preparar(m, { cola: REABIERTA })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'arriba:4' })
  await ui.press({ key: 'pasos:arriba:4' })
  const PASO = '#a3a3a3'
  const props = async (t: RegExp) => ((await ui.find({ type: 'Text', text: t })) as Nodo | undefined)?.props
  // Hecho: número y texto atenuados.
  expect(await props(/^Elegir el gris$/)).toMatchObject({ color: '#4f4f4f' })
  expect(await props(/^  1$/)).toMatchObject({ color: '#4f4f4f' })
  // En curso: encendido, y el número en negrita.
  expect(await props(/^Aplicarlo a los bloques$/)).toMatchObject({ color: PASO })
  expect(await props(/^  2$/)).toMatchObject({ color: PASO, weight: 'bold' })
  // Pendiente, con su «×»: encendido y sin negrita.
  expect(await hay(ui, { type: 'Button', key: 'quitar-paso:arriba:4:2' })).toBe(true)
  expect(await props(/^Probarlo$/)).toMatchObject({ color: PASO })
  expect(await props(/^  3$/)).toMatchObject({ color: PASO, weight: 'regular' })
  await ui.unmount()
})

test('/sf_paso añade un paso pendiente a la tarea en curso', async (...m) => {
  const { archivos, prompts } = await preparar(m, { cola: REABIERTA })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const r = await m[0].command.run({ command: 'sf_paso', args: 'Revisar el contraste' })
  expect(r.text).toContain('Paso añadido a la 4')
  const cola = JSON.parse(archivos[COLA]) as { peticiones: { id: number; pasos?: unknown[] }[] }
  expect(cola.peticiones.find(x => x.id === 4)?.pasos?.at(-1)).toEqual({ texto: 'Revisar el contraste', estado: 'pendiente' })
  await ui.press({ key: 'arriba:4' })
  expect(await hay(ui, { type: 'Button', key: 'pasos:arriba:4', text: /^Pasos 1\/4$/ })).toBe(true)
  // Y se lo pide a Claude, que se pone con él sin esperar un «continúa».
  expect(prompts.some(t => t.includes('«Revisar el contraste»') && t.includes('Hazlo ahora'))).toBe(true)
  await ui.unmount()
})

test('/sf_redescribir 9 pide a Claude que vuelva a redactar la descripción de la 9, sin tocar la cola', async (...m) => {
  const { archivos, prompts } = await preparar(m, {
    cola: [
      { id: 9, texto: 'Con descripción', estado: 'en-cola', descripcion: 'Un texto que no se entiende.' },
      { id: 10, texto: 'Sin descripción', estado: 'en-cola' },
    ],
  })
  const antes = archivos[COLA]
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const r = await m[0].command.run({ command: 'sf_redescribir', args: ' 9 ' })
  expect(r.text).toContain('se lo paso a Claude')
  // El aviso a Claude sale de un temporizador de 50 ms.
  await new Promise(fin => setTimeout(fin, 200))
  expect(prompts.some(t => t.startsWith('Redacta de nuevo la descripción de la 9 («Con descripción»)') && t.includes('espera mi OK; solo entonces guárdala con `python -I -X utf8 "$HOME/.claude/sf/cola.py" redescribir 9`'))).toBe(true)
  expect(archivos[COLA]).toBe(antes)
  // Sin número, con una que no está o sin descripción: lo dice y no pide nada.
  for (const [args, dice] of [['', 'Uso: /sf_redescribir'], ['77', 'La 77 no está en la cola'], ['10', 'La 10 no tiene descripción']] as const)
    expect((await m[0].command.run({ command: 'sf_redescribir', args })).text).toContain(dice)
  expect(prompts.filter(t => t.startsWith('Redacta de nuevo'))).toHaveLength(1)
  await ui.unmount()
})

test('/sf_config pasa a Claude cambiar la configuración con sf:configurar_proyecto, con lo pedido; fuera de un proyecto incorporado, no', async (...m) => {
  const { archivos, prompts } = await preparar(m, { sinMarca: true, extra: { '/sf/.sf/proyecto.json': JSON.stringify({ proyecto: 'Demo', color: 'blue' }) } })
  const antes = archivos['/sf/.sf/proyecto.json']
  const r = await m[0].command.run({ command: 'sf_config', args: ' idioma ' })
  expect(r.text).toBe('/sf_config: se lo paso a Claude.')
  // El encargo sale de un temporizador de 50 ms; el mod no toca la configuración.
  await new Promise(fin => setTimeout(fin, 200))
  expect(prompts.some(t => t.startsWith('Cambia la configuración del proyecto con la skill sf:configurar_proyecto') && t.includes('Quiero cambiar: «idioma».'))).toBe(true)
  expect(archivos['/sf/.sf/proyecto.json']).toBe(antes)
  // Sin .sf/proyecto.json, no está incorporado: lo dice y no pide nada.
  delete archivos['/sf/.sf/proyecto.json']
  expect((await m[0].command.run({ command: 'sf_config', args: '' })).text).toContain('no está incorporado')
  // En la SF, tampoco: su configuración sale de su marca.
  archivos['/sf/plugins/sf/.claude-plugin/plugin.json'] = '{}'
  expect((await m[0].command.run({ command: 'sf_config', args: '' })).text).toContain('la SF no tiene .sf/proyecto.json')
  await new Promise(fin => setTimeout(fin, 200))
  expect(prompts.filter(t => t.startsWith('Cambia la configuración'))).toHaveLength(1)
})

test('/sf_paso sin tarea en curso lo dice', async (...m) => {
  await preparar(m, { cola: CERRADAS.filter(x => x.id !== 3) })
  const r = await m[0].command.run({ command: 'sf_paso', args: 'algo' })
  expect(r.text).toContain('No hay ninguna tarea en curso')
})

test('/sf_paso en la tarea que se prueba (en observación) lo pide a cola.py y entra antes de los pasos de cierre', async (...m) => {
  const mirada: Pet = {
    id: 5,
    texto: 'En prueba',
    estado: 'en-observacion',
    observando: true,
    pasos: [
      { texto: 'Hacer A', estado: 'hecho' },
      { texto: 'Probar la tarea', estado: 'pendiente' },
    ],
  }
  const { archivos, colas } = await preparar(m, { cola: [mirada] })
  const r = await m[0].command.run({ command: 'sf_paso', args: 'Corregir el color' })
  expect(r.text).toContain('Paso añadido a la 5')
  expect(colas).toEqual(['paso añadir 5 Corregir el color'])
  expect((tareaCola(archivos, 5)?.pasos as Pet[]).map(x => x.texto)).toEqual(['Hacer A', 'Corregir el color', 'Probar la tarea'])
})

// La copia de cola.py (decisión 136): al cargar, el panel copia el cola.py de su plugin a ~/.claude/sf/cola-<sesión>.py
// y lanza siempre la copia, aunque el del disco cambie (la C, la R o Activar rama cambian de rama la carpeta del plugin).
const EN_CURSO: Pet = { id: 5, texto: 'En curso', estado: 'en-curso' }
const cliDe = (linea: string[]) => linea[4]!.replace(/\\/g, '/').replace(/^[A-Za-z]:/, '')
// La copia lleva en su primera línea la raíz del plugin, donde busca sus módulos (tarea 322).
const copiaDe = (cola: string) => (texto: string | undefined) => {
  const [primera, ...resto] = (texto ?? '').split('\n')
  return primera!.startsWith('# sf-plugin: ') && primera!.length > 13 && resto.join('\n') === cola
}

test('cola.py: al cargar se copia y el panel lanza la copia, aunque el del disco cambie después', async (...m) => {
  const { archivos, lineasCola, toasts } = await preparar(m, { cola: [EN_CURSO] })
  expect(copiaDe('# cola.py v1')(archivos[COPIA_COLA])).toBe(true)
  // La C cambia de rama la carpeta: el cola.py del disco ya es otro.
  archivos[CLI_PLUGIN] = '# cola.py de develop'
  await m[0].command.run({ command: 'sf_paso', args: 'Uno' })
  expect(lineasCola.map(cliDe)).toEqual([COPIA_COLA])
  expect(copiaDe('# cola.py v1')(archivos[COPIA_COLA])).toBe(true)
  expect(toasts.some(t => t.includes('no se pudo copiar cola.py'))).toBe(false)
  // /reload-plugins carga el panel de nuevo: copia el cola.py que hay ahora.
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  expect(copiaDe('# cola.py de develop')(archivos[COPIA_COLA])).toBe(true)
})

test('cola.py: al cargar se copia el lanzador de Claude a ~/.claude/sf/cola.py, y solo si ha cambiado', async (...m) => {
  const { archivos, toasts } = await preparar(m, { cola: [EN_CURSO] })
  expect(archivos[LANZADOR]).toBe('# lanzador v1')
  archivos[LANZADOR_PLUGIN] = '# lanzador v2'
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  expect(archivos[LANZADOR]).toBe('# lanzador v2')
  expect(toasts.some(t => t.includes('lanzador'))).toBe(false)
})

test('cola.py: sin copia, el panel lanza el del disco y avisa una vez', async (...m) => {
  const { lineasCola, toasts } = await preparar(m, { cola: [EN_CURSO], sinCola: true })
  await m[0].command.run({ command: 'sf_paso', args: 'Uno' })
  await m[0].command.run({ command: 'sf_paso', args: 'Dos' })
  expect(lineasCola.map(cliDe).every(c => c.endsWith('/plugins/sf/tools/cola.py'))).toBe(true)
  expect(lineasCola).toHaveLength(2)
  expect(toasts.filter(t => t.includes('no se pudo copiar cola.py'))).toHaveLength(1)
})

test('/sf_paso: si cola.py no lo añade, lo dice y no avisa a Claude', async (...m) => {
  const { prompts } = await preparar(m, { cola: REABIERTA, respuestas: { 'paso añadir': { ok: false, mensaje: 'La 4 no está en la cola.' } } })
  const r = await m[0].command.run({ command: 'sf_paso', args: 'algo' })
  expect(r.text).toBe('/sf_paso: La 4 no está en la cola.')
  await new Promise(fin => setTimeout(fin, 200))
  expect(prompts).toHaveLength(0)
})

// El rojo, solo en las reabiertas, como fondo del número (petición del propietario, 2026-10-31): las de sesiones
// anteriores, en gris, como las de la sesión.
test('Número en gris, de la sesión o de antes; sobre rojo solo si se reabrió, arriba y en Pendientes', async (...m) => {
  const cola: Pet[] = [
    { id: 30, texto: 'Nueva', estado: 'en-cola', historial: [ev('creada', 'en-cola')] },
    { id: 31, texto: 'De antes', estado: 'en-cola', historial: [ev('creada', 'en-cola', ANTES)] },
    { id: 32, texto: 'Nacida de un split', estado: 'en-cola', historial: [ev('nacida', 'de la 31')] },
    { id: 33, texto: 'Reabierta', estado: 'en-curso', reabierta: true, historial: [ev('creada', 'en-cola'), ev('reabierta')] },
    { id: 34, texto: 'Sin historial', estado: 'en-cola' },
    { id: 35, texto: 'Reabierta en cola', estado: 'en-cola', reabierta: true, historial: [ev('creada', 'en-cola', ANTES), ev('reabierta')] },
  ]
  await preparar(m, { cola })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  for (const [id, color] of [[30, GRIS], [31, GRIS], [32, GRIS], [34, GRIS]] as const) expect(await colores(ui, id)).toEqual([color])
  // Las reabiertas, sobre rojo: en curso, arriba; en cola, en Pendientes, con el gris de las tareas.
  expect(await colores(ui, 33)).toEqual(['heredado sobre error'])
  expect(await colores(ui, 35)).toEqual([`${GRIS} sobre error`])
  await ui.unmount()
})

test('Modo prueba: al entrar se apaga y la etiqueta lanza /reload-plugins', async (...m) => {
  const ajustes = {
    extraKnownMarketplaces: { 'softwarefactory-dev': {} },
    enabledPlugins: { 'sf@softwarefactory-dev': true, 'sf@softwarefactory': false },
  }
  const { archivos, comandos } = await preparar(m, { extra: { [AJUSTES]: JSON.stringify(ajustes) } })
  const leidos = () => JSON.parse(archivos[AJUSTES]).enabledPlugins
  // Siempre desactivado al entrar: los ajustes piden el plugin publicado.
  expect(leidos()).toEqual({ 'sf@softwarefactory-dev': false, 'sf@softwarefactory': true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'modo-prueba' })).toBe(true)
  const antes = comandos.filter(c => c === 'reload-plugins').length
  await ui.press({ key: 'modo-prueba' })
  expect(comandos.filter(c => c === 'reload-plugins').length).toBe(antes + 1)
  // El aviso de recargar: «entrar en el» o «salir del», nunca «salir de el».
  expect(await hay(ui, { type: 'Text', text: /reload-plugins para (entrar en el|salir del) modo prueba/ })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /de el modo/ })).toBe(false)
  await ui.unmount()
})

// Tarea 338: una carpeta de prueba, sin la SF, con el catálogo local y la copia de trabajo pedida en sus ajustes: al
// entrar, el mod no la apaga ni recarga, y no crea .sf/ (ni la marca ni el registro).
test('Modo prueba: en una carpeta de prueba, al entrar no se apaga ni se escribe en .sf/', async (...m) => {
  const ajustes = {
    extraKnownMarketplaces: { 'softwarefactory-dev': {} },
    enabledPlugins: { 'sf@softwarefactory-dev': true, 'sf@softwarefactory': false },
  }
  const { archivos, comandos } = await preparar(m, { sinMarca: true, copia: true, extra: { [AJUSTES]: JSON.stringify(ajustes) } })
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  expect(JSON.parse(archivos[AJUSTES]).enabledPlugins).toEqual(ajustes.enabledPlugins)
  expect(comandos).not.toContain('reload-plugins')
  // La cola la pone la prueba; nada más en .sf/.
  expect(Object.keys(archivos).filter(a => a.startsWith('/sf/.sf/') && a !== COLA)).toEqual([])
})

// Tarea 185: el cambio de modo con /sf_prueba, sin el panel. Con Claude trabajando, Claude Code guarda la recarga hasta
// que acaba el turno: se avisa, y el panel de antes sigue mientras.
test('Modo prueba: /sf_prueba lo cambia sin el panel; con Claude trabajando, avisa de que recarga al acabar el turno', async (...m) => {
  const ajustes = { extraKnownMarketplaces: { 'softwarefactory-dev': {} } }
  const { archivos, comandos, toasts, reloj } = await preparar(m, { reloj: true, extra: { [AJUSTES]: JSON.stringify(ajustes) } })
  const leidos = () => JSON.parse(archivos[AJUSTES]).enabledPlugins
  const recargas = () => comandos.filter(c => c === 'reload-plugins').length
  // Desde el publicado: lo enciende y recarga ahora, sin aviso.
  let antes = recargas()
  const r1 = await m[0].command.run({ command: 'sf_prueba', args: '' })
  expect(r1.text).toBe('Modo prueba encendido: recargo ahora.')
  expect(leidos()).toEqual({ 'sf@softwarefactory-dev': true, 'sf@softwarefactory': false })
  await reloj!.advance(10)
  expect(recargas()).toBe(antes + 1)
  expect(toasts.some(t => /Modo prueba/.test(t))).toBe(false)
  // Con un turno del principal en curso: avisa de que la recarga espera al final del turno.
  await m[0].turn.start({ text: 'trabaja', turnId: 't1' })
  antes = recargas()
  const r2 = await m[0].command.run({ command: 'sf_prueba', args: '' })
  expect(r2.text).toBe('Modo prueba encendido: recargo al acabar el turno de Claude.')
  expect(toasts).toContain('Modo prueba encendido: recargo al acabar el turno de Claude. Mientras, sigue este panel.')
  await reloj!.advance(10)
  expect(recargas()).toBe(antes + 1)
  // El turno de un subagente no cuenta; al acabar el del principal, recarga otra vez «ahora».
  await m[0].turn.complete({ turnId: 'a1', agentId: 'sub', answer: '', durationMs: 1, isAborted: false, reason: 'answer' } as never)
  expect((await m[0].command.run({ command: 'sf_prueba', args: '' })).text).toMatch(/al acabar el turno/)
  await m[0].turn.complete({ turnId: 't1', answer: '', durationMs: 1, isAborted: false, reason: 'answer' } as never)
  expect((await m[0].command.run({ command: 'sf_prueba', args: '' })).text).toBe('Modo prueba encendido: recargo ahora.')
})

test('Modo prueba: /sf_prueba sin el catálogo local no cambia nada', async (...m) => {
  const { archivos, comandos } = await preparar(m)
  const r = await m[0].command.run({ command: 'sf_prueba', args: '' })
  expect(r.text).toMatch(/solo está en la SF/)
  expect(AJUSTES in archivos).toBe(false)
  expect(comandos).not.toContain('reload-plugins')
})

// Tarea 307: la copia de trabajo se reconoce por su repositorio (el .git dos niveles por encima del plugin), no por el
// nombre de la carpeta en la que se ejecuta la prueba: desde ella, /sf_prueba apaga el modo y vuelve al publicado.
test('Modo prueba: desde la copia de trabajo, /sf_prueba lo apaga', async (...m) => {
  const ajustes = { extraKnownMarketplaces: { 'softwarefactory-dev': {} } }
  const { archivos } = await preparar(m, { copia: true, reloj: true, extra: { [AJUSTES]: JSON.stringify(ajustes) } })
  const r = await m[0].command.run({ command: 'sf_prueba', args: '' })
  expect(r.text).toBe('Modo prueba apagado: recargo ahora.')
  expect(JSON.parse(archivos[AJUSTES]).enabledPlugins).toEqual({ 'sf@softwarefactory-dev': false, 'sf@softwarefactory': true })
})

// Tarea 185: /sf con el panel ya abierto lo cierra y lo abre de nuevo, para reparar uno que se ha quedado en blanco.
test('/sf: con el panel abierto, lo cierra y lo vuelve a abrir', async (...m) => {
  const { cierres } = await preparar(m, { paneles: () => [{ id: 'sf-estado', title: 'Software Factory', isShown: true, isFocused: false, isPlaced: true }] })
  const r = await m[0].command.run({ command: 'sf', args: '' })
  expect(cierres).toEqual(['sf-estado'])
  expect(r.text).toBe('Panel de la SF abierto.')
})

// Tras un /clear el motor no lanza session.start: el SessionStart de los ajustes, con source «clear», vuelve a leer el
// estado (tarea 239).
test('/clear: con el estado vacío, el panel deja «Leyendo el estado…» y pinta la cola', async (...m) => {
  await preparar(m, { sinArranque: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Text', text: /Leyendo el estado/ })).toBe(true)
  await m[0].classic.SessionStart({ source: 'clear' })
  expect(await hay(ui, { type: 'Text', text: /Leyendo el estado/ })).toBe(false)
  expect(await hay(ui, { type: 'Text', text: /Panel lateral/ })).toBe(true)
  await ui.unmount()
})

test('/clear: con el estado leído, vuelve a leer la cola; otro SessionStart no', async (...m) => {
  const { archivos } = await preparar(m)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  archivos[COLA] = JSON.stringify({ peticiones: [...INICIAL, { id: 9, texto: 'Llegada tras el clear', estado: 'en-curso' }] })
  await m[0].classic.SessionStart({ source: 'compact' })
  expect(await hay(ui, { type: 'Text', text: /Llegada tras el clear/ })).toBe(false)
  await m[0].classic.SessionStart({ source: 'clear' })
  expect(await hay(ui, { type: 'Text', text: /Llegada tras el clear/ })).toBe(true)
  await ui.unmount()
})

// Un /clear empieza una sesión nueva en el panel (decisión 165): la duración, los prompts y las Cerradas, de cero,
// aunque el estado siga leído. /reload-plugins (otro session.start) no los reinicia.
test('/clear: la duración, los prompts y las Cerradas empiezan de cero; /reload-plugins no', async (...m) => {
  const { cambiarCola, reloj } = await preparar(m, { reloj: true })
  await cambiarCola(CERRADAS, [CERRADA_4])
  await m[0].prompt.submit({ text: 'hola', origin: { kind: 'composer' }, wait: false })
  await reloj!.advance(3 * 60_000)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const pintado = async () => JSON.stringify(await ui.drawn())
  const prompts = async () => (await ui.find({ type: 'Text', text: /^\d+$/, weight: 'bold' }))?.text
  expect(await pintado()).toMatch(/ 3m /)
  expect(await prompts()).toBe('1')
  expect(await colores(ui, 4)).toEqual(['success'])
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  expect(await pintado()).toMatch(/ 3m /)
  expect(await prompts()).toBe('1')
  expect(await colores(ui, 4)).toEqual(['success'])
  await m[0].classic.SessionStart({ source: 'clear' })
  expect(await pintado()).toMatch(/ 0m /)
  expect(await prompts()).toBe('0')
  expect(await conNumero(ui, 4)).toBe(false)
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0$/ })).toBe(true)
  await ui.unmount()
})

// Reanudar una conversación (--continue, --resume, /resume) cuenta como abrir la sesión (tarea 350): la duración, los
// prompts y las Cerradas, desde ahí, no desde que empezó la conversación.
test('Reanudar: la duración, los prompts y las Cerradas empiezan de cero (tarea 350)', async (...m) => {
  const { cambiarCola, reloj } = await preparar(m, { reloj: true })
  await cambiarCola(CERRADAS, [CERRADA_4])
  await m[0].prompt.submit({ text: 'hola', origin: { kind: 'composer' }, wait: false })
  await reloj!.advance(3 * 60_000)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const pintado = async () => JSON.stringify(await ui.drawn())
  const prompts = async () => (await ui.find({ type: 'Text', text: /^\d+$/, weight: 'bold' }))?.text
  expect(await colores(ui, 4)).toEqual(['success'])
  await m[0].classic.SessionStart({ source: 'resume' })
  expect(await pintado()).toMatch(/ 0m /)
  expect(await prompts()).toBe('0')
  expect(await conNumero(ui, 4)).toBe(false)
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0$/ })).toBe(true)
  await ui.unmount()
})

// Reanudar con /resume o --resume deja el mod en la sesión reanudada, con su $.state vacío y sin session.start, como
// tras un /clear: el SessionStart «resume» la carga entera y el panel no se queda en «Leyendo el estado…» (tarea 350).
test('Reanudar: con el estado vacío, el panel deja «Leyendo el estado…» y pinta la cola con lo plegado guardado (tarea 350)', async (...m) => {
  await preparar(m, { sinArranque: true, plegado: { hecho: true } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Text', text: /Leyendo el estado/ })).toBe(true)
  await m[0].classic.SessionStart({ source: 'resume' })
  expect(await hay(ui, { type: 'Text', text: /Leyendo el estado/ })).toBe(false)
  expect(await hay(ui, { type: 'Text', text: /Panel lateral/ })).toBe(true)
  expect(JSON.stringify(await ui.drawn())).toMatch(/ 0m /)
  // Lo plegado por el propietario, del $.store: la carga entera, no solo la relectura de la cola.
  expect(await hay(ui, { type: 'Button', text: /CERRADAS ▸\s+0$/ })).toBe(true)
  await ui.unmount()
})

// Con el estado recién vaciado (/reload-plugins que cambia de plugin), una relectura de la cola antes de que el mod
// fije el inicio de la sesión no mete en Cerradas lo cerrado en otras sesiones (tarea 350).
test('Cerradas: con el estado vacío, una relectura antes de cargar no cuenta lo cerrado en otras sesiones (tarea 350)', async (...m) => {
  const vaciar = estadoVaciable(m[1])
  const { archivos } = await preparar(m)
  vaciar()
  archivos[HISTORIAL_JSONL] = JSON.stringify({ id: 7, texto: 'Cerrada ayer', estado: 'cerrada', historial: [ev('cerrada', 'develop abc1234', ANTES)] }) + '\n'
  // El fin de un turno relee la cola (sin esperar a cargar).
  await m[0].turn.complete({ turnId: 't1', answer: '', durationMs: 1, isAborted: false, reason: 'answer' } as never)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await conNumero(ui, 7)).toBe(false)
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0$/ })).toBe(true)
  await ui.unmount()
})

// El registro del modo prueba (.sf/prueba.log), solo en la SF: en un proyecto consumidor no aparece en git.
const REGISTRO_LOG = '/sf/.sf/prueba.log'
// El cierre (session.end) no se puede lanzar desde las pruebas: lo cubre la misma comprobación en anotarPrueba.
test('Registro del modo prueba: sin el catálogo local, al arrancar no se escribe', async (...m) => {
  const { archivos } = await preparar(m)
  expect(REGISTRO_LOG in archivos).toBe(false)
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  expect(REGISTRO_LOG in archivos).toBe(false)
})

test('Registro del modo prueba: en la SF, con el catálogo local, se anota el arranque', async (...m) => {
  const { archivos } = await preparar(m, { extra: { [AJUSTES]: JSON.stringify({ extraKnownMarketplaces: { 'softwarefactory-dev': {} } }) } })
  expect(archivos[REGISTRO_LOG]).toMatch(/arranque: marca/)
})

// Los avisos se turnan con la cabecera en sus filas, unos 5 s cada uno, con el reloj del mod (decisión 164): al abrir,
// la cabecera; a los 5 s, los avisos, en dos filas, con fondo blanco y letra oscura, fuera del cuerpo que sube
// con el scroll, 10 s; a los 15 s, otra vez la cabecera, 5 s.
type ConProps = { props: Record<string, unknown> }
type Montado = { find: (q: object) => Promise<unknown>; findAll: (q: object) => Promise<unknown[]> }
const enCabecera = async (ui: Montado, text: RegExp) => {
  expect(((await ui.find({ type: 'Text', text })) as ConProps).props.color).toBe('#1a1a1a')
  const cajas = (await ui.findAll({ type: 'Box', text })) as ConProps[]
  expect(cajas.some(b => b.props.backgroundColor === '#ffffff' && b.props.height === 2)).toBe(true)
  expect(cajas.some(b => b.props.overflow === 'hidden' && b.props.backgroundColor !== '#ffffff')).toBe(false)
}
const SF_032 = { type: 'Text', text: /^ *SF 0\.32\.3 *$/ }

// El error de la cola, también en la cabecera: antes iba en TAREAS.
test('Cola ilegible: el aviso se turna con la cabecera, con fondo blanco', async (...m) => {
  const { reloj } = await preparar(m, { reloj: true, extra: { [COLA]: '{ roto' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Text', text: /^⚠ no se puede leer/ })).toBe(false)
  await reloj!.advance(5000)
  await enCabecera(ui, /^⚠ no se puede leer/)
  await ui.unmount()
})

// Un proyecto incorporado con una SF anterior: el panel lo dice y cómo ponerlo al día.
for (const [sf, atras] of [['0.13', true], ['0.32.0', false]] as const) {
  test(`Proyecto en la SF ${sf}: ${atras ? 'avisa, turnándose con la cabecera,' : 'no avisa y la cabecera se queda'} de que va por detrás`, async (...m) => {
    const { reloj } = await preparar(m, { reloj: true, sinMarca: true, extra: { '/sf/.sf/proyecto.json': JSON.stringify({ sf, proyecto: 'Demo' }) } })
    const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
    // En el panel de 38 columnas, la primera de sus dos filas.
    const textoAviso = /^⚠ incorporado con la SF 0\.13; va/
    // Al abrir, la cabecera.
    expect(await hay(ui, SF_032)).toBe(true)
    expect(await hay(ui, { type: 'Text', text: textoAviso })).toBe(false)
    // Un solo aviso, con las dos versiones; ningún «→».
    expect(await hay(ui, { type: 'Text', text: /→/ })).toBe(false)
    // La línea gris del proyecto no sale en el panel lateral (decisión 166).
    expect(await hay(ui, { type: 'Text', text: new RegExp(`^SF ${sf.replaceAll('.', '\\.')} · `) })).toBe(false)
    // A los 5 s, el aviso en lugar de la cabecera; sin aviso, la cabecera sigue.
    await reloj!.advance(5000)
    expect(await hay(ui, { type: 'Text', text: textoAviso })).toBe(atras)
    expect(await hay(ui, SF_032)).toBe(!atras)
    expect(await hay(ui, { type: 'Button', key: 'turbo' })).toBe(!atras)
    if (atras) await enCabecera(ui, textoAviso)
    // El aviso dura 10 s: a los 10, sigue; a los 15, otra vez la cabecera, 5 s.
    await reloj!.advance(5000)
    expect(await hay(ui, { type: 'Text', text: textoAviso })).toBe(atras)
    await reloj!.advance(5000)
    expect(await hay(ui, SF_032)).toBe(true)
    expect(await hay(ui, { type: 'Text', text: textoAviso })).toBe(false)
    await reloj!.advance(5000)
    expect(await hay(ui, { type: 'Text', text: textoAviso })).toBe(atras)
    await ui.unmount()
  })
}

// La cabecera, con avisos o sin ellos, tiene el mismo alto: sus dos filas y el relleno.
// Un clic en el aviso blanco lo quita hasta su siguiente turno: la cabecera, con sus 5 s enteros, y otra vez el aviso,
// con sus 10 (petición del propietario, 2026-11-01).
test('Avisos: un clic los quita hasta su siguiente turno', async (...m) => {
  const { reloj } = await preparar(m, { reloj: true, sinMarca: true, extra: { '/sf/.sf/proyecto.json': JSON.stringify({ sf: '0.13', proyecto: 'Demo' }) } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const aviso = { type: 'Text', text: /incorporado con la SF 0\.13/ }
  await reloj!.advance(5000)
  expect(await hay(ui, aviso)).toBe(true)
  await ui.press({ key: 'aviso:0' })
  expect(await hay(ui, aviso)).toBe(false)
  expect(await hay(ui, SF_032)).toBe(true)
  await reloj!.advance(4000)
  expect(await hay(ui, aviso)).toBe(false)
  await reloj!.advance(1000)
  expect(await hay(ui, aviso)).toBe(true)
  // El turno de antes del clic ya no cuenta: a los 15 s desde el principio, el aviso sigue.
  await reloj!.advance(5000)
  expect(await hay(ui, aviso)).toBe(true)
  await reloj!.advance(5000)
  expect(await hay(ui, aviso)).toBe(false)
  await ui.unmount()
})

// Un aviso que no cabe en las dos filas se recorta con «…»; con varios, una fila cada uno.
test('Avisos: dos filas; el que no cabe, recortado con «…»', async (...m) => {
  const { reloj } = await preparar(m, { reloj: true, sinMarca: true, extra: { '/sf/.sf/proyecto.json': JSON.stringify({ sf: '0.13', proyecto: 'Demo' }) } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await reloj!.advance(5000)
  const filas = ((await ui.findAll({ type: 'Text', text: /./ })) as { text?: string; props: Record<string, unknown> }[])
    .filter(t => t.props.color === '#1a1a1a')
    .map(t => String(t.text ?? ''))
  expect(filas).toHaveLength(2)
  expect(filas[0]).toBe('⚠ incorporado con la SF 0.13; va')
  expect(filas[1]!.endsWith('…')).toBe(true)
  expect(filas.every(f => f.length <= 34)).toBe(true)
  await ui.unmount()
})

// Con varios, uno por turno blanco, con sus dos filas, en ciclo; un clic pasa al siguiente en su turno (petición del
// propietario, 2026-11-01).
test('Avisos: con dos, uno por turno, en ciclo; tras un clic, el siguiente', async (...m) => {
  const { reloj } = await preparar(m, { reloj: true, sinMarca: true, extra: { [COLA]: '{ roto', '/sf/.sf/proyecto.json': JSON.stringify({ sf: '0.13', proyecto: 'Demo' }) } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const filas = async () => ((await ui.findAll({ type: 'Text', text: /./ })) as { text?: string; props: Record<string, unknown> }[])
    .filter(t => t.props.color === '#1a1a1a')
    .map(t => String(t.text ?? ''))
  const cola = /^⚠ no se puede leer/
  const version = /^⚠ incorporado con la SF 0\.13/
  // 5 s: el de la cola, en sus dos filas, sin «(+N)».
  await reloj!.advance(5000)
  let f = await filas()
  expect(f).toHaveLength(2)
  expect(f[0]).toMatch(cola)
  expect(f.some(x => version.test(x) || /\(\+\d+\)/.test(x))).toBe(false)
  // El fondo alterna: el primero, blanco; el segundo, gris claro.
  const fondo = async (text: RegExp) => ((await ui.findAll({ type: 'Box', text })) as ConProps[]).map(b => b.props.backgroundColor).find(c => c !== undefined)
  expect(await fondo(cola)).toBe('#ffffff')
  // 15 s, la cabecera; 20 s, el del proyecto atrasado.
  await reloj!.advance(10_000)
  expect(await filas()).toHaveLength(0)
  await reloj!.advance(5000)
  f = await filas()
  expect(f[0]).toMatch(version)
  expect(f.some(x => cola.test(x))).toBe(false)
  expect(await fondo(version)).toBe('#d4d4d4')
  // 35 s, otra vez el de la cola; un clic lo quita y, en el turno siguiente, sale el otro.
  await reloj!.advance(15_000)
  expect((await filas())[0]).toMatch(cola)
  await ui.press({ key: 'aviso:0' })
  expect(await filas()).toHaveLength(0)
  await reloj!.advance(5000)
  expect((await filas())[0]).toMatch(version)
  await ui.unmount()
})

test('Cabecera: tres filas de alto sin rama, con la cabecera normal y con los avisos', async (...m) => {
  const { reloj } = await preparar(m, { reloj: true, sinMarca: true, extra: { '/sf/.sf/proyecto.json': JSON.stringify({ sf: '0.13', proyecto: 'Demo' }) } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const alto = async (text: RegExp) => ((await ui.findAll({ type: 'Box', text })) as ConProps[]).map(b => b.props.height).filter(h => h !== undefined)
  expect(await alto(/ TURBO /)).toEqual([3])
  await reloj!.advance(5000)
  // Los avisos, en un bloque de dos filas dentro de las tres de la cabecera.
  expect(await alto(/incorporado con la SF/)).toEqual([3, 2])
  await ui.unmount()
})

test('Cabecera: con rama, cuatro filas de alto, la cabecera normal y con los avisos (tarea 260)', async (...m) => {
  const { reloj } = await preparar(m, { reloj: true, extra: { ...GIT('ref: refs/heads/develop\n'), [COLA]: '{' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const alto = async (text: RegExp) => ((await ui.findAll({ type: 'Box', text })) as ConProps[]).map(b => b.props.height).filter(h => h !== undefined)
  expect(await alto(/ TURBO /)).toEqual([4])
  await reloj!.advance(5000)
  // Los avisos, en su bloque de dos filas, dentro de las cuatro de la cabecera: no cambia de alto.
  expect(await alto(/no se puede leer/)).toEqual([4, 2])
  await ui.unmount()
})

// El amarillo: la línea, solo arriba; en las secciones, solo el código de la tarea en curso; los pasos, sin él
// (decisión del propietario, 2026-10-28, precisada el 2026-10-29).
const AMARILLO = '#facc15'
const conAmarillo = (nodo: unknown) => JSON.stringify(nodo).includes(AMARILLO)

test('Amarillo: la línea, solo arriba; en Pendientes, nada; los pasos, no', async (...m) => {
  await preparar(m, { cola: [...REABIERTA, { id: 6, texto: 'En cola', estado: 'en-cola' }] })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // Arriba, la línea de la tarea en amarillo, y solo ahí: en curso, no sale en Pendientes.
  const lineas = await ui.findAll({ type: 'Text', text: /Fondos por bloque/ })
  expect(lineas.filter(conAmarillo)).toHaveLength(1)
  expect(String(lineas.find(conAmarillo)?.text ?? '')).toBe('Fondos por bloque')
  expect(await hay(ui, { type: 'Box', text: /^4 Fondos por bloque/ })).toBe(true)
  expect(await ui.find({ type: 'Button', key: 'pet:cola:4' })).toBe(undefined)
  // Una tarea en cola, sin amarillo.
  const fila6 = await ui.find({ type: 'Box', text: /^6 En cola$/ })
  expect(fila6 !== undefined && !conAmarillo(fila6)).toBe(true)
  // El paso en curso, sin amarillo.
  await ui.press({ key: 'arriba:4' })
  await ui.press({ key: 'pasos:arriba:4' })
  expect(await hay(ui, { type: 'Text', text: /Aplicarlo a los bloques/ })).toBe(true)
  expect((await ui.findAll({ type: 'Text', text: /Aplicarlo a los bloques/ })).some(conAmarillo)).toBe(false)
  await ui.unmount()
})

test('Pasos: con todos hechos, siguen la cuenta y el despliegue', async (...m) => {
  const hechos = REABIERTA.map(p =>
    p.id === 4 ? { ...p, pasos: (p.pasos as Pet[]).map(x => ({ ...x, estado: 'hecho' })) } : p,
  )
  await preparar(m, { cola: hechos })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'arriba:4' })
  expect(await hay(ui, { type: 'Button', key: 'pasos:arriba:4', text: /^Pasos 3\/3$/ })).toBe(true)
  await ui.press({ key: 'pasos:arriba:4' })
  expect(await hay(ui, { type: 'Text', text: /^Probarlo$/ })).toBe(true)
  await ui.unmount()
})

test('/sf_paso sin texto explica el uso y no avisa a Claude', async (...m) => {
  const { prompts } = await preparar(m, { cola: REABIERTA })
  const r = await m[0].command.run({ command: 'sf_paso', args: '  ' })
  expect(r.text).toContain('Uso: /sf_paso')
  expect(prompts).toHaveLength(0)
})

test('Pasos: un paso pendiente se quita con la × y dos clics; los hechos y el en curso no la llevan', async (...m) => {
  const { archivos, reloj } = await preparar(m, { cola: REABIERTA, reloj: true })
  const antes = archivos[COLA]
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'arriba:4' })
  await ui.press({ key: 'pasos:arriba:4' })
  // Solo el pendiente (el 3.º, índice 2) lleva el botón.
  expect(await ui.find({ type: 'Button', key: 'quitar-paso:arriba:4:0' })).toBe(undefined)
  expect(await ui.find({ type: 'Button', key: 'quitar-paso:arriba:4:1' })).toBe(undefined)
  expect(await hay(ui, { type: 'Button', key: 'quitar-paso:arriba:4:2', text: /^ ×$/ })).toBe(true)
  // El primer clic pide confirmación, sin quitarlo; a los 5 s vuelve a ser la ×.
  await ui.press({ key: 'quitar-paso:arriba:4:2' })
  expect(archivos[COLA]).toBe(antes)
  expect(await hay(ui, { type: 'Text', text: /^ ¿Quitar\? sí$/ })).toBe(true)
  await reloj!.advance(5500)
  expect(await ui.find({ type: 'Text', text: /^ ¿Quitar\? sí$/ })).toBe(undefined)
  await ui.press({ key: 'quitar-paso:arriba:4:2' })
  await ui.press({ key: 'quitar-paso:arriba:4:2' })
  const cola = JSON.parse(archivos[COLA]) as { peticiones: { id: number; pasos?: { texto: string }[] }[] }
  expect(cola.peticiones.find(x => x.id === 4)?.pasos?.map(x => x.texto)).toEqual(['Elegir el gris', 'Aplicarlo a los bloques'])
  expect(await ui.find({ type: 'Text', text: /^Probarlo$/ })).toBe(undefined)
  expect(await hay(ui, { type: 'Button', key: 'pasos:arriba:4', text: /^Pasos 1\/2$/ })).toBe(true)
  await ui.unmount()
})

test('Pasos: con varias en curso arriba, cada una despliega los suyos', async (...m) => {
  // La 9, más reciente, va primera; la 4, con pasos, debajo.
  await preparar(m, { cola: [...REABIERTA, { id: 9, texto: 'Otra en curso', estado: 'en-curso' }] })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'arriba:4' })
  expect(await ui.find({ type: 'Button', key: 'pasos:arriba:9' })).toBe(undefined)
  await ui.press({ key: 'pasos:arriba:4' })
  expect(await hay(ui, { type: 'Text', text: /^Elegir el gris$/ })).toBe(true)
  await ui.unmount()
})

test('/sf_paso con varias en curso: con su número va a esa; sin él, pregunta a cuál', async (...m) => {
  const [$, on] = m
  const preguntas: unknown[] = []
  on('tool.call', { tool: 'AskUserQuestion' }, (_, e) => {
    preguntas.push(e)
    const q = (e as unknown as { questions: { question: string }[] }).questions[0]!.question
    return { result: { questions: (e as unknown as { questions: unknown[] }).questions, answers: { [q]: '4 Fondos por bloque' } } }
  })
  const { archivos } = await preparar(m, { cola: [...REABIERTA, { id: 9, texto: 'Otra en curso', estado: 'en-curso' }] })
  const pasosDe = (id: number) =>
    (JSON.parse(archivos[COLA]) as { peticiones: { id: number; pasos?: { texto: string }[] }[] }).peticiones
      .find(x => x.id === id)?.pasos?.map(x => x.texto) ?? []
  // Con el número delante, a esa tarea, sin preguntar.
  const r1 = await $.command.run({ command: 'sf_paso', args: '4 Revisar el contraste' })
  expect(r1.text).toContain('Paso añadido a la 4')
  expect(pasosDe(4).at(-1)).toBe('Revisar el contraste')
  expect(preguntas).toHaveLength(0)
  // Sin número, pregunta; la respuesta elige la tarea.
  const r2 = await $.command.run({ command: 'sf_paso', args: 'Otro paso' })
  expect(r2.text).toContain('elige a cuál')
  const ui = await $.ui.mount({ ...PANEL, surface: 'terminal' })
  expect(preguntas).toHaveLength(1)
  expect(pasosDe(4).at(-1)).toBe('Otro paso')
  expect(pasosDe(9)).toHaveLength(0)
  await ui.unmount()
})

// /sf_split (decisión del propietario, 2026-10-29): la 4, en curso, con tres pasos; la 7, en cola, con uno; la 8, en
// curso, sin pasos; la 9, en cola, con dos.
const SPLIT: Pet[] = [
  ...REABIERTA,
  { id: 7, texto: 'Un solo paso', estado: 'en-cola', pasos: [{ texto: 'Único', estado: 'pendiente' }] },
  { id: 8, texto: 'Sin pasos', estado: 'en-curso' },
  {
    id: 9,
    texto: 'Dos pasos',
    estado: 'en-cola',
    pasos: [
      { texto: 'Uno, con coma', estado: 'pendiente' },
      { texto: 'Dos', estado: 'pendiente' },
    ],
  },
]

// Una tarea de la cola, sin su historial (lo mira eventosDe).
const tareaCola = (archivos: Record<string, string>, id: number) => {
  const t = (JSON.parse(archivos[COLA] ?? '{}') as { peticiones: Pet[] }).peticiones.find(x => x.id === id)
  if (!t) return undefined
  const { historial: _, ...resto } = t
  return resto
}
// Los eventos del historial de una tarea, en la cola o, si ha salido, en .sf/historial.jsonl (la última línea).
const eventosDe = (archivos: Record<string, string>, id: number) => {
  const fuera = (archivos[HISTORIAL_JSONL] ?? '').split('\n').filter(Boolean).map(l => JSON.parse(l) as Pet).reverse()
  const t = (JSON.parse(archivos[COLA] ?? '{}') as { peticiones: Pet[] }).peticiones.find(x => x.id === id) ?? fuera.find(x => x.id === id)
  return ((t?.historial as { evento: string }[] | undefined) ?? []).map(e => e.evento)
}

test('/sf_split 4 2,3 crea la tarea nueva en la cola, sin Claude', async (...m) => {
  const { archivos, prompts, colas } = await preparar(m, { cola: SPLIT })
  const r = await m[0].command.run({ command: 'sf_split', args: '4 2,3' })
  expect(r.text).toBe('Separado de la 4 los pasos 2 y 3: tarea 10, «Aplicarlo a los bloques», en cola.')
  expect(prompts).toHaveLength(0)
  expect(colas).toEqual(['split 4 2,3'])
  expect(eventosDe(archivos, 10)).toEqual(['nacida'])
  expect(tareaCola(archivos, 4)!.pasos).toEqual([{ texto: 'Elegir el gris', estado: 'hecho' }])
  expect(tareaCola(archivos, 10)).toEqual({
    id: 10,
    texto: 'Aplicarlo a los bloques',
    estado: 'en-cola',
    pasos: [
      { texto: 'Aplicarlo a los bloques', estado: 'en-curso' },
      { texto: 'Probarlo', estado: 'pendiente' },
    ],
  })
  expect((JSON.parse(archivos[COLA]!) as { ultimo: number }).ultimo).toBe(10)
})

test('/sf_split: el número sigue al último dado, aunque ya no esté en la cola; avisa si un paso ya está hecho', async (...m) => {
  const { archivos } = await preparar(m, { cola: SPLIT })
  archivos[COLA] = JSON.stringify({ ultimo: 50, peticiones: SPLIT })
  const r = await m[0].command.run({ command: 'sf_split', args: '4 1' })
  expect(r.text).toBe('Separado de la 4 el paso 1: tarea 51, «Elegir el gris», en cola. El trabajo del paso 1, ya hecho, sigue en la rama de la 4.')
  expect(tareaCola(archivos, 51)!.texto).toBe('Elegir el gris')
})

test('/sf_split: sin pasos, paso que no existe, todos los pasos o mal escrito, lo dice y no cambia nada', async (...m) => {
  const { archivos, prompts } = await preparar(m, { cola: SPLIT })
  const antes = archivos[COLA]
  const dice = async (args: string) => (await m[0].command.run({ command: 'sf_split', args })).text
  expect(await dice('8 1')).toBe('La 8 no tiene pasos que separar.')
  expect(await dice('7 1')).toBe('La 7 solo tiene un paso: separarlo es renombrarla.')
  expect(await dice('4 5')).toBe('La 4 no tiene paso 5: tiene 3.')
  expect(await dice('4 1,2,3')).toBe('No se pueden separar todos los pasos de la 4: eso es renombrarla.')
  expect(await dice('4 3 1 2')).toBe('No se pueden separar todos los pasos de la 4: eso es renombrarla.')
  expect(await dice('2 1')).toBe('La 2 no está en curso ni en cola.')
  expect(await dice('hola')).toContain('Uso: /sf_split')
  expect(prompts).toHaveLength(0)
  expect(archivos[COLA]).toBe(antes)
})

test('/sf_split: si la tarea ha cambiado desde que se vio, no cambia nada', async (...m) => {
  const { archivos, prompts } = await preparar(m, { cola: SPLIT })
  // Claude cambia los pasos de la 4 y el panel aún no lo ha releído.
  archivos[COLA] = JSON.stringify({
    peticiones: SPLIT.map(p => (p.id === 4 ? { ...p, pasos: [{ texto: 'Otro', estado: 'pendiente' }, ...(p.pasos as Pet[])] } : p)),
  })
  const antes = archivos[COLA]
  const r = await m[0].command.run({ command: 'sf_split', args: '4 2' })
  expect(r.text).toContain('la 4 ha cambiado')
  expect(prompts).toHaveLength(0)
  expect(archivos[COLA]).toBe(antes)
})

test('/sf_split a secas pregunta la tarea y después los pasos, con varios a la vez', async (...m) => {
  const [$, on] = m
  const preguntas: { question: string; options: { label: string }[]; multiSelect?: boolean }[] = []
  on('tool.call', { tool: 'AskUserQuestion' }, (_, e) => {
    const qs = (e as unknown as { questions: typeof preguntas }).questions
    preguntas.push(qs[0]!)
    const q = qs[0]!.question
    const a = q.includes('De qué tarea') ? '9 Dos pasos' : '1 Uno  con coma'
    return { result: { questions: qs, answers: { [q]: a } } }
  })
  const { archivos, prompts } = await preparar(m, { cola: SPLIT })
  const antes = archivos[COLA]
  const r = await $.command.run({ command: 'sf_split', args: '' })
  expect(r.text).toBe('Elige de qué tarea separas pasos (9, 4).')
  const ui = await $.ui.mount({ ...PANEL, surface: 'terminal' })
  expect(preguntas.map(q => q.options.map(o => o.label))).toEqual([
    ['9 Dos pasos', '4 Fondos por bloque'],
    ['1 Uno  con coma', '2 Dos'],
  ])
  expect(preguntas[1]!.multiSelect).toBe(true)
  expect(prompts).toHaveLength(0)
  expect(archivos[COLA]).not.toBe(antes)
  expect(tareaCola(archivos, 9)!.pasos).toEqual([{ texto: 'Dos', estado: 'pendiente' }])
  expect(tareaCola(archivos, 10)!.texto).toBe('Uno, con coma')
  await ui.unmount()
})

// La S del panel (decisión del propietario, 2026-10-29): la 9, en cola, con dos pasos pendientes; la 12, en curso,
// con uno hecho y cinco pendientes; la 4, con un solo pendiente, y la 7, con uno, no la llevan.
const CON_S: Pet[] = [
  ...SPLIT,
  {
    id: 12,
    texto: 'Muchos pasos',
    estado: 'en-curso',
    pasos: [
      { texto: 'Hecho', estado: 'hecho' },
      ...['A', 'B', 'C', 'D', 'E'].map(t => ({ texto: t, estado: 'pendiente' as const })),
    ],
  },
  // Un pendiente y los dos de cierre: «Probar» y «Cerrar» no cuentan, no lleva S.
  {
    id: 13,
    texto: 'Solo falta cerrar',
    estado: 'en-cola',
    pasos: [
      { texto: 'Uno', estado: 'pendiente' },
      { texto: 'Probar la tarea', estado: 'pendiente' },
      { texto: 'Cerrar la tarea', estado: 'pendiente' },
    ],
  },
]

test('S: en las tareas con dos pasos pendientes o más, en Pendientes y arriba', async (...m) => {
  await preparar(m, { desplegadas: true, cola: CON_S })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'split-tarea:cola:9' })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'split-tarea:arriba:12' })).toBe(true)
  expect(await ui.find({ type: 'Button', key: 'split-tarea:cola:12' })).toBe(undefined)
  expect(await ui.find({ type: 'Button', key: 'split-tarea:cola:4' })).toBe(undefined)
  expect(await ui.find({ type: 'Button', key: 'split-tarea:arriba:4' })).toBe(undefined)
  expect(await ui.find({ type: 'Button', key: 'split-tarea:cola:7' })).toBe(undefined)
  expect(await ui.find({ type: 'Button', key: 'split-tarea:cola:8' })).toBe(undefined)
  expect(await ui.find({ type: 'Button', key: 'split-tarea:cola:13' })).toBe(undefined)
  await ui.unmount()
})

test('S: pregunta solo los pasos pendientes, con varios a la vez, y separa sin Claude', async (...m) => {
  const [$, on] = m
  const preguntas: { question: string; options: { label: string }[]; multiSelect?: boolean }[] = []
  on('tool.call', { tool: 'AskUserQuestion' }, (_, e) => {
    const qs = (e as unknown as { questions: typeof preguntas }).questions
    preguntas.push(qs[0]!)
    return { result: { questions: qs, answers: { [qs[0]!.question]: '2 Dos' } } }
  })
  const cola: Pet[] = [
    ...SPLIT.filter(p => p.id !== 9),
    {
      id: 9,
      texto: 'Tres pasos',
      estado: 'en-cola',
      pasos: [
        { texto: 'Hecho', estado: 'hecho' },
        { texto: 'Dos', estado: 'pendiente' },
        { texto: 'Tres', estado: 'pendiente' },
      ],
    },
  ]
  const { archivos, prompts, toasts } = await preparar(m, { desplegadas: true, cola })
  const ui = await $.ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'split-tarea:cola:9' })
  await new Promise(r => setTimeout(r, 200))
  expect(preguntas.map(q => q.options.map(o => o.label))).toEqual([['2 Dos', '3 Tres']])
  expect(preguntas[0]!.multiSelect).toBe(true)
  expect(prompts).toHaveLength(0)
  expect(tareaCola(archivos, 9)!.pasos).toEqual([
    { texto: 'Hecho', estado: 'hecho' },
    { texto: 'Tres', estado: 'pendiente' },
  ])
  expect(tareaCola(archivos, 10)).toEqual({ id: 10, texto: 'Dos', estado: 'en-cola', pasos: [{ texto: 'Dos', estado: 'pendiente' }] })
  expect(toasts).toContain('Separado de la 9 el paso 2: tarea 10, «Dos», en cola.')
  await ui.unmount()
})

test('S: con más de cuatro pasos pendientes, recuerda la forma corta en vez de preguntar', async (...m) => {
  const [$, on] = m
  let preguntado = false
  on('tool.call', { tool: 'AskUserQuestion' }, () => {
    preguntado = true
    return { result: { questions: [], answers: {} } }
  })
  const { archivos, toasts } = await preparar(m, { desplegadas: true, cola: CON_S })
  const antes = archivos[COLA]
  const ui = await $.ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'split-tarea:arriba:12' })
  await new Promise(r => setTimeout(r, 200))
  expect(preguntado).toBe(false)
  // La orden primero: el aviso se corta por el final (tarea 257).
  expect(toasts).toContain('/sf_split 12 2,3 con los pasos que separas. Pendientes: 2 A · 3 B · 4 C · 5 D · 6 E')
  expect(archivos[COLA]).toBe(antes)
  await ui.unmount()
})

// /sf_fusionar (decisión del propietario, 2026-10-29): la 2, en observación; la 4, en cola, con dos pasos y descripción;
// la 6, en cola, sin pasos y con prueba; la 7, en cola, y la 8, en curso, con rama; la 9, en cola, con un paso y
// descripción; la 11, descartada.
const FUSION: Pet[] = [
  { id: 2, texto: 'Secciones plegables', estado: 'en-observacion', prueba: 'pulsar la cabecera' },
  {
    id: 4,
    texto: 'Fondos por bloque',
    estado: 'en-cola',
    descripcion: 'Grises suaves.',
    pasos: [
      { texto: 'Elegir el gris', estado: 'hecho' },
      { texto: 'Aplicarlo', estado: 'pendiente' },
    ],
  },
  { id: 6, texto: 'Sin pasos en cola', estado: 'en-cola', prueba: 'mirar el fondo' },
  { id: 7, texto: 'Con rama', estado: 'en-cola', rama: 'feature/07-con-rama' },
  { id: 8, texto: 'Sin pasos en curso', estado: 'en-curso', rama: 'feature/08-en-curso' },
  { id: 9, texto: 'La que queda', estado: 'en-cola', descripcion: 'La suya.', pasos: [{ texto: 'Su paso', estado: 'pendiente' }] },
  { id: 11, texto: 'Descartada', estado: 'descartada' },
]
const idsDe = (archivos: Record<string, string>) =>
  (JSON.parse(archivos[COLA] ?? '{}') as { peticiones: Pet[] }).peticiones.map(x => x.id)

test('/sf_fusionar 4 6 9: queda la 9, con los pasos de todas en orden y las descripciones sin origen, sin Claude', async (...m) => {
  const { archivos, prompts } = await preparar(m, { cola: FUSION })
  const r = await m[0].command.run({ command: 'sf_fusionar', args: '9 4,6' })
  expect(r.text).toBe('Fusionadas en la 9 las 4 y 6: 4 pasos.')
  expect(prompts).toHaveLength(0)
  expect(idsDe(archivos)).toEqual([2, 7, 8, 9])
  expect(tareaCola(archivos, 9)).toEqual({
    id: 9,
    texto: 'La que queda',
    estado: 'en-cola',
    descripcion: 'La suya.\n\nGrises suaves.',
    prueba: 'mirar el fondo',
    pasos: [
      { texto: 'Elegir el gris', estado: 'hecho' },
      { texto: 'Aplicarlo', estado: 'pendiente' },
      { texto: 'Sin pasos en cola', estado: 'pendiente' },
      { texto: 'Su paso', estado: 'pendiente' },
    ],
  })
})

test('/sf_fusionar: la que queda sin pasos aporta su nombre; una en curso la pasa a en curso y le da su rama', async (...m) => {
  const { archivos } = await preparar(m, { cola: FUSION })
  const r1 = await m[0].command.run({ command: 'sf_fusionar', args: '4 6' })
  expect(r1.text).toBe('Fusionadas en la 6 la 4: 3 pasos.')
  expect(tareaCola(archivos, 6)).toEqual({
    id: 6,
    texto: 'Sin pasos en cola',
    estado: 'en-cola',
    descripcion: 'Grises suaves.',
    prueba: 'mirar el fondo',
    pasos: [
      { texto: 'Elegir el gris', estado: 'hecho' },
      { texto: 'Aplicarlo', estado: 'pendiente' },
      { texto: 'Sin pasos en cola', estado: 'pendiente' },
    ],
  })
  const r2 = await m[0].command.run({ command: 'sf_fusionar', args: '8 9' })
  expect(r2.text).toBe('Fusionadas en la 9 la 8: 2 pasos. Rama: feature/08-en-curso.')
  expect(tareaCola(archivos, 9)).toMatchObject({
    estado: 'en-curso',
    rama: 'feature/08-en-curso',
    pasos: [
      { texto: 'Sin pasos en curso', estado: 'en-curso' },
      { texto: 'Su paso', estado: 'pendiente' },
    ],
  })
  expect(idsDe(archivos)).toEqual([2, 6, 7, 9])
})

test('/sf_fusionar: dos con rama, En observación, descartada, fuera de la cola o menos de dos, lo dice y no cambia nada', async (...m) => {
  const { archivos, prompts, cambiarCola } = await preparar(m, { cola: FUSION })
  // Al empezar la sesión, la descartada de otra sale de la cola: vuelve a estar, descartada en esta.
  await cambiarCola(FUSION.map(p => (p.id === 11 ? { ...p, historial: [ev('descartada', 'feature/11-x')] } : p)))
  // La relectura tras la herramienta no se espera: se espera a que el panel pinte la 11 en Cerradas.
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await colores(ui, 11)).toEqual([GRIS])
  await ui.unmount()
  const antes = archivos[COLA]
  const dice = async (args: string) => (await m[0].command.run({ command: 'sf_fusionar', args })).text
  // Con dos ramas decide cola.py, que ve git; el panel pasa su motivo.
  expect(await dice('7 8 9')).toBe(
    '/sf_fusionar: La rama feature/07-con-rama tiene commits que no están en feature/08-en-curso: intégrala en feature/08-en-curso antes de fusionar.',
  )
  expect(await dice('2 9')).toBe('La 2 está en observación: no se fusiona.')
  expect(await dice('11 9')).toBe('La 11 está descartada: no se fusiona.')
  expect(await dice('9 200')).toBe('La 200 no está en la cola.')
  expect(await dice('9')).toContain('Hacen falta dos tareas o más')
  expect(await dice('9 9')).toContain('Hacen falta dos tareas o más')
  expect(await dice('hola')).toContain('Uso: /sf_fusionar')
  expect(prompts).toHaveLength(0)
  expect(archivos[COLA]).toBe(antes)
})

test('/sf_fusionar: si una tarea ha cambiado desde que se vio, no cambia nada', async (...m) => {
  const { archivos, prompts } = await preparar(m, { cola: FUSION })
  // Claude añade un paso a la 6 y el panel aún no lo ha releído.
  archivos[COLA] = JSON.stringify({
    peticiones: FUSION.map(p => (p.id === 6 ? { ...p, pasos: [{ texto: 'Nuevo', estado: 'pendiente' }] } : p)),
  })
  const antes = archivos[COLA]
  const r = await m[0].command.run({ command: 'sf_fusionar', args: '6 9' })
  expect(r.text).toContain('la 6 ha cambiado')
  expect(prompts).toHaveLength(0)
  expect(archivos[COLA]).toBe(antes)
})

test('/sf_fusionar a secas pregunta cuáles, con varias a la vez; con menos de dos, no fusiona', async (...m) => {
  const [$, on] = m
  const preguntas: { question: string; options: { label: string }[]; multiSelect?: boolean }[] = []
  const respuestas = ['9 La que queda, 6 Sin pasos en cola', '9 La que queda']
  on('tool.call', { tool: 'AskUserQuestion' }, (_, e) => {
    const qs = (e as unknown as { questions: typeof preguntas }).questions
    preguntas.push(qs[0]!)
    return { result: { questions: qs, answers: { [qs[0]!.question]: respuestas[preguntas.length - 1]! } } }
  })
  const { archivos, prompts, toasts } = await preparar(m, { cola: FUSION })
  const r = await $.command.run({ command: 'sf_fusionar', args: '' })
  expect(r.text).toBe('Elige qué tareas fusionas (9, 8, 7, 6).')
  const ui = await $.ui.mount({ ...PANEL, surface: 'terminal' })
  expect(preguntas[0]!.options.map(o => o.label)).toEqual(['9 La que queda', '8 Sin pasos en curso', '7 Con rama', '6 Sin pasos en cola'])
  expect(preguntas[0]!.multiSelect).toBe(true)
  expect(toasts).toContain('Fusionadas en la 9 la 6: 2 pasos.')
  expect(idsDe(archivos)).toEqual([2, 4, 7, 8, 9])
  // Una sola elegida: lo dice y no toca la cola.
  const antes = archivos[COLA]
  await $.command.run({ command: 'sf_fusionar', args: '' })
  await ui.unmount()
  const ui2 = await $.ui.mount({ ...PANEL, surface: 'terminal' })
  expect(toasts).toContain('Elige dos tareas o más: no se ha fusionado nada.')
  expect(archivos[COLA]).toBe(antes)
  expect(prompts).toHaveLength(0)
  await ui2.unmount()
})

test('/sf_fusionar: las que salen no entran en Cerradas ni cuentan como hechas', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { cola: FUSION, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await m[0].command.run({ command: 'sf_fusionar', args: '4 6 9' })
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  // Otra relectura de la cola tampoco las cierra.
  await cambiarCola((JSON.parse(archivos[COLA] ?? '{}') as { peticiones: Pet[] }).peticiones)
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  await ui.unmount()
})

test('/sf_fusionar deshecha: la que vuelve a la cola no es reabierta ni sale en Cerradas', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { cola: FUSION, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await m[0].command.run({ command: 'sf_fusionar', args: '4 6' })
  expect(eventosDe(archivos, 4)).toEqual(['absorbida'])
  // Se deshace: la 4 vuelve a la cola con su historial.
  const fusionada = (JSON.parse(archivos[COLA] ?? '{}') as { peticiones: Pet[] }).peticiones
  await cambiarCola([...fusionada, { ...FUSION[1]!, historial: [ev('creada', 'en-cola', ANTES), ev('absorbida', 'en 6', 1), ev('restaurada', 'en-cola', 2)] }])
  // Vuelve a Pendientes como estaba, de otra sesión (en gris, sin fondo), y no a Cerradas.
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  if (!(await hay(ui, { type: 'Button', key: 'pet:cola:4' }))) await ui.press({ key: 'sec:cola' })
  expect(await hay(ui, { type: 'Button', key: 'pet:cola:4' })).toBe(true)
  expect(await colores(ui, 4)).toEqual([GRIS])
  await ui.unmount()
})

test('/sf_fusionar deshecha: la que entró en la sesión vuelve en gris, no en rojo', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { cola: FUSION, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const nueva: Pet = { id: 3, texto: 'Nueva de la sesión', estado: 'en-cola', historial: [ev('creada', 'en-cola')] }
  await cambiarCola([...FUSION, nueva])
  await m[0].command.run({ command: 'sf_fusionar', args: '3 9' })
  const fusionada = (JSON.parse(archivos[COLA] ?? '{}') as { peticiones: Pet[] }).peticiones
  await cambiarCola([...fusionada.filter(p => p.id !== 3), { ...nueva, historial: [ev('creada', 'en-cola'), ev('absorbida', 'en 9', 1), ev('restaurada', 'en-cola', 2)] }])
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  // Sin descripción no se despliega: se mira su título para saber si Pendientes está abierta.
  if (!(await hay(ui, { type: 'Text', text: /Nueva de la sesión/ }))) await ui.press({ key: 'sec:cola' })
  expect(await colores(ui, 3)).toEqual([GRIS])
  await ui.unmount()
})

// Propuestas: las por decidir de sf/propuestas.md del proyecto (decisión 203); la P02, por decidir, y la P03, ya decidida.
const PROPUESTAS = '/sf/sf/propuestas.md'
// El sitio de antes, que se sigue leyendo mientras el proyecto no se ha puesto al día.
const PROPUESTAS_ANTES = '/sf/docs/propuestas.md'
const PROPUESTAS_EJ = [
  '# Propuestas',
  '',
  '## Propuestas pendientes',
  '',
  '### P02 El detalle, solo cuando está claro',
  '',
  '- **Origen:** SoftwareFactory, 2026-10-27.',
  '- **Tipo:** documentar.',
  '- **Cambio propuesto:** Detallar solo lo que está claro. Lo demás, después.',
  '- **Estado:** propuesta, pendiente de aprobación.',
  '',
  '### P03 Otra ya decidida',
  '',
  '- **Estado:** decidida.',
  '',
  '## Descartadas',
  '',
].join('\n')

// Plegada, una propuesta solo muestra número y título; desplegada, su fila de etiquetas (decisión 197).
const P02 = 'prop:El detalle, solo cuando está claro'
const abrirP02 = async (ui: { press: (q: object) => Promise<unknown>; findAll: (q: object) => Promise<unknown[]>; find: (q: object) => Promise<unknown> }) => {
  if (await hay(ui, { type: 'Button', key: 'a-pendientes:P02' })) return
  if (!(await hay(ui, { type: 'Button', key: P02 }))) await ui.press({ key: 'sec:propuestas' })
  await ui.press({ key: P02 })
}

test('Propuestas: plegada, solo número y título; desplegada, «A Pendientes» en su fila de etiquetas, a la izquierda', async (...m) => {
  await preparar(m, { extra: { [PROPUESTAS]: PROPUESTAS_EJ } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  if (!(await hay(ui, { type: 'Button', key: P02 }))) await ui.press({ key: 'sec:propuestas' })
  expect(await hay(ui, { type: 'Button', key: 'a-pendientes:P02' })).toBe(false)
  expect(await hay(ui, { type: 'Text', text: /^Detallar solo lo que está claro/ })).toBe(false)
  await ui.press({ key: P02 })
  expect(await hay(ui, { type: 'Button', key: 'a-pendientes:P02' })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /^Detallar solo lo que está claro/ })).toBe(true)
  // La fila de etiquetas, tras todo el texto: título, resumen y, después, «A Pendientes».
  const dibujo = JSON.stringify(await ui.drawn())
  const [titulo, resumen, etiqueta] = ['El detalle, solo cuando está claro', 'Detallar solo lo que está claro', 'A Pendientes'].map(t => dibujo.indexOf(t))
  expect(titulo).toBeGreaterThan(-1)
  expect(resumen).toBeGreaterThan(titulo)
  expect(etiqueta).toBeGreaterThan(resumen)
  await ui.press({ key: P02 })
  expect(await hay(ui, { type: 'Button', key: 'a-pendientes:P02' })).toBe(false)
  await ui.unmount()
})

test('Propuestas: «A Pendientes», con dos clics, la pasa a tarea en cola, con su resumen y su tipo, y cola.py la marca en propuestas.md, sin Claude', async (...m) => {
  const { archivos, prompts, toasts, colas } = await preparar(m, { reloj: true, extra: { [PROPUESTAS]: PROPUESTAS_EJ } })
  archivos[COLA] = JSON.stringify({ ultimo: 40, peticiones: INICIAL })
  await m[0].tool.call({ tool: 'Bash', command: 'true' })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await abrirP02(ui)
  expect(await hay(ui, { type: 'Button', key: 'a-pendientes:P03' })).toBe(false)
  await ui.press({ key: 'a-pendientes:P02' })
  await ui.press({ key: 'a-pendientes:P02' })
  expect(colas).toEqual(['de-propuesta El detalle, solo cuando está claro --numero P02 --descripcion Detallar solo lo que está claro. --tipo documentar'])
  expect(tareaCola(archivos, 41)).toEqual({
    id: 41,
    texto: 'El detalle, solo cuando está claro',
    estado: 'en-cola',
    descripcion: 'Detallar solo lo que está claro.',
    tipo: 'documentar',
  })
  // Su «Estado» ya no dice «pendiente de…»: sale de la lista y no se pasa dos veces. Lo demás queda igual.
  expect(archivos[PROPUESTAS]).toBe(
    PROPUESTAS_EJ.replace('- **Estado:** propuesta, pendiente de aprobación.', '- **Estado:** pasada a la tarea 41 de la cola el 2026-10-27.'),
  )
  expect(toasts).toContain('Tarea 41 en cola: El detalle, solo cuando está claro')
  expect(prompts).toHaveLength(0)
  expect(await hay(ui, { type: 'Button', key: 'a-pendientes:P02' })).toBe(false)
  await ui.unmount()
})

// «A Pendientes» es una etiqueta de orden con dos clics (decisión 197): el primero pide «¿A Pendientes? sí» sin tocar la cola.
test('Propuestas: el primer clic en «A Pendientes» pide confirmar; a los 5 s vuelve a ser la etiqueta', async (...m) => {
  const { colas, reloj } = await preparar(m, { reloj: true, extra: { [PROPUESTAS]: PROPUESTAS_EJ } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await abrirP02(ui)
  expect(await hay(ui, { type: 'Text', text: /^ A Pendientes $/ })).toBe(true)
  await ui.press({ key: 'a-pendientes:P02' })
  expect(await hay(ui, { type: 'Text', text: /^ ¿A Pendientes\? sí $/ })).toBe(true)
  expect(colas).toEqual([])
  await reloj!.advance(5100)
  expect(await hay(ui, { type: 'Text', text: /^ A Pendientes $/ })).toBe(true)
  expect(colas).toEqual([])
  await ui.unmount()
})

// Sin «Tipo», o con uno que cola.py no conoce, la tarea se crea sin tipo. Sin «Cambio propuesto», el «Tipo» no hace de
// resumen: sin más apartados, la tarea va sin descripción.
for (const [caso, linea] of [['sin «Tipo»', ''], ['con un «Tipo» desconocido', '- **Tipo:** pensar.\n']] as const)
  test(`Propuestas: ${caso}, «A Pendientes» la pasa sin tipo`, async (...m) => {
    const md = PROPUESTAS_EJ.replace('- **Tipo:** documentar.\n', linea).replace(/- \*\*Cambio propuesto:\*\*.*\n/, '')
    const { colas } = await preparar(m, { reloj: true, extra: { [PROPUESTAS]: md } })
    const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
    await abrirP02(ui)
    await ui.press({ key: 'a-pendientes:P02' })
    await ui.press({ key: 'a-pendientes:P02' })
    expect(colas).toEqual(['de-propuesta El detalle, solo cuando está claro --numero P02'])
    await ui.unmount()
  })

test('Propuestas: si cola.py no crea la tarea, propuestas.md queda como estaba y lo dice', async (...m) => {
  const { archivos, toasts } = await preparar(m, {
    reloj: true,
    extra: { [PROPUESTAS]: PROPUESTAS_EJ },
    respuestas: { 'de-propuesta': { ok: false, mensaje: 'cola.py no responde (python: not found).' } },
  })
  const cola = archivos[COLA]
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await abrirP02(ui)
  await ui.press({ key: 'a-pendientes:P02' })
  await ui.press({ key: 'a-pendientes:P02' })
  expect(archivos[PROPUESTAS]).toBe(PROPUESTAS_EJ)
  expect(archivos[COLA]).toBe(cola)
  expect(toasts).toContain('A Pendientes: cola.py no responde (python: not found).')
  expect(await hay(ui, { type: 'Button', key: 'a-pendientes:P02' })).toBe(true)
  await ui.unmount()
})

// propuestas.md vive en develop (tarea 273): con otra rama activa, Propuestas lee el de develop, donde cola.py hace sus
// commits; el de la rama activa aún dice «pendiente».
const PASADA_EN_DEVELOP = PROPUESTAS_EJ.replace('- **Estado:** propuesta, pendiente de aprobación.', '- **Estado:** pasada a la tarea 41 de la cola el 2026-10-27.')
const CON_DEVELOP = { [PROPUESTAS]: PROPUESTAS_EJ, '/sf/.git/refs/heads/develop': 'abc', '/sf/.git/refs/heads/feature/6-algo': 'abc' }
// Con P02 por decidir solo en la carpeta: sale con develop activa; con otra, solo si en develop también lo está.
for (const [rama, enDevelop, sale] of [
  ['feature/6-algo', PASADA_EN_DEVELOP, false],
  ['feature/6-algo', PROPUESTAS_EJ, true],
  ['develop', PASADA_EN_DEVELOP, true],
] as const)
  test(`Propuestas: con ${rama} activa, ${sale ? 'sale' : 'no sale'} la P02 ${enDevelop === PROPUESTAS_EJ ? 'por decidir' : 'pasada'} en develop`, async (...m) => {
    const { ordenes } = await preparar(m, {
      extra: { ...CON_DEVELOP, '/sf/.git/HEAD': `ref: refs/heads/${rama}
` },
      git: { propuestasDevelop: enDevelop },
    })
    const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
    for (let i = 0; i < 2 && !(await hay(ui, { type: 'Button', key: P02 })); i++)
      if (await hay(ui, { type: 'Button', key: 'sec:propuestas' })) await ui.press({ key: 'sec:propuestas' })
    expect(await hay(ui, { type: 'Button', key: P02 })).toBe(sale)
    expect(ordenes.includes('git show develop:sf/propuestas.md')).toBe(rama !== 'develop')
    await ui.unmount()
  })

// Decisión 203: mientras el proyecto no se ha puesto al día, Propuestas lee docs/propuestas.md; con los dos, manda sf/.
test('Propuestas: sin sf/propuestas.md, las de docs/propuestas.md, también en develop con otra rama activa', async (...m) => {
  const { ordenes } = await preparar(m, {
    extra: { [PROPUESTAS_ANTES]: PROPUESTAS_EJ, '/sf/.git/refs/heads/develop': 'abc', '/sf/.git/refs/heads/feature/6-algo': 'abc', '/sf/.git/HEAD': 'ref: refs/heads/feature/6-algo\n' },
    git: { propuestasDevelop: PROPUESTAS_EJ, rutaDevelop: 'docs/propuestas.md' },
  })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await abrirP02(ui)
  expect(await hay(ui, { type: 'Button', key: 'a-pendientes:P02' })).toBe(true)
  expect(ordenes.includes('git show develop:docs/propuestas.md')).toBe(true)
  await ui.unmount()
})

test('Propuestas: con sf/propuestas.md y docs/propuestas.md, las de sf/', async (...m) => {
  const viejas = PROPUESTAS_EJ.replace('P02 El detalle, solo cuando está claro', 'P05 Una de antes')
  await preparar(m, { extra: { [PROPUESTAS]: PROPUESTAS_EJ, [PROPUESTAS_ANTES]: viejas } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await abrirP02(ui)
  expect(await hay(ui, { type: 'Button', key: 'a-pendientes:P02' })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /Una de antes/ })).toBe(false)
  await ui.unmount()
})

// 269: con CLAUDE_CONFIG_DIR (una configuración desechable), las copias de cola.py no van a ~/.claude.
test('CLAUDE_CONFIG_DIR: las copias de cola.py van a su carpeta, nada al ~/.claude real', async (...m) => {
  const { archivos, lineasCola } = await preparar(m, { cola: [EN_CURSO], entorno: { CLAUDE_CONFIG_DIR: 'C:\\config\\' } })
  expect(archivos['/config/sf/fuente.json']).toBe(undefined)
  expect(copiaDe('# cola.py v1')(archivos['/config/sf/cola-sesion-1.py'])).toBe(true)
  expect(archivos['/config/sf/cola.py']).toBe('# lanzador v1')
  expect(Object.keys(archivos).filter(k => k.startsWith('/home/'))).toEqual([])
  await m[0].command.run({ command: 'sf_paso', args: 'Uno' })
  expect(lineasCola.map(cliDe)).toEqual(['/config/sf/cola-sesion-1.py'])
})

// Decisión 194: cada proyecto ve sus propias propuestas, con «→»; ni registro ni mejoras de la SF, aunque quede un
// fuente.json de antes que la apunte.
test('Propuestas en otro proyecto: las de su sf/propuestas.md, con «A Pendientes»; sin SF ENHANCE ni las de la SF', async (...m) => {
  const deLaSf = PROPUESTAS_EJ.replace('P02 El detalle, solo cuando está claro', 'P05 Una mejora de la SF')
  const { colas } = await preparar(m, {
    reloj: true,
    sinMarca: true,
    extra: {
      '/sf/.sf/proyecto.json': JSON.stringify({ sf: '0.33', proyecto: 'Demo' }),
      [PROPUESTAS]: PROPUESTAS_EJ,
      '/home/.claude/sf/fuente.json': JSON.stringify({ ruta: '/fuente' }),
      '/fuente/plugins/sf/.claude-plugin/plugin.json': '{}',
      '/fuente/.sf/registro.json': JSON.stringify({ registro: [{ id: 7, tipo: 'friccion', texto: 'Una fricción' }] }),
      '/fuente/docs/propuestas.md': deLaSf,
    },
  })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await abrirP02(ui)
  expect(await hay(ui, { type: 'Text', text: /^SF ENHANCE$/ })).toBe(false)
  expect(await hay(ui, { type: 'Button', text: /^REGISTRO/ })).toBe(false)
  expect(await hay(ui, { type: 'Text', text: /Una fricción|Una mejora de la SF/ })).toBe(false)
  // La última sección, tras Cerradas, y sin bloque PROYECTO (decisión 197).
  expect(await hay(ui, { type: 'Text', text: /^PROYECTO$/ })).toBe(false)
  const cabeceras = ((await ui.findAll({ type: 'Button', text: /^(PROPUESTAS|PENDIENTES|EN OBSERVACIÓN|CERRADAS) [▸▾]/ })) as { text?: unknown }[]).map(b => String(b.text).replace(/ [▸▾].*$/, ''))
  expect(cabeceras).toEqual(['PENDIENTES', 'EN OBSERVACIÓN', 'CERRADAS', 'PROPUESTAS'])
  expect(await hay(ui, { type: 'Button', text: /^PROPUESTAS [▸▾]\s+1/ })).toBe(true)
  await ui.press({ key: 'a-pendientes:P02' })
  await ui.press({ key: 'a-pendientes:P02' })
  expect(colas).toEqual(['de-propuesta El detalle, solo cuando está claro --numero P02 --descripcion Detallar solo lo que está claro. --tipo documentar'])
  await ui.unmount()
})

test('Pasos: «?» en cada paso pide a Claude que lo explique, sin tocar la cola', async (...m) => {
  const { archivos, prompts } = await preparar(m, { cola: REABIERTA })
  const antes = archivos[COLA]
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'arriba:4' })
  await ui.press({ key: 'pasos:arriba:4' })
  for (const i of [0, 1, 2]) expect(await hay(ui, { type: 'Button', key: `info-paso:arriba:4:${i}` })).toBe(true)
  // En verde, para que se vea que es un botón.
  const interrogantes = (await ui.findAll({ type: 'Text', text: /^ \?$/ })).map(x => x.props.color)
  expect(interrogantes.length >= 3 && interrogantes.every(c => c === 'success')).toBe(true)
  await ui.press({ key: 'info-paso:arriba:4:0' })
  expect(prompts.some(t => t.includes('Explícame el paso «Elegir el gris» de la 4 (hecho)'))).toBe(true)
  expect(archivos[COLA]).toBe(antes)
  await ui.unmount()
})

test('Pasos: el «?» de los pasos de cierre explica el flujo de tareas (253)', async (...m) => {
  const { archivos, prompts } = await preparar(m, { cola: CERRABLES, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const antes = archivos[COLA]
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'arriba:12' })
  await ui.press({ key: 'pasos:arriba:12' })
  await ui.press({ key: 'info-paso:arriba:12:1' })
  await ui.press({ key: 'info-paso:arriba:12:2' })
  const probar = prompts.find(t => t.startsWith('Explícame el paso «Activar rama para poder probar» de la 12 (pendiente) para alguien que no conoce'))
  const cerrar = prompts.find(t => t.startsWith('Explícame el paso «Cerrar la tarea» de la 12 (pendiente) para alguien que no conoce'))
  for (const t of [probar, cerrar]) {
    for (const trozo of ['feature/12-', 'develop', 'squash', 'subagente', 'En observación', 'si se cierra sin probarla', 'hacer ahora con la 12', 'no lo hagas ni cambies nada'])
      expect(t).toContain(trozo)
  }
  expect(probar).toContain('recargando el plugin')
  expect(cerrar).toContain('OK del propietario')
  expect(archivos[COLA]).toBe(antes)
  await ui.unmount()
})

test('Arriba: una tarea con descripción se despliega para verla', async (...m) => {
  const cola = REABIERTA.map(p => (p.id === 4 ? { ...p, descripcion: 'Gris fijo para el tema oscuro' } : p))
  await preparar(m, { cola: [...cola, { id: 9, texto: 'Otra en curso', estado: 'en-curso', descripcion: 'Detalle de la 9' }] })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // Plegadas: sin descripción a la vista.
  expect(await ui.find({ type: 'Text', text: /Gris fijo para el tema oscuro/ })).toBe(undefined)
  // La primera (9) y la segunda (4) se despliegan cada una, con su «Descripción» abierta, sin tocar sus partes.
  await ui.press({ key: 'arriba:4' })
  expect(await hay(ui, { type: 'Text', text: /Gris fijo para el tema oscuro/ })).toBe(true)
  expect(await ui.find({ type: 'Text', text: /Detalle de la 9/ })).toBe(undefined)
  await ui.press({ key: 'arriba:9' })
  expect(await hay(ui, { type: 'Text', text: /Detalle de la 9/ })).toBe(true)
  await ui.unmount()
})

test('Arriba: una descripción con párrafos se pinta en un texto por párrafo', async (...m) => {
  await preparar(m, { cola: [{ id: 9, texto: 'En curso', estado: 'en-curso', descripcion: 'Primer párrafo.\n\nSegundo párrafo.' }] })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'arriba:9' })
  expect(await hay(ui, { type: 'Text', text: /^Primer párrafo\.$/ })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /^Segundo párrafo\.$/ })).toBe(true)
  await ui.unmount()
})

test('Arriba: desplegados, los pasos van enteros, sin «…»', async (...m) => {
  const largo = 'Un paso en curso con un texto muy largo que no cabe en una sola línea del panel estrecho'
  await preparar(m, {
    cola: [{ id: 150, texto: 'En curso', estado: 'en-curso', pasos: [{ texto: largo, estado: 'en-curso' }, { texto: 'Otro', estado: 'pendiente' }] }],
  })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'arriba:150' })
  await ui.press({ key: 'pasos:arriba:150' })
  // Partido por palabras en varias líneas (los botones siguen a la última), sin perder nada.
  const t = ((await ui.findAll({ type: 'Text' })) as { children: unknown[] }[]).map(x => x.children.join('')).filter(x => x !== '' && largo.includes(x))
  expect(t.length > 1).toBe(true)
  for (const x of t) expect(x.includes('…')).toBe(false)
  expect(t.join(' ')).toBe(largo)
  await ui.unmount()
})

test('Arriba: todas las tareas en curso van enteras, también la segunda, sin «…»', async (...m) => {
  const larga = 'Una tarea en curso con un título muy largo que no cabe en una sola línea del panel'
  await preparar(m, {
    cola: [
      { id: 150, texto: 'Primera en curso', estado: 'en-curso' },
      { id: 144, texto: larga, estado: 'en-curso' },
    ],
  })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Box', text: /^144 Una tarea/ })).toBe(true)
  const t = (await ui.findAll({ type: 'Text', text: /^Una tarea/ })).map(x => String((x as { text?: unknown }).text))
  expect(t.length > 0).toBe(true)
  for (const x of t) expect(x).toBe(larga)
  await ui.unmount()
})

// Eliminar una tarea (decisión del propietario, 2026-10-29): E roja en las en cola o en curso sin rama.
const ELIMINABLES: Pet[] = [
  { id: 1, texto: 'Panel lateral', estado: 'en-curso' },
  { id: 6, texto: 'En curso con rama', estado: 'en-curso', rama: 'feature/6-algo' },
  { id: 7, texto: 'En cola sin empezar', estado: 'en-cola' },
  { id: 8, texto: 'En cola con rama', estado: 'en-cola', rama: 'feature/8-otra' },
  { id: 2, texto: 'Secciones plegables', estado: 'en-observacion', prueba: 'pulsar la cabecera' },
]
const idsCola = (archivos: Record<string, string>) =>
  (JSON.parse(archivos[COLA] ?? '{}') as { peticiones: { id: number }[] }).peticiones.map(x => x.id)
const estadoEnCola = (archivos: Record<string, string>, id: number) =>
  (JSON.parse(archivos[COLA] ?? '{}') as { peticiones: Pet[] }).peticiones.find(x => x.id === id)?.estado
const confirmando = /^ ¿Eliminar\? sí $/

test('Eliminar: E solo en las en cola o en curso sin rama; las en curso, arriba', async (...m) => {
  await preparar(m, { desplegadas: true, cola: ELIMINABLES, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  for (const k of ['cola:7', 'arriba:1']) expect(await hay(ui, { type: 'Button', key: `eliminar-tarea:${k}` })).toBe(true)
  for (const k of ['cola:1', 'cola:8', 'arriba:6', 'observacion:2']) expect(await ui.find({ type: 'Button', key: `eliminar-tarea:${k}` })).toBe(undefined)
  await ui.unmount()
})

test('Eliminar: la en curso sin rama lleva la E también arriba', async (...m) => {
  await preparar(m, { desplegadas: true, cola: ELIMINABLES, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'eliminar-tarea:arriba:1' })).toBe(true)
  expect(await ui.find({ type: 'Button', key: 'eliminar-tarea:arriba:6' })).toBe(undefined)
  // Desde arriba también se elimina, con dos clics.
  await ui.press({ key: 'eliminar-tarea:arriba:1' })
  await ui.press({ key: 'eliminar-tarea:arriba:1' })
  expect(await ui.find({ type: 'Text', text: /Panel lateral/ })).toBe(undefined)
  await ui.unmount()
})

test('Eliminar: el primer clic pide confirmar; un clic en otro sitio o 5 s lo dejan como estaba', async (...m) => {
  const { archivos, reloj } = await preparar(m, { desplegadas: true, cola: ELIMINABLES, reloj: true })
  const antes = archivos[COLA]
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'eliminar-tarea:cola:7' })
  expect(archivos[COLA]).toBe(antes)
  expect(await hay(ui, { type: 'Text', text: confirmando })).toBe(true)
  await ui.press({ key: 'sec:hecho' })
  expect(await ui.find({ type: 'Text', text: confirmando })).toBe(undefined)
  // Otra vez, y se espera: a los 5 s vuelve a ser una E.
  await ui.press({ key: 'eliminar-tarea:cola:7' })
  await reloj!.advance(4000)
  expect(await hay(ui, { type: 'Text', text: confirmando })).toBe(true)
  await reloj!.advance(1500)
  expect(await ui.find({ type: 'Text', text: confirmando })).toBe(undefined)
  // Y el siguiente clic vuelve a pedir confirmación, sin eliminar.
  await ui.press({ key: 'eliminar-tarea:cola:7' })
  expect(archivos[COLA]).toBe(antes)
  await ui.unmount()
})

test('Eliminar: el segundo clic la quita de la cola y no entra en Cerradas', async (...m) => {
  const { archivos, cambiarCola, colas } = await preparar(m, { desplegadas: true, cola: ELIMINABLES, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // Una en cola y la en curso, con dos clics cada una.
  for (const k of ['cola:7', 'arriba:1']) {
    await ui.press({ key: `eliminar-tarea:${k}` })
    await ui.press({ key: `eliminar-tarea:${k}` })
  }
  expect(colas).toEqual(['eliminar 7', 'eliminar 1'])
  expect(idsCola(archivos)).toEqual([6, 8, 2])
  // Su historial queda en .sf/historial.jsonl, de donde se restaura.
  expect(eventosDe(archivos, 7)).toEqual(['eliminada'])
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  expect(await ui.find({ type: 'Text', text: /En cola sin empezar/ })).toBe(undefined)
  // Otra relectura de la cola tampoco la cierra.
  await cambiarCola((JSON.parse(archivos[COLA] ?? '{}') as { peticiones: Pet[] }).peticiones)
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  await ui.unmount()
})

test('Eliminar deshecha: la restaurada no es reabierta ni sale en Cerradas y conserva su color', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { desplegadas: true, cola: ELIMINABLES, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // La 10 entra en la sesión (en gris); la 7 ya estaba (en rojo).
  const nueva: Pet = { id: 10, texto: 'Nueva de la sesión', estado: 'en-cola', historial: [ev('creada', 'en-cola')] }
  await cambiarCola([...ELIMINABLES, nueva])
  // La 10 entra plegada: se despliega para ver su Eliminar.
  expect(await hay(ui, { type: 'Button', key: 'pet:cola:10' })).toBe(true)
  await ui.press({ key: 'pet:cola:10' })
  for (const id of [7, 10]) {
    await ui.press({ key: `eliminar-tarea:cola:${id}` })
    await ui.press({ key: `eliminar-tarea:cola:${id}` })
  }
  expect(idsCola(archivos)).toEqual([1, 6, 8, 2])
  // Se restauran (cola.py restaurar): vuelven a la cola con su historial.
  const restaurada = (p: Pet, creada: number) => ({ ...p, historial: [ev('creada', 'en-cola', creada), ev('eliminada', 'en-cola', 1), ev('restaurada', 'en-cola', 2)] })
  await cambiarCola([...ELIMINABLES.map(p => (p.id === 7 ? restaurada(p, ANTES) : p)), restaurada(nueva, 0)])
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  if (!(await hay(ui, { type: 'Text', text: /Nueva de la sesión/ }))) await ui.press({ key: 'sec:cola' })
  expect(await colores(ui, 7)).toEqual([GRIS])
  expect(await colores(ui, 10)).toEqual([GRIS])
  await ui.unmount()
})

test('Eliminar: si entretanto le han puesto rama, no la elimina', async (...m) => {
  const { archivos } = await preparar(m, { desplegadas: true, cola: ELIMINABLES, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'eliminar-tarea:cola:7' })
  archivos[COLA] = JSON.stringify({ peticiones: ELIMINABLES.map(p => (p.id === 7 ? { ...p, rama: 'feature/7-x' } : p)) })
  await ui.press({ key: 'eliminar-tarea:cola:7' })
  expect(idsCola(archivos)).toEqual([1, 6, 7, 8, 2])
  await ui.unmount()
})

// A propuesta (tarea 243): en Pendientes, en las en cola sin rama, solo si la SF tiene sus propuestas.
const confirmandoPropuesta = /^ ¿A propuesta\? sí $/
test('A propuesta: solo en las en cola sin rama, y solo con propuestas.md', async (...m) => {
  await preparar(m, { desplegadas: true, cola: ELIMINABLES, reloj: true, extra: { [PROPUESTAS]: PROPUESTAS_EJ } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'propuesta-tarea:cola:7', text: /^ A propuesta $/ })).toBe(true)
  for (const k of ['cola:8', 'arriba:1', 'arriba:6', 'observacion:2']) expect(await ui.find({ type: 'Button', key: `propuesta-tarea:${k}` })).toBe(undefined)
  await ui.unmount()
})

test('A propuesta: sin propuestas.md no sale', async (...m) => {
  await preparar(m, { desplegadas: true, cola: ELIMINABLES, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'eliminar-tarea:cola:7' })).toBe(true)
  expect(await ui.find({ type: 'Button', key: 'propuesta-tarea:cola:7' })).toBe(undefined)
  await ui.unmount()
})

test('A propuesta: el primer clic pide confirmar; el segundo lanza cola.py a-propuesta y la saca, sin Claude', async (...m) => {
  const { archivos, colas, toasts, prompts } = await preparar(m, { desplegadas: true, cola: ELIMINABLES, reloj: true, extra: { [PROPUESTAS]: PROPUESTAS_EJ } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'propuesta-tarea:cola:7' })
  expect(colas).toEqual([])
  expect(await hay(ui, { type: 'Text', text: confirmandoPropuesta })).toBe(true)
  await ui.press({ key: 'propuesta-tarea:cola:7' })
  expect(colas).toEqual(['a-propuesta 7'])
  expect(idsCola(archivos)).toEqual([1, 6, 8, 2])
  expect(eventosDe(archivos, 7)).toEqual(['a-propuesta'])
  expect(toasts).toContain('La 7, a propuesta: nueva propuesta P09; sale de la cola.')
  expect(prompts).toHaveLength(0)
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  await ui.unmount()
})

test('A propuesta: si entretanto le han puesto rama, no la pasa', async (...m) => {
  const { archivos, colas } = await preparar(m, { desplegadas: true, cola: ELIMINABLES, reloj: true, extra: { [PROPUESTAS]: PROPUESTAS_EJ } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'propuesta-tarea:cola:7' })
  archivos[COLA] = JSON.stringify({ peticiones: ELIMINABLES.map(p => (p.id === 7 ? { ...p, rama: 'feature/7-x' } : p)) })
  await ui.press({ key: 'propuesta-tarea:cola:7' })
  expect(colas).toEqual([])
  expect(idsCola(archivos)).toEqual([1, 6, 7, 8, 2])
  await ui.unmount()
})

// La rama activa en la cabecera y la de cada tarea al desplegarla (decisión del propietario, 2026-10-29).
const CON_RAMAS: Pet[] = [
  { id: 1, texto: 'Panel lateral', estado: 'en-curso', rama: 'feature/1-panel' },
  { id: 2, texto: 'Secciones plegables', estado: 'en-observacion', rama: 'feature/2-borrada' },
  { id: 7, texto: 'En cola sin empezar', estado: 'en-cola' },
]
// Un panel ancho, para que la rama quepa entera.
const ANCHO = { ...PANEL, props: { ...PANEL.props, bodyColumns: 70 } }
const GIT = (head: string) => ({
  '/sf/.git/HEAD': head,
  '/sf/.git/refs/heads/develop': 'abc',
  '/sf/.git/packed-refs': '# pack-refs\nabc1234 refs/heads/feature/1-panel\n',
})

test('Rama: la activa, atenuada en la cabecera', async (...m) => {
  await preparar(m, { extra: GIT('ref: refs/heads/develop\n') })
  // Ancho: con el modo prueba activo en la sesión que corre las pruebas, la etiqueta «prueba» le quita sitio.
  const ui = await m[0].ui.mount({ ...ANCHO, surface: 'terminal' })
  const t = await ui.find({ type: 'Text', text: /^ ?develop ?$/ })
  expect(t !== undefined).toBe(true)
  expect(conAmarillo(t)).toBe(false)
  await ui.unmount()
})

test('Rama: la de una tarea en curso, en amarillo; una cabeza separada, su commit corto', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { cola: CON_RAMAS, extra: GIT('ref: refs/heads/feature/1-panel\n') })
  const ui = await m[0].ui.mount({ ...ANCHO, surface: 'terminal' })
  expect(conAmarillo(await ui.find({ type: 'Text', text: /^ ?feature\/1-panel ?$/ }))).toBe(true)
  archivos['/sf/.git/HEAD'] = '0123456789abcdef0123456789abcdef01234567\n'
  await cambiarCola(CON_RAMAS)
  expect(await hay(ui, { type: 'Text', text: /^ ?\(0123456\) ?$/ })).toBe(true)
  await ui.unmount()
})

test('Rama: sin .git, nada', async (...m) => {
  await preparar(m, { cola: CON_RAMAS })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await ui.find({ type: 'Text', text: /^ ?feature\/1-panel ?$/ })).toBe(undefined)
  await ui.unmount()
})

test('Rama: sin SF no se muestra aunque haya .git', async (...m) => {
  await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await ui.find({ type: 'Text', text: /^ ?develop ?$/ })).toBe(undefined)
  await ui.unmount()
})

test('Rama: en un worktree, .git es un archivo que apunta a su HEAD', async (...m) => {
  await preparar(m, {
    cola: CON_RAMAS,
    extra: {
      '/sf/.git': 'gitdir: /repo/.git/worktrees/w\n',
      '/repo/.git/worktrees/w/HEAD': 'ref: refs/heads/feature/2-borrada\n',
      '/repo/.git/worktrees/w/commondir': '../..\n',
      '/repo/.git/refs/heads/feature/1-panel': 'abc',
    },
  })
  const ui = await m[0].ui.mount({ ...ANCHO, surface: 'terminal' })
  // La 2 está en observación: su rama, en amarillo.
  expect(conAmarillo(await ui.find({ type: 'Text', text: /^ ?feature\/2-borrada ?$/ }))).toBe(true)
  // Las ramas, en la carpeta común: la 1 existe y la 2 no.
  await ui.press({ key: 'arriba:1' })
  expect(await hay(ui, { type: 'Text', text: /^Rama: feature\/1-panel$/ })).toBe(true)
  await ui.press({ key: 'sec:observacion' })
  await ui.press({ key: 'pet:observacion:2' })
  expect(await hay(ui, { type: 'Text', text: /^Rama: feature\/2-borrada \(no existe\)$/ })).toBe(true)
  await ui.unmount()
})

test('Rama: desplegada, «Rama:» y « (no existe)» si no está; sin rama, sin línea', async (...m) => {
  await preparar(m, { cola: CON_RAMAS, extra: GIT('ref: refs/heads/develop\n') })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await ui.find({ type: 'Text', text: /^rama:/ })).toBe(undefined)
  // En packed-refs: existe. La en curso, arriba, una sola vez.
  await ui.press({ key: 'arriba:1' })
  expect((await ui.findAll({ type: 'Text', text: /^Rama: feature\/1-panel$/ })).length).toBe(1)
  // Ni en refs/heads ni en packed-refs: no existe.
  await ui.press({ key: 'sec:observacion' })
  await ui.press({ key: 'pet:observacion:2' })
  expect(await hay(ui, { type: 'Text', text: /^Rama: feature\/2-borrada \(no existe\)$/ })).toBe(true)
  // La 7, sin rama, se despliega por su menú (Eliminar), pero sin línea de rama (decisión 168).
  const ramas = (await ui.findAll({ type: 'Text', text: /^Rama:/ })).length
  await ui.press({ key: 'pet:cola:7' })
  expect(await hay(ui, { type: 'Button', key: 'eliminar-tarea:cola:7' })).toBe(true)
  expect((await ui.findAll({ type: 'Text', text: /^Rama:/ })).length).toBe(ramas)
  await ui.unmount()
})

test('Rama: en un panel estrecho se recorta por el final', async (...m) => {
  await preparar(m, { cola: CON_RAMAS, extra: GIT('ref: refs/heads/feature/1-panel-con-un-nombre-que-no-cabe-en-el-panel\n') })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // Sola en la tercera fila (tarea 260): se recorta al ancho del panel.
  const t = await ui.find({ type: 'Text', text: /^ ?feature\/1-.*… ?$/ })
  expect(t !== undefined).toBe(true)
  expect(conAmarillo(t)).toBe(false)
  expect(await hay(ui, { type: 'Text', text: /^ *SF 0\.32\.3 *$/ })).toBe(true)
  await ui.unmount()
})

// Cabecera fija (decisión del propietario, 2026-10-29): con scroll, la ventana del panel no se mueve; sube el cuerpo.
type Nodo = { type?: string; props?: Record<string, unknown>; children?: unknown }
const hijos = (n: Nodo): Nodo[] => {
  const c = n.children ?? n.props?.children
  return (Array.isArray(c) ? c : c ? [c] : []).filter((x): x is Nodo => typeof x === 'object' && x !== null)
}
const buscar = (n: Nodo, f: (n: Nodo) => boolean): Nodo | undefined => (f(n) ? n : hijos(n).map(h => buscar(h, f)).find(x => x))
const desplazado = (n: Nodo) => n.props?.position === 'relative'

test('Cabecera: fija al hacer scroll; el cuerpo sube bajo ella, hasta el final del panel', async (...m) => {
  const [$, on] = m
  // El motor no mueve la ventana: el panel responde sin pasar el scroll.
  let ventana = 0
  on('ui.scroll', () => {
    ventana++
    return {}
  })
  await preparar(m, { extra: GIT('ref: refs/heads/develop\n') })
  const ui = await $.ui.mount({ ...ANCHO, surface: 'terminal' })
  const scroll = (by: number) =>
    $.ui.scroll({ component: 'Pane', requestId: 'sf-estado', offset: 0, by, bodyRows: 40, contentRows: 100, origin: { kind: 'person' } })
  const cuerpo = async () => buscar((await ui.drawn()) as Nodo, desplazado)
  expect((await cuerpo())?.props?.top).toBe(0)
  await scroll(5)
  const c = await cuerpo()
  expect(c?.props?.top).toBe(-5)
  // La cabecera, fuera de lo que sube: la etiqueta de la SF, prompts y rama; las secciones, dentro.
  const enCuerpo = JSON.stringify(c)
  for (const t of ['SF 0.32.3', 'prompts', 'develop']) expect(enCuerpo.includes(t)).toBe(false)
  for (const t of ['SF 0.32.3', 'prompts', 'develop']) expect(JSON.stringify(await ui.drawn()).includes(t)).toBe(true)
  expect(enCuerpo.includes('PENDIENTES')).toBe(true)
  // Topes: arriba, 0; abajo, el alto del árbol menos la ventana.
  await scroll(1000)
  expect((await cuerpo())?.props?.top).toBe(-60)
  await scroll(-1000)
  expect((await cuerpo())?.props?.top).toBe(0)
  expect(ventana).toBe(0)
  await ui.unmount()
})

// Etiqueta de la cabecera (decisión del propietario, 2026-10-30): «SF» y la versión del plugin que corre, en lugar
// del nombre del proyecto, en todos los proyectos; sin versión legible, «SF» a secas.
test('Cabecera: la etiqueta dice SF y la versión del plugin, no el nombre del proyecto', async (...m) => {
  await preparar(m, { sinMarca: true, extra: { '/sf/.sf/proyecto.json': JSON.stringify({ sf: '0.30.0', proyecto: 'Demo', color: 'green' }) } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const etiqueta = await ui.find({ type: 'Text', text: /^ *SF 0\.32\.3 *$/ })
  expect(etiqueta !== undefined).toBe(true)
  expect(JSON.stringify(etiqueta)).toContain('#000000')
  expect(JSON.stringify(await ui.drawn()).includes('DEMO')).toBe(false)
  await ui.unmount()
})

test('Cabecera: sin SF en el proyecto, la etiqueta sigue diciendo la versión del plugin', async (...m) => {
  await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Text', text: /^ *SF 0\.32\.3 *$/ })).toBe(true)
  // Sin la línea gris «sin SF» (decisión 166): lo dice la bienvenida (tarea 289).
  expect(await hay(ui, { type: 'Text', text: / incorpora este proyecto a la SF / })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /^sin SF$/ })).toBe(false)
  await ui.unmount()
})

test('Cabecera: sin versión legible del plugin, SF a secas', async (...m) => {
  await preparar(m, { extra: { '/plugin/plugin.json': '{' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Text', text: /^ *SF *$/ })).toBe(true)
  await ui.unmount()
})

// Cabecera en dos filas (decisión del propietario, 2026-10-29): arriba, los prompts y, a la derecha, TURBO, el modo
// prueba y la etiqueta de la SF; abajo, la duración a la izquierda y la rama a la derecha.
const todos = (n: Nodo, f: (n: Nodo) => boolean): Nodo[] => [...(f(n) ? [n] : []), ...hijos(n).flatMap(h => todos(h, f))]
const fila = (raiz: Nodo, ...textos: string[]) =>
  todos(raiz, n => n.props?.flexDirection === 'row' && textos.every(t => JSON.stringify(n).includes(t))).sort(
    (a, b) => JSON.stringify(a).length - JSON.stringify(b).length,
  )[0]
const AJUSTES_PRUEBA = {
  extraKnownMarketplaces: { 'softwarefactory-dev': {} },
  enabledPlugins: { 'sf@softwarefactory-dev': true, 'sf@softwarefactory': false },
}

test('Cabecera: fila 1, RELEASE, TURBO y prueba a la izquierda y la etiqueta de la SF a la derecha; fila 2, duración y prompts; fila 3, la rama a la izquierda', async (...m) => {
  await preparar(m, { extra: { ...GIT('ref: refs/heads/develop\n'), [AJUSTES]: JSON.stringify(AJUSTES_PRUEBA) } })
  const ui = await m[0].ui.mount({ ...ANCHO, surface: 'terminal' })
  const raiz = (await ui.drawn()) as Nodo
  const f1 = fila(raiz, ' TURBO ', 'SF 0.32.3')
  expect(f1 !== undefined).toBe(true)
  const t1 = JSON.stringify(f1)
  const prueba = Math.max(t1.indexOf(' PRUEBA '), t1.indexOf('prueba'))
  expect(t1.indexOf(' TURBO ') < prueba).toBe(true)
  expect(prueba < t1.indexOf('SF 0.32.3')).toBe(true)
  // Antes de la etiqueta, una caja vacía que crece: los botones quedan a la izquierda y la etiqueta a la derecha.
  const h1 = hijos(f1!)
  expect(h1.at(-2)?.props?.flexGrow).toBe(1)
  expect(JSON.stringify(h1[0]).includes(' RELEASE ')).toBe(true)
  expect(JSON.stringify(h1.at(-1)).includes('SF 0.32.3')).toBe(true)
  expect(t1.includes('prompts') || t1.includes('develop') || t1.includes(' 0m ')).toBe(false)
  // Fila 2: la duración y los prompts, en la caja que crece, sin la rama.
  const f2 = fila(raiz, ' 0m ', 'prompts')
  expect(f2 !== undefined).toBe(true)
  const ti = JSON.stringify(f2)
  expect(ti.indexOf(' 0m ') < ti.indexOf('prompts')).toBe(true)
  expect(f2?.props?.flexGrow).toBe(1)
  expect(JSON.stringify(f2).includes('develop')).toBe(false)
  // Fila 3 (tarea 260): la rama, sola, a la izquierda: su fila no lleva caja que crezca delante.
  const f3 = todos(raiz, n => n.props?.flexDirection === 'row' && JSON.stringify(n).includes('develop') && !JSON.stringify(n).includes('prompts')).sort(
    (a, b) => JSON.stringify(b).length - JSON.stringify(a).length,
  )[0]
  expect(f3 !== undefined).toBe(true)
  expect(JSON.stringify(f3).includes('TURBO')).toBe(false)
  expect(hijos(f3!).length).toBe(1)
  expect(hijos(f3!)[0]?.props?.flexGrow).toBe(undefined)
  await ui.unmount()
})

// Etiquetas de la cabecera del mismo ancho, salvo la rama (tarea 260): el de « ACTUALIZAR » («todos del tamaño de
// actualizar»); «N prompts» se come su relleno hasta 9999; lo más largo crece. En un panel estrecho, lo que quepa
// comiéndose el relleno, sin bajar del texto más largo; si no, cada una el suyo.
test('Cabecera: el ancho común es el de ACTUALIZAR, crece lo más largo y se reduce a lo que cabe, o se deja', () => {
  expect(ANCHO_ETIQUETA).toBe(' ACTUALIZAR '.length)
  // Lo que necesita cada una como mínimo: su texto.
  const filas = (f1: string[], prompts = '138 prompts') => [
    { necesita: f1.map(t => t.length), reserva: 0 },
    { necesita: ['4h 36m'.length, prompts.length], reserva: 0 },
  ]
  const f1 = ['RELEASE', 'TURBO', 'PRUEBA', 'SF 1.3.0']
  // Cuatro de 12 y tres separaciones: 51.
  expect(anchoComun(80, filas(f1))).toBe(12)
  expect(anchoComun(51, filas(f1))).toBe(12)
  // Algo más estrecho: el común baja, sin quedarse por debajo de «138 prompts» (11): 4×11 + 3 = 47.
  expect(anchoComun(50, filas(f1))).toBe(11)
  expect(anchoComun(47, filas(f1))).toBe(11)
  expect(anchoComun(46, filas(f1))).toBe(null)
  // «9999 prompts», 12, cabe en 12; «12345 prompts» crece.
  expect(anchoComun(51, filas(f1, '9999 prompts'))).toBe(12)
  expect(anchoComun(51, filas(f1, '12345 prompts'))).toBe(12)
  // Con ACTUALIZAR, cinco en la primera fila: 64 columnas a 12. En el panel real de unas 60 (59 útiles), a 11, con
  // ACTUALIZAR casi sin relleno, en vez de volver cada una a su ancho, que es lo que vio el propietario. Con «138
  // prompts» (11) no baja de 11; con dos cifras, hasta 10, el texto de ACTUALIZAR: 54.
  expect(anchoComun(64, filas(['ACTUALIZAR', ...f1]))).toBe(12)
  expect(anchoComun(59, filas(['ACTUALIZAR', ...f1]))).toBe(11)
  expect(anchoComun(58, filas(['ACTUALIZAR', ...f1]))).toBe(null)
  expect(anchoComun(54, filas(['ACTUALIZAR', ...f1], '38 prompts'))).toBe(10)
  expect(anchoComun(53, filas(['ACTUALIZAR', ...f1], '38 prompts'))).toBe(null)
  expect(centrar('TURBO', 12)).toBe('   TURBO    ')
  expect(centrar('ACTUALIZAR', 12)).toBe(' ACTUALIZAR ')
})

// Lo que el terminal pinta de una etiqueta: el texto de sus Text, letra a letra (el kit no pinta; en la cabecera no hay
// letras anchas). Las etiquetas llevan su relleno dentro del texto, así que esto es su ancho en pantalla.
const pintado = (n: Nodo): string => {
  const c = n.children ?? n.props?.children
  return (Array.isArray(c) ? c : c === undefined || c === null ? [] : [c]).map(x => (typeof x === 'string' ? x : typeof x === 'object' && x ? pintado(x as Nodo) : '')).join('')
}
// La etiqueta de la cabecera que contiene t: la caja más interior que no se encoge.
const etiquetaCon = (r: Nodo, t: string) =>
  todos(r, n => n.type === 'Box' && n.props?.flexShrink === 0 && JSON.stringify(n).includes(t)).sort(
    (a, b) => JSON.stringify(a).length - JSON.stringify(b).length,
  )[0]

test('Cabecera: en un panel ancho, todas las etiquetas pintan el ancho de ACTUALIZAR, centradas, salvo la rama; en uno estrecho, cada una el suyo', async (...m) => {
  await preparar(m, { extra: { ...GIT('ref: refs/heads/develop\n'), [AJUSTES]: JSON.stringify(AJUSTES_PRUEBA) } })
  // Unas 80 columnas, como el panel en que lo probó el propietario.
  const ui = await m[0].ui.mount({ ...PANEL, props: { ...PANEL.props, bodyColumns: 80 }, surface: 'terminal' })
  const raiz = (await ui.drawn()) as Nodo
  // El modo prueba, por la clave de su botón: «PRUEBA» o «prueba», según de dónde venga el panel.
  for (const t of ['RELEASE', 'TURBO', 'modo-prueba', 'SF 0.32.3', '0m', 'prompts']) {
    const c = etiquetaCon(raiz, t)
    expect([t, pintado(c!).length, c?.props?.width]).toEqual([t, ANCHO_ETIQUETA, ANCHO_ETIQUETA])
  }
  expect(pintado(etiquetaCon(raiz, 'TURBO')!)).toBe('   TURBO    ')
  // La rama, con el suyo: su nombre y un espacio a cada lado, sin ancho fijado.
  const rama = (await ui.find({ type: 'Text', text: /^ ?develop ?$/ })) as { text?: string } | undefined
  expect(rama?.text).toBe(' develop ')
  for (const c of todos(raiz, n => n.type === 'Box' && JSON.stringify(n).includes('develop') && !JSON.stringify(n).includes('prompts'))) {
    expect(c.props?.width).toBe(undefined)
  }
  await ui.unmount()
  // En el panel estrecho de 38 columnas, con PRUEBA, no caben cuatro iguales: cada una, con su ancho, en una sola línea.
  const estrecho = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const r2 = (await estrecho.drawn()) as Nodo
  expect(pintado(etiquetaCon(r2, 'TURBO')!)).toBe(' TURBO ')
  expect(pintado(etiquetaCon(r2, 'RELEASE')!)).toBe(' RELEASE ')
  expect(await hay(estrecho, { type: 'Text', text: /^ ?develop ?$/ })).toBe(true)
  await estrecho.unmount()
})

test('Cabecera: con tres cifras de prompts, su etiqueta sigue del ancho de ACTUALIZAR, comiéndose el relleno', async (...m) => {
  await preparar(m, { extra: GIT('ref: refs/heads/develop\n') })
  for (let i = 0; i < 100; i++) await m[0].prompt.submit({ text: 'hola', origin: { kind: 'composer' }, wait: false })
  const ui = await m[0].ui.mount({ ...PANEL, props: { ...PANEL.props, bodyColumns: 80 }, surface: 'terminal' })
  const c = etiquetaCon((await ui.drawn()) as Nodo, 'prompts')
  expect(pintado(c!)).toBe('100 prompts ')
  expect(pintado(c!).length).toBe(ANCHO_ETIQUETA)
  await ui.unmount()
})

// TURBO («TURBO pone en curso las tareas que no necesitan al propietario», 160): pasa a Claude que ponga en curso,
// con su subagente, las de la cola que no necesitan al propietario y lance el de las en curso que no lo tienen.
test('TURBO: sale en la SF y, al pulsarlo, el prompt llega tras el temporizador, con un toast', async (...m) => {
  const { prompts, toasts, reloj } = await preparar(m, { reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'turbo' })).toBe(true)
  await ui.press({ key: 'turbo' })
  expect(prompts).toHaveLength(0)
  expect(toasts.some(t => t.startsWith('TURBO'))).toBe(true)
  await reloj!.advance(100)
  expect(prompts).toHaveLength(1)
  expect(prompts[0]).toContain('TURBO: pon en curso, cada una con su subagente, las tareas de la cola')
  expect(prompts[0]).toContain('sin interactuar con el propietario')
  expect(prompts[0]).toContain('el subagente de las tareas en curso que aún no lo tienen')
  await ui.unmount()
})

test('TURBO: sale en un proyecto con SF', async (...m) => {
  await preparar(m, { sinMarca: true, extra: { '/sf/.sf/proyecto.json': JSON.stringify({ sf: '0.32.3', proyecto: 'Demo' }) } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'turbo' })).toBe(true)
  await ui.unmount()
})

test('TURBO: fuera de un proyecto con SF no sale', async (...m) => {
  await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await ui.find({ type: 'Button', key: 'turbo' })).toBe(undefined)
  // Sin la línea gris «sin SF» (decisión 166): lo dice la bienvenida (tarea 289).
  expect(await hay(ui, { type: 'Text', text: / incorpora este proyecto a la SF / })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /^sin SF$/ })).toBe(false)
  await ui.unmount()
})

// Descartar una tarea (decisión del propietario, 2026-10-29): D en las que tienen rama, en cola o en curso; en
// En observación ya entró en develop y va la R (decisión 115). El panel lo pide a cola.py descartar, sin Claude («Comandos
// antes que inferencia»): borra la rama y la pasa a `descartada`. Lo de git lo prueba test_cola.py.
const DESCARTABLES: Pet[] = [
  ...ELIMINABLES,
  { id: 9, texto: 'En observación con rama', estado: 'en-observacion', rama: 'feature/9-prueba', prueba: 'mirar' },
]
const descartando = /^ ¿Descartar\? sí $/
const descartar = (ids: number[]) =>
  DESCARTABLES.map(p => (ids.includes(p.id as number) ? { ...p, estado: 'descartada', historial: [ev('descartada', p.rama as string)] } : p))

test('Descartar: D solo en las que tienen rama, en Pendientes y arriba; en observación, no', async (...m) => {
  await preparar(m, { desplegadas: true, cola: DESCARTABLES, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'sec:observacion' })
  for (const k of ['cola:8', 'arriba:6']) expect(await hay(ui, { type: 'Button', key: `descartar-tarea:${k}` })).toBe(true)
  for (const k of ['cola:6', 'cola:7', 'arriba:1', 'observacion:2', 'observacion:9']) expect(await ui.find({ type: 'Button', key: `descartar-tarea:${k}` })).toBe(undefined)
  // Una tarea con rama no lleva la E.
  for (const k of ['arriba:6', 'cola:8']) expect(await ui.find({ type: 'Button', key: `eliminar-tarea:${k}` })).toBe(undefined)
  await ui.unmount()
})

test('Descartar: el primer clic pide confirmar; el segundo la pide a cola.py y entra en Cerradas, sin Claude', async (...m) => {
  const { archivos, prompts, ordenes, colas, toasts, reloj } = await preparar(m, {
    desplegadas: true,
    cola: DESCARTABLES,
    reloj: true,
    extra: { '/sf/.git/HEAD': 'ref: refs/heads/develop\n', '/sf/.git/refs/heads/feature/8-otra': 'abc' },
  })
  const antes = archivos[COLA]
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'descartar-tarea:cola:8' })
  expect(await hay(ui, { type: 'Text', text: descartando })).toBe(true)
  // Otro botón lo deja como estaba; y a los 5 s, también.
  await ui.press({ key: 'sec:hecho' })
  expect(await ui.find({ type: 'Text', text: descartando })).toBe(undefined)
  await ui.press({ key: 'descartar-tarea:cola:8' })
  await reloj!.advance(5500)
  expect(await ui.find({ type: 'Text', text: descartando })).toBe(undefined)
  expect(archivos[COLA]).toBe(antes)
  expect(colas).toEqual([])
  // Con dos clics seguidos: cola.py descartar, y el panel no ejecuta git por su cuenta.
  await ui.press({ key: 'descartar-tarea:cola:8' })
  await ui.press({ key: 'descartar-tarea:cola:8' })
  await reloj!.advance(100)
  expect(colas).toEqual(['descartar 8'])
  expect(ordenes.some(o => o.startsWith('git switch') || o.startsWith('git branch'))).toBe(false)
  expect(estadoEnCola(archivos, 8)).toBe('descartada')
  expect(eventosDe(archivos, 8)).toEqual(['descartada'])
  expect(toasts).toContain('Descartada la 8: rama feature/8-otra borrada.')
  expect(prompts).toHaveLength(0)
  // Cerradas, plegada por el clic de antes en su cabecera, la cuenta descartada.
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+1$/ })).toBe(true)
  await ui.unmount()
})

// Pulsa la D de la 6 (en curso, con rama) dos veces seguidas; cola.py responde `respuesta`.
const descartarLa6 = async (m: Motor, respuesta: Respuesta) => {
  const r = await preparar(m, {
    desplegadas: true,
    cola: DESCARTABLES,
    reloj: true,
    extra: { '/sf/.git/HEAD': 'ref: refs/heads/feature/6-algo\n', '/sf/.git/refs/heads/feature/6-algo': 'abc' },
    respuestas: { descartar: respuesta },
  })
  const antes = r.archivos[COLA]
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'descartar-tarea:arriba:6' })
  await ui.press({ key: 'descartar-tarea:arriba:6' })
  await ui.unmount()
  return { ...r, antes }
}

test('Descartar: si cola.py no puede (cambios sin commit, la rama en otro worktree), dice por qué y no toca la cola', async (...m) => {
  const mensaje = 'La rama feature/6-algo está en el worktree /sf/.claude/worktrees/agent-1. Para ese agente y quita el worktree antes.'
  const { archivos, antes, colas, marcados } = await descartarLa6(m, { ok: false, mensaje })
  expect(colas).toEqual(['descartar 6'])
  expect(archivos[COLA]).toBe(antes)
  // Un error: marca roja y la ruta del worktree, abreviada (tarea 257).
  expect(marcados.map(t => t.text)).toContain('🟥 D: La rama feature/6-algo está en el worktree agent-1. Para ese agente y quita el worktree antes.')
})

test('Descartar: si la tarea ha cambiado en la cola, no llama a cola.py', async (...m) => {
  const { archivos, colas, toasts } = await preparar(m, { desplegadas: true, cola: DESCARTABLES, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'descartar-tarea:arriba:6' })
  archivos[COLA] = JSON.stringify({ peticiones: DESCARTABLES.map(p => (p.id === 6 ? { ...p, rama: null } : p)) })
  await ui.press({ key: 'descartar-tarea:arriba:6' })
  expect(colas).toEqual([])
  expect(toasts).toContain('La 6 ya no se puede descartar: ha cambiado en la cola.')
  await ui.unmount()
})

test('Descartar: la descartada sale de Pendientes y de En observación y entra en Cerradas, en gris', async (...m) => {
  const { cambiarCola } = await preparar(m, { cola: DESCARTABLES, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', text: /PENDIENTES [▸▾]\s+2$/ })).toBe(true)
  await cambiarCola(descartar([8, 9]))
  expect(await hay(ui, { type: 'Button', text: /PENDIENTES [▸▾]\s+1$/ })).toBe(true)
  expect(await hay(ui, { type: 'Button', text: /EN OBSERVACIÓN [▸▾]\s+1/ })).toBe(true)
  expect(await colores(ui, 8)).toEqual([GRIS])
  expect(await colores(ui, 9)).toEqual([GRIS])
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+2$/ })).toBe(true)
  await ui.unmount()
})

test('Descartar: el botón de Cerradas limpia las descartadas con cola.py y siguen fuera de la lista', async (...m) => {
  const { archivos, cambiarCola, colas } = await preparar(m, { cola: DESCARTABLES, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await cambiarCola(descartar([8]))
  expect(await hay(ui, { type: 'Text', text: /Limpiar \(1\)/ })).toBe(true)
  await ui.press({ key: 'limpiar-cerradas' })
  await ui.press({ key: 'limpiar-cerradas' })
  expect(colas).toEqual(['limpiar'])
  expect(idsCola(archivos)).toEqual([1, 6, 7, 2, 9])
  expect(eventosDe(archivos, 8)).toEqual(['descartada', 'limpiada'])
  expect(await conNumero(ui, 8)).toBe(false)
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  // Otra relectura no la devuelve.
  await m[0].tool.call({ tool: 'Bash', command: 'true' })
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  await ui.unmount()
})

test('Descartar: al empezar la sesión, las descartadas de otra salen de la cola con cola.py limpiar, sin entrar en Cerradas', async (...m) => {
  const { archivos, colas } = await preparar(m, { cola: DESCARTABLES.map(p => (p.id === 8 ? { ...p, estado: 'descartada', historial: [ev('descartada', 'feature/8-otra', ANTES)] } : p)) })
  expect(colas).toEqual(['limpiar'])
  expect(idsCola(archivos)).toEqual([1, 6, 7, 2, 9])
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  await ui.unmount()
})

test('Descartar: sin descartadas, al empezar no llama a cola.py; al recargar el plugin, tampoco limpia', async (...m) => {
  const { colas, cambiarCola } = await preparar(m, { cola: DESCARTABLES })
  expect(colas).toEqual([])
  // Descartada en la sesión y /reload-plugins: vuelve a empezar el módulo, no la sesión; sigue en Cerradas.
  await cambiarCola(descartar([8]))
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  expect(colas).toEqual([])
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await conNumero(ui, 8)).toBe(true)
  await ui.unmount()
})

// Probar una tarea en su rama (decisión del propietario, 2026-10-29): T verde delante de la D, si la rama existe y
// no es la activa. Un clic, sin confirmar: el panel lo pide a cola.py probar, sin Claude.
// Existen las ramas de la 6 y la 9; la de la 8, no.
const RAMAS_PROBAR = {
  '/sf/.git/refs/heads/develop': 'abc',
  '/sf/.git/refs/heads/feature/6-algo': 'abc',
  '/sf/.git/refs/heads/feature/9-prueba': 'abc',
}

test('Probar: T en las que tienen rama existente y no activa, en Pendientes, arriba y en observación', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { desplegadas: true, cola: DESCARTABLES, extra: { ...RAMAS_PROBAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'sec:observacion' })
  for (const k of ['arriba:6', 'observacion:9']) expect(await hay(ui, { type: 'Button', key: `probar-tarea:${k}` })).toBe(true)
  // La etiqueta Activar rama, no Activar rama de antes (decisión 168).
  expect((await ui.findAll({ type: 'Text', text: /^ Activar rama $/ })).length).toBe(2)
  expect(await ui.find({ type: 'Text', text: /^ T$/ })).toBe(undefined)
  // Sin rama (1, 7, 2) o con una rama que no existe (8), sin T; la 6, en curso, no sale en Pendientes.
  for (const k of ['cola:6', 'cola:7', 'cola:8', 'arriba:1', 'observacion:2']) expect(await ui.find({ type: 'Button', key: `probar-tarea:${k}` })).toBe(undefined)
  // Con la rama de la 6 activa, la 6 ya no lleva T; la 9, sí.
  archivos['/sf/.git/HEAD'] = 'ref: refs/heads/feature/6-algo\n'
  await cambiarCola(DESCARTABLES)
  for (const k of ['cola:6', 'arriba:6']) expect(await ui.find({ type: 'Button', key: `probar-tarea:${k}` })).toBe(undefined)
  expect(await hay(ui, { type: 'Button', key: 'probar-tarea:observacion:9' })).toBe(true)
  await ui.unmount()
})

test('Probar: un clic la pide a cola.py probar, sin Claude ni recargar; sin la rama, nada', async (...m) => {
  const { archivos, comandos, prompts, ordenes, colas, toasts } = await preparar(m, { desplegadas: true, cola: DESCARTABLES, extra: { ...RAMAS_PROBAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const recargasAntes = comandos.filter(c => c === 'reload-plugins').length
  await ui.press({ key: 'probar-tarea:arriba:6' })
  expect(colas).toEqual(['probar 6'])
  expect(ordenes.some(o => o.startsWith('git switch'))).toBe(false)
  expect(archivos['/sf/.git/HEAD']).toBe('ref: refs/heads/feature/6-algo\n')
  // La recarga queda a cargo del propietario.
  expect(comandos.filter(c => c === 'reload-plugins').length).toBe(recargasAntes)
  expect(toasts.some(t => t.startsWith('La 6, en prueba: rama feature/6-algo activa'))).toBe(true)
  expect(prompts).toHaveLength(0)
  expect(estadoEnCola(archivos, 6)).toBe('en-curso')
  expect(eventosDe(archivos, 6)).toEqual(['probar'])
  // Ya activa, la 6 pierde Activar rama.
  expect(await ui.find({ type: 'Button', key: 'probar-tarea:arriba:6' })).toBe(undefined)
  // Si entretanto ya no tiene esa rama, no llama a cola.py.
  archivos[COLA] = JSON.stringify({ peticiones: DESCARTABLES.map(p => (p.id === 9 ? { ...p, rama: null } : p)) })
  await ui.press({ key: 'sec:observacion' })
  await ui.press({ key: 'probar-tarea:observacion:9' })
  expect(colas).toEqual(['probar 6'])
  await ui.unmount()
})

const EXTRA_PROBAR = { ...RAMAS_PROBAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' }

test('Probar: una tarea en cola pasa a en curso', async (...m) => {
  const cola = DESCARTABLES.map(p => (p.id === 6 ? { ...p, estado: 'en-cola' } : p))
  const { archivos } = await preparar(m, { desplegadas: true, cola, extra: EXTRA_PROBAR })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'probar-tarea:cola:6' })
  const seis = (JSON.parse(archivos[COLA]) as { peticiones: Pet[] }).peticiones.find(p => p.id === 6)
  expect(seis?.estado).toBe('en-curso')
  await ui.unmount()
})

test('Probar: si cola.py no cambia de rama (cambios sin commit, otro worktree), dice por qué', async (...m) => {
  const mensaje = 'Hay cambios sin commit en la rama activa. Haz commit antes.'
  const a = await preparar(m, { desplegadas: true, cola: DESCARTABLES, extra: EXTRA_PROBAR, respuestas: { probar: { ok: false, mensaje } } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'probar-tarea:arriba:6' })
  expect(a.archivos['/sf/.git/HEAD']).toBe('ref: refs/heads/develop\n')
  expect(a.toasts).toContain(`Activar rama: ${mensaje}`)
  // Sin rama activa, no busca documentos ni abre nada.
  expect(a.ordenes.some(o => o.startsWith('git diff -z') || o.startsWith('xdg-open'))).toBe(false)
  await ui.unmount()
})

test('Probar: con choques al integrar develop, no activa y se lo pasa a Claude para que lo resuelva el subagente', async (...m) => {
  const probar = { ok: false, mensaje: 'No se activa', fallo: 'choques', motivo: 'choques al integrar develop en feature/6-algo: a.txt' }
  const a = await preparar(m, { desplegadas: true, cola: DESCARTABLES, extra: EXTRA_PROBAR, reloj: true, respuestas: { probar } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'probar-tarea:arriba:6' })
  expect(a.archivos['/sf/.git/HEAD']).toBe('ref: refs/heads/develop\n')
  expect(a.toasts).toContain('Choques al integrar develop en la 6: se lo paso a Claude.')
  expect(a.ordenes.some(o => o.startsWith('git diff -z'))).toBe(false)
  // Sale desde el temporizador, no desde el hook que atiende el panel.
  expect(a.prompts).toHaveLength(0)
  await a.reloj!.advance(100)
  expect(a.prompts).toHaveLength(1)
  const pedido = JSON.stringify(a.prompts[0])
  for (const x of ['Activa la rama de la 6', 'feature/6-algo: a.txt', 'integrando develop', '/.claude/sf/cola.py', ' probar 6`']) expect(pedido).toContain(x)
  await ui.unmount()
})

test('Probar: con trabajo del subagente sin traer, no activa y se lo pasa a Claude', async (...m) => {
  const probar = { ok: false, mensaje: 'No se activa', fallo: 'sin-traer', motivo: 'trabajo del subagente sin traer a feature/6-algo: sub-6 (2 commits)' }
  const a = await preparar(m, { desplegadas: true, cola: DESCARTABLES, extra: EXTRA_PROBAR, reloj: true, respuestas: { probar } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'probar-tarea:arriba:6' })
  expect(a.toasts).toContain('La 6 tiene trabajo del subagente sin traer: se lo paso a Claude.')
  await a.reloj!.advance(100)
  const pedido = JSON.stringify(a.prompts[0])
  for (const x of ['sub-6 (2 commits)', '--ff-only', ' probar 6`']) expect(pedido).toContain(x)
  await ui.unmount()
})

test('Probar: Activar rama abre en el navegador los .html que la rama cambia respecto a develop, todos', async (...m) => {
  const html = ['docs/vision.html', 'docs/specs/funcional/interfaz.html']
  const a = await preparar(m, { desplegadas: true, cola: DESCARTABLES, extra: EXTRA_PROBAR, git: { html } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'probar-tarea:arriba:6' })
  expect(a.ordenes).toContain("git diff -z --name-only --diff-filter=d develop...feature/6-algo -- *.html")
  // Tras activar la rama, uno por documento, con la ruta en la raíz.
  expect(a.ordenes.filter(o => o.startsWith('xdg-open'))).toEqual(html.map(x => `xdg-open ${RAIZ}/${x}`))
  expect(a.toasts.some(t => t.startsWith('La 6, en prueba: rama feature/6-algo activa') && t.endsWith(`Abiertos en el navegador: ${html.join(', ')}.`))).toBe(true)
  expect(a.prompts).toHaveLength(0)
  await ui.unmount()
})

test('Probar: sin .html en la rama, Activar rama hace lo de siempre', async (...m) => {
  const a = await preparar(m, { desplegadas: true, cola: DESCARTABLES, extra: EXTRA_PROBAR })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'probar-tarea:arriba:6' })
  expect(a.ordenes.some(o => /^(xdg-open|open|rundll32) /.test(o))).toBe(false)
  expect(a.toasts.some(t => t.startsWith('La 6, en prueba: rama feature/6-algo activa') && !t.includes('navegador'))).toBe(true)
  await ui.unmount()
})

test('Abrir archivos: en Windows, Activar rama abre con rundll32 y la ruta con barras invertidas', async (...m) => {
  const a = await preparar(m, { desplegadas: true, raiz: 'D:/sf', cola: DESCARTABLES, extra: EXTRA_PROBAR, git: { html: ['docs/a.html'] } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'probar-tarea:arriba:6' })
  expect(a.ordenes.filter(o => /^(xdg-open|open|rundll32) /.test(o))).toEqual([
    'rundll32 url.dll,FileProtocolHandler D:\\sf\\docs\\a.html',
  ])
  await ui.unmount()
})

test('Probar: sin xdg-open, Activar rama los abre con open', async (...m) => {
  const a = await preparar(m, { desplegadas: true, cola: DESCARTABLES, extra: EXTRA_PROBAR, git: { html: ['a.html'], sinAbridor: ['xdg-open'] } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'probar-tarea:arriba:6' })
  expect(a.ordenes).toContain(`open ${RAIZ}/a.html`)
  await ui.unmount()
})

test('Probar: si no hay con qué abrirlos, Activar rama lo dice y la rama queda activa', async (...m) => {
  const a = await preparar(m, { desplegadas: true, cola: DESCARTABLES, extra: EXTRA_PROBAR, git: { html: ['a.html'], sinAbridor: ['xdg-open', 'open'] } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'probar-tarea:arriba:6' })
  expect(a.archivos['/sf/.git/HEAD']).toBe('ref: refs/heads/feature/6-algo\n')
  expect(a.toasts.some(t => t.endsWith('No se ha podido abrir: a.html.'))).toBe(true)
  await ui.unmount()
})

test('Menú: Probar y Descartar van en la fila del menú; el título, entero en su línea, sin «…»', async (...m) => {
  const larga = 'Una tarea con un título muy largo que no cabe en el panel'
  const cola = DESCARTABLES.map(p => (p.id === 6 ? { ...p, texto: larga, estado: 'en-cola' } : p))
  await preparar(m, { desplegadas: true, cola, extra: { ...RAMAS_PROBAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'probar-tarea:cola:6' })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'descartar-tarea:cola:6' })).toBe(true)
  // El título, entero y partido con sangría colgante; las órdenes, debajo, en su menú.
  expect(await hay(ui, { type: 'Text', text: new RegExp(`^${larga}$`) })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /…/ })).toBe(false)
  await ui.unmount()
})

// Cerrar una tarea (decisión del propietario, 2026-10-29): C verde en las tareas en curso con rama que solo esperan
// cerrarse, o probarse y cerrarse; sin pasos, sin C. Dos clics; el segundo la pasa a develop por squash, sin Claude, y la saca de la cola.
const CERRABLES: Pet[] = [
  {
    id: 12,
    texto: 'Lista para cerrar',
    estado: 'en-curso',
    rama: 'feature/12-lista',
    pasos: [
      { texto: 'Hacer A', estado: 'hecho' },
      { texto: 'Probar la tarea', estado: 'pendiente' },
      { texto: 'Cerrar la tarea', estado: 'pendiente' },
    ],
  },
  {
    id: 13,
    texto: 'Con trabajo',
    estado: 'en-curso',
    rama: 'feature/13-x',
    pasos: [
      { texto: 'Hacer B', estado: 'en-curso' },
      { texto: 'Probar la tarea', estado: 'pendiente' },
    ],
  },
  { id: 14, texto: 'En cola con rama', estado: 'en-cola', rama: 'feature/14-y' },
  { id: 15, texto: 'Sin pasos', estado: 'en-curso', rama: 'feature/15-z' },
  {
    id: 16,
    texto: 'Sin mirar',
    estado: 'en-curso',
    rama: 'feature/16-w',
    pasos: [
      { texto: 'Hacer C', estado: 'hecho' },
      { texto: 'Cerrar la tarea', estado: 'pendiente' },
    ],
  },
  { id: 2, texto: 'Secciones plegables', estado: 'en-observacion', prueba: 'pulsar la cabecera' },
]
const RAMAS_CERRAR = Object.fromEntries(
  ['develop', 'feature/12-lista', 'feature/13-x', 'feature/14-y', 'feature/15-z', 'feature/16-w'].map(r => [`/sf/.git/refs/heads/${r}`, 'abc']),
)
const cerrando = /^ ¿Cerrar\? sí $/

test('Pasos: los de cierre no llevan la × (174)', async (...m) => {
  await preparar(m, { cola: CERRABLES, reloj: true, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  for (const k of ['arriba:12', 'pasos:arriba:12', 'arriba:13', 'pasos:arriba:13']) await ui.press({ key: k })
  for (const k of ['12:1', '12:2', '13:1']) expect(await ui.find({ type: 'Button', key: `quitar-paso:arriba:${k}` })).toBe(undefined)
  await ui.unmount()
})

test('Cerrar: C en las tareas en curso con rama y «Cerrar la tarea» como único paso por hacer, salvo «Probar»', async (...m) => {
  await preparar(m, { desplegadas: true, cola: CERRABLES, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // La 16, sin «Probar la tarea» (una cola de antes de la 174) y con «Cerrar la tarea»: se cierra.
  for (const k of ['arriba:12', 'arriba:16']) expect(await hay(ui, { type: 'Button', key: `cerrar-tarea:${k}` })).toBe(true)
  // La 15, sin pasos, no; y en Pendientes, ninguna: las en curso solo salen arriba.
  for (const k of ['arriba:13', 'cola:14', 'arriba:15', 'cola:12', 'cola:16']) expect(await ui.find({ type: 'Button', key: `cerrar-tarea:${k}` })).toBe(undefined)
  // Convive con la D.
  expect(await hay(ui, { type: 'Button', key: 'descartar-tarea:arriba:12' })).toBe(true)
  await ui.unmount()
})

// Ayudas de prueba (decisión 184): tras «Activar rama», con «(opcional)», fuera de la cuenta y sin exigirlas para la C.
test('Cerrar: las ayudas de prueba pendientes no quitan la C; se ven con «(opcional)» y no cuentan', async (...m) => {
  const cola: Pet[] = [
    {
      id: 17,
      texto: 'Con ayudas',
      estado: 'en-curso',
      rama: 'feature/17-v',
      pasos: [
        { texto: 'Hacer D', estado: 'hecho' },
        { texto: 'Activar rama para poder probar', estado: 'hecho' },
        { texto: 'Abrir el panel', estado: 'pendiente', ayuda: true },
        { texto: 'Cerrar la tarea', estado: 'pendiente' },
      ],
    },
  ]
  const extra = { '/sf/.git/refs/heads/develop': 'abc', '/sf/.git/refs/heads/feature/17-v': 'abc', '/sf/.git/HEAD': 'ref: refs/heads/develop\n' }
  await preparar(m, { desplegadas: true, cola, extra })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'cerrar-tarea:arriba:17' })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'pasos:arriba:17', text: /^Pasos 2\/3$/ })).toBe(true)
  await ui.press({ key: 'pasos:arriba:17' })
  expect(await hay(ui, { type: 'Text', text: /^Abrir el panel \(opcional\)$/ })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'quitar-paso:arriba:17:2' })).toBe(true)
  await ui.unmount()
})

// Con un subagente trabajando en la tarea, ⚙ verde (decisión 162) en lugar de Activar rama, la C, la D y la E (decisión del propietario,
// 2026-10-29): sale de $.agent.list(), por la descripción «Tarea NN: …», no de los worktrees. Pulsarlo solo avisa.
const EN_12 = (status = 'running'): Agente[] => [{ description: 'Tarea 12: cerrar la lista', status }]

test('Subagente: con uno trabajando en la 12, ⚙ delante y siguen Activar rama, la C y la D; pulsarlo solo avisa', async (...m) => {
  const a = await preparar(m, { desplegadas: true, cola: CERRABLES, agentes: EN_12(), extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  for (const k of ['arriba:12']) {
    expect(await hay(ui, { type: 'Button', key: `subagente-tarea:${k}` })).toBe(true)
    for (const b of ['probar', 'cerrar', 'descartar']) expect(await hay(ui, { type: 'Button', key: `${b}-tarea:${k}` })).toBe(true)
  }
  // La marca es ●, que toma el color en todos los terminales (la ⚙ sale como emoji gris en Windows Terminal), con
  // un espacio a cada lado: tres columnas, como reserva anchoBotones.
  expect(((await ui.find({ type: 'Button', key: 'subagente-tarea:arriba:12' })) as { text: string }).text).toBe(' ● ')
  // La 16, sin subagente, conserva Activar rama y la C.
  for (const b of ['probar', 'cerrar']) expect(await hay(ui, { type: 'Button', key: `${b}-tarea:arriba:16` })).toBe(true)
  await ui.press({ key: 'subagente-tarea:arriba:12' })
  expect(a.ordenes.some(o => o.startsWith('git'))).toBe(false)
  expect(a.toasts).toContain('⚙: un subagente trabaja en la 12 (Tarea 12: cerrar la lista)')
  await ui.unmount()
})

for (const status of ['pending', 'waiting']) {
  test(`Subagente: ${status} también cuenta como trabajando`, async (...m) => {
    await preparar(m, { cola: CERRABLES, agentes: EN_12(status), extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
    const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
    expect(await hay(ui, { type: 'Button', key: 'subagente-tarea:arriba:12' })).toBe(true)
    await ui.unmount()
  })
}

// Al entregar su informe, el subagente queda esperando instrucciones (completed o idle): se puede retomar con su
// contexto, así que su ⚙ sigue, roja, mientras la tarea esté en curso (decisión 162). Parado (killed) o
// fallido (failed), se va.
// El color de la ⚙ de la tarea, arriba: verde si trabaja, roja si espera instrucciones (decisión 162).
const marca = async (ui: { find: (q: object) => Promise<unknown> }, id: number) =>
  ((await ui.find({ type: 'Button', key: `subagente-tarea:arriba:${String(id)}` })) as { children: Nodo[] } | undefined)?.children[0]?.props
for (const status of ['completed', 'idle']) {
  test(`Subagente: ${status}, la ⚙ sigue, con Activar rama, la C y la D`, async (...m) => {
    const agentes = EN_12()
    const { cambiarCola } = await preparar(m, { desplegadas: true, cola: CERRABLES, agentes, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
    const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
    agentes[0]!.status = status
    await cambiarCola(CERRABLES)
    expect(await marca(ui, 12)).toEqual({ color: 'error' })
    for (const b of ['probar', 'cerrar', 'descartar']) expect(await hay(ui, { type: 'Button', key: `${b}-tarea:arriba:12` })).toBe(true)
    await ui.unmount()
  })
}

test('Subagente: el que espera avisa distinto; si otro trabaja en la tarea, manda el que trabaja', async (...m) => {
  const agentes = [{ description: 'Tarea 12: cerrar la lista', status: 'completed' }]
  const a = await preparar(m, { cola: CERRABLES, agentes, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await marca(ui, 12)).toEqual({ color: 'error' })
  await ui.press({ key: 'subagente-tarea:arriba:12' })
  expect(a.toasts).toContain('⚙: el subagente de la 12 espera instrucciones (Tarea 12: cerrar la lista)')
  agentes.push({ description: 'Tarea 12: segundo paso', status: 'running' })
  await a.cambiarCola(CERRABLES)
  expect(await marca(ui, 12)).toEqual({ color: 'success' })
  await ui.press({ key: 'subagente-tarea:arriba:12' })
  expect(a.toasts).toContain('⚙: un subagente trabaja en la 12 (Tarea 12: segundo paso)')
  await ui.unmount()
})

test('Subagente: el que espera no da ⚙ si la tarea no está en curso', async (...m) => {
  const agentes = [
    { description: 'Tarea 9: en observación', status: 'completed' },
    { description: 'Tarea 8: en cola', status: 'completed' },
    { description: 'Tarea 7: en cola, trabajando', status: 'running' },
  ]
  await preparar(m, { cola: DESCARTABLES, agentes, reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'sec:observacion' })
  expect(await hay(ui, { type: 'Button', key: 'subagente-tarea:cola:7' })).toBe(true)
  for (const k of ['observacion:9', 'cola:8']) expect(await ui.find({ type: 'Button', key: `subagente-tarea:${k}` })).toBe(undefined)
  await ui.unmount()
})

test('Subagente: el latido pasa la ⚙ de trabajando a esperando sin que pase nada más', async (...m) => {
  const agentes = EN_12()
  const a = await preparar(m, { cola: CERRABLES, agentes, reloj: true, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  agentes[0]!.status = 'completed'
  await a.reloj!.advance(60_000)
  expect(await marca(ui, 12)).toEqual({ color: 'error' })
  await ui.press({ key: 'subagente-tarea:arriba:12' })
  expect(a.toasts).toContain('⚙: el subagente de la 12 espera instrucciones (Tarea 12: cerrar la lista)')
  await ui.unmount()
})

// El motor deja de listar un subagente poco después de que entregue su informe, aunque siga retomable: el panel
// recuerda en la sesión los que vio, y uno que trabajaba y desaparece de la lista espera instrucciones.
const ESPERA = { color: 'error' }
test('Subagente: el motor deja de listarlo tras su informe y la ⚙ sigue, en espera', async (...m) => {
  const agentes = EN_12()
  const { cambiarCola } = await preparar(m, { cola: CERRABLES, agentes, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await marca(ui, 12)).toEqual({ color: 'success' })
  agentes.splice(0)
  await cambiarCola(CERRABLES)
  expect(await marca(ui, 12)).toEqual(ESPERA)
  await ui.unmount()
})

test('Subagente: parado con TaskStop, la ⚙ se va aunque el motor ya no lo liste', async (...m) => {
  const agentes = EN_12()
  m[1]('tool.call', { tool: 'TaskStop' }, () => ({ result: { message: 'stopped' } as never }))
  const { cambiarCola } = await preparar(m, { desplegadas: true, cola: CERRABLES, agentes, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await marca(ui, 12)).toEqual({ color: 'success' })
  agentes.splice(0)
  await m[0].tool.call({ tool: 'TaskStop', task_id: 'a0' })
  await cambiarCola(CERRABLES)
  expect(await ui.find({ type: 'Button', key: 'subagente-tarea:arriba:12' })).toBe(undefined)
  for (const b of ['probar', 'cerrar', 'descartar']) expect(await hay(ui, { type: 'Button', key: `${b}-tarea:arriba:12` })).toBe(true)
  await ui.unmount()
})

test('Subagente: si TaskStop no encuentra nada que parar (ya entregó su informe), sigue en espera', async (...m) => {
  const agentes = EN_12('completed')
  m[1]('tool.call', { tool: 'TaskStop' }, () => ({ result: 'No task found' as never, text: 'No task found', isError: true }))
  const { cambiarCola } = await preparar(m, { cola: CERRABLES, agentes, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  agentes.splice(0)
  await m[0].tool.call({ tool: 'TaskStop', task_id: 'a0' })
  await cambiarCola(CERRABLES)
  expect(await marca(ui, 12)).toEqual(ESPERA)
  await ui.unmount()
})

test('Subagente: al pararlo (killed), la ⚙ se va y vuelven Activar rama, la C y la D', async (...m) => {
  const agentes = EN_12()
  const { cambiarCola } = await preparar(m, { desplegadas: true, cola: CERRABLES, agentes, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'subagente-tarea:arriba:12' })).toBe(true)
  agentes[0]!.status = 'killed'
  await cambiarCola(CERRABLES)
  expect(await ui.find({ type: 'Button', key: 'subagente-tarea:arriba:12' })).toBe(undefined)
  for (const b of ['probar', 'cerrar', 'descartar']) expect(await hay(ui, { type: 'Button', key: `${b}-tarea:arriba:12` })).toBe(true)
  await ui.unmount()
})

test('Subagente: el latido relee los subagentes; la ⚙ se va sin que pase nada más', async (...m) => {
  const agentes = EN_12()
  const { reloj } = await preparar(m, { desplegadas: true, cola: CERRABLES, agentes, reloj: true, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'subagente-tarea:arriba:12' })).toBe(true)
  agentes[0]!.status = 'failed'
  await reloj!.advance(60_000)
  expect(await ui.find({ type: 'Button', key: 'subagente-tarea:arriba:12' })).toBe(undefined)
  expect(await hay(ui, { type: 'Button', key: 'probar-tarea:arriba:12' })).toBe(true)
  await ui.unmount()
})

test('Subagente: al lanzarlo, su ⚙ sale al momento', async (...m) => {
  const agentes: Agente[] = []
  m[1]('agent.spawn', (_, e) => {
    agentes.push({ description: e.description ?? '', status: 'running' })
    return { model: 'x', agentId: 'a9' }
  })
  await preparar(m, { cola: CERRABLES, agentes, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await ui.find({ type: 'Button', key: 'subagente-tarea:arriba:12' })).toBe(undefined)
  await m[0].agent.spawn({ prompt: 'Cierra la lista', description: 'Tarea 12: cerrar la lista' })
  expect(await hay(ui, { type: 'Button', key: 'subagente-tarea:arriba:12' })).toBe(true)
  await ui.unmount()
})

test('Subagente: «Tarea 120» no es la 12; «tarea 15», en minúscula, sí es la 15', async (...m) => {
  const agentes = [
    { description: 'Tarea 120: otra cosa', status: 'running' },
    { description: 'tarea 15 sin dos puntos', status: 'running' },
  ]
  await preparar(m, { desplegadas: true, cola: CERRABLES, agentes, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await ui.find({ type: 'Button', key: 'subagente-tarea:arriba:12' })).toBe(undefined)
  expect(await hay(ui, { type: 'Button', key: 'probar-tarea:arriba:12' })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'subagente-tarea:arriba:15' })).toBe(true)
  await ui.unmount()
})

test('Subagente: un worktree con la rama de la 12, sin subagente, no da ⚙', async (...m) => {
  const wt = {
    '/sf/.git/worktrees/agent-1/HEAD': 'ref: refs/heads/feature/12-lista\n',
    '/sf/.git/worktrees/agent-1/gitdir': '/sf/.claude/worktrees/agent-1/.git\n',
    '/sf/.claude/worktrees/agent-1/.git': 'gitdir: /sf/.git/worktrees/agent-1\n',
  }
  await preparar(m, { desplegadas: true, cola: CERRABLES, agentes: EN_12('killed'), extra: { ...RAMAS_CERRAR, ...wt, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await ui.find({ type: 'Button', key: 'subagente-tarea:arriba:12' })).toBe(undefined)
  for (const b of ['probar', 'cerrar', 'descartar']) expect(await hay(ui, { type: 'Button', key: `${b}-tarea:arriba:12` })).toBe(true)
  await ui.unmount()
})

// Avisos emergentes (tarea 257): lo importante primero, las rutas abreviadas y una marca distinta para los errores.
test('Emergentes: la C con subagente recogido dice la tarea y lo quitado, con las rutas abreviadas y la marca azul', async (...m) => {
  const mensaje = 'Cerrada la 12 en develop (c0ffee1). Quitados: D:/Projectes/SoftwareFactory-wt-12, sub-12.'
  const { marcados, ui } = await cerrarLa12(m, {}, { respuesta: { ok: true, mensaje } })
  expect(marcados.map(t => t.text)).toContain('🟦 Cerrada la 12 en develop (c0ffee1). Quitados: wt-12, sub-12.')
  await ui.unmount()
})

test('Emergentes: un fallo de la C, con la marca roja y más tiempo a la vista', async (...m) => {
  const mensaje = 'Hay cambios sin commit en la rama activa. Haz commit antes.'
  const { marcados, ui } = await cerrarLa12(m, {}, { respuesta: { ok: false, mensaje } })
  expect(marcados).toContainEqual({ text: `🟥 C: ${mensaje}`, timeoutMs: 8000 })
  await ui.unmount()
})

test('Emergentes: rutas abreviadas, marcas y duración', () => {
  expect(MARCA_AVISO_EMERGENTE).not.toBe(MARCA_ERROR_EMERGENTE)
  expect(abreviarRutas('Quitados: D:/Projectes/SoftwareFactory-wt-256, sub-256.')).toBe('Quitados: wt-256, sub-256.')
  expect(abreviarRutas('queda el worktree C:\\x\\Proyecto-wt-3: tiene cambios')).toBe('queda el worktree wt-3: tiene cambios')
  expect(abreviarRutas('en el worktree /sf/.claude/worktrees/agent-1.')).toBe('en el worktree agent-1.')
  // Lo que no es una ruta absoluta se queda: una orden, una ruta relativa, una rama.
  const igual = '/sf_split 12 2,3 · plugins/sf/.claude-plugin/plugin.json · rama feature/6-algo · docs/propuestas.md'
  expect(abreviarRutas(igual)).toBe(igual)
  expect(pareceError('C: no se pudo')).toBe(true)
  expect(pareceError('/sf_split: la 9 ha cambiado')).toBe(true)
  expect(pareceError('→: cola.py no responde')).toBe(true)
  expect(pareceError('TURBO: se lo paso a Claude.')).toBe(false)
  expect(pareceError('/sf_split 12 2,3 con los pasos que separas.')).toBe(false)
  expect(textoEmergente('Hecho.', false)).toBe(`${MARCA_AVISO_EMERGENTE} Hecho.`)
  expect(textoEmergente('C: no.', true)).toBe(`${MARCA_ERROR_EMERGENTE} C: no.`)
  expect(duracionEmergente('corto', false)).toBe(4000)
  expect(duracionEmergente('x'.repeat(150), false)).toBe(9000)
  expect(duracionEmergente('corto', true)).toBe(8000)
  expect(duracionEmergente('x'.repeat(1000), true)).toBe(15000)
})

test('Subagente: en una tarea sin rama, ⚙ y la E', async (...m) => {
  await preparar(m, { desplegadas: true, cola: ELIMINABLES, agentes: [{ description: 'Tarea 7: empezarla', status: 'running' }] })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'subagente-tarea:cola:7' })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'eliminar-tarea:cola:7' })).toBe(true)
  // La 1, en curso y sin subagente, también tiene su E, arriba.
  expect(await hay(ui, { type: 'Button', key: 'eliminar-tarea:arriba:1' })).toBe(true)
  await ui.unmount()
})

// Pulsa la C de la 12 (con su rama activa) una o dos veces; cola.py responde `respuesta`, si se da.
const cerrarLa12 = async (m: Motor, git: Git, { clics = 2, respuesta }: { clics?: number; respuesta?: Respuesta } = {}) => {
  const r = await preparar(m, {
    desplegadas: true,
    cola: CERRABLES,
    reloj: true,
    extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/feature/12-lista\n' },
    git,
    ...(respuesta ? { respuestas: { cerrar: respuesta } } : {}),
  })
  const antes = r.archivos[COLA]
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  for (let i = 0; i < clics; i++) await ui.press({ key: 'cerrar-tarea:arriba:12' })
  return { ...r, antes, ui }
}

test('Cerrar: el primer clic pide confirmar; el segundo la pide a cola.py cerrar, sin Claude, y entra en Cerradas', async (...m) => {
  const { archivos, ordenes, colas, lineasCola, toasts, prompts, ui } = await cerrarLa12(m, {}, { clics: 1 })
  expect(await hay(ui, { type: 'Text', text: cerrando })).toBe(true)
  expect(colas).toEqual([])
  await ui.press({ key: 'cerrar-tarea:arriba:12' })
  expect(colas).toEqual(['cerrar 12'])
  // Con las opciones comunes: el propietario, desde el panel, en la carpeta de la sesión.
  expect(lineasCola[0]!.slice(-9)).toEqual(['--raiz', RAIZ, '--json', '--quien', 'propietario', '--via', 'panel', 'cerrar', '12'])
  // El panel no ejecuta git por su cuenta: lo hace cola.py.
  expect(ordenes.some(o => /^git (switch|merge|commit|push|branch)/.test(o))).toBe(false)
  expect(idsCola(archivos)).toEqual([13, 14, 15, 16, 2])
  expect(toasts).toContain('Cerrada la 12 en develop (c0ffee1).')
  expect(prompts).toHaveLength(0)
  expect(await colores(ui, 12)).toEqual(['success'])
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+1/ })).toBe(true)
  await ui.unmount()
})

test('Cerrar: si falla el push, la cierra igual, avisa y Cerradas dice que falta hasta que origin/develop lo tenga', async (...m) => {
  const git: Git = { pushFalla: true, noAncestro: true }
  const { archivos, toasts, cambiarCola, ui } = await cerrarLa12(m, git)
  expect(idsCola(archivos)).toEqual([13, 14, 15, 16, 2])
  expect(toasts.some(t => t.startsWith('Cerrada la 12 en develop (c0ffee1). Aviso: falta el push de develop'))).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /falta el push de develop \(12\)/ })).toBe(true)
  // Hecho el push (origin/develop ya tiene el commit), la línea se va.
  git.noAncestro = false
  await cambiarCola((JSON.parse(archivos[COLA]!) as { peticiones: Pet[] }).peticiones)
  expect(await ui.find({ type: 'Text', text: /falta el push de develop/ })).toBe(undefined)
  await ui.unmount()
})

test('Cerrar: si cola.py no puede (cambios sin commit, la rama en otro worktree), dice por qué y no toca la cola', async (...m) => {
  const mensaje = 'Hay cambios sin commit en la rama activa. Haz commit antes.'
  const { archivos, antes, toasts, prompts, ui } = await cerrarLa12(m, {}, { respuesta: { ok: false, mensaje } })
  expect(archivos[COLA]).toBe(antes)
  expect(toasts).toContain(`C: ${mensaje}`)
  expect(prompts).toHaveLength(0)
  await ui.unmount()
})

test('Cerrar: con choques, cola.py lo deshace y el panel se lo pasa a Claude para repetir el cierre', async (...m) => {
  const respuesta = { ok: false, mensaje: 'Choques', fallo: 'choques', motivo: 'choques al pasar feature/12-lista a develop' }
  const { archivos, antes, toasts, prompts, reloj, ui } = await cerrarLa12(m, {}, { respuesta })
  expect(archivos[COLA]).toBe(antes)
  expect(toasts).toContain('Choques al pasar la 12 a develop: se lo paso a Claude.')
  // Sale desde el temporizador, no desde el hook que atiende el panel.
  expect(prompts).toHaveLength(0)
  await reloj!.advance(100)
  expect(prompts).toHaveLength(1)
  const pedido = JSON.stringify(prompts[0])
  for (const x of ['Cierra la 12', 'choques al pasar feature/12-lista a develop', 'feature/12-lista', '/.claude/sf/cola.py', ' cerrar 12`']) expect(pedido).toContain(x)
  await ui.unmount()
})

test('Cerrar: si falla el commit, también se lo pasa a Claude', async (...m) => {
  const respuesta = { ok: false, mensaje: 'x', fallo: 'commit', motivo: 'el hook de commit lo rechaza' }
  const { toasts, prompts, reloj, ui } = await cerrarLa12(m, {}, { respuesta })
  expect(toasts).toContain('C: no se pudo hacer el commit de la 12 en develop: se lo paso a Claude.')
  await reloj!.advance(100)
  expect(JSON.stringify(prompts[0])).toContain('el hook de commit lo rechaza')
  await ui.unmount()
})

// Revertir una tarea mergeada (decisión del propietario, 2026-10-29): R negra sobre naranja en Cerradas, solo en
// las C con su commit «… (N)» en develop; en observación, en lugar de la D (decisión 115, 4). El primer clic la parte en
// «R eliminar» y «R pendiente»; el segundo, en uno de ellos, lo pide a cola.py revertir con ese destino, sin Claude ni
// push (decisión 134). La 20 y la 21 se han cerrado en la sesión (C); solo la 20 tiene su squash en develop. La 22,
// revertida antes de la decisión 134: sigue con R.
const SALIDAS_REVERTIR: Pet[] = [
  { id: 20, texto: 'Botón de prueba', estado: 'cerrada', commit: 'aaa1111', historial: [ev('creada', 'en-cola', ANTES), ev('cerrada', 'develop aaa1111')] },
  { id: 21, texto: 'Sin mergear', estado: 'cerrada', historial: [ev('creada', 'en-cola', ANTES), ev('cerrada', 'sin rama')] },
  { id: 22, texto: 'Ya revertida', estado: 'revertida', historial: [ev('creada', 'en-cola', ANTES), ev('cerrada', 'develop ddd4444'), ev('revertida', 'develop f0f0f01 revierte ddd4444')] },
]
const EN_CURSO_1: Pet[] = [{ id: 1, texto: 'Panel lateral', estado: 'en-curso' }]
const LOG_DEVELOP = 'f0f0f01\tRevert "Ya revertida (22)"\naaa1111\tBotón de prueba (20)\nbbb2222\tOtra cosa (sf 0.3)\nddd4444\tYa revertida (22)\n'
const revirtiendo = /^¿Revertir\?$/
// Cada caso, con develop en un commit distinto: el panel guarda lo leído de develop con su commit.
let commitsDevelop = 0

const revertirLa20 = async (m: Motor, { clics = 2, destino = 'pendiente', respuesta, cola = EN_CURSO_1 }: { clics?: number; destino?: string; respuesta?: Respuesta; cola?: Pet[] } = {}) => {
  const r = await preparar(m, {
    desplegadas: true,
    cola,
    salidas: SALIDAS_REVERTIR,
    reloj: true,
    extra: { '/sf/.git/HEAD': 'ref: refs/heads/develop\n', '/sf/.git/refs/heads/develop': `d${++commitsDevelop}` },
    git: { log: LOG_DEVELOP },
    ...(respuesta ? { respuestas: { revertir: respuesta } } : {}),
  })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  if (clics >= 1) await ui.press({ key: 'revertir-tarea:hecho:20' })
  if (clics >= 2) await ui.press({ key: `revertir-tarea:hecho:20:${destino}` })
  await r.reloj!.advance(100)
  return { ...r, antes: r.archivos[COLA], ui }
}

test('Revertir: R solo en las cerradas que han entrado en develop y siguen sin revertir', async (...m) => {
  const { colas, ui } = await revertirLa20(m, { clics: 0 })
  expect(await colores(ui, 20)).toEqual(['success'])
  expect(await colores(ui, 22)).toEqual([GRIS])
  expect(await hay(ui, { type: 'Button', key: 'revertir-tarea:hecho:20' })).toBe(true)
  for (const id of [21, 22]) expect(await ui.find({ type: 'Button', key: `revertir-tarea:hecho:${id}` })).toBe(undefined)
  // Ni en las tareas de la cola.
  for (const k of ['cola:1', 'arriba:1']) expect(await ui.find({ type: 'Button', key: `revertir-tarea:${k}` })).toBe(undefined)
  expect(colas).toEqual([])
  await ui.unmount()
})

// A observación (296): en las cerradas (C), con o sin commit en develop; dos clics, «cola.py reobservar», sin Claude ni
// git. Vuelve a la cola en observación, con su commit: sale en observación con su Revertir y ya no en Cerradas.
test('A observación: una cerrada vuelve a observación con cola.py reobservar, con dos clics y sin Claude', async (...m) => {
  const { archivos, colas, ordenes, toasts, prompts, ui } = await revertirLa20(m, { clics: 0 })
  for (const id of [20, 21]) expect(await hay(ui, { type: 'Button', key: `reobservar-tarea:hecho:${id}`, text: /^ A observación $/ })).toBe(true)
  expect((await etiqueta(ui, 'reobservar-tarea:hecho:20'))?.color).toBe('success')
  // Ni en las revertidas de antes (R) ni en las tareas de la cola.
  expect(await ui.find({ type: 'Button', key: 'reobservar-tarea:hecho:22' })).toBe(undefined)
  for (const k of ['cola:1', 'arriba:1']) expect(await ui.find({ type: 'Button', key: `reobservar-tarea:${k}` })).toBe(undefined)
  await ui.press({ key: 'reobservar-tarea:hecho:20' })
  expect(await hay(ui, { type: 'Button', key: 'reobservar-tarea:hecho:20', text: /^ ¿A observación\? sí $/ })).toBe(true)
  expect(colas).toEqual([])
  await ui.press({ key: 'reobservar-tarea:hecho:20' })
  expect(colas).toEqual(['reobservar 20'])
  expect(ordenes.some(o => /^git (switch|revert|push|commit)/.test(o))).toBe(false)
  expect(toasts).toContain('La 20 vuelve a observación, con su commit de develop (aaa1111).')
  expect(prompts).toHaveLength(0)
  expect(idsCola(archivos)).toEqual([1, 20])
  expect(eventosDe(archivos, 20)).toEqual(['creada', 'cerrada', 'reobservada'])
  expect(await ui.find({ type: 'Button', key: 'reobservar-tarea:hecho:20' })).toBe(undefined)
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+2$/ })).toBe(true)
  await ui.press({ key: 'sec:observacion' })
  expect(await hay(ui, { type: 'Button', key: 'revertir-tarea:observacion:20' })).toBe(true)
  await ui.unmount()
})

test('Revertir: el primer clic la parte en «¿Revertir?» [eliminar] [a Pendientes]; a los 5 s vuelve a ser Revertir', async (...m) => {
  const { colas, reloj, ui } = await revertirLa20(m, { clics: 1 })
  expect(await hay(ui, { type: 'Text', text: revirtiendo })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /^ eliminar $/ })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /^ a Pendientes $/ })).toBe(true)
  for (const d of ['eliminar', 'pendiente']) expect(await hay(ui, { type: 'Button', key: `revertir-tarea:hecho:20:${d}` })).toBe(true)
  expect(await ui.find({ type: 'Button', key: 'revertir-tarea:hecho:20' })).toBe(undefined)
  expect(colas).toEqual([])
  // Un clic en otro sitio lo deja como estaba.
  await ui.press({ key: 'sec:cola' })
  expect(await ui.find({ type: 'Text', text: revirtiendo })).toBe(undefined)
  expect(await hay(ui, { type: 'Button', key: 'revertir-tarea:hecho:20' })).toBe(true)
  // Y a los 5 s.
  await ui.press({ key: 'revertir-tarea:hecho:20' })
  await reloj!.advance(5100)
  expect(await ui.find({ type: 'Text', text: revirtiendo })).toBe(undefined)
  expect(colas).toEqual([])
  await ui.unmount()
})

test('Revertir y dejar pendiente: cola.py, sin Claude; vuelve a Pendientes reabierta y sale solo allí', async (...m) => {
  const { archivos, ordenes, colas, toasts, prompts, ui } = await revertirLa20(m, { destino: 'pendiente' })
  expect(colas).toEqual(['revertir 20 --pendiente'])
  expect(ordenes.some(o => /^git (switch|revert|push)/.test(o))).toBe(false)
  expect(toasts).toContain('Revertida la 20 en develop (c0ffee1), sin push; vuelve a Pendientes, en cola.')
  expect(prompts).toHaveLength(0)
  expect(idsCola(archivos)).toEqual([1, 20])
  expect(eventosDe(archivos, 20)).toEqual(['creada', 'cerrada', 'revertida', 'reabierta'])
  // Solo en Pendientes, como cualquier reabierta: sobre rojo; ni en Cerradas ni con el botón de revertir.
  expect(await colores(ui, 20)).toEqual([`${GRIS} sobre error`])
  expect(await ui.find({ type: 'Button', key: 'revertir-tarea:hecho:20' })).toBe(undefined)
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+2$/ })).toBe(true)
  await ui.unmount()
})

test('Revertir y eliminar: sale de la cola sin rastro, como con la E; no queda en Cerradas', async (...m) => {
  const { archivos, colas, toasts, ui } = await revertirLa20(m, { destino: 'eliminar' })
  expect(colas).toEqual(['revertir 20 --eliminar'])
  expect(toasts).toContain('Revertida la 20 en develop (c0ffee1), sin push, y eliminada; su número no se reutiliza.')
  expect(idsCola(archivos)).toEqual([1])
  expect(eventosDe(archivos, 20)).toEqual(['creada', 'cerrada', 'revertida', 'eliminada'])
  expect(await conNumero(ui, 20)).toBe(false)
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+2$/ })).toBe(true)
  await ui.unmount()
})

test('Revertir: con choques, cola.py lo deshace y el panel se lo pasa a Claude; sigue en verde y con su R', async (...m) => {
  const respuesta = { ok: false, mensaje: 'x', fallo: 'choques', motivo: 'choques al revertir aaa1111' }
  const { toasts, prompts, ui } = await revertirLa20(m, { respuesta })
  expect(toasts).toContain('Choques al revertir la 20: se lo paso a Claude.')
  expect(prompts.some(t => JSON.stringify(t).includes('la 20') && JSON.stringify(t).includes('aaa1111') && JSON.stringify(t).includes('sin push'))).toBe(true)
  expect(await colores(ui, 20)).toEqual(['success'])
  expect(await hay(ui, { type: 'Button', key: 'revertir-tarea:hecho:20' })).toBe(true)
  await ui.unmount()
})

test('Revertir: si cola.py no puede (cambios sin commit, develop en otro worktree), dice por qué', async (...m) => {
  const mensaje = 'develop está en el worktree /sf/principal. Revierte allí.'
  const { toasts, prompts, ui } = await revertirLa20(m, { respuesta: { ok: false, mensaje } })
  expect(toasts).toContain('R: develop está en el worktree principal. Revierte allí.')
  expect(prompts).toHaveLength(0)
  expect(await colores(ui, 20)).toEqual(['success'])
  await ui.unmount()
})

test('Revertir: en observación, R en lugar de D; revertida y pendiente, vuelve a Pendientes sin R', async (...m) => {
  const observada: Pet = { id: 30, texto: 'En observación', estado: 'en-observacion', prueba: 'mirar', historial: [ev('creada', 'en-cola', ANTES), ev('a-observacion', 'develop abc1234', ANTES)] }
  const { archivos, colas, toasts, ui } = await revertirLa20(m, { clics: 0, cola: [...EN_CURSO_1, observada] })
  await ui.press({ key: 'sec:observacion' })
  expect(await hay(ui, { type: 'Button', key: 'revertir-tarea:observacion:30' })).toBe(true)
  expect(await ui.find({ type: 'Button', key: 'descartar-tarea:observacion:30' })).toBe(undefined)
  await ui.press({ key: 'revertir-tarea:observacion:30' })
  await ui.press({ key: 'revertir-tarea:observacion:30:pendiente' })
  expect(colas).toEqual(['revertir 30 --pendiente'])
  expect(toasts).toContain('Revertida la 30 en develop (c0ffee1), sin push; vuelve a Pendientes, en cola.')
  expect(idsCola(archivos)).toEqual([1, 30])
  expect(estadoEnCola(archivos, 30)).toBe('en-cola')
  expect(await ui.find({ type: 'Button', key: 'revertir-tarea:observacion:30' })).toBe(undefined)
  await ui.unmount()
})

test('A observación: junto a Cerrar; el primer clic pide «¿A observación? sí»; el segundo, cola.py a-observacion, y pasa a observación (241)', async (...m) => {
  const { archivos, colas, lineasCola, toasts, prompts, ui } = await cerrarLa12(m, {}, { clics: 0 })
  for (const k of ['arriba:12', 'arriba:16']) expect(await hay(ui, { type: 'Button', key: `a-observacion-tarea:${k}`, text: /^ A observación $/ })).toBe(true)
  for (const k of ['arriba:13', 'cola:14', 'arriba:15']) expect(await ui.find({ type: 'Button', key: `a-observacion-tarea:${k}` })).toBe(undefined)
  expect((await etiqueta(ui, 'a-observacion-tarea:arriba:12'))?.color).toBe('success')
  await ui.press({ key: 'a-observacion-tarea:arriba:12' })
  expect(await hay(ui, { type: 'Button', key: 'a-observacion-tarea:arriba:12', text: /^ ¿A observación\? sí $/ })).toBe(true)
  expect(colas).toEqual([])
  await ui.press({ key: 'a-observacion-tarea:arriba:12' })
  expect(colas).toEqual(['a-observacion 12'])
  expect(lineasCola[0]!.slice(-3)).toEqual(['panel', 'a-observacion', '12'])
  expect(estadoEnCola(archivos, 12)).toBe('en-observacion')
  expect(toasts).toContain('La 12, en observación en develop (c0ffee1).')
  expect(prompts).toHaveLength(0)
  await ui.unmount()
})

// Sin rama (188): una tarea en curso sin rama con sus pasos de trabajo hechos se cierra o pasa a observación desde el
// panel, sin squash ni commit.
const SIN_RAMA: Pet[] = [
  {
    id: 18,
    texto: 'Solo cola',
    estado: 'en-curso',
    pasos: [
      { texto: 'Anotar en la cola', estado: 'hecho' },
      { texto: 'Activar rama para poder probar', estado: 'pendiente' },
      { texto: 'Cerrar la tarea', estado: 'pendiente' },
    ],
  },
  {
    id: 19,
    texto: 'Sin rama con trabajo',
    estado: 'en-curso',
    pasos: [
      { texto: 'Hacer E', estado: 'en-curso' },
      { texto: 'Cerrar la tarea', estado: 'pendiente' },
    ],
  },
]

for (const [orden, clave, aviso, estado] of [
  ['cerrar', 'cerrar-tarea', 'Cerrada la 18, sin rama.', null],
  ['a-observacion', 'a-observacion-tarea', 'La 18, en observación.', 'en-observacion'],
] as const) {
  test(`Sin rama: Cerrar y A observación en la en curso con los pasos hechos; ${orden} la saca sin git (188)`, async (...m) => {
    const r = await preparar(m, { desplegadas: true, cola: SIN_RAMA, reloj: true, extra: { '/sf/.git/refs/heads/develop': 'abc', '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
    const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
    expect(await hay(ui, { type: 'Button', key: 'cerrar-tarea:arriba:18', text: /^ Cerrar $/ })).toBe(true)
    expect(await hay(ui, { type: 'Button', key: 'a-observacion-tarea:arriba:18', text: /^ A observación $/ })).toBe(true)
    // Con un paso de trabajo sin hacer, ninguna de las dos.
    for (const k of ['cerrar-tarea', 'a-observacion-tarea']) expect(await ui.find({ type: 'Button', key: `${k}:arriba:19` })).toBe(undefined)
    for (let i = 0; i < 2; i++) await ui.press({ key: `${clave}:arriba:18` })
    expect(r.colas).toEqual([`${orden} 18`])
    expect(r.ordenes.some(o => /^git (switch|merge|commit|push|branch)/.test(o))).toBe(false)
    expect(r.toasts).toContain(aviso)
    expect(r.prompts).toHaveLength(0)
    if (estado) expect(estadoEnCola(r.archivos, 18)).toBe(estado)
    else expect(idsCola(r.archivos)).toEqual([19])
    await ui.unmount()
  })
}

test('Deliberativa sin rama: Cerrar, sin A observación ni Activar rama (218, 278; tarea 345)', async (...m) => {
  const cola = [
    { id: 18, texto: 'Deliberar algo', tipo: 'deliberar', estado: 'en-curso', pasos: [{ texto: 'Escrito el informe', estado: 'hecho' }, { texto: 'Cerrar la tarea', estado: 'pendiente' }] },
  ]
  await preparar(m, { desplegadas: true, cola, reloj: true, extra: { '/sf/.git/refs/heads/develop': 'abc', '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'cerrar-tarea:arriba:18', text: /^ Cerrar $/ })).toBe(true)
  for (const k of ['a-observacion-tarea', 'probar-tarea']) expect(await ui.find({ type: 'Button', key: `${k}:arriba:18` })).toBe(undefined)
  await ui.unmount()
})

test('A observación: con choques, se lo pasa a Claude para repetir cola.py a-observacion (241)', async (...m) => {
  const respuesta = { ok: false, mensaje: 'Choques', fallo: 'choques', motivo: 'choques al pasar feature/12-lista a develop' }
  const r = await preparar(m, { desplegadas: true, cola: CERRABLES, reloj: true, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' }, respuestas: { 'a-observacion': respuesta } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  for (let i = 0; i < 2; i++) await ui.press({ key: 'a-observacion-tarea:arriba:12' })
  expect(r.toasts).toContain('Choques al pasar la 12 a develop: se lo paso a Claude.')
  await r.reloj!.advance(100)
  const pedido = JSON.stringify(r.prompts[0])
  for (const x of ['Pasa a observación la 12', '/.claude/sf/cola.py', ' a-observacion 12`']) expect(pedido).toContain(x)
  await ui.unmount()
})

test('Cerrar en observación: el primer clic pide «¿Cerrar? sí»; el segundo, cola.py cerrar, sin Claude, y sale de la cola (241)', async (...m) => {
  const r = await preparar(m, { desplegadas: true, cola: CERRABLES, reloj: true, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'sec:observacion' })
  expect(await hay(ui, { type: 'Button', key: 'cerrar-observada-tarea:observacion:2', text: /^ Cerrar $/ })).toBe(true)
  expect((await etiqueta(ui, 'cerrar-observada-tarea:observacion:2'))?.color).toBe('success')
  // Solo en observación: las en curso cierran con la suya.
  expect(await ui.find({ type: 'Button', key: 'cerrar-observada-tarea:arriba:12' })).toBe(undefined)
  await ui.press({ key: 'cerrar-observada-tarea:observacion:2' })
  expect(await hay(ui, { type: 'Button', key: 'cerrar-observada-tarea:observacion:2', text: cerrando })).toBe(true)
  expect(r.colas).toEqual([])
  await ui.press({ key: 'cerrar-observada-tarea:observacion:2' })
  expect(r.colas).toEqual(['cerrar 2'])
  expect(r.ordenes.some(o => /^git /.test(o))).toBe(false)
  expect(idsCola(r.archivos)).toEqual([12, 13, 14, 15, 16])
  expect(r.toasts).toContain('Cerrada la 2, en observación: sale de la cola.')
  expect(r.prompts).toHaveLength(0)
  expect(await ui.find({ type: 'Button', key: 'cerrar-observada-tarea:observacion:2' })).toBe(undefined)
  await ui.unmount()
})

// Un proyecto por sesión: Write pasa a la herramienta de la prueba, que responde «ok»; un bloqueo sale como deny.
const escribirEn = async ([$]: Motor, file_path: string, agentId?: string) =>
  (await $.tool.call({ tool: 'Write', file_path, content: 'x', ...(agentId ? { agentId } : {}) })) as { deny?: string }

test('Un proyecto por sesión: un worktree del repositorio de la sesión es el mismo proyecto', async (...m) => {
  const wt = '/sf/.claude/worktrees/agent-x'
  await preparar(m, {
    extra: { [`${wt}/plugins/sf/.claude-plugin/plugin.json`]: '{}', [`${wt}/.git`]: 'gitdir: /sf/.git/worktrees/agent-x\n' },
  })
  expect((await escribirEn(m, `${wt}/plugins/sf/hooks/control.ts`)).deny).toBe(undefined)
})

// Los worktrees de los subagentes (<raíz>/.claude/worktrees/<nombre>) son del proyecto por su ruta, aunque su .git
// no se lea; con barras invertidas y la unidad en otra caja, igual.
test('Un proyecto por sesión: el worktree de un subagente es el mismo proyecto, aunque no se lea su .git', async (...m) => {
  const wt = '/sf/.claude/worktrees/agent-y'
  await preparar(m, { raiz: 'D:/sf', extra: { [`${wt}/plugins/sf/.claude-plugin/plugin.json`]: '{}' } })
  expect((await escribirEn(m, `D:${wt}/plugins/sf/hooks/control.ts`)).deny).toBe(undefined)
  expect((await escribirEn(m, 'd:\\sf\\.claude\\worktrees\\agent-y\\plugins\\sf\\hooks\\lectura.ts')).deny).toBe(undefined)
})

test('Un proyecto por sesión: con la sesión en el worktree, escribe en él y en su raíz', async (...m) => {
  const wt = '/sf/.claude/worktrees/agent-z'
  await preparar(m, { raiz: wt, extra: { [`${wt}/plugins/sf/.claude-plugin/plugin.json`]: '{}' } })
  expect((await escribirEn(m, `${wt}/plugins/sf/hooks/control.ts`)).deny).toBe(undefined)
  expect((await escribirEn(m, '/sf/plugins/sf/hooks/control.ts')).deny).toBe(undefined)
})

test('Un proyecto por sesión: lo que parece un worktree sin serlo se bloquea', async (...m) => {
  await preparar(m, {
    extra: { '/sf/.claude/worktrees-x/otro/.sf/proyecto.json': '{}', '/sf/anidado/worktrees/agent-1/.sf/proyecto.json': '{}' },
  })
  expect((await escribirEn(m, '/sf/.claude/worktrees-x/otro/a.ts')).deny ?? '').toMatch(/es de otro y esta sesión es de sf/)
  expect((await escribirEn(m, '/sf/anidado/worktrees/agent-1/a.ts')).deny ?? '').toMatch(/es de agent-1 y esta sesión es de sf/)
})

test('Un proyecto por sesión: el worktree de un subagente de otro proyecto se bloquea', async (...m) => {
  await preparar(m, { extra: { '/sf/anidado/p2/.sf/proyecto.json': '{}', '/sf/anidado/p2/.claude/worktrees/agent-1/.sf/proyecto.json': '{}' } })
  expect((await escribirEn(m, '/sf/anidado/p2/.claude/worktrees/agent-1/a.ts')).deny ?? '').toMatch(/es de p2 y esta sesión es de sf/)
})

test('Un proyecto por sesión: otro proyecto se bloquea', async (...m) => {
  // Anidado en /sf: la prueba lleva cualquier marca de la SF fuera de /sf a la del plugin.
  await preparar(m, { extra: { '/sf/anidado/otro/.sf/proyecto.json': '{}' } })
  expect((await escribirEn(m, '/sf/anidado/otro/src/a.ts')).deny ?? '').toMatch(/es de otro y esta sesión es de sf/)
})

// Decisión 194: desde otro proyecto, la SF es un proyecto más; ni sus propuestas ni su registro se escriben.
test('Un proyecto por sesión: desde otro proyecto, la SF se bloquea, también propuestas.md y registro.json', async (...m) => {
  await preparar(m, {
    sinMarca: true,
    extra: { '/sf/.sf/proyecto.json': JSON.stringify({ sf: '1.1.0', proyecto: 'Demo' }), '/sf/fuente/plugins/sf/.claude-plugin/plugin.json': '{}' },
  })
  for (const ruta of ['/sf/fuente/docs/propuestas.md', '/sf/fuente/.sf/registro.json', '/sf/fuente/plugins/sf/hooks/panel.tsx'])
    expect((await escribirEn(m, ruta)).deny ?? '').toMatch(/es de fuente y esta sesión es de sf\. Hazlo en una sesión abierta en \/sf\/fuente\./)
  expect((await escribirEn(m, '/sf/docs/propuestas.md')).deny).toBe(undefined)
})

test('Cola: un subagente no la escribe; el principal, sí', async (...m) => {
  await preparar(m)
  expect((await escribirEn(m, COLA, 'a1')).deny ?? '').toMatch(/Solo el principal escribe la cola/)
  expect((await escribirEn(m, COLA)).deny).toBe(undefined)
})


// La caja sobre el prompt en pantalla completa: cede su sitio solo al panel que se ve (colocado y al frente).
const CAJA = {
  plugin: 'sf',
  component: 'AbovePrompt',
  surface: 'terminal',
  viewport: { columns: 160, rows: 50, isFullscreen: true },
  props: { hasSurvey: false, isWorking: false, maxRows: 12, bodyColumns: 100, scroll: { offset: 0, bodyRows: 11 }, view: {} },
} as const
const panelSf = (isPlaced: boolean, isShown: boolean) => ({ id: 'sf-estado', title: 'Software Factory', isShown, isFocused: false, isPlaced })
const conCaja = async (m: Motor, paneles: () => unknown[]) => {
  await preparar(m, { paneles })
  const ui = await m[0].ui.mount(CAJA)
  const caja = await hay(ui, { type: 'Text', text: /\/sf abre el panel/ })
  await ui.unmount()
  return caja
}

// Con el panel a la vista, la caja repetiría lo mismo: no sale (decisión 164, corregida tras probarla).
test('Caja: con el panel a la vista, no sale', async (...m) => {
  expect(await conCaja(m, () => [panelSf(true, true)])).toBe(false)
})

test('Caja: con el panel detrás de otra pestaña, sale', async (...m) => {
  expect(await conCaja(m, () => [panelSf(true, false)])).toBe(true)
})

test('Caja: con el panel abierto sin colocar (terminal estrecho), sale', async (...m) => {
  expect(await conCaja(m, () => [panelSf(false, false)])).toBe(true)
})

// Sus avisos, como los del panel: fondo blanco y letra oscura (decisión 164).
test('Caja: con la cola ilegible, el aviso en blanco con letra oscura', async (...m) => {
  await preparar(m, { paneles: () => [panelSf(true, false)], extra: { [COLA]: '{ roto' } })
  const ui = await m[0].ui.mount(CAJA)
  const texto = /^⚠ revisar \.sf\/peticiones\.json$/
  expect(((await ui.find({ type: 'Text', text: texto })) as ConProps).props.color).toBe('#1a1a1a')
  expect(((await ui.findAll({ type: 'Box', text: texto })) as ConProps[]).some(b => b.props.backgroundColor === '#ffffff')).toBe(true)
  await ui.unmount()
})

// ── La configuración del proyecto (informe «Configuración inicial», tarea 193) ──
const DEMO_CONF = (campos: Record<string, unknown> = {}) => ({ '/sf/.sf/proyecto.json': JSON.stringify({ sf: '0.32.3', proyecto: 'Demo', ...campos }) })
const GIT_CONFIG = (remotos: Record<string, string>) => ({
  '/sf/.git/config': `[core]\n\tbare = false\n${Object.entries(remotos).map(([n, u]) => `[remote "${n}"]\n\turl = ${u}\n\tfetch = +refs/heads/*:refs/remotes/${n}/*\n`).join('')}[branch "develop"]\n\tremote = origin\n`,
})
const lineaCaja = async (m: Motor, extra: Record<string, string>) => {
  await preparar(m, { sinMarca: true, paneles: () => [panelSf(true, false)], extra: { ...GIT('ref: refs/heads/develop\n'), ...extra } })
  const ui = await m[0].ui.mount(CAJA)
  const textos = ((await ui.findAll({ type: 'Text', text: /./ })) as { text?: string }[]).map(t => String(t.text ?? ''))
  await ui.unmount()
  return textos
}
const ESTADO_VISION = { '/sf/.sf/estado.json': JSON.stringify({ fase: 'vision', hechas: [] }) }

test('Configuración: con metodología, la caja da la fase; sin ella, ni la fase ni «fase sin declarar», aunque haya estado.json', async (...m) => {
  expect(await lineaCaja(m, { ...DEMO_CONF(), ...ESTADO_VISION })).toContain('SF 0.32.3 · Demo · 1/7 Visión')
})

test('Configuración: sin metodología, la caja no da fase ni la pide', async (...m) => {
  const textos = await lineaCaja(m, { ...DEMO_CONF({ metodologia: false }), ...ESTADO_VISION })
  expect(textos).toContain('SF 0.32.3 · Demo')
  expect(textos.some(t => /fase|Visión/.test(t))).toBe(false)
})

test('Configuración: sin kanban, ni falla ni avisa', async (...m) => {
  const textos = await lineaCaja(m, { ...DEMO_CONF(), ...GIT_CONFIG({ origin: 'https://github.com/x/demo.git' }) })
  expect(textos.some(t => /revisar|kanban/i.test(t))).toBe(false)
})

const AVISOS_CONF: [string, Record<string, string>, RegExp][] = [
  ['un remoto que no existe', { ...DEMO_CONF({ remoto: 'PoseTracker' }), ...GIT_CONFIG({ origin: 'https://github.com/x/demo.git' }) }, /no existe el remoto PoseTracker/],
  ['un remoto fuera de GitHub', { ...DEMO_CONF(), ...GIT_CONFIG({ origin: 'git@gitlab.com:x/demo.git' }) }, /el remoto origin no apunta a GitHub/],
  ['un valor que no se entiende', { ...DEMO_CONF({ commits: 'gitmoji' }), ...GIT_CONFIG({ origin: 'git@github.com:x/demo.git' }) }, /no se entiende commits/],
]
for (const [caso, extra, aviso] of AVISOS_CONF) {
  test(`Configuración: con ${caso}, la caja pide revisar .sf/`, async (...m) => {
    expect((await lineaCaja(m, extra)).some(t => /revisar \.sf\/$/.test(t))).toBe(true)
  })
  test(`Configuración: con ${caso}, el panel lo dice en sus avisos`, async (...m) => {
    const { reloj } = await preparar(m, { reloj: true, sinMarca: true, extra: { ...GIT('ref: refs/heads/develop\n'), ...extra } })
    expect(await avisoAtraso(m, reloj)).toMatch(aviso)
  })
}

test('Configuración: el push pendiente se mira en el remoto configurado', async (...m) => {
  const cola: Pet[] = [{ id: 12, texto: 'Lista', estado: 'en-observacion', historial: [ev('a-observacion', 'develop abc1234'), ev('push-fallido', 'fatal: sin red')] }]
  const { ordenes } = await preparar(m, { sinMarca: true, cola, extra: { ...GIT('ref: refs/heads/develop\n'), ...DEMO_CONF({ remoto: 'PoseTracker' }) } })
  expect(ordenes).toContain('git merge-base --is-ancestor abc1234 PoseTracker/develop')
  expect(ordenes.some(o => o.endsWith('origin/develop'))).toBe(false)
})

test('Configuración: los commits de una tarea en develop, con «(N)» o con el trailer, sin los revertidos', () => {
  const lineas = ['h6\tRevert "feat: otra"\t', 'h5\tfeat: otra\t9', 'h4\tTercera (8)\t', 'h3\tRevert "Segunda (8)"\t', 'h2\tSegunda (8)\t', 'h1\tfeat: primera\t9', 'h0\tSin tarea\t']
  expect(tareasEnDevelop(lineas)).toEqual({ '8': ['h4'] })
  expect(tareasEnDevelop(lineas.slice(1))).toEqual({ '9': ['h5', 'h1'], '8': ['h4'] })
})

test('Configuración: subir la versión de un manifiesto .json o pyproject.toml, también si no la tiene', () => {
  expect(subirManifiesto('{\n  "name": "x",\n  "version": "1.0.0"\n}\n', 'package.json', '1.1.0')).toEqual({ texto: '{\n  "name": "x",\n  "version": "1.1.0"\n}\n', antes: '1.0.0' })
  expect(subirManifiesto('{\n  "name": "x"\n}\n', 'web/package.json', '1.1.0')).toEqual({ texto: '{\n  "version": "1.1.0",\n  "name": "x"\n}\n', antes: null })
  expect(subirManifiesto('[build-system]\nrequires = []\n\n[project]\nname = "x"\nversion = "0.2.0"\n\n[tool.x]\nversion = "9"\n', 'pyproject.toml', '0.3.0')).toEqual({
    texto: '[build-system]\nrequires = []\n\n[project]\nname = "x"\nversion = "0.3.0"\n\n[tool.x]\nversion = "9"\n',
    antes: '0.2.0',
  })
  expect(subirManifiesto('[project]\nname = "x"\n', 'pyproject.toml', '0.3.0')).toEqual({ texto: '[project]\nversion = "0.3.0"\nname = "x"\n', antes: null })
  expect(subirManifiesto('[tool.ruff]\n', 'pyproject.toml', '0.3.0')).toBe(null)
  expect(subirManifiesto('<project/>', 'pom.xml', '0.3.0')).toBe(null)
})

test('Configuración: las reglas del método y la línea de convenciones, según la configuración', async (...m) => {
  const plugin = { '/plugin/templates/claude-sf.md': '# Software Factory\n\n- **Cola:** x.\n', '/plugin/templates/claude-sf-metodologia.md': '<!-- sf -->\n\n# Software Factory: metodología\n', '/plugin/skills/orquestacion/SKILL.md': '# Orquestación\n' }
  await preparar(m, { sinMarca: true, extra: { ...plugin, ...DEMO_CONF({ idioma: 'en', commits: 'conventional', remoto: 'gh', rama_main: 'master' }) } })
  const [c] = (await m[0].classic.SessionStart({ source: 'startup' })).additionalContext ?? []
  expect(c).toMatch(/# Software Factory\n\n- \*\*Cola:\*\* x\.\n*\n# Software Factory: metodología/)
  expect(c).toContain('Convenciones del proyecto: idioma en; commits conventional commits, con el número de la tarea como el trailer «SF-Tarea: N» al pie; remoto gh; se publica en master, que hace de main.')
})

test('Configuración: sin metodología, el mod no entrega las reglas del método', async (...m) => {
  const plugin = { '/plugin/templates/claude-sf.md': '# Software Factory\n', '/plugin/templates/claude-sf-metodologia.md': '# Software Factory: metodología\n', '/plugin/skills/orquestacion/SKILL.md': '# Orquestación\n' }
  await preparar(m, { sinMarca: true, extra: { ...plugin, ...DEMO_CONF({ metodologia: false }) } })
  const [c] = (await m[0].classic.SessionStart({ source: 'startup' })).additionalContext ?? []
  expect(c).toContain('# Software Factory')
  expect(c).not.toContain('metodología')
  expect(c).toContain('Convenciones del proyecto: idioma es; commits libres, con el número de la tarea como «(N)» al final del título; remoto origin.')
})

// RELEASE (decisión del propietario, 2026-10-29): en la primera fila, publica develop en main con su tag, sin Claude.
const RAMAS_RELEASE = { '/sf/.git/HEAD': 'ref: refs/heads/develop\n', '/sf/.git/refs/heads/develop': 'abc', '/sf/.git/refs/heads/main': 'abc' }
const MANIFIESTO = '/sf/plugins/sf/.claude-plugin/plugin.json'
const MANIFIESTO_034 = '{\n  "name": "sf",\n  "version": "0.34.3",\n  "description": "x"\n}\n'
const CON_OBSERVACION: Pet[] = [
  { id: 1, texto: 'En curso', estado: 'en-curso' },
  { id: 4, texto: 'Probar A', estado: 'en-observacion', prueba: 'mirar' },
  { id: 47, texto: 'Probar B', estado: 'en-observacion', prueba: 'mirar' },
]
const ORDEN_SF = [
  'git rev-parse -q --verify refs/heads/main',
  'git rev-parse -q --verify refs/heads/develop',
  'git symbolic-ref --short -q HEAD',
  'git status --porcelain --untracked-files=no',
  'git merge-base --is-ancestor main develop',
  'git rev-parse -q --verify refs/tags/v0.35.0',
  'git add plugins/sf/.claude-plugin/plugin.json',
  'git commit -q -F -',
  'git fetch . develop:main',
  'git tag -a v0.35.0 -m sf 0.35.0 main',
  'git push origin develop main v0.35.0',
]
type OpcRelease = { git?: Git; extra?: Record<string, string>; sinMarca?: boolean; sinMain?: boolean; cola?: Pet[] }
const release = async (m: Motor, { git = {}, extra = {}, sinMarca = false, sinMain = false, cola = INICIAL }: OpcRelease = {}) => {
  const ramas: Record<string, string> = { ...RAMAS_RELEASE }
  if (sinMain) delete ramas['/sf/.git/refs/heads/main']
  const identidad = sinMarca ? { '/sf/.sf/proyecto.json': JSON.stringify({ sf: '0.32.3', proyecto: 'Demo' }) } : { [MANIFIESTO]: MANIFIESTO_034 }
  // La versión sale del último tag, también en la SF (decisión 226): la del manifiesto, si el caso no da otros.
  const conTags = sinMarca || git.tags !== undefined ? git : { ...git, tags: 'v0.34.3' }
  const r = await preparar(m, { cola, reloj: true, sinMarca, git: conTags, extra: { ...ramas, ...identidad, ...extra } })
  const ui = await m[0].ui.mount({ ...ANCHO, surface: 'terminal' })
  return { ...r, ui }
}
const publicando = (v: string) => new RegExp(`¿Publicar v${v.replace(/\./g, '\\.')}\\? sí`)
const elegir = async (ui: { press: (q: object) => Promise<unknown> }, v: string, confirmar = true) => {
  await ui.press({ key: 'release' })
  await ui.press({ key: `release-v:${v}` })
  if (confirmar) await ui.press({ key: `release-v:${v}` })
}

test('RELEASE: en la primera fila, a la izquierda de TURBO; el primer clic da patch, minor y major', async (...m) => {
  const { ordenes, ui } = await release(m)
  const raiz = (await ui.drawn()) as Nodo
  const t1 = JSON.stringify(fila(raiz, ' TURBO ', 'SF 0.32.3'))
  expect(t1.indexOf(' RELEASE ') >= 0 && t1.indexOf(' RELEASE ') < t1.indexOf(' TURBO ')).toBe(true)
  await ui.press({ key: 'release' })
  for (const v of ['0.34.4', '0.35.0', '1.0.0']) expect(await hay(ui, { type: 'Button', key: `release-v:${v}` })).toBe(true)
  expect(await ui.find({ type: 'Button', key: 'release' })).toBe(undefined)
  expect(ordenes.some(o => /^git (add|commit|fetch|tag -a|push|merge-base)/.test(o))).toBe(false)
  await ui.unmount()
})

test('RELEASE: al elegir, pide confirmar y avisa de lo que queda en observación; a los 5 s o con otro clic vuelve a RELEASE', async (...m) => {
  const { archivos, ordenes, reloj, ui } = await release(m, { cola: CON_OBSERVACION })
  await elegir(ui, '0.35.0', false)
  expect(await hay(ui, { type: 'Text', text: publicando('0.35.0') })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /2 en observación: 4, 47/ })).toBe(true)
  await reloj!.advance(4000)
  expect(await hay(ui, { type: 'Text', text: publicando('0.35.0') })).toBe(true)
  await reloj!.advance(1500)
  expect(await hay(ui, { type: 'Button', key: 'release' })).toBe(true)
  expect(await ui.find({ type: 'Text', text: /en observación: 4/ })).toBe(undefined)
  // Con un clic en otro botón, también.
  await elegir(ui, '0.34.4', false)
  await ui.press({ key: 'sec:hecho' })
  expect(await hay(ui, { type: 'Button', key: 'release' })).toBe(true)
  // Y la lista de versiones, sin elegir ninguna, también vuelve a los 5 s.
  await ui.press({ key: 'release' })
  await reloj!.advance(5500)
  expect(await hay(ui, { type: 'Button', key: 'release' })).toBe(true)
  expect(archivos[MANIFIESTO]).toBe(MANIFIESTO_034)
  expect(ordenes.some(o => /^git (add|commit|fetch|tag -a|push)/.test(o))).toBe(false)
  await ui.unmount()
})

test('RELEASE: sin nada en observación, no avisa', async (...m) => {
  const { ui } = await release(m, { cola: [{ id: 1, texto: 'En curso', estado: 'en-curso' }] })
  await elegir(ui, '0.35.0', false)
  expect(await hay(ui, { type: 'Text', text: publicando('0.35.0') })).toBe(true)
  expect(await ui.find({ type: 'Text', text: /en observación:/ })).toBe(undefined)
  await ui.unmount()
})

test('RELEASE: confirmado, sube la versión con su commit, fast-forward, tag y push, en orden y sin Claude', async (...m) => {
  const { archivos, ordenes, entradas, toasts, prompts, ui } = await release(m)
  await elegir(ui, '0.35.0')
  const posiciones = ORDEN_SF.map(o => ordenes.indexOf(o))
  expect(posiciones.every((x, i) => x >= 0 && (i === 0 || x > posiciones[i - 1]!))).toBe(true)
  expect(archivos[MANIFIESTO]).toBe(MANIFIESTO_034.replace('0.34.3', '0.35.0'))
  expect(entradas).toEqual(['sf 0.35.0\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n'])
  expect(ordenes.some(o => o.startsWith('git switch') || o.startsWith('git merge '))).toBe(false)
  expect(toasts).toContain('Publicada v0.35.0')
  expect(prompts).toHaveLength(0)
  await ui.unmount()
})

test('RELEASE: si falla el push, lo local queda hecho y lo dice', async (...m) => {
  const { archivos, ordenes, toasts, ui } = await release(m, { git: { pushFalla: true } })
  await elegir(ui, '0.34.4')
  expect(ordenes).toContain('git tag -a v0.34.4 -m sf 0.34.4 main')
  expect(archivos[MANIFIESTO]).toContain('"version": "0.34.4"')
  expect(toasts.some(t => t.startsWith('Publicada v0.34.4 en local; falta el push') && t.includes('sin red'))).toBe(true)
  await ui.unmount()
})

test('RELEASE: revisa lo que sale desde el último tag, con el remoto de la configuración, como la acción release, antes de tocar nada (252, 332)', async (...m) => {
  const { ordenes, toasts, ui } = await release(m)
  await elegir(ui, '0.35.0')
  const i = ordenes.indexOf('revision --repo /sf --remoto origin --hasta develop --json --decidir --accion release --repetir vuelve a pulsar RELEASE y elige v0.35.0 --desde v0.34.3')
  expect(i).toBeGreaterThanOrEqual(0)
  expect(i).toBeLessThan(ordenes.indexOf('git add plugins/sf/.claude-plugin/plugin.json'))
  expect(toasts).toContain('Publicada v0.35.0')
  await ui.unmount()
})

// La decisión (bloquear o pedir permiso) y su texto son de revision_publica.py, el mismo para el push del cierre (259).
for (const accion of ['bloquear', 'permiso']) {
  test(`RELEASE: si la revisión dice ${accion}, no publica y enseña su mensaje (259)`, async (...m) => {
    const mensaje = `hay 6 cosas que quizá no deban publicarse: abc0001 docs/a.md: correo «p1@ejemplo.es» y 5 más (${accion})`
    const { archivos, ordenes, toasts, ui } = await release(m, { git: { revision: { ok: true, accion, mensaje, hallazgos: [{}] } } })
    await elegir(ui, '0.35.0')
    expect(toasts).toContain(`RELEASE no publica: ${mensaje}`)
    expect(archivos[MANIFIESTO]).toBe(MANIFIESTO_034)
    expect(ordenes.some(o => /^git (add|commit|fetch|tag -a|push)/.test(o))).toBe(false)
    await ui.unmount()
  })
}

test('RELEASE: si la revisión no responde, no publica (252)', async (...m) => {
  const { archivos, ordenes, toasts, ui } = await release(m, { git: { revision: null } })
  await elegir(ui, '0.35.0')
  expect(toasts.some(x => /no se pudo revisar lo que sale.*No se publica/.test(x))).toBe(true)
  expect(archivos[MANIFIESTO]).toBe(MANIFIESTO_034)
  expect(ordenes.some(o => /^git (add|commit|fetch|tag -a|push)/.test(o))).toBe(false)
  await ui.unmount()
})

const RECHAZOS: [string, OpcRelease, RegExp][] = [
  ['sin main', { sinMain: true }, /no tiene la rama main/],
  ['fuera de develop', { extra: { '/sf/.git/HEAD': 'ref: refs/heads/feature/9-x\n' } }, /la rama activa es feature\/9-x.*git switch develop/],
  ['con cambios sin commit', { git: { status: ' M a.md\n' } }, /cambios sin commit/],
  ['sin fast-forward', { git: { noAncestro: true } }, /main tiene commits que no están en develop.*git merge main/],
  ['con el tag ya creado', { git: { tags: 'v0.34.3\nv0.35.0' } }, /el tag v0\.35\.0 ya existe/],
]
for (const [caso, opc, aviso] of RECHAZOS) {
  test(`RELEASE: ${caso}, no hace nada y dice cómo arreglarlo`, async (...m) => {
    const { archivos, ordenes, toasts, ui } = await release(m, opc)
    await elegir(ui, '0.35.0')
    expect(toasts.some(t => aviso.test(t))).toBe(true)
    expect(archivos[MANIFIESTO]).toBe(MANIFIESTO_034)
    expect(ordenes.some(o => /^git (add|commit|fetch|tag -a|push)/.test(o))).toBe(false)
    await ui.unmount()
  })
}

test('RELEASE: en un proyecto sin plugin.json, las versiones salen del último tag y no hay commit de versión', async (...m) => {
  const { archivos, ordenes, entradas, toasts, ui } = await release(m, { sinMarca: true, git: { tags: 'v2.10.1\nv2.9.0\nv-raro\nv1.0.0' } })
  const manifiesto = MANIFIESTO in archivos
  await ui.press({ key: 'release' })
  for (const v of ['2.10.2', '2.11.0', '3.0.0']) expect(await hay(ui, { type: 'Button', key: `release-v:${v}` })).toBe(true)
  await ui.press({ key: 'release-v:2.11.0' })
  await ui.press({ key: 'release-v:2.11.0' })
  expect(ordenes).toContain('git tag --list v* --sort=-v:refname')
  expect(ordenes.some(o => o.startsWith('git add') || o.startsWith('git commit'))).toBe(false)
  expect(entradas).toHaveLength(0)
  const orden = ['git fetch . develop:main', 'git tag -a v2.11.0 -m v2.11.0 main', 'git push origin develop main v2.11.0'].map(o => ordenes.indexOf(o))
  expect(orden.every((x, i) => x >= 0 && (i === 0 || x > orden[i - 1]!))).toBe(true)
  expect(MANIFIESTO in archivos).toBe(manifiesto)
  expect(toasts).toContain('Publicada v2.11.0')
  await ui.unmount()
})

test('RELEASE: sin plugin.json ni tags, pregunta la primera versión: v0.1.0 o v1.0.0', async (...m) => {
  const { ordenes, toasts, ui } = await release(m, { sinMarca: true })
  await ui.press({ key: 'release' })
  expect(await hay(ui, { type: 'Text', text: /¿Primera versión\?/ })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'release-v:0.1.0' })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'release-v:1.0.0' })).toBe(true)
  await ui.press({ key: 'release-v:0.1.0' })
  expect(await hay(ui, { type: 'Text', text: publicando('0.1.0') })).toBe(true)
  await ui.press({ key: 'release-v:0.1.0' })
  expect(ordenes.some(o => o.startsWith('git add') || o.startsWith('git commit'))).toBe(false)
  expect(ordenes).toContain('git push origin develop main v0.1.0')
  expect(toasts).toContain('Publicada v0.1.0')
  await ui.unmount()
})

test('RELEASE: con la configuración, publica en rama_main, sube sus manifiestos en un commit vX.Y.Z, avisa del que no cuadra y hace push a su remoto', async (...m) => {
  const conf = { sf: '0.32.3', proyecto: 'Demo', remoto: 'PoseTracker', rama_main: 'master', manifiesto: ['package.json', 'backend/pyproject.toml'] }
  const { archivos, ordenes, entradas, toasts, ui } = await release(m, {
    sinMarca: true,
    sinMain: true,
    git: { tags: 'v2.10.1\nv2.9.0' },
    extra: {
      '/sf/.git/refs/heads/master': 'abc',
      '/sf/.sf/proyecto.json': JSON.stringify(conf),
      '/sf/package.json': '{\n  "name": "demo",\n  "version": "2.10.1"\n}\n',
      '/sf/backend/pyproject.toml': '[project]\nname = "demo"\nversion = "2.9.0"\n',
    },
  })
  await elegir(ui, '2.11.0')
  expect(archivos['/sf/package.json']).toContain('"version": "2.11.0"')
  expect(archivos['/sf/backend/pyproject.toml']).toContain('version = "2.11.0"')
  // Sin `coautor` en la configuración, el commit va sin línea de coautoría (238).
  expect(entradas).toEqual(['v2.11.0\n'])
  const orden = [
    'git rev-parse -q --verify refs/heads/master',
    'git merge-base --is-ancestor master develop',
    'git add package.json backend/pyproject.toml',
    'git commit -q -F -',
    'git fetch . develop:master',
    'git tag -a v2.11.0 -m v2.11.0 master',
    'git push PoseTracker develop master v2.11.0',
  ].map(o => ordenes.indexOf(o))
  expect(orden.every((x, i) => x >= 0 && (i === 0 || x > orden[i - 1]!))).toBe(true)
  expect(ordenes.some(o => / main\b|origin/.test(o) && o.startsWith('git '))).toBe(false)
  expect(toasts).toContain('Publicada v2.11.0. Aviso: backend/pyproject.toml decía 2.9.0, no 2.10.1.')
  await ui.unmount()
})

test('RELEASE: el commit de la versión lleva la línea de `coautor` de la configuración (238)', async (...m) => {
  const conf = { sf: '0.32.3', proyecto: 'Demo', manifiesto: 'package.json', coautor: 'Ana <ana@example.com>' }
  const { entradas, ui } = await release(m, {
    sinMarca: true,
    git: { tags: 'v2.10.1' },
    extra: { '/sf/.sf/proyecto.json': JSON.stringify(conf), '/sf/package.json': '{\n  "version": "2.10.1"\n}\n' },
  })
  await elegir(ui, '2.11.0')
  expect(entradas).toEqual(['v2.11.0\n\nCo-Authored-By: Ana <ana@example.com>\n'])
  await ui.unmount()
})

test('RELEASE: con rama_main sin crear, dice que falta esa rama', async (...m) => {
  const { toasts, ui } = await release(m, { sinMarca: true, git: { tags: 'v1.0.0' }, extra: { '/sf/.sf/proyecto.json': JSON.stringify({ sf: '0.32.3', proyecto: 'Demo', rama_main: 'master' }) } })
  await elegir(ui, '1.0.1')
  expect(toasts.some(t => /no tiene la rama master/.test(t))).toBe(true)
  await ui.unmount()
})

test('RELEASE: fuera de un proyecto con SF no sale', async (...m) => {
  await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await ui.find({ type: 'Button', key: 'release' })).toBe(undefined)
  await ui.unmount()
})

// ACTUALIZAR (decisión del propietario, 2026-10-29): sale solo con una versión publicada mayor que la instalada de
// sf@softwarefactory en algún scope del proyecto; actualiza con claude plugin update, sin Claude.
const USER_100: Instalada = { scope: 'user', version: '1.0.0' }
const LOCAL_100: Instalada = { scope: 'local', projectPath: RAIZ, version: '1.0.0' }
const UPDATE = (scope: string) => `claude plugin update sf@softwarefactory --scope ${scope}`
const LS_REMOTE = 'git ls-remote --tags https://github.com/jumibot/SoftwareFactory.git'
const REFRESCO = 'claude plugin marketplace update softwarefactory'
// corre: la versión del plugin que corre en la sesión (sin ella, la instalada, 1.0.0); copia: corre la copia de trabajo.
// deps: las dependencies del plugin.json de cada versión instalada de sf; otros: otros plugins ya instalados;
// proyecto: el .sf/proyecto.json del proyecto.
// ajustes: los settings de cada archivo (ruta → contenido), para enabledPlugins.
type OpcActualizar = { entradas?: Instalada[]; remoto?: string | null; updateFalla?: string[]; catalogoFalla?: boolean; alDia?: string[]; corre?: string; copia?: boolean; deps?: Record<string, unknown[]>; otros?: Record<string, Instalada[]>; installFalla?: string[]; proyecto?: object; ajustes?: Record<string, object> }
// La primera comprobación sale de un temporizador, al segundo de empezar.
const actualizar = async (m: Motor, { entradas = [USER_100, LOCAL_100], remoto = remotos('0.9.0', '1.1.0', '1.0.0'), updateFalla, catalogoFalla, alDia, corre = '1.0.0', copia, deps = {}, otros = {}, installFalla, proyecto, ajustes = {} }: OpcActualizar = {}) => {
  const manifiesto = { '/plugin/plugin.json': JSON.stringify({ name: 'sf', version: corre }) }
  const base = instalado(entradas)
  const registro = JSON.parse(base[INSTALADAS]!) as { plugins: Record<string, unknown> }
  Object.assign(registro.plugins, otros)
  const manifiestos = Object.fromEntries(Object.entries(deps).map(([v, d]) => [`/home/.claude/plugins/cache/softwarefactory/sf/${v}/.claude-plugin/plugin.json`, JSON.stringify({ name: 'sf', version: v, dependencies: d })]))
  const extra = { ...GIT('ref: refs/heads/develop\n'), ...base, [INSTALADAS]: JSON.stringify(registro), ...manifiesto, ...manifiestos, ...(proyecto ? { '/sf/.sf/proyecto.json': JSON.stringify(proyecto) } : {}), ...Object.fromEntries(Object.entries(ajustes).map(([r, a]) => [r, JSON.stringify(a)])) }
  const r = await preparar(m, { reloj: true, copia, git: { remoto, updateFalla, catalogoFalla, alDia, installFalla }, extra })
  const ui = await m[0].ui.mount({ ...ANCHO, surface: 'terminal' })
  await r.reloj!.advance(1000)
  return { ...r, ui }
}
const updates = (ordenes: string[]) => ordenes.filter(o => o.startsWith('claude plugin update '))

test('ACTUALIZAR: con un tag mayor que la instalada, sale a la izquierda de RELEASE; ninguna orden hasta confirmar', async (...m) => {
  const { ordenes, toasts, ui } = await actualizar(m)
  const raiz = (await ui.drawn()) as Nodo
  const t1 = JSON.stringify(fila(raiz, ' TURBO ', 'SF 1.0.0'))
  expect(t1.indexOf(' ACTUALIZAR ') >= 0 && t1.indexOf(' ACTUALIZAR ') < t1.indexOf(' RELEASE ')).toBe(true)
  expect(JSON.stringify(hijos(fila(raiz, ' TURBO ', 'SF 1.0.0')!)[0]).includes(' ACTUALIZAR ')).toBe(true)
  expect(ordenes).toContain(LS_REMOTE)
  expect(updates(ordenes)).toHaveLength(0)
  expect(toasts).toHaveLength(0)
  await ui.unmount()
})

const SIN_BOTON: [string, OpcActualizar][] = [
  ['con el tag más alto igual a la instalada', { remoto: remotos('0.9.0', '1.0.0') }],
  ['si git ls-remote falla', { remoto: null }],
  ['sin tags vX.Y.Z', { remoto: 'abc\trefs/tags/v-raro\n' }],
  ['si solo está desactualizado el local de otro proyecto', { entradas: [USER_100, LOCAL_100, { scope: 'local', projectPath: '/otro', version: '0.5.0' }], remoto: remotos('1.0.0') }],
  ['sin el plugin instalado en ningún scope del proyecto', { entradas: [{ scope: 'local', projectPath: '/otro', version: '0.5.0' }] }],
  ['si la sesión corre la copia de trabajo, aunque sea más vieja', { remoto: remotos('1.0.0'), corre: '0.9.0', copia: true }],
  ['si la sesión corre una versión más nueva que la instalada y la publicada', { remoto: remotos('1.0.0'), corre: '1.1.0' }],
  // La sesión de la SF (tarea 229, reabierta): sf@softwarefactory, desactivado en sus ajustes locales, con una copia
  // local vieja y la de usuario al día; corre el plugin de desarrollo, de la copia de trabajo.
  ['con sf@softwarefactory desactivado en el proyecto y una copia local vieja, en la copia de trabajo', { entradas: [{ scope: 'user', version: '1.1.0' }, LOCAL_100], copia: true, ajustes: { [AJUSTES]: { enabledPlugins: { 'sf@softwarefactory-dev': true, 'sf@softwarefactory': false } } } }],
  ['con sf@softwarefactory desactivado en el proyecto, aunque lo instalado vaya por detrás', { ajustes: { [AJUSTES]: { enabledPlugins: { 'sf@softwarefactory': false } } } }],
  ['con sf@softwarefactory desactivado en los ajustes del usuario y sin valor en el proyecto', { corre: '0.9.0', ajustes: { '/home/.claude/settings.json': { enabledPlugins: { 'sf@softwarefactory': false } } } }],
]
for (const [caso, opc] of SIN_BOTON) {
  test(`ACTUALIZAR: no sale ${caso}, y no avisa`, async (...m) => {
    const { toasts, ui } = await actualizar(m, opc)
    expect(await ui.find({ type: 'Button', key: 'actualizar' })).toBe(undefined)
    expect(await ui.find({ type: 'Button', key: 'refrescar' })).toBe(undefined)
    expect(await ui.find({ type: 'Text', text: /ACTUALIZAR|REFRESCAR/ })).toBe(undefined)
    expect(toasts).toHaveLength(0)
    await ui.unmount()
  })
}

test('ACTUALIZAR: el primer clic pide confirmar; a los 5 s o con otro clic vuelve, sin actualizar', async (...m) => {
  const { ordenes, reloj, ui } = await actualizar(m)
  await ui.press({ key: 'actualizar' })
  expect(await hay(ui, { type: 'Text', text: /¿Actualizar a v1\.1\.0\? sí/ })).toBe(true)
  await reloj!.advance(4000)
  expect(await hay(ui, { type: 'Text', text: /¿Actualizar a v1\.1\.0\? sí/ })).toBe(true)
  await reloj!.advance(1500)
  expect(await hay(ui, { type: 'Text', text: / ACTUALIZAR / })).toBe(true)
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'sec:hecho' })
  expect(await hay(ui, { type: 'Text', text: / ACTUALIZAR / })).toBe(true)
  expect(updates(ordenes)).toHaveLength(0)
  await ui.unmount()
})

test('ACTUALIZAR: confirmado, claude plugin update en el scope user y en el local del proyecto, no en el de otro; avisa de reiniciar y desaparece', async (...m) => {
  const otro: Instalada = { scope: 'local', projectPath: '/otro', version: '0.5.0' }
  // El local del proyecto, con la ruta escrita con barras invertidas y barra final: es la misma carpeta.
  const local: Instalada = { scope: 'local', projectPath: '\\sf\\', version: '1.0.0' }
  const { ordenes, toasts, prompts, cwds, ui } = await actualizar(m, { entradas: [USER_100, otro, local] })
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  expect(updates(ordenes)).toEqual([UPDATE('user'), UPDATE('local')])
  expect(cwds.every(c => c === RAIZ)).toBe(true)
  expect(toasts).toContain('Actualizado a v1.1.0: reinicia Claude Code')
  expect(prompts).toHaveLength(0)
  expect(await ui.find({ type: 'Button', key: 'actualizar' })).toBe(undefined)
  await ui.unmount()
})

test('ACTUALIZAR: refresca el catálogo antes de actualizar, una vez', async (...m) => {
  const { ordenes, ui } = await actualizar(m)
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  expect(ordenes.filter(o => o.startsWith('claude '))).toEqual([REFRESCO, UPDATE('user'), UPDATE('local')])
  await ui.unmount()
})

test('ACTUALIZAR: si no se puede refrescar el catálogo, no actualiza, avisa y el botón sigue', async (...m) => {
  const { ordenes, toasts, ui } = await actualizar(m, { catalogoFalla: true })
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  expect(updates(ordenes)).toEqual([])
  expect(toasts.some(t => /^ACTUALIZAR: no se pudo refrescar el catálogo softwarefactory \(Failed to update marketplace\)/.test(t))).toBe(true)
  expect(toasts.some(t => t.includes('reinicia'))).toBe(false)
  expect(await hay(ui, { type: 'Button', key: 'actualizar' })).toBe(true)
  await ui.unmount()
})

test('ACTUALIZAR: en rojo, distinto del violeta de RELEASE, también al confirmar', async (...m) => {
  const { ui } = await actualizar(m)
  const color = async (text: RegExp) => (await ui.find({ type: 'Text', text }))?.props.color
  expect(await color(/ ACTUALIZAR /)).toBe('#f87171')
  expect(await color(/ RELEASE /)).toBe('#c084fc')
  await ui.press({ key: 'actualizar' })
  expect(await color(/¿Actualizar a v1\.1\.0\? sí/)).toBe('#f87171')
  await ui.unmount()
})

test('ACTUALIZAR: si Claude Code ya tenía la versión, la anota en el registro y no pide reiniciar', async (...m) => {
  const otro: Instalada = { scope: 'local', projectPath: '/otro', version: '0.5.0' }
  const { archivos, toasts, ui } = await actualizar(m, { entradas: [USER_100, LOCAL_100, otro], alDia: ['user', 'local'] })
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  const sf = (JSON.parse(archivos[INSTALADAS]!) as { plugins: Record<string, { scope: string; version: string; projectPath?: string }[]> }).plugins['sf@softwarefactory']!
  expect(sf.map(x => [x.scope, x.projectPath ?? '', x.version])).toEqual([['user', '', '1.1.0'], ['local', RAIZ, '1.1.0'], ['local', '/otro', '0.5.0']])
  expect(toasts).toContain('sf ya estaba en v1.1.0: anotado en el registro')
  expect(toasts.some(t => t.includes('reinicia'))).toBe(false)
  expect(await ui.find({ type: 'Button', key: 'actualizar' })).toBe(undefined)
  await ui.unmount()
})

test('ACTUALIZAR: con un scope ya al día y otro actualizado, pide reiniciar', async (...m) => {
  const { archivos, toasts, ui } = await actualizar(m, { alDia: ['local'] })
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  const sf = (JSON.parse(archivos[INSTALADAS]!) as { plugins: Record<string, { scope: string; version: string }[]> }).plugins['sf@softwarefactory']!
  expect(sf.map(x => x.version)).toEqual(['1.1.0', '1.1.0'])
  expect(toasts).toContain('Actualizado a v1.1.0: reinicia Claude Code')
  await ui.unmount()
})

test('ACTUALIZAR: solo los scopes desactualizados', async (...m) => {
  const { ordenes, ui } = await actualizar(m, { entradas: [{ scope: 'user', version: '1.1.0' }, LOCAL_100] })
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  expect(updates(ordenes)).toEqual([UPDATE('local')])
  await ui.unmount()
})

test('ACTUALIZAR: si falla un scope, avisa con el error y el botón sigue con ese scope', async (...m) => {
  const { ordenes, toasts, ui } = await actualizar(m, { updateFalla: ['local'] })
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  expect(toasts.some(t => /^ACTUALIZAR: no se pudo actualizar a v1\.1\.0 \(local: Failed to update plugin in local scope\)/.test(t))).toBe(true)
  expect(toasts.some(t => t.includes('reinicia'))).toBe(false)
  expect(await hay(ui, { type: 'Button', key: 'actualizar' })).toBe(true)
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  expect(updates(ordenes)).toEqual([UPDATE('user'), UPDATE('local'), UPDATE('local')])
  await ui.unmount()
})

// La sesión sigue con un plugin más viejo que el instalado: otra sesión lo actualizó (tarea 229). Sin scopes por
// actualizar, el botón es REFRESCAR y recarga los plugins, sin claude plugin update (decisión 177).
test('REFRESCAR: con lo instalado al día y la sesión en una versión más vieja, sale en lugar de ACTUALIZAR y recarga los plugins', async (...m) => {
  const { comandos, ordenes, toasts, ui } = await actualizar(m, { remoto: remotos('1.0.0'), corre: '0.9.0' })
  expect(await hay(ui, { type: 'Text', text: / REFRESCAR / })).toBe(true)
  expect(await ui.find({ type: 'Text', text: /ACTUALIZAR/ })).toBe(undefined)
  expect(await ui.find({ type: 'Button', key: 'actualizar' })).toBe(undefined)
  await ui.press({ key: 'refrescar' })
  expect(await hay(ui, { type: 'Text', text: /¿Refrescar a v1\.0\.0\? sí/ })).toBe(true)
  expect(comandos).not.toContain('reload-plugins')
  await ui.press({ key: 'refrescar' })
  expect(ordenes.filter(o => o.startsWith('claude '))).toEqual([])
  expect(comandos).toContain('reload-plugins')
  expect(toasts).toContain('REFRESCAR: recargando sf v1.0.0…')
  expect(toasts).toContain('REFRESCAR: sf v1.0.0 ya instalada, recargando los plugins')
  expect(await ui.find({ type: 'Button', key: 'refrescar' })).toBe(undefined)
  await ui.unmount()
})

// Las filas del aviso blanco de la cabecera, juntas; vacío si la cabecera está en su turno.
const textoAvisos = async (ui: Montado) =>
  ((await ui.findAll({ type: 'Text', text: /./ })) as { text?: string; props: Record<string, unknown> }[])
    .filter(t => t.props.color === '#1a1a1a')
    .map(t => String(t.text ?? ''))
    .join(' ')

test('REFRESCAR: el primer clic pide confirmar; a los 5 s vuelve, sin recargar', async (...m) => {
  const { comandos, reloj, ui } = await actualizar(m, { remoto: remotos('1.0.0'), corre: '0.9.0' })
  await ui.press({ key: 'refrescar' })
  expect(await hay(ui, { type: 'Text', text: /¿Refrescar a v1\.0\.0\? sí/ })).toBe(true)
  await reloj!.advance(5000)
  expect(await hay(ui, { type: 'Text', text: /¿Refrescar/ })).toBe(false)
  expect(comandos).not.toContain('reload-plugins')
  // Pasado el turno del aviso, la cabecera, con REFRESCAR otra vez.
  if (await textoAvisos(ui)) await ui.press({ key: 'aviso:0' })
  expect(await hay(ui, { type: 'Text', text: / REFRESCAR / })).toBe(true)
  await ui.unmount()
})

test('REFRESCAR: con la sesión más vieja que la instalada, sale aunque git ls-remote falle', async (...m) => {
  const { ui } = await actualizar(m, { remoto: null, corre: '0.9.0' })
  await ui.press({ key: 'refrescar' })
  expect(await hay(ui, { type: 'Text', text: /¿Refrescar a v1\.0\.0\? sí/ })).toBe(true)
  await ui.unmount()
})

// Con REFRESCAR, también un aviso en el carrusel de la cabecera: se ve aunque la cabecera se turne con otros avisos.
test('REFRESCAR: sale el aviso «Esta sesión usa la SF X y está instalada la Y: pulsa REFRESCAR»', async (...m) => {
  const { reloj, ui } = await actualizar(m, { remoto: remotos('1.0.0'), corre: '0.9.0' })
  await reloj!.advance(5000)
  expect((await textoAvisos(ui)).replace(/\s+/g, ' ')).toMatch(/Esta sesión usa la SF 0\.9\.0 y está instalada la 1\.0\.0: pulsa REFRESCAR/)
  await ui.unmount()
})

test('ACTUALIZAR: con una versión publicada sin instalar, no sale el aviso de REFRESCAR', async (...m) => {
  const { reloj, ui } = await actualizar(m, { corre: '0.9.0' })
  await reloj!.advance(5000)
  expect(await ui.find({ type: 'Text', text: /pulsa REFRESCAR/ })).toBe(undefined)
  await ui.unmount()
})

test('ACTUALIZAR: con un scope por detrás, actualiza aunque la sesión también vaya por detrás', async (...m) => {
  const { comandos, ordenes, toasts, ui } = await actualizar(m, { corre: '0.9.0' })
  expect(await ui.find({ type: 'Button', key: 'refrescar' })).toBe(undefined)
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  expect(updates(ordenes)).toEqual([UPDATE('user'), UPDATE('local')])
  expect(comandos).not.toContain('reload-plugins')
  expect(toasts).toContain('Actualizado a v1.1.0: reinicia Claude Code')
  await ui.unmount()
})

// Medida 2 de la decisión 176: claude plugin update no instala las dependencias nuevas, y sin una sf no carga.
const INSTALL = (id: string, scope: string) => `claude plugin install ${id} --scope ${scope}`
const installs = (ordenes: string[]) => ordenes.filter(o => o.startsWith('claude plugin install '))
const DEPS_110 = { '1.1.0': ['nueva@softwarefactory', 'vieja', { name: 'ajena', marketplace: 'otro' }] }
const VIEJA: Record<string, Instalada[]> = { 'vieja@softwarefactory': [{ scope: 'user', version: '1' }] }

test('ACTUALIZAR: tras actualizar, instala las dependencias de la versión nueva que faltan, una vez en el scope de usuario, y luego pide reiniciar', async (...m) => {
  const { ordenes, toasts, ui } = await actualizar(m, { deps: DEPS_110, otros: VIEJA })
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  expect(ordenes.filter(o => o.startsWith('claude '))).toEqual([REFRESCO, UPDATE('user'), UPDATE('local'), INSTALL('nueva@softwarefactory', 'user'), INSTALL('ajena@otro', 'user')])
  expect(toasts).toContain('Actualizado a v1.1.0: reinicia Claude Code')
  await ui.unmount()
})

// Las órdenes del aviso de dependencias: las líneas que empiezan por «claude plugin install».
const ordenesDelAviso = (t: string) => t.split('\n').filter(l => l.startsWith('claude plugin install '))

test('ACTUALIZAR: si una dependencia no se puede instalar, avisa con su orden en una línea y no pide reiniciar', async (...m) => {
  const { ordenes, toasts, ui } = await actualizar(m, { deps: DEPS_110, otros: VIEJA, installFalla: ['nueva@softwarefactory'] })
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  const aviso = toasts.find(t => t.startsWith('ACTUALIZAR: sf necesita nueva@softwarefactory y no se pudieron instalar'))
  expect(aviso).toBeDefined()
  expect(ordenesDelAviso(aviso!)).toEqual([INSTALL('nueva@softwarefactory', 'user')])
  // Sigue con las demás: la que falla no corta las siguientes.
  expect(installs(ordenes)).toEqual([INSTALL('nueva@softwarefactory', 'user'), INSTALL('ajena@otro', 'user')])
  expect(toasts).not.toContain('Actualizado a v1.1.0: reinicia Claude Code')
  await ui.unmount()
})

// claude plugin install instala solo el primer plugin que se le da: el aviso da una orden por dependencia (tarea 259).
test('ACTUALIZAR: si fallan varias dependencias, una orden por dependencia, una por línea', async (...m) => {
  const { toasts, ui } = await actualizar(m, { deps: DEPS_110, otros: VIEJA, installFalla: ['nueva@softwarefactory', 'ajena@otro'] })
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  const aviso = toasts.find(t => t.startsWith('ACTUALIZAR: sf necesita nueva@softwarefactory, ajena@otro y no se pudieron instalar'))
  expect(aviso).toBeDefined()
  expect(ordenesDelAviso(aviso!)).toEqual([INSTALL('nueva@softwarefactory', 'user'), INSTALL('ajena@otro', 'user')])
  expect(aviso).toMatch(/una orden por línea:\n/)
  await ui.unmount()
})

test('REFRESCAR: instala las dependencias que faltan antes de recargar', async (...m) => {
  const { comandos, ordenes, ui } = await actualizar(m, { remoto: remotos('1.0.0'), corre: '0.9.0', deps: { '1.0.0': ['nueva'] } })
  await ui.press({ key: 'refrescar' })
  await ui.press({ key: 'refrescar' })
  expect(installs(ordenes)).toEqual([INSTALL('nueva@softwarefactory', 'user')])
  expect(comandos).toContain('reload-plugins')
  await ui.unmount()
})

test('REFRESCAR: si la dependencia no se instala, no recarga y deja la orden', async (...m) => {
  const { comandos, toasts, ui } = await actualizar(m, { remoto: remotos('1.0.0'), corre: '0.9.0', deps: { '1.0.0': ['nueva'] }, installFalla: ['nueva@softwarefactory'] })
  await ui.press({ key: 'refrescar' })
  await ui.press({ key: 'refrescar' })
  expect(comandos).not.toContain('reload-plugins')
  const aviso = toasts.find(t => t.startsWith('REFRESCAR: sf necesita nueva@softwarefactory'))
  expect(ordenesDelAviso(aviso ?? '')).toEqual([INSTALL('nueva@softwarefactory', 'user')])
  await ui.unmount()
})

test('ACTUALIZAR: con el interruptor apagado en .sf/proyecto.json, no instala dependencias, pero da la orden de cada una que falta', async (...m) => {
  const { ordenes, toasts, ui } = await actualizar(m, { deps: DEPS_110, otros: VIEJA, proyecto: { nombre: 'x', automatizaciones: { dependencias_al_actualizar: false } } })
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  expect(installs(ordenes)).toEqual([])
  const aviso = toasts.find(t => t.startsWith('ACTUALIZAR: sf necesita nueva@softwarefactory, ajena@otro y no están instaladas'))
  expect(ordenesDelAviso(aviso ?? '')).toEqual([INSTALL('nueva@softwarefactory', 'user'), INSTALL('ajena@otro', 'user')])
  expect(toasts).not.toContain('Actualizado a v1.1.0: reinicia Claude Code')
  await ui.unmount()
})

test('ACTUALIZAR: con el interruptor apagado y las dependencias ya instaladas, pide reiniciar', async (...m) => {
  const { toasts, ui } = await actualizar(m, { deps: { '1.1.0': ['vieja'] }, otros: VIEJA, proyecto: { nombre: 'x', automatizaciones: { dependencias_al_actualizar: false } } })
  await ui.press({ key: 'actualizar' })
  await ui.press({ key: 'actualizar' })
  expect(toasts).toContain('Actualizado a v1.1.0: reinicia Claude Code')
  await ui.unmount()
})

// Las dependencias de la SF desde la 1.3.0 (decisión 176), tal como las da el aviso: una orden por línea.
test('avisoDependencias: una orden por dependencia, una por línea; sin ninguna, null', () => {
  const tres: [string, string][] = ['threejs-skills', 'oklch-skill', 'gsap-skills'].map(n => [`${n}@softwarefactory`, 'user'])
  const aviso = avisoDependencias('ACTUALIZAR', 'no están instaladas', tres)!
  expect(aviso.split('\n').slice(1)).toEqual(tres.map(([id]) => `claude plugin install ${id} --scope user`))
  expect(avisoDependencias('ACTUALIZAR', 'no están instaladas', [])).toBe(null)
})

test('ACTUALIZAR: /sf, que abre el panel, vuelve a comprobar', async (...m) => {
  const { ordenes, ui } = await actualizar(m, { remoto: remotos('1.0.0') })
  expect(ordenes.filter(o => o === LS_REMOTE)).toHaveLength(1)
  await m[0].command.run({ command: 'sf', args: '' })
  expect(ordenes.filter(o => o === LS_REMOTE)).toHaveLength(2)
  await ui.unmount()
})

test('ACTUALIZAR: comprueba al empezar y cada 5 minutos, no en cada render', async (...m) => {
  const { archivos, ordenes, reloj, ui } = await actualizar(m, { remoto: remotos('1.0.0') })
  const consultas = () => ordenes.filter(o => o === LS_REMOTE).length
  expect(consultas()).toBe(1)
  for (const k of ['sec:hecho', 'sec:hecho', 'sec:hecho']) await ui.press({ key: k })
  await reloj!.advance(4 * 60_000)
  expect(consultas()).toBe(1)
  expect(await ui.find({ type: 'Button', key: 'actualizar' })).toBe(undefined)
  // Entretanto, otra sesión deja vieja la instalada: a los 5 minutos sale.
  Object.assign(archivos, instalado([{ scope: 'user', version: '0.9.0' }]))
  await reloj!.advance(2 * 60_000)
  expect(consultas()).toBe(2)
  expect(await hay(ui, { type: 'Button', key: 'actualizar' })).toBe(true)
  await ui.unmount()
})

// La etiqueta de la versión (tarea 238): al pulsarla, cuánto falta para la próxima comprobación y la hora de la última.
const horaLocal = (ms: number) => `${String(new Date(ms).getHours()).padStart(2, '0')}:${String(new Date(ms).getMinutes()).padStart(2, '0')}`

test('Versión: la próxima comprobación es el primer latido a 5 minutos o más de la última', () => {
  expect(proximaComprobacion(AHORA)).toBe(AHORA + 5 * 60_000)
  // Desde una hora suelta (la del arranque), el latido de después, en minuto exacto.
  expect(proximaComprobacion(AHORA + 30_000)).toBe(AHORA + 6 * 60_000)
  expect(avisoComprobacion(AHORA, AHORA + 2 * 60_000)).toBe(`Próxima comprobación de versión en 3 min (última, a las ${horaLocal(AHORA)})`)
  // Lo que queda, redondeado hacia arriba; al llegar, en menos de un minuto.
  expect(avisoComprobacion(AHORA, AHORA + 4 * 60_000 + 1)).toContain('en 1 min')
  expect(avisoComprobacion(AHORA, AHORA + 5 * 60_000)).toContain('en menos de 1 min')
  expect(avisoComprobacion(null, AHORA)).toBe('Versión: aún sin comprobar si hay una nueva')
})

test('Versión: al pulsar su etiqueta, avisa de cuánto falta para la próxima comprobación, que el latido renueva', async (...m) => {
  const { toasts, reloj } = await preparar(m, { reloj: true })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const pulsar = async () => {
    await ui.press({ key: 'version-sf' })
    return toasts.at(-1)
  }
  expect(await pulsar()).toBe(`Próxima comprobación de versión en 5 min (última, a las ${horaLocal(AHORA)})`)
  await reloj!.advance(3 * 60_000)
  expect(await pulsar()).toBe(`Próxima comprobación de versión en 2 min (última, a las ${horaLocal(AHORA)})`)
  // A los 5 minutos, el latido comprueba: la última pasa a ser esa y vuelven a faltar 5.
  await reloj!.advance(2 * 60_000)
  expect(await pulsar()).toBe(`Próxima comprobación de versión en 5 min (última, a las ${horaLocal(AHORA + 5 * 60_000)})`)
  await ui.unmount()
})

// El ajuste del proyecto manda sobre el del usuario: desactivado para el usuario y activo en el proyecto, cuenta.
test('ACTUALIZAR: activo en los ajustes del proyecto aunque el usuario lo desactive, sale', async (...m) => {
  const { ui } = await actualizar(m, { ajustes: { '/home/.claude/settings.json': { enabledPlugins: { 'sf@softwarefactory': false } }, [AJUSTES]: { enabledPlugins: { 'sf@softwarefactory': true } } } })
  expect(await hay(ui, { type: 'Button', key: 'actualizar' })).toBe(true)
  await ui.unmount()
})

// En la copia de trabajo con sf@softwarefactory activo y la de usuario por detrás, ACTUALIZAR sigue saliendo: lo
// instalado sí corre en el proyecto cuando se sale del modo prueba.
test('ACTUALIZAR: en la copia de trabajo, con sf@softwarefactory activo y por detrás, sale', async (...m) => {
  const { ui } = await actualizar(m, { copia: true, ajustes: { [AJUSTES]: { enabledPlugins: { 'sf@softwarefactory': true } } } })
  expect(await hay(ui, { type: 'Button', key: 'actualizar' })).toBe(true)
  await ui.unmount()
})

// Otra sesión instala una versión nueva: esta, que sigue con la vieja, lo ve en el siguiente latido, sin consultar la
// red, y no a los 5 minutos (tarea 229, reabierta).
test('REFRESCAR: si otra sesión instala una versión nueva, sale al minuto, sin consultar la red', async (...m) => {
  const { archivos, ordenes, reloj, ui } = await actualizar(m, { entradas: [USER_100], remoto: remotos('1.0.0') })
  const consultas = () => ordenes.filter(o => o === LS_REMOTE).length
  expect(consultas()).toBe(1)
  expect(await ui.find({ type: 'Button', key: 'refrescar' })).toBe(undefined)
  Object.assign(archivos, instalado([{ scope: 'user', version: '1.1.0' }]))
  await reloj!.advance(60_000)
  expect(consultas()).toBe(1)
  // Con REFRESCAR sale también su aviso, que se turna con la cabecera: si está en su turno, un clic lo quita.
  if (await textoAvisos(ui)) await ui.press({ key: 'aviso:0' })
  await ui.press({ key: 'refrescar' })
  expect(await hay(ui, { type: 'Text', text: /¿Refrescar a v1\.1\.0\? sí/ })).toBe(true)
  await ui.unmount()
})

test('ACTUALIZAR: tras publicar con RELEASE vuelve a comprobar', async (...m) => {
  const { ordenes, reloj, ui } = await release(m, { extra: instalado([USER_100]) })
  await reloj!.advance(1000)
  const antes = ordenes.filter(o => o === LS_REMOTE).length
  expect(antes).toBe(1)
  await elegir(ui, '0.35.0')
  expect(ordenes.filter(o => o === LS_REMOTE).length).toBe(antes + 1)
  await ui.unmount()
})

// /sf y RELEASE también cuentan como última comprobación: reinician la cuenta de 5 minutos del latido (tarea 238).
test('Versión: /sf comprueba, fija la última y reinicia la cuenta de 5 minutos del latido', async (...m) => {
  const { ordenes, toasts, reloj, ui } = await actualizar(m, { remoto: remotos('1.0.0') })
  const consultas = () => ordenes.filter(o => o === LS_REMOTE).length
  await reloj!.advance(2 * 60_000)
  await m[0].command.run({ command: 'sf', args: '' })
  expect(consultas()).toBe(2)
  // El reloj va un segundo por delante (la comprobación del arranque): la próxima es el latido de 5 min y 59 s después.
  await ui.press({ key: 'version-sf' })
  expect(toasts.at(-1)).toBe(`Próxima comprobación de versión en 6 min (última, a las ${horaLocal(AHORA + 2 * 60_000)})`)
  // A los 5 minutos del arranque, el latido ya no comprueba: cuenta desde /sf.
  await reloj!.advance(5 * 60_000)
  expect(consultas()).toBe(2)
  await reloj!.advance(60_000)
  expect(consultas()).toBe(3)
  await ui.unmount()
})

test('Versión: RELEASE, al publicar, fija la última comprobación', async (...m) => {
  const { toasts, reloj, ui } = await release(m, { extra: instalado([USER_100]) })
  await reloj!.advance(3 * 60_000)
  await elegir(ui, '0.35.0')
  await ui.press({ key: 'version-sf' })
  expect(toasts.at(-1)).toBe(`Próxima comprobación de versión en 5 min (última, a las ${horaLocal(AHORA + 3 * 60_000)})`)
  await ui.unmount()
})

// Cada tarea, en una sola sección (decisión del propietario, 2026-10-31); arriba es el foco y puede repetirla.
const seccionesDe = async (ui: { findAll: (q: object) => Promise<unknown[]> }, id: number) => {
  const claves = ((await ui.findAll({ type: 'Button' })) as { key?: unknown }[]).map(b => String(b.key ?? ''))
  return ['cola', 'observacion', 'hecho'].filter(s => claves.includes(`pet:${s}:${id}`) || claves.includes(`hecho:${id}`) && s === 'hecho')
}

test('Una sola sección: pasada a observación en la sesión, en observación y no en Cerradas', async (...m) => {
  const { cambiarCola } = await preparar(m, { cola: [] })
  await cambiarCola([{ id: 40, texto: 'A observación', estado: 'en-observacion', commit: 'develop abc', historial: [ev('a-observacion', 'develop abc')] }])
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'sec:observacion' })
  expect(await seccionesDe(ui, 40)).toEqual(['observacion'])
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  await ui.unmount()
})

test('Una sola sección: reabierta desde En observación o desde Cerradas, en Pendientes, sobre rojo, y no en Cerradas', async (...m) => {
  const reabierta = (id: number, desde: string): Pet => ({
    id,
    texto: `Reabierta desde ${desde}`,
    estado: 'en-cola',
    commit: 'develop abc',
    reabierta: true,
    historial: [ev(desde === 'observación' ? 'a-observacion' : 'cerrada', 'develop abc'), ev('reabierta', 'falla', 1)],
  })
  const { cambiarCola } = await preparar(m, { cola: [] })
  await cambiarCola([reabierta(41, 'observación'), reabierta(42, 'Cerradas')])
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  for (const id of [41, 42]) {
    expect(await seccionesDe(ui, id)).toEqual(['cola'])
    // El número de la reabierta, gris sobre fondo rojo.
    expect(await colores(ui, id)).toEqual([`${GRIS} sobre error`])
  }
  expect(await hay(ui, { type: 'Button', text: /CERRADAS [▸▾]\s+0/ })).toBe(true)
  await ui.unmount()
})

test('Una sola sección: en curso, solo arriba; la que se prueba, también solo arriba', async (...m) => {
  await preparar(m, {
    cola: [
      { id: 43, texto: 'En curso', estado: 'en-curso', commit: 'x' },
      { id: 44, texto: 'Probándose', estado: 'en-observacion', observando: true, commit: 'y' },
    ],
  })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // Sin otras tareas, Pendientes y En observación, con 0.
  expect(await hay(ui, { type: 'Button', text: /^PENDIENTES [▸▾] 0$/ })).toBe(true)
  expect(await hay(ui, { type: 'Button', text: /^EN OBSERVACIÓN [▸▾] 0$/ })).toBe(true)
  for (const id of [43, 44]) {
    expect(await seccionesDe(ui, id)).toEqual([])
    expect(await colores(ui, id)).toEqual(['heredado'])
  }
  await ui.unmount()
})

// La sangría de lo desplegado (decisión del propietario, 2026-10-31): la descripción, en la columna del título; la
// rama y el contador de pasos de arriba, en la columna 0; la lista de pasos, con sangría 2.
type Caja = { props: { paddingLeft?: number } }
const sangrias = async (ui: { findAll: (q: object) => Promise<unknown[]> }, text: RegExp) =>
  ((await ui.findAll({ type: 'Box', text })) as Caja[]).map(b => b.props.paddingLeft ?? 0).filter(x => x > 0)

test('Desplegada, la descripción empieza en la columna del título, arriba y en Pendientes', async (...m) => {
  await preparar(m, {
    cola: [
      { id: 4, texto: 'Fondos por bloque', estado: 'en-curso', descripcion: 'Grises suaves.' },
      {
        id: 7,
        texto: 'En cola',
        estado: 'en-cola',
        descripcion: 'Un gris.',
        pasos: [
          { texto: 'A', estado: 'hecho' },
          { texto: 'B', estado: 'pendiente' },
        ],
      },
    ],
  })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  for (const k of ['arriba:4', 'pet:cola:7']) await ui.press({ key: k })
  // Arriba, «  4 Fondos…»: hueco (2), número (1) y espacio (1).
  expect(await sangrias(ui, /^Grises suaves\.$/)).toEqual([4])
  // En Pendientes, «  7 En cola»: igual, sin la cuenta de pasos.
  expect(await sangrias(ui, /^Un gris\.$/)).toEqual([4])
  await ui.unmount()
})

test('Desplegada, la rama y la cabecera de los pasos, en la columna 0; los pasos, sin sangría y con el número en tres columnas', async (...m) => {
  await preparar(m, {
    cola: [
      { id: 1, texto: 'Panel lateral', estado: 'en-curso', rama: 'feature/1-panel', pasos: [{ texto: 'Uno', estado: 'en-curso' }, { texto: 'Dos', estado: 'pendiente' }] },
      { id: 7, texto: 'En cola', estado: 'en-cola', rama: 'feature/7-cola' },
    ],
    extra: GIT('ref: refs/heads/develop\n'),
  })
  const ui = await m[0].ui.mount({ ...ANCHO, surface: 'terminal' })
  await ui.press({ key: 'arriba:1' })
  expect(await sangrias(ui, /^Pasos 0\/2$/)).toEqual([])
  await ui.press({ key: 'pet:cola:7' })
  expect(await hay(ui, { type: 'Text', text: /^Rama: feature\/1-panel/ })).toBe(true)
  expect(await sangrias(ui, /^Rama: feature\/1-panel/)).toEqual([])
  expect(await sangrias(ui, /^Rama: feature\/7-cola/)).toEqual([])
  await ui.press({ key: 'pasos:arriba:1' })
  expect(await sangrias(ui, /^Pasos 0\/2/)).toEqual([])
  expect(await sangrias(ui, /^  1$/)).toEqual([])
  // La fila del paso: su número y, a su derecha, el texto con sus botones.
  expect(await columnaDe(ui, 'Uno', '  1')).toEqual({ ancho: 4, fija: 0, encoge: 1, titulo: true })
  await ui.unmount()
})

// Desplegada, una tarea muestra debajo, en este orden, la línea de la rama (con el commit, la prueba y el OK de Claude),
// «Descripción» (desplegable) y «Pasos N/M» (desplegable); plegada, solo su título (decisión del propietario, 2026-10-31).
const COMPLETA: Pet = {
  id: 7,
  texto: 'Completa',
  estado: 'en-observacion',
  descripcion: 'Su descripción.',
  rama: 'feature/7-completa',
  commit: 'develop abc1234',
  prueba: 'abrir el panel',
  comprobado: 'lo abrí',
  pasos: [
    { texto: 'Hacer', estado: 'hecho' },
    { texto: 'Probar la tarea', estado: 'pendiente' },
  ],
}

test('Plegada, una tarea muestra solo su título, arriba y en las secciones', async (...m) => {
  await preparar(m, { cola: [{ ...COMPLETA, id: 4, estado: 'en-curso' }, { ...COMPLETA, estado: 'en-cola' }], extra: GIT('ref: refs/heads/develop\n') })
  const ui = await m[0].ui.mount({ ...ANCHO, surface: 'terminal' })
  for (const fuera of [/Su descripción/, /^Descripción$/, /^rama:/, /develop abc1234/, /^Pasos /, /Probar la tarea/])
    expect(await ui.find({ type: 'Text', text: fuera })).toBe(undefined)
  await ui.unmount()
})

test('Desplegada: la línea de la rama, Descripción y Pasos, en ese orden; la Descripción, abierta al empezar, y los pasos, plegados', async (...m) => {
  await preparar(m, { cola: [{ ...COMPLETA, estado: 'en-cola' }], extra: GIT('ref: refs/heads/develop\n') })
  const ui = await m[0].ui.mount({ ...ANCHO, surface: 'terminal' })
  await ui.press({ key: 'pet:cola:7' })
  const fila = String(((await ui.find({ type: 'Box', text: /^7 Completa/ })) as { text?: unknown } | undefined)?.text ?? '')
  const donde = (t: string) => fila.indexOf(t)
  expect(donde('Rama: feature/7-completa') > 0).toBe(true)
  expect(donde('Rama: feature/7-completa') < donde('Descripción')).toBe(true)
  expect(donde('Descripción') < donde('Pasos 1/2')).toBe(true)
  // La descripción, a la vista (sus partes sin tocar); la lista de pasos, plegada.
  expect(await hay(ui, { type: 'Text', text: /^Su descripción\.$/ })).toBe(true)
  expect(await ui.find({ type: 'Text', text: /Probar la tarea/ })).toBe(undefined)
  await ui.press({ key: 'pasos:cola:7' })
  expect(await hay(ui, { type: 'Text', text: /^Probar la tarea$/ })).toBe(true)
  // Y se vuelven a plegar.
  await ui.press({ key: 'desc:cola:7' })
  await ui.press({ key: 'pasos:cola:7' })
  expect(await ui.find({ type: 'Text', text: /Su descripción/ })).toBe(undefined)
  expect(await ui.find({ type: 'Text', text: /Probar la tarea/ })).toBe(undefined)
  await ui.unmount()
})

// Tarea 237: en observación y en la que se prueba, la línea de la rama, como en las demás secciones (rama y commit, en la
// columna 0); el OK de Claude y la prueba, cada uno en su línea y en la columna del título, como la descripción.
test('En observación y en la que se prueba, la línea de la rama, como en las demás; el OK de Claude y la prueba, en la columna del título', async (...m) => {
  await preparar(m, { cola: [COMPLETA, { ...COMPLETA, id: 8, observando: true }, { ...COMPLETA, id: 9, estado: 'en-cola' }], extra: GIT('ref: refs/heads/develop\n') })
  const ui = await m[0].ui.mount({ ...ANCHO, surface: 'terminal' })
  await ui.press({ key: 'sec:observacion' })
  await ui.press({ key: 'pet:observacion:7' })
  await ui.press({ key: 'arriba:8' })
  await ui.press({ key: 'pet:cola:9' })
  await ui.press({ key: 'prueba:observacion:7' })
  await ui.press({ key: 'prueba:arriba:8' })
  const lineas = (await ui.findAll({ type: 'Text', text: /^Rama: feature\/7-completa \(no existe\) · / })).map(x => String((x as { text?: unknown }).text))
  expect(lineas).toEqual(Array(3).fill('Rama: feature/7-completa (no existe) · Commit: develop abc1234'))
  expect(await sangrias(ui, /^Rama: feature\/7-completa/)).toEqual([])
  // En observación y arriba: los apartados, en la columna del título («  7 », 4), como la descripción; en Pendientes, no salen.
  expect(await sangrias(ui, /^Comprobado por Claude$/)).toEqual([4, 4])
  expect(await sangrias(ui, /^Qué mirar$/)).toEqual([4, 4])
  expect(await sangrias(ui, /^Su descripción\.$/)).toEqual([4, 4, 4])
  await ui.unmount()
})

// Tarea 237: las tareas de En observación, plegadas y desplegadas, con la misma sangría y alineación que las de Pendientes:
// el número en la misma columna, el título a su derecha y el detalle en las mismas columnas.
test('En observación: plegadas y desplegadas, alineadas y sangradas como en Pendientes', async (...m) => {
  const larga = 'Una tarea con un título largo que no cabe en una sola línea del panel estrecho'
  await preparar(m, {
    cola: [
      { id: 6, texto: `${larga} (cola)`, estado: 'en-cola', rama: 'feature/6-x', commit: 'c6', descripcion: 'Desc seis.', pasos: [{ texto: 'Uno', estado: 'pendiente' }] },
      { id: 8, texto: `${larga} (observada)`, estado: 'en-observacion', rama: 'feature/8-x', commit: 'c8', descripcion: 'Desc ocho.', prueba: 'abrirlo', comprobado: 'lo abrí', pasos: [{ texto: 'Uno', estado: 'hecho' }] },
    ],
  })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  if (!(await hay(ui, { type: 'Button', key: 'pet:observacion:8' }))) await ui.press({ key: 'sec:observacion' })
  const forma = async () => {
    const raiz = (await ui.drawn()) as Nodo
    return (t: string) => {
      const f = fila(raiz, t)
      const [izq, der] = f ? hijos(f) : []
      return [f ? sangriaDe(raiz, f) : undefined, izq?.props?.width, izq?.props?.paddingLeft, izq?.props?.flexShrink, der?.props?.flexShrink]
    }
  }
  // Plegadas: «  6 » y «  8 », en la columna 0, con el título a su derecha y encogible.
  let col = await forma()
  expect(col(`${larga} (observada)`)).toEqual([0, 4, 2, 0, 1])
  expect(col(`${larga} (cola)`)).toEqual([0, 4, 2, 0, 1])
  // Desplegadas: igual; la línea de la rama y las cabeceras, en la columna 0; la descripción, la prueba y el OK, en la del título.
  await ui.press({ key: 'pet:cola:6' })
  await ui.press({ key: 'pet:observacion:8' })
  await ui.press({ key: 'prueba:observacion:8' })
  col = await forma()
  expect(col(`${larga} (observada)`)).toEqual([0, 4, 2, 0, 1])
  expect(col(`${larga} (cola)`)).toEqual([0, 4, 2, 0, 1])
  expect(await sangrias(ui, /^Rama: feature\/[68]-x/)).toEqual([])
  expect(await sangrias(ui, /^(Pasos|Prueba)/)).toEqual([])
  expect(await sangrias(ui, /^Desc (seis|ocho)\.$/)).toEqual([4, 4])
  expect(await sangrias(ui, /^(Comprobado por Claude|Qué mirar)$/)).toEqual([4, 4])
  await ui.unmount()
})

// Tarea 237 (petición del propietario, tras la decisión 179): el OK de Claude y la prueba, en un desplegable propio,
// «Prueba», plegado al empezar, con «✓» tras la cabecera si Claude comprobó algo; su estado se guarda como el de
// Descripción y Pasos. En observación y en la que se prueba arriba; en Pendientes, no sale.
test('Prueba: desplegable propio, plegado al empezar, con ✓ si Claude comprobó algo, guardado como los demás', async (...m) => {
  const { guardado } = await preparar(m, {
    cola: [
      COMPLETA,
      { ...COMPLETA, id: 8, observando: true, comprobado: null },
      { ...COMPLETA, id: 9, estado: 'en-cola' },
    ],
    extra: GIT('ref: refs/heads/develop\n'),
  })
  const ui = await m[0].ui.mount({ ...ANCHO, surface: 'terminal' })
  await ui.press({ key: 'sec:observacion' })
  await ui.press({ key: 'pet:observacion:7' })
  await ui.press({ key: 'arriba:8' })
  await ui.press({ key: 'pet:cola:9' })
  // Plegado: solo la cabecera, subrayada y atenuada como «Pasos»; con «✓» si Claude comprobó algo.
  expect(await hay(ui, { type: 'Button', key: 'prueba:observacion:7', text: /^Prueba ✓$/ })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'prueba:arriba:8', text: /^Prueba$/ })).toBe(true)
  expect(await ui.find({ type: 'Button', key: 'prueba:cola:9' })).toBe(undefined)
  expect(await ui.find({ type: 'Text', text: /^(Comprobado por Claude|Qué mirar|Lo abrí|Abrir el panel)$/ })).toBe(undefined)
  const cabecera = (await ui.find({ type: 'Text', text: /^Prueba$/ })) as { props: { underline?: boolean; dimColor?: boolean } }
  expect([cabecera.props.underline, cabecera.props.dimColor]).toEqual([true, true])
  // Va tras la línea de la rama y antes de «Descripción».
  const fila = String(((await ui.find({ type: 'Box', text: /^7 Completa/ })) as { text?: unknown } | undefined)?.text ?? '')
  expect(fila.indexOf('Commit: develop abc1234') < fila.indexOf('Prueba')).toBe(true)
  expect(fila.indexOf('Prueba') < fila.indexOf('Descripción')).toBe(true)
  // Desplegado: sus apartados, en la columna del título; la Descripción, que seguía sin tocar, se guarda abierta.
  await ui.press({ key: 'prueba:observacion:7' })
  expect(await sangrias(ui, /^Comprobado por Claude$/)).toEqual([4])
  expect(await sangrias(ui, /^Qué mirar$/)).toEqual([4])
  expect(await hay(ui, { type: 'Text', text: /^Lo abrí$/ })).toBe(true)
  const plegado = guardado.plegado as Record<string, boolean>
  expect([plegado['prueba:observacion:7'], plegado['desc:observacion:7']]).toEqual([false, false])
  // Y se vuelve a plegar.
  await ui.press({ key: 'prueba:observacion:7' })
  expect(await ui.find({ type: 'Text', text: /^Abrir el panel$/ })).toBe(undefined)
  await ui.unmount()
})

// Tarea 237: lo que mirar y lo que comprobó Claude, estructurado: un rótulo atenuado por apartado y, debajo, un punto
// por línea, con guion y sangría colgante; el contexto del principio («Tras publicar:»), antes de los puntos.
test('Prueba: «Comprobado por Claude» y «Qué mirar», un punto por línea, con el contexto aparte', async (...m) => {
  await preparar(m, {
    cola: [
      {
        ...COMPLETA,
        comprobado: '262 del plugin y validate pasan',
        prueba: 'Tras publicar: la sesión en modo prueba no muestra ACTUALIZAR; con dos sesiones, la otra muestra REFRESCAR',
      },
    ],
    extra: GIT('ref: refs/heads/develop\n'),
  })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'sec:observacion' })
  await ui.press({ key: 'pet:observacion:7' })
  await ui.press({ key: 'prueba:observacion:7' })
  const fila = String(((await ui.find({ type: 'Box', text: /^7 Completa/ })) as { text?: unknown } | undefined)?.text ?? '')
  const orden = ['Prueba ✓', 'Comprobado por Claude', '262 del plugin y validate pasan', 'Qué mirar', 'Tras publicar:', 'La sesión en modo prueba no muestra ACTUALIZAR', 'Con dos sesiones, la otra muestra REFRESCAR', 'Descripción']
  const pos = orden.map(t => fila.indexOf(t))
  expect(pos.every(x => x >= 0)).toBe(true)
  expect([...pos].sort((a, b) => a - b)).toEqual(pos)
  // Rótulos y contexto, atenuados; cada punto, con su guion en una columna de 2 y el texto encogible (sangría colgante).
  for (const t of [/^Comprobado por Claude$/, /^Qué mirar$/, /^Tras publicar:$/])
    expect(((await ui.find({ type: 'Text', text: t })) as { props: { dimColor?: boolean } }).props.dimColor).toBe(true)
  const punto = fila_(await ui.drawn(), 'Con dos sesiones, la otra muestra REFRESCAR')
  expect(punto).toEqual([2, 0, 1])
  // El commit, con su rótulo.
  expect(await hay(ui, { type: 'Text', text: /^Rama: feature\/7-completa \(no existe\) · Commit: develop abc1234$/ })).toBe(true)
  await ui.unmount()
})
const fila_ = (raiz: unknown, t: string) => {
  const f = fila(raiz as Nodo, t)
  const [izq, der] = f ? hijos(f) : []
  return [izq?.props?.width, izq?.props?.flexShrink, der?.props?.flexShrink]
}

test('puntosDe: parte por «;», con el contexto corto del principio aparte; sin «;», un punto', () => {
  expect(puntosDe('Tras publicar: a; b;  ; c')).toEqual({ contexto: 'Tras publicar', puntos: ['A', 'B', 'C'] })
  expect(puntosDe('262 del plugin y validate pasan')).toEqual({ contexto: null, puntos: ['262 del plugin y validate pasan'] })
  expect(puntosDe('abrir uno; luego: otro')).toEqual({ contexto: null, puntos: ['Abrir uno', 'Luego: otro'] })
  expect(puntosDe('Un texto largo sin punto y coma que no es contexto aunque tenga: dos puntos')).toEqual({ contexto: null, puntos: ['Un texto largo sin punto y coma que no es contexto aunque tenga: dos puntos'] })
  expect(puntosDe('Solo:')).toEqual({ contexto: null, puntos: ['Solo:'] })
})

test('Sin más detalle ni órdenes, la tarea se despliega igual por su «?» (254), que es su menú', async (...m) => {
  await preparar(m, { cola: [{ id: 7, texto: 'Otra', estado: 'en-observacion' }] })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'sec:observacion' })
  expect((await numeros(ui, 7)).map(x => x.props.underline)).toEqual([true])
  expect(await ui.find({ type: 'Button', key: 'explicar-tarea:observacion:7' })).toBe(undefined)
  await ui.press({ key: 'pet:observacion:7' })
  expect(await hay(ui, { type: 'Button', key: 'explicar-tarea:observacion:7', text: /^ \? $/ })).toBe(true)
  await ui.unmount()
})

test('Menú: una tarea sin detalle pero con órdenes se despliega, y la primera fila es su menú (decisión 168)', async (...m) => {
  await preparar(m, { cola: [{ id: 4, texto: 'Sola', estado: 'en-curso' }, { id: 7, texto: 'Otra', estado: 'en-cola' }] })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  for (const id of [4, 7]) expect((await numeros(ui, id)).map(x => x.props.underline)).toEqual([true])
  // Plegadas, ninguna orden.
  for (const k of ['arriba:4', 'cola:7']) expect(await ui.find({ type: 'Button', key: `eliminar-tarea:${k}` })).toBe(undefined)
  await ui.press({ key: 'arriba:4' })
  await ui.press({ key: 'pet:cola:7' })
  // Arriba, Paso + y Eliminar; en Pendientes, solo Eliminar.
  expect(await hay(ui, { type: 'Button', key: 'paso-tarea:arriba:4', text: /^ Paso \+ $/ })).toBe(true)
  for (const k of ['arriba:4', 'cola:7']) expect(await hay(ui, { type: 'Button', key: `eliminar-tarea:${k}`, text: /^ Eliminar $/ })).toBe(true)
  expect(await ui.find({ type: 'Button', key: 'paso-tarea:cola:7' })).toBe(undefined)
  await ui.unmount()
})

// El menú de órdenes de cada tarea (decisión 168): etiquetas con su nombre en la primera fila de la tarea desplegada.
const etiqueta = async (ui: { find: (q: object) => Promise<unknown> }, key: string) =>
  ((await ui.find({ type: 'Button', key })) as { children: Nodo[] } | undefined)?.children[0]?.props

test('Menú: plegada, la tarea no lleva ninguna orden, solo el ● del subagente', async (...m) => {
  await preparar(m, { cola: CERRABLES, agentes: EN_12(), extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'subagente-tarea:arriba:12' })).toBe(true)
  for (const b of ['probar', 'cerrar', 'descartar', 'split', 'paso', 'redescribir', 'explicar']) expect(await ui.find({ type: 'Button', key: `${b}-tarea:arriba:12` })).toBe(undefined)
  // Las letras de antes no salen en ningún sitio.
  for (const l of ['T', 'C', 'D', 'E', 'S', 'R']) expect(await ui.find({ type: 'Text', text: new RegExp(`^ ${l}$`) })).toBe(undefined)
  // Desplegada, el menú: primero las de la tarea, Activar rama, Cerrar, A observación (241), «?» y Descartar; después, Paso +, la de sus pasos.
  await ui.press({ key: 'arriba:12' })
  const textos = ((await ui.findAll({ type: 'Button' })) as { key?: string; children: Nodo[] }[])
    .filter(b => /-tarea:arriba:12$/.test(String(b.key)) && !String(b.key).startsWith('subagente'))
    .map(b => String(b.key).split('-tarea')[0])
  expect(textos).toEqual(['probar', 'cerrar', 'a-observacion', 'explicar', 'descartar', 'paso'])
  await ui.unmount()
})

test('Paso de prueba: con el nombre nuevo, «Activar rama para poder probar», Cerrar sale y el paso no se quita (decisiones 172 y 174)', async (...m) => {
  const cola: Pet[] = [{
    id: 12, texto: 'Lista', estado: 'en-curso', rama: 'feature/12-lista',
    pasos: [{ texto: 'Hacer A', estado: 'hecho' }, { texto: 'Activar rama para poder probar', estado: 'pendiente' }, { texto: 'Cerrar la tarea', estado: 'pendiente' }],
  }]
  await preparar(m, { desplegadas: true, cola, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', key: 'cerrar-tarea:arriba:12' })).toBe(true)
  await ui.press({ key: 'pasos:arriba:12' })
  for (const i of [1, 2]) expect(await ui.find({ type: 'Button', key: `quitar-paso:arriba:12:${String(i)}` })).toBe(undefined)
  await ui.unmount()
})

test('Pasos: en un paso de varias líneas, el «?» y la «×» siguen a la última palabra, en la última línea', async (...m) => {
  const largo = 'Implementado el menú de etiquetas al desplegar la tarea con todas sus órdenes en una fila'
  const cola: Pet[] = [{ id: 4, texto: 'Con un paso largo', estado: 'en-curso', pasos: [{ texto: largo, estado: 'pendiente' }, { texto: 'Corto', estado: 'pendiente' }] }]
  await preparar(m, { cola })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'arriba:4' })
  await ui.press({ key: 'pasos:arriba:4' })
  const ancho = PANEL.props.bodyColumns - 1 - 4
  // Partido por palabras, sin perder ninguna; ninguna línea pasa del ancho de su columna.
  const lineas = ((await ui.findAll({ type: 'Text', text: /^(Implementado|[a-zé]).*$/ })) as { children: unknown[] }[])
    .map(t => t.children.join(''))
    .filter(t => largo.includes(t) && t !== '')
  expect(lineas.length).toBeGreaterThan(1)
  expect(lineas.join(' ')).toBe(largo)
  for (const l of lineas) expect(l.length).toBeLessThanOrEqual(ancho)
  // El «?» y la «×», en la misma fila que la última línea, detrás de ella.
  const fila = (await ui.find({ type: 'Box', text: new RegExp(`^${lineas.at(-1)} \\? ×$`) })) as unknown
  expect(fila !== undefined).toBe(true)
  // El paso corto, en una línea con sus botones detrás.
  expect(await hay(ui, { type: 'Box', text: /^Corto \? ×$/ })).toBe(true)
  await ui.unmount()
})

test('Desplegada con sus partes sin tocar, la Descripción sale abierta; tocada una, manda lo guardado', async (...m) => {
  const cola: Pet[] = [
    { id: 4, texto: 'Con descripción', estado: 'en-curso', descripcion: 'Su texto.', pasos: [{ texto: 'Uno', estado: 'pendiente' }] },
    { id: 7, texto: 'Otra', estado: 'en-cola', descripcion: 'La de la 7.' },
  ]
  const { guardado } = await preparar(m, { cola })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'arriba:4' })
  expect(await hay(ui, { type: 'Text', text: /^Su texto\.$/ })).toBe(true)
  // Abrir los pasos no pliega la Descripción: se guarda abierta.
  await ui.press({ key: 'pasos:arriba:4' })
  expect(await hay(ui, { type: 'Text', text: /^Su texto\.$/ })).toBe(true)
  expect(guardado.plegado).toMatchObject({ 'desc:arriba:4': false, 'pasos:arriba:4': false })
  // Plegada a mano, sigue plegada.
  await ui.press({ key: 'desc:arriba:4' })
  expect(await ui.find({ type: 'Text', text: /^Su texto\.$/ })).toBe(undefined)
  await ui.press({ key: 'arriba:4' })
  await ui.press({ key: 'arriba:4' })
  expect(await ui.find({ type: 'Text', text: /^Su texto\.$/ })).toBe(undefined)
  // En otra tarea sin tocar, abierta; un clic la pliega.
  await ui.press({ key: 'pet:cola:7' })
  expect(await hay(ui, { type: 'Text', text: /^La de la 7\.$/ })).toBe(true)
  await ui.press({ key: 'desc:cola:7' })
  expect(await ui.find({ type: 'Text', text: /^La de la 7\.$/ })).toBe(undefined)
  await ui.unmount()
})

test('Menú: una fila sin órdenes no se pinta; sin órdenes de pasos, solo la de la tarea', async (...m) => {
  const cola: Pet[] = [
    // La 9, en cola con rama y dos pasos pendientes; la 7, en cola sin rama ni pasos.
    { id: 9, texto: 'Solo pasos', estado: 'en-cola', rama: 'feature/9-x', pasos: [{ texto: 'Uno', estado: 'pendiente' }, { texto: 'Dos', estado: 'pendiente' }] },
    { id: 7, texto: 'Solo tarea', estado: 'en-cola' },
  ]
  await preparar(m, { desplegadas: true, cola })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const filasDe = async (id: number) =>
    todos((await ui.drawn()) as Nodo, n => n.props?.flexDirection === 'row' && n.props?.flexWrap === 'wrap')
      .map(f => JSON.stringify(f))
      .filter(f => f.includes(`-tarea:cola:${id}`))
  // La 9: Descartar en la de la tarea y Separar pasos en la de los pasos (su rama no existe: sin Activar rama).
  expect((await filasDe(9)).length).toBe(2)
  // La 7, sin pasos: solo la fila de la tarea, con Eliminar.
  const f7 = await filasDe(7)
  expect(f7.length).toBe(1)
  expect(f7[0]!.includes('Eliminar')).toBe(true)
  await ui.unmount()
})

test('Menú: orden completo, las de la tarea y después las de sus pasos, Separar pasos y Paso +', async (...m) => {
  const cola: Pet[] = [{
    id: 6, texto: 'Con todo', estado: 'en-curso', rama: 'feature/6-algo', descripcion: 'Algo.',
    pasos: [{ texto: 'Uno', estado: 'pendiente' }, { texto: 'Dos', estado: 'pendiente' }],
  }]
  await preparar(m, { desplegadas: true, cola, extra: { ...RAMAS_PROBAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const claves = ((await ui.findAll({ type: 'Button' })) as { key?: string }[])
    .filter(b => /-tarea:arriba:6$/.test(String(b.key)) && !String(b.key).startsWith('subagente'))
    .map(b => String(b.key).split('-tarea')[0])
  expect(claves).toEqual(['probar', 'redescribir', 'explicar', 'descartar', 'split', 'paso'])
  // En dos filas: la de la tarea y, debajo, la de los pasos.
  const filas = todos((await ui.drawn()) as Nodo, n => n.props?.flexDirection === 'row' && n.props?.flexWrap === 'wrap')
    .map(f => JSON.stringify(f))
    .filter(f => f.includes('-tarea:arriba:6'))
  expect(filas.length).toBe(2)
  expect(['Activar rama', 'Redescribir', 'Descartar'].every(t => filas[0]!.includes(t)) && !filas[0]!.includes('Paso +')).toBe(true)
  expect(['Separar pasos', 'Paso +'].every(t => filas[1]!.includes(t)) && !filas[1]!.includes('Activar rama')).toBe(true)
  await ui.unmount()
})

test('Menú: cada etiqueta, con su nombre, sobre su fondo (FONDO_ORDEN): las de la tarea en verde, las que destruyen en rojo, las de los pasos atenuadas; confirmar dice «¿Cerrar? sí»', async (...m) => {
  const { reloj } = await preparar(m, { desplegadas: true, cola: CERRABLES, reloj: true, extra: { ...RAMAS_CERRAR, '/sf/.git/HEAD': 'ref: refs/heads/develop\n' } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const gris = FONDO_ORDEN // el fondo de las etiquetas del menú
  for (const k of ['probar', 'cerrar']) expect(await etiqueta(ui, `${k}-tarea:arriba:12`)).toMatchObject({ color: 'success', weight: 'regular', backgroundColor: gris })
  expect(await etiqueta(ui, 'descartar-tarea:arriba:12')).toMatchObject({ color: '#f87171', weight: 'regular', backgroundColor: gris })
  // Las de los pasos, con la letra atenuada.
  expect(await etiqueta(ui, 'paso-tarea:arriba:12')).toMatchObject({ color: '#717171', weight: 'regular', backgroundColor: gris })
  for (const [k, t] of [['probar', 'Activar rama'], ['cerrar', 'Cerrar'], ['descartar', 'Descartar'], ['paso', 'Paso +']] as const)
    expect(await hay(ui, { type: 'Button', key: `${k}-tarea:arriba:12`, text: new RegExp(`^ ${t.replace('+', '\\+')} $`) })).toBe(true)
  await ui.press({ key: 'cerrar-tarea:arriba:12' })
  expect(await hay(ui, { type: 'Button', key: 'cerrar-tarea:arriba:12', text: /^ ¿Cerrar\? sí $/ })).toBe(true)
  expect((await etiqueta(ui, 'cerrar-tarea:arriba:12'))?.color).toBe('success')
  // La de una destructiva, en rojo también al confirmar.
  await ui.press({ key: 'descartar-tarea:arriba:12' })
  expect(await etiqueta(ui, 'descartar-tarea:arriba:12')).toMatchObject({ color: '#f87171', backgroundColor: gris })
  expect(await hay(ui, { type: 'Button', key: 'descartar-tarea:arriba:12', text: /^ ¿Descartar\? sí $/ })).toBe(true)
  await reloj!.advance(5500)
  expect(await hay(ui, { type: 'Button', key: 'cerrar-tarea:arriba:12', text: /^ Cerrar $/ })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'descartar-tarea:arriba:12', text: /^ Descartar $/ })).toBe(true)
  await ui.unmount()
})

test('Menú: Separar pasos, con la letra atenuada de las órdenes de los pasos, en las que tienen dos pasos pendientes o más', async (...m) => {
  const cola: Pet[] = [
    { id: 9, texto: 'Para separar', estado: 'en-cola', pasos: [{ texto: 'Uno', estado: 'pendiente' }, { texto: 'Dos', estado: 'pendiente' }] },
  ]
  await preparar(m, { desplegadas: true, cola })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await etiqueta(ui, 'split-tarea:cola:9')).toMatchObject({ color: '#717171', backgroundColor: FONDO_ORDEN })
  expect(await hay(ui, { type: 'Button', key: 'split-tarea:cola:9', text: /^ Separar pasos $/ })).toBe(true)
  await ui.unmount()
})

test('Menú: Redescribir, en las que tienen descripción, pide a Claude lo mismo que /sf_redescribir, sin tocar la cola', async (...m) => {
  const cola: Pet[] = [
    { id: 9, texto: 'Con descripción', estado: 'en-cola', descripcion: 'Un texto que no se entiende.' },
    { id: 10, texto: 'Sin descripción', estado: 'en-cola' },
    { id: 11, texto: 'En observación', estado: 'en-observacion', descripcion: 'Otro texto.' },
  ]
  const { archivos, prompts, toasts } = await preparar(m, { desplegadas: true, cola })
  const antes = archivos[COLA]
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'sec:observacion' })
  for (const k of ['cola:9', 'observacion:11']) expect(await hay(ui, { type: 'Button', key: `redescribir-tarea:${k}`, text: /^ Redescribir $/ })).toBe(true)
  expect(await ui.find({ type: 'Button', key: 'redescribir-tarea:cola:10' })).toBe(undefined)
  await ui.press({ key: 'redescribir-tarea:cola:9' })
  expect(toasts).toContain('Redescribir: se lo paso a Claude.')
  await new Promise(fin => setTimeout(fin, 200))
  expect(prompts.some(t => t.startsWith('Redacta de nuevo la descripción de la 9 («Con descripción»)'))).toBe(true)
  expect(archivos[COLA]).toBe(antes)
  await ui.unmount()
})

test('Menú: «?», en toda tarea desplegada, pide a Claude que la explique, sin tocar la cola', async (...m) => {
  const cola: Pet[] = [
    { id: 9, texto: 'En cola', estado: 'en-cola', descripcion: 'Algo.' },
    { id: 10, texto: 'Sin descripción', estado: 'en-cola' },
    { id: 11, texto: 'En observación', estado: 'en-observacion' },
  ]
  const { archivos, prompts, toasts } = await preparar(m, { desplegadas: true, cola })
  const antes = archivos[COLA]
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'sec:observacion' })
  for (const k of ['cola:9', 'cola:10', 'observacion:11']) expect(await hay(ui, { type: 'Button', key: `explicar-tarea:${k}`, text: /^ \? $/ })).toBe(true)
  // En verde, sobre el fondo de las órdenes, tras Redescribir y antes de la que destruye.
  expect(await etiqueta(ui, 'explicar-tarea:cola:9')).toMatchObject({ color: 'success', backgroundColor: FONDO_ORDEN })
  const orden = ((await ui.findAll({ type: 'Button' })) as { key?: string }[]).map(b => String(b.key)).filter(k => k.endsWith(':cola:9'))
  const pos = (pre: string) => orden.findIndex(k => k.startsWith(pre))
  expect(pos('redescribir-tarea') < pos('explicar-tarea') && pos('explicar-tarea') < pos('eliminar-tarea')).toBe(true)
  await ui.press({ key: 'explicar-tarea:cola:10' })
  expect(toasts).toContain('«?»: le pido a Claude que explique la 10.')
  await new Promise(fin => setTimeout(fin, 200))
  expect(prompts.some(t => t.startsWith('Explícame la 10 («Sin descripción») de forma breve y sencilla') && t.includes('qué espera de mí'))).toBe(true)
  expect(archivos[COLA]).toBe(antes)
  await ui.unmount()
})

test('Menú: Paso +, solo arriba, deja «/sf_paso N » en el prompt para escribir el paso, sin tocar la cola', async (...m) => {
  const { archivos, rellenos, prompts } = await preparar(m, { desplegadas: true, cola: ELIMINABLES })
  const antes = archivos[COLA]
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  for (const k of ['arriba:1', 'arriba:6']) expect(await hay(ui, { type: 'Button', key: `paso-tarea:${k}` })).toBe(true)
  for (const k of ['cola:7', 'cola:8', 'observacion:2']) expect(await ui.find({ type: 'Button', key: `paso-tarea:${k}` })).toBe(undefined)
  await ui.press({ key: 'paso-tarea:arriba:6' })
  await new Promise(fin => setTimeout(fin, 200))
  expect(rellenos).toEqual(['/sf_paso 6 '])
  expect(prompts).toHaveLength(0)
  expect(archivos[COLA]).toBe(antes)
  await ui.unmount()
})

test('Cerradas: sin rama, desplegada, la línea empieza por el commit, en la columna 0', async (...m) => {
  const { cambiarCola } = await preparar(m, { cola: [] })
  await cambiarCola([], [{ ...CERRADA_4, commit: 'sf 0.9' }])
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'hecho:4' })
  expect(await hay(ui, { type: 'Text', text: /^Commit: sf 0\.9$/ })).toBe(true)
  expect(await sangrias(ui, /^Commit: sf 0\.9$/)).toEqual([])
  await ui.unmount()
})

// Sangría colgante en los títulos (decisión del propietario, 2026-10-31): lo que va antes del título (relleno,
// número y espacio), en una columna de ancho fijo; el título, a su derecha y encogible: al partirse, sus líneas
// siguientes empiezan en su columna, no en la 0.
const columnaDe = async (ui: { drawn: () => Promise<unknown> }, titulo: string, ...mas: string[]) => {
  const r = fila((await ui.drawn()) as Nodo, titulo, ...mas)
  const [izq, der] = r ? hijos(r) : []
  return { ancho: izq?.props?.width, fija: izq?.props?.flexShrink, encoge: der?.props?.flexShrink, titulo: JSON.stringify(der ?? {}).includes(titulo) }
}

test('Un título largo que se parte sigue en la columna del título, arriba y en Pendientes', async (...m) => {
  const larga = 'Analizar el trabajo con la SF en el desarrollo del panel, con un título que no cabe'
  await preparar(m, {
    cola: [
      { id: 194, texto: larga, estado: 'en-curso' },
      { id: 7, texto: `${larga} (en cola)`, estado: 'en-cola', pasos: [{ texto: 'Uno', estado: 'pendiente' }] },
    ],
  })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // Arriba, «194 »: número (3) y espacio (1).
  expect(await columnaDe(ui, larga)).toEqual({ ancho: 4, fija: 0, encoge: 1, titulo: true })
  // En Pendientes, plegada y desplegada, «  7 »: hueco, número y espacio, como arriba.
  expect(await columnaDe(ui, `${larga} (en cola)`)).toEqual({ ancho: 4, fija: 0, encoge: 1, titulo: true })
  await ui.press({ key: 'pet:cola:7:num' })
  expect(await columnaDe(ui, `${larga} (en cola)`)).toEqual({ ancho: 4, fija: 0, encoge: 1, titulo: true })
  expect(await hay(ui, { type: 'Text', text: /^Pasos/ })).toBe(true)
  // El número y el título despliegan y pliegan los dos; el subrayado, solo en el número.
  expect(await hay(ui, { type: 'Button', key: 'pet:cola:7' })).toBe(true)
  await ui.press({ key: 'pet:cola:7' })
  expect(await hay(ui, { type: 'Text', text: /^Pasos/ })).toBe(false)
  expect((await numeros(ui, 7)).map(x => x.props.underline)).toEqual([true])
  await ui.unmount()
})

// El tipo de cada tarea, tras su título, entre paréntesis, en mayúsculas y atenuado (decisión del propietario,
// 2026-10-31): arriba, en Pendientes, En observación y Cerradas; sin tipo, nada.
test('Tipo: tras el título, « (deliberar)» en minúsculas y en el color del título, arriba, en Pendientes, En observación y Cerradas; sin tipo, nada', async (...m) => {
  const { cambiarCola } = await preparar(m, { cola: [] })
  await cambiarCola(
    [
      { id: 4, texto: 'Analizar el trabajo', estado: 'en-curso', tipo: 'deliberar' },
      { id: 6, texto: 'Escribirlo', estado: 'en-cola', tipo: 'documentar' },
      { id: 7, texto: 'Sin tipo', estado: 'en-cola' },
      { id: 8, texto: 'Mirarlo', estado: 'en-observacion', tipo: 'corregir' },
    ],
    [{ id: 9, texto: 'Hecha', estado: 'cerrada', tipo: 'implementar', historial: [ev('cerrada', 'sin rama')] }],
  )
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'sec:observacion' })
  for (const [titulo, tipo] of [['Analizar el trabajo', 'deliberar'], ['Escribirlo', 'documentar'], ['Mirarlo', 'corregir'], ['Hecha', 'implementar']]) {
    expect(await hay(ui, { type: 'Text', text: new RegExp(`^${titulo} \\(${tipo}\\)$`) })).toBe(true)
    const marca = (await ui.find({ type: 'Text', text: new RegExp(`^ \\(${tipo}\\)$`) })) as Nodo | undefined
    expect(marca?.props.dimColor).toBeUndefined()
    expect(marca?.props.color).toBeUndefined()
  }
  expect(await hay(ui, { type: 'Text', text: /^Sin tipo$/ })).toBe(true)
  await ui.unmount()
})

test('Tipo: tras el título entero, sin romper la sangría colgante', async (...m) => {
  const larga = 'Una tarea en cola con un título muy largo que no cabe en el panel'
  await preparar(m, { cola: [{ id: 6, texto: larga, estado: 'en-cola', tipo: 'investigar' }] })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // Plegada, sin recortar: el título entero y el tipo, a la derecha de la columna del número («  6 », 4).
  expect(await hay(ui, { type: 'Text', text: /…/ })).toBe(false)
  expect(await columnaDe(ui, larga)).toEqual({ ancho: 4, fija: 0, encoge: 1, titulo: true })
  expect(JSON.stringify(fila((await ui.drawn()) as Nodo, larga)).includes(' (investigar)')).toBe(true)
  await ui.unmount()
})

// Plegadas, las tareas de Pendientes, En observación y Cerradas, como las de arriba (decisión del propietario, 2026-10-31):
// solo «número título (tipo)», con el título entero; ni la cuenta de pasos ni la ✓ de Claude delante.
test('Secciones: la tarea plegada muestra solo número, título entero y tipo', async (...m) => {
  const larga = 'Una tarea observada con un título muy largo que no cabe en una sola línea del panel'
  await preparar(m, {
    cola: [
      {
        id: 8,
        texto: larga,
        estado: 'en-observacion',
        tipo: 'investigar',
        comprobado: 'lo abrí',
        pasos: [
          { texto: 'A', estado: 'hecho' },
          { texto: 'B', estado: 'pendiente' },
        ],
      },
    ],
  })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  if (!(await hay(ui, { type: 'Button', key: 'pet:observacion:8' }))) await ui.press({ key: 'sec:observacion' })
  // A la izquierda, solo «  8 » (hueco, número y espacio); a la derecha, el título entero con su tipo.
  expect(await columnaDe(ui, `${larga} (investigar)`)).toEqual({ ancho: 4, fija: 0, encoge: 1, titulo: true })
  expect(await hay(ui, { type: 'Text', text: /…/ })).toBe(false)
  expect(await hay(ui, { type: 'Text', text: /1\/2/ })).toBe(false)
  expect(await hay(ui, { type: 'Text', text: /✓/ })).toBe(false)
  // Desplegada, la ✓ en «Prueba» y la cuenta en «Pasos».
  await ui.press({ key: 'pet:observacion:8' })
  await ui.press({ key: 'prueba:observacion:8' })
  expect(await hay(ui, { type: 'Text', text: /^Lo abrí$/ })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /1\/2/ })).toBe(true)
  await ui.unmount()
})

// Las tareas de las secciones, con la misma sangría que las de arriba (decisión del propietario, 2026-10-31): el
// número, en la misma columna. La columna de una fila: la suma de los paddingLeft de sus antepasados.
const sangriaDe = (raiz: Nodo, objetivo: Nodo): number | undefined => {
  if (raiz === objetivo) return 0
  for (const h of hijos(raiz)) {
    const x = sangriaDe(h, objetivo)
    if (x !== undefined) return x + Number(raiz.props?.paddingLeft ?? 0)
  }
  return undefined
}
test('Secciones de tareas: el número, en la misma columna que el de las tareas de arriba', async (...m) => {
  await preparar(m, {
    cola: [
      { id: 4, texto: 'Arriba en curso', estado: 'en-curso' },
      { id: 6, texto: 'En Pendientes', estado: 'en-cola' },
      { id: 8, texto: 'En observación', estado: 'en-observacion' },
    ],
  })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  if (!(await hay(ui, { type: 'Text', text: /^En observación$/ }))) await ui.press({ key: 'sec:observacion' })
  const raiz = (await ui.drawn()) as Nodo
  const columna = (t: string) => {
    const f = fila(raiz, t)
    return f ? [sangriaDe(raiz, f), hijos(f)[0]?.props?.width] : []
  }
  // Arriba, «  4 »: columna 0 y 4 de ancho; en Pendientes y en observación, igual.
  expect(columna('Arriba en curso')).toEqual([0, 4])
  expect(columna('En Pendientes')).toEqual([0, 4])
  expect(columna('En observación')).toEqual([0, 4])
  await ui.unmount()
})

// Los números de tarea, en tres columnas alineados a la derecha, en todos los apartados (petición del propietario,
// 2026-10-31): «  4», « 41», «236» y un espacio. El hueco va como margen de la columna, fuera del botón del número.
test('Números de tarea en tres columnas, a la derecha, arriba, en Pendientes, En observación y Cerradas', async (...m) => {
  const { cambiarCola } = await preparar(m, { cola: [] })
  await cambiarCola(
    [
      { id: 4, texto: 'Arriba uno', estado: 'en-curso' },
      { id: 236, texto: 'Arriba tres', estado: 'en-curso', descripcion: 'Con detalle.' },
      { id: 41, texto: 'Pendiente dos', estado: 'en-cola' },
      { id: 5, texto: 'Pendiente uno', estado: 'en-cola', descripcion: 'Con detalle.' },
      { id: 7, texto: 'Observada uno', estado: 'en-observacion', commit: 'x' },
      { id: 120, texto: 'Observada tres', estado: 'en-observacion' },
    ],
    [{ id: 9, texto: 'Cerrada uno', estado: 'cerrada', commit: 'y', historial: [ev('cerrada', 'sin rama')] }],
  )
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  if (!(await hay(ui, { type: 'Text', text: /^Observada uno$/ }))) await ui.press({ key: 'sec:observacion' })
  if (!(await hay(ui, { type: 'Text', text: /^Cerrada uno$/ }))) await ui.press({ key: 'sec:hecho' })
  const raiz = (await ui.drawn()) as Nodo
  const columna = (t: string) => {
    const izq = hijos(fila(raiz, t) as Nodo)[0]
    return [izq?.props?.paddingLeft ?? 0, izq?.props?.width]
  }
  for (const [t, hueco] of [
    ['Arriba uno', 2],
    ['Arriba tres', 0],
    ['Pendiente dos', 1],
    ['Pendiente uno', 2],
    ['Observada uno', 2],
    ['Observada tres', 0],
    ['Cerrada uno', 2],
  ] as const)
    expect([t, ...columna(t)]).toEqual([t, hueco, 4])
  // Ningún número lleva espacios delante dentro de su botón: el botón no los recorta.
  expect(await hay(ui, { type: 'Button', text: /^ +\d/ })).toBe(false)
  await ui.unmount()
})

// Pendientes y En observación se ven siempre, también con 0, como Cerradas (petición del propietario, 2026-10-31).
test('Pendientes, En observación y Cerradas se ven con 0', async (...m) => {
  await preparar(m, { cola: [{ id: 4, texto: 'Solo en curso', estado: 'en-curso' }] })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  for (const t of ['PENDIENTES', 'EN OBSERVACIÓN', 'CERRADAS']) expect(await hay(ui, { type: 'Button', text: new RegExp(`^${t} [▸▾] 0$`) })).toBe(true)
  await ui.unmount()
})

// La cabecera de una sección (decisión del propietario, 2026-10-31): el nombre en mayúsculas y, a su derecha, el icono
// de desplegar, antes de la cuenta: «PENDIENTES ▸ 1». Las claves no cambian.
test('Secciones: cabecera en mayúsculas, con el icono tras el nombre y antes de la cuenta', async (...m) => {
  await preparar(m, { cola: [{ id: 6, texto: 'En Pendientes', estado: 'en-cola' }] })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  const cabecera = async () => String(((await ui.find({ type: 'Button', key: 'sec:cola' })) as { text?: unknown } | undefined)?.text ?? '')
  const antes = await cabecera()
  expect(antes).toMatch(/^PENDIENTES [▸▾] 1$/)
  await ui.press({ key: 'sec:cola' })
  const despues = await cabecera()
  expect(despues).toMatch(/^PENDIENTES [▸▾] 1$/)
  expect(new Set([antes, despues])).toEqual(new Set(['PENDIENTES ▸ 1', 'PENDIENTES ▾ 1']))
  // Ninguna cabecera empieza por el icono.
  expect(await hay(ui, { type: 'Button', text: /^[▸▾]/ })).toBe(false)
  expect(await hay(ui, { type: 'Button', text: /^CERRADAS [▸▾] 0$/ })).toBe(true)
  await ui.unmount()
})

// Las propuestas, como las tareas (decisión del propietario, 2026-10-31): el número en una columna de ancho
// fijo, común a todas; el título entero a su derecha, con sangría colgante; el resumen, en la columna del título.
test('Propuestas: el título, entero en la columna tras el número; desplegada, el resumen en esa columna', async (...m) => {
  const larga = 'El detalle, solo cuando está claro, con un título largo que no cabe en una sola línea del panel'
  const md = PROPUESTAS_EJ.replace('### P02 El detalle, solo cuando está claro', `### P02 ${larga}`).replace(
    '### P03 Otra ya decidida',
    '### P110 Otra por decidir\n\n- **Estado:** pendiente de decisión.\n\n### P03 Otra ya decidida',
  )
  await preparar(m, { extra: { [PROPUESTAS]: md } })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  if (!(await hay(ui, { type: 'Text', text: /^Otra por decidir$/ }))) await ui.press({ key: 'sec:propuestas' })
  // «P110» manda: la columna, 4 y un espacio; «P02», alineado a la derecha.
  expect(await columnaDe(ui, larga)).toEqual({ ancho: 5, fija: 0, encoge: 1, titulo: true })
  expect(await hay(ui, { type: 'Text', text: /…/ })).toBe(false)
  // Sin rótulo ni cuentas encima de la lista.
  expect(await hay(ui, { type: 'Text', text: /esperan tu sí o no|abiertas ·|sin kanban/ })).toBe(false)
  await ui.press({ key: `prop:${larga}` })
  expect(await sangrias(ui, /^Detallar solo lo que está claro/)).toEqual([5])
  await ui.unmount()
})

// «Descripción» y «Pasos N/M», con el brillo de la línea de la rama (decisión del propietario, 2026-10-31): atenuados,
// como «Rama: …»; los rótulos, subrayados de desplegable.
test('Desplegada: «Descripción» y «Pasos» con el brillo de la rama', async (...m) => {
  await preparar(m, { cola: [{ ...COMPLETA, estado: 'en-cola' }], extra: GIT('ref: refs/heads/develop\n') })
  const ui = await m[0].ui.mount({ ...ANCHO, surface: 'terminal' })
  await ui.press({ key: 'pet:cola:7' })
  type T = { props: Record<string, unknown> }
  const estilo = async (text: RegExp) => {
    // El más interno: la línea de la rama va dentro de la Text que la junta con el commit.
    const t = ((await ui.findAll({ type: 'Text', text })) as T[]).at(-1)
    return { dim: t?.props.dimColor, color: t?.props.color }
  }
  const rama = await estilo(/^Rama: feature\/7-completa/)
  expect(rama).toEqual({ dim: true, color: undefined })
  expect(await estilo(/^Descripción$/)).toEqual(rama)
  expect(await estilo(/^Pasos$/)).toEqual(rama)
  expect(await estilo(/^ 1\/2$/)).toEqual(rama)
  expect(((await ui.find({ type: 'Text', text: /^Descripción$/ })) as T).props.underline).toBe(true)
  expect(((await ui.find({ type: 'Text', text: /^Pasos$/ })) as T).props.underline).toBe(true)
  await ui.unmount()
})


// ── Avisos del panel (tarea 228) ──
// Un mensaje del propietario, escrito en la terminal.
const escribe = (m: Motor, text: string) => m[0].prompt.submit({ text, origin: { kind: 'composer' }, wait: false })
const SUB_12 = { evento: 'subagente', fecha: new Date(AHORA - 100_000).toISOString(), quien: 'principal', via: 'cli', detalle: 'D:/wt-12 · sub-12' }
const AVISABLES: Pet[] = [
  {
    id: 13,
    texto: 'En curso desde el panel',
    estado: 'en-curso',
    historial: [ev('en-curso', undefined, 2), { evento: 'paso', fecha: new Date(AHORA + 3000).toISOString(), quien: 'principal', via: 'cli', detalle: 'añadido 1: algo' }],
  },
]
const CERRADA_12: Pet = { id: 12, texto: 'Cerrada con la C', estado: 'cerrada', historial: [SUB_12, ev('cerrada', 'develop c0ffee1', 4)] }

test('Avisos del panel: el mensaje del propietario lleva lo cambiado desde el panel, y el siguiente ya no', async (...m) => {
  const { contextos, reloj } = await preparar(m, { cola: AVISABLES, salidas: [CERRADA_12], reloj: true })
  await reloj!.advance(10_000)
  await escribe(m, 'hola')
  // Lo de Claude (via cli) no se avisa; el cierre con la C pide recoger el subagente.
  expect(contextos.at(-1)).toEqual([
    'Desde el panel: la 13, en curso; cerrada la 12. Recoge el subagente de la 12 (D:/wt-12 · sub-12): páralo, quita su worktree y borra su rama auxiliar.',
  ])
  await reloj!.advance(5000)
  await escribe(m, 'otra cosa')
  expect(contextos.at(-1)).toBe(undefined)
})

test('Avisos del panel: con la recogida de cola.py (tarea 246), pide solo detener el subagente, y dice lo que quedó', async (...m) => {
  const recogida = (id: number, evento: string, detalle: string): Pet => ({
    id,
    texto: 'Con subagente',
    estado: id === 12 ? 'cerrada' : 'descartada',
    historial: [SUB_12, ev(id === 12 ? 'cerrada' : 'descartada', undefined, 4), ev(evento, detalle, 4)],
  })
  const { contextos, reloj } = await preparar(m, {
    cola: [recogida(14, 'recogida-con-avisos', 'queda el worktree D:/wt-12: tiene cambios sin commit')],
    salidas: [recogida(12, 'recogida', 'D:/wt-12, sub-12')],
    reloj: true,
  })
  await reloj!.advance(10_000)
  await escribe(m, 'hola')
  expect(contextos.at(-1)).toEqual([
    'Desde el panel: cerrada la 12; descartada la 14. Detén el subagente de la 12: cola.py ya quitó su worktree y su rama auxiliar. ' +
      'Detén el subagente de la 14; al recogerlo, cola.py avisó: queda el worktree D:/wt-12: tiene cambios sin commit.',
  ])
})

test('Avisos del panel: un prompt que no es del propietario no lleva el aviso ni lo gasta', async (...m) => {
  const { contextos, reloj } = await preparar(m, { cola: AVISABLES, reloj: true })
  await reloj!.advance(10_000)
  await m[0].prompt.submit({ text: 'aviso', origin: { kind: 'task-notification' }, wait: false })
  expect(contextos.at(-1)).toBe(undefined)
  await escribe(m, 'hola')
  expect(contextos.at(-1)).toEqual(['Desde el panel: la 13, en curso.'])
})

test('Avisos del panel: la C cierra y el mensaje siguiente lo dice; sin subagente, no pide recogerlo', async (...m) => {
  const { contextos, reloj, ui } = await cerrarLa12(m, {})
  await reloj!.advance(3000)
  await escribe(m, '¿cerramos la 12?')
  expect(contextos.at(-1)).toEqual(['Desde el panel: cerrada la 12.'])
  await ui.unmount()
})

test('Avisos del panel: /reload-plugins no pierde lo cambiado antes de recargar ni repite lo ya dado (tarea 285)', async (...m) => {
  const { contextos, reloj } = await preparar(m, { cola: AVISABLES, salidas: [CERRADA_12], reloj: true })
  await reloj!.advance(10_000)
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  await reloj!.advance(2000)
  await escribe(m, 'hola')
  expect(contextos.at(-1)?.[0]).toMatch(/^Desde el panel: la 13, en curso; cerrada la 12\./)
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  await reloj!.advance(2000)
  await escribe(m, 'otra cosa')
  expect(contextos.at(-1)).toBe(undefined)
})

test('Avisos del panel: /reload-plugins que cambia de plugin y vacía el estado tampoco pierde ni repite (tarea 285)', async (...m) => {
  const vaciar = estadoVaciable(m[1])
  const { contextos, reloj } = await preparar(m, { cola: AVISABLES, salidas: [CERRADA_12], reloj: true })
  // Los cambios del panel llegan antes de recargar; nadie los ha avisado aún.
  await reloj!.advance(10_000)
  vaciar()
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  await reloj!.advance(2000)
  await escribe(m, 'hola')
  expect(contextos.at(-1)?.[0]).toMatch(/^Desde el panel: la 13, en curso; cerrada la 12\./)
  vaciar()
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  await reloj!.advance(2000)
  await escribe(m, 'otra cosa')
  expect(contextos.at(-1)).toBe(undefined)
})

test('Avisos del panel: al reanudar una sesión de hace más de 12 horas, no avisa lo cambiado entonces ni pide recoger subagentes de tareas cerradas entonces (tarea 351)', async (...m) => {
  const vaciar = estadoVaciable(m[1])
  const { contextos, reloj, guardado } = await preparar(m, { cola: AVISABLES, salidas: [CERRADA_12], reloj: true })
  await reloj!.advance(10_000)
  // Lo último avisado en esta sesión, hace 13 horas; el proceso es nuevo, con el estado vacío.
  guardado.avisadoPanel = { sesion: 'sesion-1', avisado: AHORA - 13 * 3600_000 }
  vaciar()
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  await reloj!.advance(2000)
  await escribe(m, 'hola')
  expect((contextos.at(-1) ?? []).filter(c => c.startsWith('Desde el panel'))).toEqual([])
})

test('Avisos del panel: una versión anterior del mod cargada entre medias (el modo prueba) no hace perder lo cambiado (tarea 285, reabierta)', async (...m) => {
  const estado = estadoVaciable(m[1])
  const { contextos, reloj, archivos } = await preparar(m, { cola: AVISABLES, salidas: [CERRADA_12], reloj: true })
  // Un mensaje antes de los cambios del panel: nada que avisar, pero queda dado hasta aquí.
  await escribe(m, 'antes')
  expect(contextos.at(-1)).toBe(undefined)
  await reloj!.advance(10_000)
  // Se cierra en el panel y se apaga el modo prueba: carga la versión publicada, anterior, que pone el «desde» en la
  // hora de su carga y reescribe .sf/subagentes.json a su manera; se vuelve a encender, y carga este mod.
  estado.poner('avisadoPanel', AHORA + 10_000)
  delete archivos['/sf/.sf/subagentes.json']
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  await reloj!.advance(2000)
  await escribe(m, 'hola')
  expect(contextos.at(-1)?.[0]).toMatch(/^Desde el panel: la 13, en curso; cerrada la 12\./)
  // Sin cambios nuevos, no lo repite.
  await reloj!.advance(10_000)
  await escribe(m, 'nada nuevo')
  expect(contextos.at(-1)).toBe(undefined)
})

// Al reanudar la conversación, el $.store de su sesión guarda hasta dónde se avisó hace días: lo hecho desde el panel
// entre medias se dijo en otras sesiones, no aquí (tarea 350).
test('Avisos del panel: al reanudar la conversación cuentan desde ahí, aunque el $.store guarde un aviso viejo (tarea 350)', async (...m) => {
  const vaciar = estadoVaciable(m[1])
  const { contextos, reloj, guardado } = await preparar(m, { cola: AVISABLES, salidas: [CERRADA_12], reloj: true })
  await reloj!.advance(10_000)
  // Un proceso nuevo con la misma sesión: el estado, vacío; el $.store, con el aviso de cuando se dejó.
  vaciar()
  guardado.avisadoPanel = { sesion: 'sesion-1', avisado: AHORA - 3 * 86400_000 }
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  await m[0].classic.SessionStart({ source: 'resume' })
  await reloj!.advance(2000)
  await escribe(m, 'hola')
  expect(contextos.at(-1)?.some(c => c.startsWith('Desde el panel'))).not.toBe(true)
})

// Un mensaje que llega con el estado recién vaciado, antes de que el mod lo cargue: el aviso sigue desde el último
// dado en la sesión, no desde el principio del historial (tarea 350).
test('Avisos del panel: un mensaje con el estado vacío, antes de cargar, no avisa de todo lo hecho desde el panel (tarea 350)', async (...m) => {
  const vaciar = estadoVaciable(m[1])
  const vieja: Pet = { id: 11, texto: 'Cerrada hace días', estado: 'cerrada', historial: [ev('cerrada', 'develop abc1234', ANTES)] }
  const { contextos, reloj } = await preparar(m, { cola: AVISABLES, salidas: [vieja, CERRADA_12], reloj: true })
  await escribe(m, 'antes')
  expect(contextos.at(-1)).toBe(undefined)
  await reloj!.advance(10_000)
  vaciar()
  await escribe(m, 'hola')
  expect(contextos.at(-1)?.[0]).toMatch(/^Desde el panel: la 13, en curso; cerrada la 12\./)
  expect(contextos.at(-1)?.[0]).not.toMatch(/la 11/)
})

test('Avisos del panel: tras un /clear cuentan desde ahí', async (...m) => {
  const { contextos, reloj } = await preparar(m, { cola: AVISABLES, salidas: [CERRADA_12], reloj: true })
  await reloj!.advance(10_000)
  await m[0].classic.SessionStart({ source: 'clear' })
  await reloj!.advance(2000)
  await escribe(m, 'hola')
  expect(contextos.at(-1)?.some(c => c.startsWith('Desde el panel'))).not.toBe(true)
})

test('Avisos del panel: un cierre en el panel y luego un encargo del panel a Claude: el aviso va con el encargo, y el mensaje siguiente ya no lo repite (tarea 285)', async (...m) => {
  // La 12 se cierra con la C (sin subagente) y, después, «Activar rama» de la 6 falla por choques: el panel pasa el
  // encargo a Claude con un temporizador. El hook prompt.submit del mod no ve ese prompt (el motor lo salta).
  const probar = { ok: false, mensaje: 'No se activa', fallo: 'choques', motivo: 'choques al integrar develop en feature/6-algo: a.txt' }
  const a = await preparar(m, { desplegadas: true, cola: DESCARTABLES, salidas: [CERRADA_12], extra: EXTRA_PROBAR, reloj: true, respuestas: { probar } })
  await a.reloj!.advance(10_000)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'probar-tarea:arriba:6' })
  await a.reloj!.advance(100)
  expect(a.prompts).toHaveLength(1)
  const encargo = a.prompts[0]!
  expect(encargo).toMatch(/^Activa la rama de la 6/)
  expect(encargo).toContain('\n\nDesde el panel: cerrada la 12. Recoge el subagente de la 12')
  await a.reloj!.advance(5000)
  await escribe(m, 'hola')
  expect(a.contextos.at(-1)).toBe(undefined)
  await ui.unmount()
})

test('Avisos del panel: si el encargo del panel no llega a enviarse, el aviso queda para el mensaje siguiente (tarea 285)', async (...m) => {
  const probar = { ok: false, mensaje: 'No se activa', fallo: 'choques', motivo: 'choques al integrar develop en feature/6-algo: a.txt' }
  // El motor no admite el encargo del panel.
  m[1]('prompt.submit', { origin: { kind: 'plugin' } } as never, () => {
    throw new Error('no')
  })
  const a = await preparar(m, { desplegadas: true, cola: DESCARTABLES, salidas: [CERRADA_12], extra: EXTRA_PROBAR, reloj: true, respuestas: { probar } })
  await a.reloj!.advance(10_000)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'probar-tarea:arriba:6' })
  await a.reloj!.advance(100)
  expect(a.toasts.some(t => t.includes('no se pudo'))).toBe(true)
  await escribe(m, 'hola')
  expect(a.contextos.at(-1)?.[0]).toMatch(/^Desde el panel: cerrada la 12\./)
  await ui.unmount()
})

test('Avisos del panel: si no se puede leer la cola, el mensaje no gasta el aviso: va en el siguiente (tarea 285)', async (...m) => {
  const { contextos, reloj, archivos } = await preparar(m, { cola: AVISABLES, reloj: true })
  await reloj!.advance(10_000)
  const cola = archivos[COLA]!
  archivos[COLA] = '{"peticiones": ['
  await escribe(m, 'hola')
  expect(contextos.at(-1)).toBe(undefined)
  archivos[COLA] = cola
  await escribe(m, 'otra')
  expect(contextos.at(-1)).toEqual(['Desde el panel: la 13, en curso.'])
})

test('Avisos del panel: cada evento, como frase corta, sin la rama ni el detalle crudo', async (...m) => {
  const cola: Pet[] = [
    { id: 20, texto: 'Con la T', estado: 'en-curso', rama: 'feature/20-t', historial: [ev('probar', 'feature/20-t', 1)] },
    { id: 21, texto: 'Con pasos', estado: 'en-curso', historial: [ev('paso', 'añadido 2: Revisar el color', 2), ev('paso', '1 hecho: Elegir', 3), ev('tipo', 'corregir (antes: implementar)', 4)] },
    { id: 22, texto: 'Fusionada', estado: 'en-cola', historial: [ev('fusion', 'absorbe 23', 5)] },
  ]
  const { contextos, reloj } = await preparar(m, { cola, salidas: [{ id: 23, texto: 'x', estado: 'absorbida', historial: [ev('absorbida', 'en 22', 5)] }], reloj: true })
  await reloj!.advance(10_000)
  await escribe(m, 'hola')
  expect(contextos.at(-1)).toEqual([
    'Desde el panel: la 20, en prueba; la 21, paso añadido: «Revisar el color»; la 21, paso 1 hecho; la 21, de tipo corregir; la 22 absorbe la 23.',
  ])
})


// ── Avisos de subagentes (tarea 249) ──
// Las en curso de INICIAL: la 1 y la 4. Un informe de cola.py, `segundos` después de AHORA.
const informe = (segundos: number) => ({ evento: 'informe', fecha: new Date(AHORA + 1000 * segundos).toISOString(), quien: 'principal', via: 'cli', detalle: 'terminado' })
// El aviso de lanzar los que faltan (tarea 351): aparte, imperativo y, en el mensaje, el primero.
const LANZA = (ns: number[], nueva = false) =>
  `ANTES DE NADA, en este turno y antes de contestar: lanza el subagente de cada tarea en curso que no lo tiene: ${ns.map(n => `la ${String(n)} («Tarea ${String(n)}: …»)`).join(', ')}.` +
  (nueva ? ' Sesión nueva: los de la anterior ya no viven.' : '')
const RECOGE = (n: number) => `el subagente de la ${String(n)} ha terminado: recógelo (revisar el diff, merge --ff-only, \`python -I -X utf8 "$HOME/.claude/sf/cola.py" informe ${String(n)}\`, pasos, listo)`

test('Avisos de subagentes: al abrir la sesión, lanzar el de cada tarea en curso; y en cada mensaje mientras falten, sin «Sesión nueva» (tarea 351)', async (...m) => {
  const agentes: Agente[] = []
  const { contextos } = await preparar(m, { agentes })
  await escribe(m, 'hola')
  expect(contextos.at(-1)).toEqual([LANZA([1, 4], true)])
  await escribe(m, 'otra cosa')
  expect(contextos.at(-1)).toEqual([LANZA([1, 4])])
  agentes.push({ description: 'Tarea 1: panel', status: 'running' }, { description: 'Tarea 4: fondos', status: 'running' })
  await escribe(m, 'lanzados')
  expect(contextos.at(-1)).toBe(undefined)
})

test('Avisos de subagentes: el de lanzar va el primero, antes de lo cambiado desde el panel (tarea 351)', async (...m) => {
  const { contextos, reloj } = await preparar(m, { cola: AVISABLES, salidas: [CERRADA_12], reloj: true, agentes: [] })
  await reloj!.advance(10_000)
  await escribe(m, 'hola')
  const c = contextos.at(-1)!
  expect(c[0]).toMatch(/^ANTES DE NADA, en este turno y antes de contestar: lanza el subagente de cada tarea en curso que no lo tiene: la 13 /)
  expect(c[1]).toMatch(/^Desde el panel: /)
})

test('Avisos de subagentes: el que termina pide recogerlo, en su notificación; con el informe anotado, nada; si vuelve a trabajar y termina, otra vez', async (...m) => {
  const agentes: Agente[] = [{ description: 'Tarea 1: panel', status: 'running' }]
  const { contextos, reloj, cambiarCola } = await preparar(m, { agentes, reloj: true })
  await escribe(m, 'hola')
  expect(contextos.at(-1)).toEqual([LANZA([4], true)])
  agentes.push({ description: 'Tarea 4: fondos', status: 'running' })
  await reloj!.advance(5000)
  agentes[0]!.status = 'completed'
  await m[0].prompt.submit({ text: 'El subagente ha terminado', origin: { kind: 'task-notification' }, wait: false })
  expect(contextos.at(-1)).toEqual([`Subagentes: ${RECOGE(1)}.`])
  // Recogido: cola.py informe, después de verlo trabajar.
  await reloj!.advance(5000)
  await cambiarCola(INICIAL.map(p => (p.id === 1 ? { ...p, historial: [informe(8)] } : p)))
  await escribe(m, 'sigue')
  expect(contextos.at(-1)).toBe(undefined)
  // Retomado con SendMessage: trabaja y vuelve a terminar después del informe.
  agentes[0]!.status = 'running'
  await reloj!.advance(5000)
  await escribe(m, 'y ahora')
  expect(contextos.at(-1)).toBe(undefined)
  agentes[0]!.status = 'completed'
  await m[0].prompt.submit({ text: 'El subagente ha terminado', origin: { kind: 'task-notification' }, wait: false })
  expect(contextos.at(-1)).toEqual([`Subagentes: ${RECOGE(1)}.`])
})

test('Avisos de subagentes: el que se para vuelve a pedir lanzarlo; sin la lista del motor, no se avisa', async (...m) => {
  const agentes: Agente[] = [
    { description: 'Tarea 1: panel', status: 'running' },
    { description: 'Tarea 4: fondos', status: 'running' },
  ]
  const { contextos } = await preparar(m, { agentes })
  await escribe(m, 'hola')
  expect(contextos.at(-1)).toBe(undefined)
  agentes[1]!.status = 'killed'
  await escribe(m, 'sigue')
  expect(contextos.at(-1)).toEqual([LANZA([4])])
})

for (const source of ['compact', 'clear'] as const)
  test(`Avisos de subagentes: tras ${source === 'clear' ? 'un /clear' : 'compactar'}, lo pendiente se vuelve a avisar, sin «Sesión nueva»`, async (...m) => {
    const agentes: Agente[] = [
      { description: 'Tarea 1: panel', status: 'running' },
      { description: 'Tarea 4: fondos', status: 'running' },
    ]
    const { contextos, reloj } = await preparar(m, { agentes, reloj: true })
    await escribe(m, 'hola')
    await reloj!.advance(5000)
    agentes[0]!.status = 'completed'
    agentes[1]!.status = 'killed'
    await escribe(m, 'sigue')
    expect(contextos.at(-1)).toEqual([LANZA([4]), `Subagentes: ${RECOGE(1)}.`])
    await escribe(m, 'más')
    expect(contextos.at(-1)).toEqual([LANZA([4])])
    await m[0].classic.SessionStart({ source })
    await escribe(m, 'otra')
    expect(contextos.at(-1)).toEqual([LANZA([4]), `Subagentes: ${RECOGE(1)}.`])
  })

test('Avisos de subagentes: el resultado del Agent del principal lleva los nuevos', async (...m) => {
  const agentes: Agente[] = [{ description: 'Tarea 1: panel', status: 'running' }]
  m[1]('tool.call', { tool: 'Agent' }, () => {
    agentes[0]!.status = 'completed'
    return { result: 'informe' as never }
  })
  await preparar(m, { agentes })
  await escribe(m, 'hola')
  const r = await m[0].tool.call({ tool: 'Agent', description: 'Tarea 1: panel', prompt: 'x' } as never)
  expect((r as { context?: string[] }).context).toEqual([LANZA([4]), `Subagentes: ${RECOGE(1)}.`])
})

// El estado de la sesión en un almacén del caso, que se puede vaciar como al cambiar de plugin con /reload-plugins
// (entrar o salir del modo prueba, otra versión): el motor empieza el estado del plugin nuevo de cero.
function estadoVaciable(on: Motor[1]) {
  const valores = new Map<string, { value: unknown; version: number }>()
  const clave = (e: { plugin: string; key: string; id?: string }) => `${e.plugin}/${e.key}/${e.id ?? ''}`
  on('state.get', (_, e) => ({ value: valores.get(clave(e)) ?? { value: undefined, version: 0 } }) as never)
  on('state.set', (_, e) => {
    const w = e as { plugin: string; key: string; id?: string; value: unknown; ifVersion?: number }
    const actual = valores.get(clave(w))?.version ?? 0
    if (w.ifVersion !== undefined && w.ifVersion !== actual) return { value: { isSet: false, version: actual } } as never
    valores.set(clave(w), { value: w.value, version: actual + 1 })
    return { value: { isSet: true, version: actual + 1 } } as never
  })
  // poner: lo que deja en $.state otra versión del mod cargada entre medias (el modo prueba).
  const poner = (key: string, value: unknown) => valores.set(`sf/${key}/`, { value, version: (valores.get(`sf/${key}/`)?.version ?? 0) + 1 })
  return Object.assign(() => valores.clear(), { poner })
}

test('Avisos de subagentes: /reload-plugins que cambia de plugin y vacía el estado no hace la sesión nueva ni pide lanzar los que viven (tarea 277)', async (...m) => {
  const vaciar = estadoVaciable(m[1])
  const agentes: Agente[] = [
    { description: 'Tarea 4: fondos', status: 'running' },
    { description: 'Tarea 1: panel', status: 'running' },
  ]
  const { contextos, archivos } = await preparar(m, { agentes })
  await escribe(m, 'hola')
  expect(contextos.at(-1)).toBe(undefined)
  // La 1 entrega su informe y el motor deja de listarla; la 4 sigue trabajando.
  agentes.pop()
  await m[0].prompt.submit({ text: 'El subagente ha terminado', origin: { kind: 'task-notification' }, wait: false })
  expect(contextos.at(-1)).toEqual([`Subagentes: ${RECOGE(1)}.`])
  expect(Object.keys(JSON.parse(archivos['/sf/.sf/subagentes.json']!).sesiones)).toEqual(['sesion-1'])
  vaciar()
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  await escribe(m, 'sigo')
  expect(contextos.at(-1)).toBe(undefined)
})

test('Avisos de subagentes: con lo guardado de otra sesión, la nueva sí es nueva (tarea 277)', async (...m) => {
  const otra = { sesiones: { 'sesion-0': { fecha: AHORA - 60_000, claves: [], vistos: { x: { tarea: 1, descripcion: 'Tarea 1: panel', estado: 'esperando' } } } } }
  const { contextos } = await preparar(m, { agentes: [], extra: { '/sf/.sf/subagentes.json': JSON.stringify(otra) } })
  await escribe(m, 'hola')
  expect(contextos.at(-1)).toEqual([LANZA([1, 4], true)])
})

test('Avisos de subagentes: con automatizaciones.avisos_subagentes a false en .sf/proyecto.json, nada', async (...m) => {
  const { contextos } = await preparar(m, { agentes: [], extra: { '/sf/.sf/proyecto.json': JSON.stringify({ automatizaciones: { avisos_subagentes: false } }) } })
  await escribe(m, 'hola')
  expect(contextos.at(-1)).toBe(undefined)
})

// ── Lo que pinta la SF y lo global no son del proyecto (decisión 167) ──
const COMPOSE = { model: 'm', promptModel: 'm', surfaces: ['terminal'], tools: [], outputStyle: null, traits: [] } as const
const regla = async (m: Motor) => (await m[0].prompt.compose(COMPOSE)).sections

test('Regla de lo que es de la SF: en un proyecto, el prompt de sistema la lleva al final, una vez', async (...m) => {
  await preparar(m, { sinMarca: true, extra: { '/sf/.sf/proyecto.json': JSON.stringify({ sf: '1.1.0', proyecto: 'Demo' }) } })
  const s = await regla(m)
  expect(s.map(x => [x.id, x.scope])).toEqual([['intro', 'shared'], ['sf:lo-que-es-de-la-sf', 'session']])
  expect(s.at(-1)!.text).toMatch(/panel, caja sobre el prompt con su línea gris «SF x.y.z · fase», avisos/)
  expect(s.at(-1)!.text).toMatch(/ni en su cola ni en sus propuestas: se dice en una línea que es de la SF/)
  expect(s.at(-1)!.text).not.toMatch(/docs\/propuestas\.md/)
  expect(s.at(-1)!.text).toMatch(/~\/\.claude.*no se toca sin que el propietario lo pida y lo confirme/)
  // Cada petición la compone de nuevo: no se acumula.
  expect((await regla(m)).length).toBe(2)
})

test('Regla de lo que es de la SF: en una carpeta sin SF el prompt queda como estaba', async (...m) => {
  await preparar(m, { sinMarca: true })
  expect((await regla(m)).map(x => x.id)).toEqual(['intro'])
})

test('Regla de lo que es de la SF: en el repositorio de la SF el prompt queda como estaba', async (...m) => {
  // La SF con su propio .sf/proyecto.json: tampoco.
  await preparar(m, { extra: { '/sf/.sf/proyecto.json': JSON.stringify({ proyecto: 'SoftwareFactory' }) } })
  expect((await regla(m)).map(x => x.id)).toEqual(['intro'])
})


// ── Las reglas de la SF y la orquestación, del plugin instalado (decisión 187) ──
const PLANTILLA = '<!-- sf {{version}} · Generado por la skill. No editar a mano. -->\n\n# Software Factory\n\n- **Método:** la skill `sf:metodologia`.\n'
const ORQUESTACION = '---\nname: orquestacion\ndescription: "Reglas del agente principal"\n---\n\n# Orquestación\n\n## Con cada mensaje\n'
const PROYECTO_DEMO = (extra: Record<string, unknown> = {}) => JSON.stringify({ sf: '1.4.0', proyecto: 'Demo', ...extra })
const REGLAS_PLUGIN = { '/plugin/templates/claude-sf.md': PLANTILLA, '/plugin/skills/orquestacion/SKILL.md': ORQUESTACION }
// Las filas del aviso blanco de la cabecera, a los 5 s (con el reloj en memoria); null sin aviso.
const avisoAtraso = async (m: Motor, reloj: { advance: (ms: number) => Promise<unknown> } | null) => {
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await reloj!.advance(5000)
  const filas = async () =>
    ((await ui.findAll({ type: 'Text', text: /./ })) as { text?: string; props: Record<string, unknown> }[]).filter(t => t.props.color === '#1a1a1a').map(t => String(t.text ?? ''))
  const texto = (await filas()).join(' ')
  await ui.unmount()
  return texto || null
}
const inicio = async (m: Motor, source: 'startup' | 'resume' | 'clear' | 'compact' | 'fork', agente?: string) =>
  (await m[0].classic.SessionStart({ source, ...(agente ? { agent_id: agente, agent_type: 'general-purpose' } : {}) })).additionalContext ?? []

test('Reglas: en un proyecto, al empezar, tras /clear y tras compactar, las reglas y sf:orquestacion entera, sin cabeceras', async (...m) => {
  await preparar(m, { sinMarca: true, extra: { ...REGLAS_PLUGIN, '/sf/.sf/proyecto.json': PROYECTO_DEMO() } })
  for (const source of ['startup', 'clear', 'compact'] as const) {
    const c = await inicio(m, source)
    expect(c.length).toBe(1)
    expect(c[0]).toMatch(/^Software Factory \(plugin sf, entregado por su mod/)
    expect(c[0]).toMatch(/# Software Factory\n\n- \*\*Método:\*\*/)
    expect(c[0]).toMatch(/sf:orquestacion, ya cargada[\s\S]*sin cargarla con la herramienta Skill[\s\S]*# Orquestación\n\n## Con cada mensaje/)
    expect(c[0]).toMatch(/Carpeta de la skill, para sus referencias: .*\/skills\/orquestacion/)
    expect(c[0]).not.toMatch(/<!--|name: orquestacion|\{\{version\}\}/)
  }
  expect((await inicio(m, 'compact'))[0]).toMatch(/al compactar/)
})

test('Reglas: al reanudar o bifurcar la conversación, nada: ya las tiene', async (...m) => {
  await preparar(m, { sinMarca: true, extra: { ...REGLAS_PLUGIN, '/sf/.sf/proyecto.json': PROYECTO_DEMO() } })
  expect(await inicio(m, 'resume')).toEqual([])
  expect(await inicio(m, 'fork')).toEqual([])
})

test('Reglas: en la propia SF, nada, aunque tenga .sf/proyecto.json', async (...m) => {
  await preparar(m, { extra: { ...REGLAS_PLUGIN, '/sf/.sf/proyecto.json': JSON.stringify({ proyecto: 'SoftwareFactory' }) } })
  expect(await inicio(m, 'startup')).toEqual([])
  expect(await inicio(m, 'compact')).toEqual([])
})

test('Reglas: en una carpeta sin SF, nada', async (...m) => {
  await preparar(m, { sinMarca: true, extra: REGLAS_PLUGIN })
  expect(await inicio(m, 'startup')).toEqual([])
})

// «La orden de Python sale del intérprete que se detecta» (236): el mod prueba python, python3 y py.
test('Python: con solo python3 (macOS), el panel lanza cola.py con él y Claude recibe la orden con python3, en cualquier carpeta', async (...m) => {
  const { lineasCola, prompts } = await preparar(m, { sinMarca: true, cola: [EN_CURSO, { id: 9, texto: 'Otra', estado: 'en-cola', descripcion: 'x' }], pythons: { python3: '3 9' } })
  await m[0].command.run({ command: 'sf_paso', args: 'Uno' })
  expect(lineasCola.map(x => x[0])).toEqual(['python3'])
  for (const source of ['startup', 'clear', 'compact'] as const) {
    const c = await inicio(m, source)
    expect(c.length).toBe(1)
    expect(c[0]).toContain('Python se lanza con `python3`, no con `python`')
    expect(c[0]).toContain('`python3 -I -X utf8 "$HOME/.claude/sf/cola.py"`')
  }
  expect(await inicio(m, 'resume')).toEqual([])
  expect(await inicio(m, 'startup', 'sub-1')).toEqual([])
  // Lo que el panel pide a Claude con una orden de la cola, también con python3.
  await m[0].command.run({ command: 'sf_redescribir', args: '9' })
  await new Promise(fin => setTimeout(fin, 200))
  expect(prompts.some(t => t.includes('`python3 -I -X utf8 "$HOME/.claude/sf/cola.py" redescribir 9`'))).toBe(true)
})

test('Python: en un proyecto, la línea del intérprete va aparte de las reglas; con python, no sale', async (...m) => {
  await preparar(m, { sinMarca: true, extra: { ...REGLAS_PLUGIN, '/sf/.sf/proyecto.json': PROYECTO_DEMO() }, pythons: { python3: '3 12' } })
  const c = await inicio(m, 'startup')
  expect(c.length).toBe(2)
  expect(c[0]).toMatch(/^Software Factory \(plugin sf, entregado por su mod/)
  expect(c[1]).toContain('`python3`')
})

test('Python: el atajo de la Microsoft Store y un Python 3.8 no valen; py sí (Windows)', async (...m) => {
  const { lineasCola } = await preparar(m, { cola: [EN_CURSO], pythons: { python: null, python3: '3 8', py: '3 13' } })
  await m[0].command.run({ command: 'sf_paso', args: 'Uno' })
  expect(lineasCola.map(x => x[0])).toEqual(['py'])
  expect((await inicio(m, 'startup')).join('')).toContain('se lanza con `py`')
})

test('Python: sin ninguno, Claude recibe que falta y cómo instalarlo', async (...m) => {
  await preparar(m, { cola: [EN_CURSO], pythons: {} })
  const [c] = await inicio(m, 'startup')
  expect(c).toContain('no responde Python 3.9 o posterior (se han probado python, python3, py)')
  expect(c).toContain('xcode-select --install')
})

test('Python: en la SF con python (Windows), nada cambia: ninguna línea y la orden de siempre', async (...m) => {
  const { lineasCola } = await preparar(m, { cola: [EN_CURSO] })
  expect(await inicio(m, 'startup')).toEqual([])
  await m[0].command.run({ command: 'sf_paso', args: 'Uno' })
  expect(lineasCola.map(x => x[0])).toEqual(['python'])
})

test('Reglas: con la línea @.sf/claude-sf.md en el CLAUDE.md, solo la orquestación, y el panel avisa de que va atrasado', async (...m) => {
  const { reloj } = await preparar(m, { reloj: true,
    sinMarca: true,
    extra: { ...REGLAS_PLUGIN, '/sf/.sf/proyecto.json': PROYECTO_DEMO({ sf: '0.31' }), '/sf/CLAUDE.md': '# Demo\n\n@.sf/claude-sf.md\n' },
  })
  const c = await inicio(m, 'compact')
  expect(c.length).toBe(1)
  expect(c[0]).toMatch(/# Orquestación/)
  expect(c[0]).not.toMatch(/# Software Factory\n/)
  // Atrasado también de versión: el aviso de siempre, con el mismo remedio.
  expect(await avisoAtraso(m, reloj)).toMatch(/^⚠ incorporado con la SF 0\.31; va/)
})

test('Reglas: con la línea y el proyecto al día de versión, el aviso de atraso sale igual', async (...m) => {
  const { reloj } = await preparar(m, { reloj: true,
    sinMarca: true,
    extra: { ...REGLAS_PLUGIN, '/sf/.sf/proyecto.json': PROYECTO_DEMO({ sf: '0.32.3' }), '/sf/.claude/CLAUDE.md': '@./.sf/claude-sf.md\n' },
  })
  expect(await avisoAtraso(m, reloj)).toMatch(/^⚠ su CLAUDE\.md importa la copia vieja de las reglas/)
})

test('Reglas: sin la línea, el panel no avisa de la copia', async (...m) => {
  const { reloj } = await preparar(m, { reloj: true, sinMarca: true, extra: { ...REGLAS_PLUGIN, '/sf/.sf/proyecto.json': PROYECTO_DEMO({ sf: '0.32.3' }), '/sf/CLAUDE.md': '# Demo\nVer `.sf/claude-sf.md`\n' } })
  expect(await avisoAtraso(m, reloj)).toBe(null)
})

test('Reglas: con el interruptor automatizaciones.orquestacion apagado, solo las reglas', async (...m) => {
  await preparar(m, { sinMarca: true, extra: { ...REGLAS_PLUGIN, '/sf/.sf/proyecto.json': PROYECTO_DEMO({ automatizaciones: { orquestacion: false } }) } })
  const c = await inicio(m, 'startup')
  expect(c.length).toBe(1)
  expect(c[0]).toMatch(/# Software Factory/)
  expect(c[0]).not.toMatch(/Orquestación/)
})

test('Reglas: con la línea y el interruptor apagado, nada', async (...m) => {
  await preparar(m, {
    sinMarca: true,
    extra: { ...REGLAS_PLUGIN, '/sf/.sf/proyecto.json': PROYECTO_DEMO({ automatizaciones: { orquestacion: false } }), '/sf/CLAUDE.md': '@.sf/claude-sf.md' },
  })
  expect(await inicio(m, 'startup')).toEqual([])
})

test('Reglas: un SessionStart desde un subagente no recibe nada', async (...m) => {
  await preparar(m, { sinMarca: true, extra: { ...REGLAS_PLUGIN, '/sf/.sf/proyecto.json': PROYECTO_DEMO() } })
  expect(await inicio(m, 'startup', 'a1')).toEqual([])
})

test('Reglas: lo que añaden otros hooks de SessionStart se conserva', async (...m) => {
  await preparar(m, { sinMarca: true, contextoMotor: ['de otro'], extra: { ...REGLAS_PLUGIN, '/sf/.sf/proyecto.json': PROYECTO_DEMO() } })
  const c = await inicio(m, 'startup')
  expect(c).toEqual(['de otro', expect.stringMatching(/# Orquestación/)])
})

// ── Sin pantalla completa, los clics no llegan (tarea 264) ──
// La terminal dice en cada dibujo si está en pantalla completa; el móvil dice false, pero allí los toques llegan.
const AVISO_PANTALLA = /^⚠ Los botones necesitan la pantalla completa: pide a Claude que la active\.$/
const sinPantalla = { columns: 160, rows: 50, isFullscreen: false }
const CAJA_NORMAL = { ...CAJA, viewport: sinPantalla }
const PANEL_NORMAL = { ...PANEL, surface: 'terminal', viewport: sinPantalla, props: { ...PANEL.props, placement: 'inline' } }

test('Pantalla completa: sin ella, la caja y el panel lo dicen en texto, con el estilo de los avisos', async (...m) => {
  await preparar(m)
  const caja = await m[0].ui.mount(CAJA_NORMAL)
  expect(((await caja.find({ type: 'Text', text: AVISO_PANTALLA })) as ConProps).props.color).toBe('#1a1a1a')
  await caja.unmount()
  const panel = await m[0].ui.mount(PANEL_NORMAL)
  expect(await hay(panel, { type: 'Text', text: AVISO_PANTALLA })).toBe(true)
  expect(((await panel.findAll({ type: 'Box', text: AVISO_PANTALLA })) as ConProps[]).some(b => b.props.backgroundColor === '#ffffff')).toBe(true)
  await panel.unmount()
})

test('Pantalla completa: con ella, o en el móvil, sin aviso', async (...m) => {
  await preparar(m, { paneles: () => [panelSf(true, false)] })
  const caja = await m[0].ui.mount(CAJA)
  expect(await hay(caja, { type: 'Text', text: /\/sf abre el panel/ })).toBe(true)
  expect(await hay(caja, { type: 'Text', text: AVISO_PANTALLA })).toBe(false)
  await caja.unmount()
  for (const q of [{ ...PANEL, surface: 'terminal', viewport: { ...sinPantalla, isFullscreen: true } }, { ...PANEL_NORMAL, surface: 'mobile' }]) {
    const panel = await m[0].ui.mount(q)
    expect(await hay(panel, { type: 'Text', text: AVISO_PANTALLA })).toBe(false)
    await panel.unmount()
  }
})

const ofertaTras = async (m: Motor, q: object) => {
  const ui = await m[0].ui.mount(q)
  await ui.unmount()
}

test('Pantalla completa: sin ella, el primer mensaje del propietario lleva la oferta, una vez; tras /clear, otra vez', async (...m) => {
  const { contextos } = await preparar(m)
  await ofertaTras(m, CAJA_NORMAL)
  await escribe(m, 'hola')
  const oferta = contextos.at(-1)!.at(-1)!
  expect(oferta).toMatch(/no está en pantalla completa.*sus botones no reciben clics/)
  expect(oferta).toMatch(/hazlo solo con su OK/)
  expect(oferta).toMatch(/"tui": "fullscreen" a \.claude\/settings\.local\.json del proyecto \(nunca a ~\/\.claude sin su OK expreso\)/)
  expect(oferta).toMatch(/\/exit y claude --continue/)
  await escribe(m, 'otra cosa')
  expect(contextos.at(-1)).toBe(undefined)
  // Tras /reload-plugins, no se repite; tras /clear, que empieza otra conversación, sí.
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  await escribe(m, 'sigo')
  expect(contextos.at(-1)).toBe(undefined)
  await m[0].classic.SessionStart({ source: 'clear' })
  await escribe(m, 'de nuevo')
  expect(contextos.at(-1)?.at(-1)).toMatch(/no está en pantalla completa/)
})

test('Pantalla completa y avisos de subagentes conviven en el mismo mensaje, el de lanzar antes (tarea 351)', async (...m) => {
  const { contextos } = await preparar(m, { agentes: [] })
  await ofertaTras(m, CAJA_NORMAL)
  await escribe(m, 'hola')
  const c = contextos.at(-1)!
  expect(c.length).toBe(2)
  expect(c[0]).toBe(LANZA([1, 4], true))
  expect(c[1]).toMatch(/no está en pantalla completa/)
})

test('Pantalla completa: con ella, ningún mensaje lleva la oferta', async (...m) => {
  const { contextos } = await preparar(m, { paneles: () => [panelSf(true, false)] })
  await ofertaTras(m, CAJA)
  await escribe(m, 'hola')
  expect(contextos.at(-1)).toBe(undefined)
})

test('Pantalla completa: la oferta dice la causa que se lee (variable de entorno o ajuste ya puesto)', async (...m) => {
  const entorno: Record<string, string> = { CLAUDE_CODE_NO_FLICKER: '0' }
  const { contextos } = await preparar(m, { entorno, ajustes: { tui: 'fullscreen' } })
  await ofertaTras(m, CAJA_NORMAL)
  await escribe(m, 'hola')
  expect(contextos.at(-1)!.at(-1)).toMatch(/variable de entorno CLAUDE_CODE_NO_FLICKER=0: que la retire/)
  delete entorno.CLAUDE_CODE_NO_FLICKER
  await m[0].classic.SessionStart({ source: 'clear' })
  await escribe(m, 'otra')
  expect(contextos.at(-1)!.at(-1)).toMatch(/El ajuste «tui» ya la pide.*\/tui fullscreen/)
})

// «En observación», sin alias ni rastros (decisión 215): una cola, un historial y un plegado guardados con los nombres
// de antes se leen ya convertidos, aunque cola.py aún no haya escrito. Solo las líneas con «migración 215» los nombran.
const VIEJA_215: Pet = { id: 50, texto: 'Guardada antes', estado: 'sin-probar', probando: true, historial: [ev('a-testing', 'develop abc1234', ANTES)] } // migración 215
const SALIDA_215: Pet = { id: 51, texto: 'Salida antes', estado: 'cerrada', historial: [ev('a-testing', 'develop def5678', ANTES), ev('probada', undefined, 1)] } // migración 215

test('Migración 215: una cola vieja sale en En observación y la mirada, arriba, con sus órdenes nuevas', async (...m) => {
  await preparar(m, { cola: [VIEJA_215, { ...VIEJA_215, id: 52, texto: 'Otra antes', probando: undefined }] }) // migración 215
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Button', text: /^EN OBSERVACIÓN [▸▾] 1$/ })).toBe(true)
  // La mirada (antes con el campo viejo), arriba, como en curso; la otra, en En observación.
  expect(await hay(ui, { type: 'Button', key: 'arriba:50' })).toBe(true)
  await ui.press({ key: 'sec:observacion' })
  await ui.press({ key: 'pet:observacion:52' })
  expect(await hay(ui, { type: 'Button', key: 'cerrar-observada-tarea:observacion:52', text: /^ Cerrar $/ })).toBe(true)
  // Su commit, del evento viejo de paso a observación: la R sale.
  expect(await hay(ui, { type: 'Button', key: 'revertir-tarea:observacion:52' })).toBe(true)
  await ui.unmount()
})

test('Migración 215: una cerrada del historial viejo entra en Cerradas, y el plegado guardado pasa a la sección nueva', async (...m) => {
  const { guardado } = await preparar(m, { cola: [], salidas: [SALIDA_215], plegado: { probar: false, 'pet:probar:7': false, 'pet:cola:3': true } }) // migración 215
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(guardado.plegado).toEqual({ observacion: false, 'pet:observacion:7': false, 'pet:cola:3': true })
  expect(await hay(ui, { type: 'Button', text: /^CERRADAS [▸▾] 1$/ })).toBe(true)
  await ui.unmount()
})

// La bienvenida sin SF (tarea 289): la marca, qué es y la orden para empezar; nada de JSON, rutas, skills ni secciones.
test('Bienvenida: sin SF, la marca y qué escribir, sin JSON ni secciones', async (...m) => {
  await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Text', text: /Para empezar/ })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: / incorpora este proyecto a la SF / })).toBe(true)
  const pintado = JSON.stringify(await ui.drawn())
  for (const nada of ['proyecto.json', 'estado.json', 'sf:incorporar', '"fase"', 'PENDIENTES', 'CERRADAS', 'ninguna tarea en curso'])
    expect(pintado.includes(nada)).toBe(false)
  await ui.unmount()
})

// La pastilla de la orden es un botón que la pasa a Claude (decisión 248); en el escritorio, el logo va en SVG y la orden,
// en un solo botón centrado; en el terminal, como texto (tarea 323). En el morado de la SF.
for (const surface of ['terminal', 'desktop'] as const) {
  test(`${surface}: Bienvenida: la orden es un botón que la pasa a Claude; el logo, en SVG solo en el escritorio`, async (...m) => {
    const { prompts, reloj } = await preparar(m, { sinMarca: true, reloj: true, extra: GIT('ref: refs/heads/develop\n') })
    const ui = await m[0].ui.mount({ ...PANEL, props: { ...PANEL.props, bodyColumns: 60 }, surface })
    expect(await hay(ui, { type: 'Svg' })).toBe(surface === 'desktop')
    expect(await hay(ui, { type: 'Text', text: /▄█████/ })).toBe(surface === 'terminal')
    const clave = surface === 'desktop' ? 'incorporar' : (((await ui.findAll({ type: 'Button' })) as { key?: string }[]).find(b => b.key?.startsWith('incorporar:'))?.key ?? '')
    expect(clave.startsWith('incorporar')).toBe(true)
    expect(JSON.stringify(await ui.drawn()).includes('#827dbd')).toBe(true)
    await ui.press({ key: clave })
    await reloj!.advance(100)
    expect(prompts).toEqual(['incorpora este proyecto a la SF'])
    await ui.unmount()
  })
}

// La marca de la bienvenida, siempre en el morado de la SF, aunque la sesión tenga color (decisión 249, corregida).
test('Bienvenida: la marca va en el morado de la SF aunque la sesión tenga otro color', async (...m) => {
  await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  await m[0].command.run({ command: 'color', args: 'green' })
  const ui = await m[0].ui.mount({ ...PANEL, props: { ...PANEL.props, bodyColumns: 60 }, surface: 'desktop' })
  const pintado = JSON.stringify(await ui.drawn())
  expect(pintado.includes('#827dbd')).toBe(true)
  expect(pintado.includes('#16a34a')).toBe(false)
  await ui.unmount()
})

// El rótulo bajo el logo, «S O F T W A R E   F A C T O R Y», en el morado de la SF, como el logo (tarea 334).
for (const surface of ['terminal', 'desktop'] as const) {
  test(`${surface}: Bienvenida: el nombre bajo el logo va en el morado de la SF`, async (...m) => {
    await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
    const ui = await m[0].ui.mount({ ...PANEL, props: { ...PANEL.props, bodyColumns: 60 }, surface })
    expect(((await ui.find({ type: 'Text', text: /S O F T W A R E {3}F A C T O R Y/ })) as ConProps).props.color).toBe('#827dbd')
    await ui.unmount()
  })
}

// La caja sobre el prompt sin SF: qué es la SF, la orden como botón y qué pasa al incorporar (tarea 323).
test('Caja: sin SF, qué es la SF, la orden y qué pasa al incorporar', async (...m) => {
  await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  const ui = await m[0].ui.mount(CAJA)
  for (const t of [/^Tu fábrica de software sobre Claude Code/, /^Para empezar, pulsa o escríbelo/, /no cambia nada sin tu OK/, /\/sf abre el panel/])
    expect(await hay(ui, { type: 'Text', text: t })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'incorporar-caja' })).toBe(true)
  // El mini splash: en el terminal, el logo en texto; en el escritorio, en SVG.
  expect(await hay(ui, { type: 'Text', text: /^▄█████ ██████$/ })).toBe(true)
  await ui.unmount()
  const esc = await m[0].ui.mount({ ...CAJA, surface: 'desktop' })
  expect(await hay(esc, { type: 'Svg' })).toBe(true)
  expect(await hay(esc, { type: 'Text', text: /▄█████/ })).toBe(false)
  await esc.unmount()
})

test('Bienvenida: el logo en SVG, la barra en el morado claro y las letras en el de la SF', () => {
  const svg = logoSvg()
  expect(svg.startsWith('<svg')).toBe(true)
  expect(svg).toContain(`fill="${COLOR_BARRA}"`)
  expect(svg).toContain(`fill="${COLOR_LETRAS}"`)
  expect(logoSvg(5, false)).not.toContain(`fill="${COLOR_BARRA}"`)
})

// El logo «/SF» de la bienvenida (tarea 339): con la barra desde 18 columnas; de 13 a 17, solo las letras; por debajo, sin logo.
test('Bienvenida: el logo con barra en 18 columnas, solo las letras de 13 a 17 y ninguno por debajo', () => {
  for (const w of [18, 60]) {
    const logo = bienvenida(w).filter(x => x.estilo === 'logo')
    expect(logo.map(x => x.logo?.barra)).toEqual(BARRA)
    expect(logo.map(x => x.logo?.letras)).toEqual(LETRAS.map(f => f.trimEnd()))
    for (const x of logo) expect(x.texto).toBe(' '.repeat(x.logo!.sangria) + (x.logo!.barra + LETRAS[logo.indexOf(x)]).trimEnd())
  }
  for (const w of [13, 17]) {
    const logo = bienvenida(w).filter(x => x.estilo === 'logo')
    expect(logo.length).toBe(LETRAS.length)
    expect(logo.every(x => x.logo?.barra === '')).toBe(true)
  }
  expect(bienvenida(12).some(x => x.estilo === 'logo')).toBe(false)
})

// En el terminal, la barra y las letras de la bienvenida y del mini splash, cada una con su color.
for (const [nombre, montar] of [
  ['bienvenida', { ...PANEL, props: { ...PANEL.props, bodyColumns: 60 }, surface: 'terminal' }],
  ['caja', CAJA],
] as const) {
  test(`terminal: Logo /SF en la ${nombre}: la barra en el morado claro y las letras en el de la SF`, async (...m) => {
    await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
    const ui = await m[0].ui.mount(montar)
    expect(((await ui.find({ type: 'Text', text: /^\s*▄█▀\s*$/ })) as ConProps).props.color).toBe(COLOR_BARRA)
    expect(((await ui.find({ type: 'Text', text: /^▄█████ ██████$/ })) as ConProps).props.color).toBe(COLOR_LETRAS)
    await ui.unmount()
  })
}

test('Bienvenida: en ancho, el logo y el nombre espaciado; en estrecho, sin partir nada fuera del ancho', () => {
  const ancha = bienvenida(60)
  expect(ancha.filter(x => x.estilo === 'logo').length).toBe(LETRAS.length)
  expect(ancha.some(x => x.texto.trim() === NOMBRE_ANCHO)).toBe(true)
  for (const w of [12, 20, 28, 40, 60, 90]) for (const x of bienvenida(w)) expect(x.texto.length).toBeLessThanOrEqual(Math.max(12, w))
  const estrecha = bienvenida(12)
  expect(estrecha.some(x => x.estilo === 'logo')).toBe(false)
  expect(estrecha.filter(x => x.estilo === 'nombre').map(x => x.texto.trim())).toEqual(NOMBRE.split(' '))
  expect(bienvenida(20).filter(x => x.estilo === 'orden').length).toBeGreaterThan(1)
  expect(partir('una palabra', 5)).toEqual(['una', 'palab'])
})

// ── Tras incorporar, las reglas sin reiniciar (decisión 242); sin SF, ofrecer incorporarla (243) ──
test('Reglas: una carpeta que se incorpora en la conversación recibe las reglas con el siguiente mensaje, una vez', async (...m) => {
  const { archivos, contextos } = await preparar(m, { sinMarca: true, extra: REGLAS_PLUGIN })
  expect(await inicio(m, 'startup')).toEqual([])
  await escribe(m, 'hola')
  expect(contextos.at(-1)?.some(c => /entregado por su mod/.test(c))).toBe(false)
  archivos['/sf/.sf/proyecto.json'] = PROYECTO_DEMO()
  await escribe(m, 'ya está incorporado')
  const dado = contextos.at(-1)!.find(c => /entregado por su mod/.test(c))!
  expect(dado).toMatch(/^Software Factory \(plugin sf, entregado por su mod al incorporarse el proyecto en esta conversación\)/)
  expect(dado).toMatch(/sf:orquestacion, ya cargada/)
  await escribe(m, 'sigo')
  expect(contextos.at(-1)?.some(c => /entregado por su mod/.test(c)) ?? false).toBe(false)
  // /clear, de respaldo: las vuelve a dar en su SessionStart, sin repetirlas después.
  expect((await inicio(m, 'clear'))[0]).toMatch(/al hacer \/clear/)
  await escribe(m, 'tras clear')
  expect(contextos.at(-1)?.some(c => /entregado por su mod/.test(c)) ?? false).toBe(false)
})

test('Reglas: en un proyecto ya incorporado, el primer mensaje no las repite', async (...m) => {
  const { contextos } = await preparar(m, { sinMarca: true, extra: { ...REGLAS_PLUGIN, '/sf/.sf/proyecto.json': PROYECTO_DEMO() } })
  expect((await inicio(m, 'startup')).length).toBe(1)
  await escribe(m, 'hola')
  expect(contextos.at(-1)?.some(c => /entregado por su mod/.test(c)) ?? false).toBe(false)
})

test('Incorporar: sin SF, el primer mensaje lleva el encargo de preguntar con un menú, una vez; tras /clear, otra vez', async (...m) => {
  const { contextos } = await preparar(m, { sinMarca: true })
  await escribe(m, 'hola')
  const encargo = contextos.at(-1)!.find(c => /no está incorporada a la SF/.test(c))!
  expect(encargo).toMatch(/AskUserQuestion/)
  expect(encargo).toMatch(/«Sí, incorporarlo», «Ahora no» y «No, y no vuelvas a preguntar en esta carpeta»/)
  expect(encargo).toMatch(/escribiendo «incorpora este proyecto a la SF»/)
  expect(encargo).toMatch(/sf:incorporar_proyecto_a_sf/)
  await escribe(m, 'otra')
  expect(contextos.at(-1)).toBe(undefined)
  await m[0].classic.SessionStart({ source: 'clear' })
  await escribe(m, 'de nuevo')
  expect(contextos.at(-1)?.some(c => /no está incorporada a la SF/.test(c))).toBe(true)
})

test('Incorporar: en un proyecto con SF o en la propia SF, nada', async (...m) => {
  const { contextos } = await preparar(m)
  await escribe(m, 'hola')
  expect(contextos.at(-1)?.some(c => /no está incorporada a la SF/.test(c)) ?? false).toBe(false)
})

test('Pantalla completa: sin SF no se ofrece; tras incorporar, con el siguiente mensaje, junto a las reglas', async (...m) => {
  const { archivos, contextos } = await preparar(m, { sinMarca: true, extra: REGLAS_PLUGIN })
  await inicio(m, 'startup')
  await ofertaTras(m, CAJA_NORMAL)
  await escribe(m, 'hola')
  expect(contextos.at(-1)?.some(c => /no está en pantalla completa/.test(c))).toBe(false)
  archivos['/sf/.sf/proyecto.json'] = PROYECTO_DEMO()
  await escribe(m, 'incorporado')
  const c = contextos.at(-1)!
  expect(c.some(x => /entregado por su mod al incorporarse/.test(x))).toBe(true)
  expect(c.some(x => /no está en pantalla completa/.test(x))).toBe(true)
})

// Decisión 246: «No, y no vuelvas a preguntar en esta carpeta» se recuerda por carpeta; «Ahora no», solo en la conversación.
const respondeMenu = (m: Motor, respuesta: string) => {
  m[1]('tool.call', { tool: 'AskUserQuestion' }, (_, e) => {
    const q = (e as unknown as { questions: { question: string }[] }).questions[0]!.question
    return { result: { questions: (e as unknown as { questions: unknown[] }).questions, answers: { [q]: respuesta } } as never }
  })
}
const preguntaIncorporar = (m: Motor) =>
  m[0].tool.call({ tool: 'AskUserQuestion', questions: [{ question: '¿Incorporar este proyecto a la SF?', header: 'SF', multiSelect: false, options: [{ label: 'Sí, incorporarlo', description: '' }, { label: 'Ahora no', description: '' }, { label: 'No, y no vuelvas a preguntar en esta carpeta', description: '' }] }] } as never)

test('Incorporar: con «No, y no vuelvas a preguntar en esta carpeta», no se pregunta más en ella, ni tras /clear', async (...m) => {
  respondeMenu(m, 'No, y no vuelvas a preguntar en esta carpeta')
  const { contextos, guardado } = await preparar(m, { sinMarca: true })
  await escribe(m, 'hola')
  expect(contextos.at(-1)?.some(c => /no está incorporada a la SF/.test(c))).toBe(true)
  await preguntaIncorporar(m)
  expect(guardado.noIncorporar).toEqual({ '/sf': true })
  await m[0].classic.SessionStart({ source: 'clear' })
  await escribe(m, 'de nuevo')
  expect(contextos.at(-1)?.some(c => /no está incorporada a la SF/.test(c)) ?? false).toBe(false)
})

test('Incorporar: con «Ahora no», nada guardado: tras /clear se vuelve a preguntar', async (...m) => {
  respondeMenu(m, 'Ahora no')
  const { contextos, guardado } = await preparar(m, { sinMarca: true })
  await escribe(m, 'hola')
  await preguntaIncorporar(m)
  expect(guardado.noIncorporar).toBe(undefined)
  await m[0].classic.SessionStart({ source: 'clear' })
  await escribe(m, 'de nuevo')
  expect(contextos.at(-1)?.some(c => /no está incorporada a la SF/.test(c))).toBe(true)
})

// En la app de escritorio (fuente proporcional y botones nativos), sin anchos fijos en columnas en la cabecera ni en
// el número, y el título plegado se corta con puntos suspensivos; desplegado, se parte. El terminal, como estaba (tarea 323).
for (const surface of ['terminal', 'desktop'] as const) {
  test(`${surface}: cabecera y números sin ancho fijo en el escritorio; títulos cortados al plegar y partidos al desplegar`, async (...m) => {
    type Caja = { props: Record<string, unknown> }
    await preparar(m, { cola: [...INICIAL, { id: 236, texto: 'Un título de tarea muy largo que no cabe en el panel lateral estrecho', estado: 'en-cola', descripcion: 'detalle' }] })
    const ui = await m[0].ui.mount({ ...PANEL, surface })
    const conFondo = ((await ui.findAll({ type: 'Box' })) as Caja[]).filter(x => x.props.backgroundColor === '#3f3f46')
    expect(conFondo.length > 0).toBe(true)
    expect(conFondo.every(x => (surface === 'desktop' ? x.props.width === undefined : typeof x.props.width === 'number'))).toBe(true)
    const envolturas = async () =>
      ((await ui.findAll({ type: 'Text', text: /Un título de tarea muy largo/ })) as Caja[]).map(x => x.props.wrap).filter(w => w !== undefined)
    expect(await envolturas()).toEqual(surface === 'desktop' ? ['truncate-end'] : [])
    await ui.press({ key: 'pet:cola:236' })
    expect(await envolturas()).toEqual(surface === 'desktop' ? ['wrap'] : [])
    await ui.unmount()
  })
}

// Sin SF, la línea del prompt sugiere la orden de incorporar (tarea 323): al empezar, no en la SF ni en un proyecto
// incorporado, ni donde se dijo «no vuelvas a preguntar» (decisión 246).
const sugerencias = (on: Motor[1]) => {
  const vistas: string[] = []
  on('prompt.suggest', (_, e) => {
    vistas.push(e.text)
    return { isShown: true }
  })
  return vistas
}
test('Sugerencia: sin SF, el prompt sugiere «incorpora este proyecto a la SF» al empezar', async (...m) => {
  const vistas = sugerencias(m[1])
  const { reloj } = await preparar(m, { sinMarca: true, reloj: true })
  await reloj!.advance(600)
  expect(vistas).toEqual(['incorpora este proyecto a la SF'])
})
test('Sugerencia: en la SF, nada', async (...m) => {
  const vistas = sugerencias(m[1])
  const { reloj } = await preparar(m, { reloj: true })
  await reloj!.advance(600)
  expect(vistas).toEqual([])
})
test('Sugerencia: donde se dijo que no se vuelva a preguntar, nada', async (...m) => {
  const vistas = sugerencias(m[1])
  const { guardado, reloj } = await preparar(m, { sinMarca: true, reloj: true, sinArranque: true })
  guardado.noIncorporar = { '/sf': true }
  await m[0].session.start({ cwd: RAIZ, surface: 'terminal', isInteractive: true })
  await reloj!.advance(600)
  expect(vistas).toEqual([])
})
test('Sugerencia: tras /sf vuelve; tras un turno de Claude, no', async (...m) => {
  const vistas = sugerencias(m[1])
  const { reloj } = await preparar(m, { sinMarca: true, reloj: true })
  await reloj!.advance(600)
  await m[0].command.run({ command: 'sf' })
  await reloj!.advance(600)
  expect(vistas).toEqual(['incorpora este proyecto a la SF', 'incorpora este proyecto a la SF'])
  await escribe(m, 'hola')
  await reloj!.advance(600)
  expect(vistas.length).toBe(2)
})

// ── La incorporación, paso a paso (tarea 333) ──
// El progreso que anota Claude con tools/incorporacion.py, en la carpeta de la SF de Claude Code, por sesión.
// Por proyecto, no por sesión: la clave de la carpeta /sf (tarea 333).
const PROGRESO = '/home/.claude/sf/incorporacion-_sf.json'
const progreso = (actual: number, respuestas: (string | null)[], carpeta = RAIZ) =>
  JSON.stringify({
    version: 1,
    carpeta,
    caso: 'existente',
    actual,
    pasos: ['Caso', 'Diagnóstico', 'Identidad', 'Repositorio', 'Convenciones', 'Cambios y OK', 'Aplicar', 'CLAUDE.md', 'Pasar a sf/', 'Comprobación'].map((nombre, i) => ({ nombre, respuesta: respuestas[i] ?? null })),
  })

test('Incorporación: sin SF, bajo la bienvenida sin su invitación, todos los pasos si caben y el actual en morado', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  archivos[PROGRESO] = progreso(3, ['Existente', 'falta .sf/ y develop'])
  await cambiarCola(INICIAL)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // La marca y el lema se quedan; la invitación a empezar, no: compite con la lista (tarea 333).
  expect(await hay(ui, { type: 'Text', text: /Tu fábrica de software/ })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: /Para empezar/ })).toBe(false)
  expect(await hay(ui, { type: 'Text', text: /unas pocas preguntas/ })).toBe(false)
  expect(await hay(ui, { type: 'Text', text: 'paso 3 de 10' })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: ' En curso ', backgroundColor: '#827dbd', color: '#000000' })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: 'falta .sf/ y develop' })).toBe(true)
  // El actual, en el morado de la marca y negrita, no en amarillo.
  expect(await hay(ui, { type: 'Text', text: 'Identidad ◂', color: '#827dbd', weight: 'bold' })).toBe(true)
  // Caben los diez: ni plegados ni flechas.
  for (const t of ['Caso', 'Aplicar', 'CLAUDE.md', 'Comprobación']) expect(await hay(ui, { type: 'Text', text: t })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'incorporacion:arriba' })).toBe(false)
  expect(await hay(ui, { type: 'Button', key: 'incorporacion:abajo' })).toBe(false)
  await ui.unmount()
})

test('Incorporación: si no caben, pliega solo los que sobran, con el actual a la vista; ▲ y ▼ mueven la ventana', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  archivos[PROGRESO] = progreso(3, ['Existente', 'falta .sf/ y develop'])
  await cambiarCola(INICIAL)
  const bajo = (filas: number) => ({ ...PANEL, surface: 'terminal', props: { ...PANEL.props, scroll: { offset: 0, bodyRows: filas } } })
  const visibles = async (ui: { find: (q: object) => Promise<unknown> }) => {
    let n = 0
    for (const t of ['Caso', 'Diagnóstico', 'Identidad ◂', 'Repositorio', 'Convenciones', 'Cambios y OK', 'Aplicar', 'CLAUDE.md', 'Pasar a sf/', 'Comprobación'])
      if (await hay(ui, { type: 'Text', text: t })) n++
    return n
  }
  const corto = await m[0].ui.mount(bajo(28))
  const n28 = await visibles(corto)
  expect(n28 > 1 && n28 < 10).toBe(true)
  expect(await hay(corto, { type: 'Text', text: 'Identidad ◂' })).toBe(true)
  expect(await hay(corto, { type: 'Button', key: 'incorporacion:abajo' })).toBe(true)
  // ▼ baja la ventana hasta el final; ▲, la sube hasta el principio.
  for (let k = 0; k < 10 && (await hay(corto, { type: 'Button', key: 'incorporacion:abajo' })); k++) await corto.press({ key: 'incorporacion:abajo' })
  expect(await hay(corto, { type: 'Text', text: 'Comprobación' })).toBe(true)
  for (let k = 0; k < 10 && (await hay(corto, { type: 'Button', key: 'incorporacion:arriba' })); k++) await corto.press({ key: 'incorporacion:arriba' })
  expect(await hay(corto, { type: 'Text', text: 'Caso' })).toBe(true)
  await corto.unmount()
  // Con una fila más de alto, uno más a la vista (o todos): pliega lo mínimo.
  const algo = await m[0].ui.mount(bajo(29))
  expect((await visibles(algo)) >= n28).toBe(true)
  await algo.unmount()
})

test('Incorporación: la ventana vuelve a seguir al paso actual cuando Claude pasa de paso', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  archivos[PROGRESO] = progreso(1, [])
  await cambiarCola(INICIAL)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal', props: { ...PANEL.props, scroll: { offset: 0, bodyRows: 28 } } })
  await ui.press({ key: 'incorporacion:abajo' })
  expect(await hay(ui, { type: 'Text', text: 'Caso ◂' })).toBe(false)
  archivos[PROGRESO] = progreso(9, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
  await cambiarCola(INICIAL)
  expect(await hay(ui, { type: 'Text', text: 'Pasar a sf/ ◂' })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: 'Comprobación' })).toBe(true)
  await ui.unmount()
})

test('Incorporación terminada: con panel operativo se queda hasta el turno siguiente; sin él, con «Hecho», que la cierra', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  const todos = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
  // Sin SF (simulada, o un diagnóstico): terminada, sigue, sin Continuar ni Abandonar y con «Hecho»; el turno no la quita.
  archivos[PROGRESO] = progreso(0, todos)
  await cambiarCola(INICIAL)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Text', text: ' Terminada ' })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'incorporacion:continuar' })).toBe(false)
  expect(await hay(ui, { type: 'Button', key: 'incorporacion:abandonar' })).toBe(false)
  expect(await hay(ui, { type: 'Button', key: 'incorporacion:cerrar' })).toBe(true)
  await acabaTurno(m, 't1')
  await m[0].turn.start({ text: 'sigue', turnId: 't2' })
  expect(sinPasos(archivos)).toBe(false)
  // Con el panel operativo (ya hay .sf/proyecto.json): la lista, con Aplicar y Comprobación marcados, se queda.
  archivos['/sf/.sf/proyecto.json'] = JSON.stringify({ proyecto: 'Demo', color: 'blue' })
  await cambiarCola(INICIAL)
  expect(await hay(ui, { type: 'Text', text: '10 de 10 pasos' })).toBe(true)
  expect(await hay(ui, { type: 'Button', key: 'incorporacion:cerrar' })).toBe(false)
  await acabaTurno(m, 't2')
  expect(sinPasos(archivos)).toBe(false)
  // Y al empezar el turno siguiente, el mod la quita.
  await m[0].turn.start({ text: 'gracias', turnId: 't3' })
  expect(sinPasos(archivos)).toBe(true)
  expect(await hay(ui, { type: 'Text', text: 'INCORPORACIÓN' })).toBe(false)
  await ui.unmount()
})

test('Incorporación terminada sin SF: «Hecho» quita la lista y vuelve la invitación de la bienvenida', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  archivos[PROGRESO] = progreso(0, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
  await cambiarCola(INICIAL)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Text', text: /Para empezar/ })).toBe(false)
  await ui.press({ key: 'incorporacion:cerrar' })
  expect(sinPasos(archivos)).toBe(true)
  expect(await hay(ui, { type: 'Text', text: 'INCORPORACIÓN' })).toBe(false)
  expect(await hay(ui, { type: 'Text', text: /Para empezar/ })).toBe(true)
  await ui.unmount()
})

test('Incorporación: con SF (al actualizar), arriba del cuerpo; de otra carpeta, no sale; borrado, se va', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { sinMarca: true, extra: { '/sf/.sf/proyecto.json': JSON.stringify({ proyecto: 'Demo', color: 'blue' }) } })
  archivos[PROGRESO] = progreso(2, ['Actualizar'])
  await cambiarCola(INICIAL)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  expect(await hay(ui, { type: 'Text', text: 'paso 2 de 10' })).toBe(true)
  archivos[PROGRESO] = progreso(2, ['Actualizar'], '/otra')
  await cambiarCola(INICIAL)
  expect(await hay(ui, { type: 'Text', text: 'INCORPORACIÓN' })).toBe(false)
  archivos[PROGRESO] = progreso(0, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
  await cambiarCola(INICIAL)
  expect(await hay(ui, { type: 'Text', text: '10 de 10 pasos' })).toBe(true)
  delete archivos[PROGRESO]
  await cambiarCola(INICIAL)
  expect(await hay(ui, { type: 'Text', text: 'INCORPORACIÓN' })).toBe(false)
  await ui.unmount()
})

// En pausa (decisión 258): un turno que acaba, o se interrumpe, con la incorporación a medias la pone en pausa sin
// borrar lo respondido; el panel ofrece Continuar (a Claude) y Abandonar (sin Claude). Se borra con un no a incorporar
// y al cargar el mod.
const sinPasos = (archivos: Record<string, string>) => !archivos[PROGRESO] || !JSON.parse(archivos[PROGRESO]!).pasos
const enPausa = (archivos: Record<string, string>) => JSON.parse(archivos[PROGRESO]!).pausa === true
const acabaTurno = (m: Motor, turnId: string, isAborted = false) =>
  m[0].turn.complete({ turnId, answer: '', durationMs: 1, isAborted, reason: isAborted ? 'aborted' : 'answer' } as never)

test('Incorporación: al acabar o interrumpirse el turno a medias, en pausa con lo respondido; terminada, no', async (...m) => {
  const { archivos } = await preparar(m, { sinMarca: true })
  archivos[PROGRESO] = progreso(3, ['Existente', 'falta .sf/'])
  await acabaTurno(m, 't1', true)
  expect(enPausa(archivos)).toBe(true)
  expect(JSON.parse(archivos[PROGRESO]!).pasos[1].respuesta).toBe('falta .sf/')
  archivos[PROGRESO] = progreso(0, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
  await acabaTurno(m, 't2')
  expect(enPausa(archivos)).toBe(false)
})

test('Incorporación en pausa: lista atenuada con Continuar, que lo pasa a Claude, y Abandonar, que la borra', async (...m) => {
  const { archivos, cambiarCola, prompts, reloj } = await preparar(m, { sinMarca: true, reloj: true, extra: GIT('ref: refs/heads/develop\n') })
  archivos[PROGRESO] = progreso(3, ['Existente', 'falta .sf/'])
  await acabaTurno(m, 't1', true)
  await cambiarCola(INICIAL)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  // La cabecera (tarea 333): el nombre en el morado de la marca, el estado como etiqueta en morado claro y la cuenta, atenuada.
  expect(await hay(ui, { type: 'Text', text: 'INCORPORACIÓN', color: '#827dbd', weight: 'bold' })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: ' En pausa ', backgroundColor: '#b3aee6', color: '#000000' })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: 'paso 3 de 10', dimColor: true })).toBe(true)
  expect(await hay(ui, { type: 'Text', text: 'Identidad ◂' })).toBe(false)
  // Continuar, como la orden de la bienvenida (morado de la marca, letra negra en negrita); Abandonar, en el morado
  // claro sin fondo; ninguno en amarillo ni en rojo, centrados con espacios en el terminal (tarea 333).
  expect(await etiqueta(ui, 'incorporacion:continuar')).toMatchObject({ backgroundColor: '#827dbd', color: '#000000', weight: 'bold' })
  const abandonar = (await etiqueta(ui, 'incorporacion:abandonar')) as Record<string, unknown>
  expect(abandonar).toMatchObject({ color: '#b3aee6' })
  expect(abandonar.backgroundColor).toBe(undefined)
  const fila = (await ui.find({ type: 'Box', key: 'incorporacion:continuar:fila' })) as { children: { type: string; children: unknown[] }[] }
  expect(fila.children[0]).toMatchObject({ type: 'Text', children: [expect.stringMatching(/^ +$/)] })
  await ui.press({ key: 'incorporacion:continuar' })
  await reloj!.advance(100)
  expect(prompts).toEqual(['continúa la incorporación a la SF'])
  await ui.press({ key: 'incorporacion:abandonar' })
  await reloj!.advance(100)
  expect(sinPasos(archivos)).toBe(true)
  expect(await hay(ui, { type: 'Text', text: 'INCORPORACIÓN' })).toBe(false)
  expect(await hay(ui, { type: 'Text', text: /Para empezar/ })).toBe(true)
  await ui.unmount()
})

test('Incorporación en pausa tras Esc: si Claude Code no admite el encargo de Continuar, se deja escrito en el prompt y se dice', async (...m) => {
  // Tras interrumpir con Esc, el motor no deja que un plugin pase mensajes hasta que el propietario escribe: { drop }.
  m[1]('prompt.submit', { origin: { kind: 'plugin' } } as never, () => ({ drop: 'interrumpido' }))
  const { archivos, cambiarCola, rellenos, toasts, reloj } = await preparar(m, { sinMarca: true, reloj: true, extra: GIT('ref: refs/heads/develop\n') })
  archivos[PROGRESO] = progreso(3, ['Existente', 'falta .sf/'])
  await acabaTurno(m, 't1', true)
  await cambiarCola(INICIAL)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'terminal' })
  await ui.press({ key: 'incorporacion:continuar' })
  await reloj!.advance(100)
  expect(rellenos).toEqual(['continúa la incorporación a la SF'])
  expect(toasts.some(t => t.includes('pulsa Intro'))).toBe(true)
  await ui.unmount()
})

test('Incorporación en pausa: en una superficie gráfica, los dos botones centrados con la caja', async (...m) => {
  const { archivos, cambiarCola } = await preparar(m, { sinMarca: true, extra: GIT('ref: refs/heads/develop\n') })
  archivos[PROGRESO] = progreso(3, ['Existente', 'falta .sf/'])
  await acabaTurno(m, 't1', true)
  await cambiarCola(INICIAL)
  const ui = await m[0].ui.mount({ ...PANEL, surface: 'desktop' })
  for (const k of ['continuar', 'abandonar'])
    expect(await hay(ui, { type: 'Box', key: `incorporacion:${k}:fila`, justifyContent: 'center' })).toBe(true)
  expect(await etiqueta(ui, 'incorporacion:continuar')).toMatchObject({ backgroundColor: '#827dbd', color: '#000000', weight: 'bold' })
  await ui.unmount()
})

test('Incorporación: un no a incorporar en un menú la borra; otra respuesta, no', async (...m) => {
  const respuestas = ['Demo', 'Ahora no']
  m[1]('tool.call', { tool: 'AskUserQuestion' }, (_, e) => {
    const q = (e as unknown as { questions: { question: string }[] }).questions[0]!.question
    return { result: { questions: (e as unknown as { questions: unknown[] }).questions, answers: { [q]: respuestas.shift()! } } as never }
  })
  const { archivos } = await preparar(m, { sinMarca: true })
  archivos[PROGRESO] = progreso(3, ['Existente'])
  const pregunta = () => m[0].tool.call({ tool: 'AskUserQuestion', questions: [{ question: '¿Y ahora?', header: 'SF', multiSelect: false, options: [{ label: 'Demo', description: '' }] }] } as never)
  await pregunta()
  expect(sinPasos(archivos)).toBe(false)
  await pregunta()
  expect(sinPasos(archivos)).toBe(true)
})

test('Incorporación: un progreso a medias de antes de cargar el mod (/reload-plugins, modo prueba, sesión nueva) queda en pausa, no se borra', async (...m) => {
  const { archivos } = await preparar(m, { sinMarca: true, extra: { [PROGRESO]: progreso(3, ['Existente']) } })
  expect(sinPasos(archivos)).toBe(false)
  expect(enPausa(archivos)).toBe(true)
  expect(JSON.parse(archivos[PROGRESO]!).pasos[0].respuesta).toBe('Existente')
})

test('Incorporación: una terminada de antes de cargar el mod se conserva, sin pausa', async (...m) => {
  const { archivos } = await preparar(m, { sinMarca: true, extra: { [PROGRESO]: progreso(0, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']) } })
  expect(sinPasos(archivos)).toBe(false)
  expect(enPausa(archivos)).toBe(false)
})

test('Incorporación: la clave del archivo de progreso es la de incorporacion.py (por proyecto)', () => {
  expect(claveIncorporacion('C:\\Proyectos\\Ejemplo/')).toBe('c__proyectos_ejemplo')
  expect(claveIncorporacion('/sf')).toBe('_sf')
  expect(claveIncorporacion('/srv/Año')).toBe('_srv_a_o')
})
