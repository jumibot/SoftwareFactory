# El tipo de tarea decide cómo se maneja el repositorio

- **Origen:** SoftwareFactory, 2026-11-02. Al repasar los tipos de tarea de «Tareas deliberativas: registrar decisiones y dilemas abiertos» (274), el propietario: «entre tipos de tareas también cambia el manejo del repo».
- **Contexto:** todas las tareas seguían el mismo camino que una de código: rama `feature/NN-nombre`, worktree del subagente, squash en `develop` y observación. Las decisiones «Los documentos nuevos van a develop en cada vuelta y se ofrecen en el navegador» (216), «Antes de sustituir un documento, se respalda en _respaldo/» (217) y «Una tarea deliberativa da un informe y las tareas que salgan» (218) ya marcan caminos distintos.
- **Decisión:** el tipo de una tarea decide cómo se maneja el repositorio en ella, y no solo cómo se cierra:
  - **Código** (implementar, corregir): rama de la tarea, worktree del subagente, squash en `develop` al cerrar y observación.
  - **Documentos nuevos** (también el informe de una deliberativa): sin rama para el documento; cada vuelta se copia a `develop` con su respaldo previo, y se cierra con la aprobación del propietario, sin observación.
  - **Cambio de documentos existentes:** rama de la tarea y squash al cerrar, con la aprobación del propietario.
  - El modelo de ramas del proyecto (`develop`, `main`) no cambia («El manejo del repositorio no se negocia: siempre develop», 205); lo que cambia es cómo lo usa cada tipo.
- **Consecuencias:** `cola.py` (la rama al poner en curso, el encargo del subagente, la recogida y los pasos de cierre) y `sf:flujo_tareas` tienen que distinguir el tipo. Es la base de la propuesta de familias de la 274, cuyas preguntas lo concretan.
- **Aplicada en:** metodología, «Tareas y cola» («El tipo decide cómo se maneja el repositorio»); `plugins/sf/tools/cola.py` (`TIPOS`, `DELIBERATIVAS`, `PREFIJO_POR_TIPO`, el encargo según el tipo); `sf:flujo_tareas` («Deliberativas sin rama»); `sf:orquestacion` («Probar y cerrar»); pendiente: el camino propio de las tareas documentales y «Cómo funciona la Software Factory».
