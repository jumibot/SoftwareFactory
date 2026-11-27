# Separar pasos de una tarea en una tarea nueva lo hace cola.py, sin Claude

`/sf_split` y «Separar pasos» del panel separan pasos de una tarea en curso o en cola en una tarea nueva, también a mitad de turno. `/sf_split 89 2,3` separa los pasos 2 y 3 de la 89, numerados como salen al desplegarla; `/sf_split 89` pregunta cuáles; `/sf_split` a secas pregunta antes la tarea, entre las cuatro más recientes con dos pasos o más (otra, por su número).

Lo hace `cola.py split`, sin Claude. Antes, el mod relee la cola: si la tarea o sus pasos han cambiado, avisa y no cambia nada.

La nueva va en cola, sin rama, con el número siguiente al último dado, los pasos separados con su estado y el tipo de la original. Se llama como su primer paso y no lleva descripción (098). Si un paso separado ya estaba hecho, cola.py avisa de que su trabajo sigue en la rama de la original. Renombrar queda para el propietario o para Claude.

No se separan los pasos de cierre ni las ayudas de prueba; hacen falta dos pasos de trabajo o más, y no se pueden separar todos: eso es renombrarla.

Recoge lo que sigue valiendo de «/split separa pasos en una tarea nueva» (097), que queda deprecada.

Porqué: separar la eliminación de la 89 en la 96 hubo que pedírselo a Claude a mano (097). Separar es mover datos de la cola; el propietario de la Software Factory: «/split 106 2 se podría hacer sin inferencia? solo es tocar datos» («Comandos antes que inferencia»).

Aplicada en: `plugins/sf/hooks/register.tsx`, `cola.ts` y `panel.tsx` («Separar pasos»), y sus pruebas; `plugins/sf/tools/cola.py` (`split`); `sf:flujo_tareas`.
