# Poner un proyecto al día con la SF, sin tarea

- **Origen:** SoftwareFactory, 2026-11-01. El propietario: «la actualización de un proyecto a la última versión es farragosa innecesariamente… Hay que hacerlo más directo, sin tarea, informar de los cambios, pedir autorización y hacerlos».
- **Contexto:** poner un proyecto al día con la SF (caso «actualizar» de `sf:incorporar_proyecto_a_sf`) pasaba por crear una tarea con su rama, probarla y cerrarla en `develop`. El proceso ya está probado en la SF, así que esa ceremonia sobra.
- **Decisión:** poner un proyecto al día no crea tarea ni rama. Claude dice qué va a cambiar, pide la autorización del propietario y, con ella, aplica los cambios directamente en `develop` del proyecto, con su commit.
- **Consecuencias:** actualizar es un paso corto en la sesión del proyecto. Es una excepción a trabajar siempre bajo una tarea en curso, limitada a esta operación. Sigue siendo en una sesión abierta en el proyecto.
- **Aplicada en:** `sf:incorporar_proyecto_a_sf` («Actualizar, sin tarea») y `sf:orquestacion` («Con cada mensaje», 4).
