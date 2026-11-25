---
antetitulo: Software Factory · Informe de investigación · Noviembre 2026
lema: Un estilo por proyecto, no por documento; // un solo motor que maqueta y skills que solo dicen qué contar.
subtitulo: Qué skills producen documentos HTML y con qué maqueta, qué documentos salieron de cada generador y cómo llegar a una base común de maquetación con el tema del proyecto, también en los diagramas.
version: Versión 1.0 · 05/11/2026
estado: Propuesta · Tarea 385
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de investigación
pie: Informe de la tarea «Que cada proyecto tenga un solo estilo de documentos: una base común de maquetación para todas las skills de documentos» (385). Parte de las skills de documentos del plugin en develop, del kit de documentos, de la rama de «Cómo funcionan los estados» y de los documentos HTML de la SF y de los proyectos del propietario. Espera la decisión del propietario de la Software Factory.
---
# Un estilo de documentos por proyecto: un motor común de maquetación

## Resumen | Dos maquetas en el mismo proyecto | Resumen {#resumen}

Hoy un proyecto tiene dos estilos de documento porque la SF tiene **dos generadores con dos maquetas**. El generador común de `crear_documentos` (`documento_a_html.py`) maqueta el fundacional, los informes y los diagramas: portada editorial, secciones numeradas con antetítulo («01 / ETIQUETA»), hoja de 1240 px y letra de 17 px. El de la visión (`doc_to_html.py`, con `carcasa.py` y `estilo_base.css`) maqueta la visión, los «Cómo funciona…», el índice de decisiones y `DESARROLLO.html`: franja de cabecera, barras plegables con chip, página de 980 px y otra escala de títulos. Los dos comparten temas, identidad y kit de herramientas, pero no la maqueta, y cada uno tiene cosas que el otro no: solo el común carga los diagramas; solo el de la visión aplica el `estilo` del tema, colorea el código y pasa los colores de los SVG al tema. Por eso «Cómo funcionan los estados» cambió de aspecto al pasarse al común para tener diagramas.

Se propone **fundir los dos en un solo motor**, el común, con una sola maqueta por proyecto que sale de su identidad (tema y su `estilo`, logo, producto, CSS propio). Las skills de cada tipo de documento quedan para el contenido, la estructura y el procedimiento, con su perfil; los recursos narrativos de la visión pasan a su perfil, y lo que sirve a todos, al catálogo. Los diagramas dejan de llevar el tema `tinta` grabado y toman el del documento. La visión se migra con un conversor de cabecera y se comprueba con la comparación de palabras.

