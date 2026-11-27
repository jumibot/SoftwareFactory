# Por qué de cada regla

El porqué de cada regla de la skill, en el orden de sus secciones. Cada entrada cita la decisión de la SF que la fijó, con su título y su número entre paréntesis.

## Qué es el informe

- **Tres familias de tarea** («Siete tipos de tarea en tres familias, para agentes especializados», 223): los siete tipos se cerraban todos como si fueran de código. Las deliberativas (investigar, deliberar, diseñar) dialogan, deciden y separan temas; las documentales escriben un documento acordado. Por eso son familias distintas, cada una con su forma de trabajar.
- **Un informe y las tareas que salgan** («Una tarea deliberativa da un informe y las tareas que salgan», 218): cada deliberación dejaba su informe con su forma, y lo decidido se aplicaba unas veces en la misma tarea y otras en tareas nuevas; nada decía qué produce una deliberativa. Los dilemas viven en su informe, al día con cada respuesta, para que no se pierdan en la cola ni en otro archivo.
- **Lo que es de otra tarea se propone separar** («En una deliberativa, lo que es de otra tarea se propone separar», 221): en las deliberaciones surgían temas que no eran suyos y todo se quedaba en la misma tarea, que crecía y perdía el foco. Al cerrar, lo que siga abierto sale a su tarea: ningún dilema abierto se pierde.
- **La skill del agente de la familia deliberativa** (223; «Agentes del plugin por familia de tarea, solo si la especialización aporta», 282): las familias existen para que cada una pueda tener su agente especializado, pero solo si la especialización aporta algo a cómo se hace su trabajo. Mientras no exista, la carga el subagente de la tarea.
- **Una skill propia, ligera sobre el diseño común** («Una skill propia para los informes de las deliberativas, ligera sobre el diseño común», 231): cada informe se maquetaba distinto y con HTML a mano. Esta skill reutiliza el generador y el diseño comunes y solo añade lo suyo: la estructura fija, las fichas de pregunta y el ciclo de cada vuelta. Comunicar bien es un objetivo de la SF: al decidirlo, el propietario dijo que comunicar es vital para los proyectos.

## Dónde va

- **En `sf/informes/`** («Los documentos de la SF van en la carpeta sf/», 203): en `docs/` chocaban con los documentos del proyecto, y en `.sf/` quedaban escondidos (las búsquedas de Claude se saltan las carpetas con punto, Obsidian no las ve y en macOS y Linux no se ven en el explorador).
- **También en la propia SF** («Todos los informes de las tareas de la SF se mudan a sf/informes/», 346): así todos los informes quedan en un solo sitio, como en los demás proyectos.

## Las preguntas

- **Cada pregunta se entiende sola, y sin números como sujeto** («Cada pregunta al propietario se entiende sola, sin números como sujeto», 397): en la tarea «Poner al día las decisiones: un solo formato y las antiguas, deprecadas» (439), las preguntas de su informe decían «la 115», «la 117» o «la 053 con la 054» sin explicar de qué iban. El propietario: «¿qué es la 115 o la 117? Me haces preguntas con cero contexto. Estoy trabajando con muchas tareas a la vez y no cambio de contexto igual que un ordenador». Por eso cada pregunta empieza por de qué va, en palabras llanas, y nombra cada decisión por lo que dice, con su número solo entre paréntesis.
- **Parte de lo que se ve hoy, comprobado** (397, en la misma tarea 439): aun con contexto, el propietario no entendió la pregunta sobre la caja del estado del proyecto y preguntó si estaba deprecada y si la caja seguía activa. En el chat la entendió en cuanto se le dijo, comprobado en el panel, que la caja sí funciona, cuándo sale y que lo deprecado era solo la decisión que la creó. La pregunta escrita lleva eso mismo: qué ve hoy, si funciona y qué es lo que cambia.

## Cada vuelta

- **Respaldar antes de sustituir** («Antes de sustituir un documento, se respalda en _respaldo/», 217): cada vuelta sustituye al informe en `develop`, y volver a una versión anterior exigía buscarla en el historial de git. Con la copia, volver atrás es copiarla de vuelta.
- **Regenerar el HTML en el mismo cambio** («Cada cambio de un .md regenera su HTML», 220): nada obligaba a regenerarlo y algunos informes se quedaban sin HTML o desfasados.
- **A `develop` en cada vuelta, sin rama** («Los documentos nuevos van a develop en cada vuelta y se ofrecen en el navegador», 216): un documento nuevo no rompe nada y se deshace borrándolo, pero pasaba por rama, squash y observación como el código, y el propietario tenía que ir al worktree del subagente para leerlo. En `develop` lo lee siempre, y Claude le ofrece abrir el HTML con cada versión nueva.
