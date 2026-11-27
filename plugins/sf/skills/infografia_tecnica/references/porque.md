# Por qué de cada regla

El porqué de las reglas de la skill que citan una decisión de la SF, en el orden de sus secciones. Cada entrada cita la decisión con su título y su número entre paréntesis.

## Estilo del proyecto e incrustarla en un documento

- **Del mismo proyecto que sus documentos** («La infografía técnica se puede incrustar como cualquier recurso o ir como pieza aparte», 315): puede ir incrustada en un documento, como cualquier recurso del catálogo, o aparte y enlazada; en las dos toma el estilo del proyecto.
- **Sin `estilo.json`, los valores por defecto de un tema** («Un proyecto sin estilo.json se genera con los valores por defecto de un tema elegido por su color», 323): fijar el estilo no bloquea nada; se usa el tema más cercano al color del proyecto y se avisa, como hace el generador de documentos.

## Skills de apoyo (three.js y GSAP)

- **Las skills externas, como dependencias del plugin** («Skills externas: tal cual, como dependencias; adaptadas, como propias», 175): antes viajaban en el plugin copias enteras, que no se actualizaban, no decían de dónde venían y pesaban en el contexto aunque no se usaran. Una skill externa que se usa tal cual se declara como dependencia; solo viaja en el plugin una adaptada, con su origen y lo que cambia.
- **Fijadas a su commit en el marketplace de la SF** («Todas las skills externas actuales, como dependencias», 176): un plugin solo puede depender de otros plugins, y no todas las skills externas lo eran. Con una entrada en el marketplace de la SF, fijada a su commit, instalar `sf` las trae sin añadir antes ningún catálogo ajeno.

## Flujo de trabajo

- **Los puntos clave, antes de dibujar** («Antes de una representación gráfica, decidir los puntos clave que transmite», 385): un esquema y una infografía de «Cómo funciona» se dibujaron sin fijar qué decir y no representaban la esencia (separaban como ajeno lo que la SF añade al proyecto y no distinguían lo local). Con la lista fijada antes, el dibujo la sirve y se comprueba contra ella. Por eso la lista incluye los módulos clave y sus interconexiones: lo que faltaba o sobraba en esos dibujos eran piezas y relaciones, y se ve comparando el dibujo con ellos. **Salen de la realidad, no de suposiciones**: en un esquema de «Cómo funciona la SF» se dibujó el repositorio como original y la carpeta local como copia, cuando Claude trabaja siempre en local y luego hace commit y push; por eso se verifica en el código, los documentos o la práctica, y si no se puede, se pregunta antes de dibujar. **Entender antes de dibujar**: sin entender el concepto, el dibujo tiene las piezas pero no el valor; por eso se explica primero en dos o tres frases llanas y se comprueba que el dibujo lo transmite. **Criterio, no solo dibujo** («Las skills gráficas entienden lo que representan y aportan criterio», 387): una representación solo aporta valor si refleja cómo funciona de verdad lo representado, y dibujar sin entender exigió varias correcciones del propietario. Por eso la skill actúa como un agente con criterio, no como un dibujante que ejecuta. Además aporta intención: un gráfico correcto que no sirve a lo que el lector tiene que entender o decidir en ese punto no vale, y se comprueba contra ese objetivo.
