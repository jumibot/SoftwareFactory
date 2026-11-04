---
name: documento_vision
user-invocable: false
description: "Crea o revisa un documento de visión — la explicación de primer nivel de un proyecto o especificación, pensada para personas que tienen que entender y decidir (un equipo, una dirección, un comité, un financiador) y no para desarrolladores, o para el propio autor como herramienta para definir su proyecto (más extensa y detallada). Úsala cuando pidan explicar, valorar o presentar un proyecto, una propuesta o una spec de alto nivel, o convertir un análisis en documento para compartir. Sigue un diálogo en fases: valorar la idea en conversación, proponer la visión y acordar las secciones, escribir, y afinar sobre el documento generado. Recoge el estilo narrativo, los gráficos escenográficos, el caso conductor, los temas visuales y la generación .md → .html. Lo propio de cada proyecto (tema, logo, componentes y reglas del dominio) está en su identidad.json."
---

# Documento de visión

Un **documento de visión** explica qué es un proyecto, para qué sirve y cómo funciona conceptualmente, antes de cualquier especificación técnica. Lo lee una persona que tiene que entender y decidir, no programar.

Esta skill no contiene nada de ningún proyecto ni de ningún dominio. Lo propio de cada proyecto está en su identidad (ver «Lo propio de cada proyecto»).

## Para quién es: para otros o para el autor

Hay dos clases de documento de visión, y lo primero es saber cuál se escribe. Si no está claro, se pregunta en la fase 2 junto con los lectores.

- **Para otros** (un comité, un centro, un equipo, un financiador): convence a alguien que no estuvo en la conversación. Manda el principio «Breve, porque así impacta más», con sus cifras orientativas.
- **Para el autor** (su propio proyecto o herramienta): es una herramienta para pensar y definir. El lector es el autor, y también Claude en sesiones futuras. Se le habla de tú. Puede ser más extenso: se incluye todo lo decidido y no se recorta para ganar impacto. Admite más detalle técnico (arquitectura, contratos, decisiones) y un caso prototípico que se afina para definir el propio proyecto.

En los dos se mantienen las demás reglas: el caso conductor, las escenas, solo la última decisión, sin tablas, lo ilustrativo marcado y las dudas en la conversación, no en el documento. Al entregar se informa de la extensión, pero en un documento para el autor no se propone recortar salvo que lo pida.

## Cómo se cuenta el caso: repartido o novela

El caso conductor se cuenta de una de dos formas, y se elige al empezar (fase 2), junto con los lectores. Claude pregunta cuál se quiere o sugiere una, con su porqué.

- **Repartido** (la forma de siempre): el caso abre el documento y avanza un capítulo breve al principio de cada sección, en el bloque «El caso». Conviene cuando lo que hay que entender es un producto, una propuesta o un argumento.
- **Novela**: el caso es además un **relato completo**, que se lee solo y de corrido, con el documento alrededor. Conviene cuando el tema se entiende mejor viviéndolo, como un cambio en la forma de trabajar. Cómo se hace, en «La opción novela».

### La opción novela

**La historia.**

- **Completa**: principio (situación, protagonista con nombre y su necesidad), trama (un conflicto real, con plazo, imprevistos y decisiones que cuestan algo) y final (desenlace y una moraleja o lo aprendido, en la voz de la historia, nunca como lista técnica).
- **El conflicto es lo que el documento propone, ausente**: al principio el protagonista actúa sin ello y lo paga (elige qué hacer sin la daily que fija el sprint, y se le va la mañana); después lo usa y cambia. La moraleja y algún guiño recogen esa diferencia.
- **Enlazada**: las partes narrativas se siguen sin las secciones explicativas (si hace falta, con transiciones breves dentro de ellas), y cada sección explicativa nace de algo que pasa en la historia.
- **Fiel al método que cuenta**: lo que pasa en la historia cumple las reglas del documento (cuándo arranca algo solo y cuándo se pide, qué entra y qué espera).

**El centro, el proyecto del documento.**

- **El caso es el vehículo**: aunque el caso sea de otro proyecto, el relato devuelve una y otra vez la atención al proyecto del documento y a lo que hace por el protagonista. Para eso están los guiños y la marca.
- **Guiños al método**: dos o tres momentos, bien repartidos, en que el protagonista reconoce sin decirlo el valor de lo que el documento propone, en su voz interior o en lo que dice: un alivio, una pequeña victoria, el contraste con lo que habría pasado sin ello («menos mal que el lunes la dejó encarrilada»). Sutiles y nacidos de la escena: nada de sermones.
- **Referencias a la marca**: sus elementos reconocibles (el logo y sus colores, la pantalla que ve el protagonista, una orden, el nombre dicho con naturalidad por un personaje), integrados con los guiños y sin sonar a anuncio; en el lector, la marca en el marco (`data-marca`).
- **Nombres sin choques**: las piezas del proyecto del caso no se llaman como las del proyecto del documento (si el documento tiene un panel, la pantalla del caso es otra cosa, un visor), y los términos del método (cola, tareas, sprint, objetivo, daily) solo nombran lo del proyecto del documento.

**Para un lector sin contexto.**

- **Lo técnico del caso se explica dentro del relato**, pronto (prólogo o capítulo 1) y sin romper el ritmo: dos o tres frases, en la voz de un personaje, que digan qué es el producto, qué es cada pieza técnica que se nombra (un gemelo digital: una simulación en el ordenador que reproduce el aparato para probar sin hardware) y por qué importa a quien lo espera. Cada término técnico que aparece después, igual: una aposición breve la primera vez. Si no basta, una aclaración breve fuera de la historia.
- **La extensión cede ante la claridad**: lo necesario para entender el caso se añade, con mesura, aunque pase del tope.

**Estilo.**

- **Frases cortas**, pensadas para la pantalla pequeña de un ebook de móvil: una idea por frase, sin subordinadas encadenadas ni incisos uno tras otro; la frase larga se parte en dos o tres.
- **Negrita en lo que toca al tema del documento**: los momentos clave de lo que se propone, los guiños y la moraleja, en fragmentos cortos, nunca párrafos, y unos pocos por capítulo como mucho, para que quien hojea capte la idea.

**Presentación.** El prólogo y el epílogo van como página de libro en un lector (`.lector`). El documento **se abre en la historia** (`data-al-abrir="historia"` en el lector del prólogo), con su pantalla de entrada, que anuncia el tema y lleva el aviso de ficción; el lector sale al terminar, con «Ver el documento», o con ×, y vuelve con «Leer la historia completa». El recurso, en sf:crear_documentos («Lector de libros»).

**Revisión de coherencia, obligatoria antes de entregar.** Se lee la historia entera, de corrido, buscando:

- [ ] **Cifras iguales** entre la historia, el documento y el anexo, y con los datos reales del proyecto del caso (la temperatura, la duración, los días).
- [ ] **Cifras que cambian con el tiempo** de la historia: lo que una semana después no puede seguir igual (el número de tareas en cola) no se repite.
- [ ] **Días y horas que cuadran**: las duraciones («cuarenta minutos», «dos días»), las referencias relativas («la semana anterior», con el día en que ocurre) y qué día y hora es cada escena.
- [ ] **Hilos cerrados**: lo aplazado dice adónde va (sale del sprint, vuelve a la cola) y lo que se da por cumplido no deja nada colgando.
- [ ] **Referentes sin ambigüedad**: quién pidió qué («una petición suya»), a qué apunta «lo» o «eso», qué es «la lista».
- [ ] **Palabras con doble lectura en el dominio del caso**: «urgencias» en un hospital, «cámara» en un aparato con cámara.
- [ ] **Quién habla** en cada escena y cada frase, y que no se mezclen lo que dice uno y lo que piensa otro.
- [ ] **Las reglas del método**: lo que pasa en la historia las cumple (la daily arranca sola al abrir; se pide con la orden; un paréntesis solo anota).
- [ ] **Nombres sin choques** entre los dos proyectos.
- [ ] **Términos técnicos** explicados la primera vez que salen.

