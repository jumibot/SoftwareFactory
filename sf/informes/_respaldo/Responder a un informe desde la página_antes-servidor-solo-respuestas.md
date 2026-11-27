---
antetitulo: Software Factory · Informe de diseño · Noviembre 2026
lema: Eliges en la página y pulsas Enviar; // Claude recibe tus respuestas en el chat como un mensaje tuyo.
subtitulo: Cómo puede una página de un informe mandar a la sesión de Claude Code las respuestas a sus preguntas, qué ofrece hoy el mod de la SF para hacerlo, qué diseño se recomienda y qué alternativas hay.
version: Versión 1.0 · 27/11/2026
estado: Propuesta · Tarea 475
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de diseño
pie: Informe de la tarea «Contestar las preguntas de un informe desde la página y que las respuestas lleguen a Claude» (475). Parte del código del mod de la SF (register.tsx, avisos.ts, cola.ts, lectura.ts, python.ts), de la API de mods de esta versión de Claude Code (claude-code.d.ts y reference.md de la skill plugin-authoring), del kit de documentos (herramientas.js, codigo.js) y de la especificación de Local Network Access. Espera la decisión del propietario de la Software Factory.
---
# Responder a un informe desde la página

## Resumen | Un servidor local del mod sirve el informe y recoge las respuestas | Resumen {#resumen}

Se propone que **el mod de la SF levante un servidor pequeño en el propio ordenador** (solo en `127.0.0.1`, la dirección que no sale de la máquina). Ese servidor hace dos cosas: **sirve los informes** que se abren desde la SF y **recibe las respuestas** que el propietario elige en sus fichas de preguntas. Al pulsar «Enviar», la página manda las elegidas. El mod las pasa al chat como un mensaje del propietario, con el título del informe y cada pregunta con su elección y su matiz. El principal las registra en el informe y en las decisiones, como hace hoy con las que se escriben a mano.

La API de mods no deja al mod escuchar en un puerto, pero sí lanzar un proceso hijo que vive con la sesión (`$.process.spawn`) y leer lo que escribe. Ese hijo es un script de Python, que ya es requisito de la SF. Para pasar el mensaje al chat, el mod usa lo mismo que ya usa el panel: `$.prompt.submit` como mensaje del propietario, que espera a que Claude acabe lo que está haciendo y, tras un Esc, deja el texto escrito en el prompt. Que el servidor sirva también la página evita el permiso de red local que Chrome pide a una página abierta desde el disco y le da a la página el puerto y su token sin archivos extra. Si la sesión no está abierta, las respuestas se quedan guardadas en la página y se pueden copiar para pegarlas en el chat.

Quedan **cinco preguntas** para el propietario. La más importante es si se acepta el servidor local que sirve el informe (pregunta 1). Salen dos tareas de implementar y pasos en dos tareas que ya existen.

