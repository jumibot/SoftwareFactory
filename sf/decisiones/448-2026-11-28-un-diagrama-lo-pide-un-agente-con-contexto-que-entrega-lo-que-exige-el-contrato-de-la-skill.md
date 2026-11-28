# Un diagrama lo pide un agente con contexto, que entrega lo que exige el contrato de la skill

Regla: todo diagrama lo pide un agente que tiene el contexto de lo que necesita contar. La skill de diagramas fija un contrato con lo que hay que tener claro antes de dibujar, en prosa: objetivo, concepto, puntos clave, actores, glosario y exterior (actores externos, entradas y salidas, 447). Esa petición se escribe en un archivo propio antes de dibujar, para que quede guardada. Quien dibuja trabaja solo con la petición y con la skill, sin ver diagramas anteriores; lo que el contrato pide y no está, no lo supone.

Las peticiones se guardan: se congelan como casos y se reutilizan para refinar al dibujante y al generador, comparando cada versión con la anterior sobre las mismas peticiones.

Prueba limpia y realista: un agente nuevo recibe el encargo de documentar cómo maneja el repositorio la SF (ramas, commits y releases), un documento que aún no existe. Los SVG que su documento necesite los decide él con la skill nueva (congelada para la prueba), escribiendo antes la petición de cada uno. Se auditan sus lecturas, se guardan las peticiones y se revisan los diagramas.

Porqué: quien dibuja no puede deducir lo que no se le dice, como qué es del sistema y qué es exterior; la prueba tiene que reproducir el uso real, un agente que escribe un documento y necesita sus diagramas; y las peticiones guardadas permiten mejorar el dibujante y el generador sobre casos reales y fijos (norma del propietario, 28/11/2026, tarea 483).
