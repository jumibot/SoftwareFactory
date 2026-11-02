# Origen de la skill `documento_fundacional`

- **Creada:** 2026-10-26, en la SF, por instrucción del propietario: «Lo quiero en todos los proyectos», «crea una skill, para usarse en cualquier proyecto, para crear este tipo de documentos de presentación de proyecto más formal que el de visión… usa todas las secciones que sean extrapolables a otros proyectos».
- **Decisiones del propietario (2026-10-26):** maqueta editorial; para el autor y para compartir; núcleo fijo de secciones y secciones opcionales; formato HTML, no PDF.
- **Referencias de partida** (de SmartColdBox, que es el proyecto prototípico de software, hardware y gemelo digital):
  - `SmartColdBox/docs/specs/vision/SMB_VIAL_Justificacion.html` (22/10/2026), el documento de justificación del producto SMB VIAL. Es **la referencia principal**: de él salen el núcleo de secciones (razón para desarrollar, producto, escenarios, evidencias, qué debe demostrar, fuentes), las opcionales (coste del problema, dimensionamiento, anexo de comparación, anexo de fichas) y los componentes de la maqueta (portada oscura con cifras, menú fijo con botón de imprimir, tarjetas, decisión, aviso, referencias, fichas con buscador).
  - `SmartColdBox/docs/specs/vision/SmartColdBox_Manifiesto_Fundacional_v1.pdf` (versión 1.0, octubre de 2026). De él salen la sección opcional de propósito y valores, la invitación a colaborar, la portada clara con lema y la lista numerada «01».
- **Lo que no se ha copiado:** el contenido de esos documentos. La skill no lleva nada de ningún proyecto; los ejemplos del formato son neutros o genéricos.
- **Código:** escrito para la SF. Reutiliza `documento_vision/scripts/tema_identidad.py`, extraído de `doc_to_html.py` en la misma fecha sin cambiar su comportamiento (las visiones de la SF y de SmartColdBox regeneradas salieron idénticas byte a byte).
- **`assets/fichas.js`:** buscador genérico que sustituye al filtro propio del documento de SMB VIAL. Filtra por insignias en lugar de por un atributo `data-cases`.

## Primeras conversiones (2026-10-26)

- El manifiesto de SmartColdBox, en `fundacional-smart-cold-box.md`, con su texto tal cual.
- El documento de SMB VIAL, en `fundacional-smb-vial.md`, con un conversor de un solo uso (no forma parte de la skill).
  - De las 12.948 palabras del original, solo faltan en el HTML generado las etiquetas del buscador antiguo, que sustituye el genérico.
  - La frase de su mensaje «sin resultados» pasó a una nota bajo las fichas.
  - Las 57 fuentes, las 152 referencias y las 134 insignias se conservan.
  - La calculadora quedó como componente propio en la identidad de SmartColdBox.

## Comprobación (2026-10-26)

- Playwright con Edge, a 1300 × 1000 y 390 × 844:
  - sin errores de página ni desplazamiento horizontal;
  - el filtro y la búsqueda de fichas funcionan;
  - la calculadora responde;
  - ningún enlace interno está roto y no quedan restos de sintaxis.
- Impresión A4: el manifiesto sale en 8 páginas y SMB VIAL en 64.

## Auditoría con las guías de interfaz de Vercel (2026-10-26)

El propietario pidió probar las herramientas del vídeo «5 Herramientas Para Que Tu App De Claude Code No Parezca De 2006» (revolutia). Se auditó `fundacional-smb-vial.html` contra las [Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) que usa la skill `web-design-guidelines` de `vercel-labs/agent-skills`. No se instaló la skill: solo se leyeron sus reglas.

- **Ya cumplía:** contraste AA en todo el texto (medido en el navegador), jerarquía de títulos, foco visible con `:focus-visible`, sin `outline: none`, `aria-live` en el contador, etiquetas en los campos, sin `...` ni comillas rectas, sin desplazamiento horizontal y anclajes sin tapar por el menú fijo.
- **Corregido en la skill:** enlace «Saltar al contenido»; `scroll-behavior` sin animación con `prefers-reduced-motion`; estados al pasar el ratón en botones, menú, insignias y referencias; menú e insignias con al menos 24 px de alto para pulsar; `text-wrap: balance` en títulos y `pretty` en párrafos; cifras con `tabular-nums`; `<meta name="theme-color">` con el color de la portada; logo con `width` y `height`; buscador con `name` y `autocomplete="off"`; botón de imprimir con `type="button"`; sin `preconnect` a Google Fonts cuando el tema usa las fuentes del sistema; margen de los anclajes a 84 px, porque el menú llega a 70 px entre 641 y 860 px de ancho.
- **No se ha aplicado:** las reglas de redacción en inglés (mayúsculas de título, segunda persona), los textos de menos de 12 px de las etiquetas en versalitas (no es una regla de las guías) ni llevar el filtro de fichas a la URL.

