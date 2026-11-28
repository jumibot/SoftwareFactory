# Un diagrama se construye de arriba abajo, por niveles de abstracción, cada uno con sus reglas

Regla: el generador no resuelve el diagrama de golpe. Lo construye de arriba abajo, en niveles, y cada nivel tiene sus propias reglas y se puede revisar antes de pasar al siguiente:
1. Esqueleto: las carpetas cerradas, colocadas por capas en el orden de los flujos, con un carril por par y sentido y su descripción (435, 437, 438, 439, 440).
2. Contenido: dentro de cada carpeta, sus cajas y solo sus flujos internos, con el mismo método si hay sub-carpetas (441).
3. Uniones: los carriles entre carpetas se conectan con las cajas de dentro.
Cada nivel parte de lo que fijó el anterior y no lo deshace.

Porqué: antes se intentaba colocar cajas, carpetas y flujos a la vez, y con diagramas complejos (cinco carpetas, relaciones cruzadas) el dibujo se estropeaba; partir la complejidad por niveles de abstracción la hace manejable y comprobable (norma del propietario, 28/11/2026, tarea 483).
