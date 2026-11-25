---
name: fijar_estilo
user-invocable: false
description: Fija y afina el estilo de los documentos de un proyecto (docs/identidad/estilo.json) sin escribir CSS — pregunta al desarrollador por su estilo, le enseña muestras hechas por el generador único de crear_documentos, prueba los cambios fuera de estilo.json hasta que los acepta, y en cada afinado respalda la versión anterior en _respaldo/, sube la versión y anota el historial. No maqueta. Si lo que se pide es un fallo del generador, propone arreglarlo; si es un parámetro que no existe, propone «Añadir al generador el parámetro …» (en la SF, como tarea; en otro proyecto, ofreciendo una issue en GitHub de la SF). Úsala la primera vez que un proyecto necesita documentos o cuando el generador avisa de que no tiene estilo, desde la incorporación o /sf_config, y cuando pidan cambiar el aspecto de los documentos (colores, letra, portada, cabeceras de sección, logo, esquinas, código, pie, filetes de separación y de los recuadros), elegir el estilo con muestras o ver el catálogo de temas en claro y en oscuro.
---

# Fijar el estilo de los documentos

El aspecto de los documentos es del proyecto, no de cada documento: lo guarda `docs/identidad/estilo.json` y lo aplica el generador único de `crear_documentos` a todos (decisiones 305 y 316 a 323). Esta skill es **la única que escribe `estilo.json`**. No maqueta ni toca el generador: elige valores de su catálogo, enseña con él cómo quedan y los guarda cuando el desarrollador los acepta. Qué significa cada parámetro y su valor por defecto, en `crear_documentos` («Estilo del proyecto»).

**Fijar el estilo no bloquea nada** (323): sin `estilo.json`, el generador sale del paso con los valores por defecto de un tema y avisa. Esta skill se ofrece, no se impone. El porqué de cada regla, en [references/porque.md](references/porque.md); se lee solo si hace falta.

## Herramienta

`scripts/estilo.py` de esta skill (`python -I -X utf8 <skill>/scripts/estilo.py <orden>`, desde la carpeta del proyecto o con `--raiz`). Lo que dice el estilo se lee con la herramienta, no se infiere:

| Orden | Qué hace |
| --- | --- |
| `parametros` | El catálogo del generador: grupos, parámetros, valores posibles y por defecto. Es la lista de lo que el generador sabe hacer. |
| `ver` | El estilo del proyecto (versión, origen, historial) y lo que está en prueba: todo lo cambiado frente a su tema de partida y, si el proyecto ya tiene estilo, frente a él, y lo que no pasa el contraste. |
| `partir <tema\|muestra\|juego.json> [grupo.clave=valor …]` | Pone en prueba un estilo **completo**: todos los valores resueltos desde un tema del catálogo de `crear_documentos`, una muestra del plugin por su nombre (`sereno`, `tecnico`…) (o un juego, un `estilo.json` completo), con el tema como `origen` (317). |
| `cambiar grupo.clave=valor …` | Cambia valores de la prueba; sin prueba, parte del estilo actual. `grupo.clave=` vuelve al valor por defecto. `nombre=Áureo` da nombre al estilo (`nombre=` lo quita). Se valida con el catálogo. Un `colores.primario` nuevo (también en `partir`) recalcula su familia (abajo). Enseña el último cambio y, como `ver`, todo lo cambiado. |
| `muestras <doc>.md [prueba\|actual\|tema\|juego …] [--perfil …]` | Genera el mismo documento con cada estilo, como `<doc>.muestra-<nombre>.html` junto a él. Si una no se puede rehacer (el generador se detiene), la anterior con su nombre se borra, porque ya no dice lo que hay en prueba. |
| `aceptar --motivo "…" [--cambio "…"]` | Lleva la prueba a `estilo.json`: respalda la versión anterior en `_respaldo/estilo_v<N>.json`, sube la versión y anota el historial (322). Borra la prueba y sus muestras. |
| `descartar` | Borra la prueba y sus muestras sin tocar `estilo.json`. |
| `catalogo [--salida carpeta]` | El catálogo para elegir el estilo de partida: las seis muestras del plugin y una séptima del proyecto (abajo) generan el mismo documento de muestra (`assets/catalogo/muestra.md`: portada, botones, recuadros, tabla, decisión, diagrama, tarjetas, pregunta, código y cifra) con su estilo resuelto, como `partir`, y `catalogo-temas.html` lo enseña en tres vistas, en claro y en oscuro (el de «Lectura», con `?modo=oscuro`), con una tabla de las muestras y su contraste. Las miniaturas son las propias muestras del generador en un marco reducido; un clic abre cada una. Un tema sin el contraste suficiente se enseña igual (el generador solo avisa, con su opción interna `--contraste-avisa`), con su aviso. **Es un activo del proyecto y se versiona** (decisión 352): sale dentro de él, en `<identidad>/catalogo-temas/` (`--salida` fuera del proyecto se rechaza), entra en el commit con sus muestras y se rehace cuando cambian los temas o el generador. No toca el estilo ni la prueba. Su aspecto es el estilo del proyecto (decisión 353), con las secciones abiertas; sin `estilo.json`, el tema por defecto. |

