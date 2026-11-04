---
name: crear_documentos
description: Lo común para crear cualquier documento de la Software Factory — el generador .md → HTML, el catálogo de recursos con su sintaxis (portada, secciones plegables, recuadros, tarjetas con color, icono y plegado, columnas, fichas con buscador, preguntas con opciones, fuentes y referencias, esquemas SVG), cuándo usar cada recurso y la norma de usarlos desde la primera versión, los temas y la identidad del proyecto, las herramientas de lectura, el respaldo en _respaldo/, la impresión A4 y la comprobación en escritorio y móvil. Úsala junto a la skill del tipo de documento (documento_fundacional, informe_deliberativa, documento_vision…), y también para crear un tipo de documento nuevo, añadir o cambiar un recurso, un tema o la identidad de un proyecto, o generar, respaldar y comprobar el HTML de un documento.
---

# Crear documentos

Esta skill reúne lo común a todos los documentos de la SF. Encima van las **skills de cada tipo de documento**: cada una dice para quién es su documento, qué secciones lleva y con qué tono, cómo se crea (fases, diálogo con el autor, revisión) y qué recursos de este catálogo usa. Un recurso nuevo mejora todos los documentos a la vez, y crear un tipo de documento nuevo es escribir solo lo suyo («Una skill general de diseño de documentos, y skills de contenido encima», decisión 232).

Comunicar bien es un objetivo de la SF: la usabilidad de los documentos no es un adorno (decisión 231).

## Tipos de documento

| Tipo | Skill | Generador | Recursos |
| --- | --- | --- | --- |
| Documento fundacional | `documento_fundacional` | `scripts/fundacional_to_html.py` de su skill | Su `perfil.json` |
| Informe de una tarea deliberativa | `informe_deliberativa` | `scripts/informe_to_html.py` de su skill | Su `perfil.json`, con las preguntas |
| Visión y documentos explicativos («Cómo funciona…») | `documento_vision` | `scripts/doc_to_html.py` de su skill, con maqueta propia | Escenas, caso conductor y bloques plegables propios; temas, identidad y herramientas de esta skill |

El fundacional, los informes y los tipos que vengan usan el **generador común** de esta skill, `scripts/documento_a_html.py`, con su **perfil**. La visión conserva su maqueta (carcasa, escenas, caso conductor), que es propia de su forma narrativa; de esta skill toma los temas, la identidad, las herramientas y el coloreado de código.

### El perfil de un tipo de documento

Cada skill de tipo lleva un `perfil.json` en su carpeta:

```json
{"tipo": "Documento fundacional", "descripcion": "…", "recursos": ["tarjetas", "columnas", "fichas", "fuentes"], "css": [], "js": []}
```

- `tipo`: el nombre por defecto del tipo (pie y título de la pestaña), si la cabecera del `.md` no da otro.
- `recursos`: los bloques del catálogo que usa (`tarjetas`, `columnas`, `fichas`, `preguntas`, `fuentes`). Así un tipo elige: un documento técnico puede usar recursos que uno para usuarios no usa. Si el `.md` usa uno que no está, el generador se detiene y lo dice. Sin `recursos`, todos.
- `css` y `js`: recursos propios del tipo, con rutas relativas al perfil. Van después de los comunes y antes de los del proyecto, con su marca `data-kit` para que `actualizar_copia.py` los ponga al día.

Su generador es un envoltorio de pocas líneas que llama a `documento_a_html.py` con `--perfil`; el del fundacional sirve de modelo.

### Crear un tipo nuevo

1. Una skill con su `SKILL.md`: para quién es, sus secciones, su tono, cómo se crea y qué recursos usa y por qué.
2. Su `perfil.json` y su envoltorio en `scripts/`.
3. Lo que necesite y sirva a otros tipos se añade a este catálogo, no a su skill. Lo que solo le sirve a él va en su `css` o `js`.
4. Una prueba en `plugins/sf/tests/` y un ejemplo generado.

## Catálogo de recursos

La sintaxis es la del `.md` que lee `documento_a_html.py` (Markdown con `attr_list`, `def_list`, `md_in_html` y tablas). Cada recurso dice para qué sirve; «Cuándo usar cada recurso», más abajo, dice cuándo conviene.

### Cabecera de datos

Entre dos líneas `---`, al principio; todo es opcional:

- `antetitulo`: línea pequeña sobre el título. Con ella, el nombre es el titular y el lema va debajo; sin ella, el lema es el titular.
- `lema`: `//` fuerza el salto de línea; sin él, cada frase va en su línea.
- `subtitulo`, `pie`.
- `version`, `estado`: van al pie, no a la portada.
- `tipo`: el tipo de documento; por defecto, el del perfil.
- `portada`: `oscura` para la portada sobre el color oscuro del tema.
- `destino` y `herramientas`: ver «Herramientas y opciones de lectura». Sin ellos, el generador se detiene con las opciones.
- `menu`: por defecto, el menú fijo lleva solo los botones («Buscar» en pantallas estrechas, «Plegar todo» e «Imprimir / PDF»). Con la columna de herramientas, «Plegar todo» e «Imprimir» pasan a la barra de «Guardar» como iconos y el menú vacío se oculta. `secciones` añade los enlaces a las secciones; `no` quita el menú.

```markdown
---
antetitulo: Proyecto · Documento fundacional · Octubre 2026
lema: Primera línea del lema, // segunda línea.
subtitulo: Qué es, en una línea.
version: Versión 1.0 · 22/10/2026
estado: Foco inicial · Documento de proyecto
portada: oscura
destino: proyecto
herramientas: recomendadas
pie: Texto del pie: qué distingue el documento y quién decide.
---
# Nombre del producto

> **Alcance**
> Aviso que se aplica a todo el documento (opcional).

## Etiqueta | Título | Menú {#id}

Primer párrafo: la entradilla, más grande.
```