## Lo propio de cada proyecto

Cada proyecto guarda su identidad en `doc/identidad/` o `docs/identidad/`, con un `identidad.json`. El script lo busca solo, subiendo carpetas desde el `.md`. Las rutas son relativas a esa carpeta. Claves:

- `tema`: nombre de un tema de la skill o ruta a un tema propio del proyecto (`.json`).
- `logo`: imagen de la cabecera.
- `producto`: nombre completo del producto, para la cabecera y el pie.
- `tipo`: tipo de documento, para el pie. Por defecto, «Documento de visión».
- `css`: hoja de estilos (o lista de hojas) con los componentes propios del proyecto. Puede usar las variables del tema (ver «Identidad visual y generación»).
- `reglas`: archivo Markdown con las reglas de redacción del dominio y del proyecto, y con la explicación de sus componentes.

```json
{"tema": "rojo", "logo": "emblema.png", "producto": "Producto · Organización", "css": "componentes.css", "reglas": "reglas-vision.md"}
```

**Antes de proponer la visión, leer el `identidad.json` del proyecto y, si tiene `reglas`, leerlas enteras.** Se aplican junto con las de esta skill. Si chocan, mandan las del proyecto, porque conocen su dominio. Si el proyecto no tiene identidad, se crea al definirla con el autor (ver «Logo e identidad de cada proyecto»).

## El diálogo con el autor

El documento expresa **la visión del autor**, no la de Claude, y se construye conversando, en cuatro fases que se encadenan: primero se valora la idea en conversación, después se cristaliza la visión y se acuerdan las secciones, luego se escribe y por último se afina sobre el documento ya generado. Lo que el autor da por sabido (su intención, sus prioridades, lo que descarta) es justo lo que el diálogo tiene que sacar a la luz.

### Fase 1 · Valorar la idea en conversación

Cuando el autor trae material en bruto (una propuesta pegada, una idea, una spec de otro) y dice que está valorando, **se responde en el chat, sin crear archivos ni diseñar**, hasta que pida el documento.

- **Primera respuesta: una valoración crítica honesta.** Qué está bien planteado, qué debilidades tiene (de concepto, del dominio, y lo que falta) y una recomendación breve. Si algo del material se presta a malentendido, señalarlo citando el texto.
- **El autor aporta ideas de una en una**, a menudo en mensajes muy cortos: un matiz («piensa que las reglas pueden mejorar»), una lista abierta («financiación, disponibilidad, …»), una sola palabra. Cada mensaje es una **dirección**, no una pregunta: desarrollarlo, sacar sus consecuencias, decir qué cambia de lo dicho antes y qué riesgos trae.
- **Una lista que termina en «…» es una invitación** a completarla y, sobre todo, a ordenarla: distinguir de qué tipo es cada elemento y qué papel tiene.
- **Cerrar cada respuesta con la síntesis acumulada** (una tabla de capas o una arquitectura que crece mensaje a mensaje), para que el autor vea cómo se va formando su visión.
- **Si el autor no entiende algo que se ha dicho** («no entiendo por qué dices que es determinista»), explicar de dónde salió esa lectura, con la cita, y aceptar su reencuadre sin defender la versión anterior.
- **Cuando el autor reordena prioridades** («priorizo esto; aquello, de momento, solo me sirve de apoyo»), rehacer la síntesis con el nuevo orden.
- Los reencuadres del autor son lo más valioso de esta fase: quedan como **decisiones** y no se vuelven a discutir.

### Fase 2 · Proponer la visión y acordar las secciones

Cuando el autor pide el documento, la conversación previa es la materia prima. Si no la hay, se parte del material del proyecto.

#### Arrancar con una propuesta

La conversación **no empieza con preguntas en blanco, sino con una propuesta** que el autor afina. Antes de hablar, leer lo que haya disponible (la identidad del proyecto y sus reglas, el material que aporte, la conversación previa, el código y los documentos del proyecto) y presentar un **borrador de visión** breve:

- la frase del objetivo, con su destinatario;
- el problema y la idea central, en dos o tres frases;
- qué entra y qué queda fuera;
- un caso conductor candidato, con el motivo de la elección;
- las dudas que el material no resuelve, formuladas como preguntas concretas.

Después, preguntar qué cambiaría. Lo que el autor corrija marca el rumbo de las preguntas siguientes. Si el material es tan escaso que no permite proponer nada sensato, decirlo y hacer primero las dos o tres preguntas imprescindibles.

#### Cómo preguntar

- **Pocas preguntas cada vez**, de una a tres, sobre un mismo tema. Una entrevista, no un formulario.
- **Empezar por lo grande** (para qué y para quién) y bajar después al detalle (cómo, con qué caso, con qué límites).
- **Con opciones cuando hay alternativas claras** (herramienta de preguntas con opciones, la recomendada primero); **en abierto** cuando lo que se busca es su visión con sus palabras.
- **Proponer para ayudar a pensar**: «¿lo ves más como A o como B?», o un borrador de frase para que lo corrija. Una propuesta concreta se corrige mejor que una pregunta abstracta.
- **Devolver lo entendido** cada pocas respuestas, en dos o tres frases, para que el autor confirme o corrija antes de seguir.
- **No preguntar lo que se puede averiguar**: si la respuesta está en el código, en los documentos o en los casos del proyecto, leerla y confirmar, no preguntarla.
- Si el autor contesta con una idea nueva o una corrección, **hacer la pregunta siguiente sobre esa idea** antes de volver al guion. Sus giros suelen ser lo más valioso.

#### Qué averiguar

1. **Objetivo y destinatario.** ¿Qué tiene que conseguir el proyecto y quién recibe el resultado? Sirve para la frase de apertura.
2. **El problema real.** ¿Qué pasa hoy sin el proyecto? ¿Dónde duele?
3. **La idea central.** ¿Qué lo hace distinto? ¿Cuál es la intuición que el autor quiere transmitir?
4. **Qué hace y qué no hace.** Alcance actual frente a futuro; lo que se deja fuera a propósito y por qué.
5. **Prioridades.** Qué parte importa más ahora y cuál es secundaria o de apoyo.
6. **Decisiones ya tomadas.** Lo que no está en discusión y no hay que volver a plantear.
7. **El caso conductor.** Qué caso real ilustra mejor el proyecto (proponer candidatos del conjunto de referencia si existe).
8. **Lectores.** Quién lo va a leer, qué saben ya y qué decisión tienen que tomar con él. Sobre todo, si es un documento **para otros o para el autor** (ver «Para quién es»), porque cambia la extensión y el detalle.
9. **Cómo se cuenta el caso**: repartido o novela (ver «Cómo se cuenta el caso»), con la sugerencia y su porqué.
10. **Dudas abiertas.** Lo que el autor aún no tiene claro: se habla en la conversación y no se inventa, pero no se convierte en contenido del documento.

#### Acordar las secciones

Cuando el autor da por buena la frase del objetivo y están claros el destinatario, la idea central, el alcance y el caso conductor:

1. **Resumir la visión en cinco o seis frases** y pedir confirmación.
2. **Proponer el índice de secciones**, siempre empezando por la apertura con el caso y el resumen operativo. Para cada sección, indicar:
   - el título, sin iconos ni números;
   - una línea con lo que cuenta y por qué está ahí;
   - qué aporta el caso conductor en esa sección;
   - el gráfico previsto, si lo hay, y si será una escena o un diagrama.
3. **Dejar que el autor lo afine**: añadir, quitar, fusionar, reordenar o renombrar secciones, o cambiar el foco de alguna. Repetir hasta que diga que está bien.
4. **Preguntar el destino y las herramientas**, si no están anotados en el `.md` ni en la identidad: si el `.html` es para el proyecto o para el usuario, y qué herramientas lleva (buscador, notas, «Lectura», plegado en acordeón, leyenda, edición…), con la recomendación para ese documento y destino (ver «Catálogo de herramientas y opciones de lectura»). Una sola pregunta con opciones, la recomendada primero; la elección se anota en el `.md`.

