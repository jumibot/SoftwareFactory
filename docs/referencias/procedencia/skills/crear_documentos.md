# Origen de la skill `crear_documentos`

- **Creada:** 2026-11-02, en la SF, en la tarea «Informes de las deliberativas iguales y legibles sin maquetarlos a mano: skill propia» (301), por las decisiones 231 («Una skill propia para los informes de las deliberativas, ligera sobre el diseño común») y 232 («Una skill general de diseño de documentos, y skills de contenido encima»). El propietario la nombró como la skill de **creación** de documentos, no solo de su diseño: reúne lo común para crear cualquier documento de la SF.
- **Por qué:** el generador y los recursos de maqueta vivían en `documento_fundacional`, la visión tenía su propia maqueta y los informes tomaban prestado el fundacional. Cada recurso nuevo (como las tarjetas plegables de color de la 274) se metía en el fundacional aunque sirviera a todos.

## Inventario de lo común (paso A de la 301)

| Pieza | Antes | Ahora | Lo usan |
| --- | --- | --- | --- |
| Temas, identidad, catálogo de herramientas, procedencia, enlaces externos | `documento_vision/scripts/tema_identidad.py` | `scripts/tema_identidad.py` | todos |
| Temas visuales | `documento_vision/assets/temas/` | `assets/temas/` | todos |
| Coloreado de código | `documento_vision/scripts/resaltar_codigo.py` | `scripts/resaltar_codigo.py` | la maqueta de la visión (el generador común aún no colorea código) |
| Generador editorial | `documento_fundacional/scripts/fundacional_to_html.py` | `scripts/documento_a_html.py`, con perfiles por tipo | fundacional, informes |
| Hoja de estilos editorial | `documento_fundacional/assets/estilo_fundacional.css` | `assets/estilo_documento.css` | fundacional, informes |
| Secciones y tarjetas plegables, buscador de fichas | `documento_fundacional/assets/plegado.js`, `fichas.js` | `assets/plegado.js`, `assets/fichas.js` | fundacional, informes |
| Catálogo de recursos y su sintaxis, cuándo usar cada uno, tipografía | `documento_fundacional/SKILL.md` | `SKILL.md` | todos |
| Temas, identidad visual, catálogo de herramientas de lectura | `documento_vision/SKILL.md` | `SKILL.md` | todos |
| Comprobación (escritorio, móvil, A4, accesibilidad) | `documento_fundacional/SKILL.md` | `SKILL.md` | todos |
| Herramientas de lectura | `tools/kit_documentos/` | sin cambios | todos |
| Guía de diagramas | `metodologia/references/diagramas-svg.md` | sin cambios; esta skill la enlaza | todos |

**Se queda en `documento_vision`, por ser propio de su forma narrativa:** la carcasa (`scripts/carcasa.py`), la hoja `assets/estilo_base.css`, las escenas dialogadas, el caso conductor, los gráficos escenográficos, el aviso de ficción y la comparativa de versiones. También la usan los documentos explicativos («Cómo funciona…») y el README. Unir las dos maquetas en un solo generador queda como propuesta: cambiaría el HTML de todas las visiones.

**Se queda en `documento_fundacional`:** para quién es, sus secciones, sus reglas de redacción propias y cómo se trabaja, y su `perfil.json`.

## Comprobación del traslado (paso 14 de la 301)

Se regeneraron con el código anterior y con el nuevo los 14 documentos de la SF con HTML generado: README, los cuatro explicativos de `docs/`, las tres visiones de `docs/specs/vision/`, los dos fundacionales y los cuatro informes con cabecera de fundacional. Quitado el pie de procedencia (fecha y hora de generación), los ocho de la maqueta de la visión salieron iguales, y en los seis del generador común solo cambian las rutas `data-kit` de la hoja de estilos y de `plegado.js`. `actualizar_copia.py` reconoce las rutas viejas (`ANTIGUOS`) y pone al día las copias ya repartidas.