### Portada, avisos y secciones

- **Portada sobria:** marca (logo y antetítulo), titular y lema; nada más, para que la cabecera sea baja. La versión y el estado van al pie.
- **Avisos de alcance global:** las citas `>` entre el `# Nombre` y la primera `##` van al principio, fuera de toda sección, como recuadro.
- **Secciones:** `## Etiqueta | Título | Menú {#id}`. La etiqueta sale como «01 / ETIQUETA» y el título es el `h2`. El texto de menú solo se usa con `menu: secciones`. El `{#id}` sirve para enlazar la sección. Cada sección es plegable (`assets/plegado.js`): solo la primera está abierta al cargar, un enlace interno abre la de destino y al imprimir se abre todo.

### Párrafos

- El primer párrafo de una sección es la **entradilla**. `{: .texto}` debajo lo deja como texto normal.
- `{: .nota}` letra pequeña.
- `{: .lectura}` párrafo con un filete encima.
- `{: .formula}` fórmula en bloque.
- `{: .etiqueta-tarjeta}` etiqueta pequeña que sube encima del título de su tarjeta.
- `**9.343 €** 43 unidades` y `{: .metrica}` debajo: cifra grande con su pie.

### Recuadros

- `> **Etiqueta**` y el texto en la línea siguiente: recuadro con etiqueta.
- `> **Frase en negrita.** texto` en la misma línea: recuadro sin etiqueta. Se evita, porque el párrafo arranca en negrita: mejor con etiqueta.
- `> [!aviso]` en la primera línea: aviso, en el color de acento.
- `> [!decision]` en la primera línea: decisión, sobre fondo oscuro.
- `> texto` sin negrita: cita destacada.

### Campos

`Campo` y, debajo, `:   texto` (lista de definición) dan los campos de una tarjeta, una ficha o un apartado, con rótulo pequeño y filete. El texto empieza sin negrita.

### Bloques

Los bloques empiezan con `::: tipo` y acaban con `:::`, y se pueden anidar.

- **`::: tarjetas 3`** es una rejilla de 1, 2 o 3 columnas. Cada tarjeta empieza en un `###` (o en un `####`, si la primera lo usa).
- **Tarjetas plegables:** `::: tarjetas 3 plegables` hace cada tarjeta un `<details>`: la cabecera con el título se ve siempre; se abren en pantallas anchas, se pliegan al cargar en el móvil y se abren al imprimir. Para tarjetas largas que en el móvil harían una columna interminable. Un bloque con dos o más tarjetas plegables (también preguntas y fichas) lleva delante el botón «Plegar las tarjetas / Desplegar las tarjetas» (`assets/plegado.js`), que no sale al imprimir ni en la copia guardada.
- **Tarjetas con color e icono:** `### Título {color=turquesa icono=codigo}` en el título de una tarjeta le da una cabecera con ese color de fondo y el icono; con `{: #id}` detrás, su ancla. Colores: `turquesa`, `naranja`, `verde`, `frambuesa` o `#rrggbb`. Iconos: `codigo`, `dialogo`, `documento`, `rama`, `carpeta`, `lupa`, `check`, `aviso`, y los propios del proyecto (ver «Identidad del proyecto»). Dentro, los campos llevan la marca del color, y un campo cuyo valor es una lista corta (`:   - uno` y `    - dos`) sale en chips.
- **`::: columnas`** son columnas separadas por una línea `|||`, por ejemplo dentro de una tarjeta.
- **`::: fichas 2`** son tarjetas con buscador de texto y filtro por insignias (`assets/fichas.js`). Al buscar un texto, las fichas plegables que coinciden se abren.
- **`::: preguntas 2 plegables`** son preguntas con opciones, para lo que el lector tiene que decidir. Cada pregunta es una tarjeta con cabecera que empieza en su título, con sus opciones como campos (`Opción A` / `:   …`), el campo `Recomendación` y, si ya se decidió, el campo `Decisión`. En el título, entre llaves:
  - `recomendada=A`: la opción recomendada, que se destaca con un filete y la marca «Recomendada»;
  - `estado=abierta` (por defecto), `estado=decidida elegida=B` (la elegida lleva su marca y las demás pasan a gris) o `estado=separada destino=tarea_303` (el `_` se lee como espacio). El estado sale como marca en la cabecera, sin los colores de la serie, que en el documento ya significan otra cosa;
  - `icono=…`, como en las tarjetas.

  El generador se detiene si la recomendada o la elegida no son una de las opciones, y avisa de una pregunta abierta sin recomendación. Con su `{: #pN}` detrás, cada pregunta se enlaza desde el resumen, las separaciones y los pasos de las tareas. Ejemplo y reglas de redacción, en `informe_deliberativa` («Las preguntas»).
- **`::: fuentes`** es la lista de fuentes: un párrafo por fuente con `{: #src-E1}` debajo.

### Enlaces

- `[[E1]](#src-E1 "Fuente, año"){: .ref}` es una referencia a una fuente.
- `[S2](#S2){: .insignia}` es una insignia: un código que lleva a su definición. El filtro de las fichas las usa: sin más, con su código y el título de su destino. Con `data-filtro`, la insignia da su propia etiqueta para el filtro, o varias separadas por `;` cuando lleva a más de un sitio: `[S2](#S2){: .insignia data-filtro="Conservación; Transporte"}` (la ficha sale al filtrar por cualquiera de ellas).
- `{: .salto}` es un enlace pequeño a otra parte.

