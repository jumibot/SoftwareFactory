# Diagramas en SVG

Guía común de la SF para cualquier diagrama de un documento, de la SF o de un proyecto: visiones, fundacionales, especificaciones, interfaz, definición técnica, guías e informes. Reúne las recomendaciones de los gráficos de `documento_vision` y de los esquemas del generador común de `crear_documentos` (fundacional, informes…). Esas skills añaden lo propio: escenas y caso conductor en la visión; tipografías mínimas y el catálogo de recursos, con las tarjetas de color, en `crear_documentos`.

## Norma

**Todo diagrama es un SVG inline en el propio `.md`. Nunca en ASCII ni en mermaid** (metodología, 6; norma del propietario, 2026-10-27). El HTML de la SF no dibuja ni los esquemas de caracteres ni mermaid, y se leen peor. Si un borrador o un material de partida trae uno, se redibuja en SVG.

Excepción: los árboles de carpetas no son diagramas y siguen en un bloque de texto.

## Cuándo dibujar

- **Un diagrama aclara una idea compleja de otra forma; nunca repite la prosa.** Solo se dibuja lo que cuesta entender en texto: un proceso que cambia en el tiempo, una estructura (capas, piezas que comparten algo, un mapa de actores) o una escena entre personas. Si el diagrama dice lo mismo que un párrafo, sobra uno de los dos: la prosa que lo introduce se queda en una o dos frases.
- Tampoco repite otro diagrama o un componente del documento, y el pie no repite la frase de entrada ni un texto del propio SVG.
- **Introducción, diagrama y prosa** (acuerdo del propietario, 2026-10-27). Una sección nunca empieza por un diagrama: antes va una introducción mínima en prosa. Si el diagrama describe bien el proceso, va justo después de esa introducción y el texto lo desarrolla en prosa corrida, sin repetirlo en una lista de pasos.
- Ante cada diagrama, preguntarse qué entendería de menos el lector sin él. Si la respuesta cabe en una frase, se escribe esa frase y se quita el diagrama.
- **Escenas para las dinámicas, diagramas para la estructura.** Lo que pasa entre personas o agentes se ilustra como una escena (reglas en `documento_vision`); las capas, los flujos y las comparaciones, como diagramas.

## Forma

- **Vertical, preferentemente siempre:** `<figure class="vertical">` y `viewBox` de **560 de ancho**, para que se lea en el móvil sin desplazarse. No solo los flujos: las tarjetas que se comparan se apilan, los mapas por columnas se apilan por grupos, las líneas de tiempo van una opción por fila y los ciclos, un paso por fila. Antes de entregar, comprobar que ningún diagrama pasa de 560 de ancho.
- **Con datos reales del caso o del proyecto**: nombres, rutas, cifras. Nada de «opción X / Y» ni de etiquetas genéricas.
- **Estilo ligero.** Pocos recuadros y pocos fondos. La información se ordena con tipografía (nombre en negrita y color, detalle en gris debajo), alineación en columnas y espacio en blanco. Para bloques paralelos que comparar, basta un contorno fino sin fondo por bloque. Los fondos se reservan para lo que hay que destacar (una marca, un estado, «estás aquí»).
- **Minimalismo: sin título ni línea separadora dentro del SVG.** El encabezado de la sección y el pie ya dicen qué es; el diagrama empieza por su contenido (norma del propietario, 2026-10-27).
- **Pocas palabras por elemento**: una frase corta por fila; el detalle va a la prosa.
- **Cifras en palabras, sin siglas** que haya que descifrar. Si una sigla es inevitable, se explica en el pie.
- **Mismo orden en todo el documento.** Una escala o secuencia (fases, niveles, opciones) se presenta en el mismo orden en diagramas, listas y texto.

## Color, iconos y letra

