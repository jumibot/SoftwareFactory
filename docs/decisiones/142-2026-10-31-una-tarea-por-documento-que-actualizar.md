# Una tarea por documento que actualizar

- **Origen:** SoftwareFactory, 2026-10-31, tarea 197. Al revisar la deficiencia «tareas de documentación en serie» del análisis de la tarea 194, el propietario: «las tareas documentales que tengan una descripción tipo "Actualizar Manual…" y como paso lo que haya que actualizar. Todas las tareas de actualizar el mismo documento que surjan que se fusionen directamente».
- **Contexto:** cada cambio de la SF abría su propia tarea de documentación, que tocaba varios documentos, y después había que fusionarlas a mano.
- **Decisión:** las tareas de actualizar documentación son una por documento, con el título «Actualizar <documento>», y cada cambio que hay que llevar a él es un paso. Un cambio nuevo en un documento que ya tiene su tarea abierta se añade como paso; si aun así hay dos tareas del mismo documento, el principal las fusiona directamente, sin pedírselo al propietario.
- **Consecuencias:** el paso hecho «Creada la tarea NN para actualizar la documentación» nombra la tarea del documento, nueva o ya abierta. La metodología y el CLAUDE.md de la SF se ajustan en sus tareas de actualizar.
- **Aplicada en:** plugins/sf/skills/flujo_tareas/SKILL.md y references/estados.md.
