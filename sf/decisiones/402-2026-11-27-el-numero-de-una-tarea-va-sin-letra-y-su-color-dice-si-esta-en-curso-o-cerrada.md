# El número de una tarea va sin letra, y su color dice si está en curso o cerrada

En el panel, el número de una tarea va sin letra. Su color dice su estado: dorado si está en curso y verde si está cerrada; las demás, con el color normal del texto. Una reabierta lleva el número sobre rojo, aunque haya entrado en la sesión (159). El número va subrayado si la tarea tiene algo que desplegar.

Recoge lo que sigue valiendo de «El número de una tarea lleva el color de su estado, y una reabierta cuenta como H» (373), que queda deprecada.

Porqué: los códigos de tarea pesaban a la vista; primero se quitó el guion y después la letra, que quedó solo como color (propietario de la Software Factory, 2026-10-28 y 2026-10-31). Después, la A y la H dejaron de distinguirse, y el propietario: «las tareas ya no tienen letras asociadas y lo de la H ya no se usa» (tarea 439).

Aplicada en: `plugins/sf/hooks/panel.tsx` (`colorNumero`, `fondoNumero`) y `estilo.ts` (`colorLetra`), y sus pruebas.