**Lo que se prueba no toca `estilo.json`.** Va en `docs/identidad/estilo.prueba.json`, junto a él (así valen las rutas del logo), hasta que el desarrollador lo acepta. Ni la prueba ni las muestras se suben a git: se aceptan o se descartan antes de acabar. Las muestras no se guardan; como el generador es determinista, se rehacen con el estilo y el documento.

**Un primario nuevo trae su familia** (decisión 338). Al cambiar `colores.primario`, la herramienta recalcula, con la mezcla de `tema_identidad.py`, el vivo, el fondo y el tenue; la `cabecera` de la portada destacada y su texto, apagada para que no deslumbre (351); el `primario-texto`, oscurecido lo justo para leerse a 4,5:1 sobre la página, el blanco y el fondo; el acento con su fondo y su borde, si el acento era el primario (si el tema tiene un acento propio, se queda), y en oscuro, la familia entera vuelve a derivarse de la clara (decisiones 347 y 348): el primario aclarado lo justo para leerse sobre la página oscura, las superficies y su fondo, su vivo, fondo y tenue, su `primario-texto` y su `sobre-primario` (blanco o la tinta de la página, el de más contraste). Lo que se pide en el mismo cambio no se toca: `cambiar colores.primario=#f5c400 colores.sobre-primario=#1a1a1a` deja el texto sobre el primario como se pide. `sobre-primario` no es de la familia en claro: con un primario claro hay que pedirlo (319), y el contraste lo avisa. **El contraste se comprueba en claro y en oscuro**, con el mismo aviso; lo del oscuro empieza por «en oscuro». Un estilo guarda su paleta oscura completa (`colores.colores-oscuro`, 317), con lo que su tema no daba derivado de la clara (348).

## Procedimiento

1. **Lo que hay.** `ver`. Si el proyecto tiene `identidad.json`, sus colores y su logo; si no tiene estilo, el tema que el generador usa ahora por su color (323).
2. **Cómo lo quiere.** Una pregunta corta con opciones: el carácter (sobrio, editorial, desenfadado, técnico, institucional) y si hay color o logo de marca. Si el proyecto tiene marca (una web, un logo), sus colores pasados a `#rrggbb`; un primario claro, como un amarillo, lleva `sobre-primario` y `primario-texto` (319).
3. **Muestras para elegir.** Se ofrece el catálogo de temas (`catalogo`), con su ruta, para ver todos en claro y en oscuro de un vistazo. Después, `muestras <doc>.md <origen> <origen> …` con los orígenes que encajan con la respuesta, y se enseñan las páginas lado a lado (escritorio y móvil). Cada muestra dice su origen y su carácter en una línea; las que no pasan el contraste se dicen como tales y no se ofrecen sin arreglo.
4. **Partir.** Con la que elige: `partir <origen>` y sus colores de marca si los hay (`partir tinta colores.primario=#… colores.sobre-primario=#…`).
5. **Afinar en vueltas.** Cada petición del desarrollador («los títulos de sección más visibles», «esquinas más rectas», «quita las líneas de decoración»: `portada.linea`, `pagina.filetes`, `recuadros.filete` y `secciones.etiqueta`) se traduce a parámetros con `parametros`, se prueba con `cambiar`, se enseña con `muestras <doc>.md actual prueba` y se pregunta si se queda. Si no, otra vuelta.
6. **Aceptar.** Con su OK, `aceptar --motivo "…"`: una línea de historial con qué cambia y por qué. El primer `aceptar` crea la versión 1, con el cambio «estilo de partida desde <tema>» (y lo cambiado frente a él); el motivo dice por qué se eligió, no lo repite. Después se regeneran los documentos que se vayan a tocar (309): no se regeneran todos de golpe sin pedirlo. El commit lleva `estilo.json` y su respaldo.

