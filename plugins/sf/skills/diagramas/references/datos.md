# Datos del generador

Formato de `scripts/generar_diagrama.py`. Una clave por línea; las secciones, con una entrada sangrada por línea; `#` empieza un comentario. Un ejemplo por tipo, en `assets/ejemplos/`.

```text
tipo: estados                      # estados, proceso, arquitectura, piezas, secuencia o fases
titulo: Ciclo de vida de una tarea
descripcion: Una línea; salta si hace falta, nunca se corta.
pie: SF · PANEL | LA COLA          # izquierda | derecha (opcional)
foco: curso                        # el nodo destacado
opciones: carriles, cajas=plegadas  # opcional; ver abajo
nodos:                             # en la secuencia, «actores:»
  pend: Pendientes | sin rama
  cerr: Cerradas | en develop | fin
  desc: Descartada | sin botones | salida
flechas:                           # en la secuencia, «mensajes:»
  inicio > pend
  pend > curso: ACTIVAR RAMA
  curso > pend: sin trabajo | claude
  curso > cerr: CERRAR             # en estados, sin color: verde
  curso > desc: DESCARTAR | rojo
notas:                             # lo que vale desde varios estados
  DESDE OBSERVACIÓN O CERRADAS: Claude la reabre → En curso
zonas:                             # arquitectura y piezas: cada zona, sus nodos en orden
  repo: REPOSITORIO | dev, main
fichas:                            # una por nodo, con su resumen y sus líneas
  pend: En la cola, sin rama.
    - ACTIVAR RAMA: con rama → En curso
    - ELIMINAR (rojo): → fuera de la cola
    - claude: la reabre → En curso
```

- **Nodo**: `id: Nombre | detalle | clases`. Clases: `salida` (a la segunda columna o fila), `final` (anillo de fin, sin caja), `fin` (estado final con su marca), `dec` (decisión, hexágono), `externo` (borde discontinuo), `chip=TIPO` (con `opciones: chips`).
- **Flecha**: `de > a: ETIQUETA | marcas`. El generador no da color ni estilo por su cuenta: lo dan los datos de cada flecha. Marcas:
  - **Color de la etiqueta**: `color=X` o `X` sola; **color de la línea** (y de su punta): `linea=X`. Colores: `acento`, `segundo` (los del tema), `gris`, `verde`, `rojo` y `morado`. `principal` es `linea=acento`.
  - **Estilo**: `cursiva` (la etiqueta en la cursiva de escena), `discontinua` (la línea), `vuelta` (discontinua y, entre vecinas hacia atrás en la fila horizontal, por encima). `claude` es un atajo de estilo: `cursiva` y `vuelta`.
  - `estado=X` (secuencia: el estado al que pasa).
  - El ejemplo de estados pide en sus datos el verde de sus botones (`| verde`) y la marca `claude` en lo que hace Claude.
- **Caja con acento**: `foco: id` arriba o la clase `foco` en el nodo. `inicio > id` pone el punto de inicio (a la izquierda de la fila si cabe).
- **Nota**: `CABECERA: texto`, con la acción primero («DESDE EN OBSERVACIÓN O CERRADAS: Revertir → Pendientes o fuera de la cola»). Recuadro tintado sin borde; en la horizontal, en el hueco a la derecha de las salidas si cabe en las cuatro variantes y con el tamaño amplio; si no, y en la vertical, debajo, en su propio `<svg>` del mismo ancho (y otro de 240 para ponerlas al lado). Se dibujan los tres tamaños y se ve el del ajuste. La cabecera salta de línea si no cabe.
- **Opciones** (decisión 302): casillas, encendidas por defecto tarjeta, color (los colores de los datos), estilos (su cursiva y su discontinua), notas, foco, resaltado, fichas y regla, y apagadas carriles, chips, recuento y letra; se apagan con `sin X` y se encienden con `X`. Selectores, con su valor por defecto primero: `cajas=desplegadas|plegadas|acordeon`, `forma=redondeada|croqueta`, `borde=fino|ninguno|grueso`, `fondo=papel|ninguno|tintado`, `orientacion=auto|vertical|horizontal`, `antetitulo=oculto|encima|lado`, `titulo=sans|serifa|serifa-p|mono|oculto`, `desc=linea|completa|corta|oculta`, `pie=dos|izquierda|derecha|centrado|oculto`, `ayuda=encima|debajo|discreta|oculta`, `recorrido=segundo|acento|grueso`, `lienzo=papel|ninguno|tintado` (fondo del diagrama; en la herramienta, claro, sin fondo o tintado, como `fondo` y `fondo-nota`), `grosor=fino|normal|grueso`, `punta=llena|abierta|ninguna`, `esquinas=redondeadas|rectas`, `recuadro=sin|fino|barra`, `fondo-nota=tintado|papel|ninguno`, `tamano-nota=normal|compacto|amplio`, `lugar-nota=hueco|debajo|lado` y `cabecera-nota=mono|negrita`. Quedan en la figura (`d-no-X`, `data-d-X`) y la herramienta «diagramas» del documento las cambia; carriles y chips solo existen si los datos los piden.
- **Orientación**: la vertical siempre; la horizontal, si cabe en 960. Si no cabe, avisa y deja solo la vertical (también por variante: la croqueta, más ancha, puede no caber). En la fila horizontal, las cajas llevan un mismo ancho si cabe y las flechas entre vecinas van rectas si su etiqueta cabe entre las cajas; si no, en arco por encima (la ida) o por debajo (la vuelta). Con la letra de diagram-design, las del ejemplo de estados van todas rectas. Si una etiqueta o un nombre no caben, para y dice cuál acortar.
- Grosores y letra: los de diagram-design (`references/estilo.md`).
