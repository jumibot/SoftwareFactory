# Origen de la skill `documento_vision`

- **Fuente:** skill global del propietario, `~/.claude/skills/documento_vision/` (copiada el 2026-10-25).
- **Motivo:** propuesta «Independizar la skill de visión de OncoCore» de `docs/mejora-continua.md`, aprobada el 2026-10-25.

## Cambios respecto a la fuente

La skill funciona sin acceso al proyecto OncoCore. El HTML generado es idéntico al de la fuente.

| Archivo | Cambio |
|---|---|
| `scripts/carcasa.py` | Nuevo. Funciones de `D:/Projectes/OncoCore/tools/operational/md_to_html/md_to_html.py` (v1.0.37) que usa el generador, sin cambios de comportamiento: `ensure_blank_line_before_headings`, `slugify`, `add_anchors`, `wrap_subsubsecciones`, `wrap_subsecciones`, `wrap_bloques`, `render_page` y `BLOQUE_TOGGLE_SCRIPT`. No incluye la lectura de `oncocore.ini` ni las partes clínicas. |
| `assets/estilo_base.css` | Copia de `D:/SecondMind/Proyectos/OncoCore/.claude/oncocore_html_style_operativo.css`, con la cabecera de comentario sustituida por una genérica. |
| `scripts/doc_to_html.py` | Importa `carcasa` en vez de `md_to_html`. Docstring actualizada. |
| `SKILL.md` | Solo la sección «Identidad visual y generación»: rutas relativas a la carpeta de la skill. El resto del contenido se conserva, incluidas las referencias a OncoCore. |

No se copió `scripts/doc_to_html.py.bak`.

## Comprobación

El 2026-10-25 se generó `docs/specs/vision/software-factory.md` con la skill original y con esta copia (aislada en una carpeta temporal y ejecutada con `python -I`). Se probaron tres variantes: sin logo, paleta `instituto` y opciones por defecto. Los HTML son idénticos byte a byte. La copia no cargó `md_to_html` ni añadió rutas de OncoCore a `sys.path`.

## Temas visuales (2026-10-25)

Propuesta «Temas visuales para la skill de visión», puntos 1 a 3, aprobados por el propietario.

- `assets/estilo_base.css` y los estilos de `scripts/doc_to_html.py` usan variables CSS (`var(--primario)`, `var(--fuente-texto)`…) en lugar de colores y tipografías fijos. En las URI de datos SVG, donde `var()` no funciona, hay marcadores `{{rol}}` que el script rellena.
- Las tablas `PALETA`, `PALETA_URI` y `PALETAS_EXTRA` y las funciones `recolorear` se sustituyen por archivos de tema en `assets/temas/` (entonces `oncocore.json` y `instituto.json`), la opción `--tema` (`--paleta` queda como sinónimo) y los tonos derivados (`DERIVADOS`).
- Comprobación: se compararon cuatro casos con la copia anterior (visión de la SF con y sin logo; visión de LecturaFàcil con los temas `oncocore` y `instituto`). Una vez resueltas las variables CSS, los HTML son idénticos. Un tema de prueba con solo `primario` genera el documento sin variables sin definir ni restos del morado. No se ha revisado visualmente en un navegador.

## Temas genéricos y logos en cada proyecto (2026-10-25)

Instrucción del propietario: el logo vive en cada proyecto, y la skill solo guarda temas y colores con nombres genéricos.

- Temas renombrados por su color: `oncocore` → `morado` (por defecto) y `instituto` → `rojo`. Nuevo tema `teal`, con los colores de origen de la carcasa (los de los informes del hospital), acento violeta y tipografía Assistant.
- Los temas ya no llevan logo. El script solo pone logo con `--logo <ruta>`; sin esa opción, la cabecera es solo texto.
- Logos retirados de `assets/`. El de OncoCore sigue en OncoCore (`design_handoff_oncocore/assets/`). El del instituto está ahora en LecturaFàcil, `doc/identidad/`, junto a una nota con el tema y el comando.
- Comprobación: repetidos los cuatro casos con `morado` y `rojo` y los logos tomados de cada proyecto; son idénticos a la copia anterior una vez resueltas las variables. El tema `teal` genera el documento sin variables sin definir ni restos del morado.