Solo con el índice aprobado se escribe el primer borrador, y se respeta ese índice. Si al escribir hace falta una sección nueva o sobra una acordada, se pregunta antes de cambiarlo.

### Fase 3 · Escribir y entregar

Escribir siguiendo el índice acordado, los principios de este documento y las reglas del proyecto. El primer borrador ya lleva los gráficos del índice y el detalle plegado: la norma «Desde la primera versión» de `crear_documentos`, con las formas de la visión (escenas, diagramas, el caso, fichas y bloques plegables) y sin tablas. Generar el `.html`, revisarlo visualmente y entregar con un resumen breve: qué se ha hecho, qué es ilustrativo o inventado, qué conviene que valide un experto y, como mucho, **una** propuesta de siguiente paso en una línea.

### Fase 4 · Afinar sobre el documento

El autor revisa el documento generado y señala fragmentos, a menudo con una captura y un comentario corto. **El comentario expresa una intención** que hay que leer:

- «poco sugerente» → hacerlo concreto y evocador, con el caso conductor;
- «esto es lo mismo» → fusionar lo que está duplicado;
- «el contenido no casa con el título» → reorganizar el contenido o renombrar;
- «acotar» → quedarse con la idea central y quitar los detalles operativos;
- «esto no» → quitarlo y comprobar que nada más dependa de ello;
- «ilustra escenas», «en vertical son más responsivos» → es una regla de estilo: aplicarla a ese elemento y a los equivalentes, o al menos ofrecerlo.

Pautas para el ciclo de ajustes:

- **Una corrección puntual puede expresar una preferencia general** (sin historia, sin viñetas, sin iconos, casos reales). Aplicarla a todo el documento, no solo al fragmento señalado, y anotarla como principio (ver «La skill aprende de cada documento»).
- **Si el motivo no es evidente, preguntar** qué buscaba antes de rehacer. Si la corrección contradice algo ya escrito, señalarlo y preguntar qué prevalece.
- **Los mensajes que llegan a mitad del trabajo se incorporan** en la misma pasada, avisando en una línea de cómo se ha hecho.
- **Si el autor interrumpe o rechaza una acción**, detenerse y no repetirla. Comprobar si llegó a aplicarse en parte y contarlo.
- **Palabras ambiguas o erratas**: aplicar la lectura más plausible y decirlo.
- **Cada pasada:** aplicar, regenerar, verificar visualmente e informar en pocas líneas de qué ha cambiado y qué queda pendiente.
- Las propuestas nuevas (una sección, un gráfico) se ofrecen en una línea y se espera el sí.

### La skill aprende de cada documento

Mientras se trabaja un documento de visión, **cada corrección del autor es también una lección**. En cada pasada de la fase 4:

1. Preguntarse si la corrección es particular (este texto, este gráfico), propia del dominio o del proyecto, o general (cómo debe ser cualquier documento de visión o cómo debe ser el diálogo).
2. Si es general, **añadirla a esta skill en la misma pasada**, en la sección que corresponda: principios de contenido, reglas aprendidas, gráficos, identidad o diálogo. Redactarla como regla para el primer borrador, no como anécdota, y sin nombres ni datos de ningún proyecto.
3. Si es propia del dominio o del proyecto (su vocabulario, sus fuentes, sus componentes), **añadirla a las `reglas` de su identidad**, no a la skill. Si el proyecto no tiene archivo de reglas, se crea y se enlaza en `identidad.json`.
4. Si contradice una regla existente, sustituirla: la skill y las reglas reflejan también solo la última decisión.
5. Avisar al autor en una línea de qué se ha añadido y dónde.

Esto se hace **siempre y sin que el autor tenga que recordarlo**: toda respuesta de la fase 4 termina con una línea «Añadido a la skill: …», «Añadido a las reglas del proyecto: …» o «Nada nuevo: es contenido de este documento». Si el autor tiene que pedirlo, es que no se ha hecho bien.

## Documentos explicativos

La misma skill genera los documentos que explican cómo funciona algo («Cómo funciona…», «Mejora continua…»). No son de visión: no tienen caso conductor ni escenas. Se escriben así:

- **Explicación con continuidad.** Pocos párrafos en secuencia, cada uno lleva al siguiente. No es un manual de referencia (listas largas de dónde va cada cosa) ni una historia contada como caso.
- **Frases cortas**, de unas 20 palabras o menos; una idea por frase.
- **Una negrita por párrafo como mucho**, dentro de la frase: el concepto que hace avanzar la secuencia. Elegirla bien; si un párrafo pide dos, casi siempre son dos párrafos o una sobra. Más de una, solo en casos excepcionales. Si el apartado explica un diagrama, las negritas son justo los conceptos que nombra el diagrama, en su orden, para que texto y gráfico se crucen.
- **El primer apartado da la visión de conjunto** (lectura por capas: lo más importante primero), con un diagrama del ciclo o del recorrido; los demás lo detallan y el detalle remite a la fuente (la metodología, una sección).
- **Ejemplos reales en tarjetas** (`.ficha`), sacados del propio proyecto, no inventados.
- **Un ejemplo que cuenta un recorrido** (cómo pasó algo de verdad, paso a paso) va narrado en prosa, en un recuadro gris: `<div class="ejemplo"><p>…</p></div>`. No se muestra el texto fuente (Markdown) de un archivo como ejemplo.
- **Sin paja:** nada sobre el propio documento («Hay que actualizar este documento…», «Este documento no contiene…») ni obviedades.
- **Sin historia:** solo el estado actual.

## Principios de contenido

