---
name: diagramas
user-invocable: false
description: Diagramas SVG de la Software Factory para cualquier documento — elegir el tipo (estados, flujo, secuencia, arquitectura, capas, árbol, línea de tiempo, carriles, cuadrante, ER y los demás de diagram-design), dibujarlo en vertical por defecto y en horizontal solo si la figura es ancha, con la estética de diagram-design en los colores y la letra del tema, flechas en ángulo recto, un foco, presupuesto de nodos y flechas, y la interacción propia de la SF (la ficha de cada nodo en un HUD al pulsarlo, resaltado del recorrido y Escape), accesible con teclado y toque, y comprobarlo con su script (solapes, desbordes, contraste y letra mínima a 375). Úsala al dibujar, revisar o convertir un diagrama, esquema o gráfico de proceso en un documento o una página HTML.
---

# Diagramas

Un diagrama es un SVG inline (nunca ASCII ni mermaid) que explica lo que cuesta en prosa: un proceso que cambia, una estructura, quién habla con quién. Si una tabla o un párrafo dicen lo mismo, no se dibuja. **Lo mejor suele ser quitar**: cada nodo es una idea distinta, cada flecha dice algo y el diagrama está hecho cuando no se puede quitar nada. Densidad 4 de 10.

Se aplica con la guía común `../metodologia/references/diagramas-svg.md` (cuándo dibujar, introducción antes del diagrama, nada que no esté en el texto, colores con significado, pie). Si chocan, manda esta skill en la forma y la interacción.

## Antes de dibujar

1. **Elegir el tipo** en `references/tipos.md` y leer su fila: cuándo, convenciones, límite y forma vertical. Si dos encajan, el del eje dominante.
2. **Decir el plan en una línea** al autor: tipo, forma (vertical u horizontal más vertical), qué se queda fuera por el presupuesto. Si no responde, seguir y anotarlo.
3. **Primero, el generador** (comandos antes que inferencia): escribir los datos en el formato breve de `references/datos.md` (un ejemplo por tipo en `assets/ejemplos/`) y lanzar
   `python -I -X utf8 <skills>/diagramas/scripts/generar_diagrama.py <datos.diagrama> [-o salida.html] [--tema tinta] [--fragmento]`.
   Dibuja la vertical y, si cabe, la horizontal con los mismos ids, cada una con cajas desplegadas o plegadas y redondeadas o en croqueta, con fichas en el HUD, resaltado, los ajustes por defecto de la decisión 302 y el tema (`tinta` por defecto; con `--tema ""`, sin tema: la figura toma el del documento, decisión 307), y pasa él solo el comprobador. Con `--fragmento`, solo la `<figure>`: se pega tal cual en el `.md` y `documento_a_html.py` trae lo demás, con la herramienta «diagramas» para ajustar todas las figuras (ejemplo: `assets/ejemplo-documento.md`). Si dice que algo no cabe, se acorta o se quita (no se fuerza). Tipos: estados, proceso, arquitectura, piezas, secuencia y fases.
4. Solo para los demás tipos, a mano, desde `assets/ejemplo-estados.html` (generado): el esqueleto, los marcadores, las máscaras y las fichas, con el tema de referencia, `tinta` (la paleta de diagram-design en `crear_documentos`), en claro y en oscuro.

## Forma según el ancho de la figura

- **Vertical por defecto**: `viewBox` de **400** de ancho (provisional, ver «Pendiente»), `<svg class="vertical">`. Sirve en cualquier pantalla. Los flujos bajan; lo que sale del camino principal, a un lado; las comparaciones se apilan. En arquitectura y piezas, una banda por zona con **varias cajas por fila** si caben (tres, dos, dos con un nombre en dos líneas, o una), colocadas donde sus flechas salen más cortas y con sitio para su etiqueta: rectas si se miran, en L o en Z por los huecos, por una calle entre columnas o por un carril a la derecha.
- **Horizontal solo si el contenido es ancho** (secuencia con varios actores, Gantt, cuadrante grande): dos dibujos con los mismos datos e ids, `class="ancho solo-ancho"` a **960** y `class="vertical solo-estrecho"`. La figura elige por su propio ancho: la horizontal desde 800 px. Nunca desplazamiento horizontal.
- Retícula de 4: orígenes, tamaños, huecos y rellenos múltiplos de 4.

## Reglas de diagram-design

