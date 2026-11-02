# La sección 2 de la metodología resume el flujo de tareas y remite a sf:flujo_tareas

- **Origen:** SoftwareFactory, 2026-10-29, al revisar la tabla de estados de la tarea 92. El propietario: «ok, opción 1».
- **Contexto:** la metodología es operativa: viaja en el plugin y Claude la sigue en cada proyecto. La sección 2 cuenta el flujo de tareas entero (estados, pasos, botones, ramas, subagentes), y la skill `sf:flujo_tareas` lo cuenta ordenado. Con los dos textos, Claude tendría dos instrucciones para lo mismo, que ya divergen (la «X roja», sin `descartada`), y cargaría ese detalle cada vez que lee la metodología.
- **Decisión:** la sección 2 queda en lo esencial: un proyecto por sesión, una cola, una rama por tarea, un commit por tarea al cerrarla y el principal que orquesta a los subagentes. El detalle del flujo está solo en `sf:flujo_tareas`, a la que remite. Los acuerdos con su fecha siguen en `docs/decisiones/`.
- **Consecuencias:** la skill es la fuente única del flujo; una regla nueva se escribe una vez. Lo hace una tarea de documentos aparte (decisión 112), anotada en la 92 con «Documentar: tarea 146».
- **Aplicada en:** pendiente, tarea 146.