## Identidad de cada proyecto (2026-10-25)

Instrucción del propietario: cada proyecto guarda, junto al logo, el nombre del tema.

- `identidad.json` en `doc/identidad/` o `docs/identidad/` del proyecto: `{"tema": "...", "logo": "..."}`, con el logo relativo a esa carpeta. El script lo busca subiendo desde el `.md`, o lo toma de `--identidad`. `--tema` y `--logo` mandan sobre él.
- LecturaFàcil tiene `doc/identidad/identidad.json` (tema `rojo`, logo de un instituto) e `identidad.md`.
- Comprobación: en una copia del árbol de LecturaFàcil, la identidad encontrada automáticamente da el mismo HTML, byte a byte, que `--tema rojo --logo …`. `--tema teal --logo ninguno` e `--identidad ninguna` mandan sobre ella. Sin identidad (visión de la SF), se usa `morado` sin logo.

## Serie de colores y tema `colorido` (2026-10-25)

Petición del propietario: un tema colorido, basado en varios colores, para la SF.

- Los temas aceptan `serie`, una lista de colores: cada bloque (`.bloque-N`) redefine sus variables (primario, oscuro, fondo, borde, línea, tenue, fondo suave y las de la carcasa `--brand-teal…`) con uno de ellos, en ciclo. Sin `serie`, la salida no cambia.
- Tema `colorido`: los siete colores de la serie tienen un contraste de entre 5,0 y 6,7:1 sobre blanco y de 4,7:1 o más sobre su fondo.
- SoftwareFactory tiene `docs/identidad/identidad.json` con el tema `colorido`, sin logo. Su visión se ha regenerado con él; el HTML anterior, en morado, está en `docs/specs/vision/_respaldo/software-factory_tema-morado.html`.
- Comprobación: los temas sin serie dan la misma salida que antes, salvo la cabecera de comentario de la hoja de estilos. Una captura de la visión con los bloques abiertos muestra un color distinto en cada bloque.

## Gráficos por bloque y paleta OKLCH de `colorido` (2026-10-25)

- Los colores de los gráficos y estilos del `.md` pasan a variables CSS (los atributos SVG `fill`, `stroke`… se mueven a `style`), así que cada gráfico toma los colores de su bloque. Por bloque se redefinen también `fondo-medio` y `primario-vivo`. Con el tema `morado`, una captura del documento entero no cambia ni un píxel.
- `colorido` se rehace con `skills/oklch-skill`: L 0.53 y el 90 % del croma máximo de cada tono. El orden de la serie se eligió con el validador de `dataviz`, sin fallos ni avisos (peor separación con daltonismo entre colores vecinos: ΔE 13,2; con visión normal: ΔE 19,4). Contraste de 4,6:1 o más sobre blanco y sobre el fondo de su bloque. Los fondos generales pasan a gris neutro.

## `colorido` sin morados (2026-10-25)

El propietario seguía viendo fondos morados: los del índigo (bloques 1 y 8, por el ciclo) y los del violeta. Nueva serie sin morados: azul, naranja, turquesa, rojo, azul cielo y verde (OKLCH L 0.53, 90 % del croma máximo). Es el único orden de seis colores, de entre los candidatos, que pasa en el validador de `dataviz` la separación con daltonismo (ΔE 11,5) y con visión normal (ΔE 18,2), contando el paso del último color al primero. El turquesa queda por debajo del mínimo de viveza del validador para gráficos de datos; se acepta porque cada bloque lleva su título. Comprobación: en una captura del documento entero no quedan fondos claros de tono morado.

## Temas diferenciados: opciones de `estilo` (2026-10-25)

Petición del propietario: que los temas se distingan lo suficiente como estilos completos.

