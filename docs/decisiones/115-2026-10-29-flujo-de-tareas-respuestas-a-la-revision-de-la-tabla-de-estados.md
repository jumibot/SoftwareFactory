# Flujo de tareas: respuestas a la revisión de la tabla de estados

- **Origen:** SoftwareFactory, 2026-10-29, revisión de la tabla de la tarea 92 (`flujo_tareas/references/estados.md`). El propietario: «ok a la propuesta en bloque, sí a las dos».
- **Contexto:** la tabla dejó 23 huecos e incoherencias entre las reglas escritas y el código del panel.
- **Decisión:**
  1. **Lenguaje del CLI:** Python, como `tools/indice_decisiones.py`.
  2. **El historial de lo que sale de la cola:** va a `.sf/historial.jsonl`, una línea por tarea que sale, con su historial completo.
  3. **Una eliminada «sin rastro»:** sale de la cola y de la vista, pero su historial queda en `.sf/historial.jsonl`: de ahí se recupera.
  4. **Testing con ramas:** cerrar sin probar también hace el squash en `develop`; la tarea en Testing ya no se descarta, se revierte.
  5. **La C sin pasos:** la C exige los pasos «Probar la tarea» y «Cerrar la tarea»; sin ellos no sale.
  6. **La rama de una reabierta:** una rama nueva desde `develop`.
  7. **Reabrir una descartada o una revertida:** como cualquier reabierta, con una rama nueva desde `develop`.
  8. **Deshacer una fusión o una eliminación:** deshacer una fusión es la tarea 135 (`/desfusionar`); una eliminación se recupera desde el historial.
  9. **Dejar una tarea en cola:** lo hace el principal, con el OK del propietario, y la tarea conserva su rama.
  10. **Quién, cuando actúa el panel:** `quien` es `propietario` o `principal`; `via`, `panel` o `cli`.
  11. **Pasos en el historial:** entran: cada paso añadido y marcado.
  12. **Cuántas copias:** las últimas 50.
  13. **Escrituras a la vez:** el CLI usa un archivo de bloqueo, `.sf/peticiones.lock`.
  14. **Un subagente y el CLI:** vale la norma escrita: el subagente no escribe la cola; el CLI no lo comprueba.
  15. **La rama de un subagente, ocupada:** el subagente trabaja en una rama auxiliar desde la de la tarea, y el principal la trae con `git merge --ff-only`.
  16. **Quién apunta la rama de un subagente:** el principal, antes de lanzarlo.
  17. **Subagentes en el panel:** el panel marca con ⚙ las tareas con un subagente trabajando (tarea 145).
  18. **El commit de una tarea:** el hash del squash entra en el historial y la R lo lee de ahí.
  19. **Push que falla:** entra en el historial y el panel lo recuerda.
  20. **Propuestas con rama:** una propuesta que toca un activo lleva rama y squash, sin pasar por Testing.
  21. **Proyectos donde el commit lo hace el propietario:** sigue aparte, en la tarea 104.
  22. **Restos de símbolos viejos:** a la tarea de documentos 146.
  23. **Dónde vive la regla:** la metodología (2) queda en un resumen que remite a la skill (decisión 114).
- **Consecuencias:** el CLI `cola.py` y la skill `sf:flujo_tareas` se construyen con estas respuestas; el panel pasa a leerlas en la tarea 145.
- **Aplicada en:** `plugins/sf/skills/flujo_tareas/references/estados.md`, en sus tarjetas; metodología, en la tarea 146.
