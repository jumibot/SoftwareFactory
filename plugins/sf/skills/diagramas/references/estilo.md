# Estilo

La estética de diagram-design (editorial: papel limpio, tinta, un acento para el foco, bordes finos en lugar de sombras) con los colores y la letra del tema de `crear_documentos`. Así un diagrama cambia de tema con el documento. **Tema de referencia: `tinta`** (`../crear_documentos/assets/temas/tinta.json`), su paleta, en claro y en oscuro: papel `#fbfbfa`, tinta `#25283a`, un solo acento óxido `#b8431c`; en oscuro, `#1b1d2c`, `#f2f2f0` y `#f08a59`. Con otro tema, las mismas funciones toman sus colores. Los colores se escriben con `style="fill:var(--…)"` o `stroke:var(--…)`; en una página suelta se definen esas variables en `:root`, como en `assets/ejemplo-estados.html`.

## Funciones de color

| Función | Variable | Para |
|---|---|---|
| tinta | `--texto` | Nombres de los nodos, inicio y fin |
| suave | `--texto-suave` | Detalle, etiquetas de flecha, flechas por defecto, bordes de los nodos |
| tenue | `--texto-tenue` | Borde de lo externo y de lo descartado (3:1 o más como trazo; no como texto) |
| rótulo | `--d-rotulo` | Nombres de zona, carriles, antetítulo, líneas de fase y de vida: el tenue oscurecido hacia `--texto` lo justo para 4,5:1 sobre el fondo de la figura, con cualquier tema (lo calcula `diagramas.js`; sin él, mitad y mitad) |
| línea | `--linea`, `--borde` | Separadores, zonas y la franja de la leyenda: decorativos, nunca lo único que lleva el significado |
| foco | `--primario`, con `--fondo` de relleno y `--oscuro` en su nombre | Uno o dos elementos y el camino principal |
| validado | `--acento` | Solo lo validado o la evidencia (guía común) |
| papel | `--diagrama-papel` (si no, `--pagina`, el papel del documento) | Fondo «Claro» del lienzo y máscaras de las etiquetas; el SVG no lleva fondo propio |

- **Categorías**: los colores con significado de la guía común (turquesa `#1f7a7a`, naranja `#a6501a`, verde `#1f812d`, frambuesa `#be185d`), como mucho tres por figura además del foco, solo en trazos, títulos y etiquetas. Las flechas no toman el color de la pieza.
- **Etiquetas de flecha**: texto mono, separado de su línea. La que representa un botón del panel puede llevar el color de ese botón, solo en el texto (`style="fill:<color>"`, 4,5:1 o más sobre el papel): sin cápsula, fondo ni forma de botón (decisión 301).
- **Lo destructivo** (descartar, eliminar, revertir) se distingue por el trazo discontinuo, no por otro color. ✓ en el primario; ✕ en `#991b1b`.
- **Modo oscuro**: en un documento, el de «Lectura» invierte la página entera, y el diagrama con ella; en una página suelta con un tema con `colores-oscuro`, como `tinta`, `data-theme="dark"` cambia las variables. En los dos casos, sin colores fijos ni fondo propio; las máscaras, del color de la página (`--diagrama-papel`).

## Tratamiento de los nodos

| Nodo | Relleno | Borde |
|---|---|---|
| foco (1–2) | `--fondo` | `--primario`, 2 |
| paso, servicio | ninguno | `--texto-suave`, 1,2 |
| almacén | ninguno, con el icono de cilindro | `--texto-suave` |
| externo | ninguno | `--texto-tenue` |
| entrada, persona | ninguno | `--texto-suave`, esquinas de 10 |
| opcional, previsto, asíncrono | ninguno | `--texto-tenue`, discontinuo `4,3` |
| frontera, seguridad | ninguno | `--texto-tenue`, discontinuo `4,4`, con su nombre sobre máscara |

Esquinas de 6 en los nodos, 8 en las zonas y 2 en las etiquetas de tipo (rectangulares, nunca píldoras). Trazo de 1,2; 2 el foco. Sin sombras, degradados ni brillos.