- Los temas admiten `estilo`: `cabecera` (blanca, primario, oscuro), `etiqueta` (tinte, solida, linea), `marcador` (circulo, cuadrado, ninguno) y `esquinas` (px). Sus reglas se añaden al final de los estilos del script, para que manden.
- `morado` sin cambios (en una captura del documento entero no cambia ni un píxel). `rojo`: institucional (franja oscura, línea lateral, serifa). `teal`: sobrio (franja de color, sin marcador). `colorido`: etiquetas sólidas y esquinas muy redondeadas.
- `rojo` lo usa LecturaFàcil: su visión cambiará de aspecto la próxima vez que se genere. Su HTML actual no se ha tocado.

## Skill independiente de cualquier dominio (2026-10-25)

Instrucción del propietario: la skill no contiene nada de ningún proyecto. Todo lo propio de cada uno va a su `identidad.json`.

- **`identidad.json`** admite ahora `tema` (nombre o `.json` del proyecto), `logo`, `producto`, `tipo`, `css` (una hoja o una lista) y `reglas` (reglas de redacción del dominio, que lee quien redacta). Las claves desconocidas dan error. El CSS del proyecto se añade al final, después del tema. `--producto` ya no vale «OncoCore SocratAI» por defecto: sin identidad, no hay producto y el pie dice «Documento de visión».
- **`estilo_base.css`:** fuera los apartados de los informes de OncoCore que ninguna visión usaba: insignia, versión, datos de entrada, índice, aviso de navegación, Farmacia, enlaces de Obsidian, tabla de auditoría, insignias de estado, `kb-tech` y `kb-meta`, y paneles de estado. Los alias `--brand-teal…`, `--obsidian-…`, `--bg-page` y `--text-…` pasan a los roles del tema (`--primario`, `--oscuro`…). La letra del cuerpo es `var(--fuente-texto)`. De 632 a unas 340 líneas. El original sigue en OncoCore.
- **`carcasa.py`:** comentarios sin ejemplos clínicos; `render_page` sin insignia ni datos de entrada, y sin el pie «OncoCore · Uso clínico interno» ni la carga fija de Assistant (cada tema carga sus letras).
- **`doc_to_html.py`:** comentarios genéricos; la clase `turno arnes` pasa a `turno sistema`; el estilo `esquinas` deja también la variable `--esquinas` para el CSS de cada proyecto.
- **Componentes de LecturaFàcil** (hojas del alumno, pestañas, glosario, botón de voz, formatos de papel): salen de la skill a `LecturaFacil/doc/identidad/componentes.css`, y su explicación, junto con las pautas de lectura fácil, a `reglas-vision.md`. Las visiones de la SF y de LecturaFàcil usan ahora `turno sistema`.
- **`SKILL.md`:** sin ejemplos ni rutas de proyectos. Las reglas clínicas pasan a ser principios generales (honestidad con los datos, rigor con el proyecto y su dominio), y su versión clínica queda en `docs/traslados/oncocore-reglas-vision.md` de la SF, pendiente de llevarla al proyecto que corresponda. Nueva sección «Lo propio de cada proyecto»: se leen la identidad y sus reglas antes de proponer la visión, y lo que se aprende del dominio va a las reglas del proyecto, no a la skill. Los gráficos nuevos usan la letra del tema (`font-family:var(--fuente-texto)`); los documentos ya escritos no se han cambiado.
- **Temas:** descripciones de `teal` (sin «clínico» ni «carcasa de informes») y de `colorido` (estaba desfasada) corregidas.
- **Comprobación:** las visiones de la SF y de LecturaFàcil, con los cuatro temas, a 1400 y 390 px de ancho, con todos los bloques abiertos y sin animaciones, dan en Chrome el mismo estilo calculado en cada elemento antes y después (16 casos, sin contar las variables CSS, que cambian de nombre). Mismos textos de cabecera, pie y logo. Un proyecto de prueba de otro dominio, con tema y CSS propios, se genera bien y se ha revisado en una captura. La visión de la SF se ha regenerado. La de LecturaFàcil no, porque cambiaría al nuevo aspecto de `rojo`.

