---
antetitulo: Software Factory · Informe de investigación · Noviembre 2026
lema: Un estilo por proyecto, no por documento; // un generador único que maqueta, y una skill que fija su estilo con muestras.
subtitulo: Qué skills producen documentos HTML y con qué maqueta, qué documentos salieron de cada generador y cómo llegar a una base común de maquetación con el tema del proyecto, también en los diagramas.
version: Versión 1.8 · 06/11/2026
estado: Sin preguntas abiertas · Tarea 385
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de investigación
pie: Informe de la tarea «Que cada proyecto tenga un solo estilo de documentos: una base común de maquetación para todas las skills de documentos» (385). Parte de las skills de documentos del plugin en develop, del kit de documentos, de la cola y las decisiones afines, de la rama de «Cómo funcionan los estados» y de los documentos HTML de la SF y de los proyectos del propietario. Decidido por el propietario de la Software Factory (decisiones 305 a 313).
---
# Un estilo de documentos por proyecto: un generador único con el estilo del proyecto

## Resumen | Un generador único y el estilo del proyecto | Resumen {#resumen}

Un proyecto tiene hoy dos estilos de documento porque la SF tiene **dos generadores con dos maquetas**, y cada skill de tipo usa uno. Comparten temas, identidad y kit, pero cada uno tiene lo que al otro le falta: por eso «Cómo funcionan los estados» cambió de aspecto al pasarse al común para tener diagramas. Pulsa cada pieza para ver su ficha.

![](diagramas/estilo-hoy.diagrama)

