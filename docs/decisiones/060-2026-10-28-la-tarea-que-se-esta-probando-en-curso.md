# La tarea que se está probando, en curso

- **Origen:** SoftwareFactory, 2026-10-28. El propietario: «una tarea que se esta probando tiene que aparece como tarea en curso puesto que se está trabajando en ella...».
- **Decisión:** con «Probar ahora», Claude marca la petición con `probando`. Mientras dura la prueba, el panel la muestra como en curso (en la línea de arriba y en Pendientes, en amarillo), con su código de Testing, «66-T», porque su estado no cambia. Al llegar el resultado, Claude quita la marca: sale de la cola si está probada, queda en Testing si está pendiente o se reabre si hay que corregirla.
- **Aplicada en:** metodología (2 y 6) y skill `sf:metodologia`; plantilla `templates/claude-sf.md`; mod de estado; especificación; `docs/como-funciona-la-software-factory.md`; plugin `sf` 0.30.9.