## Sustitución de la skill global (2026-10-25)

Petición del propietario: sustituir la skill global por esta, sin que OncoCore ni sus documentos se vean afectados.

- **Dependencias:** nada de OncoCore (código, hooks, vault de SecondMind) llama a la skill. La skill global antigua dependía de OncoCore, no al revés.
- **Documentos generados con la global:** SocratIX (`valoracion-propuesta-socratai`), MedRol (`sphera-sim-vision`) y SmartColdBox (`vision-smart-cold-box`). Los tres usaban los valores por defecto antiguos: tema morado, logo de OncoCore y, salvo MedRol, el producto «OncoCore SocratAI».
- **Identidades creadas** en `docs/identidad/` de los tres proyectos, con esos mismos valores y una copia del logo de OncoCore. SocratIX tiene además `reglas-vision.md`, con las reglas clínicas que salieron de esta skill. En SocratIX, `_docs/` pasó a `docs/` por indicación del propietario. En sus tres `.md`, `turno arnes` pasó a `turno sistema`.
- **Copia de seguridad** de la global antigua: `skills/_respaldo/documento_vision_global_2026-10-25/`.
- **Comprobación:** los tres documentos generados con la global antigua y con la nueva (identidad encontrada sola) dan en Chrome el mismo estilo calculado en cada elemento, a 1400 y a 390 px, y el mismo texto y logo. La única diferencia era el nombre de archivo de la prueba. Sus `.html` reales no se han regenerado.

## Ajustes posteriores (2026-10-25)

- SmartColdBox y MedRol ya no llevan el logo de OncoCore. Su identidad es: tema `morado`, sin logo, producto propio («Smart Cold Box», «Sphera SIM · Simulated Medical Instruments») y «Documento de visión». Sus HTML se regeneraron, con el anterior en `_respaldo/`.
- La visión de LecturaFàcil se regeneró con el aspecto actual del tema `rojo`, con el anterior en `_respaldo/`.
- `SKILL.md`: antes de crear un tema a partir de la web de una organización, se pregunta al autor (punto 4 de «Temas visuales», aclarado por el propietario).

## Botones de los bloques sin JavaScript (2026-10-25)

El propietario vio que plegar los bloques funcionaba unas veces y otras no. Causa: en los visores que no ejecutan JavaScript, «Expandir» y «Contraer» no hacían nada, y el título sí plegaba. Ahora el script marca `<html class="js">` y `estilo_base.css` oculta los botones sin esa clase: sin JavaScript se pliega tocando el título. Probado con Playwright en Chrome, WebKit e iPad simulado (con y sin JavaScript). No probado en el visor concreto en el que falló.

- `SKILL.md`, lista de comprobación: la comparación con el mercado no es benevolente con el propio proyecto (corrección del propietario sobre la visión de la SF, 2026-10-25).

## Módulo compartido de temas e identidad (2026-10-26)

`scripts/tema_identidad.py` reúne lo que antes estaba dentro de `doc_to_html.py`: temas, colores derivados, tipografías, variables CSS, logo y búsqueda de `identidad.json`. Lo usa también la skill `documento_fundacional`. El cambio no altera el comportamiento: las visiones de la SF, el informe de fricciones y la visión de SmartColdBox regenerados salieron idénticos byte a byte. `identidad.json` admite además la clave `js`, que solo usa el generador de `documento_fundacional`.

## Tema `pool` (2026-10-26)

Petición del propietario: el mismo esquema de colores en todo SmartColdBox, con los de su justificación de SMB VIAL («si es necesario crea una paleta nueva»), con el nombre «pool», y después añadirlo al catálogo de temas.