## Letra

Todo con la del tema (`--fuente-texto`), salvo:

- **monoespaciada** (`ui-monospace, Consolas, monospace`, `class="d-etiqueta"`) para las etiquetas de flecha y lo técnico: rutas, órdenes, puertos, tipos;
- **cursiva de escena** (`--fuente-escena`, `font-style="italic"`) para las anotaciones y lo que hace Claude.

Tamaños de diagram-design (su escala «standard»), en el `viewBox` de 960 de la horizontal; la vertical de 400, que a 375 se ve a un 86 %, los lleva 7/6 mayores para que en el móvil se lean al tamaño de la original:

| Papel | Horizontal | Vertical | Peso |
|---|---|---|---|
| nombre del nodo | 12 | 14 | 650 |
| detalle | 9 | 10,5 | 400 |
| etiqueta de flecha, cabecera de nota, chip, carril | 8 (mono) | 9,5 | 400 |
| lo que hace Claude (cursiva) | 12 | 14 | 400 |
| texto de nota (normal; compacto 9, amplio 11,5) | 10 | 11,5 | 400 |

Cajas como las de diagram-design: 48 de alto con solo el nombre y 56 con detalle (72 con chip de tipo, que va dentro, arriba a la izquierda, en mono de 7 con su recuadro de 0,8), 150 de ancho en la fila si deja rectas las flechas entre fases (si no, el mínimo, 104), radio 6 y 16 de relleno a cada lado. El detalle, en sans o en mono (ajuste «Detalle»; la original, mono). Fuera del SVG: antetítulo .66rem y pie .72rem (mono), como la original. «Letra más grande» los sube un 9 %. Trazos: cajas 1 (el de diagram-design; «Grueso», 1,8), flechas 1,2 («Normal» 1,6, «Grueso» 2,2), puntas de 8,4 (7 por el trazo de 1,2) y carriles 1. El comprobador pide 6,5 px en pantalla: la etiqueta de 8 en la horizontal vista desde 800 px. Cuenta de ancho: 0,6 em por carácter en la letra del texto y 0,62 em en la monoespaciada; una caja deja 16 a cada lado de su texto. Lo que no cabe se acorta, no se encoge.

## Esqueleto

Orden de pintado: zonas, flechas, máscaras y etiquetas, nodos, anotaciones. Una flecha resaltable lleva `data-de` y `data-a`; su etiqueta, también.

```html
<figure class="diagrama" data-diagrama data-marca-on="x-on">
<svg class="vertical" viewBox="0 0 400 {alto}" role="img" aria-labelledby="x-t x-d">
<title id="x-t">{Nombre corto}</title><desc id="x-d">{Una frase con lo que dice}</desc>
<defs><marker id="x-m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--texto-suave)"/></marker>
<marker id="x-on" …><path … style="fill:var(--primario)"/></marker></defs>
<path data-de="a" data-a="b" d="M116,124 V182" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.4" marker-end="url(#x-m)"/>
<rect class="d-mascara" x="122" y="137" width="104" height="22" rx="2"/>
<text class="d-etiqueta" data-de="a" data-a="b" x="126" y="153" font-size="15.5" style="fill:var(--texto-suave)">VERBO</text>
<g data-nodo="a"><rect class="d-caja" x="16" y="64" width="200" height="60" rx="6" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.2"/>
<text x="32" y="90" font-size="17" font-weight="650" style="fill:var(--texto)">{Nombre}</text>
<text x="32" y="112" font-size="15.5" style="fill:var(--texto-suave)">{Detalle en una línea}</text></g>
</svg>
<figcaption>{Qué hay que ver}</figcaption>
<div class="d-fichas" hidden><div data-ficha="a" data-nombre="{Nombre}"><p>…</p></div></div>
</figure>
```

Los ids (`x-t`, `x-m`…) llevan un prefijo propio de cada figura. Leyenda, si hace falta: una franja abajo, tras una línea fina, con 60 más de alto.
