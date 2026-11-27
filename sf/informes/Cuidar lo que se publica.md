---
antetitulo: Software Factory · Informe de diseño · Noviembre 2026
lema: Revisar lo ya publicado // y decidir si develop se queda fuera.
subtitulo: Cada cuánto, con qué y qué hacer al revisar los repositorios públicos del propietario, y si develop puede guardarse en uno privado.
version: Versión 1.1 · 27/11/2026
estado: Decidido · Tarea 331
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de diseño
pie: Informe de la tarea «Cuidar lo que se publica: revisar los repositorios públicos y guardar develop en uno privado» (331). Parte de revision_publica.py, cola.py, hooks/cola.ts y las decisiones 252, 259 y 280; no se ha accedido a GitHub. Decidido por el propietario en las decisiones 391 y 392.
---
# Cuidar lo que se publica

## Resumen | Revisar con lo que ya hay, avisar en el panel, y la copia privada con cautela | Resumen {#resumen}

Hoy la SF revisa lo que **sale**: `revision_publica.py` mira los commits nuevos al subir develop y en RELEASE, y bloquea si el remoto es público (259). No mira lo que **ya está publicado** ni los demás proyectos entre releases. Se propone una revisión periódica de los repositorios públicos del propietario con la misma herramienta, ampliada para recorrer todo el historial, que avise en el panel y deje el arreglo a una sesión de cada proyecto.

La copia privada de develop es una opción por proyecto, pero con una pega: RELEASE pasa main por fast-forward desde develop, así que **los commits de develop salen igualmente al publicar**. Solo se queda fuera lo que aún no se ha publicado y las ramas de tarea. La 252 ya descartó una vez subir solo main y tags («no quiero complicarlo»); aquí se reabre con ese dato.

El propietario ha decidido las 6 preguntas y no queda ninguna abierta. Se revisa cada 15 días con la herramienta de la SF y el escaneo de GitHub, y se avisa en el panel (decisión «Los repositorios públicos se revisan cada 15 días…», 391); develop sigue en el remoto del proyecto, sin copia privada (decisión «Sin copia privada de develop…», 392). Sale una tarea, la 465, y una propuesta, «Tareas periódicas en la cola» (P26).

