# Cada documento compartido se actualiza en su propia tarea, «Actualizar <documento>»

Son documentos compartidos los «Cómo funciona…», la metodología, la plantilla `claude-sf.md` y el `CLAUDE.md` de la SF. Una tarea que necesita cambiar uno no lo cambia: su cambio va a la tarea de ese documento. Cómo se anota, en «El paso de documentar es crear la tarea de documentos» (116) y «Documentación, una vez por tarea» (147). La decisión de la tarea y sus pruebas siguen dentro de ella.

Cada documento tiene una sola tarea, «Actualizar <documento>». Un cambio nuevo en un documento con su tarea abierta se añade a ella. Si aun así hay dos tareas del mismo documento, el principal las fusiona directamente, sin pedírselo al propietario. La metodología, la plantilla y el `CLAUDE.md` de la SF comparten una («Las reglas del método se actualizan en una sola tarea», 148). Quién las hace, en «Documentos compartidos, también por subagente» (152).

Un documento compartido queda desfasado hasta que se hace su tarea.

Recoge lo que sigue valiendo de «Los documentos compartidos se actualizan en una tarea aparte» (112) y «Una tarea por documento que actualizar» (142), que quedan deprecadas.

Porqué: cada tarea cambiaba en su rama los documentos que todas tocan, y al cerrarlas con squash chocaban en ellos y en sus HTML (112). Cada cambio abría su propia tarea de documentación y había que fusionarlas a mano (142).

Aplicada en: `sf:orquestacion` («Documentos compartidos») y `references/porque.md`; `sf:flujo_tareas` («Fusionar y separar» y `references/estados.md`); metodología, «Documentos compartidos»; `CLAUDE.md` de la SF.