## Revisión de lectura con la Taste Skill (2026-10-26)

El propietario pidió probar `leonxlnx/taste-skill` (MIT) en una copia de `fundacional-smb-vial.html`, sin instalarla. Se leyeron sus scripts y se ejecutaron `lint.mjs` e `inspect.mjs` (Edge sin ventana, perfil temporal, servidor en 127.0.0.1); `assets.mjs`, que descarga imágenes de bancos públicos, no se ejecutó.

- **Descartado:** casi todo lo que señala, porque juzga el documento como una página de presentación y choca con esta maqueta: quitar los antetítulos numerados «01 /», las etiquetas en versalitas, los filetes y las tarjetas; añadir fotos, vídeo y animación al desplazarse; titulares de cinco palabras.
- **Aplicado, con el sí del propietario:**
  - texto de lectura a 16 px en tarjetas, columnas, fichas y notas (antes 14,4-14,9 px);
  - nada por debajo de 13 px: etiquetas, insignias, referencias y menú a 13 px; notas, cifras, pie y fuentes a 14 px;
  - texto corrido a 70 caracteres por línea y entradilla a 62; los recuadros y las tarjetas de una columna se estrechan enteros a 78 caracteres, porque limitar solo su texto dejaba un hueco vacío dentro de la caja.
- **Resultado en SMB VIAL:** de 235 textos por debajo de 13 px a ninguno del documento; unas 46 pantallas en lugar de 40 y 62 páginas A4 en lugar de 60.

## Ancho de la página (2026-10-26)

Tras ver la versión con el texto a 70 caracteres por línea, el propietario pidió «usar un poco más el ancho». Se compararon en copias tres versiones: la de 70 caracteres, una página de 960 px y otra de 1240 px. Eligió la de 1240 px: «Así sí para mi pantalla, obviamente para tablets y móviles 100 %».

- La página llega a 1240 px en pantallas grandes, con 32 px de margen a cada lado. Hasta 1024 px ocupa todo el ancho con 16 px de margen.
- El texto, los recuadros, las tarjetas y el menú comparten los mismos bordes. Se quitan los límites de 70 y 78 caracteres, que dejaban un hueco a la derecha de las tarjetas.
- La letra de lectura en pantalla pasa a 17 px, y a 18 px desde 1600 px de ancho. La impresión sigue a 10 pt.
- Se acepta a propósito que los párrafos de ancho completo lleguen a unos 160 caracteres por línea. Las tarjetas de dos y tres columnas quedan entre 55 y 75.

## Secciones plegables (2026-10-26)

El propietario pidió «mantener la colapsabilidad» de los documentos de visión. Cada sección `##` pasa a ser un `<details>` abierto por defecto, con su número, su etiqueta y su título en el `<summary>` y una flecha a la derecha, como en `documento_vision`. `assets/plegado.js` añade el botón «Plegar todo / Desplegar todo» del menú, abre la sección de destino de cualquier enlace interno y lo abre todo al imprimir. Comprobado en Edge: plegar y desplegar, enlace del menú y referencia a una sección plegada, carga con `#id`, impresión con todo plegado (sale completa) y móvil sin desplazamiento horizontal.

## Tarjetas, portada, plegado y buscador (2026-10-26)

Decisiones del propietario sobre `fundacional-smb-vial.html`:

- **Tarjetas.** «Hay un abuso que va contra la lectura estructurada del doc.» Se probó pasar 16 de los 24 bloques a prosa con el arranque en negrita, lista o lista numerada. El propietario corrigió: «cada párrafo tiene que empezar con la parte prosaica», el primer bloque «queda mejor en cards» y «cards o bullets cortan igual». Quedan en prosa, con subtítulo `####` y el párrafo empezando por el texto, solo los cuatro bloques que se leen seguidos; dos tarjetas únicas pasan a apartado normal; el resto vuelve a tarjetas. La regla queda en «Reglas de redacción».
- **Portada.** «Cabecera excesivamente aparatosa» y, sobre la versión, el foco y las cifras, «esto fuera». Queda marca, nombre, lema en letra normal e idea; la versión y el estado pasan al pie; `cifras` ya no se muestra (el generador avisa). De 571 a unos 300 px.
- **Plegado.** «Solo la primera sección abierta.»
- **Buscador.** Se revisó el buscador de `OncoCore/tools/dev/kit_documentos/kit_documentos.py` (v1.0.57) y se probó en una copia. El propietario pidió «la toolbar abierta en el lateral en pantalla grande, así usamos el espacio» y «en pantalla pequeña completamente minimizado». `assets/buscador.js` se reescribió para la skill a partir de sus ideas (resaltar, saltar con el teclado, resultados con contexto, abrir la sección), porque el kit es una plantilla de Python con los selectores de OncoCore y su diálogo flotante tapaba la portada en el móvil. Mejoras sobre el kit: no distingue tildes y no guarda nada en el navegador.

## Columna de herramientas, avisos globales y menú sin enlaces (2026-10-26)

- **Herramientas.** «Que por defecto usemos una sidebar no quiere decir que perdamos la capacidad de despegarlo», con el documento de los 20 casos de referencia de OncoCore como modelo («prototípico en este aspecto de uso de las tools»). `assets/buscador.js` pasa a una columna de herramientas: anclada desde 1400 px, de ancho ajustable y plegable; la chincheta la despega como ventana flotante que se arrastra, se minimiza y no se sale de la pantalla, y la vuelve a anclar. El navegador recuerda por documento el modo, la posición, el ancho y el plegado. En pantalla pequeña sigue minimizada del todo y se abre con «Buscar» como panel inferior, para no tapar la cabecera (el defecto del diálogo flotante de OncoCore en el móvil). Comprobado en Edge a 1920, 1300 y 390 px, recargando la página y en el PDF.
- **Aviso de alcance.** «Como esto es de alcance global, al principio, fuera de toda sección»: las citas `>` antes de la primera sección se ponen como recuadro antes de las secciones.
- **Idea de portada.** «Esto más bien a la primera sección y así disminuimos la cabecera»: la portada queda en marca, nombre y lema; la idea abre la primera sección. Aplicado también al manifiesto de SmartColdBox.
- **La diferencia frente a las alternativas.** «Apáñatelas para incluirlo en un párrafo de la prosa inicial de la sección»: sin subtítulo ni subapartados, una frase por alternativa.
- **Menú.** «Fuera las opciones»: por defecto, solo los botones; `menu: secciones` recupera los enlaces.

## Tesis en prosa, negrita y códigos (2026-10-26)

Sobre la tesis de inversión de `fundacional-smb-vial`, el propietario pidió: «esto también a la prosa inicial de la sección»; «en los párrafos de prosa puedes usar negrita sin abusar para destacar alguna frase o palabra. Prefiero si no se destaca lo que está al inicio del párrafo para no parecer bullets o subapartados»; «no uses S1 o S2, ya que aquí nadie sabe lo que son»; «intenta justificar un poco esta frase tan importante: ¿en qué te basas?». La tesis sale del recuadro de decisión y pasa a dos párrafos de la prosa inicial, con los tres hechos del documento que la sostienen (E1, E2, P6 con D1 y D3) y lo que falta por saber. La nota de dimensión clínica pierde su arranque en negrita. Las reglas quedan en «Reglas de redacción» y en el núcleo.

## Todos los argumentos del proyecto (2026-10-26)

«Incluye en SMB VIAL los argumentos del resto de docs fundacionales. En estos documentos de características de proyecto deben estar todos nuestros argumentos, y más si nos comparamos con otros productos. Por ejemplo, aquí no se menciona nada del gemelo digital.» Se hizo un inventario de la visión, el manifiesto y el gemelo digital frente a `fundacional-smb-vial.md`. Entraron el gemelo ya construido (Lab v4.0, verificado solo en simulación, con sus límites), la cuenta de exposición por vial, el aire de la nevera, la conectividad eSIM y LoRa, el rack de farmacia, la experiencia del paciente, la protección ante el exceso de frío, los valores y cuatro dimensiones del anexo de comparación. Quedaron pendientes del autor las contradicciones entre documentos (precio de Hemlibra, duración del transporte, geometría y actuadores, sensores). La regla queda en «Cómo se trabaja».

