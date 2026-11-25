# Por qué de cada regla

El porqué de cada regla de la skill, en el orden de sus secciones. Cada entrada cita la decisión de la SF que la fijó, con su título y su número entre paréntesis.

## Lo común a todos los documentos

- **Una skill general de diseño y skills de contenido encima** («Una skill general de diseño de documentos, y skills de contenido encima», 232): el generador y los recursos vivían dentro del documento fundacional, la visión tenía su propia maqueta y los informes la tomaban prestada; cada recurso nuevo se metía en el fundacional aunque sirviera a todos. Así un recurso nuevo mejora todos los documentos a la vez, crear un tipo nuevo es escribir solo lo suyo y los documentos tienen un aspecto común.
- **Comunicar bien es un objetivo** («Una skill propia para los informes de las deliberativas, ligera sobre el diseño común», 231): cada informe se maquetaba distinto y con HTML a mano. Al decidirlo, el propietario lo dijo así: «Me gusta mucho el tema de la usabilidad de los docs… Creo que comunicar es vital para los proyectos». De ahí que la usabilidad no sea un adorno.

## Tipos de documento

- **La maqueta antigua se migra al regenerar** («Cada documento se migra al generador único cuando se vuelve a tocar», 309): los documentos que ya existen no se migran de golpe, sino cuando se vuelven a tocar por otra razón.

## Catálogo de recursos

- **Una sección sin etiqueta sale con número y título** («Las secciones sin etiqueta salen con número y título hasta que el estilo del proyecto diga otra cosa», 306): al migrar documentos al generador único no se reescribe ninguno; la forma de la sección la fija el estilo, y mientras no la fije, esta es la regla por defecto. **La forma la elige cada proyecto** («La forma de la cabecera de sección es un parámetro del estilo», 321).
- **La infografía técnica, con el estilo del proyecto** («La infografía técnica se puede incrustar como cualquier recurso o ir como pieza aparte», 315): puede ir incrustada, como cualquier recurso, o aparte y enlazada; en las dos es del mismo proyecto que el documento.
- **La infografía, en cualquier tipo de documento** («Una infografía técnica se puede meter en cualquier documento que la necesite», 330): lo pidió el propietario: se mete donde el documento lo requiera, sin limitarlo por perfil.
- **El diagrama es un recurso del catálogo** («El diagrama es un recurso del catálogo y el generador único llama al motor de la skill de diagramas», 314): el documento nombra su `.diagrama` y el generador lo dibuja al generar, así que sale al día sin tocar el `.md`. El motor no se funde en el generador: la skill de diagramas conserva su comprobador, sus pruebas y sus páginas sueltas.
- **Los diagramas toman el estilo del documento** («Los diagramas toman el estilo del documento; tinta, en el selector y en páginas sueltas», 307): se pintan con el papel, los colores, el acento y la letra del documento. El tema tinta queda para el selector de la herramienta y las páginas sueltas.
- **La marca del lector, en los colores del logo** («Logo «/SF»: barra estrecha y empinada en morado claro», 255): la barra de «/SF» va en un morado más claro que las letras, para destacarla como la tecla de la orden; el lector lo repite.
- **Los recursos de la visión, para todos** («Todos los recursos de la visión pasan al catálogo común», 308): los narrativos y los generales de la maqueta de la visión sirven a cualquier documento; la skill de cada tipo dice cuáles le convienen.

## Cuándo usar cada recurso

- **Recursos desde la primera versión, nada monótono** (231): la usabilidad de los documentos es un objetivo de la SF, no un retoque que se pide después.

## Estilo del proyecto

