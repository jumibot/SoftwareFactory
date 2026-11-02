# Flujo de tareas: un CLI común, historial por tarea y copias de la cola

- **Origen:** SoftwareFactory, 2026-10-29, tarea 92 (skill sf:flujo_tareas). El propietario eligió las tres opciones recomendadas.
- **Contexto:** los cambios de estado de las tareas estaban repartidos entre la metodología, la plantilla, CLAUDE.md, las decisiones y cola.ts. El panel deducía lo ocurrido comparando lecturas de la cola, con errores (una H en lugar de una A, reabiertas falsas, la 117 con C y sin R). La cola, fuera de git, no tenía copia.
- **Opciones:** comandos en un CLI común, en dos implementaciones (panel y Claude) o solo en el panel; historial por tarea, registro de eventos aparte o seguir deduciendo; copias locales rotativas, la cola en git o en JKanban.
- **Decisión:**
  - **Un CLI común** para cada cambio de estado (crear, poner en curso con su rama, paso, cerrar, descartar, revertir, reabrir, eliminar, fusionar, separar). Lo usan Claude, por Bash, y el panel, con `$.process.run`. Una sola implementación de cada regla.
  - **Historial por tarea:** cada tarea guarda en `.sf/peticiones.json` la lista de sus cambios de estado, con fecha y quién lo hizo. El panel lee el historial en lugar de deducirlo.
  - **Copias locales rotativas:** cada escritura de la cola guarda antes una copia en `.sf/copias/`, con las últimas N; se recupera con un comando.
- **Consecuencias:** la lógica de cola.ts pasa al CLI; la skill sf:flujo_tareas es la fuente única del ciclo de vida, y CLAUDE.md y la plantilla remiten a ella.
- **Aplicada en:** tarea 92.
