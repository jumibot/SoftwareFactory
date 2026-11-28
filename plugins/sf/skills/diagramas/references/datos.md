# Datos del generador

Formato de `scripts/generar_diagrama.py`. Una clave por línea; las secciones, con una entrada sangrada por línea; `#` empieza un comentario. Un ejemplo por tipo, en `assets/ejemplos/`.

## Antes de dibujar

Lo que fijan los pasos 0 y 1 de `SKILL.md` (decisiones 385 y 387), por escrito al principio de los datos, para que el generador y el comprobador lo usen:

```text
objetivo: Qué tiene que entender o decidir quien lo mira, en qué documento y en qué punto.
concepto: El concepto en dos o tres frases llanas.
puntos-clave:                      # una frase cada uno | dónde se ve: nodo o zona (una caja que lo resume vale), «a > b», «a > b > a» (un bucle: cada tramo, por un camino del dibujo)
  Un fallo vuelve a lanzar lo ya pasado. | pruebas > repetir > pruebas
modulos-clave: vuelta, pruebas, repetir   # los nodos o zonas que tienen que estar; las carpetas, solo de estos
interconexiones-clave:             # las conexiones (o bucles) que tienen que estar
  pruebas > repetir > pruebas
decisiones: repetir               # los pasos del concepto que son decisiones (dec, con su pregunta): cada «si …»
actores: subagente, orden          # quién actúa; con más de uno, el primer paso dice cuál y luego donde cambia
glosario:                          # cinco a diez términos importantes: término | qué es (423); inspira, no obliga (426)
  orden | la herramienta que selecciona, lanza y resume los tests de la vuelta
compara-con: otro.diagrama         # opcional: va al lado de otro, los dos en vertical sin leerse (salvo que fijen otra orientación); avisa si cambian el tipo, las cajas, la forma, la orientación o el glosario
antes: viejo.diagrama              # opcional: se rehace; mismos pasos, flechas, bucles y etiquetas que él
fijo: pasos, flechas, bucles       # opcional: qué compara «antes:», por ids (por defecto, eso, las decisiones y las etiquetas)
```

Errores: un punto clave sin dónde o que no aparece, un módulo o una interconexión clave que no aparecen, una carpeta que no es un módulo clave y lo que cambie respecto a `antes:`. Sin objetivo, concepto o puntos clave, un aviso; con `--exigir`, un error. El comprobador mira que cada punto clave se vea en el dibujo; con los bloques cerrados al empezar, cuenta como visible si se ve su bloque; el glosario no se le exige: ni términos sin usar ni palabras de fuera (decisión 426). Avisos de los rótulos (decisiones 422 y 423): un paso sin verbo y objeto o con un modo («a ojo») en su lugar, el actor que no se dice o que va en cada título, un rótulo que no habla de su id, un bucle que no dice cuándo acaba, una rama que no vuelve sin decir en qué acaba, una etiqueta que explica en vez de decir lo que pasa y la discontinua con dos sentidos; y de la estructura: un bucle que vuelve desde una acción, un paso que es una condición («si …», «tras cada …») sin ser decisión y un proceso o unos estados sin `inicio > id`; y de lo que sobra (387, criterio): más de ocho cajas con objetivo («¿la versión más simple?») y un código o una cifra en un nombre o una etiqueta (a la ficha). Error: un paso de «decisiones:» que no es `dec`; lo que cuelga de un solo paso o sale del camino y acaba fuera de él (la rama de una decisión que no vuelve, con lo que solo se une a ella) y no cabe a su lado: se acortan los rótulos, no se quita su marca; con `--exigir`, también dejarlo en el eje con `una-columna` (sin él, un aviso); y unas vueltas largas que no caben a la derecha de la columna. El comprobador da error si una flecha se sale del dibujo (queda cortada) o su etiqueta queda a más de 16 de ella, y avisa si la de una salida de una decisión queda lejos de la decisión. `--lectura` da el dibujo en texto para la lectura en frío.

