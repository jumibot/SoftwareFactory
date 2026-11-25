# Libre, el orquestador desbloquea las tareas en curso

- **Origen:** SoftwareFactory, 2026-10-29. El propietario: «la prioridad del orquestador cuando no estoy conversando de una tarea (no estoy interactuando) y está libre el agente principal es ver si hay alguna tarea en curso pendiente del desarrollador. En tal caso debe preguntar para resolverlo necesario y poder continuar la tarea».
- **Contexto:** varias tareas en curso se quedaron paradas esperando una respuesta que nadie pedía; el propietario tuvo que preguntar qué estaba pendiente de él.
- **Decisión:** cuando el principal está libre y el propietario no está hablando de una tarea, lo primero es repasar las tareas en curso que esperan algo del propietario (una decisión, un diseño, una prueba) y preguntarle lo necesario para que sigan. Lo que no necesita al propietario se lanza sin preguntar (orquestación con subagentes).
- **Aplicada en:** metodología, 2 («Orquestación con subagentes»); plantilla `claude-sf.md`; `CLAUDE.md`.
