---
name: documento_fundacional
user-invocable: false
description: Crea o revisa el documento fundacional de un proyecto o de un producto — su presentación formal, más formal que el documento de visión y sin historia conductora — con la necesidad documentada, la tesis de desarrollo, qué es el producto, los escenarios de uso, las evidencias con lo que respaldan y lo que no, qué debe demostrar el piloto y las fuentes. Para el autor y para compartir con colaboradores, socios o financiadores. Úsala cuando pidan un documento fundacional, una presentación o justificación formal del proyecto, un manifiesto, un dossier o un caso de desarrollo, o convertir uno existente (PDF, HTML) a este formato. Genera .md → .html con el generador y los recursos comunes de crear_documentos (portada sobria, secciones plegables, tarjetas, fichas con buscador, referencias) y el tema de la identidad del proyecto; se imprime en A4.
---

# Documento fundacional

El **documento fundacional** presenta un proyecto, o un producto de una familia, de forma formal y compacta: qué necesidad atiende, por qué merece desarrollarse, qué es, en qué situaciones aporta valor, qué lo respalda y qué tiene que demostrar. Es la descripción de referencia del proyecto.

Se diferencia del **documento de visión** (skill `documento_vision`) en tres cosas:

- **Sin historia conductora.** No hay caso, escenas ni prólogo. Es una descripción ordenada, como un dossier.
- **Más formal.** Cada afirmación del dominio lleva su referencia, y se separa siempre lo publicado, lo que es objetivo de diseño y lo que es supuesto de cálculo.
- **Para el autor y para compartir.** Sirve al autor (y a Claude en sesiones futuras) como descripción compacta y sin distracciones, y se puede entregar tal cual a colaboradores, socios o financiadores.

Los dos conviven. La visión cuenta el proyecto con una historia; el fundacional lo describe. Si uno cambia, se revisa el otro.

Esta skill dice qué lleva un fundacional y cómo se escribe. El generador, los recursos y su sintaxis, los temas, las herramientas y la comprobación son los comunes de `crear_documentos`, que se lee junto a esta.

## Dónde va

Los documentos fundacionales de un proyecto van juntos en `docs/specs/vision/` (metodología de la SF, «Estructura documental común»): la visión, el fundacional y las infografías técnicas en `infografias/`.

- Del proyecto: `docs/specs/vision/fundacional-<proyecto>.md` y su `.html`.
- De cada producto de una familia, si lo tiene: `fundacional-<producto>.md`.

El `.md` es la fuente. El `.html` se genera y no se edita a mano. Si se parte de un PDF o de un HTML existente, se convierte a `.md` y el original se conserva junto a él o en `_respaldo/`.

**Modelo.** Si el proyecto ya tiene un fundacional que aplica bien estas reglas, se lee como ejemplo al escribir o revisar otro; lo propio de su dominio no se copia.

## Secciones

Hay un **núcleo** que todo documento fundacional tiene y **secciones opcionales** que se incluyen cuando el proyecto las necesita. Se numeran en el orden en que aparecen. Los anexos van al final, con etiqueta «Anexo A · …».

**Orden: primero explicar, después justificar.** El lector tiene que saber qué es el producto antes de valorar los argumentos. Tras la apertura (propósito, si lo hay, y la prosa de la razón para desarrollar con la idea, la diferencia y la tesis), van las secciones que explican: el sistema o la familia, el producto y su funcionamiento, los escenarios y las alternativas. Después, las que justifican: la necesidad documentada y el coste del problema, el impacto, el dimensionamiento, los riesgos y «Qué debe demostrar». Las tarjetas de la necesidad documentada pueden ir en su propia sección, tras el producto, si la apertura ya resume la tesis.

**Portada sobria.** Marca, nombre y lema en letra normal (una o dos líneas). Nada más, para que la cabecera sea baja: la idea con el propósito abre la primera sección como entradilla, la versión y el estado van al pie, y no hay fila de cifras (contar fichas o evidencias es inventario, no argumento; si una cifra argumenta, va en el texto).

**Avisos de alcance global** (qué del documento es objetivo de diseño y qué está validado, o cualquier criterio que se aplica a todo el texto): van al principio, fuera de toda sección. Se escriben como cita `>` entre el `# Nombre` y la primera `##`; el generador los pone antes de las secciones, como recuadro.

### Núcleo