**Las muestras del plugin** (decisión 335, 6 y 7) están en `assets/juegos/`: una por tema del catálogo, cada una con una forma propia para que se distingan a primera vista y no solo por el color — A `sereno` (morado), B `desenfadado` (colorido), C `tecnico` (pool), D `institucional` (rojo), E `sobrio` (teal) y F `editorial` (tinta). Cada archivo dice su tema (`origen`), su carácter y sus cambios sobre él; `partir <nombre>` lo resuelve entero. La séptima, G, es el estilo del proyecto tal cual (su `estilo.json` entero: portada, cabecera, logos y lo afinado), marcada como el estilo actual y titulada con su `nombre` si lo tiene («G · Áureo (estilo del proyecto, v3)»); sin `estilo.json`, es `tinta` con el color del proyecto (el del tema de su `identidad.json` o su color de sesión) y su texto encima derivado. El marco de las miniaturas (960 × 600) cabe la portada entera de cada muestra. El documento de muestra corto, con todos los recursos, es `assets/catalogo/muestra.md`.

El documento de las muestras de `muestras` es, por ahora, uno real del proyecto (el que se va a generar o el más completo); si no hay ninguno, el de ejemplo de `diagramas` (`../diagramas/assets/ejemplo-documento.md`), copiado antes al proyecto con su carpeta `ejemplos/`. Las muestras salen junto al documento, que tiene que estar dentro del proyecto; la lista de las hechas (`estilo.prueba.muestras`) guarda sus rutas relativas al proyecto, y aceptar o descartar no borra nada fuera de él.

## Lo que el generador no sabe hacer

Antes de cambiar nada, cada petición se mira contra el catálogo (`parametros`):

- **Lo sabe hacer:** se prueba con sus valores (paso 5).
- **Es un fallo del generador** (un texto que no se lee, un enlace ilegible, un hueco que falta): se arregla el generador, sin parámetro nuevo. En la SF, es una tarea de implementar; en otro proyecto, se dice en una línea y se ofrece la issue (abajo).
- **Es una preferencia que no tiene parámetro:** se propone «Añadir al generador el parámetro …», con lo que pidió el desarrollador y los valores que tendría. Nunca una excepción en el proyecto (CSS propio para el aspecto, `portada` o `tema` en un `.md`): el aspecto lo fija solo el estilo (318). Mientras tanto, el documento sigue con lo que el generador ya sabe hacer.

Dónde va la propuesta:

- **En la SF** (el repositorio de la propia Software Factory): una tarea de implementar «Añadir al generador el parámetro …» en su cola, bajo la tarea permanente **Mejorar la Software Factory** (la cola, con `sf:flujo_tareas`).
- **En otro proyecto** (decisión 324): el desarrollador solo tiene el plugin. Se dice en una línea que es de la SF y se ofrece abrir una issue en su repositorio de GitHub; no se anota en el estilo del proyecto. Con su OK, y enseñándole antes el texto:

  ```
  gh issue create --repo jumibot/SoftwareFactory --title "Estilo: añadir al generador el parámetro <grupo.clave>" --body "<qué se pide, para qué y los valores que tendría>"
  ```

  El cuerpo dice lo que se pide en general, sin datos del proyecto que el desarrollador no quiera publicar (el repositorio de la SF es público). Sin `gh` o sin sesión, se le da el texto para abrirla a mano.

## Al acabar

- `ver` no deja nada en prueba (aceptado o descartado).
- El generador pasa sin errores de contraste con el estilo nuevo; los avisos de bordes se dicen, no se arreglan aquí.
- El documento regenerado se mira en escritorio y en móvil, como dice `crear_documentos` («Comprobación»).
