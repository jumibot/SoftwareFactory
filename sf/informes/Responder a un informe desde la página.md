---
antetitulo: Software Factory · Informe de diseño · Noviembre 2026
lema: Un servidor local para las páginas de la SF; // tus respuestas llegan al chat como un mensaje tuyo.
subtitulo: Cómo puede una página generada por la SF hablar con la sesión de Claude Code, con las respuestas de un informe como primer uso, qué ofrece hoy el mod, qué diseño se recomienda y qué protege.
version: Versión 2.2 · 27/11/2026
estado: Propuesta · Tarea 475
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de diseño
pie: Informe de la tarea «Contestar las preguntas de un informe desde la página y que las respuestas lleguen a Claude» (475). Parte del código del mod de la SF (register.tsx, avisos.ts, cola.ts, lectura.ts, python.ts), de la API de mods de esta versión de Claude Code (claude-code.d.ts y reference.md de la skill plugin-authoring), del kit de documentos (herramientas.js, codigo.js) y de la decisión «El servidor local sf_proxy escucha cualquier petición de una página generada por la SF, con un token por apertura y las peticiones numeradas» (416). Espera la decisión del propietario de la Software Factory sobre las preguntas abiertas.
---
# Responder a un informe desde la página

## Resumen | sf_proxy: un servidor local genérico, con un token por apertura y peticiones numeradas | Resumen {#resumen}

Por decisión del propietario (416), **el mod de la SF levanta en el propio ordenador un servidor genérico, `sf_proxy`**, solo en `127.0.0.1` (la dirección que no sale de la máquina). Cada `sf_proxy` vale solo para **una sesión concreta de Claude**: lo que le llega va a esa sesión y muere con ella. No recoge solo respuestas de informes: **atiende cualquier petición de una página que haya generado la SF**, para poder montar interfaces externas con él. Lo que lo protege es doble: la página la ha generado Claude y la sirve el propio servidor, **cada vez que se abre una página interactiva lleva un token nuevo**, y **cada petición va numerada**: el servidor rechaza un número repetido o anterior, así que ninguna petición vale dos veces. Sin token válido, no atiende. El propietario lo usará de momento solo en su ordenador y no pidió limitar las peticiones a tipos declarados.

**La respuesta de un informe es el primer uso.** En las fichas de preguntas se elige y se pulsa «Enviar»; la página manda una petición con las elecciones, y el mod la pone en el chat como un mensaje del propietario, con el título del informe y cada pregunta con su elección y su matiz. El principal las registra en el informe y en las decisiones, como hace hoy con las que se escriben a mano. Cualquier otra interfaz futura usa el mismo camino: su petición llega al chat, o a quien la atienda.

La API de mods no deja al mod escuchar en un puerto, pero sí lanzar un proceso hijo que vive con la sesión (`$.process.spawn`). Ese hijo es un script de Python, requisito ya de la SF. Para escribir en el chat, el mod usa lo que ya usa el panel: `$.prompt.submit` como mensaje del propietario, que espera a que Claude acabe lo que hace y, tras un Esc, deja el texto escrito en el prompt.

