# Cada vuelta de un documento la lleva a develop una sola orden, solo con ese documento

Una orden de cola.py lleva cada vuelta de un documento a develop: la tarea declara su documento, se respalda la versión de develop, se regenera el HTML, se hace el commit en develop sin cambiar de rama y, si la tarea es el foco, se abre el HTML.

- Solo su documento: la orden solo lleva a develop el documento declarado y lo suyo; en una documental con rama, cerrar se niega si la rama toca otros archivos.
- Documento nuevo: su subagente escribe en un worktree desprendido desde develop, sin rama propia (compatible con la 278); la orden lo lleva a develop y pone el worktree al día.
- Abrir: lo abre la orden si la tarea es el foco (382); si no, lo dice en su salida y el principal lo da como off-topic. Para volver a abrirlo, el botón Abrir de la 452.
- Respaldos: con el nombre de la 217, y «-2», «-3»… solo si ya existe; solo de los documentos que se reescriben enteros, no de los registros (propuestas, decisiones y su índice), que ya guarda git.
- Búsquedas: un .ignore con _respaldo/ en la raíz de la SF y en la de cada proyecto (lo pone la incorporación), para que Claude no cite como vigente una versión anterior.
- Revisión con notas: la copia anotada se guarda junto al documento y fuera de git (*.notas-*.html en el .gitignore, también en los proyectos); el subagente le pasa extraer_notas.py en la vuelta siguiente.

Porqué: las piezas existen pero van a mano, y se nota: 11 de los 25 HTML no corresponden a su .md y seis informes no tienen HTML. El propietario da el OK a las recomendaciones del informe «Tareas de documentos de punta a punta» (tarea 303).

Aplicada en: pendiente, en las tareas que salen de la 303.