0. **Breve, porque así impacta más** (en los documentos para otros; en los que son para el autor, ver «Para quién es»). Un documento de visión es un discurso de ascensor ampliado, no un catálogo exhaustivo de nada. Busca cuatro cosas: **impactar** (el lector siente el problema en la primera página), **iluminar** (entiende la idea central sin esfuerzo), **involucrar** (se ve dentro de la historia y de la decisión) y **transmitir** (puede contarlo después en pocas frases). Tiene que estar todo lo fundamental, y nada más. Ante cada sección, cada párrafo y cada anexo hay que preguntarse si ayuda a una de esas cuatro cosas: si no ayuda, se quita, no se pliega. Cuando el autor pide añadir algo, se añade en su forma más corta y se busca qué sobra a cambio. Los catálogos, los listados de fuentes, de productos o de reglas, se quedan en lo que sostiene un argumento del documento. Lo demás va a la conversación, o a otro documento si el autor lo pide. Si dudas entre más completo y más breve, elige más breve. **Cifras orientativas:** cuerpo (sin anexos ni el entregable mostrado tal cual) de unas 2.500-3.000 palabras, unos 12-14 minutos de lectura; prólogo de unas 180; resumen operativo de unas 150; cada sección de unas 200, capítulo del caso incluido; capítulos de tres o cuatro frases. Los datos de contexto (lugar, cifras de la organización) van al anexo, no al prólogo. Medir con un script las palabras por sección (sin el código de los SVG) en cada pasada e informar al autor de la extensión.
1. **Solo la última decisión.** El documento refleja el estado actual, sin historial («planteamiento original», «revisado», «antes pensábamos»). Quien lo lee no necesita la historia.
2. **Abre con el caso, sin bloque de objetivo.** El documento empieza, antes de cualquier sección, con un párrafo gancho: el caso conductor en pocas líneas, que termina en la pregunta clave («¿qué conviene proponer en este caso, y con qué razones?»). Así se presenta desde la primera línea la historia que servirá de hilo conductor. No lleva cita de objetivo: la frase del objetivo («El objetivo de X es que [quién] reciba [qué], [cómo], [con qué garantías]») se acuerda en la conversación y guía la escritura, pero en el documento se cuenta en prosa en el resumen operativo, que responde a la pregunta del gancho y nombra al destinatario real.
3. **Resumen operativo corto y narrativo.** Su tarea es crear expectativa, no explicarlo todo: si cansa, el lector no sigue. Unos tres párrafos breves y uno o dos gráficos, en prosa y **sin viñetas**, que arrancan de la pregunta del gancho: qué hace el sistema para responderla, qué recibe el destinatario (el gráfico que despierta el interés) y una frase de paso hacia el resto. El detalle (reglas, arquitectura, ciclos) va en su sección, con su gráfico. **Cada gráfico tiene que aportar algo que no esté ya en el texto ni en otro gráfico**: un «antes y ahora» por personaje que repite el prólogo no aporta, y se quita. Ante cada gráfico, preguntarse qué entendería de menos el lector sin él; si la respuesta cabe en una frase, se escribe esa frase y se quita el gráfico.
3b. **Lectura por capas, lo más importante primero.** Quien lee solo la primera capa se lleva lo esencial; cada capa siguiente profundiza. El orden es de importancia, no el de cómo se llegó a las conclusiones: el documento empieza por lo que más importa al lector, cada sección abre con su idea central en la primera frase, y el detalle técnico y las fuentes van en un segundo nivel, como subapartados `####`, que el generador pliega. Los anexos, al final. El recorrido esencial (todas las secciones salvo los anexos) debe entenderse sin desplegar nada.
4. **Todo el cuerpo en prosa ligera, sin tablas.** Las viñetas solo cuando enumeran elementos realmente paralelos y breves; nunca como sustituto del razonamiento. **Nada de tablas ni rejillas**, tampoco en los anexos: cuesta leerlas y casi nunca sostienen el argumento. Lo que iría en una tabla pasa a una lista breve, de una línea por elemento, o a una frase. El respaldo de una afirmación (estudio, norma, producto) no es una columna ni un párrafo: basta un enlace en la propia frase. **Párrafos ligeros**: una idea por párrafo, dos o tres frases, sin «tochos». La evidencia se cuenta en una frase con su enlace; los autores, años y métodos se quedan en la fuente.
4b. **El documento respeta las sensibilidades del tema.** El dominio del proyecto marca cómo debe escribirse el propio documento. Antes de escribir, preguntarse qué exige el tema y aplicarlo a todo el texto: si el proyecto defiende la legibilidad, el documento se lee con facilidad; si trata de personas en situación vulnerable, el lenguaje se centra en la persona y su papel es visible. Un documento que contradice lo que defiende pierde la credibilidad. Las pautas concretas del dominio están en las reglas del proyecto. En todo caso, frases de unas 20 palabras o menos y siglas explicadas la primera vez; medir las frases largas con un script antes de entregar.
5. **Un caso conductor real.** Elegir un caso del conjunto de referencia del proyecto, si lo tiene (las reglas del proyecto dicen dónde está), y usarlo **en todo el documento**: texto, ejemplos y gráficos. El debate es sobre ese caso concreto, no una comparación genérica de bondades. Datos reales y coherentes entre sí. Si el proyecto aún no tiene conjunto de referencia, se acuerda con el autor un **caso ficticio** coherente, contrastado con fuentes, y el anexo declara qué es ficticio y qué está respaldado. El caso se presenta **completo en un anexo al final** (sus datos, todas las opciones con su respaldo y dónde queda cada una, qué se debate, qué es ilustrativo o añadido, y la ruta de la fuente). El resumen y el cuerpo solo usan los datos que necesitan y remiten al anexo.
6. **Honestidad con los datos.** Marcar lo ilustrativo como tal («ilustrativo, no es una recomendación»). No se inventan datos para la historia (una preferencia de una persona, un resultado): lo que el caso no trae se convierte en la pregunta que hay que hacer. Lo hipotético que sea imprescindible (un plazo orientativo, un parámetro de ejemplo) se marca en el momento en que aparece y se declara al entregar. **Toda cifra o afirmación de evidencia se contrasta con fuentes antes de escribirla** (búsqueda en la web o documentos del proyecto), nunca de memoria, y las fuentes se dan al autor al entregar.
6b. **Rigor máximo con el proyecto y con su dominio.** Antes de afirmar algo sobre el proyecto, contrastarlo con su propia documentación y sus datos: el estado real frente a la meta (no dar por hecho lo que aún es objetivo), las opciones y su respaldo, y la fuente exacta que se cita. Antes de afirmar algo del dominio, buscar la evidencia y comprobar que dice lo que se le atribuye, también cuando las fuentes se contradicen. Los resultados esperados y las predicciones se dan siempre con su evidencia (el estudio, la publicación y, si existe, el subgrupo parecido al caso); sin evidencia citada, no entran. Nada se escribe de memoria. Las fuentes obligatorias del dominio están en las reglas del proyecto.
7. **Propuestas, no imposiciones.** Lo que el sistema entrega al destinatario se presenta como una propuesta razonada que él valora en cada caso («propuesta 1 · a valorar»), nunca como una indicación cerrada. Evitar «posición», «se impone» o «debe»; preferir «propone», «a valorar», «decide quien corresponde».
8. **Para elegir entre opciones: resultado esperado, y después pros y contras.** Cada opción empieza por lo que cabe esperar de ella, con las cifras de su estudio o fuente de referencia y su nombre, que es la referencia común para comparar. Después vienen los pros y contras *para este caso*, cada uno con su dato y su fuente. Aclarar en el pie que son resultados de estudio, no una predicción individual.
9. **Alcance disciplinado.** Si piden «acotar», presentar solo la idea y dejar los detalles operativos fuera. No añadir secciones ni propuestas no pedidas: ofrecerlas en una línea al final.
10. **Cabeceras limpias.** Sin iconos ni numeración. El título debe corresponder exactamente con el contenido; si no casa, reorganizar el contenido o renombrar. Sin referencias «§N»: citar los apartados por su nombre.
11. **Sin duplicar entidades.** Si dos cajas representan lo mismo (por ejemplo, un informe y el sistema que lo produce, cuando el lector solo ve el informe), son una sola.

### Reglas aprendidas de las revisiones

Estas reglas salieron de correcciones de autores sobre documentos anteriores. Tienen que cumplirse **en el primer borrador**, sin esperar a que nadie las pida:

