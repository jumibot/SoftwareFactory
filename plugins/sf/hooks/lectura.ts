import { atom, read, update, type EngineInterface } from 'claude-code'
import type { SubagenteVisto, Estado, Incorporacion, Evento, Paso, Peticion, Realimentacion, Salida } from '../types'
import { ANTIGUO, CAMPO_VIEJO, CARPETA_COPIAS, PREFIJO_INCORPORACION, COLORES, COLOR_SF, ESTADO, ESTADOS_PETICION, ESTADOS_VIEJOS, EVENTO_CERRADA_VIEJO, EVENTOS_VIEJOS, FASES, HISTORIAL, MARCA_SF, PETICIONES, PROYECTO } from './constantes'
import { avisosConfiguracion, leerConfiguracion, remotos, TRAILER_TAREA } from './configuracion'
import { igual, normal } from './control'
import { guardarSesion } from './memoria'

export type $ = EngineInterface

export function nombreCarpeta(ruta: string): string {
  const partes = ruta.split(/[\\/]/).filter(Boolean)
  return partes[partes.length - 1] ?? ruta
}

export function texto(v: unknown): string | null {
  return typeof v === 'string' && v.trim() !== '' ? v.trim() : null
}

export async function leerJson($: $, ruta: string): Promise<Record<string, unknown>> {
  return JSON.parse(await $.fs.read(ruta)) as Record<string, unknown>
}

// Lee la cola; un archivo ausente es una cola vacía.
// La carpeta del usuario.
export async function carpetaUsuario($: $): Promise<string | null> {
  const home = (await $.env.get('USERPROFILE')) ?? (await $.env.get('HOME'))
  return home ? normal(home) : null
}

// La carpeta de Claude Code, donde viven las copias de cola.py: la de CLAUDE_CONFIG_DIR si está
// puesta, si no ~/.claude. Así una configuración desechable no toca la SF del ~/.claude real (tarea 269).
export async function carpetaClaude($: $): Promise<string | null> {
  const config = await $.env.get('CLAUDE_CONFIG_DIR')
  if (config) return normal(config)
  const home = await carpetaUsuario($)
  return home ? `${home}/.claude` : null
}

// Último cambio de una tarea: la fecha más reciente de su historial (ISO con zona, de tools/cola.py), en ms.
// null si no tiene historial o ninguna fecha se entiende.
export function ultimoCambio(historial: unknown): number | null {
  if (!Array.isArray(historial)) return null
  let max: number | null = null
  for (const e of historial) {
    const f = Date.parse(texto((e as Record<string, unknown> | null)?.fecha) ?? '')
    if (!Number.isNaN(f) && (max === null || f > max)) max = f
  }
  return max
}

export async function leerPeticiones($: $, raiz: string): Promise<{ peticiones: Peticion[]; error: string | null }> {
  const ruta = `${raiz}/${PETICIONES}`
  if (!(await $.fs.exists(ruta))) return { peticiones: [], error: null }
  try {
    const datos = await leerJson($, ruta)
    const lista = Array.isArray(datos.peticiones) ? (datos.peticiones as unknown[]) : []
    const peticiones: Peticion[] = []
    let rechazadas = 0
    lista.forEach((v, i) => {
      const p = (v ?? {}) as Record<string, unknown>
      // Una cola de antes de «En observación» se lee ya convertida, como la deja cola.py al cargarla (decisión 215).
      const est = ESTADOS_PETICION.find(x => x === (ESTADOS_VIEJOS[String(p.estado)] ?? p.estado))
      const txt = texto(p.texto)
      if (!est || !txt) { rechazadas++; return }
      peticiones.push({
        id: typeof p.id === 'number' ? p.id : i + 1,
        texto: txt,
        estado: est,
        prueba: texto(p.prueba),
        descripcion: texto(p.descripcion),
        tipo: texto(p.tipo),
        observando: p.observando === true || p[CAMPO_VIEJO] === true,
        pasos: conComprobado(leerPasos(p.pasos), texto(p.comprobado)),
        reabierta: p.reabierta === true,
        commit: texto(p.commit),
        rama: texto(p.rama),
        historial: leerEventos(p.historial),
        cambio: ultimoCambio(p.historial),
      })
    })
    return {
      peticiones,
      error: rechazadas ? `${rechazadas} petición(es) sin texto o con estado distinto de ${ESTADOS_PETICION.join(', ')}` : null,
    }
  } catch (err) {
    return { peticiones: [], error: `no se puede leer ${PETICIONES}: ${String(err)}` }
  }
}

