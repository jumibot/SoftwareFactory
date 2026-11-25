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

## Cada vuelta

- **Respaldar antes de sustituir** («Antes de sustituir un documento, se respalda en _respaldo/», 217): cada vuelta sustituye al informe en `develop`, y volver a una versión anterior exigía buscarla en el historial de git. Con la copia, volver atrás es copiarla de vuelta.
- **Regenerar el HTML en el mismo cambio** («Cada cambio de un .md regenera su HTML», 220): nada obligaba a regenerarlo y algunos informes se quedaban sin HTML o desfasados.
- **A `develop` en cada vuelta, sin rama** («Los documentos nuevos van a develop en cada vuelta y se ofrecen en el navegador», 216): un documento nuevo no rompe nada y se deshace borrándolo, pero pasaba por rama, squash y observación como el código, y el propietario tenía que ir al worktree del subagente para leerlo. En `develop` lo lee siempre, y Claude le ofrece abrir el HTML con cada versión nueva.
