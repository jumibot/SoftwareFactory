# Los documentos compartidos se actualizan en una tarea aparte

Estado: deprecada el 2026-11-25 por «Cada documento compartido se actualiza en su propia tarea, «Actualizar <documento>»» (377); lo demás, por «El paso de documentar es crear la tarea de documentos» (116), «Documentación, una vez por tarea» (147) y «Documentos compartidos, también por subagente» (152).

- **Origen:** SoftwareFactory, 2026-10-29, tras varios cierres que chocaron en los mismos documentos. El propietario: «las tareas que requieran actualizar documentos que lo anoten como nueva tarea y así evitamos la colisión de este tipo».
- **Contexto:** cada tarea actualizaba en su rama los documentos que todas tocan, y al cerrarlas con squash chocaban en ellos y en sus HTML generados.
- **Decisión:** una tarea que necesita cambiar un documento compartido no lo cambia: anota una tarea nueva para ello y añade el paso «Documentar: tarea NN». Son documentos compartidos «Cómo funciona la Software Factory», «Cómo funciona el panel», la metodología, la plantilla `claude-sf.md` y `CLAUDE.md`. La decisión de la tarea, en su propio archivo, y sus pruebas siguen dentro de la tarea. Las tareas de documentos se hacen de una en una, en el principal, sin subagentes en paralelo. Cuando hay varias, el orquestador sugiere fusionarlas con `/fusionar` (regla «El orquestador sugiere fusiones y splits»).
- **Consecuencias:** los documentos compartidos quedan desfasados hasta que se hace su tarea; el paso «Documentar: tarea NN» lo recuerda. Matiza la regla de actualizar «Cómo funciona» al cambiar una pieza.
- **Aplicada en:** lo vigente, en `sf:orquestacion` («Documentos compartidos») y la metodología, «Documentos compartidos».