// ── Historial (decisión 115, tarea 145) ──
// Cada tarea lleva su historial, que escribe cola.py: el panel lee de ahí lo que ha pasado en la sesión, sin deducirlo
// comparando lecturas de la cola. Los eventos que no se entienden se ignoran; la fecha, en ms (null si no se entiende).
export function leerEventos(v: unknown): Evento[] {
  if (!Array.isArray(v)) return []
  return v.flatMap(x => {
    const o = (x ?? {}) as Record<string, unknown>
    const leido = texto(o.evento)
    if (!leido) return []
    // Los eventos de antes de «En observación», ya convertidos, como cola.py al cargarlos (decisión 215).
    const evento = EVENTOS_VIEJOS[leido] ?? leido
    const detalle = texto(o.detalle) ?? (leido === EVENTO_CERRADA_VIEJO ? 'en observación' : null)
    const f = typeof o.fecha === 'string' ? Date.parse(o.fecha) : Number.NaN
    const via = texto(o.via)
    return [{ evento, fecha: Number.isNaN(f) ? null : f, detalle, ...(via ? { via } : {}) }]
  })
}

// Los eventos que ponen una tarea en Cerradas: su cierre, su paso a observación, su descarte, su reversión y su
// reapertura. Eliminar y fusionar la sacan sin cerrarla; limpiar quita una descartada que ya estaba en Cerradas.
export const CIERRES = ['a-observacion', 'cerrada', 'descartada', 'revertida', 'reabierta']

// Cuándo entró en la cola: creada o, por /sf_split, nacida; null sin historial (anterior a cola.py).
export function creadaEn(h: Evento[]): number | null {
  return h.find(e => e.evento === 'creada' || e.evento === 'nacida')?.fecha ?? null
}

// El último evento de cierre desde `desde` (ms), o null.
export function ultimoCierre(h: Evento[], desde: number): Evento | null {
  for (let i = h.length - 1; i >= 0; i--) {
    const e = h[i]!
    if (e.fecha !== null && e.fecha < desde) return null
    if (CIERRES.includes(e.evento)) return e
  }
  return null
}

// Los commits de la tarea en develop, del historial: el squash de su cierre o de su paso a observación («develop <hash>»),
// sin los ya revertidos; el más reciente primero. Como hashes_de de cola.py.
export function commitsDe(h: Evento[]): string[] {
  const hechos: string[] = []
  const revertidos = new Set<string>()
  for (const e of h) {
    const m = /^develop ([0-9a-f]{4,40})/.exec(e.detalle ?? '')
    if ((e.evento === 'cerrada' || e.evento === 'a-observacion') && m) hechos.push(m[1]!)
    if (e.evento === 'revertida') for (const x of (e.detalle ?? '').split('revierte')[1]?.match(/[0-9a-f]{7,40}/g) ?? []) revertidos.add(x)
  }
  return hechos.reverse().filter(x => !revertidos.has(x))
}

// El commit de su último cierre con squash, si después anotó push-fallido; null si no.
function pushFallido(h: Evento[]): string | null {
  let hash: string | null = null
  for (const e of h) {
    if (e.evento === 'cerrada' || e.evento === 'a-observacion') hash = /^develop ([0-9a-f]{4,40})/.exec(e.detalle ?? '')?.[1] ?? null
    else if (e.evento === 'push-fallido') return hash
  }
  return null
}

// Las tareas que han salido de la cola con algún cambio desde `desde` (ms): la última línea de cada número de
// .sf/historial.jsonl. Las líneas que no se entienden se ignoran.
export async function leerSalidas($: $, raiz: string, desde: number): Promise<Salida[]> {
  const ruta = `${raiz}/${HISTORIAL}`
  if (!(await $.fs.exists(ruta))) return []
  const ultimas = new Map<number, Record<string, unknown>>()
  for (const linea of (await $.fs.read(ruta)).split('\n')) {
    if (!linea.trim()) continue
    try {
      const t = JSON.parse(linea) as Record<string, unknown>
      if (typeof t.id === 'number') ultimas.set(t.id, t)
    } catch {
      // Una línea rota no impide leer las demás.
    }
  }
  const salidas: Salida[] = []
  for (const [id, t] of ultimas) {
    const historial = leerEventos(t.historial)
    if (!historial.some(e => e.fecha !== null && e.fecha >= desde)) continue
    salidas.push({ id, texto: texto(t.texto) ?? '', estado: texto(t.estado) ?? '', commit: texto(t.commit), historial, tipo: texto(t.tipo) })
  }
  return salidas
}

// Las tareas con el push de develop pendiente: su último cierre anotó push-fallido y <remoto>/develop aún no tiene
// su commit (el remoto de la configuración, origin si no dice otro). Solo ejecuta git si hay alguna.
async function leerPushPendiente($: $, raiz: string, tareas: { id: number; historial: Evento[] }[], remoto = 'origin'): Promise<number[]> {
  const pendientes: number[] = []
  for (const t of tareas) {
    const hash = pushFallido(t.historial)
    if (hash === null) continue
    const r = await $.process.run(['git', 'merge-base', '--is-ancestor', hash, `${remoto}/develop`], { cwd: raiz }).catch(() => null)
    if (r?.exitCode !== 0) pendientes.push(t.id)
  }
  return pendientes
}

