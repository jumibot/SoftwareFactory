# kit_documentos · origen

Biblioteca de herramientas de los documentos HTML de la SF. La usan todos los documentos: los del generador común de la skill `crear_documentos` (fundacional, informes) y los de la maqueta de `documento_vision`, que la buscan en `tools/kit_documentos/` junto a `skills/`. Desde el 2026-10-27 viaja dentro del plugin `sf` (`plugins/sf/tools/kit_documentos/`) y ya no se copia a `~/.claude/tools/`.

## Qué contiene

- `herramientas.js`: columna de herramientas (anclada, despegable, de ancho ajustable), buscador, notas personales, barra del documento con versión y «Guardar» (copia aparte o el mismo archivo) y aviso al cerrar. Lleva `VERSION`, que se sube al cambiar cualquier archivo de la biblioteca.
- `lectura.js`: herramienta «Lectura» y opciones de lectura: modo oscuro, un solo bloque abierto, título fijo, bocadillo de las fuentes, subapartados en bocadillo, anchos de tabla y leyenda.
- `edicion.js`: edición de párrafos en su sitio, con trazabilidad, y párrafos añadidos desde una nota.
- `herramientas.css`: el estilo de todo lo anterior, con las variables del tema.
- `extraer_notas.py`: las notas y los párrafos cambiados de una copia guardada, en Markdown.
- `actualizar_copia.py`: pone al día el código de una copia ya repartida sin tocar su contenido.

El catálogo, con los valores iniciales según el destino del documento (proyecto o usuario), está en `skills/crear_documentos/scripts/tema_identidad.py` (`HERRAMIENTAS`), y se explica en `skills/crear_documentos/SKILL.md` («Herramientas y opciones de lectura»).

## Historia

- **2026-10-26.** La columna nació en `documento_fundacional` con el modelo de los 20 casos de referencia de OncoCore (`tools/dev/kit_documentos`, v1.0.57). Después se compartió con `documento_vision`, desde `documento_vision/assets/`. Luego se le añadieron las notas, la versión, las ventajas de más impacto del kit de OncoCore (herramientas 1.1.0) y el catálogo de opciones.
- **2026-10-26, herramientas 1.2.0.** El propietario pidió «aplica todas las opciones de oncocore pendientes, con valores iniciales en cada caso que puedes proponer tu con lógica de si es mejor o no y dejar ajustar», y que la biblioteca estuviera «dentro de una carpeta de tools». Se portaron:
  - anchos de tabla (ANCHOS_JS);
  - un solo bloque abierto (ACORDEON_JS);
  - título fijo (FIJO_JS, solo la parte del título);
  - bocadillo de la fuente y resaltado (FUENTE_JS y RESALTA_JS, adaptados a las referencias `[E1]`);
  - edición del párrafo y nota convertida en párrafo (_EDICION_JS y _PARRAFOS_JS, sin las etiquetas clínicas);
  - guardar sobre el mismo archivo y aviso al cerrar (NOTAS_JS);
  - actualizador de copias (Actualizador);
  - la leyenda, el modo oscuro y los subapartados en bocadillo, que son nuevos.

  Lo que el lector ajusta se recuerda por documento; la elección del autor es el punto de partida.
- **No se porta, porque es propio de OncoCore:** selectores clínicos, escala lavanda, plantillas de URL clínicas (CIMA, BIFIMED, OncoKB, PubMed) y el enunciado fijo del caso.
- **Probado en Edge con un fundacional y una visión de SmartColdBox, con todas las opciones activas:**
  - bocadillo y resaltado;
  - título fijo, en claro y en oscuro;
  - acordeón;
  - edición, con «Modificado»;
  - nota convertida en párrafo, con «Retirar»;
  - modo oscuro;
  - copia guardada, limpia y con los cambios;
  - `extraer_notas.py` con los párrafos y `actualizar_copia.py --comprobar`;
  - anchos de tabla;
  - subapartados en bocadillo;
  - móvil a 390 px sin desplazamiento horizontal;
  - sin errores de página.
- **Limitación conocida:** durante un desplazamiento suave, el título fijo puede ir un instante por detrás del texto, porque se coloca desde JavaScript.

## 1.2.1 · Espacio duro en el buscador (2026-10-26)