El propietario de la Software Factory ha decidido las diez preguntas (decisiones 305 a 315). **Un solo generador de documentos, determinista**, maqueta todos los documentos con los parámetros del estilo del proyecto. **Una skill ayuda a fijar esos parámetros**: el desarrollador elige entre varias muestras, hechas por el generador, la primera vez que necesita documentos, y los afina con el uso. La skill no maqueta, y el generador gana parámetros con el uso: lo que un afinado pida y no sepa hacer se le añade como parámetro nuevo, no como excepción en un documento. En la SF, el estilo de partida es el de este informe. Los diagramas y el color de sesión salen de ese estilo, todos los recursos de la visión pasan al catálogo común y cada documento se migra cuando se vuelve a tocar ([Migración](#migracion)).

![](diagramas/estilo-propuesta.diagrama)

Salen **nueve tareas nuevas**, dos de diseño y siete de implementar, una para que la infografía técnica tome también el estilo y otra para la web comercial. Cambian cinco tareas de la cola. **Las diez preguntas están decididas** (decisiones 305 a 315): el diagrama es un recurso del catálogo, y la infografía técnica puede ir incrustada como recurso o aparte.

[Ver las tareas que salen](#tareas){: .salto} [Ver la infografía](#infografia){: .salto}

## Skills | Lo que se duplica y lo que se pierde | Skills {#skills}

El detalle de cada skill y cada generador está en las fichas del primer diagrama. Además de las del diagrama, `infografia_tecnica` da una página three.js propia, sin kit ni identidad; también tomará el estilo del proyecto ([La infografía técnica](#infografia)). Dos herramientas generan HTML con el generador de la visión: `tools/indice_decisiones.py` (el índice de decisiones) y `scripts/readme_a_html.py` (`DESARROLLO.html`).

Los dos generadores repiten la lectura de la identidad y de las opciones, el logo, los enlaces externos, la procedencia, las tablas en fichas para el móvil y el arranque del kit, cada uno a su manera. Lo grave no es la repetición sino **lo que cada uno no tiene**. El común no colorea el código, aunque lo pide para todo documento la decisión «Forma de los documentos: texto literal, tarjetas, color con significado y código coloreado» (28). Los proyectos ya lo parchean: SpriteAnimation lleva en su identidad un `codigo.css` («el kit solo da estilo al código en línea») y un `cabecera.css` con reglas para las dos cabeceras, una por maqueta.

> **El tema de los diagramas, resuelto**
> Con `--tema ""` el fragmento sale sin `data-d-tema` y toma los colores y la letra del documento, como los dos de este informe. La mejora de la skill de diagramas (386, cerrada en develop) resolvió los tres flecos: «Por defecto» vuelve al tema de la figura, el fondo «Claro» es el papel del documento y los rótulos llegan a 4,5:1 con cualquier tema. Los dos diagramas de este informe están regenerados con esa versión, y el comprobador ya no da el error de contraste del tema azul (`texto-tenue` `#9ca3af`, 2,54:1). Queda solo un aviso, no un error: el borde de las cajas da 2,43:1 frente a 3:1, y es del tema, para la tarea del estilo de partida.


## Documentos | Qué salió de cada generador | Documentos {#documentos}

En la SF, **diecisiete HTML salen del generador de la visión y cinco del común**; otros seis informes solo tienen `.md`. El reparto no sigue el tipo de documento sino la fecha: los fundacionales y los informes anteriores al generador común (la decisión «Una skill general de diseño de documentos», 232) siguen con la maqueta de la visión.

| Documentos de la SF | Generador | Nota |
| --- | --- | --- |
| «Cómo funciona la SF», «Cómo funciona el panel», «Cómo funcionan los estados» y «Mejora continua» (`docs/`) | Visión | Los estados pasan al común en su rama, con portada compacta y diagramas en `tinta` |
| Visiones y fundacionales de `docs/specs/vision/` (seis) | Visión | Los dos fundacionales son anteriores al generador común |
| Informes «Configuración inicial», «Fricciones humanas», «Incorporar sin cambiar el proyecto», «Recursos para la SF» y «Trabajo con la SF y sin ella» | Visión | Informes cerrados, de antes del formato de fichas |
| Informes «Liberar al agente principal», «Primeros cinco minutos», «Sprints con objetivo» y «Tipos de tarea» | Común | Con el perfil del informe |
| `DESARROLLO.html` y `docs/decisiones/README.html` | Visión | Los generan `readme_a_html.py` e `indice_decisiones.py` |
| Ejemplo de la skill de diagramas | Común | Diagramas con `tinta` sobre el tema de la SF |

En los demás proyectos del propietario, leídos sin cambiarlos, pasa lo mismo:

| Proyecto | Documentos | Generador |
| --- | --- | --- |
| SpriteAnimation (tema `pool`) | Fundacional y «Estructura de la demo» con el común; visión, «Interfaces del MVP» e índice de decisiones con la visión | Los dos, y CSS propio para cada maqueta |
| SmartColdBox (`pool`) | Visión y fundacional | Visión |
| LecturaFàcil (`rojo`), MedRol y SocratIX (`morado`) | Visión o valoración | Visión, MedRol y SocratIX de antes del kit |
| PoseTracker | Índice de decisiones | Visión |
| OncoCore y OncoCore_app | Sus catálogos, revisiones y auditorías | Generadores propios del proyecto, origen de la carcasa de la visión: fuera de la SF |

## Alternativas | Las tres que se valoraron y lo decidido | Alternativas {#alternativas}

Las tres cumplen la norma del propietario si se aplican hasta el final: el estilo lo da el proyecto y todos sus documentos lo comparten. Se diferencian en cuánto se mantiene después y en cuánto cambia lo que ya existe.

::: tarjetas 3 plegables

### A · Fundir en el motor común {color=turquesa icono=check}

Qué es
:   `documento_a_html.py` es el único motor. Recibe lo que solo tiene la visión (el `estilo` del tema, el coloreado de código, los colores de los SVG al tema, las tablas anchas en fichas) y la visión pasa a ser un perfil con sus recursos narrativos, como el fundacional. `doc_to_html.py` queda como envoltorio y después se retira con `carcasa.py` y `estilo_base.css`.

A favor
:   Una sola maqueta que mantener; cada recurso nuevo llega a todos los documentos; es lo que ya pedía la decisión «Una skill general de diseño de documentos» (232) y el camino que tomaron el fundacional, los informes y los estados.

En contra
:   Las visiones y los «Cómo funciona…» cambian de aspecto; hay que convertir su cabecera y comprobar cada uno.

### B · Un motor y dos maquetas a elegir {color=naranja icono=rama}

Qué es
:   Un solo motor, pero la maqueta (editorial o de barras) es una clave de la identidad: `"maqueta": "barras"`. Todos los documentos del proyecto usan la que elija.

A favor
:   Un proyecto que prefiera la visión conserva su aspecto; nada cambia hasta que se elige.

En contra
:   Dos maquetas para siempre: cada recurso, cada herramienta y cada comprobación se prueban dos veces, y vuelven a separarse con el tiempo.

### C · Una maqueta nueva {color=frambuesa icono=aviso}

Qué es
:   Se diseña una tercera maqueta con lo mejor de las dos (por ejemplo, barras plegables compactas con la tipografía editorial) y todo se migra a ella.

A favor
:   La ocasión de corregir lo que no gusta de ninguna.

En contra
:   Una tarea de diseño antes de poder migrar nada; todo cambia de aspecto, también los informes que ya están bien, y se retrasa la solución.

:::

### Lo decidido: un generador único con el estilo del proyecto

> [!decision]
> Ni A, ni B, ni C tal cual («Un solo generador determinista con el estilo del proyecto; una skill ayuda a fijar sus parámetros con muestras y afinado», 305). **Un solo generador de documentos, determinista**, para todas las skills de documentos: todo lo común de la maquetación va a él, y maqueta cualquier documento con los parámetros del estilo del proyecto. **Una skill ayuda a fijar esos parámetros**: pregunta al desarrollador, le enseña muestras hechas por el generador y afina en vueltas, como en la skill de diagramas. La skill no maqueta.

Las piezas quedan así (detalle en las fichas del segundo diagrama):

- **El generador único**: `documento_a_html.py`; `doc_to_html.py` pasa a envoltorio y se retira la carcasa de la visión. Suma lo que hoy solo tiene la visión: el `estilo` del tema, el coloreado de código y los colores de los SVG al tema. Su catálogo recibe todos los recursos de la visión («Todos los recursos de la visión pasan al catálogo común», 308).
- **El estilo del proyecto**: parámetros en `docs/identidad/` que lee el generador: el tema (colores, letra, serie) y la forma (portada, secciones, escala, ancho, pie). Mientras no fije la forma de las secciones, una sección sin etiqueta sale con número y título («Las secciones sin etiqueta salen con número y título…», 306).
- **El catálogo de recursos** (`crear_documentos`): los recursos con su sintaxis y la norma de cuándo usar cada uno, ahora también los de la visión (308). Las skills de tipo eligen de él y el generador los dibuja.
- **Las herramientas de lectura** (`kit_documentos`): buscador, notas, lectura y «Diagramas». El generador las añade según el destino y las herramientas de cada documento, como hoy.
- **La calidad de la salida**: la comprobación en escritorio y móvil y la impresión A4 pasan a ser trabajo determinista del generador, una orden que se lanza en cada vuelta, no una lista que se repasa a mano.
- **La identidad del proyecto**: el logo y el nombre del producto **forman parte del estilo**, porque se ven en la portada y el pie y se eligen con las muestras. Los componentes propios (CSS y JS, como una calculadora) **van al lado**: no son estilo ni los fija la skill, pero usan sus variables. Todo vive en `docs/identidad/` («El logo y el producto forman parte del estilo; los componentes propios van al lado y usan sus variables», 313).
- **La skill de estilo**: fija y afina esos parámetros con muestras del generador. No genera ni maqueta nada; si el desarrollador pide algo que el generador no sabe hacer, propone el parámetro nuevo ([El generador evoluciona](#evoluciona)).
- **Las skills de tipo**: contenido, estructura, tono y procedimiento, y qué recursos del catálogo les convienen.
- **Los diagramas, un recurso del catálogo** («El diagrama es un recurso del catálogo y el generador único llama al motor de la skill de diagramas», 314): el `.md` nombra su `.diagrama` y el generador lo dibuja al generar, con el estilo del documento (307), llamando al motor de la skill de diagramas. Se acaban los fragmentos pegados a mano; `tinta` queda en el selector y en las páginas sueltas.
- **El color de sesión**: el de `/color` más cercano al primario del estilo (310), sin reserva para la SF (311).
- **La infografía técnica**: no pasa por el generador de documentos, pero lee los mismos parámetros del estilo ([La infografía técnica](#infografia)). Va incrustada en un documento como un recurso más o aparte y enlazada, y en las dos toma el estilo del proyecto («La infografía técnica se puede incrustar como cualquier recurso o ir como pieza aparte», 315).

### Versiones y respaldo, iguales para todos {: #versiones}

Cada vuelta de cualquier documento sube su versión en la cabecera (`version`) y guarda la anterior en `_respaldo/` con `respaldar.py` («Antes de sustituir un documento, se respalda en _respaldo/», 217). Hoy la visión anota su estado en una línea del cuerpo y no en la cabecera; con el generador único, versión, estado y respaldo son iguales en todos los tipos.

### La web comercial {: #web}

La web de la SF (`site/`) es una página comercial con su propio diseño, y de ella sale el amarillo de la SF («El amarillo del botón de la web pasa a ser el color y la identidad de la SF», 304). Comparte los colores y la letra del estilo de la SF y conserva su propia forma de página («La web comercial comparte los colores y la letra del estilo de la SF, con su propia forma de página», 312; [pregunta 8](#p8)).

### El generador evoluciona: parámetros nuevos, no excepciones {: #evoluciona}

El generador es una pieza que evoluciona: gana parámetros y refinamientos con el uso (305). **Cuando un afinado pide algo que el generador no sabe hacer, se le añade como parámetro nuevo**, y no como excepción en un documento ni como CSS suelto en la identidad del proyecto. Los `codigo.css` y `cabecera.css` de SpriteAnimation son justo las excepciones que se evitan: con un generador que evoluciona, serían parámetros. El CSS y el JS de la identidad quedan solo para los componentes propios del proyecto, como una calculadora.

::: tarjetas 2

#### Cómo se registra {color=verde icono=documento}

En el generador
:   Cada parámetro entra en el catálogo de parámetros del generador, como hoy `HERRAMIENTAS` en `tema_identidad.py`: nombre, valores, valor por defecto y qué cambia. El generador se detiene ante un parámetro que no conoce y enseña los posibles, como hace con las claves de `identidad.json`.

Valor por defecto
:   El de antes: un parámetro nuevo no cambia ningún documento que no lo pida.

En la skill y el plugin
:   Su línea en la referencia de parámetros de `crear_documentos` y en las notas de la versión del plugin; el estilo del proyecto que lo usa lo anota con su valor.

Quién lo pide
:   La skill de estilo, al afinar, propone una tarea de implementar «Añadir al generador el parámetro …» con lo que pidió el desarrollador; mientras tanto, el documento sigue con lo que el generador ya sabe hacer.

#### Cómo se prueba {color=turquesa icono=check}

Prueba del parámetro
:   Una prueba en `plugins/sf/tests/` que genera el documento de muestra con cada valor del parámetro y comprueba lo que cambia en el HTML.

Sin cambios con el valor por defecto
:   La misma muestra, generada sin el parámetro, sale igual que antes de añadirlo. Se compara con una copia de referencia guardada en las pruebas.

Determinismo
:   Dos generaciones con los mismos parámetros dan el mismo HTML, sin contar la fecha y la procedencia del pie.

A la vista
:   Las muestras con el valor nuevo se comprueban como cualquier documento, en escritorio y en móvil («Comprobación» de `crear_documentos`), y el propietario las ve en la vuelta de afinado que lo pidió.

:::

### La infografía técnica {: #infografia}

La infografía técnica (skill `infografia_tecnica`) no es un documento de lectura, pero **también toma el estilo del proyecto**: es una página three.js que se copia de `assets/plantilla-infografia.html` y se rellena a mano, sin generador. Hoy no lee nada del tema ni de la identidad. Solo lee las reglas de contenido de `docs/identidad/reglas-infografia.md`.

::: tarjetas 2

#### Lo que lleva fijo {color=frambuesa icono=aviso}

Página
:   Fondo, tinta y texto suave propios (`--bg #eef1f5`, `--ink #1b2430`, `--muted`), con su modo oscuro.

Letra
:   IBM Plex Sans y Plex Mono, de Google Fonts, sin relación con la del tema.

Escenario y HUD
:   Escenario siempre oscuro (`--stage-a`, `--stage-b`), retícula y barrido en cian, HUD cian `#6ff3ff` con cristal translúcido; la propia skill lo fija como regla («Escenario oscuro siempre… color HUD cian»).

Modelo y flujos
:   Los colores de los materiales, las luces y los flujos animados, escritos en el JavaScript (`0x…`), y los `rgba` del cian repetidos en el CSS.

#### Lo que tomaría del estilo {color=turquesa icono=check}

Página y panel de estado
:   Fondo, texto, letra, esquinas y acento del estilo, como un documento.

HUD
:   El primario o el acento del estilo en lugar del cian, con su contraste sobre el escenario.

Escenario
:   Oscuro, pero derivado del oscuro del estilo; queda como opción del estilo, para no perder el aspecto de holograma.

Lo que no cambia
:   Los colores con significado del modelo (materiales, flujos de aire, avisos), que dicen qué es cada cosa y no la identidad del proyecto.

:::

Encaja como una **tarea propia**, no fundida con la de los diagramas: el código es otro (una plantilla three.js y su CSS, sin el motor ni la herramienta «Diagramas»), y depende del diseño del estilo, que la de los diagramas no necesita. Toma el estilo con las variables del tema que ya escribe `tema_identidad.py`.

### El diagrama y la infografía, ¿recursos del catálogo? {: #recursos}

Un recurso del catálogo es algo que el `.md` describe con su sintaxis y el generador dibuja, siempre igual, con el estilo del documento. **El diagrama lo cumple** salvo en un punto: hoy se genera aparte con `generar_diagrama.py --fragmento` y su HTML se pega a mano en el `.md`. El generador de documentos solo añade su CSS, su JS y la herramienta «Diagramas» cuando lo encuentra. Pegarlo tiene dos fallos: el fragmento se queda viejo si cambian el `.diagrama` o el motor, y el `.md` carga cientos de líneas de SVG que nadie lee.

Como recurso, el `.md` lleva una línea que nombra su `.diagrama` y el generador lo dibuja en cada generación, con el estilo del documento. La skill de diagramas sigue explicando cómo diseñar uno (tipo, presupuesto, foco, fichas). El generador **llama al motor** y no se funde con él (314): el motor tiene su comprobador, sus pruebas, sus páginas sueltas en `tinta` y el modo de repetición de la 381, y evoluciona con su skill. El generador sigue siendo la única puerta y el resultado sigue siendo determinista: el mismo `.diagrama` con el mismo estilo da el mismo SVG.

**La infografía técnica no lo cumple igual**: no se describe con datos, sino que se escribe a mano para cada producto (el modelo three.js, sus modos y su relato); pesa (three.js), ocupa la pantalla y no se imprime en A4. Por eso va de las dos formas (315): aparte y enlazada, o dentro de un documento con un recurso del catálogo que la incrusta, con una imagen fija al imprimir. En las dos toma el estilo del proyecto (tarea 8).

## Migración | Los documentos existentes | Migración {#migracion}

No hay migración en bloque: cada documento pasa al generador único **cuando se vuelve a tocar** por otra razón («Cada documento se migra al generador único cuando se vuelve a tocar», 309). Hasta entonces, su HTML sigue como está.

La pieza que lo hace posible es `doc_to_html.py`. Con la tarea «Llevar la visión, los explicativos y los índices al generador único», deja de maquetar y pasa a ser un envoltorio que llama al generador único con el perfil de la visión, y `carcasa.py` y `estilo_base.css` se retiran. Así, **regenerar un documento ya lo migra**, se use la orden que se use. Lo mismo pasa con `indice_decisiones.py` y `readme_a_html.py`.

Al tocar un documento con la maqueta antigua, en su misma vuelta:

1. Se respalda en `_respaldo/`, como cualquier vuelta.
2. El conversor de cabecera pasa los comentarios de opciones (`<!-- destino: … -->`) a la cabecera `---`. El contenido no se toca.
3. Se regenera. Una sección sin etiqueta («## Guía rápida») sale con su número y su título, sin antetítulo repetido, hasta que el estilo del proyecto fije otra forma de sección («Las secciones sin etiqueta salen con número y título…», 306). Ningún documento se reescribe por esto.
4. Se comprueba como cualquier documento, en escritorio y en móvil, y con la comparación de palabras de una conversión.

En los demás proyectos pasa igual: cada documento cambia al tocarlo en una sesión abierta en ese proyecto («Un proyecto por sesión»).

## Lo afín | Lo que ya está en la cola o decidido | Lo afín {#afin}

Se revisó la cola, sin cambiarla, y lo deliberado y decidido sobre documentos, temas, identidad y el kit. **Nada de lo decidido antes choca con las decisiones 305 a 310.** Lo que cambia es el texto actual de `crear_documentos` («La visión conserva su maqueta…, propia de su forma narrativa»), que no era una decisión. Con las respuestas del propietario, cinco tareas de la cola cambian.

::: tarjetas 2 plegables

### Cambian con las decisiones {color=turquesa icono=check}

Regenerar las visiones de los proyectos y sus SVG (232)
:   **Se puede descartar.** Con «Cada documento se migra al generador único cuando se vuelve a tocar» (309) no hay regeneración en bloque: cada visión de LecturaFàcil, SocratIX, MedRol, SmartColdBox o SpriteAnimation cambia cuando se toque en su proyecto, y el proyecto elige su estilo cuando necesite documentos (305).

Actualizar Cómo funciona la Software Factory (313)
:   Gana un paso: reflejar el generador único, el estilo del proyecto como parámetros, la skill que los fija y el color de sesión derivado, cuando estén hechos. Con la 309, el propio documento se migra en esa vuelta.

Cambiar el color y la identidad de la SF al amarillo (382)
:   Con «El color de sesión se deriva del color primario del estilo del proyecto» (310), su paso 4 deja de elegir el color de sesión de la SF: sale del amarillo, `yellow`, el mismo que el panel usa para «En curso», que es su paso 2. Su paso 5 (el tema amarillo) es el estilo de partida de la SF (305) y se hace con la tarea de las muestras. El color de la SF no se reserva («El color de sesión de la SF no se reserva…», 311).

Documentos nuevos a develop en cada vuelta (297)
:   Su paso 2, la orden única para regenerar, va después de llevar la visión al generador único: así la orden solo llama a un generador.

Decidir nombres de las skills… y maqueta de la visión (312)
:   La «maqueta de la visión» ya está decidida (305 y 308). Le queda el nombre de la skill que fija el estilo, con los demás nombres, y el «sitio de diagramas-svg.md», que va con la tarea de los diagramas.

### Van antes o después {color=naranja icono=rama}

Actualizar Cómo funcionan los estados (308)
:   Ya usa el generador común, que será el único. Puede regenerar ya sus diagramas con el estilo del documento (`--tema ""`, decisión 307).

Actualizar Cómo funciona el panel (198)
:   Se cierra como está; su próxima vuelta lo migra (309).

Escribir el fundacional de la SF (235) y afinar «El taller del hombre orquesta» (230)
:   Mejor después de llevar la visión al generador único y de fijar el estilo de partida de la SF: así nacen con él.

Ciclo de las tareas de documentos (303)
:   No cambia la maqueta, pero dice cómo se hacen las vueltas de los compartidos, que ahora son también las de su migración.

Aprovechar el espacio alrededor del lector de libro (349)
:   El lector ya es común: lo que se decida vale para todos los documentos.

Afinar la skill de diagramas tras su primer uso (386)
:   Cerrada: resolvió en el motor los flecos del tema («Por defecto», el fondo «Claro» y el contraste de los rótulos). Sus fragmentos siguen pegados a mano; pasan a referencias al `.diagrama` con la tarea 5.

### No tienen que ver {color=frambuesa icono=aviso}

Sección de documentos del panel como árbol (348)
:   Organiza y abre los documentos; no los maqueta.

Replay de los diagramas (381)
:   Un modo de la skill de diagramas, independiente del estilo.

Página comercial de la SF (368)
:   La web tiene su diseño; solo comparte el amarillo de la 382.

:::

### El color de sesión con la 310

`/color` acepta ocho colores con nombre: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink` y `cyan`. Hoy `purple` es de la SF (`COLOR_SF` en `hooks/constantes.ts` y `tools/configuracion.py`) y cada proyecto elige entre los otros siete en `.sf/proyecto.json`. Con la 310, el color sale del primario del estilo: el más cercano de los ocho, medido en OKLCH. Varios proyectos azules saldrán `blue`, y la configuración deja de preguntarlo. Un proyecto sin estilo todavía conserva el color que tiene hasta que lo elija. La SF pasa a `yellow` cuando su estilo sea amarillo, y `purple` queda libre para los proyectos. El color de la SF no se reserva (311): un proyecto amarillo puede salir `yellow` como ella.

## Decidido | Lo que ya está decidido | Decidido {#decidido}

| Nº | Decisión | Qué fija aquí |
| --- | --- | --- |
| 305 | Un solo generador determinista con el estilo del proyecto; una skill ayuda a fijar sus parámetros con muestras y afinado | El planteamiento: el generador maqueta; la skill solo fija los parámetros; en la SF, el estilo de este informe |
| 306 | Las secciones sin etiqueta salen con número y título hasta que el estilo del proyecto diga otra cosa | La forma de las secciones migradas al generador único |
| 307 | Los diagramas toman el estilo del documento; tinta, en el selector y en páginas sueltas | El tema de los diagramas |
| 308 | Todos los recursos de la visión pasan al catálogo común | Al catálogo del generador único, también los narrativos |
| 309 | Cada documento se migra al generador único cuando se vuelve a tocar | Sin migración en bloque |
| 310 | El color de sesión se deriva del color primario del estilo del proyecto | Una sola fuente del color del proyecto |
| 311 | El color de sesión de la SF no se reserva: un proyecto puede salir del mismo color | Sin reserva para la SF |
| 312 | La web comercial comparte los colores y la letra del estilo de la SF, con su propia forma de página | La tarea 9 |
| 313 | El logo y el producto forman parte del estilo; los componentes propios van al lado y usan sus variables | Qué es estilo y qué va al lado en `docs/identidad/` |
| 314 | El diagrama es un recurso del catálogo y el generador único llama al motor de la skill de diagramas | La tarea 5 |
| 315 | La infografía técnica se puede incrustar como cualquier recurso o ir como pieza aparte | La tarea 8 |
| 3 | Temas visuales de la skill de visión | Temas genéricos de pocos colores; el tema y el logo viven en el proyecto |
| 7 | Fuente de las skills en la SF y lo propio de cada proyecto en `docs/identidad/` | El estilo del proyecto vive en su identidad |
| 17 | Kit de documentos HTML en la SF | Las herramientas de lectura ya son comunes |
| 28 | Forma de los documentos: texto literal, tarjetas, color con significado y código coloreado | El generador único tiene que colorear el código |
| 183 | El generador de documentos no elige por el autor | El conversor y la orden única piden destino y herramientas |
| 220 | Cada cambio de un .md regenera su HTML | Pide la orden única (paso 2 de la 297) |
| 231 | Una skill propia para los informes de las deliberativas, ligera sobre el diseño común | El modelo de perfil sobre el generador único |
| 232 | Una skill general de diseño de documentos, y skills de contenido encima | Cada tipo elige recursos y aporta su procedimiento |
| 300 | Una skill propia de diagramas | Los diagramas, en los colores y la letra del tema |
| 302 | Opciones de los diagramas: todas ajustables | El tema sigue en el selector de la herramienta |
| 304 | El amarillo del botón de la web pasa a ser el color y la identidad de la SF | El estilo de partida de la SF, en amarillo (382) |

## Por decidir | Las preguntas, todas decididas | Preguntas {#por-decidir}

Las diez preguntas están decididas; ninguna sigue abierta. La 9 y la 10 salen de preguntar si el diagrama es un recurso más del catálogo ([El diagrama y la infografía](#recursos)).

::: preguntas 2 plegables

### 1 · Cómo se llega a una base común {estado=decidida elegida=D recomendada=A} {: #p1}

Hoy hay dos generadores con dos maquetas, y el tipo de documento decide cuál.

Opción A
:   Fundir en el motor común: una sola maqueta; la visión pasa a ser un perfil y su generador se retira.

Opción B
:   Un motor con dos maquetas, editorial o de barras, que elige cada proyecto en su identidad.

Opción C
:   Diseñar una maqueta nueva con lo mejor de las dos y migrar todo a ella.

Opción D
:   Propuesta del propietario: un generador único y determinista que maqueta con los parámetros del estilo del proyecto, y una skill que los fija con muestras y afinado.

Recomendación
:   **A.** Una sola maqueta que mantener.

Decisión
:   **D** («Un solo generador determinista con el estilo del proyecto; una skill ayuda a fijar sus parámetros con muestras y afinado», 305). La skill no maqueta. En la SF, el estilo de partida es el de este informe.

### 2 · Cómo entran los títulos de la visión {estado=decidida elegida=A recomendada=A} {: #p2}

El común numera cada sección con un antetítulo; las visiones solo tienen `## Título`.

Opción A
:   Un `##` sin etiqueta sale con su número y su título, sin antetítulo repetido; nada que reescribir.

Opción B
:   Se reescriben los títulos de todas las visiones con su etiqueta.

Opción C
:   La numeración y el antetítulo pasan a ser opción del `estilo` del tema.

Recomendación
:   **A.** La migración no toca el contenido.

Decisión
:   **A** mientras el estilo del proyecto no fije la forma de las secciones; después, la que fije (306).

### 3 · Con qué tema se pintan los diagramas {estado=decidida elegida=A recomendada=A} {: #p3}

El fragmento lleva hoy `tinta` grabado por defecto.

Opción A
:   Por defecto, el del documento; `tinta` en el selector y en las páginas sueltas.

Opción B
:   Como hoy: `tinta` por defecto.

Recomendación
:   **A.** El diagrama se ve como parte del documento.

Decisión
:   **A**: papel, colores, acento y letra del documento (307).

### 4 · Adónde van los recursos propios de la visión {estado=decidida elegida=A recomendada=B} {: #p4}

Escena, caso conductor, expediente, aviso de ficción, ficha acordada, comparativa y tablas anchas en fichas.

Opción A
:   Todos al catálogo común, para cualquier documento.

Opción B
:   Los narrativos al perfil de la visión; los generales al catálogo.

Recomendación
:   **B.** La regla de `crear_documentos` sobre lo que sirve a otros tipos.

Decisión
:   **A**: todos al catálogo; la skill de cada tipo dice cuáles le convienen (308).

### 5 · Qué documentos se migran {estado=decidida elegida=C recomendada=A} {: #p5}

Diecisiete HTML de la SF tienen la maqueta de la visión.

Opción A
:   Los vivos ahora; los informes cerrados, como están.

Opción B
:   Todos, también los informes cerrados.

Opción C
:   Ninguno de golpe: cada documento, cuando se vuelva a tocar.

Recomendación
:   **A.** El estilo del proyecto se vería ya en lo que se lee hoy.

Decisión
:   **C**: sin migración en bloque (309).

### 6 · Una sola fuente del color del proyecto {estado=decidida elegida=B recomendada=A} {: #p6}

El color de sesión sale de `.sf/proyecto.json` y el de los documentos, del tema.

Opción A
:   Independientes, como hoy.

Opción B
:   El color de sesión se deriva del primario del estilo, el más cercano de los de `/color`.

Recomendación
:   **A.** La paleta cerrada de `/color` no sigue bien a un tema.

Decisión
:   **B**: una sola fuente, el primario del estilo del proyecto (310).

### 7 · El color de sesión de la SF y el de los proyectos {estado=decidida elegida=B recomendada=A} {: #p7}

Con la 310, la SF sale `yellow`, el color de «En curso» en el panel, y un proyecto de primario amarillo saldría igual que la SF. Hoy el color de la SF está reservado (`purple`).

Opción A
:   El color de la SF sigue reservado: un proyecto cuyo más cercano sea el de la SF toma el segundo más cercano. Cómo se distingue de «En curso» lo decide el paso 2 de la 382.

Opción B
:   Sin reserva: un proyecto puede salir del mismo color que la SF.

Opción C
:   La SF conserva `purple` como color de sesión, como excepción a la 310.

Recomendación
:   **A.** El color dice de un vistazo que la sesión es la de la SF, y la 310 se cumple en todos los proyectos.

Decisión
:   **B**: el color de la SF no se reserva; que hoy haya menos temas que colores es circunstancial, y puede haber varios amarillos («El color de sesión de la SF no se reserva: un proyecto puede salir del mismo color», 311).

### 8 · Si la web comercial comparte el estilo del proyecto {estado=decidida elegida=A recomendada=A} {: #p8}

La web de la SF (`site/`) tiene su propio diseño, y el amarillo de la SF sale de ella (304). No es un documento ni pasa por el generador.

Opción A
:   Comparte los parámetros de color y letra del estilo de la SF, como la infografía, pero conserva su propia forma de página.

Opción B
:   Queda fuera: su diseño es propio, y el estilo de los documentos solo toma de ella el amarillo.

Opción C
:   Se genera con el generador de documentos, con un perfil de página comercial.

Recomendación
:   **A.** Un estilo por proyecto también en lo que ve quien llega a la SF, sin forzar a la web a parecer un documento.

Decisión
:   **A**: comparte los colores y la letra del estilo de la SF y conserva su propia forma de página (312).

### 9 · Si el diagrama es un recurso del catálogo y cómo lo dibuja el generador {estado=decidida elegida=A recomendada=A} {: #p9}

Hoy se genera aparte y se pega a mano en el `.md`. Como recurso, el `.md` nombra su `.diagrama` y el generador lo dibuja al generar.

Opción A
:   Recurso del catálogo; el generador llama al motor de la skill de diagramas, que sigue en ella con su comprobador y sus pruebas.

Opción B
:   Recurso del catálogo; el motor pasa al generador único y la skill de diagramas queda solo como guía de diseño.

Opción C
:   Sigue aparte: se genera con su script y se pega en el `.md`, como hoy.

Recomendación
:   **A.** Un recurso más para quien escribe, sin fragmentos viejos, y un motor que evoluciona con su skill sin agrandar el generador.

Decisión
:   **A**: el diagrama es un recurso del catálogo y el generador único llama al motor de la skill de diagramas («El diagrama es un recurso del catálogo y el generador único llama al motor de la skill de diagramas», 314).

### 10 · Si la infografía técnica se puede incrustar en un documento {estado=decidida elegida=B recomendada=A} {: #p10}

Se escribe a mano para cada producto con three.js, ocupa la pantalla y no se imprime. Tomará el estilo del proyecto (tarea 8).

Opción A
:   Pieza aparte: el documento la enlaza, como hoy.

Opción B
:   Pieza aparte, y además un recurso del catálogo la incrusta en un documento, en un marco, con una imagen fija para la impresión.

Opción C
:   Recurso de pleno derecho: el `.md` la describe con datos y el generador la construye.

Recomendación
:   **A.** Es una página para explorar, no una figura de lectura; B se puede añadir después si un documento la pide. C pide un generador 3D que hoy no hace falta.

Decisión
:   **B**, que es A y B a la vez: va incrustada en un documento como cualquier recurso, o aparte y enlazada; en las dos toma el estilo del proyecto («La infografía técnica se puede incrustar como cualquier recurso o ir como pieza aparte», 315).

:::

## Separar | Lo que es de otra tarea | Separar {#separar}

Cuatro cosas tocan este tema pero ya tienen su tarea.

::: tarjetas 2

### El amarillo de la SF {: #a-tema-amarillo}

Se lleva
:   El color de «En curso» frente al de la SF y el tema amarillo como estilo de partida de la SF.

Adónde
:   Pasos 2 y 5 de «Cambiar el color y la identidad de la SF al amarillo de la web» (382); el 5, junto con la tarea de las muestras.

### La orden única {: #a-orden}

Se lleva
:   La orden que regenera cualquier documento con el generador único.

Adónde
:   Paso 2 de «Documentos nuevos a develop en cada vuelta» (297), después de llevar la visión al generador único.

### El nombre de la skill {: #a-nombre}

Se lleva
:   Cómo se llama la skill que fija el estilo: una parte de `crear_documentos` o una skill propia.

Adónde
:   «Decidir nombres de las skills…» (312), con los demás nombres.

### Los documentos compartidos {: #a-compartidos}

Se lleva
:   Los textos nuevos de «Cómo funciona la Software Factory» y de la metodología («Estructura documental común»); cada «Cómo funciona…» se migra en su propia vuelta (309).

Adónde
:   A sus tareas «Actualizar …» (313 y las de cada documento), de una en una, cada una con su subagente.

:::

## Tareas | Las tareas que salen, listas para crear | Tareas {#tareas}

Nueve tareas nuevas: dos de diseño (deliberativas, con su informe) y siete de implementar. Las de la columna «Después de» no empiezan hasta que la otra esté cerrada.

::: tarjetas 2 plegables

### 1 · Diseñar los parámetros del estilo de un proyecto y dónde se guardan {color=naranja icono=dialogo}

Tipo
:   Diseñar (deliberativa).

Qué gana el propietario
:   Un estilo por proyecto que el generador aplica igual a todos sus documentos, sin repetirlo en cada uno.

Qué decide
:   Qué parámetros forman el estilo de partida (tema y forma: portada, secciones, escala, ancho, pie), dónde se guardan en `docs/identidad/` y cómo los lee el generador, cómo se registra cada vuelta de afinado, cómo se pide y se acepta un parámetro nuevo, y la forma de sección que sustituye a la de la 306.

Después de
:   Nada; puede ir a la vez que la 3.

### 2 · Diseñar con el propietario las muestras de estilo y el estilo de partida de la SF {color=naranja icono=dialogo}

Tipo
:   Diseñar (deliberativa), con afinado en vueltas como en la skill de diagramas.

Qué gana el propietario
:   Un juego de muestras, hechas por el generador, para elegir en cada proyecto, y los parámetros de la SF fijados: el estilo de este informe con el amarillo (305 y paso 5 de la 382).

Después de
:   La 1 y la 3 (las muestras las hace el generador completo).

### 3 · Completar el generador único con lo que solo tiene la visión {color=turquesa icono=codigo}

Tipo
:   Implementar.

Qué gana el propietario
:   Un generador determinista que maqueta cualquier documento con todos los recursos y sale igual, sea del tipo que sea.

Qué hace
:   En `documento_a_html.py`: el catálogo de parámetros con su comprobación y la prueba de «sin cambios con el valor por defecto» ([El generador evoluciona](#evoluciona)); una orden de comprobación de la salida (escritorio, móvil e impresión A4); versión, estado y respaldo iguales en todos los tipos ([Versiones y respaldo](#versiones)); el `estilo` del tema, el coloreado de código (28), los colores de los SVG al tema, todos los recursos de la visión en el catálogo (308) y el diagrama como uno más (314, tarea 5), el `##` sin etiqueta con número y título (306), las opciones en comentarios y el conversor de cabecera, con sus pruebas.

Después de
:   Nada.

### 4 · Llevar la visión, los explicativos y los índices al generador único {color=turquesa icono=codigo}

Tipo
:   Implementar.

Qué gana el propietario
:   Un solo generador que mantener, y que regenerar cualquier documento ya lo migre (309).

Qué hace
:   `doc_to_html.py` como envoltorio del generador único; perfiles de la visión, los explicativos, la definición técnica y la interfaz; `indice_decisiones.py` y `readme_a_html.py` con el generador único; retirar `carcasa.py` y `estilo_base.css`.

Después de
:   La 3. Después va el paso 2 de la 297 (orden única).

### 5 · Hacer del diagrama un recurso del catálogo del generador único {color=turquesa icono=codigo}

Tipo
:   Implementar.

Qué gana el propietario
:   Diagramas que se escriben como cualquier recurso y nunca se quedan viejos: el generador los dibuja en cada generación, con el estilo del documento (307).

Qué hace
:   Con la 314: la sintaxis que nombra el `.diagrama` en el `.md`, la llamada del generador al motor con el estilo del documento, la comprobación de diagramas dentro de la orden de comprobación, pasar a referencias los fragmentos pegados (los de este informe y los de la 386), la «Integración» pendiente de la skill de diagramas y el sitio de `diagramas-svg.md` (312). Los flecos del tema (el «Por defecto», el fondo «Claro» y el contraste) ya los resolvió la 386.

Después de
:   La 3 (la 386 ya está cerrada).

### 6 · Construir la skill que fija los parámetros del estilo con muestras y afinado {color=turquesa icono=codigo}

Tipo
:   Implementar.

Qué gana el propietario
:   Que un proyecto le pregunte por su estilo la primera vez que necesita documentos, le enseñe muestras hechas por el generador y lo afine con él, también más adelante (305). La skill no maqueta: solo escribe los parámetros.

Qué hace
:   Lo que diseñen la 1 y la 2: la pregunta, las muestras (el generador con parámetros distintos sobre el mismo contenido), el registro de los parámetros (también el logo y el nombre del producto) y de sus vueltas, la propuesta de una tarea «Añadir al generador el parámetro …» cuando un afinado pide lo que el generador no sabe hacer, y la llamada desde la incorporación y desde `/sf_config`.

Después de
:   La 1, la 2 y la 3.

### 7 · Derivar el color de sesión del primario del estilo del proyecto {color=turquesa icono=codigo}

Tipo
:   Implementar.

Qué gana el propietario
:   Un solo color por proyecto, el de sus documentos, en la sesión y en el panel (310).

Qué hace
:   El color de `/color` más cercano al primario de los parámetros del estilo, en OKLCH; sin reservar el de la SF (311); `hooks/constantes.ts`, `tools/configuracion.py`, la incorporación y `/sf_config`, que dejan de pedirlo; un proyecto sin estilo conserva el suyo.

Después de
:   La 1 (dónde está el primario) y el paso 2 de la 382 (cómo se distingue la SF de «En curso»).

### 8 · Que la infografía técnica tome el estilo del proyecto y se pueda incrustar en un documento {color=turquesa icono=codigo}

Tipo
:   Implementar.

Qué gana el propietario
:   Infografías con los colores, la letra y el acento del proyecto, sin rehacerlas a mano, que se abren aparte o se ven dentro de un documento (315).

Qué hace
:   Que la plantilla lea los parámetros del estilo del proyecto (página, panel, HUD y, como opción del estilo, el escenario), con un script determinista que los escriba en la copia del proyecto; quitar los colores fijos repetidos; poner al día la regla del escenario y del HUD cian de la skill; comprobar el contraste del HUD sobre el escenario. Y un recurso del catálogo que la incrusta: el `.md` nombra la página, y el generador la pone en un marco a lo ancho de la columna, con su pie y un enlace para abrirla aparte. **Al imprimir en A4** no sale el marco, sino una imagen fija de la vista principal (la guarda la skill junto a la página al terminarla), con el pie y la dirección de la página.

Después de
:   La 1 (qué parámetros lleva el estilo) y la 3 (el catálogo del generador único). Conviene después de la 5, que fija cómo el generador incluye un recurso que viene de otra skill.

### 9 · Que la web comercial tome los colores y la letra del estilo de la SF {color=turquesa icono=codigo}

Tipo
:   Implementar (312).

Qué gana el propietario
:   Que la web, los documentos y la sesión de la SF se reconozcan como la misma cosa.

Qué hace
:   Que `site/` lea los parámetros de color y letra del estilo de la SF, sin cambiar su forma de página.

Después de
:   La 2 (estilo de partida de la SF) y el paso 3 de la 382 (el amarillo en la web).

:::

Y en tareas que ya existen, con el OK del propietario:

| Tarea | Cambio | Cuándo |
| --- | --- | --- |
| Regenerar las visiones de los proyectos y sus SVG (232) | Descartarla: la cubren la 305 y la 309 | Ya |
| Cambiar el color y la identidad de la SF al amarillo (382) | Paso 4: el color de sesión sale del estilo (310); paso 5, con la tarea 2 | Ya |
| Documentos nuevos a develop en cada vuelta (297) | Paso 2 tras la tarea 4 | Al crear la 4 |
| Decidir nombres de las skills… (312) | Quitar «maqueta de la visión»; añadir el nombre de la skill que fija el estilo | Ya |
| Actualizar Cómo funciona la Software Factory (313) | Paso: reflejar el generador único, el estilo como parámetros, la skill que los fija y el color derivado | Al cerrar la 4, la 6 y la 7 |
