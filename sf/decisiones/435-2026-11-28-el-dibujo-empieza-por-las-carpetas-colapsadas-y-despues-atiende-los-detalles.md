# El dibujo empieza por las carpetas colapsadas y después atiende los detalles

Regla: el generador coloca primero el diagrama de las carpetas vacías, colapsadas: cada carpeta es un nodo y los flujos entre cajas de carpetas distintas se agregan en flujos entre carpetas. Con esa colocación fijada, despliega cada carpeta en su sitio y coloca sus cajas y flujos internos, y luego los flujos entre cajas de carpetas distintas siguiendo el recorrido ya decidido entre sus carpetas. Vale para todos los diagramas con carpetas, también en la horizontal.

Porqué: con cinco carpetas y relaciones complejas entre ellas (flujo de audio de LupDub), colocar cajas y carpetas a la vez estropea el dibujo; decidir primero la forma de las carpetas da un esqueleto estable y los detalles se acomodan dentro (norma del propietario, 28/11/2026, tarea 483).