Los títulos aceptan `{: #id}` (`### S2 · Conservación domiciliaria {: #S2}`).

### Esquemas

Un SVG en el propio `.md`, dentro de `<figure class="vertical">` y con un `<figcaption>` breve en cursiva que diga qué hay que ver. Norma de la SF para todo documento, tenga el proyecto metodología o no: todo esquema es SVG inline, nunca ASCII ni mermaid. La guía común es `../metodologia/references/diagramas-svg.md`, que viaja en el plugin con la skill `metodologia` y se lee aunque el proyecto no la use: cuándo dibujar, forma vertical de 560 de ancho, estilo ligero, color con significado, accesibilidad y revisión. En el generador común:

- títulos de 18 y detalle de 15 como mínimo;
- colores y letra del tema con `style`: `fill:var(--primario)`, `var(--oscuro)`, `var(--texto-suave)`, `var(--linea)`, `var(--fondo)`, y `style="font-family:var(--fuente-texto)"` en el `<svg>`. Sin fondo propio: en modo oscuro se invierte con la página;
- lo que existe, con trazo continuo y el primario; lo previsto o futuro, con trazo discontinuo y gris;
- `role="img"` y `aria-label` (o `<title>`) con lo que dice el esquema;
- **nada que no esté también en el texto**: el buscador de las herramientas no entra en los SVG, así que una cifra, un nombre o una condición que solo esté en el esquema no se encuentra. El esquema muestra lo que el texto ya dice.

Dentro de un bloque HTML del `.md` no se dejan líneas en blanco: el conversor de Markdown lo cortaría.

### Lector de libros

Para contar una historia como un libro (la opción novela de los documentos de visión, o cualquier documento que lo pida). El generador lo añade solo cuando el documento lleva `class="libro"` o `class="lector"`: estilo en `assets/lector.css` y script en `assets/lector.js`.

```html
<div class="lector" data-titulo="El verano de Marc · prólogo" data-al-abrir="historia" data-marca="/SF"
     data-invitacion="Pulsa el logo… para vivir, con…, qué cambia cuando…" style="--lector-marca:#827dbd;--lector-marca-claro:#b3aee6">
<div class="libro">
<p class="libro-capitulo">Prólogo</p>
<p class="libro-titulo">Tres días para el jueves</p>
<p>Primer párrafo, con capitular…</p>
<p class="libro-ornamento"></p>
<p>…</p>
</div>
</div>
```

- **`.libro`**: una página de ebook: columna estrecha, letra serif de lectura, encabezado de capítulo (`.libro-capitulo`), título (`.libro-titulo`), capitular en el primer párrafo, sangría y separador (`.libro-ornamento`). Sola, se ve como una página en el documento.
- **`.lector`**: la página dentro de un lector electrónico que pagina (botones ‹ ›, zonas de toque, deslizar, flechas del teclado y «Página 1 de N»). **Conserva siempre el aspecto de ebook**: en móvil, a pantalla completa; en tableta y escritorio, el aparato de 6-7" a escala, con su marco, la pantalla de tinta en 3:4, centrado y con un fondo sobrio. Sin JS o al imprimir, el texto se ve seguido.
- **Tinta electrónica**: papel gris cálido y mate, tinta negra con algo de grano, sin sombras, degradados ni colores; en el modo oscuro de «Lectura» no se invierte. Al pasar página, un destello oscuro breve encima de la página nueva, que se pinta ya; sin él con movimiento reducido. **El paso es inmediato siempre**: nada de filtros ni sombras de texto que obliguen a repintar la página, y los efectos con Web Animations, sin forzar el diseño. Un ajuste en el marco (▣ / ❏) cambia el paso a **hoja de papel**, que gira desde el lomo; la elección se recuerda en el navegador.
- **La historia completa**: con un `.lector` y al menos dos partes narrativas (`.libro`, `.caso` y `.escena`, salvo las que estén dentro de `data-historia="no"`), aparece «Leer la historia completa». Abre un lector a pantalla completa con todas ellas seguidas, por capítulos, con su índice y la página de cada uno; se cierra con Esc o con ×, y al terminar, con «Ver el documento». Sale del mismo texto: nada se duplica en el `.md`.
- **`data-titulo`**: el rótulo del marco.
- **`data-marca`** (y, si se quiere, `--lector-marca` y `--lector-marca-claro` en `style`): la marca del proyecto en el marco, como el logo de un aparato. Lo que va antes de la primera letra o cifra (la barra de «/SF») sale en `--lector-marca-claro` y el resto, en `--lector-marca`: en la SF, `--lector-marca:#827dbd;--lector-marca-claro:#b3aee6`, los colores de su logo (decisión 255).
- **`data-al-abrir="historia"`**: el documento se abre en la historia completa, a pantalla completa y sin nada encima.
- **Pantalla de entrada** (con `data-al-abrir` y `data-marca`), como el encendido del lector. **Anuncia el tema del documento, no la marca**: arriba, el tema y su subtítulo (`data-tema` y `data-subtitulo`; por defecto, el título del documento partido por sus dos puntos); en medio, el logo en sus colores con un **latido** (un halo suave que respira lento, unos 2 s, siempre visible y que es también su señal de foco; fijo con movimiento reducido); debajo, la invitación (`data-invitacion`); y abajo, en letra pequeña, el **aviso de ficción** (`data-aviso`; por defecto, «Historia de ficción: personajes y escenas son imaginados.»; vacío, sin aviso). Pulsar el logo, o Intro o espacio sobre él, lleva a la página 1.