[Ver lo decidido](#decidido){: .salto}

## Hoy | Lo que ya revisa la SF y lo que no | Hoy {#hoy}

::: tarjetas 3

### Qué cubre

`revision_publica.py` busca secretos, datos personales, rutas de la máquina y archivos internos en los commits entre el último tag y develop. Lo lanzan RELEASE y `cola.py subir` (también al cerrar una tarea). Con remoto público, lo nuevo bloquea; lo ya subido pide permiso (259).

### Qué no cubre

El historial anterior al último tag, el árbol actual de repositorios ya publicados, los proyectos que no están abiertos, y el paso del tiempo: nada se vuelve a mirar tras publicar. Los hallazgos que no se corrigen se aceptan en `.sf/publicable.txt`.

### Qué ya sirve

Sin `--desde`, `revisar` mira todos los commits de la rama, así que un recorrido completo ya es posible con un clon local. Necesita `gh` para saber si el repositorio es público. La identidad de la máquina (usuario, rutas) solo se detecta en el equipo del propietario.

:::

## Revisión | Cómo sería la revisión de los públicos | Revisión {#revision}

Se propone: una orden de la SF (`revision_publica.py --repositorios`) que lista con `gh repo list --visibility public`, clona cada uno en una carpeta temporal y revisa todo el historial de su rama de publicación y su árbol actual; sin tocar los repositorios ni escribir en ellos. Lo que cuenta como hallazgo es lo de hoy (secretos, datos personales, rutas, internos), con las excepciones de cada proyecto en `.sf/publicable.txt` cuando se tenga su clon. Para repositorios ajenos a la SF no hay esa lista: se aceptan hallazgos en un archivo del propietario.

Límites: esta revisión detecta por patrones, no entiende el contexto; un historial ya público no se «despublica» con arreglar el árbol (haría falta reescribir la historia o rotar el secreto); y GitHub ofrece de serie secret scanning y push protection para repositorios públicos, que cubren secretos pero no rutas ni datos personales.

## Decidido | Lo que ya está decidido | Decidido {#decidido}

| Nº | Decisión | Qué fija aquí |
| --- | --- | --- |
| 252 | La SF se trabaja en el repositorio público, con revisión antes de publicar | develop se sube al público; se valoró subir solo main y tags y no se quiso |
| 259 | Revisión antes de publicar: bloquear en público, preguntar en privado, y revisar también al subir develop | La herramienta y su política, de la que parte este informe |
| 280 | Migración al repositorio público: develop público, ramas de tarea locales y _respaldo/ públicos | Hoy las ramas feature no se suben |
| 391 | Los repositorios públicos se revisan cada 15 días con la herramienta de la SF y lo encontrado se avisa en el panel | Preguntas 1 a 4: herramienta de la SF con el escaneo de GitHub además, cada 15 días con aviso del panel, sin escribir en proyectos ajenos |
| 392 | Sin copia privada de develop: develop sigue en el remoto del proyecto | Pregunta 5, opción A; la 6 decae |

## Por decidir | Lo que queda por decidir | Por decidir {#por-decidir}

Las seis preguntas, por importancia, están decididas; ninguna sigue abierta. Las 1 a 4 son de la revisión periódica (decisión 391); la 5 y la 6, de la copia privada (decisión 392).

::: preguntas 2 plegables

### 1 · Con qué se revisan los repositorios públicos {estado=decidida elegida=B} {: #p1}

Hoy `revision_publica.py` ya sabe buscar; falta el recorrido de repositorios y la periodicidad.

Opción A
:   Solo lo de GitHub (secret scanning y push protection, que se activan por repositorio). Sin código nuevo, pero solo secretos.

Opción B
:   Herramienta de la SF: ampliar `revision_publica.py` con un recorrido de los repositorios públicos y su historial. Cubre secretos, datos personales y rutas; corre en el equipo del propietario.

Opción C
:   Rutina programada en la nube (skill `schedule`) que ejecuta la revisión. Corre sola, pero no ve la identidad de la máquina ni los repositorios locales, y gasta cuota sin que el propietario lo vea.

Recomendación
:   **B**, con la opción A activada además, que es gratis. La nube (C) se descarta por no ver rutas ni usuario de la máquina, que es lo que más se cuela.

Decisión
:   **B**, con el escaneo de secretos de GitHub activado además. Decisión 391.

### 2 · Cada cuánto se revisan {estado=decidida elegida=B} {: #p2}

Opción A
:   Solo a mano, cuando el propietario lo pida.

Opción B
:   Cada 15 días, avisando cuando pasa el plazo sin revisar: el latido del panel mira la fecha de la última revisión y, si venció, avisa; revisar es un clic.

Opción C
:   Cada vez que se abre sesión, si pasó una semana.

Recomendación
:   **B.** Los repositorios públicos cambian poco entre releases; un aviso propio del panel evita depender de la memoria sin lanzar nada en segundo plano.

Decisión
:   **B**: cada 15 días, con aviso del panel cuando vence. Decisión 391.

### 3 · Qué se hace con lo encontrado {estado=decidida elegida=A} {: #p3}

Opción A
:   El panel lo avisa con la lista corta (repositorio, archivo, motivo) y una orden para abrir la lista completa. El arreglo de cada repositorio se hace en una sesión de ese proyecto, como pidió el propietario; la SF no toca repositorios ajenos.

Opción B
:   Además, se apunta una petición en la cola de cada proyecto afectado. Más directo, pero escribe en colas de proyectos no abiertos.

Opción C
:   Solo un informe en un archivo, sin avisar.

Recomendación
:   **A.** Avisar y no escribir en proyectos ajenos; B puede venir después con la sesión del proyecto ya abierta.

Decisión
:   **A**: el panel avisa y cada repositorio se arregla en una sesión de su proyecto. Decisión 391.

### 4 · Cómo se programa: tarea periódica o aviso del panel {estado=decidida elegida=B} {: #p4}

El paso «Diseñar las tareas periódicas: una tarea que pasa sola a en curso según su programación» pide decidir si la SF tiene tareas periódicas en general.

Opción A
:   Tareas periódicas en la cola: una tarea con programación que pasa sola a en curso al vencer. Útil en general, pero choca con el máximo de seis en curso (453), con que un cambio de estado de la cola lo hace una sesión, y no existe hoy ningún campo de programación.

Opción B
:   Para esta revisión, un aviso del panel con la fecha de la última (pregunta 2); las tareas periódicas generales, como propuesta aparte con su diseño.

Opción C
:   Rutina programada en la nube que crea la tarea; depende de que la cola sea accesible desde la nube, que no lo es.

Recomendación
:   **B.** Resuelve este caso con poco; las tareas periódicas son un cambio grande de la cola y merecen su propia propuesta.

Decisión
:   **B**: aviso del panel para esta revisión; las tareas periódicas, como propuesta aparte (P26, «Tareas periódicas en la cola»). Decisión 391.

### 5 · Si develop puede guardarse en un repositorio privado {estado=decidida elegida=A} {: #p5}

Con repositorio público, la 252 sube develop al público. Con fast-forward de develop a main, lo que se publica en cada RELEASE son los mismos commits: la copia privada no evita que salgan, solo que salgan antes de tiempo.

Opción A
:   Como hoy: develop público, ramas feature locales (252 y 280). Se mantiene la revisión al subir.

Opción B
:   Opcional por proyecto: remoto privado de respaldo con develop y ramas de tarea; al público, solo main y tags en RELEASE.

Opción C
:   B, y además RELEASE publica en main un commit compuesto (squash) en lugar de la historia de develop. Es lo único que oculta de verdad el historial, pero rompe el fast-forward y las versiones dejan de coincidir con develop.

Recomendación
:   **A**, salvo que el propietario quiera guardar ramas y trabajo aún sin publicar fuera del equipo; entonces **B**. La ganancia es pequeña frente a la complicación que ya se rechazó en la 252. Esta pregunta reabre su concreción.

Decisión
:   **A**: sin copia privada; develop sigue en el remoto del proyecto. Decisión 392.

### 6 · Si es B, cómo se configura {estado=decidida} {: #p6}

Depende de la [pregunta 5](#p5).

Opción A
:   Un campo nuevo `respaldo` en `.sf/proyecto.json` con el remoto privado. `origin` sigue siendo el público: `cola.py subir` y el push del cierre pasan a `respaldo`, y RELEASE sube a `origin` solo main y el tag.

Opción B
:   Invertir: `remoto` pasa a ser el privado y se añade `publicacion` con el público.

Recomendación
:   **A.** No cambia el significado de `remoto` para los proyectos que no lo usen.

Decisión
:   Decae: al no haber copia privada (pregunta 5, opción A), no hay nada que configurar. Decisión 392.

:::

## Separar | Las separaciones, al día | Separar {#separar}

::: tarjetas 2

### 1 · La copia privada {: #a-copia}

Se lleva
:   Las preguntas [5](#p5) y [6](#p6).

Adónde
:   Ninguna tarea: la 5 se decidió con A y la 6 decae (decisión 392).

### 2 · Tareas periódicas en general {: #a-periodicas}

Se lleva
:   La opción A de la [pregunta 4](#p4).

Adónde
:   La propuesta «Tareas periódicas en la cola» (P26) en `sf/propuestas.md`, no una tarea, hasta que el propietario la quiera.

:::

## Tareas | Las tareas que salen | Tareas {#tareas}

| Tarea | Tipo | Qué hace |
| --- | --- | --- |
| 465 · Revisar cada 15 días los repositorios públicos y avisar en el panel de lo encontrado | programar | Ampliar `revision_publica.py` con el recorrido de repositorios y su historial, y el aviso del panel por la fecha de la última revisión; incluye, como paso, activar el escaneo de secretos de GitHub en los repositorios públicos (decisión 391) |
| Actualizar la documentación y la metodología | documental | Las que pida la 465 al aplicarse («Cómo funciona…», la metodología y las skills), cada una en su tarea y su subagente |

Sin tarea: la copia privada (decisión 392). La propuesta «Tareas periódicas en la cola» (P26) está en `sf/propuestas.md`.

