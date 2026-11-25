# Un solo generador determinista con el estilo del proyecto; una skill ayuda a fijar sus parámetros con muestras y afinado

Un solo generador de documentos, determinista, para todas las skills de documentos. Todo lo común de la maquetación se extrae a ese generador, que maqueta cualquier documento con los parámetros del estilo del proyecto.

El estilo es del proyecto, no de cada documento: vale para todos sus documentos y se guarda como parámetros que lee el generador.

Una skill ayuda a fijar esos parámetros. Cuando un proyecto necesita documentos, pregunta al desarrollador por su estilo y le enseña varias muestras, hechas por el generador, para que elija. Después lo afina en vueltas sucesivas, como se hizo con la skill de diagramas. La skill no maqueta: el generador sigue haciendo su trabajo.

El estilo se puede seguir afinando a medida que avanza el proyecto.

El generador es una pieza que evoluciona: gana parámetros y refinamientos a lo largo de su uso.

En la Software Factory, el estilo de partida es el del informe deliberativo «Un estilo de documentos por proyecto» (385).

Tarea: «Que cada proyecto tenga un solo estilo de documentos: una base común de maquetación para todas las skills de documentos» (385).