1. **Razón para desarrollar.** Empieza con una prosa inicial, antes de las tarjetas y sin subtítulos:
   - la idea con el propósito, como entradilla;
   - **la diferencia** frente a las alternativas existentes, en un párrafo, con su referencia y una frase por alternativa;
   - la **tesis de desarrollo**: qué merece financiarse o construirse ahora y con qué condición tendrá valor. Va en prosa, no en un recuadro, y **se justifica**: en qué hechos del documento se apoya, con su cifra y su referencia, y qué falta por saber, que es lo que debe medir el piloto.

   Después, dos o tres tarjetas con la necesidad documentada (el problema medido, la capacidad de intervenir, la consecuencia), cada una con su referencia. Esta forma, prosa que argumenta y después tarjetas justificadas, es el modelo de todas las secciones (ver «Reglas de redacción»).
2. **El producto.** Qué es en pocas cifras (capacidad, autonomía, alcance…), cómo funciona por subsistemas, su arquitectura, sus funciones principales, cómo evoluciona (familia, plataforma, verificar / reconfigurar / rediseñar) y qué no hace.
3. **Escenarios de uso.** Las situaciones en que el producto puede aportar valor, con un código cada una (S1, S2…) para citarlas en el resto del documento. En cada una: **cuándo aporta valor**, **límite del argumento**, **qué medir** y la base documental. Los escenarios son compatibles entre sí; no se suman como poblaciones independientes.
4. **Evidencias.** Primero, el método y el alcance de la búsqueda. Después, una tarjeta por evidencia: tipo (medición, piloto, guía, estudio…), qué dice con su cifra, a qué escenarios afecta y una **lectura para el proyecto** que diga qué respalda **y qué no**.
5. **Qué debe demostrar.** El paso del documento al piloto: fases priorizadas, cada una con su circuito, su motivo y su **condición para avanzar**; las validaciones necesarias (técnica, operativa, económica); las **decisiones de avance** (puertas); la decisión propuesta y cómo se medirá.
6. **Fuentes y referencias.** Todas las fuentes con código por tipo (por ejemplo E evidencias, F fichas técnicas, P precios, D economía, C clínica, M documentos del propio proyecto), su procedencia, su enlace y la fecha de revisión.

### Opcionales

- **Propósito y valores** (misión, visión y valores), al principio, como sección propia o como tarjetas dentro de la primera. Para proyectos que buscan alinear a un equipo o a colaboradores.
- **Coste del problema**, cuando hay una dimensión económica: casos documentados con su cifra y su «implicación y alcance», qué se puede evitar y el modelo económico (una fórmula). Va después de la razón para desarrollar.
- **Dimensionamiento** del mercado o del territorio: lo que las fuentes permiten afirmar y lo que no, qué datos harían falta (denominador, exposición, economía), un escenario transparente (puede llevar una calculadora como componente propio) y cómo convertirlo en una estimación defendible. Va antes de «Qué debe demostrar».
- **Anexo de comparación** con una referencia existente: una tarjeta por dimensión, con dos columnas («referencia · publicado» y «proyecto · diseño») y la aportación de cada enfoque. Al final, los valores que debe conservar la comparación y cómo comprobar el valor añadido.
- **Anexo de fichas** por elemento (medicamentos, materiales, componentes, clientes tipo…): una ficha por elemento con sus datos y sus escenarios. El generador añade un buscador y un filtro por escenario.
- **Impacto**: qué cambiaría si el producto funciona, siempre condicionado a lo que demuestre el piloto. Una tarjeta por dimensión (económica, para las personas, para el territorio o el entorno) con «Qué puede cambiar» y su **indicador**, medible antes y después. La prosa inicial nombra la línea de base que ya existe y lo que falta medir; ninguna cifra de ahorro se atribuye al proyecto sin ese contraste. Los ODS, si se citan, con su nombre oficial y su fuente. Va después del coste del problema o de la necesidad.
- **Riesgos**: qué puede fallar y cómo se mitiga. Una tarjeta por riesgo, con su clase como etiqueta (técnico, operativo, económico, regulatorio), «Mitigación» y «Se comprueba en», que remite a una fase o puerta de «Qué debe demostrar». La prosa inicial dice el riesgo principal y cómo el plan lo detecta pronto. Lo que aún no se ha analizado (por ejemplo, el encaje regulatorio) se declara como riesgo abierto, con sus fuentes cuando las haya. Va justo antes de «Qué debe demostrar».
- **Invitación a colaborar**: qué perfiles se buscan, qué se ofrece y qué se espera. Para documentos que se comparten.