## Ventajas de OncoCore portadas y catálogo de opciones (2026-10-26)

Con el inventario completo del kit de OncoCore (v1.0.57) y de su skill `diseno_documentos` frente a la SF, se portó lo de más impacto: aspecto de tarjeta de las herramientas, asa visible, F3 / Ctrl+G, «/» que selecciona, resultado activo, «Sin resultados» en rojo, destello al saltar, anclas que abren su sección en la visión, impresión de la visión con todo abierto, una sola convención de flechas (▸ / ▾) con foco visible, enlaces externos con ↗, pie con procedencia y el registro de limpieza de la copia guardada. Herramientas v1.1.0. Lo que la SF ya hacía mejor se conserva: buscador sin tildes, memoria por documento (las claves del kit son globales), móvil sin desplazamiento horizontal e impresión sin herramientas. El resto queda en el catálogo de `documento_vision/SKILL.md` como opciones que se presentan al autor, porque «no todo es aplicable en todo documento, pero quiero tener la opción y que se me presente».

## Las opciones se preguntan (2026-10-26)

Cada opción del catálogo es opcional: si el documento no la especifica, la skill pregunta al autor, con una recomendación que depende de si el artefacto es para el proyecto (manda el `.md`) o para el usuario (el `.html` es el entregable y puede editarse en su sitio). Indicación del propietario: «con opcionalidad, me refiero que el skill pregunte si no se especifica».

## Biblioteca en tools/kit_documentos y todas las opciones (2026-10-26)

La columna de herramientas y sus opciones salen de la skill y pasan a la biblioteca de la SF `tools/kit_documentos/` (ver [su procedencia](../kit_documentos.md)), que las dos skills buscan junto a `skills/`. Herramientas 1.2.0: se portan todas las opciones pendientes del kit de OncoCore, con valores iniciales según el destino del documento (`destino: proyecto|usuario`) y las de lectura ajustables por el lector. Los bloques de código llevan `data-kit` para poder actualizar copias ya repartidas.

## Campos, recuadros y tipografía (2026-10-26)

El propietario pidió revisar el formato de los fundacionales de SmartColdBox: «ajusta no solo las negritas sino todo el formato, ya que hemos incluido recomendaciones de Vercel». En `fundacional-smb-vial.md`, 108 párrafos empezaban con una etiqueta en negrita (en el HTML, 139 párrafos que no eran cifras ni fuentes).

- **Campos repetidos** de tarjetas y fichas («Lectura para SMB», «Cuándo aporta valor», «Límite del argumento», «Qué medir», «Base documental», «Circuito», «Motivo», «Condición para avanzar», «Aportación conceptual», «Implicación y alcance», «Supuestos condicionados», «Encaje técnico»…): pasan a lista de definición. La hoja de estilos da a toda `dl` de una sección el rótulo pequeño con filete que antes solo tenían las fichas, que también sustituye al filete de `.lectura`.
- **Etiquetas sueltas** («Umbral de equilibrio:», «Criterio de éxito propuesto:», «Por qué Hemlibra primero.»…): integradas en la frase, o quitadas si la frase ya lo dice. La lista con arranques en negrita pasa a lista de definición.
- **Recuadros** con la primera frase en negrita: la frase pasa a etiqueta del recuadro.
- **Guías de Vercel aplicadas al contenido:** espacio duro entre cifra y unidad (233 en SMB VIAL), rótulos escritos en mayúsculas pasados a minúscula (la hoja los pone en versalitas), tarjetas que estaban al mismo nivel que el título de su grupo bajadas a `####`. Ya cumplía las comillas tipográficas y los puntos suspensivos. Los dos buscadores (`assets/fichas.js` y `tools/kit_documentos/herramientas.js`, herramientas 1.2.1) tratan el espacio duro y el fino como un espacio, para que «35 °C» se encuentre escrito con un espacio normal.
- **No aplicado:** mayúsculas de título, segunda persona y cifras en lugar de palabras al empezar la frase («Quince unidades…»), porque son reglas del inglés; el texto de enlace «Abrir fuente ↗» de las fuentes, porque va junto al título de cada fuente.
- Reglas en «Reglas de redacción» (campos repetidos y tipografía), «Formato del .md» y «Comprobación».

## Prosa inicial en todas las secciones (2026-10-26)