## Datos

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
zonas:                             # cada zona, sus nodos en el orden en que se colocan (una cadena, en serpentina)
  repo: REPOSITORIO | dev, main
fichas:                            # una por nodo, con su resumen y sus líneas
  pend: En la cola, sin rama.
    - ACTIVAR RAMA: con rama → En curso
    - ELIMINAR (rojo): → fuera de la cola
    - claude: la reabre → En curso
recorrido:                         # opcional: el replay, paso a paso, con el porqué de cada uno
  pend: La tarea espera en la cola, sin rama.
  pend > curso: Al activar la rama empieza el trabajo.
```

- **Nodo**: `id: Nombre | detalle | clases`. Clases: `accion` (una acción fuera del camino que cambia algo: píldora con borde morado; con eje, a la izquierda salvo con `lado`), `nuevo` (lo que cambia: «Solo lo nuevo» lo deja a la vista; también como marca de flecha), `previsto` (lo que aún no existe: discontinuo y en gris; también como marca de flecha), `lado` e `izquierda` (proceso y estados: al lado del eje, en la columna de la derecha o de la izquierda, a la altura del nodo al que se unen; ver «Eje con entradas»; con `lado`, el generador prueba también la izquierda y se queda con la que mejor se lee), `salida` (a la segunda columna o fila), `final` (anillo de fin, sin caja), `fin` (estado final con su marca), `dec` (decisión, hexágono), `externo` (borde discontinuo), `chip=TIPO` (con `opciones: chips`; en la ficha del HUD sale siempre, como tipo encima del nombre). Las clases van separadas por `|` o por espacios (`externo lado`).
- **Flecha**: `de > a: ETIQUETA | marcas` o, sin etiqueta, `de > a | marcas`; las marcas, separadas por `|` o por espacios (`flujo discontinua`). El generador no da color ni estilo por su cuenta: lo dan los datos de cada flecha. Marcas:
  - **Color de la etiqueta**: `color=X` o `X` sola; **color de la línea** (y de su punta): `linea=X`. Colores: `acento`, `segundo` (los del tema), `gris`, `verde`, `rojo` y `morado`. `principal` es `linea=acento`.
  - **Flujo**: `flujo` marca las flechas que llevan el concepto que fluye (`SKILL.md`, «Flujos que se leen de un tirón»): en el acento y más gruesas, las principales; `principal` solo colorea la línea.
  - **Estilo**: `cursiva` (la etiqueta en la cursiva de escena), `discontinua` (la línea), `vuelta` (discontinua y, entre vecinas hacia atrás en la fila horizontal, por encima). `claude` es un atajo de estilo: `cursiva` y `vuelta`.
  - `estado=X` (secuencia: el estado al que pasa).
  - El ejemplo de estados pide en sus datos el verde de sus botones (`| verde`) y la marca `claude` en lo que hace Claude.
- **Eje con entradas** (proceso y estados, decisión 326): con algún nodo `lado` o `izquierda`, la vertical pone el camino (los nodos sin esas clases, en el orden de los datos) en una columna y cada nodo de al lado en la suya, a la altura de su ancla: el primer nodo del eje al que se une o, si no hay, el de la otra columna. Su flecha va recta y corta. Los de al lado sin ancla se apilan en su columna, en el orden de los datos (el control encima de las entradas, por ejemplo). Un origen con tres flechas o más a una misma columna de al lado reparte en bus: un tronco por fuera de la columna y ramas cortas. Cada zona es un marco alrededor de sus nodos, estén en la columna que estén; las vueltas van por un carril a la derecha, por fuera de todo. Si las columnas no caben, lo dice: nombres más cortos (se parten en dos líneas, y una ruta tras una barra) o un detalle que pase a la ficha.
- **Caja con acento**: `foco: id` arriba o la clase `foco` en el nodo. `inicio > id` pone el punto de inicio (a la izquierda de la fila si cabe).
- **Recorrido** (replay): un paso por línea, en el orden de la historia: `id: porqué` ilumina un nodo y `de > a: porqué` una flecha de «flechas:». El porqué, una o dos frases con lo que pasa y por qué, que el dibujo no dice; sin él, el paso enseña la ficha del nodo. La figura gana el botón «Recorrer paso a paso» (`references/interaccion.md`).
- **Nota**: `CABECERA: texto`, con la acción primero («DESDE EN OBSERVACIÓN O CERRADAS: Revertir → Pendientes o fuera de la cola»). Recuadro tintado sin borde; en la horizontal, en el hueco a la derecha de las salidas si cabe en las cuatro variantes y con el tamaño amplio; si no, y en la vertical, debajo, en su propio `<svg>` del mismo ancho (y otro de 240 para ponerlas al lado). Se dibujan los tres tamaños y se ve el del ajuste. La cabecera salta de línea si no cabe.
- **Bloques** (proceso y estados con dos zonas o más, decisión 415): el generador deduce, con todas las flechas entre zonas (sin las de las acciones), su forma, por partes: un par de zonas con flechas en los dos sentidos (ida y vuelta) cuenta por su ida y va vecino, con la ida y la vuelta separadas; un ciclo, de todas las zonas o de solo algunas, en anillo (la primera zona, una fila arriba de derecha a izquierda; las demás, columnas que bajan y suben; lo que no está en el ciclo, en columnas que cuelgan de él); sin ciclo, una cadena o una jerarquía (en columnas, por orden); lo dibuja y lo mide contra la forma apilada; se queda la que mejor se lee. Cada zona es una sola carpeta en cualquier forma: la apilada junta los pasos de una zona aunque la ruta salga y vuelva a ella, y el comprobador da error si una zona se pinta en dos carpetas. `anillo: a, b, c` (las zonas en el orden del ciclo, la primera arriba) o `columnas: a | b | c` lo fijan; `opciones: una-columna` lo apaga. La figura empieza con los bloques cerrados (una carpeta por zona, con su nombre en la pestaña, cuántos pasos tiene y el fondo suave del color de su cauce; las zonas abiertas son la misma carpeta en grande; entre dos cerrados, una flecha ancha; pulsarla la abre en su sitio y el nombre de la zona la cierra; «Abrir todos», entera; al imprimir, abierta); `opciones: abiertos` empieza abierta. Dentro de un bloque, una cadena lineal sigue en el camino aunque sus pasos sean `lado`: va recta si cabe.
- **Ramas laterales** (proceso y estados): una caja que solo se une con un paso que no es el de antes va al lado de ese paso si así se lee mejor (el generador dibuja las dos y mide; en la horizontal, en la segunda fila). Lo que sale del camino y acaba fuera de él (la rama de una decisión que no vuelve) también. `opciones: una-columna` lo deja todo en una columna, salvo eso último (con `--exigir`, error; sin él, aviso).
- **Zonas dentro de zonas**: una zona nombra otra por su id (`motor: MOTOR | cad, d` y `cad: CADENA | a, b, c`). La de dentro es una carpeta dentro de la de fuera, con su nombre en la pestaña y el fondo suave de su cauce, en todos los tipos (opción B del propietario): en el eje y en los bloques, si en su marco no cae ninguna caja de fuera; en la columna, si sus nodos van seguidos en el camino; en la rejilla de arquitectura y piezas, en su propio trozo de la banda o de la columna, o en su fila. Si no hay sitio para la pestaña sin que la cruce una flecha, su nombre va de cabecera sobre su primer nodo. La fila horizontal del proceso y de los estados no dibuja zonas: si una es un punto clave, la figura se queda en vertical. Una zona va dentro de una sola.
- **Flecha a una zona** (decisión 420): lo que actúa sobre varias cajas a la vez apunta a la zona que las lleva (`acc > cadena`, con el id de la zona) y la flecha llega a su carpeta, a la altura de su centro; una zona de dentro a la que llega una flecha se dibuja como carpeta, con su nombre en la pestaña. Sus pasos van seguidos en una columna. En arquitectura y piezas, la flecha se enruta a su paso de en medio y se corta donde entra en la carpeta. Donde no hay carpetas (la fila sin bloques, la columna), la flecha llega a su paso de en medio. `corchetes:` ya no existe: el generador lo rechaza y pide una zona.
- **Completo**: `opciones: completo` deja en informativo el aviso del presupuesto (9 nodos y 12 flechas, una recomendación), para un diagrama que tiene que estar entero.
- **Cauces**: `cauce=X` en una flecha dice qué viaja por ella (audio, control…; `_` por espacio). El cauce de las flechas `flujo` va en el color del camino (acento); los demás, en segundo, morado, verde y gris, por orden (una `linea=` de los datos manda). Con dos cauces o más, la figura lleva su leyenda bajo la cabecera: una raya de cada color con su nombre.
- **Fichas**: cada línea, `- texto`; `- CABECERA: texto` la pone en negrita (`(color)` tras la cabecera le da color), `- claude: texto` en cursiva y `- codigo: texto`, una orden, una ruta o un nombre del código, en mono.
- **Opciones** (decisión 302): casillas, encendidas por defecto tarjeta, color (los colores de los datos), estilos (su cursiva y su discontinua), notas, foco, resaltado, fichas y regla, y apagadas carriles, chips, recuento y letra; se apagan con `sin X` y se encienden con `X`. Selectores, con su valor por defecto primero: `cajas=desplegadas|plegadas|acordeon`, `forma=redondeada|croqueta`, `borde=fino|ninguno|grueso`, `fondo=papel|ninguno|tintado`, `orientacion=auto|vertical|horizontal`, `antetitulo=oculto|encima|lado`, `titulo=sans|serifa|serifa-p|mono|oculto`, `desc=linea|completa|corta|oculta`, `pie=dos|izquierda|derecha|centrado|oculto`, `ayuda=encima|debajo|discreta|oculta`, `recorrido=segundo|acento|grueso`, `lienzo=papel|ninguno|tintado` (fondo del diagrama; en la herramienta, claro, sin fondo o tintado, como `fondo` y `fondo-nota`), `grosor=fino|normal|grueso`, `punta=llena|abierta|ninguna`, `esquinas=redondeadas|rectas`, `recuadro=sin|fino|barra`, `fondo-nota=tintado|papel|ninguno`, `tamano-nota=normal|compacto|amplio`, `lugar-nota=hueco|debajo|lado` y `cabecera-nota=mono|negrita`. Quedan en la figura (`d-no-X`, `data-d-X`) y la herramienta «diagramas» del documento las cambia; carriles y chips solo existen si los datos los piden.
- **Croqueta que no cabe**: si la vertical en croqueta no cabe (es más ancha) y la redondeada sí, esa variante usa el dibujo redondeado (`data-forma-dibujo`) y se avisa.
- **Orientación**: la vertical siempre; la horizontal, si cabe en 960. Si no cabe, avisa y deja solo la vertical (también por variante: la croqueta, más ancha, puede no caber); la figura lo apunta (`data-sin-h`, con las variantes sin horizontal) y, si se elige «Horizontal» (en los datos o en la herramienta), dice «No cabe en horizontal a este ancho: se ve en vertical». La herramienta desactiva la opción si no cabe en ninguna figura y, si no cabe en algunas, dice cuántas. Ni desplazamiento horizontal ni dibujo encogido: bajaría de la letra mínima. En la fila horizontal, las cajas llevan un mismo ancho si cabe y las flechas entre vecinas van rectas si su etiqueta cabe entre las cajas; si no, en arco por encima (la ida) o por debajo (la vuelta). Con la letra de diagram-design, las del ejemplo de estados van todas rectas. Si una etiqueta o un nombre no caben, para y dice cuál acortar.
- Grosores y letra: los de diagram-design (`references/estilo.md`).