**Lectura por capas.** Se comunica primero lo más importante, y cada capa siguiente profundiza: quien solo lee la primera se lleva lo esencial, y quien quiere más sigue leyendo. El orden es de importancia, no el de cómo se llegó a las conclusiones. Vale para todo el documento y para cada sección, que abre con su conclusión (ver «Reglas de redacción») y deja el detalle a las tarjetas, los `####` plegados y los anexos.

Si el proyecto necesita una sección que no está aquí, se propone al autor antes de escribirla. Si es útil para otros proyectos, es una mejora de esta skill, que es de la SF: no se anota en el proyecto, se dice en una línea; en la propia SF es del proyecto.

## Reglas de redacción

- **Solo la última decisión.** El documento describe el estado actual, sin historial.
- **Tres clases de afirmación, siempre separadas**: hechos publicados (con referencia), objetivos de diseño del proyecto (lo que se quiere que haga) y supuestos de cálculo (marcados como ilustrativos). Un recuadro de alcance al principio lo explica, y las etiquetas «publicado» y «diseño» lo recuerdan donde se comparan.
- **Toda cifra o afirmación del dominio se contrasta con fuentes antes de escribirla**, nunca de memoria, y lleva su referencia en la misma frase. Para buscar en la web, pedir permiso al autor si no lo ha dado.
- **Cada evidencia dice también lo que no demuestra.** «Lectura para el proyecto», «Límite del argumento», «Implicación y alcance»: el documento gana credibilidad cuando marca sus propios límites.
- **Compacto.** Párrafos de dos o tres frases, frases de unas 20 palabras o menos, siglas explicadas la primera vez. El núcleo se lee de un tirón; el detalle extenso va a los anexos.
- **Sin paja.** Nada sobre el propio documento («Hay que actualizar este documento…», «Este documento no contiene…») ni obviedades: cada frase aporta algo del proyecto.
- **Cada sección abre con prosa que argumenta**, como la primera: unos dos o tres párrafos, antes de cualquier tarjeta y sin subtítulos, con la conclusión de la sección, los hechos que la sostienen con su cifra y su referencia, y lo que falta por saber. Una frase de presentación («Seis experiencias permiten…») no basta. La tesis o la lectura de conjunto va en esa prosa, no en un recuadro. Las tarjetas vienen después y aportan el detalle que se consulta, sin repetir el argumento.
- **Frases completas, no catálogo.** Dentro de cada apartado (`###`) se escribe con frases con verbo que explican cómo funciona algo y por qué, no enumeraciones sin verbo («Identificación, inventario, trazabilidad…»). Los apartados se titulan por la pregunta que responden («Cómo mantiene el frío»), no con el patrón «Tema: subtema», y no se trocean en `####` partes de un párrafo: el `####` queda para el detalle que se pliega.
- **Estructura visible, sin romper la lectura:** cuándo van tarjetas, prosa, apartados, recuadros, tablas o listas, la negrita, los campos repetidos y la tipografía, en `crear_documentos` («Cuándo usar cada recurso»). En un fundacional, las tarjetas típicas son experiencias, escenarios, evidencias, fases, puertas, dimensiones de una comparación, fichas y las cifras clave del producto; en un balance, lo que ha funcionado se cuenta en prosa y las deficiencias van en una tabla con lo que pasa y su estado.
- **Sin códigos que el lector aún no conoce.** Los códigos internos (S1, S2…) solo se usan después de la sección que los define y donde ayudan a cruzar referencias. Antes, y en la prosa que argumenta, se dice con palabras («el transporte al domicilio y la conservación en casa»).
- **Toda afirmación clave se justifica en el mismo sitio.** Una tesis o una conclusión importante dice en qué se basa (los hechos del documento, con cifra y referencia) y qué no está demostrado todavía.
- **Propuestas, no imposiciones.** «Se propone», «a valorar», «decide quien corresponde».
- **Respeta las sensibilidades del dominio.** Las reglas del dominio del proyecto están en las `reglas` de su identidad (las mismas que lee `documento_vision`).

## Cómo se trabaja

