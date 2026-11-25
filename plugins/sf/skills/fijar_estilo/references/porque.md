# Por qué de cada regla

El porqué de cada regla de la skill, en el orden de sus secciones. Cada entrada cita la decisión de la SF que la fijó, con su título y su número entre paréntesis. Lo que significa cada parámetro, y el porqué de los del estilo, está también en el `porque.md` de `crear_documentos`.

## Para qué sirve

- **Un estilo por proyecto, fijado con muestras y afinado** («Un solo generador determinista con el estilo del proyecto; una skill ayuda a fijar sus parámetros con muestras y afinado», 305): el estilo vale para todos los documentos del proyecto y se guarda como parámetros que lee el generador. Esta skill pregunta, enseña muestras hechas por el generador para elegir y afina en vueltas; no maqueta, y el estilo se puede seguir afinando con el proyecto.
- **En `docs/identidad/estilo.json`** («El estilo del proyecto se guarda en docs/identidad/estilo.json, con la referencia a los archivos de su logo», 316): aparte de `identidad.json`, que queda para los componentes, los iconos y las reglas.
- **Fijar el estilo no bloquea nada** («Un proyecto sin estilo.json se genera con los valores por defecto de un tema elegido por su color», 323): sin `estilo.json`, el generador usa los valores por defecto de un tema, elegido por el color del proyecto, y avisa una vez; tocar un documento no espera al estilo.
- **La cabecera de sección, un parámetro más** («La forma de la cabecera de sección es un parámetro del estilo», 321): cada proyecto elige su forma con las muestras, como el resto del estilo.
- **El contraste lo vigila el generador, no esta skill** («El generador se detiene con un texto por debajo de 4,5:1 y avisa con un borde o una línea», 320): el contraste es calidad de la salida y el generador la garantiza; por eso las muestras con poco contraste salen con su aviso.

## Herramienta

- **Partir de un estilo completo; el tema, solo como origen** («estilo.json guarda los valores resueltos; el tema del catálogo es solo la muestra de partida», 317): con todos los valores resueltos, una actualización del plugin no cambia el estilo de un proyecto sin una vuelta de afinado.
- **Aceptar sube la versión, anota el historial y respalda** («Cada afinado del estilo sube su versión, se anota en su historial y respalda la anterior», 322): el pie de cada documento cita la versión del estilo con que se generó, y la anterior queda en `_respaldo/` para volver atrás.
- **El catálogo y las muestras, dentro del proyecto** («Todo documento que genera la SF se guarda en su proyecto como un activo», 352): lo generado fuera del proyecto se pierde y no se puede consultar ni compartir después; una carpeta temporal sirve solo para pruebas.
- **El catálogo, con el estilo del proyecto** («El estilo de la SF es el de un proyecto más, sin tema propio en el plugin», 353): la SF no tiene un tema especial; su estilo es su `estilo.json`, hecho con esta skill como en cualquier proyecto, porque la SF se lleva igual que los demás.
- **Un primario nuevo trae su familia** («Al cambiar el color principal del estilo se recalculan solos sus derivados», 338): al probar la skill, poner el primario en amarillo dejó el resto en el terracota del tema de partida, y el documento salió medio amarillo y medio terracota. Se descartaron un atajo `colores.marca` aparte y cambiar los derivados a mano.
- **La cabecera destacada, apagada** («La cabecera destacada usa un color propio, derivado del primario, para claro y para oscuro», 351): un primario vivo, como un amarillo, a todo el ancho resulta demasiado brillante.
- **El modo oscuro, derivado de la clara** («El modo oscuro de los documentos usa la paleta oscura del estilo en lugar de invertir la página», 347; «Los temas sin paleta oscura la derivan solos de la clara», 348): invertir la página cambiaba el color de la marca (el amarillo salía ocre; el terracota, salmón). Derivar con reglas fijas vale para cualquier estilo sin diseñar a mano una paleta oscura por tema.

## Procedimiento

- **Un primario claro lleva `sobre-primario` y `primario-texto`** («Dos roles de color para un primario claro: sobre-primario y primario-texto», 319): un primario de marca claro, como el amarillo de la SF, no se lee como texto ni lleva texto blanco encima; con estos dos roles se usa sin perder contraste.
- **No se regeneran todos los documentos de golpe** («Cada documento se migra al generador único cuando se vuelve a tocar», 309): cada documento toma el estilo nuevo cuando se vuelve a tocar por otra razón.
- **Las seis muestras del plugin y una con el color del proyecto** («Estilo de la SF: amarillo de la web, cabecera en banda, portada oscura y las demás recomendadas del informe de estilo», 335, puntos 6 y 7): una muestra por tema, más una séptima con el color del proyecto, y un documento corto con todos los recursos para enseñarlas. Salió de comparar muestras reales con sus alternativas.

## Lo que el generador no sabe hacer

- **Sin excepciones en el proyecto** («El aspecto lo fija solo el estilo; cada documento fija cómo se lee», 318): el aspecto es del proyecto, no de cada documento; si un `.md` lo fija, el generador avisa. Lo que falta se pide como parámetro nuevo del generador, que gana parámetros con su uso (305).
- **En otro proyecto, una issue en GitHub de la SF** («Un parámetro de estilo que pide otro proyecto se dice en una línea y se ofrece abrir una issue en GitHub de la SF», 324): los desarrolladores de otros proyectos solo tienen el plugin, no el proyecto de la SF; un «pedido a la SF» en su historial no llegaría a nadie, y la issue sí.