<figure class="vertical">
<svg viewBox="0 0 560 470" width="100%" role="img" aria-label="Propuesta: la identidad del proyecto da el tema, el estilo, el logo y el CSS al motor común, que tiene una sola maqueta. Encima, los perfiles de cada tipo de documento: visión, explicativo, fundacional, informe y técnico, que solo eligen recursos y añaden los suyos. Los diagramas se pegan como fragmento y toman el tema del documento. Sale un HTML con el estilo del proyecto." style="font-family:var(--fuente-texto);display:block">
<g font-size="15">
<rect x="20" y="10" width="520" height="92" rx="8" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5"/>
<text x="280" y="34" text-anchor="middle" font-size="18" font-weight="700" style="fill:var(--oscuro)">Perfiles de tipo de documento</text>
<text x="280" y="58" text-anchor="middle" style="fill:var(--texto)">visión · explicativo · fundacional · informe · técnico</text>
<text x="280" y="82" text-anchor="middle" style="fill:var(--texto-suave)">contenido, estructura, recursos elegidos</text>
<line x1="280" y1="102" x2="280" y2="140" style="stroke:var(--texto-suave)" stroke-width="1.5"/>
<path d="M274 132 L280 142 L286 132 Z" style="fill:var(--texto-suave)"/>
<rect x="20" y="146" width="250" height="78" rx="8" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5"/>
<text x="145" y="176" text-anchor="middle" font-size="18" font-weight="700" style="fill:var(--oscuro)">Identidad</text>
<text x="145" y="200" text-anchor="middle" style="fill:var(--texto-suave)">tema, estilo, logo, CSS</text>
<rect x="290" y="146" width="250" height="78" rx="8" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5"/>
<text x="415" y="176" text-anchor="middle" font-size="18" font-weight="700" style="fill:var(--oscuro)">Diagramas</text>
<text x="415" y="200" text-anchor="middle" style="fill:var(--texto-suave)">fragmento sin tema propio</text>
<line x1="145" y1="224" x2="145" y2="262" style="stroke:var(--texto-suave)" stroke-width="1.5"/>
<path d="M139 254 L145 264 L151 254 Z" style="fill:var(--texto-suave)"/>
<line x1="415" y1="224" x2="415" y2="262" style="stroke:var(--texto-suave)" stroke-width="1.5"/>
<path d="M409 254 L415 264 L421 254 Z" style="fill:var(--texto-suave)"/>
<rect x="20" y="268" width="520" height="96" rx="8" fill="none" style="stroke:var(--primario)" stroke-width="3"/>
<text x="280" y="298" text-anchor="middle" font-size="18" font-weight="700" style="fill:var(--primario)">Motor común · una maqueta</text>
<text x="280" y="322" text-anchor="middle" style="fill:var(--texto)">portada, secciones, catálogo, pie, kit</text>
<text x="280" y="346" text-anchor="middle" style="fill:var(--texto-suave)">documento_a_html.py</text>
<line x1="280" y1="364" x2="280" y2="402" style="stroke:var(--primario)" stroke-width="2"/>
<path d="M274 394 L280 404 L286 394 Z" style="fill:var(--primario)"/>
<rect x="120" y="408" width="320" height="52" rx="8" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/>
<text x="280" y="440" text-anchor="middle" font-weight="700" style="fill:var(--oscuro)">HTML con el estilo del proyecto</text>
</g>
</svg>
<figcaption>La propuesta: la maqueta vive en un solo motor; la identidad le da el estilo del proyecto y los perfiles solo eligen qué se cuenta.</figcaption>
</figure>

Quedan **cinco preguntas** para el propietario: la base común, cómo entran los títulos de la visión, el tema de los diagramas, adónde van los recursos de la visión y qué documentos se migran.