- **Semántica de color estable** en todo el documento: el primario para el sistema; el acento solo para lo validado o la evidencia; ✓ en el primario y ✕ en rojo oscuro (`#991b1b`); gris para lo descartado (visible, nunca oculto). Lo que existe, con trazo continuo; lo previsto o futuro, con trazo discontinuo.
- **Colores del tema.** En documentos generados con `documento_vision`, los colores de los roles se escriben con los valores del tema `teal` (primario `#00726b`, oscuro `#004d47`, líneas `#b2deda`, fondo suave `#e0f4f3`) o `morado` (`#7b2cbf`), y el generador los convierte en variables del tema elegido. En el fundacional se usan directamente las variables (`var(--primario)`, `var(--oscuro)`, `var(--texto-suave)`, `var(--linea)`, `var(--fondo)`). Sin fondo propio en el SVG: el modo oscuro lo invierte con la página.
- **Colores con significado, más allá del tema** (acuerdo del propietario, 2026-10-27). Para distinguir categorías se usan los colores de la serie del tema `colorido`, validados para daltonismo y con contraste suficiente sobre blanco: turquesa `#1f7a7a`, naranja `#a6501a`, verde `#1f812d` y el acento frambuesa `#be185d`. Son los mismos cuatro, con el mismo valor, que las tarjetas de color del generador común (`{color=turquesa}`…, `crear_documentos`, «Tarjetas con color e icono»): mismo color, mismo significado en esquemas y tarjetas. Reglas:
  - cada color significa una sola cosa en todo el documento, en diagramas y en tarjetas (en «Cómo funciona»: turquesa, las skills; naranja, el mod y el estado; verde, los proyectos; frambuesa, las mejoras y la decisión del propietario);
  - como mucho tres de estos colores por figura, además del color del tema;
  - solo en títulos, bordes, líneas y etiquetas, sin fondos de color: un fondo claro se queda claro en el modo oscuro y desentona;
  - en una tarjeta del generador común, con `{color=…}` en su título (cabecera de ese color); en una tarjeta escrita a mano, en el borde superior y en el título: `style="--oscuro:<color oscurecido>;--borde:<color aclarado>;border-top:4px solid <color>"`.
- **Letra del tema:** `style="font-family:var(--fuente-texto);display:block"` en el `<svg>`.
- **Iconos con significado.** Todo lo que almacena información (repositorios, documentos de registro, catálogos, cachés, bases de datos) lleva el icono de almacenamiento: un cilindro, con el color de su tipo. Nada de iconos genéricos.
- **Nada que no esté en el texto.** El buscador de las herramientas de lectura no entra en los SVG: un dato que solo esté en el diagrama no se encuentra. El diagrama muestra lo que el texto dice.
- **Texto de derecha a izquierda** (árabe, hebreo): `direction="rtl"` con `text-anchor="start"`.

## Accesibilidad y pie

- `role="img"` y `aria-label` en el `<svg>` (o un `<title>`) con lo que dice el diagrama, para lectores de pantalla.
- `<figcaption>` breve, en cursiva, que diga qué hay que ver.
- Los enlaces de los elementos del diagrama van en una línea debajo, no dentro del SVG.

## Revisión

- Ningún texto se sale de su caja ni del `viewBox`; no hay solapes; las flechas siguen la lógica correcta.
- Cada SVG se revisa en una captura del HTML generado (Chrome sin cabeza, `--screenshot`), no solo en el código: los desbordes y solapes solo se ven así.
- El diagrama es coherente con el texto y con los demás diagramas.
- Al rehacer un diagrama, listar antes las piezas que nombraba y comprobar después que siguen todas.
- Una regla de estilo se aplica a todos los diagramas equivalentes del documento, no solo al primero.
- Dentro de un bloque HTML del `.md` no se dejan líneas en blanco: el conversor de Markdown lo cortaría.

## Esqueleto

```html
<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 {alto}" width="100%" role="img" aria-label="{Qué dice el diagrama}" style="font-family:var(--fuente-texto);display:block">
<circle cx="34" cy="22" r="7" fill="#fff" stroke="#00726b" stroke-width="2"/>
<text x="56" y="20" font-size="14.5" font-weight="700" fill="#004d47">{Paso o pieza}</text>
<text x="56" y="38" font-size="12.5" fill="#555">{Detalle en una frase}</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">{Qué hay que ver}</figcaption>
</figure>
```

Ejemplos en uso: los gráficos de las visiones de la SF (`docs/specs/vision/`) y los de [Cómo funciona la Software Factory](https://github.com/jumibot/SoftwareFactory/blob/main/docs/como-funciona-la-software-factory.md).