El buscador trata el espacio duro (U+00A0) y el fino (U+202F) como un espacio, para encontrar «35 °C» escrito con un espacio normal en los documentos que separan la cifra de su unidad con espacio duro (regla tipográfica de las guías de interfaz de Vercel, aplicada en `documento_fundacional`). La correspondencia carácter a carácter con el texto no cambia.

## 1.2.2 · Modo del sistema por defecto (2026-10-26)

El propietario pidió «por defecto el modo del sistema». El documento parte del modo claro u oscuro del sistema del lector; la opción `oscuro` del autor lo fuerza a empezar en oscuro, y el lector sigue eligiendo claro, oscuro o el del sistema, que se recuerda por documento.

## 1.3.0 · Clases de nota (2026-10-26)

El propietario pidió «más opciones de las tools de documentos, en cuanto a la anotación, que pueda haber una nota global o una por sección según se decida». Las notas pasan a tres clases que el autor activa por separado: `nota-texto` («Anotar» sobre un texto), `nota-seccion` (una por sección: el botón abre la existente en lugar de crear otra) y `nota-global` (una de todo el documento, primera del panel y de `extraer_notas.py`). La nota general no se convierte en párrafo, porque no tiene sitio en el texto. Las copias anteriores, que no nombran ninguna clase, siguen con todas, y sus notas de sección múltiples se conservan.

## 1.3.1 · Convertir una nota en párrafo, como opción propia (2026-10-26)

El propietario recordó «otra opcionalidad a considerar (ya usada en oncocore) es la posibilidad de permitir convertir notas en párrafos». Existía desde la 1.2.0 (_PARRAFOS_JS de OncoCore), pero solo con `edicion`. Ahora es `nota-a-parrafo`, independiente: sin `edicion`, el párrafo añadido lleva «Añadido · fecha» y «Retirar», sin lápiz. Los documentos anteriores a la 1.3.0 que tenían `edicion` la conservan.

## 1.4.0 · Notas como en gene_associations (2026-10-26)

El propietario señaló, con una captura del panel de la 1.3.1: «mira cómo se manejan varias notas en gen_associations, que no es exactamente como ha quedado aquí implementado». Se adopta el modelo de COLUMNA_JS de OncoCore: sin botones «Nota general» ni «Nota en…»; la columna muestra sola la tarjeta de la sección en foco y las de las secciones que la contienen, con su cabecera y plegada si está vacía, que se despliega al tener texto; lo escrito se ve también, solo para leer, al final de su sección (el «espejo»), y pulsarlo lleva a la nota. Se conservan las ventajas propias: la nota general (siempre arriba), los comentarios sobre un texto («Anotar»), que van en la tarjeta de su sección, y un resumen «Todas las notas (N)» que lleva a cada una, que OncoCore no tiene. El espejo no entra en el buscador, en la impresión ni en la copia guardada. Probado en Edge con SMB VIAL: tarjetas al cambiar de sección, espejo, nota general, «Anotar», resumen, recarga y móvil, sin errores.

## 1.4.1 · Cada nota, su propia tarjeta (2026-10-26)

Con una captura del panel de la 1.4.0, el propietario: «pero así no es como está en gen associations». En OncoCore (`.notas-tools.por-seccion`) no hay panel común: cada nota es una herramienta de la columna, con el aspecto del buscador. Ahora, en la columna, el panel «Notas» es transparente y sin cabecera; la nota general, la de cada sección en foco y «Tus notas» (el nombre y el resumen, plegada) son tarjetas con franja, título en versalitas y flecha. La nota de sección lleva un área de texto amplia y solo «Convertir en párrafo», desactivado mientras está vacía; los comentarios sobre un texto conservan su fecha y «Borrar». En la ventana flotante y en el móvil, las tarjetas van dentro del panel «Notas». Probado en Edge en claro y en oscuro, y a 900 px.

## 1.4.2 · Guardar en la columna y tamaño de las notas (2026-10-26)