**Cada documento con preguntas es un front, una interfaz a su medida** (417): el servidor y el camino al chat son comunes, y cada front define cómo envía lo suyo. El propietario aceptó las cinco recomendaciones de las preguntas anteriores (417) y queda **una pregunta abierta**: cómo envía la información un front, y qué conviene a los informes deliberativos como primero ([Cómo envía un front lo que se contesta (7)](#p7)). Todo se implementa en esta misma tarea.

[Ver la pregunta abierta](#por-decidir){: .salto}

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 470" width="100%" role="img" aria-label="El recorrido de una petición: la página generada por la SF, servida desde 127.0.0.1 con su token, manda una petición numerada a sf_proxy; sf_proxy, hijo del mod y de una sola sesión, comprueba el token y el número y se la pasa al mod; el mod la pone en el chat como mensaje del propietario o la entrega a quien la atiende; el principal actúa, por ejemplo registra las respuestas en el informe y en las decisiones" style="font-family:var(--fuente-texto);display:block">
<rect x="10" y="10" width="440" height="70" rx="10" fill="none" style="stroke:var(--primario-linea)" stroke-width="1.5"/>
<text x="26" y="40" font-size="18" font-weight="700" style="fill:var(--oscuro)">La página generada por la SF</text>
<text x="26" y="64" font-size="15" style="fill:var(--texto-suave)">token por apertura; petición numerada</text>
<rect x="10" y="105" width="440" height="70" rx="10" fill="none" style="stroke:var(--primario-linea)" stroke-width="1.5"/>
<text x="26" y="135" font-size="18" font-weight="700" style="fill:var(--oscuro)">sf_proxy, en 127.0.0.1</text>
<text x="26" y="159" font-size="15" style="fill:var(--texto-suave)">de una sesión; token y número, o no atiende</text>
<rect x="10" y="200" width="440" height="70" rx="10" fill="none" style="stroke:var(--primario)" stroke-width="2.5"/>
<text x="26" y="230" font-size="18" font-weight="700" style="fill:var(--oscuro)">El mod de la SF</text>
<text x="26" y="254" font-size="15" style="fill:var(--texto-suave)">lee la petición y la encamina</text>
<rect x="10" y="295" width="440" height="70" rx="10" fill="none" style="stroke:var(--primario-linea)" stroke-width="1.5"/>
<text x="26" y="325" font-size="18" font-weight="700" style="fill:var(--oscuro)">El chat, o quien la atienda</text>
<text x="26" y="349" font-size="15" style="fill:var(--texto-suave)">un mensaje tuyo con lo que manda la página</text>
<rect x="10" y="390" width="440" height="70" rx="10" fill="none" style="stroke:var(--primario-linea)" stroke-width="1.5"/>
<text x="26" y="420" font-size="18" font-weight="700" style="fill:var(--oscuro)">El principal</text>
<text x="26" y="444" font-size="15" style="fill:var(--texto-suave)">actúa; con un informe, lo registra</text>
<path d="M230 80 V105 M230 175 V200 M230 270 V295 M230 365 V390" style="stroke:var(--texto-suave)" stroke-width="1.5" fill="none"/>
<path d="M224 99 L230 105 L236 99 M224 194 L230 200 L236 194 M224 289 L230 295 L236 289 M224 384 L230 390 L236 384" style="stroke:var(--texto-suave)" stroke-width="1.5" fill="none"/>
<path d="M450 140 H490 V45 H456" style="stroke:var(--texto-suave)" stroke-width="1.5" stroke-dasharray="5 4" fill="none"/>
<path d="M462 39 L456 45 L462 51" style="stroke:var(--texto-suave)" stroke-width="1.5" fill="none"/>
<text x="498" y="98" font-size="13" style="fill:var(--texto-suave)">acuse a</text>
<text x="498" y="114" font-size="13" style="fill:var(--texto-suave)">la página</text>
</svg>
<figcaption><em>Una petición recorre siempre el mismo camino; lo que cambia es qué es y quién la atiende.</em></figcaption>
</figure>

## Lo que hay hoy | Qué permite cada pieza, comprobado en el código y la documentación | Lo que hay {#lo-que-hay}

Cada vía se ha comprobado en el código del mod, en los tipos de la API de mods de esta versión de Claude Code (`claude-code.d.ts`, unas 29 700 líneas) y en su `reference.md`. Lo que no se ha podido probar se dice como tal.

::: tarjetas 2 plegables

### El mod no escucha, pero lanza un hijo que sí {color=turquesa icono=codigo}

La API del mod no tiene servidor: `$.http.fetch` solo **hace** peticiones hacia fuera. Lo que sí hay es `$.process.spawn`, que lanza un proceso que vive con la sesión; su documentación pone de ejemplo «un hijo para toda la sesión», que acaba con la sesión o al descargarse el módulo. El mod lee, trozo a trozo, lo que escribe ese hijo. Al hijo solo se le puede pasar texto por su entrada estándar **al arrancar**: después no hay forma de escribirle por ahí. Python 3.9 ya es requisito de la SF y el mod ya lo detecta (`python.ts`); su biblioteca estándar trae el servidor HTTP.

### El mod ya sabe poner un mensaje en el chat {color=turquesa icono=dialogo}

`encargarAClaude` (`avisos.ts`) llama a `$.prompt.submit({ text, asUser: true })`, que entra como un mensaje del propietario. Si Claude está trabajando, el mensaje espera a que acabe su turno. Tras un Esc, el motor no lo admite (`drop`): el mod lo deja escrito en el prompt con `$.prompt.fill` para enviarlo con Intro, y lo dice en un aviso. Lo usan ya `/sf_paso`, Activar rama y otros botones del panel.

### Una página abierta desde el disco y la red local {color=aviso icono=aviso}

Chrome pide permiso a una página que llama a una dirección local («Local Network Access», desde la versión 141). La especificación trata, «por ahora», una página abierta desde el disco (`file://`) como de la red local, así que llamar desde ella a `127.0.0.1` pediría el permiso «loopback-network». Es una deducción, **sin probar** en el navegador del propietario. Una página servida desde `127.0.0.1` que llama a su propio origen no pide nada: por eso el servidor sirve las páginas.

### La página ya guarda archivos y copia texto {color=turquesa icono=documento}

El «Guardar» de las notas del kit de documentos (`herramientas.js`) ya escribe archivos desde una página abierta del disco, y el botón de copiar de los bloques de código (`codigo.js`) ya copia al portapapeles. Las dos sirven de vía de respaldo cuando no hay servidor.

### Vigilar un archivo es consultar cada poco {color=info icono=lupa}

El mod no tiene un aviso de «este archivo ha cambiado»: tiene temporizadores (`$.clock.every`) y `$.fs.stat`. El latido del mod pasa una vez por minuto, poco para esto. Con el servidor como hijo que escribe una línea por petición, el mod no necesita consultar nada.

### Otras vías del motor, más lejanas {color=info icono=rama}

El motor conoce los mensajes que llegan por un **canal** de un servidor MCP (origen `channel`); usarlo pide un servidor MCP en el plugin y una opción al arrancar Claude Code, sin probar aquí. **Claude in Chrome** puede leer la página, pero solo cuando se lo pides. Un **Artifact** de claude.ai con base de datos recoge lo que se hace en la página, pero sube el informe a claude.ai.

:::

## El diseño recomendado | Cómo se conecta, qué protege y qué cambia | Diseño {#diseno}

### El servidor genérico y la página que lo usa {#diseno-servidor}

- **Quién lo levanta, y para quién.** El mod, solo en la sesión que tiene la SF activa en el proyecto (decisión «Una sola sesión con la SF por proyecto», 193). Cada `sf_proxy` es de **una sesión concreta**: lo que le llega va a esa sesión, nunca a otra, y muere con ella (no sobrevive a `/clear` de la sesión ni a su cierre). Lanza `tools/sf_proxy.py` del plugin con `$.process.spawn` y el Python detectado, y le pasa por la entrada estándar, al arrancar, la carpeta del proyecto, el puerto preferido y el secreto de la sesión. Con `/sf_forzar_inactiva` o al cerrar la sesión, el mod lo para; con `/reload-plugins` muere el hijo y el siguiente arranque lo levanta de nuevo. Cuándo se enciende es la pregunta [Cuándo está encendido el servidor (2)](#p2).
- **El puerto.** La primera vez lo elige el sistema y el mod lo guarda por proyecto en `$.store`; las siguientes veces se pide el mismo y, si está ocupado, otro. El hijo escribe el puerto en su primera línea.
- **La página es de la SF.** Una página interactiva la genera Claude con el generador de documentos (o con una skill que lo haga) y solo se abre por la SF: Abrir en el panel o la orden de cada vuelta de un documento (decisiones «El botón Abrir de una tarea abre su documento», 396, y «Cada vuelta de un documento la lleva a develop una sola orden», 393). Al abrirla, la orden pide al servidor que la **registre**, y el servidor solo sirve páginas registradas: una web cualquiera, o un archivo que no abrió la SF, no es una página suya.
- **El token, nuevo en cada apertura.** Al registrar la página, el servidor genera un token aleatorio (nuevo cada vez, no derivado del anterior) y abre `http://127.0.0.1:<puerto>/<ruta>?t=<token>`. Al servirla, pone el token dentro de la página (`window.SF`). El HTML del repositorio no cambia ni lleva ningún token. Abrir de nuevo la página da otro token y deja de valer el anterior de esa página; con una sesión nueva, valen solo los nuevos.
- **Cada petición, numerada.** La página lleva un contador y manda un número creciente en cada petición; `sf_proxy` guarda el último aceptado por página y rechaza un número repetido o anterior. Así una petición copiada o repetida no vale dos veces. Se descartó renovar el token en cada llamada: en local aporta poco (quien roba el token ya lee la página) y es frágil, porque la página consulta cada pocos segundos y con dos pestañas o una respuesta perdida quedaría bloqueada.
- **Cualquier petición.** `sf_proxy` atiende cualquier petición de una página con token válido y número nuevo (ruta, método y cuerpo libres, hasta el tamaño máximo). No hay lista de tipos declarados: así se pueden montar interfaces nuevas sin tocar el servidor. Lo que la petición **hace** lo decide quien la atiende (ver más abajo).
- **Abierta desde el disco**, con doble clic o desde otra carpeta, la página no tiene puerto ni token: no es una página abierta por la SF. Las fichas de preguntas se pueden elegir igual y su botón es «Copiar las respuestas»; la página dice cómo abrirla conectada: con Abrir, desde el panel.

### La seguridad, ajustada a esto {#diseno-seguridad}

La decisión (416) fija la protección: página generada por la SF y token nuevo en cada apertura, para uso local. Se mantiene el resto de lo barato, sin limitar tipos de petición, porque no cuesta nada ni quita lo genérico.

::: columnas 2

**Lo que decide 416**

- Escucha solo en `127.0.0.1`, nunca en todas las interfaces: nada de fuera de la máquina llega al puerto.
- Solo sirve páginas registradas por la SF al abrirlas; sin token válido, no atiende ninguna petición.
- El token es aleatorio, nuevo en cada apertura (invalida el anterior de esa página) y solo vive mientras dura la sesión; no se guarda en git.
- Cada petición va numerada y se rechaza un número repetido o anterior.
- Cada `sf_proxy` es de una sola sesión: lo que le llega va a ella y muere con ella.
- No hay lista de tipos de petición: el servidor las atiende todas.

|||

**Lo que se añade sin limitar tipos**

- Sin cabeceras CORS: ninguna web de internet lee lo que contesta.
- Rechaza lo que no traiga el `Host` y el `Origin` del propio servidor, contra el truco de un dominio que apunta a `127.0.0.1` («rebinding»).
- Limita el tamaño de la petición (64 KB) y su ritmo, para que una página con un fallo no llene el chat.
- Guarda un registro de lo recibido, que se puede mirar si algo raro llega.

:::

**El límite que se acepta.** Con peticiones libres, cualquier página abierta por la SF, y quien tenga su token mientras dura, puede poner un texto en el chat como mensaje del propietario. Si un día se abre a otras personas o a otros equipos, habría que declarar tipos de petición, atar el token a cada página y no pasar texto libre al chat. Hoy no hace falta, y el propietario lo valoró y no lo pidió.

### Cada documento con preguntas es un front {#diseno-front}

Lo común es el servidor (`sf_proxy`), el token, la numeración y el camino al chat. Lo que cambia es la interfaz: cada documento con preguntas se considera un **front** y se crea a la medida de sus necesidades concretas (417). El informe deliberativo es el primero; la visión, la definición técnica o cualquier otro documento con preguntas tendrán el suyo, sin heredar sin más el del informe. Cómo envía su información cada front lo trata [Cómo envía un front lo que se contesta (7)](#p7).

Quien crea un front nuevo define, como mínimo:

- **Qué se contesta:** qué es una pregunta o un dato en ese documento y qué formas de respuesta admite (opción, matiz, texto libre, cifra).
- **Cuándo se envía:** todo a la vez, cada respuesta, por bloques o un borrador (pregunta 7).
- **Qué mensaje llega al chat:** su texto, con el título del documento, la versión y la huella, y cómo se nombra cada cosa para entenderse sola.
- **Qué hace Claude al recibirlo:** dónde lo registra (el documento, las decisiones) y con qué skill.
- **Cómo se corrige:** si se puede mandar de nuevo algo ya enviado y qué prevalece.
- **Qué ve quien contesta:** el estado de cada cosa (elegida, enviada, en el chat, guardada) y qué pasa sin sesión.
- **Cómo cambia el documento:** qué pasa si se regenera con cambios en lo ya contestado.

### La respuesta de un informe, el primer front {#diseno-fichas}

El generador común (`documento_a_html.py`) añade a cada pregunta abierta de `::: preguntas` lo que hace falta para contestarla. Su comportamiento vive en un script nuevo del kit, `respuestas.js`, que no sale al imprimir ni en la copia guardada:

- elegir una opción (A, B, C…) pulsando en ella, con la recomendada marcada como hoy, y un campo «Matiz» opcional;
- una barra fija «Enviar a Claude · N elegidas», solo con la página conectada; desde el disco, «Copiar las respuestas»;
- **el estado de cada ficha**, con su marca: *Abierta*, *Elegida* (guardada en el navegador, sin enviar), *Enviada* (el mod la ha recibido), *En el chat* (Claude ya la tiene o la verá al acabar lo que hace), *Escrita en tu prompt* (tras un Esc: pulsa Intro) y *Guardada aquí* (sin sesión);
- al regenerar el informe con la pregunta `estado=decidida`, la ficha sale decidida y la página olvida lo que tenía guardado para ella.

Lo elegido se guarda en el navegador por la dirección de la página **sin** el token, de modo que al abrirla otra vez, con su token nuevo, las elecciones siguen ahí. La página manda la ruta del informe, su versión y su huella (las del pie del HTML); si no coinciden con el `.md` actual, el mensaje lo dice, para que el principal mire si la pregunta ha cambiado. El envío es una petición más: `POST /respuestas` con las elecciones en JSON.

### Cómo llega una petición al chat, o a quien la atienda {#diseno-mensaje}

El servidor escribe una línea por petición. El mod la lee y la encamina:

1. **Por defecto, al chat.** El mod la convierte en un mensaje del propietario con el nombre de la página y lo que manda, y llama a `encargarAClaude`. El principal decide qué hacer, como con cualquier mensaje tuyo.
2. **A quien la atienda.** Una petición puede ir marcada para otro destino (un proceso hijo, una skill, un script) cuando una interfaz necesite una respuesta inmediata sin pasar por Claude. Cómo se marca y si ya se diseña es la pregunta [Qué pasa con una petición que no es una respuesta (6)](#p6).
3. **El acuse.** Al hijo no se le puede escribir tras arrancar, así que el mod contesta con `$.http.fetch` a una ruta interna con su propia clave, o con un archivo de acuse si la política de red del motor no deja llamar a `127.0.0.1` (lo primero que hay que probar). La página pregunta el estado cada pocos segundos y lo enseña.

El mensaje de las respuestas de un informe, con cada pregunta por su título y su número entre paréntesis (decisión «Cada pregunta al propietario se entiende sola», 397):

```text
Respuestas al informe «Responder a un informe desde la página» (tarea 475), versión 2.0, enviadas desde la página:

- Cuándo está encendido el servidor (pregunta 2): A, la recomendada.
- Qué hace Claude al recibir las respuestas (pregunta 3): B. Matiz: «solo la primera vez».
- Sin responder: Mandar solo algunas respuestas (pregunta 4).

Regístralas en el informe (una vuelta, con sf:informe_deliberativa) y en las decisiones que salgan.
```

Si la sesión no está abierta, la petición falla. La página deja las elegidas en *Guardada aquí* y lo vuelve a intentar cada diez segundos mientras está abierta; «Copiar las respuestas» copia el mismo texto para pegarlo en el chat. Con una sesión nueva, el token anterior no vale: el servidor contesta «ábrela de nuevo desde la SF», y las elecciones siguen en el navegador.

## Alternativas | Las otras formas de hacerlo, con sus pros y sus contras | Alternativas {#alternativas}

::: tarjetas 2 plegables

### Renovar el token en cada llamada {color=aviso icono=aviso}

**Pros:** cada token valdría una sola vez.

**Contras:** descartada por el propietario (416). En local aporta poco, porque quien roba el token ya lee la página, y es frágil: la página consulta cada pocos segundos y con dos pestañas o una respuesta perdida quedaría bloqueada. La numeración de las peticiones da lo mismo sin ese riesgo.

### Un servidor solo para las respuestas de informe {color=aviso icono=rama}

**Pros:** superficie mínima; solo atiende una ruta y un formato conocidos.

**Contras:** es lo que proponía la versión 1.0 y el propietario lo descartó (416): hay que ampliarlo para cada interfaz nueva, y se quería uno reutilizable.

### Un servidor genérico con tipos de petición declarados {color=aviso icono=carpeta}

**Pros:** cada página dice qué peticiones puede hacer y el servidor rechaza las demás; es lo más seguro si algún día se abre a otros.

**Contras:** hay que declarar cada tipo antes de usarlo. El propietario lo consideró y no lo pidió (416): solo lo usará en local. Queda como la salida natural si cambia el alcance.

### La página desde el disco llama al servidor {color=aviso icono=rama}

**Pros:** el mismo archivo sirve con doble clic.

**Contras:** Chrome trataría la llamada como de la red local y pediría permiso, o la bloquearía (sin probar). Todas las páginas del disco comparten el origen «null», y el servidor no las distingue: el token por apertura no se podría poner en la página.

### Un archivo de respuestas que el mod vigila {color=aviso icono=carpeta}

**Pros:** sin red ni servidor; funciona aunque la sesión esté cerrada.

**Contras:** el diálogo de guardar la primera vez, o el archivo en Descargas; consultar cada dos o tres segundos; la página no sabe si Claude lo ha recibido; y no sirve para otras interfaces.

### Solo copiar al portapapeles {color=info icono=documento}

**Pros:** trivial; el botón de copiar del kit ya existe.

**Contras:** sigue a mano. Es el respaldo del diseño recomendado, no la solución.

### Un canal MCP del plugin {color=info icono=dialogo}

**Pros:** es la vía del motor para mensajes que llegan de fuera.

**Contras:** pide un servidor MCP en el plugin y una opción al arrancar Claude Code, sin probar, y el servidor HTTP seguiría haciendo falta.

### Claude in Chrome lee la página o un Artifact con base de datos {color=info icono=lupa}

**Pros:** sin servidor propio.

**Contras:** el primero necesita la extensión y que avises a Claude; el segundo sube el informe a claude.ai y cambia dónde viven los informes. Ninguno da una interfaz propia en local.

:::

## Decidido | Lo que el propietario ya fijó | Decidido {#decidido}

| Nº | Decisión | Qué fija aquí |
| --- | --- | --- |
| 417 | Las respuestas de una página llegan al chat y Claude las registra, y cada documento con preguntas es un front hecho a su medida | Aceptadas las cinco recomendaciones: [(6)](#p6), [(2)](#p2), [(3)](#p3), [(4)](#p4) y [(5)](#p5). Cada documento con preguntas es un front. |
| 416 | El servidor local sf_proxy escucha cualquier petición de una página generada por la SF, con un token por apertura y las peticiones numeradas | `sf_proxy` es genérico, en `127.0.0.1`, de una sola sesión, con la página servida por él, un token nuevo en cada apertura y cada petición numerada. Resuelve [Cómo encuentra la página la sesión de Claude (1)](#p1) y marca el límite de la seguridad. |

## Por decidir | Lo que tiene que elegir el propietario | Por decidir {#por-decidir}

Una pregunta abierta, nueva. Las otras cinco las decidió el propietario (417) y la primera, la 416; se quedan abajo con su estado.

::: preguntas 2 plegables

### Cómo envía un front lo que se contesta (7) {recomendada=A} {: #p7}

Cada documento con preguntas tendrá su interfaz propia. Hoy contestas en el chat, una cosa tras otra. Hay que decidir cuándo manda la página lo que has elegido, empezando por el informe deliberativo, que tiene entre una y diez preguntas y suele decidirse en una sentada.

Opción A
:   **Todo a la vez, al pulsar «Enviar».** Eliges con calma, lo elegido queda guardado en la página como borrador, y un solo mensaje lleva lo elegido y dice qué falta. Si cambias algo ya enviado, lo mandas de nuevo y prevalece lo último. Un mensaje, poco ruido, poder corregir antes. El riesgo: una elección sin enviar se pierde si cierras la página sin avisar, y Claude no sabe nada hasta que envías.

Opción B
:   **Cada respuesta, al elegirla.** Cada elección es un mensaje. Claude se entera enseguida y no se pierde nada, pero el chat se llena, los mensajes llegan mientras Claude trabaja y se encolan, y corregir una elección es otro mensaje que alguien tiene que reconciliar.

Opción C
:   **Por bloques o fases.** «Enviar» manda un bloque de preguntas (por ejemplo, las de un bloque de «Por decidir»). Sirve a informes largos con partes independientes, pero obliga a partir las preguntas y deja más botones y estados que seguir.

Opción D
:   **Borrador guardado en el servidor y envío al final.** Lo elegido se guarda en `sf_proxy` mientras eliges y se envía de una vez al acabar. Sobrevive a cerrar o recargar la página, pero añade estado en el servidor que muere con la sesión y casi no mejora sobre A, donde el navegador ya guarda el borrador.

Recomendación
:   **A.** Es como decides hoy en el chat (una tanda de respuestas) y combina con lo decidido de mandar solo las elegidas: un mensaje, sin ruido y con la elección guardada en el navegador hasta enviarla. Si un informe largo lo pide, su front puede pasar a C sin tocar el servidor.

### Qué pasa con una petición que no es una respuesta (6) {estado=decidida elegida=A recomendada=A} {: #p6}

Hoy, lo que escribes en el chat lo lee Claude y actúa. Con el servidor genérico, una página puede mandar peticiones de cualquier clase, no solo respuestas de un informe, y hay que decidir qué hace el mod con ellas.

Opción A
:   Todas van al chat como un mensaje tuyo, con el nombre de la página y lo que manda. Claude decide qué hacer, como con cualquier mensaje. Si una interfaz necesita una respuesta inmediata sin pasar por Claude, se diseña cuando haga falta.

Opción B
:   Desde ya, una petición puede ir marcada para una ruta que atiende un script del plugin, sin pasar por el chat, y devuelve su respuesta a la página.

Recomendación
:   **A.** Es lo que da hoy todo lo que se necesita (las respuestas de un informe) con un solo camino; B añade un mecanismo de despacho que nadie usa aún, y se puede añadir después sin cambiar lo anterior.

Decisión
:   **A:** todo va al chat como un mensaje tuyo, con el nombre de la página; Claude decide qué hacer (decisión 417).

### Cuándo está encendido el servidor (2) {estado=decidida elegida=A recomendada=A} {: #p2}

`sf_proxy` solo hace falta mientras hay una página interactiva abierta. Encendido de más es un puerto abierto en tu ordenador sin usar, aunque solo se llegue a él desde la propia máquina.

Opción A
:   Se enciende al abrir la primera página interactiva por la SF y sigue hasta cerrar la sesión, o hasta `/sf_forzar_inactiva`.

Opción B
:   Siempre, desde que empieza la sesión con la SF activa.

Recomendación
:   **A.** Solo está encendido cuando se usa, y una página abierta sigue conectada toda la sesión.

Decisión
:   **A:** se enciende al abrir la primera página interactiva y sigue hasta cerrar la sesión (decisión 417).

### Qué hace Claude al recibir las respuestas (3) {estado=decidida elegida=A recomendada=A} {: #p3}

Las respuestas de un informe llegan al chat como un mensaje tuyo. Hoy, cuando contestas en el chat, Claude registra lo que dices en el informe y en las decisiones.

Opción A
:   Las registra directamente, como si las hubieras escrito: una vuelta del informe y sus decisiones. Solo te pregunta si un matiz deja algo dudoso.

Opción B
:   Te las repite en el chat y espera tu OK antes de registrar nada.

Recomendación
:   **A.** Pulsar Enviar ya es tu decisión; repetirla es el paso que la página quiere ahorrar.

Decisión
:   **A:** Claude registra directamente las respuestas de un documento, sin pedir otro OK salvo un matiz dudoso (decisión 417).

### Mandar solo algunas respuestas (4) {estado=decidida elegida=A recomendada=A} {: #p4}

Un informe puede tener muchas preguntas, y a veces sabes unas y otras no.

Opción A
:   «Enviar» manda las que has elegido. Las demás siguen abiertas en la página y en el informe, y el mensaje dice cuáles faltan.

Opción B
:   «Enviar» solo se activa con todas las preguntas abiertas elegidas.

Recomendación
:   **A.** Deja decidir por partes, que es como se trabaja hoy en el chat.

Decisión
:   **A:** «Enviar» manda las elegidas (decisión 417).

### En qué documentos se puede contestar (5) {estado=decidida elegida=A recomendada=A} {: #p5}

Las fichas de preguntas son un recurso común del generador de documentos. Las usan los informes de las deliberativas, y pueden usarlas la visión, la definición técnica y los demás documentos con preguntas al propietario.

Opción A
:   En todos los documentos del generador que tengan preguntas abiertas.

Opción B
:   Solo en los informes de las tareas deliberativas, para empezar.

Recomendación
:   **A.** El recurso es el mismo; limitarlo costaría más que no hacerlo.

Decisión
:   **A:** en todos los documentos del generador con preguntas abiertas (decisión 417).

### Cómo encuentra la página la sesión de Claude (1) {estado=decidida elegida=A recomendada=A} {: #p1}

Para que «Enviar» llegue a Claude, la página del informe tiene que hablar con el mod de la SF de tu sesión, y el mod no puede escuchar por sí mismo.

Opción A
:   El mod levanta un servidor en `127.0.0.1` que **sirve la página** y recoge sus peticiones. Abrir y la orden de cada vuelta la abren por él. Con doble clic, desde el disco, solo se puede copiar.

Opción B
:   El mismo servidor, pero la página se abre desde el disco, como hoy, y lo llama; Chrome puede pedir permiso de red local o bloquearlo.

Opción C
:   Sin servidor: la página guarda un archivo de respuestas y el mod lo recoge consultando la carpeta cada pocos segundos.

Recomendación
:   **A.** Es la única que no depende de un permiso del navegador y que permite poner un token nuevo en la página al servirla.

Decisión
:   **A, y genérico:** el servidor escucha cualquier petición de una página generada por la SF, con un token por apertura y las peticiones numeradas (decisión 416).

:::

## Pasos de esta tarea | Lo que se implementa aquí | Pasos {#tareas}

Por decisión del propietario, todo se hace en esta tarea (475), que pasa a ser de implementar: no salen tareas aparte, son sus pasos. Con el servidor `sf_proxy` de la decisión 416 y los informes deliberativos como primer front.

| Paso | Tipo | Qué hace |
| --- | --- | --- |
| Servir las páginas de la SF y atender sus peticiones con sf_proxy, el servidor local del mod | implementar | Primero, probar que `$.http.fetch` llega a `127.0.0.1`. `tools/sf_proxy.py` y el mod: levantarlo para una sesión concreta, con el puerto guardado y el secreto de la sesión, y pararlo con ella; registrar cada página al abrirla y darle un token nuevo; servirla con el token dentro; rechazar un número de petición repetido o anterior; las demás comprobaciones de seguridad; el encaminado de cada petición al chat con `encargarAClaude` y los acuses. Primero, probar en Chrome y Edge que `$.http.fetch` llega a `127.0.0.1`. |
| Front de los informes deliberativos: elegir, matizar, Enviar y el estado de cada ficha | implementar | Primer front, con el envío que decida la pregunta 7. El generador común y `respuestas.js` del kit: la numeración de cada petición, las fichas que se eligen, la barra de Enviar o Copiar, el estado de cada ficha y lo guardado en el navegador; y el texto de `sf:crear_documentos` y `sf:informe_deliberativa`. Depende de la anterior. |
| Abrir las páginas interactivas por el servidor, con su token nuevo | implementar | Cambiar el botón Abrir (decisión 396) y la orden de cada vuelta (decisión 393): registrar la página, abrir la dirección con su token y, si el servidor no está, el archivo. |
| Qué hace el principal con un mensaje de respuestas, y la lista de lo que define un front | implementar | La regla en `sf:orquestacion` (texto en el anexo). |
| Actualizar «Cómo funciona la Software Factory» y Actualizar «Cómo funciona el panel» | documentar | Al final, con el texto del anexo y en su tarea «Actualizar un documento». |

## Anexo: texto propuesto para otros documentos | Para los pasos que los cambian | Anexo {#anexo}

**«Cómo funciona la Software Factory»**, al final de «El mod de estado»:

> El mod también levanta en el propio ordenador `sf_proxy`, un servidor local (`127.0.0.1`, que no sale de la máquina) para una sesión concreta de Claude, que muere con ella, y que sirve las páginas interactivas que genera la SF y atiende sus peticiones. Cada vez que se abre una página interactiva lleva un token nuevo, cada petición va numerada y no vale una repetida, y sin token válido el servidor no atiende. Lo primero que hace con él es recoger las respuestas a las preguntas de los documentos: se elige y se pulsa «Enviar», y llegan al chat como un mensaje del propietario. Sin la sesión abierta, las respuestas se quedan en la página para enviarlas o copiarlas después.

**«Cómo funciona el panel»**, en «Actuar desde el panel», un apartado nuevo «Las respuestas de los documentos»:

> Abrir y la orden de cada vuelta abren el documento por `sf_proxy`, el servidor local del mod, si está encendido (`http://127.0.0.1:<puerto>/…`), con un token nuevo en cada apertura. En la página, cada pregunta abierta se contesta eligiendo una opción y, si hace falta, un matiz. «Enviar a Claude» las manda, y cada ficha dice si está elegida, enviada, en el chat o guardada en la página. El mod pone en el chat un mensaje tuyo con el título del documento y cada pregunta con su elección. Si Claude está trabajando, el mensaje espera a que acabe; tras un Esc, se queda escrito en el prompt para enviarlo con Intro. Abierto desde el disco, el documento solo permite copiar las respuestas.

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
