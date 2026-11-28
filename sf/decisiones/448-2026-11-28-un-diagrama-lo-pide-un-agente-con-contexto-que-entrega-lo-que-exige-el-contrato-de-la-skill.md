# Un diagrama lo pide un agente con contexto, que entrega lo que exige el contrato de la skill

Regla: todo diagrama lo pide un agente que tiene el contexto de lo que necesita contar. La skill de diagramas fija un contrato con lo que hay que tener claro antes de dibujar, en prosa: objetivo, concepto, puntos clave, actores, glosario y exterior (actores externos, entradas y salidas, 447). Quien dibuja trabaja solo con eso y con la skill, sin ver diagramas anteriores; lo que el contrato pide y no está, no lo supone.

Prueba limpia y realista: un agente nuevo recibe el encargo de documentar cómo funciona el proxy de la 475, con el informe y el código y sin ningún diagrama. El resultado de su encargo es un documento, y los SVG que ese documento necesite los decide y los crea él mismo con la skill nueva (congelada para la prueba). Se auditan sus lecturas y los diagramas se comparan con la referencia.

Porqué: quien dibuja no puede deducir lo que no se le dice, como qué es del sistema y qué es exterior; y la prueba tiene que reproducir cómo se usará de verdad: un agente que escribe un documento y necesita sus diagramas (norma del propietario, 28/11/2026, tarea 483).
