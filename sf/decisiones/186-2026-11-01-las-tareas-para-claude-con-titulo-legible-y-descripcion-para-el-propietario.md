# Las tareas para Claude, con título legible y descripción para el propietario

- **Origen:** SoftwareFactory, 2026-11-01, al redescribir la tarea «cola.py encargo N genera la parte fija del encargo de un subagente» (250). El propietario preguntó «¿qué hace en realidad esta tarea?» y después: «Cuando crees una tarea para ti, tiene que tener un título legible y al menos también una parte de su descripción».
- **Contexto:** las tareas que mejoran el trabajo de Claude (órdenes de cola.py, avisos al principal, encargos de subagentes) se titulaban y describían con su mecánica interna, y el propietario no entendía para qué sirven.
- **Decisión:** toda tarea que Claude crea para sí mismo lleva un título legible para el propietario, que diga qué gana, y al menos una parte de su descripción escrita para él: qué cambia y para qué, sin jerga interna. El detalle técnico puede seguir después.
- **Consecuencias:** el propietario entiende todas las tareas de la cola, también las internas. Hay que recogerlo en `sf:orquestacion` («Cómo escribir»).
- **Aplicada en:** `sf:orquestacion` («Cómo escribir», 268).
