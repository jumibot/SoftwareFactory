# El orquestador decide el modelo de inferencia más adecuado para cada hilo

El agente principal elige, para cada hilo que lanza (el subagente de una tarea, un encargo, una investigación), el modelo de inferencia que mejor le encaja según el trabajo: su dificultad, su riesgo y su coste. No se usa por defecto el mismo modelo para todo.

Por qué: decisión del propietario de la Software Factory. Los hilos tienen necesidades muy distintas, desde una búsqueda mecánica hasta un diseño delicado, y un solo modelo para todos gasta de más en unos y se queda corto en otros.

Cómo se aplica (criterios, dónde se anota el modelo elegido, si el propietario puede cambiarlo), en su tarea.