### Componentes propios del proyecto

HTML en bruto dentro del `.md` (por ejemplo, una calculadora), con su CSS y su JS en la identidad del proyecto (`identidad.json`: `"css"` y `"js"`).

## Cuándo usar cada recurso

Estas reglas valen para cualquier documento que use el catálogo. La skill de cada tipo añade las suyas.

### Desde la primera versión

**Todo documento sale ya con sus recursos en la primera versión, sin esperar a que el propietario los pida: nada monótono** (decisión 231). Un primer borrador de prosa seguida, que se maqueta después, no se entrega. Al proponer el índice se dice qué recurso lleva cada sección, y al escribir se aplican estos criterios:

- **Esquema SVG del proceso** cuando el documento cuenta un proceso, un ciclo, un recorrido, unos estados o una estructura de tres partes o más que se relacionan: al menos uno, en la sección que da la visión de conjunto (el resumen o la primera). Vale para todo documento, **con o sin metodología** en el proyecto: la guía de diagramas viaja en el plugin (ver «Esquemas»).
- **Tarjetas** para tres o más elementos paralelos con la misma estructura; **con color e icono** cuando son de familias o tipos que conviene distinguir. Los bloques de tarjetas de un documento no son todos iguales: se combinan tarjetas con color, columnas, fichas, preguntas y métricas según el contenido.
- **Plegables para el móvil:** un bloque de cuatro tarjetas o más, o con tarjetas de más de unas 80 palabras, lleva `plegables`. El detalle que no sostiene el argumento de la sección va en `####`, plegado, o a un anexo.
- **Secciones largas, partidas:** una sección de más de unas 500 palabras, o con más de tres temas, se parte en secciones propias o en apartados `###` con el detalle plegado. Ninguna sección es un bloque de prosa de más de cinco párrafos seguidos sin un recurso que la corte (esquema, tarjetas, recuadro, tabla o métrica).
- **Recuadro** para la decisión propuesta y para el aviso que no puede pasar desapercibido; **métrica** para la cifra que sostiene el argumento; **tabla** para comparar en filas.
- **Variedad:** dos secciones seguidas no repiten el mismo recurso principal, y en un documento de cuatro secciones o más se usan al menos tres recursos distintos además de la prosa.

Son mínimos para la primera versión, no un adorno: cada recurso sigue justificándose por su contenido con las reglas de abajo. Si un criterio no aplica (un documento sin proceso no lleva esquema), se omite sin forzarlo.

### Reglas de cada recurso

- **Lectura por capas.** Lo más importante primero, y cada capa siguiente profundiza: quien solo lee la primera se lleva lo esencial. El orden es de importancia, no el de cómo se llegó a las conclusiones. Cada sección abre con su conclusión y deja el detalle a las tarjetas, los `####` plegados y los anexos.
- **Cada sección abre con prosa que argumenta**, antes de cualquier tarjeta: la conclusión, los hechos que la sostienen y lo que falta por saber. Una frase de presentación («Seis experiencias permiten…») no basta. Las tarjetas vienen después y aportan el detalle que se consulta, sin repetir el argumento.
- **Tarjetas** solo cuando están justificadas: elementos paralelos, con la misma estructura y que se consultan por separado, también cuando son pocos. Una tarjeta que no es del mismo tipo que las demás de su bloque sale del bloque. Una lista de viñetas corta la lectura igual que las tarjetas y se ve peor: no se cambian tarjetas por viñetas.
- **Color en las tarjetas** para elementos paralelos que conviene distinguir de un vistazo (familias, tipos, perfiles), no para decorar. **Mismo color, mismo significado** en todo el documento, en tarjetas y en esquemas: si el turquesa es el código en una tarjeta, es el código en el esquema. Los cuatro colores con nombre son la serie validada de la guía de diagramas (`diagramas-svg.md`, «Color, iconos y letra»), con el mismo valor allí y aquí.
- **Prosa** cuando el contenido se lee seguido: los pasos de un razonamiento, una gradación, respuestas o principios de una frase. Si las partes son largas, cada una lleva su subtítulo pequeño (`####`). **El párrafo empieza con el texto**, sin una etiqueta en negrita delante.
- **Apartado normal** (`###`) en lugar de una tarjeta única que solo enmarca prosa.
- **Recuadros** para lo que no puede pasar desapercibido (avisos) y para la decisión propuesta; nunca para lemas o principios de manifiesto.
- **Tablas** solo para datos que se comparan en filas.
- **Lista de viñetas** para muchos elementos cortos, de una o dos frases, que no merecen tarjeta. Con moderación.
- **Ningún recurso se repite sección tras sección**, ni van dos bloques de tarjetas seguidos: se alternan prosa, tarjetas, listas y tablas según lo que pide cada contenido.
- **Sin avisos sobre cómo leer o cómo razonar** («Cómo leer los costes»): son reglas para quien escribe y se aplican en el texto.
- **Negrita con moderación, dentro de la frase**, nunca al abrir el párrafo.
- **Campos repetidos, como lista de definición.** Una etiqueta que no se repite se integra en la frase. En un recuadro, la etiqueta va sola en su primera línea.
- **Tipografía.** Comillas «» o “”, nunca rectas; puntos suspensivos de un solo carácter (…); espacio duro (U+00A0) entre la cifra y su unidad (35 °C, 82 %, 9.343 €) y tras «≈». Nada en mayúsculas para enfatizar: las versalitas de los rótulos las pone la hoja de estilos. Los títulos no saltan niveles y, bajo un `###`, las tarjetas empiezan en `####`.
- **Sin códigos que el lector aún no conoce.** Un código interno (S1, P3…) solo se usa después de la sección que lo define.
- **Solo la última decisión** y **sin paja**: nada sobre el propio documento ni obviedades.