1. **Leer antes de proponer**: la visión del proyecto, su identidad y sus reglas, la especificación si existe, el código o el gemelo si aportan cifras, y el material que traiga el autor.
   **Inventariar todos los argumentos del proyecto.** Un documento fundacional de producto recoge todos los argumentos que el proyecto tiene, y más cuando se compara con otros productos: los de los demás documentos fundacionales, la visión, la especificación y lo ya construido (un gemelo digital, un prototipo, pruebas). Antes de escribir o revisar, se hace un inventario de lo que falta, con su fuente y su clase (hecho publicado, objetivo de diseño, supuesto o avance verificado solo en simulación), y de las contradicciones entre documentos, que se preguntan al autor antes de pasar ninguna cifra afectada. Lo construido se cuenta con sus límites declarados.
2. **Proponer el índice y las herramientas**: preguntar si el documento es un artefacto para el proyecto o para el usuario y qué herramientas lleva (buscador, notas, «Lectura», plegado, leyenda, edición…), con la recomendación para ese destino, en una sola pregunta con opciones; anotar la respuesta en la cabecera. Proponer el índice: el núcleo, las secciones opcionales que aplican y por qué, los escenarios candidatos con su código, las cifras de portada y el recurso de cada sección, con sus esquemas. Dejar que el autor lo afine antes de escribir.
3. **Investigar las evidencias** que falten (con permiso para buscar), con su fuente exacta.
4. **Escribir el `.md`** con los recursos de abajo, ya en la primera versión (`crear_documentos`, «Desde la primera versión»), y generar el `.html`. Antes de sustituir una versión, se respalda en `_respaldo/` (`crear_documentos`, «Respaldar»).
5. **Verificar** (ver «Comprobación») y entregar con un resumen: qué contiene, qué es ilustrativo, qué evidencias faltan y qué conviene que valide un experto.
6. **Afinar con el autor.** Cada corrección general se añade a esta skill, o a `crear_documentos` si es de un recurso o del diseño común; la propia del proyecto, a las reglas de su identidad. Avisar en una línea de qué se ha añadido y dónde.

Al **convertir un documento existente** (PDF, HTML, Word), se conserva todo su texto, sus referencias y sus enlaces. Se comprueba al final comparando las palabras del original con las del HTML generado: solo deben faltar las de la interfaz que se sustituye (menús, buscadores).

## Recursos que usa

El catálogo y su sintaxis están en `crear_documentos` («Catálogo de recursos»). El fundacional usa, según su `perfil.json`, tarjetas (con color, icono y plegado), columnas, fichas con buscador y fuentes, además de la portada, los avisos globales, los recuadros, las referencias, las insignias y los esquemas SVG.

- **Cabecera:** `antetitulo` con el proyecto, el tipo y la fecha («Proyecto · Documento fundacional · Octubre 2026»), `lema`, `subtitulo`, `version` y `estado` (al pie) y, si se comparte, `portada: oscura`. `tipo`, por defecto, «Documento fundacional».
- **Escenarios** con su código en el título (`### S2 · Conservación domiciliaria {: #S2}`) y las **insignias** `[S2](#S2){: .insignia}` donde se citan; el filtro de las fichas las usa.
- **Evidencias, fases, puertas e impacto** en tarjetas con sus campos (`Cuándo aporta valor`, `Límite del argumento`, `Qué medir`, `Lectura para el proyecto`, `Motivo`, `Condición para avanzar`, `Indicador`…).
- **La decisión propuesta** de «Qué debe demostrar», en un recuadro `> [!decision]`.
- **El anexo de fichas**, en `::: fichas 2`, con sus insignias de escenario.
- **Las fuentes**, en `::: fuentes`, con código por tipo (`{: #src-E1}`) y referencias `[[E1]](#src-E1 "Fuente, año"){: .ref}` en la frase que respaldan.
- **Componentes propios** (por ejemplo, una calculadora de dimensionamiento), en la identidad del proyecto.

Si el fundacional necesita un recurso que no está en su perfil, se añade al perfil; si no está en el catálogo, se propone para `crear_documentos`.

## Generar

```bash
python -I -X utf8 <skills>/documento_fundacional/scripts/fundacional_to_html.py docs/specs/vision/fundacional-<proyecto>.md
```

Es el generador común de `crear_documentos` con el perfil del fundacional; necesita esa skill instalada junto a esta. Usa el tema, el logo y el producto de `docs/identidad/identidad.json`, el mismo de la visión. Las opciones, el destino y las herramientas, en `crear_documentos` («Generar» y «Herramientas y opciones de lectura»).

## Comprobación

La de `crear_documentos` («Comprobación»): escritorio y móvil, secciones plegables, buscador, impresión A4, restos de sintaxis, enlaces internos, lectura y accesibilidad. En una conversión, además, la comparación de palabras con el original.