- **Un solo generador y un estilo por proyecto** («Un solo generador determinista con el estilo del proyecto; una skill ayuda a fijar sus parámetros con muestras y afinado», 305): todo lo común de la maquetación está en un generador determinista que lee los parámetros del estilo; el estilo vale para todos los documentos del proyecto y se puede seguir afinando.
- **En `docs/identidad/estilo.json`, aparte de `identidad.json`** («El estilo del proyecto se guarda en docs/identidad/estilo.json, con la referencia a los archivos de su logo», 316): `identidad.json` queda para los componentes, los iconos y las reglas; el estilo, con la referencia al logo, en su archivo.
- **Valores resueltos; el tema, solo el origen** («estilo.json guarda los valores resueltos; el tema del catálogo es solo la muestra de partida», 317): así una actualización del plugin no cambia el estilo de un proyecto sin una vuelta de afinado.
- **El aspecto, solo del estilo; la lectura, de cada documento** («El aspecto lo fija solo el estilo; cada documento fija cómo se lee», 318): el estilo es del proyecto, no de cada documento (305): si un `.md` fija su aspecto, el generador avisa. La lectura (destino, herramientas y menú) la sigue fijando cada documento, con el valor del estilo por defecto.
- **`sobre-primario` y `primario-texto`** («Dos roles de color para un primario claro: sobre-primario y primario-texto», 319): un primario de marca claro, como el amarillo de la SF, no se lee como texto ni lleva texto blanco encima; con estos dos roles se usa sin perder contraste.
- **El generador se detiene por contraste** («El generador se detiene con un texto por debajo de 4,5:1 y avisa con un borde o una línea», 320): el contraste es calidad de la salida y el generador la garantiza; un borde o una línea solo avisan. Se revisará con la práctica.
- **Versión e historial** («Cada afinado del estilo sube su versión, se anota en su historial y respalda la anterior», 322): el pie de cada documento dice con qué versión del estilo se generó, y la anterior queda en `_respaldo/` para volver atrás.
- **Sin `estilo.json`, los valores por defecto de un tema** («Un proyecto sin estilo.json se genera con los valores por defecto de un tema elegido por su color», 323): fijar el estilo no bloquea tocar un documento; se avisa una vez.
- **La cabecera destacada, con un color propio** («La cabecera destacada usa un color propio, derivado del primario, para claro y para oscuro», 351): un primario vivo, como un amarillo, a todo el ancho resulta demasiado brillante.
- **`primario-linea` a 3:1 y el aviso de los bordes** («Estilo de la SF: amarillo de la web, cabecera en banda, portada oscura y las demás recomendadas del informe de estilo», 335, puntos 8 y 9): con un primario claro, las líneas de los diagramas necesitan su propio rol para llegar a 3:1; los bordes de los campos se avisan a 3:1 y el de las cajas, suave a propósito, queda fuera. Salió de comparar muestras reales con sus alternativas.
- **`oscuro` y `tinta-oscura`, dos roles** («El rol oscuro se parte en superficie oscura y tinta fuerte», 349): con un solo valor, en modo oscuro o las superficies o la tinta quedaban ilegibles.

## Temas e identidad

- **La paleta oscura se deriva de la clara** («Los temas sin paleta oscura la derivan solos de la clara», 348): con reglas fijas vale para cualquier estilo sin diseñar a mano una paleta oscura por tema.
- **Modo oscuro con la paleta del estilo, sin invertir** («El modo oscuro de los documentos usa la paleta oscura del estilo en lugar de invertir la página», 347): al invertir, el color de la marca dejaba de ser el suyo (el amarillo salía ocre; el terracota, salmón) y no se veía la familia oscura que calcula el estilo.

## Herramientas y opciones de lectura

- **Colores de significado y de código, aclarados en oscuro** («Los colores de significado y del resaltado de código se aclaran solos en oscuro», 350): no hace falta un juego elegido a mano, y se mantiene el contraste en cualquier estilo.
- **Los ajustes de la herramienta «Diagramas»** («Opciones de los diagramas: todas ajustables, con los favoritos del propietario por defecto, cabecera y pie configurables y vertical forzable», 302): todo lo que se probó en la síntesis de los diagramas queda como opción ajustable, con los favoritos del propietario encendidos por defecto.

## Generar

- **Cada cambio del `.md` regenera su HTML** («Cada cambio de un .md regenera su HTML», 220): nada obligaba a regenerarlo y algunos informes se quedaban sin HTML o desfasados. Un `.md` y su HTML nunca quedan distintos.

## Respaldar

- **Antes de sustituir, a `_respaldo/`** («Antes de sustituir un documento, se respalda en _respaldo/», 217): cada vuelta sustituye al documento en `develop`, y volver a una versión anterior exigía buscarla en el historial de git. Con la copia, volver atrás es copiarla de vuelta.
- **Cada vuelta, a `develop`** («Los documentos nuevos van a develop en cada vuelta y se ofrecen en el navegador», 216): un documento nuevo no rompe nada y se deshace borrándolo, pero pasaba por rama, squash y observación como el código, y el propietario tenía que ir al worktree del subagente para leerlo. Qué hacer con dos vueltas del mismo motivo sigue por decidir.
