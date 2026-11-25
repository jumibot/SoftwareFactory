# Los pasos de una tarea se deciden en modo plan

- **Origen:** SoftwareFactory, 2026-11-01. El propietario: «decisión: usa plan_mode para decidir los pasos de una tarea».
- **Contexto:** al poner una tarea en curso, el principal planifica sus pasos en la cola y lanza el subagente (`sf:orquestacion`, «Poner en curso»). Los pasos se anotaban sin que el propietario viera el plan antes, y a menudo se corregían después.
- **Decisión:** el principal decide los pasos de una tarea en el modo plan de Claude Code: entra en él, prepara los pasos y los presenta como plan; el propietario lo aprueba o lo corrige al salir del modo plan. Solo con el plan aprobado se anotan los pasos en la cola, se crea la rama y se lanza el subagente.
- **Consecuencias:** el propietario ve y aprueba los pasos antes de que empiece el trabajo. Poner una tarea en curso pide un paso más del propietario. Hay que recogerlo en `sf:orquestacion`.
- **Aplicada en:** sustituida por la decisión 181 (el principal planifica los pasos sin pedir aprobación).