- **Argumentar a favor, no rebatirse.** Un documento de visión busca buenos argumentos. No se detiene en las dudas que tiene cualquier proyecto que aún no ha empezado (validación pendiente, cifras por confirmar, decisiones futuras) ni se contradice a sí mismo. Los límites se cuentan como fortalezas del diseño y los avisos de honestidad («ilustrativo, no es una recomendación») van breves, en pies de figura y en el anexo. Las dudas reales del autor se tratan en la conversación, no en el documento.
- **Concreto y sugerente, nunca abstracto.** Cada texto y cada gráfico cuenta algo del caso conductor, con sus datos reales. Si un elemento podría servir para cualquier proyecto, está poco trabajado.
- **Nada duplicado.** Cada entidad aparece una sola vez, con un solo nombre. Si dos cajas o dos párrafos cuentan lo mismo, se fusionan.
- **Cada sección cuenta lo que dice su título**, y nada más. Lo que no encaja se mueve a la sección que le corresponde.
- **Cada sección se queda en su idea central.** Los detalles operativos (procedimientos, casuística, cuestiones abiertas de diseño) no entran salvo que el autor los pida.
- **Secciones breves y con anécdotas que impliquen al lector.** Cada sección cuenta su idea en pocos párrafos y la ancla con algo reconocible: una escena (imaginada, y siempre en el bloque teatral `<div class="escena">` con sus ponentes, nunca como prosa con un «escena imaginada» entre paréntesis), una situación cotidiana del oficio, un dato curioso y real, una **noticia real y reciente que venga a cuento** (buscarla en la web y dar las fuentes al autor) o una comparación sencilla. Si la noticia se parece al proyecto, aprovecharla para marcar en qué se diferencia. Si una sección se alarga, se recorta antes de añadir más.
- **En los mapas de actores u opciones, cada elemento con su valor diferencial.** No basta con nombrar (un proveedor, una herramienta, una opción): cada uno lleva una frase corta con lo que aporta y lo distingue de los demás.
- **Los gráficos del resumen se entienden en segundos.** Pocas palabras por elemento (una frase corta por fila), jerarquía visual clara y nada de listas de pros y contras ni citas: ese detalle va al cuerpo, con su propio gráfico.
- **El debate se ilustra con argumentos, no con votos.** Lo que dicen los participantes en textos y gráficos son razonamientos breves y realistas, apoyados en datos del caso, nunca «sí», «no» o letras sueltas.
- **Escenas para las dinámicas y verticales para todo lo demás.** Lo que pasa entre personas o agentes se ilustra como una escena; los procesos y las comparaciones, como gráficos verticales. Una regla de estilo se aplica a todos los gráficos equivalentes, no solo al primero, y se vuelve a comprobar en cada pasada.
- **Secciones que responden a la pregunta que deja la anterior.** Los títulos del cuerpo son las preguntas naturales del lector, en orden («Quién interviene», «Qué ocurre cuando alguien discrepa», «Qué recibe quien decide»). El documento cierra **volviendo al caso inicial**: qué aporta ahora el sistema, qué se ha acordado y qué sigue necesitando una decisión humana, sin inventar la decisión ni el desenlace.
- **El caso se revela cuando hace falta.** El resumen da solo lo imprescindible para plantear el dilema. Cada dato del expediente aparece en la sección que lo necesita, en una línea «El caso · del expediente», y el expediente completo queda en el anexo, sin repetirlo.
- **Cada sección abre con un capítulo de la historia del caso.** El documento se lee como una historia con prólogo (el gancho), capítulos y epílogo (el cierre «De vuelta al caso»). Cada sección del cuerpo empieza con un capítulo breve, de tres a cinco frases, en el bloque del caso (`El caso · capítulo N · título`): hace avanzar la historia (qué le pasa ahora al caso dentro del sistema), plantea la pregunta que la sección responde y termina con algo que invite a seguir leyendo. El capítulo ejemplifica y justifica el contenido de la sección; las escenas y la explicación vienen después. La historia avanza con el propio proceso, nunca con datos, preferencias ni desenlaces inventados; sus días y horas se declaran ilustrativos en el anexo.
- **La historia la protagonizan personas y muestra cómo les mejora la vida.** Cuando el caso es ficticio, tiene protagonistas con nombre (quien recibe el resultado y quien trabaja con el producto), y cada capítulo enseña el antes y el después: qué le preocupaba o le costaba a cada uno y qué cambia con el producto. El resumen incluye un gráfico «lo que cambia» para cada protagonista. La mejora se cuenta en su experiencia (tranquilidad, tiempo, información para decidir), nunca con desenlaces inventados.
- **Cada funcionalidad, vista en acción dentro de la historia.** Las bondades y el funcionamiento del producto no se enuncian solo en la explicación: cada uno aparece en un momento concreto de la historia (una frase de una escena, un episodio pequeño y recurrente, un detalle del cierre) que muestra cómo funciona y qué resuelve. Cuando el autor añade una funcionalidad, se le busca su momento en la historia además de su línea en los requisitos.
- **Una entidad, un solo nombre, y nada se duplica al incorporar novedades.** Antes de añadir lo que aporta el autor, buscar si ya está en el texto con otro nombre. Si lo está, se unifica con el nombre del autor, no se crea una entidad nueva. Si una palabra del autor admite dos lecturas, se elige la que ya encaja con el documento y se confirma con él en una línea.
- **El caso conductor usa el sistema; no forma parte de él.** Si el proyecto es una herramienta, una plataforma o un método, el caso es alguien o algo que se sirve de él (un usuario, un proyecto que lo adopta), nunca una de sus propias piezas: contar la historia con un componente que a la vez es protagonista y parte implicada resulta recursivo y confunde. Si existe un piloto previsto o un proyecto real en su fase inicial, es el mejor candidato.
- **El caso, en el mundo del lector.** Si el documento es para una organización concreta, el caso conductor ocurre dentro de ella y con un material real de su día a día; el anexo declara qué es real y qué es imaginado (ver «Cuando es posible, los personajes no se inventan»). Cuando el autor cambia el caso, se rehace todo el hilo (prólogo, capítulos, escenas, gráficos y anexo) y se guarda la versión anterior en `_respaldo/`.
- **La organización destinataria, con sus datos reales.** Si el documento va a una organización concreta, se investiga en la web su perfil real: a quién atiende, qué herramientas usa ya, de dónde viene su gente y en qué momento institucional está (un traslado, una fusión, un cambio de plan). El protagonista alude a esos datos en el prólogo y en los capítulos, y el anexo del caso añade una subsección «La organización real» con cada dato y su fuente. Solo se usa lo publicado; si una fuente es de un proveedor o interesada, se dice. Ningún dato describe a personas concretas.
- **Cuando es posible, los personajes no se inventan.** Quien decide en la organización (dirección, jefaturas, gerencia) aparece en la historia con su nombre real, porque es quien lee el documento y quien tiene que decidir. Antes de escribir, se investiga en detalle el elenco: la página del equipo directivo, los órganos de gobierno, los listados de personal y los departamentos, y los nombramientos en los boletines oficiales, comprobando que el cargo sigue vigente en la fecha del caso. Si el cargo lo ocupa una mujer, la historia lo dice así, aunque el autor haya escrito el cargo en masculino. Si la web no responde, se buscan los fragmentos en el buscador o en el navegador del usuario, y se cita de dónde sale cada nombre. A las personas reales se les dan intervenciones verosímiles y respetuosas, propias de su cargo, y el anexo declara que su papel y sus palabras en la historia son imaginados. Además, **el documento abre con un aviso de ficción** (`<div class="aviso-ficcion" role="note">`, antes del prólogo): la historia es ficticia, lo que dicen y hacen los personajes reales es una dramatización inventada que no recoge sus palabras ni opiniones, y el anexo detalla qué es real. Para el elenco, buscar también en fuentes indirectas: listados de personal en PDF, versiones archivadas de la web (Wayback Machine, consultada con `curl` a `web.archive.org/cdx` y `.../web/<fecha>id_/<url>`), calendarios y la autoría de documentos públicos. Comprobar también que el contenido del caso existe en el programa o catálogo real de la organización. Solo se inventan los personajes que no se pueden confirmar (y se le pregunta al autor si conoce al real) y los que nunca deben ser reales: menores, personas atendidas y sus familias.
- **Un conflicto con plazo engancha al lector.** Desde el prólogo, la historia tiene un conflicto realista: una objeción seria de alguien con poder de decisión (una queja, un responsable que duda, una pregunta por el coste) y un plazo (una reunión el jueves). Cada capítulo responde a una parte de la objeción con la funcionalidad de su sección, apoyándose en norma o evidencia verificada. Las objeciones de gestión («ya pagamos otra herramienta», «la organización cambia de sede») se responden en la sección del mercado. El epílogo llega al momento de la decisión, pero no la inventa: la deja en manos de los cargos, y el documento se presenta como lo que el protagonista lleva a esa reunión.
- **Compararse con lo que ya existe.** Antes del cierre, una sección «En qué se diferencia de lo que ya existe» sitúa el producto en el mercado. Se investiga en la web: productos comerciales, proyectos públicos y de investigación y, sobre todo, lo que la organización destinataria ya usa. Se agrupan por familias, cada una con lo que resuelve y lo que le falta para el caso, en un gráfico vertical que acaba en el producto, y con una noticia real de un competidor que marque la diferencia. La sección es corta: pocas familias y los productos justos para que el lector se sitúe, cada uno con su enlace en el anexo de fuentes, sin tablas exhaustivas. Solo se afirma lo verificado (en caso de duda, se describe lo que hace, no lo que le falta). Lo que la organización ya usa se presenta como complemento, no como rival, y el anexo de fuentes fecha la comparación.
- **Las reglas que aplica el producto salen de fuentes primarias.** Si el producto aplica pautas o reglas, se extraen de los documentos originales, no de resúmenes. El documento muestra solo las que se ven en el caso o sostienen un argumento, cada una con su fuente y su ejemplo; el inventario completo es material de trabajo, no del documento de visión. Cuando dos fuentes chocan, se dice, y el cuerpo puede usarlo como argumento para afinar. Si una regla nueva afecta a lo ya escrito, se corrige el ejemplo del caso.
- **Se muestra lo que recibe el usuario final, no solo la redacción.** Cuando el producto entrega algo a una persona, el documento enseña ese entregable tal como llega: con su formato, sus ayudas y una etiqueta con lo que tiene activo. Si el proyecto tiene componentes para ello, están en su CSS y sus reglas.
- **Comparar versiones: completas y una lista de cambios, nunca una rejilla por ideas.** Para mostrar varias versiones de un mismo contenido (original y variantes, antes y después), se ponen las versiones completas, tal como se entregan, una visible cada vez (en pestañas, con el original primero). Debajo van una o dos frases con las cifras que resumen el cambio y una lista `####` «Qué ha cambiado, y por qué». Una rejilla que trocea el texto por ideas y versiones, con un comentario en cada celda, confunde en lugar de aclarar.
- **Las cifras de la historia salen de un cálculo.** Cuando la historia usa números técnicos (consumos, porcentajes, tiempos), se calculan con supuestos explícitos en un anexo, y cada episodio usa exactamente esas cifras. Si el cálculo cambia, se revisan los episodios y los gráficos que lo citan.
- **Cada flujo, con su camino.** En los esquemas técnicos, todo lo que se mueve (energía, materia, datos, señal) tiene un recorrido completo, dibujado y explicado: de dónde sale, por dónde pasa y adónde llega. Antes de entregar, seguir cada flujo en el esquema y comprobar que ninguna pieza queda sin conexión y que ninguna solución choca con otra.
- **El orden importa, y es el mismo en todo el documento.** Cuando hay una escala o una secuencia (niveles, grados, fases, opciones), se fija un orden la primera vez que aparece, normalmente de menos a más, y todo lo demás lo respeta: gráficos, pestañas, listas y texto. Un orden que salta (1, 3, 2) desconcierta aunque cada pieza esté bien. Antes de entregar, se repasa que cada componente siga ese orden.
- **Al rehacer un gráfico, no se pierde nada.** Antes de redibujar o recortar etiquetas, listar las piezas que nombraba el gráfico y comprobar después que siguen todas; si alguna no cabe, se agrupa con otra en la misma etiqueta, no se elimina.
- **El hilo conductor se ve.** El caso lleva siempre la misma marca visual: la narración en cursiva dentro de un recuadro gris claro, con la etiqueta «El caso» en versalitas del color oscuro del tema (sin rayas en el margen): en el gancho de apertura, en cada dato que se revela y en el cierre «De vuelta al caso». Así el lector reconoce el hilo de un vistazo y lo distingue de la explicación y de las escenas.
- **Escenas dialogadas para ver el proceso.** En los momentos clave, una escena breve muestra la dinámica: proponer, aceptar una parte y cuestionar otra, pedir una aclaración, reconocer un error, acordar, derivar lo pendiente. Se etiqueta «Escena ilustrativa», nombra a cada ponente y lleva un pie que dice que es un diálogo imaginado, no una transcripción ni un resultado validado. Después de cada escena, un párrafo breve explica qué mecanismo se acaba de ver y por qué importa. El debate no es una competición ni un camino hacia una respuesta predeterminada: los ponentes preguntan, rectifican y se complementan. Plantilla y tipografía, en «Componentes de texto».
- **Apoyos y evidencia, siempre por separado.** Cuántos participantes sostienen una conclusión no dice cuán sólida es su evidencia: en fichas y gráficos van en campos distintos. Las disconformidades minoritarias quedan visibles. Ningún símbolo («≈», «=») sugiere equivalencia donde solo falta base para ordenar: se escribe «sin orden entre ellas».
- **Sin promesas sobre los modelos.** No se atribuye a los modelos de IA comprensión humana ni se afirma que su diversidad garantice mejores resultados («tienden a», «es menos probable que»).

