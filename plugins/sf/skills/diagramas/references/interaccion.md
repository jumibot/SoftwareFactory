# Interacción

Lo que la SF añade a diagram-design: el diagrama se explora. Cada nodo tiene su ficha con lo que no cabe en el dibujo (botones, condiciones, ejemplos), y el lector la abre sin perder el dibujo. Código en `assets/diagramas.css` y `assets/diagramas.js`, sin dependencias; ejemplo en `assets/ejemplo-estados.html`.

## Marcado

| Pieza | Marcado |
|---|---|
| Figura | `<figure class="diagrama" data-diagrama>`; opcional `data-marca-on="<id de marker>"` para la punta de las flechas resaltadas, o `"auto"`: la de cada flecha con `-on` detrás (una por SVG, como hace el generador) |
| Nodo | `<g data-nodo="id">` con su caja principal en `class="d-caja"` (recibe el clic en todo su interior) |
| Flecha | `data-de="id"` y `data-a="id"` en su `<path>` o `<line>`, y en el `<text>` de su etiqueta |
| Fichas | `<div class="d-fichas" hidden>` al final de la figura, con un `<div data-ficha="id" data-nombre="Nombre">…</div>` por nodo, en el orden del dibujo |
| Forma | `class="vertical"` (400) o `class="ancho"` (960); las dos versiones con `solo-estrecho` y `solo-ancho`. El generador añade `data-cajas` y `data-forma` en cada `<svg>` (sus cuatro variantes) y la figura enseña la de `data-d-cajas` y `data-d-forma` |

Un nodo sin ficha no se pulsa. El texto de las fichas es la descripción larga del diagrama: lo que dice el dibujo está también ahí o en la prosa.

## Comportamiento

- **Pulsar un nodo** (clic, toque, Intro o Espacio): su ficha sale en el **HUD**: con la figura de 800 px o más, a la altura del nodo y fuera del dibujo si cabe, si no a su lado; con la figura más estrecha, a todo su ancho, bajo el nodo (o encima si no cabe). Volver a pulsarlo la cierra.
- **Resaltado**: el nodo, sus flechas de entrada y salida, sus etiquetas y los nodos del otro extremo; lo demás, al 28 %. Las flechas del recorrido, según el ajuste «Recorrido»: en el segundo color del tema (por defecto), en el acento o más gruesas con su color. Con el ratón al pasar, con el teclado al llegar con el tabulador, y fijo mientras su ficha está abierta.
- **Plegar una caja**: el circulito de su esquina (`<g class="d-plegar" data-plegar="id">`, que el script hace botón con `aria-expanded`) la pliega o la despliega; no abre la ficha. La caja cambia de alto en su sitio, centrada (`data-hd` y `data-hp` en su `<rect>`), y los extremos de sus flechas vuelven a su contorno; las demás no se mueven: recolocar la figura por cada combinación de cajas no cabe en un SVG generado. Con «Máximo una desplegada», empiezan todas plegadas; abrir una pliega la anterior, y volver a pulsar la abierta la pliega.
- **Escape** cierra el HUD y devuelve el foco al nodo. También cierran ✕ y pulsar fuera de la figura.
- **Sin JavaScript**: el dibujo entero, sin fichas. **Al imprimir**: sin HUD ni atenuado.
- **Copias** de las herramientas del documento: sin HUD ni resaltado (`window.alCopiarDocumento`).

## Accesibilidad

- El script pone en cada nodo con ficha `tabindex="0"`, `role="button"`, `aria-expanded`, `aria-controls` y `aria-label` («Nombre: ver su ficha»), y pasa el `<svg role="img">` a `role="group"`, porque `img` esconde sus hijos al lector de pantalla.
- El HUD es una región con `aria-live="polite"` y su botón ✕ de 44 × 44.
- Lo que se pulsa mide 24 × 24 px o más en pantalla (el script de comprobación lo mide a 375).
- Foco visible: borde del primario en la caja; transiciones de 0,15 s que se apagan con `prefers-reduced-motion`.

## Hueco para más modos

`data-modo="<nombre>"` en la figura llama a `window.sfDiagramas.modos[<nombre>](figura)` si existe. Reservado para el replay (un recorrido paso a paso con su porqué), que se decidirá en una tarea aparte; hoy no hay ningún modo.
