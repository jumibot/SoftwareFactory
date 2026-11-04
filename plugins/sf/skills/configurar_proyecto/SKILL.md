---
name: configurar_proyecto
user-invocable: false
description: Cambia la configuración de un proyecto ya incorporado a la Software Factory (SF), la de .sf/proyecto.json — nombre, descripción, color de sesión, metodología, kanban, línea de coautoría de los commits, idioma, formato de commit, remoto de GitHub, rama de publicación (rama_main), manifiestos con versión y automatizaciones — sin tarea y fuera del panel. Claude enseña lo que hay, pregunta qué cambiar con menús de hasta cuatro preguntas, pide el OK y lo aplica en develop con su commit. La lanza la orden /sf_config; también se ofrece al poner al día el proyecto. Úsala cuando pidan cambiar, ver o revisar la configuración del proyecto o uno de sus valores (activar o quitar la metodología, elegir o quitar el kanban, cambiar o quitar la firma de coautoría de los commits, cambiar el remoto, el idioma, el formato de los commits, la rama de publicación, el manifiesto, el color, el nombre o la descripción, apagar o encender una automatización).
---

# Configurar un proyecto con la SF

La configuración de un proyecto con la SF está en `.sf/proyecto.json`, en campos sueltos («Todo proyecto.json es configuración: plana, y bloques solo para lo afín», 227). Se elige al incorporarlo (`sf:incorporar_proyecto_a_sf`) y se cambia después con esta skill, pidiéndoselo a Claude o con la orden `/sf_config` («La configuración se cambia pidiéndoselo a Claude, con menús», 228, corregida el mismo día). El esquema y los valores por defecto, en el informe «Configuración inicial» de la tarea 263; aquí, lo que hace falta para cambiarlos.

**Una operación, sin tarea.** Cambiar la configuración no se anota en la cola, no crea tarea ni rama y no pasa por el panel, como incorporar y poner al día («Incorporar un proyecto es una operación sin tarea, guiada por menús», 209). Claude lo lleva desde la línea de prompts, con menús (la herramienta de preguntas con opciones) y mensajes cortos: enseña lo que hay, pregunta qué cambiar, dice qué va a cambiar, pide el OK y lo aplica en `develop`, con su commit. Lo que salga mal se deshace con git.

**Un proyecto por sesión.** Siempre el de la carpeta de la sesión. Si no tiene `.sf/proyecto.json`, no está incorporado: se dice en una línea y se ofrece incorporarlo (`sf:incorporar_proyecto_a_sf`). En el repositorio de la propia SF no hay nada que configurar: su configuración sale de su marca (el manifiesto del plugin y lo demás por defecto). Si el proyecto que se quiere configurar es otro, se propone abrir una sesión en él.

**Lo fijo no se configura.** La cola, el modelo de ramas con `develop` (205), un remoto en GitHub (230), los commits de Claude (225) y la versión con su tag (226) no tienen campo. Si se pide quitarlos, se explica en una línea por qué la SF no funciona sin ellos, como al incorporar. `sf` tampoco se cambia aquí: lo escribe la puesta al día con la versión instalada.

## Herramienta

Lo que se ve y se detecta con comandos no se infiere. `tools/configuracion.py` del plugin (`<plugin>` es la carpeta de esta skill, dos niveles arriba) solo lee; la usa también la incorporación:

- `python -I -X utf8 <plugin>/tools/configuracion.py ver` — lo que dice el archivo, lo que vale cada campo (con los valores por defecto donde falta) y los problemas. Sale con 0 sin problemas, con 1 si los hay y con 2 si el proyecto no está incorporado o no es un repositorio git.
- `python -I -X utf8 <plugin>/tools/configuracion.py detectar` — los remotos (cuáles son de GitHub y a cuál siguen `develop` y la rama de publicación), las ramas `main`, `master` y `develop`, los manifiestos con versión, la forma de los últimos 50 commits y su línea de coautoría más usada, y los colores de los proyectos vecinos.

Con `--json`, la salida para leerla. Si el mod dice que en esta máquina Python se lanza con otro nombre (en macOS, `python3`), con ese (236). El idioma no se detecta con comandos: Claude lo dice leyendo el README, el `CLAUDE.md` y los últimos commits.

