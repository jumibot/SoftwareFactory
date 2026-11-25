# Por qué de cada regla

El porqué de las reglas de la skill que citan una decisión de la SF, en el orden de sus secciones. Cada entrada cita la decisión con su título y su número entre paréntesis.

## Estilo del proyecto e incrustarla en un documento

- **Del mismo proyecto que sus documentos** («La infografía técnica se puede incrustar como cualquier recurso o ir como pieza aparte», 315): puede ir incrustada en un documento, como cualquier recurso del catálogo, o aparte y enlazada; en las dos toma el estilo del proyecto.
- **Sin `estilo.json`, los valores por defecto de un tema** («Un proyecto sin estilo.json se genera con los valores por defecto de un tema elegido por su color», 323): fijar el estilo no bloquea nada; se usa el tema más cercano al color del proyecto y se avisa, como hace el generador de documentos.

## Skills de apoyo (three.js y GSAP)

- **Las skills externas, como dependencias del plugin** («Skills externas: tal cual, como dependencias; adaptadas, como propias», 175): antes viajaban en el plugin copias enteras, que no se actualizaban, no decían de dónde venían y pesaban en el contexto aunque no se usaran. Una skill externa que se usa tal cual se declara como dependencia; solo viaja en el plugin una adaptada, con su origen y lo que cambia.
- **Fijadas a su commit en el marketplace de la SF** («Todas las skills externas actuales, como dependencias», 176): un plugin solo puede depender de otros plugins, y no todas las skills externas lo eran. Con una entrada en el marketplace de la SF, fijada a su commit, instalar `sf` las trae sin añadir antes ningún catálogo ajeno.