El propietario pidió llevar a todo SMB VIAL lo trabajado en la primera sección: «en cuanto a la prosa y al uso más limitado de las cards aplícalo a todo el doc», y precisó: «no quites las cards dónde sea apropiado su uso pero que esté justificado». Cada sección abre ahora con dos o tres párrafos que argumentan, con cifras y referencias; la lectura clínica y la lectura conceptual del anexo salen de su recuadro a la prosa. Pasan a prosa seis bloques que se leían seguidos: las tres vías de valor económico, las respuestas ante fallos, la gradación de la familia, los datos que faltan en Baleares, los valores de la comparación y una tarjeta de distinto tipo en la ampliación del mapa. Se mantienen las tarjetas de experiencias, cifras del producto, aplicaciones, gemelo, supuestos, evidencias, estudios clínicos, fases, validaciones, puertas, dimensiones y fichas. La regla queda en «Reglas de redacción».

## Frases completas, no catálogo (2026-10-26)

Sobre la parte de producto de SMB VIAL, el propietario: «todo esto parece un batiburrillo de bullets. Repiensa como presentar esto de una forma más clara y natural». Regla: frases con verbo dentro de cada apartado, títulos por la pregunta que responden y sin trocear en  partes de un párrafo.

## Sin avisos sobre cómo leer (2026-10-26)

Tras quitar «Regla de lectura económica» («esto fuera del doc»), el propietario pidió quitar también «Evitar tres saltos de inferencia» y «Cómo leer los costes». Regla: los avisos de lectura o de razonamiento son para quien escribe; lo imprescindible para el lector va en una frase de la sección.

## Esquemas SVG (2026-10-27)

Al reorganizar SMB VIAL con el sistema SMB como sección 1, el propietario aceptó un esquema («si crea el svg»). El generador ya dejaba pasar el HTML; la hoja de estilos añade `figure`, `figcaption` y la inversión en modo oscuro, y la skill recoge cómo se dibujan.

## Ids repetidos (2026-10-27)

Una sección «{#contenido}» chocaba con «<main id="contenido">» y los enlaces y las notas iban al sitio equivocado. El generador se detiene si la página tiene un id repetido y dice cuál.

## Alternativas, impacto y riesgos (2026-10-27)

Al orientar el fundacional de SMB VIAL a los criterios de una convocatoria de innovación (sustitutivos, riesgos con mitigación, impacto con indicadores y ODS), el propietario aprobó tres secciones (alternativas, impacto y riesgos) en el documento y después pidió «aplica la skill con riesgos e impacto como opcionales». Se añaden como opcionales «Impacto» y «Riesgos», con la forma que se usó en SMB VIAL. La sección de alternativas sigue como parte de «Razón para desarrollar» (la diferencia frente a las alternativas).

## Sin recuadros de lema y orden explicar–justificar (2026-10-27)

El propietario quitó el recuadro «Promesa de trabajo» de SMB VIAL («fuera»), que venía de la propia skill. Aprobó quitar la promesa de «Propósito y valores», no usar recuadros para lemas o principios de manifiesto (se quitaron también «El principio de plataforma» y «Una decisión de ingeniería, no una suposición») y pasar a la skill el orden «primero explicar y después justificar» con que se reorganizó SMB VIAL.

## Destino y herramientas, obligatorios; capas en cada sección (2026-11-01)

Tarea 204. Sin `destino` o sin `herramientas`, el generador se detiene con las opciones en lugar de usar los valores del proyecto (`recomendadas` toma las del destino; también `--destino` y `--herramientas`). La lectura por capas vale también dentro de cada sección. El documento abre siempre en claro (kit 1.9.0).

## Lo común, a `crear_documentos` (2026-11-02)

Tarea 301, decisión 232. El generador (`fundacional_to_html.py`, ahora `crear_documentos/scripts/documento_a_html.py`), la hoja de estilos, `plegado.js`, `fichas.js`, el formato del `.md`, la tipografía, cuándo usar cada recurso y la comprobación pasan a la skill general `crear_documentos`. Esta skill se queda con su contenido (para quién es, secciones, reglas de redacción propias, cómo se trabaja) y con su perfil (`perfil.json`: tipo por defecto y recursos que usa). `scripts/fundacional_to_html.py` sigue funcionando con la misma orden: llama al generador común con el perfil. Los HTML regenerados solo cambian en las rutas `data-kit`.
