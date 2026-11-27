# El registro de decisiones es obligatorio

Estado: deprecada el 2026-11-27 por «Lo mínimo de todo proyecto SF son las tareas, el repositorio y el registro de decisiones; la metodología se elige» (410); lo demás, por «Las decisiones son material de la SF: siempre en sf/decisiones/» (208) y «El mod entrega las reglas y sf:orquestacion al empezar la sesión, tras /clear y tras compactar» (379).

- **Origen:** SoftwareFactory, 2026-10-30, tarea 190. El propietario: «Todos los proyectos sf registrarán las decisiones. No es opcional».
- **Contexto:** la decisión «Configuración inicial: tareas y repo siempre, el resto opcional» dejaba el registro de decisiones en `docs/decisiones/` como elegible, desactivado por defecto sin la metodología.
- **Decisión:** todo proyecto bajo la SF registra sus decisiones en `docs/decisiones/`, una por archivo, con o sin la metodología. El mínimo fijo de la configuración inicial pasa a ser tareas, repositorio y registro de decisiones; solo la metodología se elige.
- **Consecuencias:** cambia en ese punto la decisión «Configuración inicial: tareas y repo siempre, el resto opcional». La incorporación crea siempre `docs/decisiones/` y las reglas que se importan siempre al `CLAUDE.md` incluyen la de registrar cada decisión con su porqué.
- **Aplicada en:** `sf:incorporar_proyecto_a_sf` (crea siempre `sf/decisiones/`).
