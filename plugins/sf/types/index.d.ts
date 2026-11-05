// Paso de una tarea: texto y estado. ayuda: ayuda de prueba, tras «Activar rama para poder probar» y sin exigirla
// para cerrar (decisión 184).
export type Paso = { texto: string; estado: 'hecho' | 'en-curso' | 'pendiente'; ayuda?: true }

// Petición del propietario en la cola de la sesión (.sf/peticiones.json, fuera de git)
export type Peticion = {
  id: number
  texto: string
  // descartada: con la D del panel o pidiéndoselo a Claude; se ve en Cerradas con D hasta que se limpian
  estado: 'en-curso' | 'en-cola' | 'en-observacion' | 'descartada'
  prueba: string | null // qué debe mirar el propietario (en curso o en observación)
  descripcion: string | null // los detalles de la petición; el panel la muestra al desplegarla
  tipo?: string | null // deliberar, documentar, diseñar, implementar, especificar, corregir o investigar; tras el título
  commit: string | null
  observando: boolean // en observación y el propietario la está mirando ahora: se muestra como en curso
  pasos: Paso[] // los pasos de la tarea, si tiene varios: no son tareas ni llevan número
  reabierta?: boolean // reabierta por un bug tras salir de la cola (cerrada en otra sesión): vuelve a Cerradas
  rama: string | null // rama de la tarea: con rama ya tiene trabajo efectivo y no se puede eliminar
  historial: Evento[] // cada cambio, el más antiguo primero; lo escribe cola.py
  cambio?: number | null // último cambio: la fecha más reciente de su historial, en ms; null sin historial
}

// Un cambio del historial de una tarea (cola.py): su evento, su fecha (ms; null si no se entiende) y su detalle.
// via: por dónde se hizo (cli o panel), si lo dice.
export type Evento = { evento: string; fecha: number | null; detalle: string | null; via?: string }

// Una tarea que ha salido de la cola, de .sf/historial.jsonl (la última línea de su número): estado es el de salida,
// cerrada, eliminada, absorbida, descartada o revertida.
export type Salida = { id: number; texto: string; estado: string; commit: string | null; historial: Evento[]; tipo?: string | null }

// Las propuestas del proyecto, leídas de su sf/propuestas.md (decisiones 194 y 203)
export type Realimentacion = {
  abiertas: number // propuestas en «Propuestas pendientes»
  titulos: string[] // sus títulos
  porRevisar: { numero: string | null; titulo: string; resumen: string; tipo: string | null }[] // las pendientes de aprobación o de decisión, con su resumen y su tipo («- **Tipo:**», de los de cola.py)
  sinKanban: number // abiertas sin línea «- **Kanban:**»
}


// Tarea con un cierre en la sesión (sale en Cerradas): fecha, la del último evento de cierre, en ms.
export type Cerrada = { id: number; texto: string; commit: string | null; fecha: number; tipo?: string | null }

// Modo prueba (solo en la SF): disponible, el catálogo local está registrado; pedido, los ajustes piden la copia de trabajo.
export type Prueba = { disponible: boolean; pedido: boolean }
// RELEASE: la versión de la que se parte, la del último tag vX.Y.Z (null: ninguno, se pregunta la primera), los
// manifiestos a los que se sube y si es la propia SF (decisión 226).
export type FuenteVersion = { actual: string | null; manifiestos: string[]; sf: boolean }
// ACTUALIZAR: la versión publicada más alta del plugin sf y los scopes que el proyecto usa con una instalada más vieja.
// REFRESCAR (decisión 177): sin scopes, la versión instalada y, en corre, la más vieja que corre la sesión.
export type Actualizacion = { version: string; scopes: string[]; corre?: string }

// Lo que el panel recuerda de la sesión, en $.state: las tareas quitadas de Cerradas con «limpiar», con la fecha de
// su último cierre al quitarlas. Un cierre posterior la devuelve a la lista.
export type Sesion = { limpiadas: Record<string, number> }


// El progreso de una incorporación (tarea 333), de ~/.claude/sf/incorporacion-<sesión>.json, que escribe
// tools/incorporacion.py: el caso, el paso en que se está (desde 1; 0, todos hechos) y los pasos con su respuesta.
// recarga: la incorporación pidió recargar los plugins y sigue sola tras recargar (tarea 366).
export type Incorporacion = { caso: string; actual: number; pausa: boolean; recarga?: boolean; pasos: { nombre: string; respuesta: string | null }[] }
// Qué parte de la lista de la incorporación se ve (tarea 333): desde qué paso (desde 0), movida a mano con ▲ y ▼ cuando el
// actual era `actual`; al cambiar el actual, la lista vuelve a seguirlo.
export type VistaIncorporacion = { desde: number; actual: number }

