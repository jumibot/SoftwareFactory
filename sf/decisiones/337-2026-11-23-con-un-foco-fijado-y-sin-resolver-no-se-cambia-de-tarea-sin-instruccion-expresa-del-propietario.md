# Con un foco fijado y sin resolver no se cambia de tarea sin instrucción expresa del propietario

Mientras el foco del propietario está fijado en una tarea y no se ha resuelto (cerrada, o abandonada por él), Claude no cambia de tarea ni mueve el foco a otra, salvo instrucción expresa del propietario. Anotar otra tarea, añadirle pasos, ponerla en curso o lanzar su subagente no cambian el foco: su línea FOCUS sigue nombrando la tarea fijada y lo demás va como off-topic.

Por qué: el propietario pidió actualizar las reglas de orquestación mientras probaba la 392; Claude puso en curso la 418 y movió a ella la línea del foco, sacándole de la prueba que tenía a medias. Cada cambio de tarea no pedido rompe el hilo del propietario; el foco solo lo mueve él.

Se aplica en la tarea «Afinar las reglas del foco con el uso» (417).