Con una captura de la barra en el menú, el propietario: «esto no está así en gen association», y «revisa cómo se ajusta el tamaño de las notas en la side toolbar». Como en OncoCore (`#columna-tools .barra-doc`), con la columna la barra es su primera tarjeta: versión y «kit v…» apilados, el estado («Sin cambios pendientes», «● Hay cambios sin guardar» o «Guardado el…») y «Guardar documento con notas». Sin columna vuelve al menú. La columna es una pila de toda la altura: el panel de notas ocupa lo que dejan las demás herramientas y cada nota abierta se reparte ese alto con las otras (flex 1 1 0), entre 12em y el 60 % de la pantalla; su texto llena la tarjeta, sin asa para estirarla. Las plegadas solo ocupan su cabecera.

## 1.4.3 · «Guardar» (2026-10-26)

El propietario: «será suficiente "Guardar"». El botón dice solo «Guardar»; su ayuda explica qué guarda.

## 1.4.4 · Sin hueco con las notas plegadas (2026-10-26)

El panel de notas solo crece cuando hay una nota abierta; con todas plegadas, «Lectura» queda justo debajo.

## 1.4.5 · Led rojo en «Guardar» (2026-10-27)

El propietario, sobre «● Hay cambios sin guardar»: «creo que esto lo podemos substituir por el "led rojo" en el propio botón de guardar». Con cambios pendientes, el botón lleva un punto rojo luminoso en la esquina y el texto de estado se oculta a la vista (lo siguen leyendo los lectores de pantalla y el botón dice «Guardar: hay cambios sin guardar»). Los demás estados («Sin cambios pendientes», «Guardado el…») se mantienen.

## 1.4.6 · Las notas vacías no son cambios (2026-10-27)

El propietario: «¿porqué está rojo si no he puesto ninguna nota?». Una nota escrita y borrada se quedaba guardada vacía si la página se recargaba sin salir del campo, y encendía el led. Ahora una nota sin texto ni cita no cuenta como cambio y se descarta al cargar.

## 1.5.0 · «Lectura» pasa a un modal (2026-10-27)

Con una captura de la tarjeta «Lectura», el propietario: «esto es pura configuración conviértelo en un modal que se abrirá con un icono de engranaje a la izquierda del botón de guardar». Ya no es una herramienta de la columna: el engranaje, junto a «Guardar» (o en el menú si no hay barra), abre un modal con el modo y las demás preferencias. Se cierra con ✕, con Esc o pulsando fuera, y el foco no sale de él mientras está abierto. Es una capa propia y no un <dialog>, para que el modo oscuro también la invierta. No se imprime ni entra en la copia guardada.

## 1.5.1 · Engranaje sin caja (2026-10-27)

El propietario, con el engranaje en medio de la barra: «feo. Que no tenga bg y borde solo el engranaje y alinéalo a izq o derecha». Ahora es solo el icono, sin fondo ni borde, y queda pegado a la izquierda de «Guardar» también cuando el texto de estado se oculta.

## 1.6.0 · «Plegar todo» e «Imprimir» en la barra (2026-10-27)

Con una captura de los dos botones del menú, el propietario: «esto a la toolbar a la izq del botón guardar». Con la columna, la barra lleva tres iconos sin caja a la izquierda de «Guardar»: plegar o desplegar todo (cambia de icono y de rótulo), imprimir y el engranaje de «Lectura». Son atajos a los botones del menú, que se ocultan; si el menú se queda sin nada visible, se oculta entero. Sin columna, el menú sigue como antes. En la columna, el texto de estado («Sin cambios pendientes», «Guardado el…») ya no ocupa sitio: está en el rótulo emergente de «Guardar» y, con cambios, en su led.

## 1.6.1 · El modo no se pisa en el modal (2026-10-27)

El propietario: «el desplegable de modo se está pisando un poco». Al abrir, el foco iba al desplegable y su contorno de foco chocaba con el botón de cerrar. Ahora el foco va a la caja del modal, hay más aire bajo la cabecera y el contorno de foco es más fino.

## 1.6.2 · La versión pasa al modal de configuración (2026-10-27)

En pantallas estrechas, «Guardar» bajaba a otra línea y el engranaje quedaba solo a la derecha. El propietario pidió: «la versión y el kit pasalos al modal de configuración». Con «Lectura», la versión del documento y la del kit van al pie del modal; la barra queda con el estado, los iconos y «Guardar», y cabe en una línea en el móvil. Sin «Lectura», la versión sigue en la barra. Después pidió «el engranaje alineado a la izq, separado de los botones»: el engranaje abre la barra por la izquierda y los iconos y «Guardar» quedan a la derecha.