## Gráficos (SVG inline en el .md)

- **Norma de la SF: todo diagrama es un SVG inline, nunca ASCII ni mermaid**, en todo documento, tenga el proyecto metodología o no (`crear_documentos`, «Esquemas»). La guía común de la SF, `../metodologia/references/diagramas-svg.md`, recoge las recomendaciones generales de esta sección para cualquier documento; si cambia una regla general aquí, se actualiza también allí. Si un borrador o un documento que se adapta trae un esquema hecho con caracteres, se redibuja en SVG con las reglas de esta sección. Los árboles de carpetas no son diagramas y siguen en un bloque de texto.
- **Un gráfico aclara una idea compleja de otra forma; nunca repite la prosa.** Solo se dibuja lo que cuesta entender en texto: un proceso que cambia en el tiempo, una estructura (un mapa de actores y el hueco que queda) o una escena entre personas. Si el gráfico vuelve a decir lo que ya dice un párrafo, sobra uno de los dos: se quita el gráfico o se recorta la prosa a una frase que lo introduce. Tampoco se repiten entre sí un gráfico y un componente (por ejemplo, un gráfico de algo que el entregable mostrado ya enseña), ni el pie repite la frase de entrada o un texto dentro del propio SVG. Los enlaces de los elementos del gráfico van en una línea debajo («Los productos del gráfico: …»). Al revisar, recorrer todos los gráficos y preguntarse qué entendería de menos el lector sin cada uno; si cabe en una frase, se escribe la frase y se quita el gráfico.
- **Escenas antes que diagramas** cuando se ilustra una dinámica: personajes (los agentes de IA como robots, las personas con algo propio de su oficio), una mesa con los datos encima, bocadillos con lo que dice cada uno sobre el caso. La mesa se dibuja **plana, sin perspectiva** (un rectángulo redondeado), y los personajes van fuera de ella, en filas encima y debajo, **sin solaparse** con la mesa ni entre sí; los bocadillos, hacia fuera. Diagramas abstractos solo para estructura (capas, flujos).
- **Todo gráfico en vertical** (`<figure class="vertical">`, `viewBox` de 560 de ancho): caben en el móvil sin desplazamiento. No solo los flujos: también los paneles o tarjetas que se comparan (se apilan), los mapas por columnas (se apilan los grupos), los gradientes (la barra corre en vertical), las líneas de tiempo (cada opción en su fila, con el eje debajo) y los ciclos por pasos (un paso por fila). Antes de entregar, revisar que ningún gráfico tenga más de 560 de ancho, tampoco las escenas con personajes.
- **Siempre con el caso conductor**: nada de «opción X / Y»; nombres reales y datos del caso.
- **Estilo ligero.** Pocos recuadros y pocos fondos de color: la información se ordena con tipografía (nombre en negrita y color, detalle en gris debajo), alineación en columnas y espacio en blanco. Los fondos y bordes se reservan para lo que de verdad hay que destacar (una barra, un estado, una marca). Las escenas con personajes son la excepción: ahí el dibujo es el contenido. Cuando hay bloques paralelos que comparar (tarjetas de opciones), un **contorno fino sin fondo** por bloque basta para que se aprecie la separación.
- **Semántica de color estable** en todo el documento: el color primario para el sistema; el acento solo para lo validado o la evidencia; ✓ en el primario y ✕ en rojo oscuro (`#991b1b`) para pros y contras; gris para lo podado o descartado (siempre visible, nunca oculto). Las reglas del proyecto pueden concretar qué significa cada color en su dominio.
- **Cifras en palabras, sin siglas que haya que descifrar.** «25 % menos tiempo de espera», no «TE −25 %». Si una sigla es inevitable, se explica en el pie.
- **Iconos con significado específico.** Todo lo que almacena información (informes, fuentes, catálogos, registros) lleva el icono de almacenamiento: un cilindro de base de datos, con el color de su tipo. Nada de iconos genéricos (hojas, libros, cajas) para repositorios.
- Tipografía del tema en cada SVG: `style="font-family:var(--fuente-texto);display:block"`. Así el gráfico cambia de letra con el tema.
- **Texto de derecha a izquierda (árabe, hebreo) en un SVG:** `direction="rtl"` con `text-anchor="start"`, que en RTL ancla el borde derecho. Con `text-anchor="end"` el texto se sale por la derecha y se corta.
- Pie de figura breve que diga qué hay que ver, en cursiva.
- Revisar en cada gráfico: texto que se sale de su caja, solapes, flechas con lógica correcta (p. ej. «no» → otra ronda, y solo al límite → residuo), coherencia con el texto.
- **Colores en el `.md`:** escribir los colores de los roles con los valores del tema `teal` o del tema `morado` (por ejemplo, `#00726b` o `#7b2cbf` para el primario). El generador los convierte en variables del tema elegido, y dentro de cada bloque toman el color del bloque. Los colores que no son de ningún rol se quedan como están.