## Procedimiento

1. **Lo que hay.** Se ejecutan `ver` y `detectar`, y se enseña la configuración en una tabla corta: campo, valor y «por defecto» si no está en el archivo. Debajo, los problemas que dé `ver`, cada uno con lo que se propone (por ejemplo, «`kanban` en cadena: pasa a bloque»). Si el propietario ya ha dicho qué quiere cambiar («pon los commits en conventional», `/sf_config idioma`), no se pregunta el paso 2: se va a su pregunta del paso 3 con lo pedido como opción recomendada.

2. **Qué cambiar (menú 1).** Un menú de selección múltiple, con una pregunta por grupo; los problemas de `ver` vienen ya marcados en el texto de su opción («Remoto (no existe `origin`)»):

   | Pregunta | Opciones |
   | --- | --- |
   | Identidad | Nombre / Descripción / Color / Nada de esto |
   | Método, kanban y firma | Metodología / Kanban / Coautoría / Nada de esto |
   | Convenciones | Idioma / Formato de commit / Manifiestos / Nada de esto |
   | Repositorio y automatizaciones | Remoto / Rama de publicación / Automatizaciones / Nada de esto |

   Si en todos se elige «Nada de esto», se acaba sin cambiar nada.

3. **Los valores (menús 2 y siguientes).** Una pregunta por campo elegido, hasta cuatro por menú, por este orden: identidad, método, kanban y firma, convenciones, repositorio. La opción recomendada va primero, con lo que la delata, y el valor actual lleva «(actual)». Un valor libre (un nombre, una descripción, un remoto nuevo) se escribe en «Other».

   | Campo | Pregunta | Opciones (la recomendada, primero) | Al aplicar |
   | --- | --- | --- | --- |
   | `proyecto` | ¿Nombre del proyecto? | El del README o la carpeta / el actual | — |
   | `descripcion` | ¿Descripción? (120 caracteres como mucho) | La primera frase del README / la actual | Más de 120: se acorta y se vuelve a preguntar |
   | `color` | ¿Color de las sesiones? | Dos o tres libres de `detectar` / el actual | `purple` no: es de la SF |
   | `metodologia` | ¿Seguir la metodología: fases y documentos del método? | «Sí» / «No: solo tareas, repositorio y decisiones» | Al activarla, se crea `.sf/estado.json` con la fase real, como al incorporar (su paso 3); al quitarla, `.sf/estado.json` se queda (está fuera de git) y el panel deja de pintar la fase |
   | `kanban` | ¿Kanban? | «Ninguno» / «JKanban: `<proyecto>`» | «Ninguno» quita el campo. Mientras JKanban no esté conectado, el proyecto no se crea en él: queda en los pendientes del informe (224) |
   | `coautor` | ¿Con qué línea de coautoría firma Claude sus commits? | La más usada en los últimos 50 commits (`detectar`) / «La de esta sesión: `Co-Authored-By: Claude <modelo> <noreply@anthropic.com>`» / «Sin línea de coautoría» | «Sin línea» quita el campo (o lo deja en `null`). Vale desde el siguiente commit de la SF: cierre, decisión, RELEASE y encargos nuevos (238) |
   | `idioma` | ¿En qué idioma escribe Claude commits, tareas y documentos? | El detectado / español / inglés | Código corto: `es`, `en`, `ca`… |
   | `commits` | ¿Cómo son los commits? | El propuesto por `detectar` (por ejemplo, «Conventional, 41 de los últimos 50») / «Como los de ahora (`<ejemplo>`), con `SF-Tarea: N`» / «Libres, con `(N)` al final» | Cambia la marca del número (207) y el prefijo del squash (233) desde el siguiente cierre; los commits de antes no se tocan, y el panel encuentra los de una tarea en las dos formas |
   | `manifiesto` | ¿Qué manifiestos suben de versión al publicar? | Cada uno de `detectar` (selección múltiple) / «Ninguno: solo el tag» | Ninguno: `null`. Otros formatos (`pom.xml`, `Cargo.toml`) aún no se soportan: se dice y no se guardan (226) |
   | `remoto` | ¿A qué remoto de GitHub se hace push? | Cada remoto de GitHub de `detectar`, primero el que sigue `develop` | En «Other», la url de un repositorio de GitHub: se añade como remoto (`git remote add <nombre> <url>`). Un remoto fuera de GitHub no se ofrece ni se acepta, y no se puede quedar sin remoto (230) |
   | `rama_main` | ¿En qué rama se publica? | `main` / `master` (las que existan) | Si la elegida solo está en el remoto, se crea la local siguiéndola, sin preguntar (234); si no existe, se ofrece crearla desde la actual, como al incorporar (213). La de antes queda como estaba |
   | `automatizaciones` | ¿Qué automatizaciones quedan encendidas? (selección múltiple) | `orquestacion` / `avisos_subagentes` / `encargo_subagente` / `dependencias_al_actualizar`, marcadas las encendidas | Se escriben solo las apagadas (`false`); con todas encendidas, el bloque se quita (171) |

   Qué hace cada automatización, en una frase, en la pregunta: `orquestacion`, el mod entrega `sf:orquestacion` al empezar, tras `/clear` y tras compactar (si no, la carga el principal); `avisos_subagentes`, los avisos de tareas en curso sin subagente y de subagentes terminados sin recoger; `encargo_subagente`, `cola.py encargo` escribe la parte fija del encargo; `dependencias_al_actualizar`, al actualizar el plugin desde el panel se instalan sus dependencias.