[Ver las cinco preguntas](#por-decidir){: .salto}

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 470" width="100%" role="img" aria-label="El recorrido de una respuesta: la página del informe, servida desde 127.0.0.1, manda las elegidas al servidor local; el servidor, hijo del mod, comprueba el token y se las pasa al mod; el mod las pone en el chat como mensaje del propietario; el principal las registra en el informe y en las decisiones" style="font-family:var(--fuente-texto);display:block">
<rect x="10" y="10" width="440" height="70" rx="10" fill="none" style="stroke:var(--primario-linea)" stroke-width="1.5"/>
<text x="26" y="40" font-size="18" font-weight="700" style="fill:var(--oscuro)">La página del informe</text>
<text x="26" y="64" font-size="15" style="fill:var(--texto-suave)">eliges en cada ficha y pulsas Enviar</text>
<rect x="10" y="105" width="440" height="70" rx="10" fill="none" style="stroke:var(--primario-linea)" stroke-width="1.5"/>
<text x="26" y="135" font-size="18" font-weight="700" style="fill:var(--oscuro)">El servidor local, en 127.0.0.1</text>
<text x="26" y="159" font-size="15" style="fill:var(--texto-suave)">hijo del mod; comprueba el token del informe</text>
<rect x="10" y="200" width="440" height="70" rx="10" fill="none" style="stroke:var(--primario)" stroke-width="2.5"/>
<text x="26" y="230" font-size="18" font-weight="700" style="fill:var(--oscuro)">El mod de la SF</text>
<text x="26" y="254" font-size="15" style="fill:var(--texto-suave)">lee lo que llega y lo pasa al chat</text>
<rect x="10" y="295" width="440" height="70" rx="10" fill="none" style="stroke:var(--primario-linea)" stroke-width="1.5"/>
<text x="26" y="325" font-size="18" font-weight="700" style="fill:var(--oscuro)">El chat</text>
<text x="26" y="349" font-size="15" style="fill:var(--texto-suave)">un mensaje tuyo con el informe y cada elección</text>
<rect x="10" y="390" width="440" height="70" rx="10" fill="none" style="stroke:var(--primario-linea)" stroke-width="1.5"/>
<text x="26" y="420" font-size="18" font-weight="700" style="fill:var(--oscuro)">El principal</text>
<text x="26" y="444" font-size="15" style="fill:var(--texto-suave)">registra el informe y las decisiones</text>
<path d="M230 80 V105 M230 175 V200 M230 270 V295 M230 365 V390" style="stroke:var(--texto-suave)" stroke-width="1.5" fill="none"/>
<path d="M224 99 L230 105 L236 99 M224 194 L230 200 L236 194 M224 289 L230 295 L236 289 M224 384 L230 390 L236 384" style="stroke:var(--texto-suave)" stroke-width="1.5" fill="none"/>
<path d="M450 140 H490 V45 H456" style="stroke:var(--texto-suave)" stroke-width="1.5" stroke-dasharray="5 4" fill="none"/>
<path d="M462 39 L456 45 L462 51" style="stroke:var(--texto-suave)" stroke-width="1.5" fill="none"/>
<text x="498" y="98" font-size="13" style="fill:var(--texto-suave)">estado</text>
<text x="498" y="114" font-size="13" style="fill:var(--texto-suave)">de cada</text>
<text x="498" y="130" font-size="13" style="fill:var(--texto-suave)">ficha</text>
</svg>
</figure>

## Lo que hay hoy | Qué permite cada pieza, comprobado en el código y la documentación | Lo que hay {#lo-que-hay}

Cada vía se ha comprobado en el código del mod, en los tipos de la API de mods de esta versión de Claude Code (`claude-code.d.ts`, unas 29 700 líneas) y en su `reference.md`, o en la especificación del navegador. Lo que no se ha podido probar se dice como tal.

::: tarjetas 2 plegables

### El mod no escucha, pero lanza un hijo que sí {color=turquesa icono=codigo}

La API del mod no tiene servidor: `$.http.fetch` solo **hace** peticiones hacia fuera, y no hay nada que abra un puerto. Lo que sí hay es `$.process.spawn`, que lanza un proceso que vive con la sesión. Su documentación pone de ejemplo «un hijo para toda la sesión» que sigue tras el hook y acaba con el hijo o al descargarse el módulo. El mod lee, trozo a trozo, lo que escribe ese hijo. A ese hijo solo se le puede pasar texto por su entrada estándar **al arrancar**: después no hay forma de escribirle por ahí. Python 3.9 ya es requisito de la SF, y el mod ya lo detecta (`python.ts`); su biblioteca estándar trae el servidor HTTP.

### El mod ya sabe poner un mensaje en el chat {color=turquesa icono=dialogo}

`encargarAClaude` (`avisos.ts`) llama a `$.prompt.submit({ text, asUser: true })`, que entra como un mensaje del propietario. Si Claude está trabajando, el mensaje espera a que acabe su turno: nunca se mezcla con él. Tras un Esc, el motor no lo admite (`drop`). Entonces el mod lo deja escrito en el prompt con `$.prompt.fill` para enviarlo con Intro, y lo dice en un aviso. Lo usan ya `/sf_paso`, Activar rama y otros botones del panel.

### Una página abierta desde el disco y la red local {color=aviso icono=aviso}

Chrome pide permiso a una página que llama a una dirección local («Local Network Access», en Chrome desde la versión 141). La especificación trata, «por ahora», una página abierta desde el disco (`file://`) como de la red local. Llamar desde ella a `127.0.0.1` pediría, por tanto, el permiso «loopback-network». Es una deducción de la especificación, **sin probar** en el navegador del propietario. Una página servida desde `127.0.0.1` que llama a su propio origen no pide nada.

### La página ya guarda archivos y copia texto {color=turquesa icono=documento}

El «Guardar» de las notas del kit de documentos (`herramientas.js`) ya escribe archivos desde una página abierta del disco con `showSaveFilePicker`, y descarga el archivo en los navegadores que no lo tienen. El botón de copiar de los bloques de código (`codigo.js`) ya copia al portapapeles, con un respaldo para cuando el navegador no deja. Las dos sirven de vía de respaldo.

### Vigilar un archivo es consultar cada poco {color=info icono=lupa}

El mod no tiene un aviso de «este archivo ha cambiado». Tiene temporizadores (`$.clock.every`) y `$.fs.stat`, y su propia documentación pone de ejemplo leer un archivo cada segundo. El latido del mod ya pasa una vez por minuto, que es poco para esto: habría que consultar cada dos o tres segundos. Un hook de los ajustes de Claude Code (`UserPromptSubmit`) podría añadir el archivo de respuestas, pero solo con el siguiente mensaje del propietario.

### Otras vías del motor, más lejanas {color=info icono=rama}

El motor conoce los mensajes que llegan por un **canal** de un servidor MCP (Slack, Telegram; origen `channel`). Usarlo pide un servidor MCP en el plugin y una opción al arrancar Claude Code, que aquí no se ha probado. **Claude in Chrome** puede leer la página abierta, pero solo cuando el propietario se lo pide y con la extensión conectada. Un **Artifact** de claude.ai con base de datos recoge lo que se hace en la página, pero sube el informe a claude.ai.

:::

## El diseño recomendado | Cómo se conecta, qué protege y qué cambia | Diseño {#diseno}

### El servidor y cómo lo encuentra la página {#diseno-servidor}

- **Quién lo levanta.** El mod, solo en la sesión que tiene la SF activa en el proyecto (decisión «Una sola sesión con la SF por proyecto», 193). Lanza `tools/respuestas.py` del plugin con `$.process.spawn` y el Python detectado. Le pasa por la entrada estándar, al arrancar, la carpeta del proyecto, el puerto preferido y el secreto de la sesión. Con `/sf_forzar_inactiva` o al cerrar la sesión, el mod lo para. Con `/reload-plugins` se descarga el módulo, el hijo muere y el `session.start` siguiente lo vuelve a levantar. Cuándo se enciende es la pregunta [Cuándo está encendido el servidor (2)](#p2).
- **El puerto.** La primera vez lo elige el sistema (puerto 0) y el mod lo guarda en `$.store`, por proyecto. Las siguientes veces se pide el mismo y, si está ocupado, otro. El hijo escribe el puerto en su primera línea, y el mod lo anota en `~/.claude/sf/respuestas-<clave del proyecto>.json`, la carpeta donde ya viven las copias de `cola.py` y el progreso de la incorporación. Así lo encuentra `cola.py`. Con el puerto estable, una página abierta sigue conectada tras un `/reload-plugins` o una sesión nueva.
- **Cómo llega la página.** El que abre el documento lo abre por el servidor, `http://127.0.0.1:<puerto>/sf/informes/<informe>.html`, si el servidor responde, y desde el disco si no. Lo abren el botón Abrir del panel (tarea de la decisión «El botón Abrir de una tarea abre su documento», 396) y la orden de cada vuelta de un documento (decisión «Cada vuelta de un documento la lleva a develop una sola orden», 393). La página sabe dónde mandar porque su dirección es la del servidor, y el servidor pone el token en la página al servirla. El HTML del repositorio no cambia y no lleva ningún token.
- **Abierta desde el disco**, con doble clic o desde otra carpeta, la página no sabe el puerto: deja elegir igual y su botón es «Copiar las respuestas». Dice también cómo abrirla conectada: con Abrir, desde el panel.

### La seguridad {#diseno-seguridad}

::: columnas 2

**Solo dentro del ordenador**

- Escucha solo en `127.0.0.1`, nunca en todas las interfaces: nada de fuera de la máquina llega al puerto.
- Solo sirve archivos `.html` de `sf/` y `docs/` del proyecto, sin listados ni `..`, y una sola ruta de entrada, `POST /respuestas`.
- Sin cabeceras CORS: ninguna web de internet lee lo que contesta.

**Un token por informe y comprobaciones**

- Cada informe recibe su token, derivado del secreto de la sesión y de su ruta (HMAC). Va solo en la página servida, nunca en git; con una sesión nueva cambia.
- El servidor rechaza todo lo que no traiga el `Host` y el `Origin` del propio servidor (contra el truco de un dominio que apunta a `127.0.0.1`). También rechaza lo que no sea JSON con la cabecera del token, que obliga a una consulta previa que no se contesta.
- Limita el tamaño (64 KB, y 2000 caracteres por matiz). Comprueba que las preguntas existen y siguen abiertas en el `.md`.

:::

El texto que manda la página entra en el chat como un mensaje del propietario: lo ha escrito él. La protección está en que solo su página, servida por su sesión, sepa el token.

### Las fichas en la página {#diseno-fichas}

El generador común de documentos (`documento_a_html.py`) añade a cada pregunta abierta de `::: preguntas` lo que hace falta para contestarla. Su comportamiento vive en un script nuevo del kit, `respuestas.js`, que no sale al imprimir ni en la copia guardada:

- elegir una opción (A, B, C…) pulsando en ella, con la recomendada marcada como hoy, y un campo «Matiz» opcional;
- una barra fija «Enviar a Claude · N elegidas», solo con la página conectada; desde el disco, «Copiar las respuestas»;
- **el estado de cada ficha**, con su marca: *Abierta*, *Elegida* (guardada en el navegador, sin enviar), *Enviada* (el mod la ha recibido), *En el chat* (Claude ya la tiene o la verá al acabar lo que hace), *Escrita en tu prompt* (tras un Esc: pulsa Intro) y *Guardada aquí* (sin sesión);
- al regenerar el informe con la pregunta `estado=decidida`, la ficha sale decidida y la página olvida lo que tenía guardado para ella.

La página manda la ruta del informe, su versión y su huella (las del pie del HTML). Si no coinciden con el `.md` actual, el mensaje lo dice, para que el principal mire si la pregunta ha cambiado.

### El mensaje que llega al chat {#diseno-mensaje}

El servidor escribe una línea por envío. El mod la convierte en el mensaje, le contesta *Enviada* al servidor y llama a `encargarAClaude`. Cuando el mensaje entra en el chat, contesta *En el chat*. El servidor lo guarda y la página lo pregunta cada pocos segundos. Al hijo no se le puede escribir tras arrancar, así que el mod le contesta con `$.http.fetch` a una ruta interna con su propia clave, o con un archivo de acuse si la política de red del motor no deja llamar a `127.0.0.1`: es lo primero que hay que probar. El mensaje, con cada pregunta por su título y su número entre paréntesis (decisión «Cada pregunta al propietario se entiende sola», 397):

```text
Respuestas al informe «Responder a un informe desde la página» (tarea 475), versión 1.0, enviadas desde la página:

- Cómo encuentra la página la sesión de Claude (pregunta 1): A, la recomendada.
- Qué hace Claude al recibir las respuestas (pregunta 3): B. Matiz: «solo la primera vez».
- Sin responder: Cuándo está encendido el servidor (pregunta 2).

Regístralas en el informe (una vuelta, con sf:informe_deliberativa) y en las decisiones que salgan.
```

Si la sesión no está abierta, el envío falla. La página deja las elegidas en *Guardada aquí*, en el navegador, y lo vuelve a intentar cada diez segundos mientras está abierta. «Copiar las respuestas» copia este mismo texto, para pegarlo en el chat. Con una sesión nueva, el token anterior ya no vale: el servidor contesta «recarga la página», y al recargarla las elecciones siguen ahí, porque el navegador las guarda por dirección y el puerto no cambia.

## Alternativas | Las otras formas de hacerlo, con sus pros y sus contras | Alternativas {#alternativas}

::: tarjetas 2 plegables

### La página desde el disco llama al servidor {color=aviso icono=rama}

**Pros:** el mismo archivo sirve con doble clic; no cambia cómo se abren los documentos.

**Contras:** Chrome trataría la llamada como de la red local y pediría permiso, o la bloquearía (sin probar). La página tendría que saber el puerto y el token por un archivo junto al informe, fuera de git. Todas las páginas del disco tienen el mismo origen, «null», y el servidor no las distingue.

### Un archivo de respuestas que el mod vigila {color=aviso icono=carpeta}

**Pros:** sin red ni servidor; funciona aunque la sesión esté cerrada, porque el archivo se recoge al abrirla. El «Guardar» de las notas ya lo hace así.

**Contras:** el diálogo de guardar la primera vez, eligiendo la carpeta correcta, o el archivo en Descargas. El mod tiene que consultar cada dos o tres segundos. La página no sabe si Claude lo ha recibido.

### Solo copiar al portapapeles {color=info icono=documento}

**Pros:** trivial; el botón de copiar del kit ya existe.

**Contras:** sigue a mano: el propietario pega en el chat. Es el respaldo del diseño recomendado, no la solución.

### Un canal MCP del plugin {color=info icono=dialogo}

**Pros:** es la vía del motor para mensajes que llegan de fuera.

**Contras:** pide un servidor MCP en el plugin y arrancar Claude Code con la opción de canales, que no se ha probado aquí. Además, el servidor HTTP seguiría haciendo falta.

### Claude in Chrome lee la página {color=info icono=lupa}

**Pros:** sin servidor ni cambios en el mod.

**Contras:** necesita la extensión conectada, y el propietario tiene que avisar a Claude. Claude lee el navegador del propietario.

### Publicar el informe como Artifact {color=info icono=documento}

**Pros:** la página guarda las respuestas en su base de datos, y Claude las lee.

**Contras:** sube el informe a claude.ai, pide red y cuenta, y cambia dónde viven los informes, que hoy son archivos del repositorio.

:::

## Por decidir | Lo que tiene que elegir el propietario | Por decidir {#por-decidir}

Cinco preguntas, por importancia. La primera decide el diseño entero; las demás lo afinan.

::: preguntas 2 plegables

### Cómo encuentra la página la sesión de Claude (1) {recomendada=A} {: #p1}

Para que «Enviar» llegue a Claude, la página del informe tiene que hablar con el mod de la SF de tu sesión. El mod no puede escuchar por sí mismo; sí puede lanzar un pequeño servidor en tu ordenador.

Opción A
:   El mod levanta un servidor en `127.0.0.1` que **sirve el informe** y recoge las respuestas. Abrir y la orden de cada vuelta lo abren por él. Con doble clic, desde el disco, solo se puede copiar.

Opción B
:   El mismo servidor, pero la página se abre desde el disco, como hoy, y lo llama. Puede que Chrome pida permiso de red local cada vez, o lo bloquee; hay que probarlo.

Opción C
:   Sin servidor: la página guarda un archivo de respuestas y el mod lo recoge consultando la carpeta cada pocos segundos.

Recomendación
:   **A.** Es la única que no depende de un permiso ni de un diálogo del navegador y que dice en la página si Claude ya tiene las respuestas; además, da a la página el puerto y su token sin archivos extra.

### Cuándo está encendido el servidor (2) {recomendada=A} {: #p2}

El servidor solo hace falta mientras hay un informe con preguntas abiertas en el navegador. Encendido de más es un puerto abierto en tu ordenador sin usar, aunque solo se llegue a él desde la propia máquina.

Opción A
:   Se enciende al abrir el primer documento por la SF y sigue hasta cerrar la sesión, o hasta `/sf_forzar_inactiva`.

Opción B
:   Siempre, desde que empieza la sesión con la SF activa.

Recomendación
:   **A.** Solo está encendido cuando se usa, y una página abierta sigue conectada durante toda la sesión.

### Qué hace Claude al recibir las respuestas (3) {recomendada=A} {: #p3}

Las respuestas llegan al chat como un mensaje tuyo. Hoy, cuando contestas en el chat, Claude registra lo que dices en el informe y en las decisiones.

Opción A
:   Las registra directamente, como si las hubieras escrito: una vuelta del informe y sus decisiones. Solo te pregunta si un matiz deja algo dudoso.

Opción B
:   Te las repite en el chat y espera tu OK antes de registrar nada.

Recomendación
:   **A.** Pulsar Enviar ya es tu decisión; repetirla es el paso que la página quiere ahorrar.

### Mandar solo algunas respuestas (4) {recomendada=A} {: #p4}

Un informe puede tener muchas preguntas, y a veces sabes unas y otras no.

Opción A
:   «Enviar» manda las que has elegido. Las demás siguen abiertas en la página y en el informe, y el mensaje dice cuáles faltan.

Opción B
:   «Enviar» solo se activa con todas las preguntas abiertas elegidas.

Recomendación
:   **A.** Deja decidir por partes, que es como se trabaja hoy en el chat.

### En qué documentos se puede contestar (5) {recomendada=A} {: #p5}

Las fichas de preguntas son un recurso común del generador de documentos. Las usan los informes de las deliberativas, y pueden usarlas la visión, la definición técnica y los demás documentos con preguntas al propietario.

Opción A
:   En todos los documentos del generador que tengan preguntas abiertas.

Opción B
:   Solo en los informes de las tareas deliberativas, para empezar.

Recomendación
:   **A.** El recurso es el mismo; limitarlo costaría más que no hacerlo.

:::

## Tareas | Las tareas que salen | Tareas {#tareas}

Con la opción A en [Cómo encuentra la página la sesión de Claude (1)](#p1). Si se elige otra, cambian las dos primeras.

| Tarea | Tipo | Qué hace |
| --- | --- | --- |
| Servir los documentos y recibir sus respuestas desde un servidor local del mod | implementar | `tools/respuestas.py` y el mod: levantarlo con el puerto guardado y el secreto de la sesión, las comprobaciones de seguridad, el archivo con el puerto para `cola.py`, el mensaje al chat con `encargarAClaude` y los acuses. Primero, probar en Chrome y Edge que `$.http.fetch` llega a `127.0.0.1` y qué pasa con una página del disco. |
| Contestar las preguntas en la página: elegir, matizar, Enviar y el estado de cada ficha | implementar | El generador común y `respuestas.js` del kit: las fichas que se eligen, la barra de Enviar o Copiar, el estado de cada ficha y lo guardado en el navegador; y el texto de `sf:crear_documentos` y `sf:informe_deliberativa`. |
| Abrir el documento por el servidor cuando está encendido | paso | En la tarea del botón Abrir (decisión 396) y en la de la orden de cada vuelta (decisión 393): abrir `http://127.0.0.1:<puerto>/…` si el servidor responde y, si no, el archivo. |
| Qué hace el principal con un mensaje de respuestas | paso | En la primera tarea: la regla en `sf:orquestacion` (texto en el anexo). |
| Actualizar «Cómo funciona la Software Factory» y Actualizar «Cómo funciona el panel» | documentar | Al cerrarse la primera tarea, con el texto del anexo. |

## Anexo: texto propuesto para otros documentos | Para las tareas que los cambian | Anexo {#anexo}

**«Cómo funciona la Software Factory»**, al final de «El mod de estado»:

> El mod también recoge las respuestas a las preguntas de los documentos. Al abrir un documento desde la SF, lo sirve un pequeño servidor que el mod levanta en el propio ordenador (`127.0.0.1`, que no sale de la máquina). En sus fichas de preguntas se elige y se pulsa «Enviar», y las respuestas llegan al chat como un mensaje del propietario. Cada documento lleva su token, y sin la sesión abierta las respuestas se quedan en la página para enviarlas o copiarlas después.

**«Cómo funciona el panel»**, en «Actuar desde el panel», un apartado nuevo «Las respuestas de los documentos»:

> Abrir y la orden de cada vuelta abren el documento por el servidor local del mod si está encendido (`http://127.0.0.1:<puerto>/…`). En la página, cada pregunta abierta se contesta eligiendo una opción y, si hace falta, un matiz. «Enviar a Claude» las manda, y cada ficha dice si está elegida, enviada, en el chat o guardada en la página. El mod pone en el chat un mensaje tuyo con el título del documento y cada pregunta con su elección. Si Claude está trabajando, el mensaje espera a que acabe; tras un Esc, se queda escrito en el prompt para enviarlo con Intro. Abierto desde el disco, el documento solo permite copiar las respuestas.

**`sf:orquestacion`**, en lo que hace el principal con cada mensaje del propietario:

> Un mensaje «Respuestas al documento «…»» que llega desde la página es del propietario: se registran sus elecciones en el documento (una vuelta, con la skill de su tipo) y en las decisiones que salgan, sin volver a preguntar. Solo se pregunta un matiz dudoso, o una pregunta que ha cambiado desde la versión en que se contestó.

::: fuentes

**API de mods de Claude Code 2.1.332.** Tipos `claude-code.d.ts` y `reference.md` de la skill plugin-authoring: `$.process.spawn`, `$.http.fetch`, `$.prompt.submit`, `$.prompt.fill`, `$.clock`, `$.fs`, `$.ui.copy` y el origen `channel`. Consultado el 27/11/2026.
{: #src-E1}

**Local Network Access.** WICG, especificación, apartado «File URLs», consultado el 27/11/2026. wicg.github.io/local-network-access
{: #src-E2}

**New permission prompt for Local Network Access.** Chrome for Developers, 9 de junio de 2025, consultado el 27/11/2026. developer.chrome.com/blog/local-network-access
{: #src-E3}

:::