- **Presupuesto**: 9 nodos, 12 flechas, 2 focos, 2 anotaciones como mucho; los límites de cada tipo, en su fila. Si se pasa, dos diagramas (vista general y detalle) o el detalle a las fichas.
- **Un foco**: el primario marca una o dos cosas (el estado del que se habla, la pieza clave, el camino principal). Lo demás, en tinta y gris.
- **«Desde cualquier estado»**: lo que vale desde varios estados es una nota (`Reabrir, desde Observación o Cerradas: vuelve a En curso`), no una flecha desde cada uno.
- **Flechas**: ángulo recto con codos redondeados (r = 8); recta solo si los extremos comparten x o y; salen y entran perpendiculares al borde, a 8 o más de la esquina. Gris por defecto, primario el camino principal, **discontinua** (`5,4`) lo opcional, la vuelta, lo asíncrono, lo previsto y lo destructivo. Se pintan antes que las cajas.
- **Sin solapes**: dos flechas no comparten trazo (12 de separación; un puente en el único cruce); en un mismo borde, cada una su punto (`L·k/(N+1)`, 12 de separación); ninguna pasa por detrás de una caja que no sea su origen o destino.
- **Etiquetas de flecha**: verbo en mayúsculas monoespaciadas (`class="d-etiqueta"`), 14 caracteres como mucho, sobre su máscara opaca (`class="d-mascara"`) y a 6–10 de su trazo: al lado en los tramos verticales; nunca vertical ni encima de la línea; la máscara no queda bajo una caja pintada después. Si representa un botón del panel, puede llevar su color, solo en el texto: sin cápsula, fondo ni forma de botón (decisión 301).
- **Carriles con nombre**, opcionales (apagados por defecto, decisión 302): cuando hay lados (vueltas, fases, salidas, o el actor), dicen qué es cada flecha antes que su forma.
- **Sin**: sombras, degradados, brillos, esquinas de más de 10, cajas idénticas para todo, leyenda flotando dentro del dibujo (va en una franja abajo), título dentro del SVG.

Estética, funciones de color, letra y plantillas de nodo: `references/estilo.md`.

## Interacción de la SF

Cada nodo puede tener su **ficha**, con lo que no cabe en el dibujo. Contrato del marcado y comportamiento: `references/interaccion.md`; código: `assets/diagramas.css` y `assets/diagramas.js`, sin dependencias.

- **Al pulsar** un nodo (clic, toque, Intro o Espacio): su ficha en un **HUD**; en una figura de 800 px o más, junto al nodo y fuera del dibujo si cabe; en una más estrecha, a todo su ancho, bajo el nodo. Las fichas van ocultas en la figura (`<div class="d-fichas" hidden>`): no hay lista debajo del dibujo.
- **Cajas** (grupo de la herramienta): **Forma**, redondeada o croqueta (cápsula); **Borde**, fino (el de diagram-design), sin borde o grueso; **Fondo**, sin fondo, claro o tintado; **Detalle**, sans o mono (la de diagram-design). Con `chip=TIPO` en los datos, el chip va dentro de la caja, arriba a la izquierda, y se enseña con «Chips de tipo». El foco y las salidas guardan su distinción, y las flechas tocan siempre el contorno.
- **Flechas y etiquetas**: **Grosor**, fino (el de diagram-design), normal o grueso; **Punta**, triángulo lleno, abierta o ninguna; **Esquinas**, redondeadas o en ángulo recto; **Colores de los datos** (apagado, todo en gris) y **Estilos de los datos** (apagado, sin cursivas ni discontinuas). El color y el estilo de cada flecha los dan sus datos (`references/datos.md`); el generador no tiene reglas de un tipo de diagrama.
- **Notas**: se ven o no; **Recuadro**, sin borde, fino o con barra de acento; **Fondo**, sin fondo, claro o tintado; **Tamaño**, compacto, normal o amplio; **Ubicación**, en el hueco libre de la horizontal (si no cabe, debajo; el hueco queda reservado aunque se pongan en otro sitio), debajo a todo lo ancho o en una columna de 200 al lado (el dibujo se ve al 80 %, aún dentro de la letra mínima); en la vertical, siempre debajo; **Cabecera**, mono en mayúsculas o negrita.
- **Plegado** (Interacción): todas desplegadas, todas plegadas (solo el nombre, y la figura más compacta) o máximo una desplegada (empiezan plegadas; abrir una pliega la otra, y volver a pulsarla la pliega). Cada caja con detalle lleva un circulito en su esquina que la pliega o la despliega sola: crece o encoge en su sitio, sus flechas la siguen y las demás no se mueven.
- **Recorrido** (Interacción): el resaltado en el segundo color del tema (por defecto; el foco sigue en el acento), en el acento o más grueso con su color.
- **Resaltado del recorrido**: al pasar el ratón, con el foco o con la ficha abierta, el nodo, sus flechas y sus vecinos; lo demás se atenúa.
- **Escape** cierra la ficha y devuelve el foco al nodo; pulsar fuera o ✕ también.
- **Accesible**: nodos con foco de teclado y 24 px o más; el ✕ del HUD de 44 × 44; el `<svg>` con nodos pulsables es `role="group"` (el script lo cambia); transiciones que se apagan con movimiento reducido.
- **Hueco para más modos**: `data-modo` en la figura y `window.sfDiagramas.modos`. El replay queda para una tarea aparte.

