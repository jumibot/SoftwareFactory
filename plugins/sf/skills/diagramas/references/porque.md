# Por qué de cada regla

El porqué de las reglas de la skill que citan una decisión de la SF, en el orden de sus secciones. Cada entrada cita la decisión con su título y su número entre paréntesis.

## Antes de dibujar

- **Los ajustes por defecto, los favoritos del propietario** («Opciones de los diagramas: todas ajustables, con los favoritos del propietario por defecto, cabecera y pie configurables y vertical forzable», 302): todo lo que se probó en la síntesis de los diagramas queda como opción ajustable; encendidas por defecto, las que prefirió el propietario (etiquetas con el color del botón, lo que hace Claude en cursiva y discontinuo, acento de foco, resaltado del recorrido, fichas en el HUD y croquetas), y apagadas las demás, como los carriles con nombre.
- **Sin tema, la figura toma el del documento** («Los diagramas toman el estilo del documento; tinta, en el selector y en páginas sueltas», 307): un diagrama dentro de un documento se pinta con el papel, los colores, el acento y la letra del documento. El tema tinta queda para el selector de la herramienta y las páginas sueltas.

## Reglas de diagram-design

- **Etiquetas de flecha separadas de su línea, con el color del botón solo en el texto** («Las etiquetas de las flechas, al estilo de diagram-design: texto separado de la línea, con el color del botón solo en el texto», 301): el original de diagram-design se ve más limpio. Un botón opaco sobre la flecha recarga el dibujo y rompe la regla de separar la etiqueta de su línea; el color del texto basta para reconocer el botón.
- **Carriles con nombre, apagados por defecto** (302): son una de las opciones que el propietario dejó apagadas.

## Pendiente

- **El generador de documentos dibuja cada `.diagrama`** («El diagrama es un recurso del catálogo y el generador único llama al motor de la skill de diagramas», 314): el documento solo nombra su `.diagrama`, y el generador llama al motor de esta skill al generar, así que el diagrama sale al día sin tocar el `.md`. El motor no se funde en el generador: la skill conserva su comprobador, sus pruebas y sus páginas sueltas.