## Componentes de texto

Tres niveles de lectura, que se distinguen por la tipografía y también por la etiqueta, el espaciado y el margen (el CSS está en `scripts/doc_to_html.py`):

1. **Narración y explicación:** la tipografía de texto del tema.
2. **Escenas dialogadas:** la tipografía de escena del tema, en redonda y nunca en cursiva en bloques largos, con fondo suave del tema, margen lateral, etiqueta en versalitas y el nombre de cada ponente en la tipografía de texto. Las líneas de un sistema o registro, que no son ponentes, llevan `class="turno sistema"` y van en gris.
3. **Datos del caso, fuentes y evidencias:** la tipografía de texto, compacta y con cifras tabulares. El hilo del caso va en `<div class="caso"><p class="caso-etiqueta">El caso · <nombre o identificador></p><p>…</p></div>` (apertura y cierre, HTML con `<strong>`, sin Markdown dentro) y en líneas `<p class="expediente"><b>El caso · del expediente</b>…</p>`; las evidencias y los estados, en fichas (`<div class="ficha">` con una lista `<dl>`; `dt class="acordado"` para el estado final y `dt class="evidencia"` para la solidez de la evidencia).

```html
<div class="escena" role="note" aria-label="Escena ilustrativa">
<p class="escena-etiqueta">Escena ilustrativa · revisión de la propuesta</p>
<p class="escena-contexto">Segunda ronda. Respuestas a la propuesta de la primera.</p>
<div class="turno"><p class="ponente">Marta<small>responde a Luis</small></p><p>Acepto la primera parte…</p></div>
<div class="turno sistema"><p class="ponente">Sistema<small>registro</small></p><p>Apoyos: cuatro de cinco. Pasa a acuerdo.</p></div>
<p class="escena-pie">Diálogo imaginado: no es una transcripción ni un resultado validado.</p>
</div>
```

Dentro de un bloque HTML no se dejan líneas en blanco: el conversor de Markdown lo cortaría.

**Página de libro y lector** (opción novela). Es un recurso común: su sintaxis, sus atributos y cómo se ve están en sf:crear_documentos («Lector de libros»). Aquí, la novela pone su prólogo y su epílogo en un `.lector`; el del prólogo lleva `data-al-abrir="historia"`, `data-marca` con los colores del proyecto del documento, `data-invitacion` que enlaza la historia con el tema y, si hace falta, `data-tema`, `data-subtitulo` y `data-aviso`.

Otros componentes de la skill: `.aviso-ficcion` (aviso de ficción al principio) y `.comparativa` (rejilla de versiones; no se usa en documentos nuevos, ver «Comparar versiones»). Los componentes propios de un proyecto (por ejemplo, el formato de lo que entrega a sus usuarios) van en el CSS de su identidad y se explican en sus reglas.

## Identidad visual y generación

- **Fuente única: el `.md`.** El `.html` se genera, nunca se edita a mano.
- Generar con `python <carpeta de la skill>/scripts/doc_to_html.py <ruta>.md`. El script, la carcasa (`scripts/carcasa.py`) y la hoja de estilos base (`assets/estilo_base.css`) son la maqueta propia de la visión. Los temas, la identidad, las herramientas y el coloreado de código son los comunes de la skill `crear_documentos` (`assets/temas/` y `scripts/tema_identidad.py` de esa skill), que tiene que estar instalada junto a esta. El script aplica:
  - bloques plegables por cada H2, cerrados salvo el primero; subsecciones (H3) abiertas; `####` plegados; botones Expandir y Contraer;
  - la **columna de herramientas** con el buscador (biblioteca `tools/kit_documentos/`, compartida con todos los documentos de `crear_documentos`; ver «Catálogo de herramientas y opciones de lectura»): desde 1400 px, anclada a la derecha, de ancho ajustable y plegable; la chincheta de la barra, a la derecha del engranaje, despega todas las herramientas como ventanas flotantes que se arrastran y se minimizan, y las vuelve a anclar; el navegador recuerda la elección en cada documento. Por debajo de 1400 px, minimizada hasta pulsar el botón «Buscar», abajo a la derecha, y se abre como panel inferior. Busca sin distinguir mayúsculas ni tildes, agrupa los resultados por bloque y abre el bloque plegado. Las **notas personales** (misma columna): se selecciona un texto y se pulsa «Anotar», o se añade una nota a la sección que se lee; cada nota lleva la cita, el comentario, el autor y la fecha. Se guardan solas en el navegador. La **barra del documento**, en la cabecera, muestra la versión (sube con cada guardado), el estado de las notas, la versión de las herramientas (`VERSION` en `herramientas.js`, que se sube al cambiarlas) y «Guardar», que crea una copia anotada (`<nombre>.notas-<autor>.html`) con las notas dentro, en el bloque JSON `#notas-documento`, y sin restos de las herramientas. Esa copia se puede pasar al autor como revisión: `python tools/kit_documentos/extraer_notas.py <copia>.html` lista las notas por sección para aplicarlas al `.md`. Nada de esto se imprime;
  - el **tema visual** (colores, tipografías y aspecto) y la identidad del proyecto (logo, producto, CSS propio);
  - ancho completo de pantalla, gráficos limitados a 1100 px (verticales a 560 px);
  - los bloques del caso, las escenas y las fichas ocupan el mismo ancho que el texto, sin un ancho máximo propio: en pantallas anchas un recuadro más estrecho que el texto se ve descolocado;
  - móvil (< 720 px): sin sangrías, gráficos desplazables con aviso solo cuando no caben, tablas convertidas en fichas.
