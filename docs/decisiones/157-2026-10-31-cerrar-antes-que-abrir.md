# Cerrar antes que abrir

- **Origen:** SoftwareFactory, 2026-10-31, tras valorar la sesión en que la orquestación se revisó a fondo. El propietario: «Presionar por cerrar tareas en curso si es posible cerrarlas antes que presionar por poner en curso nuevas tareas».
- **Contexto:** en la sesión se crearon 17 tareas y se cerró una; con muchas tareas en curso a la vez, cada una con su subagente, sus decisiones y su estado, la orquestación se equivoca más. Crear una tarea por cada defecto sigue siendo lo correcto: la cola larga no es el problema, sí las que hay en curso.
- **Decisión:** el principal empuja primero a cerrar las tareas en curso que se pueden cerrar (llevar al propietario lo que necesitan para probar, decidir o cerrar) y solo después propone poner en curso tareas nuevas. Las peticiones y los defectos nuevos se siguen anotando en la cola en cuanto llegan.
- **Consecuencias:** menos tareas en curso a la vez y menos errores de orquestación; al estar libre, lo primero es desbloquear y cerrar lo que está en curso.
- **Aplicada en:** `sf:orquestacion` («Poner en curso» y «Libre»); metodología, «Tareas y cola».