export type Estado = {
  // 'sf': repositorio de la propia SF; 'proyecto': tiene .sf/proyecto.json (o el antiguo docs/sf.json); 'sin-sf': ninguno
  tipo: 'sf' | 'proyecto' | 'sin-sf'
  proyecto: string
  versionSf: string | null
  versionPlugin: string | null // versión del plugin sf que se está ejecutando
  // su CLAUDE.md aún importa la copia .sf/claude-sf.md de las reglas: va atrasado (decisión 187)
  importaCopia: boolean
  // sigue la metodología (fases y documentos del método): sin ella, no hay fase ni .sf/estado.json (tarea 193)
  metodologia: boolean
  kanban: { proveedor: 'jkanban'; proyecto: string } | null // el kanban elegido, si hay (decisión 224)
  // los avisos de .sf/proyecto.json: valores que no se entienden y el remoto que falta o no es de GitHub (decisión 230)
  avisosConfiguracion: string[]
  color: string | null // color de la sesión (/color), de .sf/proyecto.json
  fase: number | null // índice en FASES, desde 0
  // índices de las fases hechas; null = todas las anteriores a la actual
  hechas: number[] | null
  detalle: string | null
  devslice: string | null
  actualizado: string | null
  pendientes: string[]
  error: string | null
  aviso: string | null // p. ej., estado aún en docs/sf.json
  peticiones: Peticion[]
  errorPeticiones: string | null
  realimentacion: Realimentacion | null
  // Rama activa de la carpeta del proyecto, leída de .git/HEAD; separada: HEAD sin rama, y nombre es el commit corto.
  // null sin .git o sin SF (decisión del propietario, 2026-10-29).
  rama: { nombre: string; separada: boolean } | null
  // Si existe cada rama de las tareas de la cola (campo rama), por su nombre.
  ramas: Record<string, boolean>
  // Los subagentes trabajando (pending, running o waiting), por el número de su tarea («Tarea NN: …» en su
  // descripción), con esa descripción. Vacío si el motor no da la lista.
  subagentes: Record<number, string>
  // Los subagentes que esperan instrucciones (idle o completed, que se pueden retomar), por su tarea, si ninguno
  // trabaja en ella. Opcional: un estado guardado antes no lo tiene.
  subagentesEsperando?: Record<number, string>
  // Tareas que han entrado en develop: por su número, sus commits cortos «… (N)» en develop aún sin revertir, el
  // más reciente primero. Son las que la R del panel puede revertir.
  mergeadas: Record<string, string[]>
  // Las tareas que han salido de la cola con algún cambio en la sesión, de .sf/historial.jsonl.
  salidas: Salida[]
  // Las tareas con el push de develop pendiente: su cierre anotó push-fallido y origin/develop aún no tiene su commit.
  pushPendiente: number[]
  // Con develop activa, el remoto de la configuración y cuántos commits de develop faltan por subir a su develop, según
  // la referencia remota local, sin red; null sin remoto o sin esa referencia (tarea 355). Opcional: un estado guardado
  // antes no lo tiene.
  develop?: { remoto: string; porSubir: number } | null
  // La incorporación en marcha en esta sesión y en esta carpeta, si la hay (tarea 333). Opcional: un estado guardado
  // antes no lo tiene.
  incorporacion?: Incorporacion | null
}

// Un subagente de una tarea visto en la sesión, por su id: su tarea, su descripción, su nombre (el de SendMessage
// y TaskStop) y cómo está. Esperando: entregó su informe y se puede retomar; parado: con TaskStop, o fallido.
// visto: la última vez (ms) que se le vio trabajando; un informe de cola.py posterior lo da por recogido (tarea 249).
export type SubagenteVisto = { tarea: number; descripcion: string; nombre?: string; estado: 'trabajando' | 'esperando' | 'parado'; visto?: number }
// Los avisos de subagentes ya dados (tarea 249): sus claves, si la sesión es nueva y aún no se ha dado ninguno, y el id
// de la sesión de la que se sabe (tarea 277; sin él, el estado acaba de empezar: se busca en .sf/subagentes.json).
export type AvisosSubagentes = { claves: string[]; nueva: boolean; sesion?: string }

declare module 'claude-code' {
  interface PluginState {
    'sf': { estado: Shaped<Estado | null>; nuevasEnSf: number; prompts: number; avisadoPanel: number; inicioSesion: number; minuto: number; sesion: Sesion; panelCerrado: boolean; plegado: Record<string, boolean>; desplazamiento: number; turnoAvisos: number; identidadPuesta: { color: string | null; nombre: string | null }; prueba: Prueba; porConfirmar: string | null; fuenteRelease: FuenteVersion | null; actualizacion: Actualizacion | null; publicadaConocida: string | null; comprobadaEn: number | null; subagentesVistos: Record<string, SubagenteVisto>; pantallaOfrecida: boolean; reglasDadas: boolean; incorporarOfrecido: boolean; avisosSubagentes: AvisosSubagentes; vistaIncorporacion: VistaIncorporacion | null }
  }
}
