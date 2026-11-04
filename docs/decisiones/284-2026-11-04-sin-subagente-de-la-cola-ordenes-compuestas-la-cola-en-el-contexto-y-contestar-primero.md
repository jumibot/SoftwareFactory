# Sin subagente de la cola: órdenes compuestas, la cola en el contexto y contestar primero

Fecha: 2026-11-04. Decidida por el propietario de la Software Factory.

No hay subagente de gestión de la cola. Para que el propietario no espere por la cola:

- Órdenes compuestas: poner en curso y recoger una tarea con una sola orden (decisión 283), y añadir varios pasos con una sola orden, también al crear la tarea.
- La cola en el contexto del principal: el mod le pone en cada mensaje del propietario las tareas en curso y lo que cambió en la cola, para que no tenga que consultarla antes de contestar. Como el contexto de entrada es barato, también lo demás que ahorre consultas.
- Contestar primero: el principal contesta al propietario y anota en la cola después, cuando lo anotado no cambia la respuesta. Anotar al llegar sigue valiendo: en el mismo turno.

Porqué: medido en cinco sesiones largas, lo que se podría delegar es casi siempre una sola orden por turno de unos 5 s, de los que solo 1,4 s son de cola.py; delegarla en un subagente también cuesta un turno del principal, así que ahorraría alrededor de un segundo por turno, a cambio de órdenes que fallan sin que nadie lo vea, operaciones desordenadas y una excepción a que solo el principal escribe la cola (informe «Que la cola no frene al principal», tarea 358).

Aplicada en: la tarea «Poner en curso y recoger una tarea con una sola orden» (360), la tarea «Que el principal tenga la cola en su contexto» y la de actualizar las reglas del método (sf:orquestacion).