## Temas e identidad

### Identidad del proyecto

Cada proyecto guarda su identidad en `doc/identidad/` o `docs/identidad/`, con un `identidad.json` que el generador busca subiendo carpetas desde el `.md`. Las rutas son relativas a esa carpeta. Claves:

- `tema`: nombre de un tema de esta skill (`assets/temas/`) o ruta a un tema propio (`.json`).
- `logo`: imagen de la cabecera.
- `producto`: nombre del producto, para la cabecera y el pie.
- `tipo`: tipo de documento por defecto, para el pie.
- `css` y `js`: hojas y scripts (o listas) de los componentes propios del proyecto. Pueden usar las variables del tema.
- `reglas`: archivo Markdown con las reglas de redacción del dominio y la explicación de sus componentes. No lo usa el generador: lo lee quien redacta.
- `destino` y `herramientas`: los de todos los documentos del proyecto.
- `iconos`: iconos propios para las tarjetas y las preguntas (`{icono=…}`), que se suman a los de la skill: nombre → trazos SVG de una caja de 24 × 24 (`"<path d='…'/>"`) o ruta a un `.svg` de la carpeta, del que se toma lo de dentro del `<svg>`. Se dibujan con trazo de 2 en el color de la cabecera, como los de la skill.

```json
{"tema": "rojo", "logo": "emblema.png", "producto": "Producto · Organización", "css": "componentes.css", "reglas": "reglas-vision.md",
 "iconos": {"cohete": "<path d='M12 2l4 8H8z'/>", "planta": "iconos/planta.svg"}}
```

### Temas, logo y CSS del proyecto

El código común está en `scripts/tema_identidad.py`: temas, identidad, herramientas, procedencia del pie y enlaces externos. Las referencias a la hoja de estilos (`estilo_base.css`, `.bloque-…`) son de la maqueta de la visión; en el generador común, las mismas variables del tema.

- **Temas visuales** (`assets/temas/<nombre>.json`). Los temas tienen nombres genéricos, por su color (`morado`, `rojo`, `teal`, `colorido`, `pool`), no por la organización que los inspiró, para reutilizarlos en cualquier proyecto. Un tema propio de un proyecto puede vivir en su carpeta de identidad (`"tema": "mi-tema.json"`). Un tema define `nombre`, `descripcion`, `colores` y, si se quiere, `tipografias` (`texto`, `titulos`, `escena` y la `url` de Google Fonts, vacía si el tema usa las fuentes del sistema; por defecto, las del tema `morado`). Cada color es un rol que la hoja de estilos usa como variable CSS: `primario`, `oscuro`, `primario-vivo`, `fondo`, `borde`, `linea`, `fondo-medio`, `fondo-suave`, `tenue`, `pagina`, `texto`, `texto-suave`, `texto-tenue`, `acento`, `acento-fondo` y `acento-borde`; las tipografías, `--fuente-texto`, `--fuente-titulos` y `--fuente-escena`. Solo `primario` es obligatorio: los demás se derivan mezclándolo con blanco o negro (`DERIVADOS` en `scripts/tema_identidad.py`), y `texto` y `acento` toman por defecto los del tema `morado`. Para imitar una identidad con exactitud, se dan todos los roles.
  - **`serie`** (opcional): una lista de colores (`#rrggbb`). Cada bloque (H2) toma uno, en ciclo, con sus fondos y bordes derivados, y sus gráficos lo siguen. Los colores de una serie deben tener contraste suficiente sobre blanco (4,5:1 o más), porque se usan también como color de texto. **Para crear una serie**, seguir la skill `oklch-skill:oklch-skill`, dependencia de `sf` (todos los colores con la misma luminosidad OKLCH y el mismo porcentaje de su croma máximo), comprobar el contraste de cada color sobre blanco y sobre el fondo de su bloque, y pasar el orden por el validador de paletas de la skill `dataviz` (`validate_palette.js "<hex,…>" --mode light`) hasta que no dé fallos, añadiendo al final el primer color, porque la serie vuelve a empezar. `dataviz` es un **requisito del entorno**: no es un plugin, no viaja con la SF ni se instala con ella. Si no está en la sesión, decírselo al autor, comprobar el contraste de cada color con un cálculo propio y, entre colores vecinos (también del último al primero), que se distinguen con visión normal y con daltonismo rojo-verde, y anotar que la serie no pasó el validador. Con la misma luminosidad, rojos, naranjas, verdes y rosas solo se distinguen en el eje rojo-verde: para quien tiene daltonismo rojo-verde se separan intercalando colores fríos (azules, turquesas). Preguntar al autor si hay colores que no quiere.
  - **`estilo`** (opcional) cambia el aspecto: `cabecera` (`blanca`, `primario` u `oscuro`: franja de color con texto blanco), `etiqueta` del bloque (`tinte`, `solida` con texto blanco, o `linea` lateral), `marcador` (`circulo`, `cuadrado` o `ninguno`), `esquinas` (radio en píxeles; queda también en la variable `--esquinas` para el CSS del proyecto) y, con etiqueta `solida`, `opacidad`: de 0.75 a 1, título blanco (por debajo de 1, grande y en negrita, para el que WCAG pide 3:1); de 0.2 a 0.5, título en el color oscuro del bloque (4,5:1 o más). Entre 0.5 y 0.75 no se lee bien ninguno de los dos y el script lo rechaza. Con opacidad menor que 1, los botones van sobre blanco. Sin `estilo`, el aspecto es el del tema `morado`.
  - **Cada tema debe distinguirse de los demás a primera vista**, no solo por el color: combinar tipografías y opciones de `estilo` distintas. Los colores neutros (blancos, grises, avisos) son fijos.