- Colores tomados de las variables de `SmartColdBox/docs/specs/vision/SMB_VIAL_Justificacion.html` (azul marino, verde azulado, menta, papel, dorado); los roles que no tenía, derivados de ellos. Serie de seis colores para gráficas.
- Para distinguirse de `teal` y `morado` a primera vista: fuentes del sistema (como el original), cabecera en franja azul marino, marcador cuadrado y esquinas de 12 px.
- `tema_identidad.py` y el generador de `documento_fundacional`: con la `url` de fuentes vacía no escriben el enlace a Google Fonts (antes habría quedado `<link href="">`).
- Comprobación: `morado`, `teal` y `rojo` generan la visión de SmartColdBox idéntica byte a byte al código anterior, y las dos visiones de la SF (tema `colorido`) no cambian. SmartColdBox usa `pool` en su identidad; capturas en Edge sin errores.

## Columna de herramientas (2026-10-26)

El propietario pidió «aplica también la columna de herramientas al documento de visión». La columna nació en `documento_fundacional`, con el modelo del documento de los 20 casos de referencia de OncoCore. Para no tener dos copias, el script y su estilo viven aquí (`assets/herramientas.js`, `assets/herramientas.css`) y `documento_fundacional` los lee de esta carpeta, como ya hacía con los temas. El script reconoce los dos tipos de documento (`.report-body` con bloques `.bloque`, o `main` con secciones `.seccion`) y no busca en el texto de los botones. Sin menú, el botón «Buscar» de pantalla pequeña flota abajo a la derecha. Ubicación provisional, a falta de decidir dónde va la biblioteca de herramientas reutilizables de la SF (`docs/mejora-continua.md`). Comprobado en Edge a 1920, 1300 y 390 px con las visiones de la SF y de SmartColdBox: sin errores ni desplazamiento horizontal y fuera de la impresión.

## Notas personales y versión del documento (2026-10-26)

El propietario pidió «activa la anotación del documento para que cada cual pueda guardar notas personales. Las versiones anotadas me pueden ser útiles para pasártelas y que las uses como feedback», y «normalmente en la cabecera va un número de versión (las tools gestionan la versión) y también la versión de las tools», como en `NOTAS_JS` y `bloque_version()` del kit de OncoCore. `herramientas.js` pasa a gestionar varias herramientas en la columna (buscador y notas), cada una con su modo, posición y plegado. Diferencias con OncoCore: las notas se anclan a un texto seleccionado además de a la sección; se guardan solas en el navegador; «Guardar» propone una copia con otro nombre (`.notas-<autor>.html`), para que regenerar el `.html` desde el `.md` no las borre; y `scripts/extraer_notas.py` las lista para aplicarlas. Comprobado en Edge con un fundacional y una visión: anotar, recargar, guardar (copia limpia, versión 2), abrir la copia en otro navegador con sus notas y móvil sin desplazamiento horizontal.

El propietario añadió: «no quiero perder ninguna ventaja [de ergonomía de lectura de OncoCore] y quiero sumar más en cada proyecto en base a SF» y «no todo es aplicable en todo documento, pero quiero tener la opción y que se me presente». Pendiente: inventario completo del kit de OncoCore frente a la SF y catálogo de herramientas opcionales que la skill presente al crear cada documento.

## Ventajas de OncoCore portadas y catálogo de opciones (2026-10-26)

Con el inventario completo del kit de OncoCore (v1.0.57) y de su skill `diseno_documentos` frente a la SF, se portó lo de más impacto: aspecto de tarjeta de las herramientas, asa visible, F3 / Ctrl+G, «/» que selecciona, resultado activo, «Sin resultados» en rojo, destello al saltar, anclas que abren su sección en la visión, impresión de la visión con todo abierto, una sola convención de flechas (▸ / ▾) con foco visible, enlaces externos con ↗, pie con procedencia y el registro de limpieza de la copia guardada. Herramientas v1.1.0. Lo que la SF ya hacía mejor se conserva: buscador sin tildes, memoria por documento (las claves del kit son globales), móvil sin desplazamiento horizontal e impresión sin herramientas. El resto queda en el catálogo de `documento_vision/SKILL.md` como opciones que se presentan al autor, porque «no todo es aplicable en todo documento, pero quiero tener la opción y que se me presente».

