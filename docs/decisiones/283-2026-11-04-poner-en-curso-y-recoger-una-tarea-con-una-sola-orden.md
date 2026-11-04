# Poner en curso y recoger una tarea con una sola orden

Fecha: 2026-11-04. Decidida por el propietario de la Software Factory.

Poner en curso una tarea lo hace todo de una vez: el estado, su rama, la carpeta de trabajo del subagente con su rama auxiliar y apuntarlo en la cola. No hace falta una orden nueva: «en-curso» hace el trabajo completo.

Al volver un subagente, se recoge con una sola orden de cola.py (traer sus commits a la rama de la tarea, registrar su informe, marcar sus pasos hechos con su texto y dejarla lista para probar con qué mirar). El subagente la deja escrita al final de su informe; el principal revisa el diff y la lanza.

Porqué: medido en las últimas sesiones largas, la mitad de las llamadas del principal son a cola.py y lo caro no son las órdenes (1,4 s) sino los turnos del modelo entre una y otra (unos 4 s cada uno). Juntarlas libera antes al principal para hablar con el propietario. Descartado delegarlo en un agente de la cola siempre vivo: cada operación sería de 2 a 3 veces más lenta (informe «Liberar al agente principal», tarea 358).

Aplicada en: la tarea «Poner en curso y recoger una tarea con una sola orden».