[Ver las 5 preguntas](#por-decidir){: .salto} [Ver las tareas que salen](#tareas){: .salto}

## Skills | Qué skill produce qué y con qué maqueta | Skills {#skills}

Siete skills del plugin dan documentos o páginas HTML, pero **solo dos generadores maquetan**: el común y el de la visión. El fundacional y el informe son envoltorios de pocas líneas sobre el común, con su perfil. Las skills técnicas (definición técnica, interfaz) escriben `.md` sin decir con qué se generan; los bocetos y las infografías son páginas propias que no son documentos.

::: tarjetas 2 plegables

### crear_documentos · el motor común {color=turquesa icono=codigo}

Generador
:   `scripts/documento_a_html.py`, con `--perfil`.

Maqueta
:   Portada blanca u oscura con marca, titular, lema y subtítulo (en la rama de los estados, también `compacta`); menú fijo con botones o secciones; secciones `details` numeradas «01 / ETIQUETA» con `h2` de hasta 2,2 rem; hoja de 1240 px; letra de 17 px (18 desde 1600 px); pie con producto, tipo, versión, estado, texto del pie y procedencia.

Recursos
:   Tarjetas (color, icono, plegables), columnas, fichas con buscador, preguntas con opciones, fuentes, recuadros, métricas, lector de libros, diagramas.

Temas e identidad
:   `tema_identidad.py`: tema, logo, producto, tipo, CSS, JS e iconos. Del tema usa solo los colores, la serie y las tipografías: **no aplica su `estilo`** (cabecera, etiqueta, marcador, esquinas).

Kit
:   `herramientas`, `lectura`, `edicion`, `diagramas.js` (solo con diagramas), `plegado.js` y `fichas.js` propios.

Le falta
:   El coloreado de código y el paso de los colores de los SVG a variables del tema.

### documento_vision · la maqueta propia {color=naranja icono=documento}

Generador
:   `scripts/doc_to_html.py`, con `carcasa.py` y `assets/estilo_base.css`, más 150 líneas de CSS dentro del script.

Maqueta
:   Franja de cabecera (logo, nombre y producto) y barra de estado opcional; bloques `details` por cada `##` con chip y marcador, `###` y `####` también plegables; página de 980 px que el script abre a todo el ancho; `h1` de 1,3 rem y `h2` de 1,05 rem; pie oscuro con producto y tipo, y procedencia.

Recursos propios
:   Escena dialogada, caso conductor, expediente, aviso de ficción, ficha con campos acordados, comparativa de versiones, tablas de cuatro columnas o más en fichas, lector de libros.

Temas e identidad
:   Los mismos de `crear_documentos`, y además aplica el `estilo` del tema y traduce los colores fijos de los SVG al tema.

Kit
:   `herramientas`, `lectura`, `edicion`. **No carga los diagramas** ni su herramienta.

Opciones
:   En comentarios al principio del `.md` (`<!-- destino: … -->`), no en cabecera.

### documento_fundacional e informe_deliberativa {color=verde icono=documento}

Generador
:   Envoltorios de 18 líneas sobre el común: `fundacional_to_html.py` e `informe_to_html.py`.

Perfil
:   `perfil.json` con su tipo y sus recursos (el informe añade las preguntas). Ninguno trae CSS ni JS propios.

Duplica
:   Nada: es el modelo de lo que se propone para la visión.

### diagramas {color=frambuesa icono=rama}

Generador
:   `generar_diagrama.py`, que da una página suelta o, con `--fragmento`, la `<figure>` para pegar en el `.md`.

Tema
:   `--tema tinta` por defecto, grabado en la figura como `data-d-tema="tinta"`. El motor común escribe los colores de **cada tema** bajo `.diagrama[data-d-tema=…]`, con papel propio: el diagrama no hereda el tema del documento.

Kit
:   `diagramas.css` y `diagramas.js` de la skill y la herramienta «Diagramas» del kit.

Pendiente en su skill
:   El ancho de las verticales (400, 420 o 560) y la integración con el generador común.

### definicion_tecnica y diseno_interfaz {icono=lupa}

Generador
:   Ninguno nombrado. Escriben `.md` con SVG inline y siguen la guía de diagramas; la metodología dice que todo documento se genera con `crear_documentos`, pero no tienen perfil ni envoltorio.

Bocetos
:   Los de la interfaz son HTML autocontenidos y neutros a propósito: el aspecto se decide después.

### infografia_tecnica {icono=aviso}

Página
:   Plantilla three.js propia, con escenario oscuro de HUD, sin el kit ni la identidad.

Encaje
:   No es un documento de lectura: queda fuera de la base común. Como mucho, podría tomar el primario y la letra del tema del proyecto.

:::

Además, dos herramientas del plugin generan HTML con el generador de la visión: `tools/indice_decisiones.py` (el `README.html` de las decisiones) y `scripts/readme_a_html.py` de la SF (`DESARROLLO.html`).

### Lo que se duplica y lo que se pierde

Los dos generadores repiten la lectura de la identidad y de las opciones, el logo, los enlaces externos, la procedencia, las tablas en fichas para el móvil y el arranque del kit, cada uno a su manera. Lo grave no es la repetición sino **lo que cada uno no tiene**: un documento con diagramas no puede tener el aspecto de la visión, y uno del común pierde el `estilo` del tema y el coloreado de código. Los proyectos ya lo parchean: SpriteAnimation lleva en su identidad un `codigo.css` («el kit solo da estilo al código en línea») y un `cabecera.css` con reglas para `.portada.oscura` y para `.site-header` a la vez, una por maqueta.

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

## Alternativas | Tres maneras de llegar a una base común | Alternativas {#alternativas}

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

### La recomendada: A, con el estilo del proyecto en el tema

> **Propuesta**
> Fundir en el motor común (A). El estilo de cada proyecto es su identidad: el tema con su `estilo`, el logo, el producto y el CSS propio, aplicados igual a todos sus documentos. Lo que hoy distingue a la visión por su maqueta (franja de cabecera, etiquetas sólidas, marcadores) pasa a ser opciones del `estilo` del tema, que el motor común aprende a aplicar.

Así, un proyecto que quiera cabecera en franja de color la pide en su tema, no eligiendo un generador. Las piezas quedan:

- **El motor** (`crear_documentos`): portada, secciones, catálogo, pie, kit, tema y su `estilo`, coloreado de código, colores de los SVG al tema, tablas anchas en fichas, diagramas y lector. Las opciones se leen de la cabecera `---`; los comentarios `<!-- destino: … -->` de la visión se aceptan mientras dure la migración.
- **Los perfiles** (cada skill de tipo): contenido, estructura, tono, procedimiento y los recursos que eligen. La visión trae los suyos (escena, caso, expediente, aviso de ficción) como CSS y JS de su perfil. Los explicativos («Cómo funciona…»), hoy dentro de la visión, tendrían su perfil con la portada compacta de la rama de los estados. La definición técnica y la interfaz, un perfil sencillo cada una.
- **Los diagramas**: el fragmento sale sin tema propio y hereda las variables del documento; `tinta` queda para las páginas sueltas y para el selector de la herramienta «Diagramas», si se conserva.
- **Una orden para generar**: la orden única que pide la decisión «Cada cambio de un .md regenera su HTML» (220) elige el perfil por el `tipo` de la cabecera o por la carpeta, y la usan el índice de decisiones, `DESARROLLO.html` y las vueltas de los informes.

### Cómo se migran los documentos

La migración es casi mecánica porque el contenido no cambia: cambia la cabecera y la maqueta. Un conversor (`migrar_a_comun.py`, en la tarea del motor) pasa los comentarios de opciones a la cabecera `---`, toma el título y la barra de «Estado» como `version` y `estado`, y deja los `##` como están. Cada documento se respalda en `_respaldo/`, se regenera y se comprueba con la comparación de palabras de una conversión y con capturas en escritorio y móvil.

Los «Cómo funciona…» son documentos compartidos: cada uno cambia en su tarea «Actualizar …» con su subagente, como manda la orquestación («Documentos compartidos»). En los demás proyectos no se cambia nada desde la SF («Un proyecto por sesión»): reciben el motor con el plugin y regeneran sus documentos al ponerse al día con la SF; los `codigo.css` y `cabecera.css` de SpriteAnimation sobran entonces.

El tema amarillo de la SF («El amarillo del botón de la web pasa a ser el color y la identidad de la SF», 304) cambia el tema de todos sus documentos: conviene que su tarea vaya antes de la migración, para regenerar una sola vez.

## Decidido | Lo que ya está decidido | Decidido {#decidido}

| Nº | Decisión | Qué fija aquí |
| --- | --- | --- |
| 232 | Una skill general de diseño de documentos, y skills de contenido encima | La skill de cada tipo elige recursos y aporta su procedimiento; el diseño es común |
| 220 | Cada cambio de un .md regenera su HTML | Pide una orden única que elija el generador |
| 300 | Una skill propia de diagramas | Los diagramas usan los colores y la letra del tema de `crear_documentos` |
| 304 | El amarillo del botón de la web pasa a ser el color y la identidad de la SF | El tema de los documentos de la SF cambiará |

## Por decidir | Lo que queda por decidir | Por decidir {#por-decidir}

Cinco preguntas, por importancia. La primera decide el resto: si se elige B o C, la segunda y la cuarta cambian de sentido.

::: preguntas 2 plegables

### 1 · Cómo se llega a una base común {recomendada=A} {: #p1}

Hoy hay dos generadores con dos maquetas, y el tipo de documento decide cuál.

Opción A
:   Fundir en el motor común: una sola maqueta; la visión pasa a ser un perfil y su generador se retira.

Opción B
:   Un motor con dos maquetas, editorial o de barras, que elige cada proyecto en su identidad.

Opción C
:   Diseñar una maqueta nueva con lo mejor de las dos y migrar todo a ella.

Recomendación
:   **A.** Una sola maqueta que mantener, y es el camino que ya toman el fundacional, los informes y los estados.

### 2 · Cómo entran los títulos de la visión {recomendada=A} {: #p2}

El común numera cada sección con un antetítulo («01 / ETIQUETA») sacado de `## Etiqueta | Título`; las visiones y los «Cómo funciona…» solo tienen `## Título`.

Opción A
:   Un `##` sin etiqueta sale con su número y su título, sin antetítulo repetido; nada que reescribir.

Opción B
:   Se reescriben los títulos de todas las visiones con su etiqueta, como los informes.

Opción C
:   La numeración y el antetítulo pasan a ser opción del `estilo` del tema, para todo el proyecto.

Recomendación
:   **A.** La migración no toca el contenido, y quien quiera etiquetas las añade al revisar.

### 3 · Con qué tema se pintan los diagramas {recomendada=A} {: #p3}

El fragmento lleva `tinta` grabado y el documento le da su papel y sus colores, distintos de los de la página.

Opción A
:   Por defecto, el tema del documento; `tinta` solo en las páginas sueltas, y la herramienta «Diagramas» puede seguir ofreciendo otro tema al lector.

Opción B
:   Siempre el tema del documento, sin selector de tema en la herramienta.

Opción C
:   Como hoy: `tinta` en todos, como estética propia de los diagramas.

Recomendación
:   **A.** El diagrama se ve como parte del documento y el lector no pierde la opción.

### 4 · Adónde van los recursos propios de la visión {recomendada=B} {: #p4}

Escena dialogada, caso conductor, expediente, aviso de ficción, ficha acordada, comparativa de versiones y tablas anchas en fichas.

Opción A
:   Todos al catálogo común, para cualquier documento.

Opción B
:   Los narrativos (escena, caso, expediente, aviso de ficción) al perfil de la visión; los que sirven a todos (comparativa, ficha acordada, tablas anchas en fichas) al catálogo.

Recomendación
:   **B.** Es la regla de `crear_documentos`: al catálogo lo que sirve a otros tipos, y lo demás al perfil.

### 5 · Qué documentos se migran {recomendada=A} {: #p5}

En la SF hay diecisiete HTML con la maqueta de la visión; cinco son informes cerrados con el formato antiguo de preguntas.

Opción A
:   Los vivos: «Cómo funciona…», visiones, fundacionales, `DESARROLLO.html` y el índice de decisiones. Los informes cerrados conservan su HTML como registro.

Opción B
:   Todos, también los informes cerrados, convirtiendo sus preguntas al formato de fichas.

Opción C
:   Ninguno de golpe: cada documento, cuando se vuelva a tocar.

Recomendación
:   **A.** El estilo del proyecto se ve en lo que se lee hoy, sin reescribir informes que ya no cambian.

:::

## Separar | Lo que es de otra tarea | Separar {#separar}

Dos cosas tocan este tema pero tienen su propia tarea o su propio cauce.

::: tarjetas 2

### El tema amarillo de la SF {: #a-tema-amarillo}

Se lleva
:   El cambio del tema de los documentos de la SF, que ya tiene su tarea pendiente («El amarillo del botón de la web pasa a ser el color y la identidad de la SF», 304).

Adónde
:   A esa tarea, que conviene hacer antes de la migración.

### Los documentos compartidos {: #a-compartidos}

Se lleva
:   La regeneración de los «Cómo funciona…» y el texto nuevo de la metodología («Estructura documental común») y de «Cómo funciona la Software Factory» (generadores y skills de documentos).

Adónde
:   A sus tareas «Actualizar …», de una en una, cada una con su subagente.

:::

## Tareas | Las tareas que salen | Tareas {#tareas}

Si se aprueba la alternativa A, salen estas tareas, en este orden. Las cuatro primeras son de código, con rama.

| Tarea | Tipo | Qué hace |
| --- | --- | --- |
| Completar el motor común con lo que solo tiene la visión | Código | `estilo` del tema, coloreado de código, colores de los SVG al tema, tablas anchas en fichas, opciones en comentarios y el conversor `migrar_a_comun.py`, con sus pruebas |
| Pasar la visión a un perfil del motor común | Código | Perfil de la visión con sus recursos narrativos, perfiles de los explicativos, de la definición técnica y de la interfaz; `doc_to_html.py` como envoltorio; índice de decisiones y `DESARROLLO.html` con el común |
| Que los diagramas tomen el tema del documento | Código | Fragmento sin tema grabado, herencia de las variables del documento y el selector de tema según la pregunta 3; resuelve la «Integración» pendiente de la skill de diagramas |
| Una orden para generar cualquier documento | Código | La orden única de la decisión 220, que elige el perfil por el tipo o la carpeta |
| Migrar los documentos vivos de la SF al motor común | Documental | Respaldo, conversión, regeneración y comprobación de cada uno; los compartidos, en sus tareas «Actualizar …» |
| Retirar la maqueta de la visión | Código | Borrar `carcasa.py` y `estilo_base.css` cuando nada los use, y poner al día `test_vision.py` |
| Actualizar «Cómo funciona la Software Factory» y la metodología | Documental | Un solo generador y las skills de tipo como perfiles |