- **Temas disponibles:**
  - **`morado`** (por defecto), moderno y sereno: cabecera blanca, etiquetas suaves con marcador circular, esquinas redondeadas; morado `#7B2CBF` con acento ámbar `#B45309`; DM Sans, Space Grotesk y Source Serif 4.
  - **`rojo`**, institucional: cabecera en franja oscura, bloques con línea lateral y marcador cuadrado, esquinas casi rectas, títulos con serifa (Source Serif 4) y texto en Source Sans 3; rojo `#C62A1F` (oscurecido para buen contraste), negro casi puro `#1D1D1B` como oscuro y texto, fondos rosados muy claros (`#FDF1EF`) y acento ámbar.
  - **`colorido`**, desenfadado: etiquetas de bloque en color al 40 % de opacidad con título grande en el color oscuro del bloque, sin marcador, esquinas muy redondeadas; seis colores sin morados y con la misma luminosidad (azul, naranja, turquesa, rojo, azul cielo, verde), uno por bloque y en ciclo, también en sus gráficos. Alterna fríos y cálidos para que se distingan con daltonismo; fondos generales en gris neutro, acento frambuesa `#BE185D`, títulos en Outfit.
  - **`pool`**, técnico y limpio: cabecera en franja azul marino, etiquetas suaves con marcador cuadrado, esquinas de 12 px; verde azulado `#08786F` y azul marino `#112F40`, con menta `#E3F2EC`, papel `#F3F6F5` y acento dorado `#B36E1D`; fuentes del sistema, sin descargas. Trae serie de seis colores para gráficas.
  - **`teal`**, sobrio: cabecera en franja de color, etiquetas suaves sin marcador, esquinas medianas; verde azulado `#00726B` con acento violeta `#6D28D9` y tipografía Assistant.
- **Logo e identidad de cada proyecto.** El logo no viaja con la skill: vive en la carpeta de identidad del proyecto (ver «Identidad del proyecto»). Si el proyecto no tiene identidad, se crea al definirla: `identidad.json`, el logo si lo hay y, si hace falta, el CSS y las reglas. Cuando el documento se dirige a una organización concreta, **primero se pregunta al autor**, en una sola pregunta con opciones: si quiere imitar la identidad de la organización o usar un tema genérico, de qué tema parte (con su aspecto en una línea), si hay colores que no quiere y si se usa el logo de la organización. Con su respuesta, se investiga su identidad en su web: se descarga el logo al proyecto, se extraen sus colores del propio logo o de la hoja de estilos y se elige el tema genérico que mejor encaje o se crea uno nuevo (el primario oscurecido si hace falta para que el texto tenga contraste). Un tema nuevo va a `assets/temas/<color>.json` si sirve a cualquier proyecto, o a la carpeta de identidad si es propio. Si el logo publicado lleva elementos temporales (un lazo de luto, sellos de programas), se usa solo el emblema. Conviene dejar en la carpeta un `identidad.md` breve con el origen del logo y la orden para generar.
- **CSS del proyecto.** Se añade al final, después del tema, así que puede ajustar cualquier cosa. Debe usar las variables del tema (`var(--primario)`, `var(--fuente-titulos)`, `var(--esquinas, 4px)`…) para seguir funcionando si el proyecto cambia de tema.

## Herramientas y opciones de lectura

La ergonomía de lectura de los documentos es una ventaja que no se pierde y que suma en cada proyecto. No todo sirve en todos los documentos, así que **cada opción del catálogo es opcional: si el autor no la ha especificado, se le pregunta**, al crear o revisar el documento, con una recomendación para ese documento, y se anota su elección. No se activa ni se descarta nada en silencio.

Todo vive en la biblioteca de la SF `tools/kit_documentos/` (`herramientas.js`, `lectura.js`, `edicion.js`, `herramientas.css`, `extraer_notas.py`, `actualizar_copia.py`), junto a `skills/`, dentro del plugin `sf` (`plugins/sf/tools/kit_documentos/` en el repositorio de la SF). El catálogo, con sus valores iniciales, está en `HERRAMIENTAS` de `scripts/tema_identidad.py`. Lo comparten todos los documentos de la SF. Lo que se cree en un proyecto y sirva a otros se trae a la biblioteca.

**Primero se pregunta para quién es el artefacto** (`destino:`), porque cambia los valores iniciales:

- **`proyecto`**: el `.md` es el original y el `.html` se regenera desde él. Lo que el lector cambie se recoge y se lleva al `.md` con `extraer_notas.py`.
- **`usuario`**: el `.html` es el entregable que el usuario se queda y trabaja, y puede tener poca relación con el `.md` del que salió. Aquí tienen sentido la edición del párrafo en su sitio, convertir una nota en párrafo y guardar sobre el mismo archivo.