4. **Lo que va a cambiar, y el OK.** Una lista corta, campo a campo, con el valor de antes y el de después (por ejemplo, «`commits`: libre → conventional»), lo que se escribe aunque coincida con el valor por defecto y lo que se hace además (un remoto que se añade, una rama que se crea, `.sf/estado.json`). Lo que el propietario no ha cambiado pero estaba mal (los problemas de `ver`, como el `kanban` en cadena) va en la misma lista, marcado como arreglo. Se pide la autorización en un menú: «Aplicar» o «No aplicar». Sin cambios reales, no hay menú: se dice que queda igual.

5. **Aplicar en `develop`.** Con el OK:
   - Si la sesión está en otra rama, se pasa a `develop`; si hay cambios sin commit en `.sf/proyecto.json`, se dice y no se aplica hasta que estén resueltos.
   - Se edita `.sf/proyecto.json` con la herramienta de edición: se cambian solo los campos elegidos y se conserva el orden y lo demás. Se escribe siempre lo confirmado, aunque coincida con el valor por defecto, salvo `automatizaciones`, que solo aparece si se apaga algo. `kanban` va en bloque, `{ "proveedor": "jkanban", "proyecto": "…" }`.
   - Se hace lo que va además (el remoto, la rama, `.sf/estado.json`).
   - Se repite `ver`, que debe salir sin problemas; si no, se dice y se arregla antes del commit.
   - Commit propio en `develop`, sin número de tarea: «Configuración del proyecto: `<campos>`», en el idioma y el formato con que queda el proyecto (con conventional, `chore: configuración del proyecto: …`). Lo hace Claude (225). Después, `git push <remoto> develop` al remoto con que queda (con `-u` si es nuevo); si falla, se dice con su orden y lo local queda hecho.

6. **Informe.** En pocas líneas: qué ha cambiado, el commit y lo que pide hacer el propietario:
   - **`/clear`**, si ha cambiado algo de lo que el mod entrega al empezar la sesión: `metodologia`, `idioma`, `commits`, `remoto`, `rama_main` o `automatizaciones.orquestacion`. La conversación en curso sigue con lo de antes.
   - El nombre y el color los aplica el mod a la sesión en cuanto lee el archivo, al acabar el turno.
   - Los subagentes que ya trabajan siguen con su encargo; lo nuevo vale para los siguientes y para los cierres a partir de ahora.
   - No se afirma que el proyecto exista en el kanban si no se ha creado.

   No queda nada en la cola.

Si algo de la SF falla, sobra o falta, no se anota en el proyecto: se dice en una línea que es de la SF, y llevarlo a ella es cosa del propietario, en una sesión de la SF («Un proyecto solo anota propuestas suyas», 210).