## 1.7.0 · Una chincheta para toda la barra (2026-10-27)

Con una captura de la chincheta en la cabecera del buscador, el propietario: «esto debería estar justo a la derecha del engranaje: es un control para toda la toolbar, no solo para la búsqueda». Las herramientas ya no llevan chincheta cada una. Hay una sola, en la barra del documento y justo a la derecha del engranaje (sin engranaje, abre la barra; sin barra, va junto a los botones del menú). Ancla todas las herramientas en la columna o las despega todas como ventanas flotantes, cada una donde estaba. Anclada, en el color primario; despegada, inclinada. En pantalla pequeña no aparece, porque no hay columna.

## 1.7.1 · La barra siempre arriba (2026-10-27)

El propietario preguntó cómo devolver las herramientas a la columna tras despegarlas: con la misma chincheta, que sin columna va en la barra, arriba. Pero en los documentos sin línea de estado (desde la 0.7.1 del plugin, sin franja bajo la cabecera) la barra acababa al final de la página. Ahora, si no hay menú ni franja, se crea una franja bajo la cabecera para la barra; no viaja en la copia guardada.

## 1.8.0 · Sin columna, cada nota en su sitio (2026-10-27)

El propietario pidió revisar «en los docs de oncocore cómo funciona lo de las notas cuando no está la sidebar» y, ante la propuesta, «copia todo lo de oncocore sobre la tool». Como en el informe de los 20 casos y en gene_associations de OncoCore, sin columna (herramientas despegadas o pantalla de menos de 1400 px) la ventana «Notas» desaparece y cada nota vuelve a su sitio: una tarjeta editable al final de su sección («Nota · <sección>», plegada si está vacía, con los comentarios de «Anotar» de esa sección), y la nota general y «Tus notas» al principio del documento. No hay espejo, porque la nota ya está en su sitio. Al volver a anclar, todo vuelve a la columna. Las tarjetas no entran en el buscador, en la edición, en la impresión ni en la copia guardada. Probado en Chrome a 900 y a 1600 px, sin errores en la consola; la escritura y «Anotar» sin columna están pendientes de probar a mano.

## 1.8.1 · Notas en su sitio, discretas (2026-10-27)

Con capturas del informe de casos y de gene_associations, el propietario: «en oncocore las notas son mucho menos invasivas». Como allí, la nota en su sitio no es una tarjeta: un rótulo pequeño en versalitas («Nota · <sección>»), el campo de texto abierto, de unas tres líneas, y «Convertir en párrafo» como botón claro a la derecha. Sin caja, sin franja de color y sin plegado. «Tus notas», al principio, sigue plegable pero sin caja.

## 1.9.0 · Siempre en claro; destino y herramientas, obligatorios (2026-11-01)

Tarea 204. El documento abre siempre en modo claro; el lector elige oscuro o el del sistema en «Lectura», y solo se recuerda el modo que eligió allí (hasta la 1.8 se guardaba «sistema» sin elegirlo). La opción `oscuro` del autor se retira: en documentos antiguos se ignora con un aviso. El generador (`tema_identidad.py`) ya no usa valores del proyecto en silencio: sin `destino` o sin `herramientas` se detiene y enseña las opciones y el catálogo; `herramientas: recomendadas` toma las del destino. Los dos se pueden pasar también con `--destino` y `--herramientas`.

## 1.9.1 · Las piezas comunes, a crear_documentos (2026-11-02)

Tarea 301. El generador común, la hoja de estilo, `plegado.js`, `fichas.js`, los temas, `tema_identidad.py` y `resaltar_codigo.py` pasan de `documento_fundacional` a la skill `crear_documentos` (`estilo_fundacional.css` → `assets/estilo_documento.css`). `actualizar_copia.py` conoce las rutas nuevas y lleva las viejas a ellas al poner al día una copia ya repartida. La biblioteca no cambia de comportamiento.

## 1.9.2 · Comentarios sin nombres de proyectos (2026-11-02)

Tarea 317. Los comentarios de `herramientas.js`, `herramientas.css`, `lectura.js`, `edicion.js` y `actualizar_copia.py` ya no nombran el proyecto de origen: remiten a este archivo, que desde esta tarea vive en el repositorio y no en el plugin. El código no cambia.