- **Barra bajo la cabecera:** lleva el estado del documento, nunca su nombre de archivo. Si antes de la primera sección hay un párrafo de una sola línea que empieza por `**Estado…:**` (por ejemplo, `**Estado:** 27 de octubre de 2026, versión 0.7.0.`), el generador lo saca del cuerpo y lo pone en la barra. Sin esa línea no hay barra: nada de decoración sin función.
- **Tarjetas y color:** con cuatro columnas o más, una tabla pasa a tarjetas (`.ficha` en una rejilla `repeat(auto-fill,minmax(min(100%,19rem),1fr))`). Tarjetas y gráficos pueden usar los colores de la serie del tema `colorido`, cada uno con un solo significado en todo el documento, sin fondos (guía de diagramas de `sf:metodologia`).
- **Tablas sin partir palabras:** las celdas usan `word-break: normal` con `overflow-wrap: anywhere` solo para lo que no cabe (rutas, código); una tabla nunca corta una palabra a media sílaba.
- **Preguntas frecuentes:** un índice de consulta o unas FAQ (pregunta y dónde o respuesta) no van en tabla, sino en `<dl class="faq">`, con cada pregunta en `<dt>` y su respuesta en `<dd>` (el código, con `<code>`). Sin cabecera ni franjas.
- **Bloques de código coloreados:** el generador colorea la sintaxis de los bloques con lenguaje (`json`, `bash` o `powershell`, `python`, `javascript` o `typescript`, `css`, `html` o `xml`, `sql`, `yaml`), sin dependencias (`scripts/resaltar_codigo.py` de `crear_documentos`). Un bloque sin lenguaje se colorea como JSON si lo es; `text` y los árboles de carpetas quedan sin color. Por eso cada bloque de órdenes o de datos lleva su lenguaje. Los colores, con significado fijo, están en `assets/estilo_base.css` (variables `--sx-…`).
- **Opciones:** `--producto "..."`, `--tipo "..."` (pie), `--tema <nombre o ruta .json>` (`--paleta` sigue valiendo como sinónimo), `--logo <ruta>|ninguno` e `--identidad <carpeta>|ninguna`. Mandan sobre la identidad del proyecto. Sin identidad ni opciones: tema `morado`, sin producto, cabecera solo con texto y pie «Documento de visión».
- **Temas, identidad y CSS del proyecto:** los temas disponibles, cómo se crea uno o una serie de colores, las opciones de `estilo`, el logo y la identidad de cada proyecto y su CSS están en `crear_documentos` («Temas e identidad»).

## Flujo de trabajo

1. **Valorar en conversación** (fase 1), si el autor está todavía evaluando la idea: valoración crítica, desarrollo de cada aportación y síntesis acumulada, sin archivos.
2. **Leer la identidad del proyecto y sus reglas**, y **proponer un borrador de visión** para afinarlo con el autor (fase 2).
3. **Acordar el índice de secciones**: título, propósito, papel del caso y gráfico de cada una; y el destino y las herramientas del documento.
4. Escribir o editar el `.md` (respaldar antes de cambios grandes).
5. Generar el `.html` con `scripts/doc_to_html.py` de esta skill.
6. **Verificar visualmente** con un navegador sin interfaz: captura de cada figura aislada y de la página. Para emular un móvil, cargar la página en un `<iframe>` de 390 px (las ventanas sin interfaz tienen un ancho mínimo y dan falsos desbordamientos). Las capturas van a la carpeta temporal de la sesión con nombres nuevos cada vez; no se borran temporales en la misma orden que edita o genera el documento (un borrado bloqueado detiene la orden entera).
   Con todos los `<details>` abiertos, se comprueba también que `scrollWidth` sea igual al ancho de la ventana: las URL largas de los anexos son la causa típica de desbordamiento, y el script ya las parte.
7. Entregar con un resumen breve (fase 3).
8. **Afinar** con el autor sobre el documento generado (fase 4), repitiendo los pasos 4 a 7 en cada pasada.

Notas técnicas. WebFetch devuelve binario con los PDF: se guarda el archivo y se extrae el texto en local con `pypdf` (`python -I`, escribiendo a un archivo UTF-8). Los scripts de edición largos se escriben con Write y se ejecutan después, porque un heredoc muy largo en Bash puede fallar sin ejecutar nada.

## Catálogo de herramientas y opciones de lectura

El catálogo, sus valores iniciales según el destino y cómo se anota la elección están en `crear_documentos` («Herramientas y opciones de lectura»). En la visión, la elección se anota con comentarios al principio del `.md`: `<!-- destino: proyecto -->` y `<!-- herramientas: recomendadas -->`. **Cada opción es opcional: si el autor no la ha especificado, se le pregunta** (fase 2, «Acordar las secciones»).

## Lista de comprobación final

- [ ] Se han leído la identidad del proyecto y sus reglas, y el documento las cumple.
- [ ] La visión se ha confirmado con el autor antes de escribir, y el documento la refleja con sus prioridades.
- [ ] El documento sigue el índice de secciones acordado con el autor.
- [ ] El documento abre con el gancho del caso, que termina en la pregunta clave, sin bloque de objetivo; el resumen la responde y nombra al destinatario.
- [ ] Está claro si el documento es para otros o para el autor, y su extensión y su detalle corresponden a esa clase.
- [ ] Extensión medida por sección. Para otros: cuerpo de unas 2.500-3.000 palabras, prólogo de unas 180 y secciones de unas 200. Para el autor: se informa de la extensión sin recortar lo decidido. En la opción novela, la extensión cede ante la claridad.
- [ ] Si es para otros, es breve: todo lo fundamental y nada más; cada sección, lista y anexo ayuda a impactar, iluminar, involucrar o transmitir, y lo que no ayuda se ha quitado, no plegado.
- [ ] El resumen operativo es corto (unos tres párrafos y uno o dos gráficos que no repiten nada), sin viñetas, y engancha con el caso.
- [ ] No queda historia del documento («original», «revisado», «ahora»).
- [ ] El caso conductor aparece en texto y en todos los gráficos donde tenga sentido.
- [ ] Ningún gráfico usa letras genéricas; todos son legibles en móvil y tienen estilo ligero (sin recuadros ni fondos innecesarios).
- [ ] Cabeceras sin iconos ni números, y cada título casa con su contenido.
- [ ] Nada es genérico ni está duplicado; cada sección se queda en su idea central; las dinámicas son escenas y los flujos, verticales.
- [ ] Lo ilustrativo está marcado; los datos inventados se han declarado.
- [ ] El tono es afirmativo: ningún pasaje duda del proyecto ni se rebate a sí mismo.
- [ ] Cada dato del proyecto se ha contrastado con su documentación y sus ficheros, y cada dato del dominio y cada resultado esperado, con su evidencia citada.
- [ ] Cada sección tiene su anécdota o dato que engancha; los mapas dan el valor diferencial de cada elemento; los debates muestran argumentos, no votos.
- [ ] Si hay organización destinataria: sus datos reales, con fuentes; sus cargos en la historia con su nombre real, verificado y vigente; un conflicto con plazo que recorre los capítulos y un epílogo que deja la decisión a los cargos.
- [ ] Hay una sección de comparación con el mercado, que incluye lo que la organización ya usa, con enlaces y fecha.
- [ ] La comparación no es benevolente con el propio proyecto: dice en qué van por delante las alternativas (madurez, cobertura, comunidad) y cuál es el estado real del proyecto frente a ellas, y deja su diferencia en lo que de verdad lo distingue.
- [ ] Las reglas que se muestran salen de fuentes primarias y son solo las que sostienen un argumento; el entregable al usuario final se ve tal como lo recibe.
- [ ] No hay tablas ni rejillas; el respaldo va como enlace en la frase; ningún párrafo pasa de tres frases ni ninguna frase, salvo citas, de unas 20 palabras.
- [ ] El texto respeta las sensibilidades del tema, y las siglas se explican la primera vez.
- [ ] Si la historia usa una organización o personas reales, el documento abre con el aviso de ficción, y el contenido del caso existe en el programa real.
- [ ] Ningún gráfico repite la prosa, otro gráfico o un componente; cada uno aclara de otra forma una idea que en texto costaría entender.
- [ ] En la opción novela, hecha la revisión de coherencia de «La opción novela».
- [ ] Lo aprendido en las revisiones de este documento ya está en la skill (si es general) o en las reglas del proyecto (si es de su dominio).
- [ ] El destino y las herramientas los ha elegido el autor y están anotados.
- [ ] Lectura por capas: lo más importante primero, cada sección abre con su idea central y el detalle va plegado.
- [ ] El `.html` se ha regenerado desde el `.md` y se ha revisado visualmente.