// Resumen de una propuesta para el panel: la primera frase de su «Cambio propuesto» (o «Propuesta original»);
// si el apartado empieza por una lista, su primer punto; sin ninguno, el primer apartado con texto que no sea
// Origen, Tipo ni Estado. Un apartado que empieza por un bloque de código no sirve de resumen.
export function resumenPropuesta(b: string): string {
  const lineas = b.split('\n')
  const apartado = (i: number) => {
    const resto = lineas[i].replace(/^- \*\*[^*]+:\*\*/, '').trim()
    if (resto && !resto.endsWith(':')) return resto
    // Lo que sigue al apartado, sangrado: su primer punto de lista o su primer párrafo.
    const sig = lineas.slice(i + 1).find(l => /^\s+\S/.test(l)) ?? ''
    if (/^\s+```/.test(sig)) return resto
    return [resto, sig.replace(/^\s+((\d+\.|-)\s)?/, '').trim()].filter(Boolean).join(' ')
  }
  const indices = (re: RegExp) => lineas.flatMap((l, i) => (re.test(l) ? [i] : []))
  const candidatos = [
    ...indices(/^- \*\*Cambio propuesto:\*\*/),
    ...indices(/^- \*\*Propuesta original:\*\*/),
    ...indices(/^- \*\*(?!Origen|Tipo|Estado|Cambio propuesto|Propuesta original)[^*]+:\*\*/),
  ]
  let texto = ''
  for (const i of candidatos) if ((texto = apartado(i))) break
  const limpio = texto.replace(/\*\*|`|\*/g, '').replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
  const frase = /^.+?\.(\s|$)/.exec(limpio)?.[0].trim() ?? limpio
  return frase.length > 220 ? frase.slice(0, 219).trimEnd() + '…' : frase
}

// Los tipos de tarea de cola.py: el «Tipo» de una propuesta solo vale si es uno de ellos.
const TIPOS_TAREA = ['deliberar', 'documentar', 'diseñar', 'implementar', 'especificar', 'corregir', 'investigar']
export function tipoPropuesta(b: string): string | null {
  const t = (/^- \*\*Tipo:\*\*(.*)$/m.exec(b)?.[1] ?? '').trim().replace(/\.$/, '').toLowerCase()
  return TIPOS_TAREA.includes(t) ? t : null
}

// Propuestas: cuenta las abiertas de sf/propuestas.md, o de docs/propuestas.md mientras el proyecto no se ha puesto
// al día (decisión 203; metodología, 11).
// Abiertas: los apartados ### de «Propuestas pendientes». Por revisar: su «Estado» dice «pendiente de aprobación»
// o «pendiente de decisión». Sin kanban: no tienen la línea «- **Kanban:** …» con su tarea.
export async function leerRealimentacion($: $, raiz: string): Promise<Realimentacion | null> {
  const md = await textoPropuestas($, raiz)
  if (md === null) return null
  const ini = md.indexOf('\n## Propuestas pendientes')
  if (ini < 0) return null
  const fin = md.indexOf('\n## ', ini + 5)
  const bloques = md.slice(ini, fin < 0 ? undefined : fin).split('\n### ').slice(1)
  const porRevisar: Realimentacion['porRevisar'] = []
  let sinKanban = 0
  for (const b of bloques) {
    const titulo = (b.split('\n')[0] ?? '').trim()
    const est = /^- \*\*Estado:\*\*(.*)$/m.exec(b)?.[1] ?? ''
    // Número fijo de la propuesta, en su título: «P07 Título».
    const m = /^(P\d+) (.+)$/.exec(titulo)
    if (/pendiente de (aprobación|decisión)/i.test(est))
      porRevisar.push({ numero: m?.[1] ?? null, titulo: m?.[2] ?? titulo, resumen: resumenPropuesta(b), tipo: tipoPropuesta(b) })
    if (!/^- \*\*Kanban:\*\*/m.test(b)) sinKanban++
  }
  // Sin el número fijo («P07 »): así una propuesta que se numera no cuenta como nueva.
  const titulos = bloques.map(b => (b.split('\n')[0] ?? '').trim().replace(/^P\d+ /, ''))
  return { abiertas: bloques.length, titulos, porRevisar, sinKanban }
}

// propuestas.md vive en develop (tarea 273): cola.py le hace sus commits allí. Con otra rama activa, se lee el de
// develop, con git; si no se puede, o con develop activa, el de la carpeta. Primero en sf/ (decisión 203); si no está,
// en docs/, el sitio de antes, como hace cola.py.
const RUTAS_PROPUESTAS = ['sf/propuestas.md', 'docs/propuestas.md']
async function textoPropuestas($: $, raiz: string): Promise<string | null> {
  const git = await carpetaGit($, raiz)
  const rama = git ? await ramaActiva($, git) : null
  if (git && rama && rama.nombre !== 'develop' && (await existeRama($, git, 'develop'))) {
    for (const rel of RUTAS_PROPUESTAS) {
      const r = await $.process.run(['git', 'show', `develop:${rel}`], { cwd: raiz }).catch(() => null)
      if (r && r.exitCode === 0) return r.stdout
    }
  }
  for (const rel of RUTAS_PROPUESTAS) {
    const ruta = `${raiz}/${rel}`
    if (await $.fs.exists(ruta)) return await $.fs.read(ruta)
  }
  return null
}

// Carpeta del proyecto de la sesión, absoluta: si $.session.root() diera una ruta relativa, se completa con la
// carpeta de trabajo de la sesión.
export const absoluta = (ruta: string) => /^([a-zA-Z]:)?\//.test(ruta)

export async function raizSesion($: $): Promise<string> {
  const raiz = normal(await $.session.root())
  if (absoluta(raiz)) return raiz
  const cwd = normal(await $.session.cwd())
  if (!absoluta(cwd)) return raiz
  const partes = raiz.split('/').filter(x => x !== '' && x !== '.')
  return partes.length ? `${cwd}/${partes.join('/')}` : cwd
}


// Versión del plugin sf que se está ejecutando, de su manifiesto.
async function versionPlugin($: $): Promise<string | null> {
  try {
    return texto((await leerJson($, `${$.plugin.root}/.claude-plugin/plugin.json`)).version)
  } catch {
    return null
  }
}

// La línea con la que un proyecto incorporado antes importaba la copia de las reglas (sf ≤ 1.3).
const IMPORTA_COPIA = /^[ \t]*@(?:\.\/)?\.sf\/claude-sf\.md[ \t]*$/m

// El CLAUDE.md del proyecto aún importa la copia .sf/claude-sf.md: las reglas ya le llegan por ahí (atrasadas).
export async function importaCopia($: $, raiz: string): Promise<boolean> {
  for (const f of ['CLAUDE.md', '.claude/CLAUDE.md']) {
    const ruta = `${raiz}/${f}`
    if ((await $.fs.exists(ruta)) && IMPORTA_COPIA.test(await $.fs.read(ruta))) return true
  }
  return false
}

// El proyecto va por detrás de la SF: se incorporó con una versión anterior (se compara mayor.menor; los
// arreglos no obligan a ponerlo al día).
export function atrasada(e: Estado): boolean {
  const num = (v: string | null) => (v ?? '').split('.').slice(0, 2).map(x => Number.parseInt(x, 10))
  const [a, b] = [num(e.versionSf), num(e.versionPlugin)]
  if (e.tipo !== 'proyecto' || a.length < 2 || b.length < 2 || [...a, ...b].some(Number.isNaN)) return false
  return a[0]! < b[0]! || (a[0] === b[0] && a[1]! < b[1]!)
}

// `desde`: el inicio de la sesión (ms), para leer del historial solo lo que ha pasado en ella.
// La incorporación en marcha (tarea 333): el progreso que anota Claude con tools/incorporacion.py, en la carpeta de
// la SF de Claude Code, por proyecto, no por sesión: sobrevive a /reload-plugins, /clear, al modo prueba y a una sesión
// nueva (tarea 333, a petición del propietario). Solo si es de esta carpeta; null si no hay o no se entiende.
// La clave, como clave() de incorporacion.py: la ruta en minúsculas, con «_» en lo que no es letra o cifra ASCII o guion.
export const claveIncorporacion = (carpeta: string) => Array.from(normal(carpeta).toLowerCase(), c => (/^[a-z0-9-]$/.test(c) ? c : '_')).join('')
export async function rutaIncorporacion($: $): Promise<string | null> {
  const claude = await carpetaClaude($)
  if (!claude) return null
  return `${claude}/${CARPETA_COPIAS}/${PREFIJO_INCORPORACION}${claveIncorporacion(await raizSesion($))}.json`
}
export async function leerIncorporacion($: $, raiz: string): Promise<Incorporacion | null> {
  const ruta = await rutaIncorporacion($)
  if (!ruta || !(await $.fs.exists(ruta))) return null
  const d = await leerJson($, ruta)
  if (typeof d.carpeta !== 'string' || !igual(normal(d.carpeta), normal(raiz)) || !Array.isArray(d.pasos)) return null
  const pasos = d.pasos
    .filter((p): p is Record<string, unknown> => typeof p === 'object' && p !== null && typeof (p as Record<string, unknown>).nombre === 'string')
    .map(p => ({ nombre: p.nombre as string, respuesta: texto(p.respuesta) }))
  if (!pasos.length) return null
  const actual = typeof d.actual === 'number' && Number.isInteger(d.actual) && d.actual >= 0 && d.actual <= pasos.length ? d.actual : 0
  const recarga = d.recargar === true || typeof d.retomar === 'number'
  return { caso: texto(d.caso) ?? '', actual, pausa: d.pausa === true && actual > 0 && !recarga, ...(recarga ? { recarga } : {}), pasos }
}

export async function leerEstado($: $, desde = 0): Promise<Estado> {
  const raiz = await raizSesion($)
  const base: Estado = {
    tipo: 'sin-sf',
    proyecto: nombreCarpeta(raiz),
    versionSf: null,
    versionPlugin: await versionPlugin($),
    importaCopia: false,
    metodologia: true,
    kanban: null,
    avisosConfiguracion: [],
    color: null,
    fase: null,
    hechas: null,
    detalle: null,
    devslice: null,
    actualizado: null,
    pendientes: [],
    error: null,
    aviso: null,
    peticiones: [],
    errorPeticiones: null,
    realimentacion: null,
    rama: null,
    ramas: {},
    ...(await subagentesDeTareas($)),
    mergeadas: {},
    salidas: [],
    pushPendiente: [],
    develop: null,
  }
  // Las propuestas del propio proyecto, en su sf/propuestas.md (decisiones 194 y 203).
  base.realimentacion = await leerRealimentacion($, raiz).catch(() => null)
  const cola = await leerPeticiones($, raiz)
  base.peticiones = cola.peticiones
  base.errorPeticiones = cola.error
  base.salidas = await leerSalidas($, raiz, desde).catch(() => [])
  base.incorporacion = await leerIncorporacion($, raiz).catch(() => null)

  const conCarpeta = await $.fs.exists(`${raiz}/${PROYECTO}`)
  const antiguo = !conCarpeta && (await $.fs.exists(`${raiz}/${ANTIGUO}`))
  const esSf = !conCarpeta && !antiguo && (await $.fs.exists(`${raiz}/${MARCA_SF}`))
  // La identidad y la configuración (informe «Configuración inicial»): un archivo que no se lee es un error del
  // panel, y la configuración vale entonces la de por defecto.
  let ident: Record<string, unknown> = {}
  let errorIdent: string | null = null
  try {
    if (conCarpeta || antiguo) ident = await leerJson($, `${raiz}/${conCarpeta ? PROYECTO : ANTIGUO}`)
  } catch (err) {
    errorIdent = `no se puede leer ${conCarpeta ? PROYECTO : ANTIGUO}: ${String(err)}`
  }
  const conf = leerConfiguracion(conCarpeta || antiguo ? ident : null, esSf)
  base.metodologia = conf.metodologia
  base.kanban = conf.kanban
  // La rama, solo en proyectos con SF (también en la propia SF); se relee con la cola, en los mismos momentos.
  const git = conCarpeta || antiguo || esSf ? await carpetaGit($, raiz) : null
  if (git) {
    base.rama = await ramaActiva($, git)
    for (const p of base.peticiones) if (p.rama && !(p.rama in base.ramas)) base.ramas[p.rama] = await existeRama($, git, p.rama)
    base.mergeadas = await leerMergeadas($, raiz, git).catch(() => ({}))
    // Solo las de la sesión: las cerradas antes ya no salen en Cerradas.
    const conCierre = [...base.peticiones, ...base.salidas].filter(t => ultimoCierre(t.historial, desde) !== null)
    base.pushPendiente = await leerPushPendiente($, raiz, conCierre, conf.remoto).catch(() => [])
    const enRemotos = await remotos($, git)
    if (!errorIdent) base.avisosConfiguracion = avisosConfiguracion(conf, enRemotos)
    // Con develop activa, sus commits sin subir al remoto de la configuración (tarea 355).
    if (base.rama?.nombre === 'develop' && !base.rama.separada && enRemotos && conf.remoto in enRemotos)
      base.develop = await leerPorSubir($, raiz, git, conf.remoto).catch(() => null)
  }
  if (conCarpeta || antiguo) {
    if (errorIdent) return { ...base, tipo: 'proyecto', error: errorIdent }
    let datos: Record<string, unknown> = antiguo ? ident : {}
    // Sin metodología, el proyecto no tiene fase: no se lee ni se pide .sf/estado.json.
    try {
      if (!antiguo && conf.metodologia && (await $.fs.exists(`${raiz}/${ESTADO}`))) datos = await leerJson($, `${raiz}/${ESTADO}`)
    } catch (err) {
      return { ...base, tipo: 'proyecto', error: `no se puede leer ${ESTADO}: ${String(err)}` }
    }
    const leyendo = antiguo ? ANTIGUO : ESTADO
    const clave = conf.metodologia ? texto(datos.fase) : null
    const indice = FASES.findIndex(f => f.clave === clave)
    const hechas = conf.metodologia && Array.isArray(datos.hechas)
      ? datos.hechas.map(h => FASES.findIndex(f => f.clave === h)).filter(i => i >= 0)
      : null
    return {
      ...base,
      tipo: 'proyecto',
      proyecto: texto(ident.proyecto) ?? base.proyecto,
      versionSf: texto(ident.sf),
      importaCopia: await importaCopia($, raiz).catch(() => false),
      color: COLORES.find(c => c === texto(ident.color)?.toLowerCase()) ?? null,
      fase: indice >= 0 ? indice : null,
      hechas,
      detalle: conf.metodologia ? texto(datos.detalle) : null,
      devslice: conf.metodologia ? texto(datos.devslice) : null,
      actualizado: texto(datos.actualizado),
      pendientes: Array.isArray(datos.pendientes)
        ? datos.pendientes.filter((p): p is string => typeof p === 'string')
        : [],
      error:
        clave !== null && indice < 0
          ? `fase desconocida «${clave}» en ${leyendo}; valores: ${FASES.map(f => f.clave).join(', ')}`
          : null,
      aviso: antiguo
        ? `${ANTIGUO} es la ubicación anterior: pasar la identidad a ${PROYECTO} y el estado a ${ESTADO}`
        : null,
    }
  }

  if (await $.fs.exists(`${raiz}/${MARCA_SF}`)) {
    return { ...base, tipo: 'sf', proyecto: 'SoftwareFactory', color: COLOR_SF }
  }
  return base
}
// ── Ramas (decisión del propietario, 2026-10-29) ──
// Sin ejecutar git: se lee .git/HEAD. En un worktree, .git es un archivo «gitdir: <ruta>» y su HEAD está allí;
// las ramas, en la carpeta común (commondir), como en la carpeta principal.
export type Git = { head: string; comun: string }
const resolver = (base: string, r: string) => (absoluta(normal(r)) ? normal(r) : `${base}/${normal(r)}`)
export async function carpetaGit($: $, raiz: string): Promise<Git | null> {
  try {
    if (await $.fs.exists(`${raiz}/.git/HEAD`)) return { head: `${raiz}/.git`, comun: `${raiz}/.git` }
    if (!(await $.fs.exists(`${raiz}/.git`))) return null
    const m = /^gitdir:\s*(.+?)\s*$/m.exec(await $.fs.read(`${raiz}/.git`))
    if (!m) return null
    const head = resolver(raiz, m[1]!)
    let comun = head
    if (await $.fs.exists(`${head}/commondir`)) comun = resolver(head, (await $.fs.read(`${head}/commondir`)).trim())
    return { head, comun }
  } catch {
    return null
  }
}

export async function ramaActiva($: $, git: Git): Promise<Estado['rama']> {
  try {
    const h = (await $.fs.read(`${git.head}/HEAD`)).trim()
    const m = /^ref:\s*refs\/heads\/(.+)$/.exec(h)
    if (m) return { nombre: m[1]!, separada: false }
    return /^[0-9a-f]{7,}$/i.test(h) ? { nombre: h.slice(0, 7), separada: true } : null
  } catch {
    return null
  }
}

// Los subagentes de las tareas, por su número: el principal los lanza con la descripción «Tarea NN: …», y el panel
// pone su ⚙ (decisión del propietario, 2026-10-29). Trabajando: pending, running y waiting. Esperando instrucciones
// (verde y roja, decisión 162): idle y completed, que el motor deja retomar con su contexto; failed y killed, parados.
// $.agent.list() deja de dar un subagente poco después de que entregue su informe, aunque siga retomable: por eso
// se apuntan en la sesión ($.state, que no pasa a otra sesión: tras reiniciar Claude Code no queda ninguno) los vistos
// por su id. Uno que se veía trabajando y ya no sale en la lista entregó su informe: espera. Uno parado con TaskStop
// o cuyo turno acaba sin respuesta (interrumpido, error) queda parado (marcarSubagente). Si una tarea tiene uno
// trabajando y otro esperando, cuenta como trabajando. Un worktree que queda al acabar no cuenta. «Tarea 1480» no es
// la 148. Si el motor no da la lista, se queda lo apuntado.
const TRABAJANDO = new Set(['pending', 'running', 'waiting'])
const ESPERANDO = new Set(['idle', 'completed'])
const vistos = atom({ plugin: 'sf', key: 'subagentesVistos' } as const, {} as Record<string, SubagenteVisto>)
const tareaDe = (descripcion: string): number | null => {
  const m = /^tarea\s+(\d+)(?!\d)/i.exec(descripcion.trim())
  return m ? Number(m[1]) : null
}
export type SubagentesDeTareas = { subagentes: Record<number, string>; subagentesEsperando: Record<number, string> }
// Lo leído, con lo apuntado de cada subagente y si el motor dio la lista (sin ella no se sabe quién vive).
export type LecturaSubagentes = SubagentesDeTareas & { vistos: Record<string, SubagenteVisto>; conLista: boolean }
export async function leerSubagentes($: $): Promise<LecturaSubagentes> {
  const antes = (await read($, vistos)) ?? {}
  const ahora: Record<string, SubagenteVisto> = {}
  for (const [id, v] of Object.entries(antes)) ahora[id] = v.estado === 'trabajando' ? { ...v, estado: 'esperando' } : v
  let conLista = true
  try {
    const t = await $.clock.now()
    for (const a of await $.agent.list()) {
      const tarea = tareaDe(a.description)
      if (tarea === null) continue
      const estado = TRABAJANDO.has(a.status) ? 'trabajando' : ESPERANDO.has(a.status) ? 'esperando' : 'parado'
      // visto: la última vez que se le vio trabajando (tarea 249): un informe anotado después lo da por recogido.
      const visto = estado === 'trabajando' ? t : antes[a.id]?.visto
      ahora[a.id] = { tarea, descripcion: a.description, estado, ...(a.name ? { nombre: a.name } : {}), ...(visto ? { visto } : {}) }
    }
  } catch {
    // Sin la lista, lo apuntado, tal cual.
    conLista = false
    Object.assign(ahora, antes)
  }
  if (JSON.stringify(ahora) !== JSON.stringify(antes)) {
    await update($, vistos, () => ahora)
    await guardarSesion($, await raizSesion($), { vistos: ahora })
  }
  const subagentes: Record<number, string> = {}
  const subagentesEsperando: Record<number, string> = {}
  for (const v of Object.values(ahora)) {
    if (v.estado === 'trabajando') subagentes[v.tarea] ??= v.descripcion
    else if (v.estado === 'esperando') subagentesEsperando[v.tarea] ??= v.descripcion
  }
  for (const id of Object.keys(subagentes)) delete subagentesEsperando[Number(id)]
  return { subagentes, subagentesEsperando, vistos: ahora, conLista }
}
export async function subagentesDeTareas($: $): Promise<SubagentesDeTareas> {
  const { subagentes, subagentesEsperando } = await leerSubagentes($)
  return { subagentes, subagentesEsperando }
}

// Un subagente apuntado que cambia por un evento: su turno acaba (espera, o parado si no hubo respuesta) o se para
// con TaskStop, que lo nombra por su id o su nombre.
export async function marcarSubagente($: $, idONombre: string, estado: SubagenteVisto['estado']): Promise<void> {
  await update($, vistos, r => {
    const actual = r ?? {}
    const id = Object.keys(actual).find(k => k === idONombre || actual[k]!.nombre === idONombre)
    return id === undefined ? actual : { ...actual, [id]: { ...actual[id]!, estado } }
  })
  await guardarSesion($, await raizSesion($), { vistos: await read($, vistos) })
}

// Tras un cambio de plugin, con el estado vacío, los vistos que se guardaron de esta sesión (tarea 277); lo que ya
// hay en el estado manda.
export async function recuperarVistos($: $, guardados: Record<string, SubagenteVisto>): Promise<void> {
  await update($, vistos, r => ({ ...guardados, ...(r ?? {}) }))
}

// Existe la rama: su archivo en refs/heads o su línea en packed-refs.
export async function existeRama($: $, git: Git, rama: string): Promise<boolean> {
  try {
    if (await $.fs.exists(`${git.comun}/refs/heads/${rama}`)) return true
    if (!(await $.fs.exists(`${git.comun}/packed-refs`))) return false
    return (await $.fs.read(`${git.comun}/packed-refs`)).split('\n').some(l => l.trim().endsWith(` refs/heads/${rama}`))
  } catch {
    return false
  }
}

// El commit de una rama: su archivo en refs/heads o su línea en packed-refs; null si no existe.
export async function commitRama($: $, git: Git, rama: string): Promise<string | null> {
  return commitRef($, git, `refs/heads/${rama}`)
}
// El commit de una referencia completa (refs/heads/…, refs/remotes/…): su archivo o su línea en packed-refs.
export async function commitRef($: $, git: Git, ref: string): Promise<string | null> {
  try {
    if (await $.fs.exists(`${git.comun}/${ref}`)) return (await $.fs.read(`${git.comun}/${ref}`)).trim() || null
    if (!(await $.fs.exists(`${git.comun}/packed-refs`))) return null
    const l = (await $.fs.read(`${git.comun}/packed-refs`)).split('\n').find(x => x.trim().endsWith(` ${ref}`))
    return l ? (l.trim().split(' ')[0] ?? null) : null
  } catch {
    return null
  }
}

// Los commits de develop sin subir a <remoto>/develop (tarea 355): los cuenta git rev-list contra la referencia remota
// local, sin red; null sin esa referencia (develop nunca subida, o sin remoto). Las dos referencias se leen de archivo y
// git solo se ejecuta cuando alguna cambia: se guarda lo contado con sus commits, como en leerMergeadas.
let porSubirLeido: { raiz: string; local: string; remota: string; commits: number } | null = null
async function leerPorSubir($: $, raiz: string, git: Git, remoto: string): Promise<Estado['develop']> {
  const local = await commitRama($, git, 'develop')
  const remota = await commitRef($, git, `refs/remotes/${remoto}/develop`)
  if (local === null || remota === null) return null
  if (local === remota) return { remoto, porSubir: 0 }
  if (porSubirLeido?.raiz === raiz && porSubirLeido.local === local && porSubirLeido.remota === remota) return { remoto, porSubir: porSubirLeido.commits }
  const r = await $.process.run(['git', 'rev-list', '--count', `refs/remotes/${remoto}/develop..refs/heads/develop`], { cwd: raiz })
  const commits = Number(r.stdout.trim())
  if (r.exitCode !== 0 || r.stdout.trim() === '' || !Number.isInteger(commits)) return null
  porSubirLeido = { raiz, local, remota, commits }
  return { remoto, porSubir: commits }
}

// Las tareas mergeadas en develop (decisión del propietario, 2026-10-29): las que tienen un commit en la historia de
// develop, el squash de la C, con su número como «(N)» al final del título o como trailer «SF-Tarea: N» (decisión
// 207). Un «Revert "<título>"» posterior deja fuera sus commits más antiguos que él: el de un título «… (N)» nombra
// la tarea; si no, la del commit más cercano, por debajo, con ese título. Como tareas_en_develop de cola.py. Aquí sí
// se ejecuta git (log): solo cuando develop cambia, porque se guarda lo leído con su commit.
export const FORMATO_LOG = `--format=%h%x09%s%x09%(trailers:key=${TRAILER_TAREA},valueonly,separator=%x2C)`
export function tareasEnDevelop(lineas: string[]): Record<string, string[]> {
  const filas: { hash: string; titulo: string; n: string | null }[] = []
  for (const linea of lineas) {
    const [hash = '', titulo = '', trailer = ''] = linea.split('\t').map(x => x.trim())
    if (!hash || !titulo) continue
    filas.push({ hash, titulo, n: / \((\d+)\)$/.exec(titulo)?.[1] ?? /\d+/.exec(trailer)?.[0] ?? null })
  }
  const corte: Record<string, number> = {}
  filas.forEach(({ titulo }, i) => {
    const rv = /^Revert "(.*)"$/.exec(titulo)
    if (!rv) return
    const n = / \((\d+)\)$/.exec(rv[1]!)?.[1] ?? filas.slice(i + 1).find(x => x.titulo === rv[1])?.n ?? null
    if (n !== null && !(n in corte)) corte[n] = i
  })
  const mergeadas: Record<string, string[]> = {}
  filas.forEach(({ hash, titulo, n }, i) => {
    if (n === null || titulo.startsWith('Revert "') || i > (corte[n] ?? filas.length)) return
    ;(mergeadas[n] ??= []).push(hash)
  })
  return mergeadas
}
let mergeadasLeidas: { raiz: string; commit: string; mergeadas: Record<string, string[]> } | null = null
export async function leerMergeadas($: $, raiz: string, git: Git, fresco = false): Promise<Record<string, string[]>> {
  const commit = await commitRama($, git, 'develop')
  if (commit === null) return {}
  if (!fresco && mergeadasLeidas?.raiz === raiz && mergeadasLeidas.commit === commit) return mergeadasLeidas.mergeadas
  const r = await $.process.run(['git', 'log', 'develop', '--first-parent', '--max-count=1000', FORMATO_LOG], { cwd: raiz })
  if (r.exitCode !== 0) return {}
  const mergeadas = tareasEnDevelop(r.stdout.split(/\r?\n/))
  mergeadasLeidas = { raiz, commit, mergeadas }
  return mergeadas
}

// Pasos de una tarea (no son tareas ni llevan número): texto y estado. Los que no se entienden se ignoran.
export const ESTADOS_PASO = ['hecho', 'en-curso', 'pendiente'] as const
export function leerPasos(v: unknown): Paso[] {
  if (!Array.isArray(v)) return []
  return v.flatMap(x => {
    const o = (x ?? {}) as Record<string, unknown>
    const t = typeof o.texto === 'string' ? o.texto.trim() : ''
    const e = ESTADOS_PASO.find(y => y === o.estado)
    if (!t || !e) return []
    return [o.ayuda === true ? { texto: t, estado: e, ayuda: true as const } : { texto: t, estado: e }]
  })
}
// El campo «comprobado» de antes se lee como un paso hecho, antes de los de cierre y de las ayudas de prueba, como lo
// deja cola.py al cargar la cola (decisión 288).
const CIERRE = ['Activar rama para poder probar', 'Cerrar la tarea']
export function conComprobado(pasos: Paso[], comprobado: string | null): Paso[] {
  if (!comprobado) return pasos
  const paso: Paso = { texto: /^comprobado/i.test(comprobado) ? comprobado : `Comprobado: ${comprobado}`, estado: 'hecho' }
  const i = pasos.findIndex(x => x.ayuda || CIERRE.includes(x.texto))
  return i < 0 ? [...pasos, paso] : [...pasos.slice(0, i), paso, ...pasos.slice(i)]
}
// «3/5»: hechos de todos, sin las ayudas de prueba, que no se exigen (decisión 184).
export const cuentaPasos = (pasos: Paso[]) => {
  const exigidos = pasos.filter(x => !x.ayuda)
  return `${exigidos.filter(x => x.estado === 'hecho').length}/${exigidos.length}`
}