## Comprobación

```bash
python -I -X utf8 <skills>/diagramas/scripts/comprobar_diagramas.py <página.html> [--anchos 375,1440] [--letra-min 6.5] [--oscuro]
```

Abre la página en Chromium (o el Chrome o el Edge del equipo) y, en cada ancho, para cada `<svg>` de una `<figure>` que se vea: textos que se pisan, se salen del dibujo o de su caja o van pegados a su borde; cajas que se pisan; líneas que cruzan un texto o máscaras que las tapan; página o dibujo más anchos que la pantalla; letra por debajo del mínimo; contraste (4,5:1 el texto, 3:1 el grande y las flechas); nombre accesible y tamaño de lo que se pulsa; y, en las figuras interactivas, que cada nodo se pulse, abra su ficha, resalte su recorrido y se cierre con Escape. Con `--oscuro`, también con `data-theme="dark"`. Sale con 1 si hay errores. Después, una captura a 375 y a 1440 y mirarla: el script no ve si el diagrama se entiende.

## Lista de comprobación

- [ ] ¿Lo diría igual una tabla o un párrafo? ¿Se puede quitar un nodo, unir dos, quitar una flecha o una etiqueta?
- [ ] Tipo de `references/tipos.md`, dentro de su presupuesto; uno o dos focos.
- [ ] Vertical a 400; horizontal solo con su vertical al lado.
- [ ] Flechas en ángulo recto, sin solapes, con su punto en cada borde, pintadas antes que las cajas.
- [ ] Etiquetas sobre su máscara, separadas de su línea.
- [ ] Datos reales, mismo orden y colores que el resto del documento; nada que no esté en el texto.
- [ ] `role` y nombre accesible (`aria-labelledby` a `<title>` y `<desc>` con ids propios, o `aria-label`); `<figcaption>` breve.
- [ ] El script sin errores, y la captura revisada.

## Pendiente (por decidir)

- **Ancho de las verticales**: 400 (provisional), 420 (página de síntesis de la tarea 308) o 560 (guía actual).
- **Integración** con `crear_documentos` y su generador (cargar `diagramas.css` y `diagramas.js`, y el ancho de `figure.vertical`).

## Origen

Adaptada de **diagram-design**, de Cathryn Lavery: <https://github.com/cathrynlavery/diagram-design>, commit `f24d98b05e2d7a5e68c2dedfe46e5b7173f50118`, licencia MIT («Copyright (c) 2025 Cathryn Lavery»; aviso completo en `LICENSE-diagram-design`). Se toman su filosofía, sus 45 tipos con sus convenciones y límites, las reglas de las flechas, el foco, el presupuesto, «desde cualquier estado», las funciones de color de los nodos y su lista de comprobación. Cambia: en español y compacta; los colores y la letra son los del tema de `crear_documentos`, y su piel pasa a ser el tema `tinta` (con `texto-tenue` oscurecido a `#666e83` para 4,5:1 sobre el papel), sin incorporación de marca ni perfiles; sin título dentro del SVG; vertical por defecto con elección de forma por figura; letra mínima medida en pantalla; la interacción (fichas en el HUD, resaltado y Escape) y el script de comprobación son de la SF; fuera la importación de draw.io, mermaid y Excalidraw, la exportación a PNG, las variantes boceto y terminal y su animación. Para el detalle fino de un tipo, su `references/type-<tipo>.md` en ese commit.