**Cómo se anota.** En los documentos del generador común (fundacional, informes…), `destino:` y `herramientas:` en la cabecera del `.md`; en la visión, comentarios al principio del `.md` (`<!-- destino: usuario -->`, `<!-- herramientas: … -->`); para todo el proyecto, `"destino"` y `"herramientas"` en `identidad.json`. También con `--destino` y `--herramientas` al generar, que mandan sobre el resto. `herramientas:` admite `recomendadas` (las del destino), la lista completa, `todas`, `ninguna` o cambios sobre los valores del destino (`+acordeon -tablas`, `todas -edicion`). **Si falta el destino o las herramientas, el generador se detiene** y enseña las opciones y el catálogo, con la recomendación para cada destino: no elige por el autor. Se le pregunta y se anota.

**Opciones y valores iniciales** (proyecto / usuario; «el lector lo ajusta» = aparece en «Lectura» con el valor del autor como punto de partida, y se recuerda en su navegador):

- `buscador` (sí / sí): buscar en el documento.
- `notas` (sí / sí): notas personales, barra con la versión y «Guardar». Las notas son de tres clases, que se eligen por separado según para qué se quieran:
  - `nota-texto` (sí / sí): comentar un texto seleccionado con «Anotar»;
  - `nota-seccion` (sí / sí): una nota por sección, sin botones para crearla. En la columna no hay panel común: cada nota es su propia tarjeta, con el aspecto de una herramienta (título en versalitas, flecha, texto amplio y «Convertir en párrafo»). Aparece sola la de la sección que se lee (y las de las secciones que la contienen), plegada si está vacía; dentro van también los comentarios sobre textos de esa sección. Lo escrito se ve, solo para leer, en un recuadro al final de la sección, que no se imprime ni se guarda en la copia;
  - `nota-global` (sí / sí): una nota general de todo el documento, siempre arriba del panel, para la valoración de conjunto.
  Al final, la tarjeta «Tus notas · N», plegada, con el nombre para firmar y el resumen por sección, que lleva a cada nota.
  Las notas abiertas se reparten el alto libre de la columna (entre 12em y el 60 % de la pantalla). Con la columna, la barra de «Guardar» es su primera tarjeta; sin ella, va en el menú. El engranaje de «Lectura» abre la barra por la izquierda, separado de los botones. A la izquierda de «Guardar» van, como iconos sin caja, «Plegar todo» e «Imprimir» (si el documento los tiene en el menú, que entonces se oculta). La versión del documento y la del kit están al pie del modal de «Lectura». El estado está en el rótulo emergente de «Guardar»; si hay cambios sin guardar, lo indica un led rojo en el botón.
  - `nota-a-parrafo` (no / sí): «Convertir en párrafo» lleva el comentario de una nota al documento, tras el texto anotado o al final de su sección, con «Añadido · fecha» y «Retirar». No necesita `edicion`, y la nota general no se convierte. En los del proyecto manda el `.md`, como con la edición.
  Por ejemplo, `todas -nota-texto` deja solo la general y las de sección. Si un documento no nombra ninguna de las tres, tiene las tres. `extraer_notas.py` lista primero la general.
- `lectura` (sí / sí): «Lectura», donde el lector ajusta las opciones ajustables. Es configuración, no una herramienta de trabajo: no va en la columna, sino en un modal que abre el engranaje del extremo izquierdo de la barra (o en el menú si no hay barra). Al pie del modal van la versión del documento y la del kit.
- `fuentes` (sí / sí; el lector lo ajusta): al pasar por una referencia `[E1]`, bocadillo con la fuente y la frase que respalda resaltada.
- `cabecera` (sí / sí; el lector lo ajusta): el título de la sección abierta se queda arriba, bajo el menú, mientras se lee.
- `tablas` (sí / sí): ancho de las columnas de tabla ajustable arrastrando su borde; doble clic, el de partida. No actúa en móvil, donde las tablas son fichas.
- `aviso` (sí / sí): aviso al cerrar solo si hay cambios que se perderían (párrafos editados o añadidos); las notas ya quedan en el navegador.
- `leyenda` (no / sí): «Cómo leer este documento» al principio, plegada, con una muestra de cada cosa que el documento usa. El autor conoce sus convenciones; el lector externo, no.
- `edicion` (no / sí): editar un párrafo en su sitio (lápiz, formato básico, Intro aplica, Esc cancela), con «Modificado · fecha» y el texto anterior en su ayuda, y «Restaurar el original». «Convertir en párrafo» es la opción aparte `nota-a-parrafo`. En los del proyecto manda el `.md`.
- `mismo-archivo` (no / sí): «Guardar» escribe sobre el mismo archivo y, tras la primera vez, no pregunta. En los del proyecto se guarda una copia aparte (`<nombre>.notas-<autor>.html`), para que regenerar el `.html` no la borre.
- `acordeon` (no / no; el lector lo ajusta): un solo bloque abierto a la vez. Por defecto no, porque comparar secciones es frecuente.
- `bocadillos` (no / no; el lector lo ajusta): en la visión, los subapartados de detalle (`####`) se abren en un bocadillo sobre el texto, sin desplazarlo.

**Modo claro siempre al abrir.** Los temas están pensados en claro y para imprimir. En «Lectura» el lector elige oscuro (invierte la página y deja imágenes y gráficos con sus colores) o el del sistema, y se recuerda por documento. El autor no puede hacer que abra en oscuro.

**Siempre activas**, porque no tienen contra:

