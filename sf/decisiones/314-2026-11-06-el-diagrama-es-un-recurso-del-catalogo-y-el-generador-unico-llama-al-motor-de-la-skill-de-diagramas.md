# El diagrama es un recurso del catálogo y el generador único llama al motor de la skill de diagramas

El diagrama es un recurso más del catálogo del generador único: el documento nombra su archivo `.diagrama` y el generador lo dibuja al generar el documento, con el estilo del documento.

Para dibujarlo, el generador único llama al motor de la skill de diagramas (`generar_diagrama.py`), que no se funde en él: la skill conserva su comprobador, sus pruebas, las páginas sueltas de diagramas y lo que venga, como el replay.

Tarea: «Que cada proyecto tenga un solo estilo de documentos: una base común de maquetación para todas las skills de documentos» (385).