## Pendiente

- Desde el 2026-10-27 la skill vive en el plugin `sf` (`plugins/sf/skills/documento_vision/`) y ya no se copia a la global: los cambios se hacen aquí y llegan a los proyectos al publicar una versión del plugin.

## Las opciones se preguntan (2026-10-26)

Cada opción del catálogo es opcional: si el documento no la especifica, la skill pregunta al autor, con una recomendación que depende de si el artefacto es para el proyecto (manda el `.md`) o para el usuario (el `.html` es el entregable y puede editarse en su sitio). Indicación del propietario: «con opcionalidad, me refiero que el skill pregunte si no se especifica».

## Biblioteca en tools/kit_documentos y todas las opciones (2026-10-26)

La columna de herramientas y sus opciones salen de la skill y pasan a la biblioteca de la SF `tools/kit_documentos/` (ver [su procedencia](../kit_documentos.md)), que las dos skills buscan junto a `skills/`. Herramientas 1.2.0: se portan todas las opciones pendientes del kit de OncoCore, con valores iniciales según el destino del documento (`destino: proyecto|usuario`) y las de lectura ajustables por el lector. Los bloques de código llevan `data-kit` para poder actualizar copias ya repartidas.

## Dependencias: `oklch-skill` y `dataviz` (2026-11-01)

Por las decisiones 175 y 176, `oklch-skill` deja de viajar copiada en el plugin y pasa a ser una dependencia de `sf`, que se instala con él. Se invoca como `oklch-skill:oklch-skill`.

| Dependencia | Procedencia | Cómo llega | Si no está |
| --- | --- | --- | --- |
| `oklch-skill` (plugin `oklch-skill`) | [jakubkrehel/oklch-skill](https://github.com/jakubkrehel/oklch-skill), MIT, commit `0e81f040e16d48fcc61d3e1b7ea548542371321f` (2026-10-02), sin cambios. La adoptó el propietario el 2026-10-25 (decisión 002). | Una entrada del marketplace de la SF, fijada a ese commit, declarada en `dependencies` de `sf` | Se instala con `sf`. Si falta, reinstalar `sf` o instalar `oklch-skill@softwarefactory`. |
| `dataviz` (validador `validate_palette.js`) | Skill de Anthropic que trae el entorno (hipótesis: viene con Claude Code). No es un plugin, así que no puede ser una dependencia. | Requisito del entorno | Avisar al autor, comprobar el contraste y la separación entre colores vecinos con cálculo propio, también con daltonismo rojo-verde, y anotar que la serie no pasó el validador (`SKILL.md`, «serie»). |

## Destino y herramientas, preguntados; lectura por capas; siempre en claro (2026-11-01)

Tarea 204. La fase 2 pregunta el destino y las herramientas al acordar las secciones, y el generador ya no usa valores del proyecto en silencio: sin destino o sin herramientas se detiene con las opciones (`recomendadas` toma las del destino; también `--destino` y `--herramientas`). El principio «Dos niveles de lectura» pasa a «Lectura por capas, lo más importante primero». Los documentos abren siempre en claro y la opción `oscuro` del autor se retira (kit 1.9.0).

## Lo común, a `crear_documentos` (2026-11-02)

Tarea 301, decisión 232. `scripts/tema_identidad.py`, `scripts/resaltar_codigo.py` y `assets/temas/` pasan a la skill general `crear_documentos`, igual que el texto de «Temas visuales», «Logo e identidad», «CSS del proyecto» y el «Catálogo de herramientas y opciones de lectura». `doc_to_html.py` los importa desde allí. La maqueta de la visión (carcasa, `estilo_base.css`, escenas, caso conductor) se queda aquí. Las ocho visiones y explicativos de la SF regenerados salen iguales (sin contar la fecha de generación del pie).