- columna de herramientas anclable y despegable, con ancho ajustable, asa visible y plegado de cada herramienta, recordados por documento;
- tarjetas de herramienta con franja de color, fondo tintado y sombra del tema;
- buscador sin tildes ni mayúsculas, F3 / Ctrl+G y Mayús para el anterior, «/» enfoca y selecciona, resultado activo marcado en la lista, «Sin resultados» en rojo, destello de la sección al saltar;
- enlaces internos y `#ancla` en la dirección que abren la sección de destino; impresión con todo abierto y sin herramientas;
- una sola convención de flechas: ▸ plegado, ▾ abierto; foco visible en todo lo que se pulsa;
- enlaces externos que se abren aparte y lo dicen con ↗;
- pie con la procedencia: fecha de generación, fuente, huella del `.md`, commit y aviso de cambios sin commit;
- en la copia guardada, cada herramienta limpia su estado (`window.alCopiarDocumento`), y las que cambian el documento lo avisan (`window.marcarCambiosDocumento()`);
- cada bloque de código del kit lleva `data-kit` con su ruta: `python tools/kit_documentos/actualizar_copia.py <copia>.html [--comprobar] [--herramientas "…"]` pone al día las herramientas de una copia ya repartida sin tocar su contenido, y guarda el original en `copias/`;
- `python tools/kit_documentos/extraer_notas.py <copia>.html` lista las notas por sección, los párrafos modificados (antes y ahora) y los añadidos, para llevarlos al `.md`.

Al cambiar cualquier archivo de la biblioteca se sube `VERSION` en `herramientas.js`, que la barra del documento muestra.

## Generar

```bash
python -I -X utf8 <skills>/<skill del tipo>/scripts/<generador>.py <documento>.md
```

El generador de cada tipo llama a `scripts/documento_a_html.py` con su perfil. Escribe el `.html` junto al `.md`; el `.md` es la fuente y el `.html` no se edita a mano. Opciones: `--tema`, `--identidad <carpeta>|ninguna`, `--logo <ruta>|ninguno`, `--producto`, `--tipo`, `--destino`, `--herramientas`, que mandan sobre la cabecera y la identidad. Paquetes de Python: `markdown` y Pillow (solo si hay logo).

**Avisos.** Markdown deja pasar el HTML en bruto, así que un `<documento>` escrito en el texto se toma por una etiqueta y no se ve. El generador avisa de cada `<…>` que no es HTML, con su línea, fuera del código: se escribe entre comillas invertidas (`` `<documento>` ``) o con `&lt;` y `&gt;`. También avisa de una pregunta abierta sin recomendación. Los avisos no detienen la generación: se corrigen antes de entregar.

**Cada cambio del `.md` regenera su HTML** en el mismo cambio («Cada cambio de un .md regenera su HTML», 220).

## Respaldar

Antes de sustituir un documento por una versión nueva, la que se va a sustituir se copia a `_respaldo/`, en la misma carpeta («Antes de sustituir un documento, se respalda en _respaldo/», 217):

```bash
python -I -X utf8 <skills>/crear_documentos/scripts/respaldar.py <documento>.md <motivo>
```

Copia el `.md` y su `.html` como `<nombre>_antes-<motivo>.<ext>`; el motivo son una o dos palabras de lo que cambia la versión nueva. Volver atrás es copiar de vuelta la versión respaldada, sin tocar git. Si ya hay un respaldo con ese nombre, se detiene: se elige otro motivo (qué hacer con dos vueltas del mismo motivo, y qué documentos se respaldan, está por decidir en «Documentos nuevos a develop en cada vuelta», 297).

## Comprobación

Antes de entregar, con Playwright y el navegador instalado. Si Playwright no tiene su Chromium descargado, usa el Chrome del equipo: `p.chromium.launch(channel="chrome")` (o `"msedge"`).

- **Escritorio** (≈1300 px) y **móvil** (390 × 844): sin desplazamiento horizontal, tarjetas en una columna en el móvil y menú sin solaparse.
- **Sin errores de página.** El buscador de fichas filtra y cuenta. «Plegar las tarjetas» pliega y despliega su bloque. Los componentes propios responden.
- **Sin avisos del generador** (`<…>` sueltos, preguntas sin recomendación).
- **Recursos desde la primera versión** («Desde la primera versión»): el esquema SVG del proceso, si lo hay; los bloques largos, plegables; ninguna sección de más de unas 500 palabras sin partir ni con más de cinco párrafos seguidos sin un recurso; dos secciones seguidas sin el mismo recurso principal. Se comprueba también en la primera versión, no solo al revisar.
- **Secciones plegables:** solo la primera abierta al cargar; un enlace interno (menú, referencia, insignia o `#id` en la dirección) abre la sección de destino; al imprimir se abre todo.
- **Herramientas:** la columna desde 1400 px; por debajo, minimizada hasta «Buscar». El buscador no distingue mayúsculas ni tildes y abre la sección plegada.
- **Impresión A4** (`page.pdf`): portada sola en la primera página, sin menú ni herramientas, tarjetas sin cortar.
- **Sin restos de sintaxis** en el HTML: `:::`, `{:`, `[!aviso]` o `**` en el texto visible.
- **Sin párrafos que empiecen en negrita** (`<p><strong>` al principio) salvo las cifras destacadas (`.metrica` o el valor de un campo) y los títulos de las fuentes.
- **Enlaces internos**: cada `#id` enlazado existe.
- En una conversión, la **comparación de palabras** con el original.
- **Lectura y accesibilidad**, que ya resuelve la hoja de estilos y un componente propio tiene que respetar: texto de lectura a 17 px en pantalla (18 px desde 1600 px); nada que se lea por debajo de 13 px; página de hasta 1240 px; contraste AA; foco visible; controles de al menos 24 px de alto; campos con `name` y etiqueta.

Las capturas van a la carpeta temporal de la sesión. La página usa desplazamiento suave: para capturar una sección, desactivarlo antes (`html{scroll-behavior:auto}`).
