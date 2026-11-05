# Ciclo de vida de una tarea: estados y cambios

Cada cambio de estado de una tarea, con su regla y su orden del CLI `tools/cola.py`. Los números entre paréntesis son decisiones de la SF (`docs/decisiones/` de su repositorio).

Cuándo usar cada cambio en la conversación con el propietario (menú al anotar, subagentes, probar y cerrar, fusionar y redescribir) está en la skill `sf:orquestacion`.

## 1. Estados y marcas

### Estados guardados en la cola

El campo `estado` de cada tarea en `.sf/peticiones.json` admite cuatro valores (`ESTADOS_PETICION`, `constantes.ts`). Una tarea con otro valor o sin texto se descarta al leer y el panel avisa.

- **`en-cola`**: anotada, sin empezar. Entra así la petición nueva que el propietario deja en cola en el menú de alta (031, 048, 139).
- **`en-curso`**: se trabaja en ella. Puede haber varias, cada una en su rama; arriba, la más reciente primero (048, 083).
- **`en-observacion`** (**En observación**): cerrada y en observación. Con rama, ya está en `develop` por squash. Se vigila cómo funciona con el uso, con su `prueba` dicha: se cierra si va bien o se revierte si va mal (050, 054, 115, 204, 212).
- **`descartada`**: su rama se ha borrado. Sigue en la cola hasta limpiar Cerradas o hasta empezar otra sesión (078, 088).

### Marca sobre un estado

- **`observando: true`**: solo en `en-observacion`. El propietario la está mirando ahora («La miro ahora»). El panel la trata como en curso, arriba y en amarillo (060).

### Situaciones fuera de la cola

La tarea sale del archivo y pasa, con su historial, a `.sf/historial.jsonl` (115). Allí su `estado` es el de salida: `cerrada`, `eliminada`, `absorbida`, `descartada` (limpiada) o, en las revertidas antes de la decisión 134, `revertida` (sección 3).

- **Cerrada**: salió por la C, cerrada en observación o por un cierre sin rama (050, 090, 101).
- **Eliminada**: salió con la E, con «R eliminar» o por Claude, sin pasar por Cerradas; su número no se reutiliza. Se recupera del historial (079, 115, 134).
- **Absorbida**: salió por `/sf_fusionar`, dentro de la de número más alto (099).
- **Revertida**: cerrada o en observación, con su squash deshecho en `develop` con `git revert` (107, 115). Solo las de antes de la decisión 134: ahora una revertida sale eliminada o vuelve a Pendientes.

Son cuatro estados guardados, una marca y cuatro situaciones fuera de la cola.

Una cola, una copia o un historial con los nombres de antes de la decisión 215 se convierte al cargarlo, una vez: el estado y el campo de antes de «En observación» y sus eventos pasan a `en-observacion`, `observando` y los eventos de ahora (`a-observacion`, `cerrada`, `observando`, `seguir`). No hay alias: las órdenes de antes ya no existen (215).

### Campos que cambian sin cambiar de estado

- `rama`: con rama, la tarea ya tiene trabajo efectivo; deja de ser eliminable y pasa a descartable (079, 082). La pierde al entrar en `develop`.
- `pasos`: cada uno `hecho`, `en-curso` o `pendiente` (067).
- `reabierta: true`: vuelve a la cola por un bug después de haber salido (061, 064).
- `historial`: cada cambio, con fecha y quién (sección 3).

### Letras del panel

La letra es el estado; el número, el código. Los dos son iguales en todos los sitios: «57-A» (054, 058). El panel la saca del historial de cada tarea (145):

- **A**: en cola o en curso, creada (o nacida de un `/sf_split`) después de abrir la sesión.
- **H**: en cola o en curso, ya estaba al abrir la sesión, está reabierta o no tiene historial. Una H no pasa a A (053, 069).
- **O**: en observación (`en-observacion`).
- **C**: fuera de la cola tras cerrarse.
- **D**: descartada, en la cola o ya limpiada (089).
- **R**: revertida, solo las de antes de la decisión 134 (107). Ahora una revertida sale sin letra, eliminada, o vuelve con H.

Fuera de la cola, la letra es el estado con que salió, en `.sf/historial.jsonl`.

### Colores y marcas de la sesión

- **Amarillo**: la tarea en curso, arriba y en su código de las secciones (039, 084).
- **Rojo en Pendientes**: el número de las H (054).
- **Rojo en Cerradas**: reabierta, A o H, hasta volver a cerrarse (061, 064).
- **Verde en Cerradas**: C; «●» si tiene commit (044).
- **Cuenta «3/5»**: pasos hechos de todos (067).

### Lo que el panel lee del historial

El panel no deduce lo ocurrido comparando colas: lo lee del historial de cada tarea y de `.sf/historial.jsonl` (113, 145). De ahí salen la A y la H; Cerradas, las tareas con un evento de cierre en la sesión (`a-observacion`, `cerrada`, `descartada`, `revertida`, `reabierta`), sin las eliminadas ni las absorbidas; los commits de cada tarea, para la R; y los push pendientes. En `$.state` solo guarda las limpiadas, con la fecha de su último cierre.

## 2. Cambios de estado

Una tarjeta por cambio, con ocho campos: **De → a**, **Cuándo**, **Quién**, **Autorización**, **Repositorio**, **Panel**, **CLI** (su orden) y **Sale de** (decisiones). «Principal» es el agente que habla con el propietario; «subagente», el que ejecuta en su worktree; «panel», el mod, que actúa al pulsar el propietario un botón o escribir un comando. Solo el principal y el panel escriben la cola (083, 110, 115).

Las órdenes van como `python -I -X utf8 "$HOME/.claude/sf/cola.py" <orden>` (el `cola.py` del plugin cargado, nunca el de una carpeta, y con el intérprete que diga el mod si no es `python`; SKILL.md); aquí, `cola.py <orden>`. Cada una comprueba las condiciones de **De → a**; si no se cumplen, no toca nada y dice por qué.

### Alta y arranque

#### 01 · Crear una tarea

- **De → a:** nada → `en-cola`, con `id` = `ultimo` + 1; `ultimo` sube.
- **Cuándo:** llega una petición, un bug o un error detectado (031, 077, 096).
- **Quién:** principal; panel con «A Pendientes» en Propuestas.
- **Autorización:** el menú de alta (139). Si, a juicio del principal, encaja como paso de una tarea, pregunta primero si se añade a ella (06); si no encaja o el propietario lo descarta, pregunta si va en curso (02) o se queda en cola. Menú breve; sin la pregunta que el propietario ya responde al pedir («tarea», «paso de la NN», «en curso», «en cola»). Con «→» en el panel, sin menú.
- **Repositorio:** nada.
- **Panel:** Pendientes, con A.
- **CLI:** `cola.py crear "texto" --descripcion "…" [--en-curso]` (la descripción, obligatoria cuando crea Claude; el propietario y el panel pueden omitirla, tarea 326). Desde una propuesta por decidir de `sf/propuestas.md` («A Pendientes» en Propuestas), `cola.py de-propuesta "título" [--numero P07] [--descripcion "…"] [--tipo T]`: crea la tarea y cambia el «Estado» de la propuesta por «pasada a la tarea N de la cola el <fecha>», con su commit en `develop` (como en «A propuesta»); si ya no está por decidir en `develop`, no hace nada.
- **Sale de:** 031, 048, 077, 096, 098 (descripción sin origen), 092, 139.

#### 02 · Crear en curso

- **De → a:** nada → `en-curso`, con los pasos de cierre, «Activar rama para poder probar» y «Cerrar la tarea», pendientes (174).
- **Cuándo:** el propietario elige «En curso» en el menú de alta o lo dice al pedir.
- **Quién:** principal.
- **Autorización:** ninguna.
- **Repositorio:** nada (la rama, en 05).
- **Panel:** arriba, en amarillo, con A.
- **CLI:** `cola.py crear "texto" --descripcion "…" --en-curso`.
- **Sale de:** 048, 139.

#### 03 · Poner en curso

- **De → a:** `en-cola` → `en-curso`, con los pasos de cierre, «Activar rama para poder probar» y «Cerrar la tarea», pendientes (174): se añaden al final los que falten, sin repetirlos. Una deliberativa (investigar, deliberar, diseñar) sin rama, solo con «Cerrar la tarea»: no se prueba (218, 278).
- **Cuándo:** el propietario pregunta por ella o la elige; o pulsa Activar rama en una tarea en cola; o pulsa TURBO y la tarea se puede hacer sin interactuar con él (160).
- **Quién:** principal; panel con Activar rama.
- **Autorización:** la pregunta del propietario basta, salvo choque: antes, el principal ejecuta `cola.py choques 87` (con `--archivos` y los previstos si aún no tiene rama); si comparte archivos con otra en curso o en observación, dice con cuál y cuáles, recomienda esperar o fusionarlas y sigue solo con el OK del propietario. No al lanzar subagentes de tareas ya en curso.
- **Repositorio:** nada; con Activar rama, `git switch` (ver 15).
- **Panel:** sube arriba, en amarillo; conserva A o H.
- **CLI:** `cola.py choques 87 [--archivos a b …]` (consulta: 0 sin choques, 3 con choques), luego `cola.py en-curso 87`.
- **Sale de:** 048, 103, 130.

#### 04 · Dejar para luego

- **De → a:** `en-curso` → `en-cola`.
- **Cuándo:** se aparca una tarea empezada.
- **Quién:** principal.
- **Autorización:** el OK del propietario.
- **Repositorio:** vuelve a la cola sin rama. Si la suya no tiene commits propios respecto a `develop`, se borra (antes pasa a `develop` si era la activa); si ya no existía, se quita la anotación. Lo de su subagente, vacío, se recoge como al cerrar: worktree y rama auxiliar. Con commits propios en su rama o en una auxiliar, o con cambios sin commit en el worktree del subagente, el CLI lo rechaza; para dejarla, se cierra, se pasa a observación o se descarta (170, 275).
- **Panel:** vuelve a Pendientes; la sesión la apunta en `dejadas`.
- **CLI:** `cola.py en-cola 87`.
- **Sale de:** 115 (9), 170, 275.

#### 05 · Crear la rama

- **De → a:** `en-curso` → `en-curso`, `rama`: null → `feature/NN-nombre`.
- **Cuándo:** antes de tocar el primer activo (todo lo escrito y versionado en el repositorio). Nunca en una deliberativa (investigar, deliberar, diseñar): no tiene rama, worktree ni `sub-NN`, y su documento va directo a `develop` en cada vuelta; `cola.py rama` se niega (256, 278).
- **Quién:** principal. Para un subagente, la crea y la anota antes de lanzarlo.
- **Autorización:** ninguna; avisa al crearla.
- **Repositorio:** `git switch -c feature/NN-nombre develop`, o `git branch` sin activarla si va a un subagente.
- **Panel:** la E deja paso a Activar rama y la D.
- **CLI:** `cola.py rama 92 flujo-tareas [--sin-activar]`; `--anotar` apunta una rama que ya existe.
- **Sale de:** 082, 079, 115 (16).

### Durante el trabajo

#### 06 · Añadir un paso

- **De → a:** sin cambio de estado; paso nuevo `pendiente`, antes de los de cierre; si «Activar rama para poder probar» estaba hecho, vuelve a pendiente: hay que probar otra vez (174). Con `--prueba`, una ayuda de prueba (`ayuda: true`): va tras «Activar rama para poder probar» y antes de «Cerrar la tarea», no la exige ningún cierre y no devuelve «Activar rama» a pendiente; se marca y se quita como cualquier paso (184).
- **Cuándo:** surge al trabajar, el propietario lo da en el chat (menú de alta, 01) o escribe `/sf_paso`. Definir, diseñar y decidir también son pasos.
- **Quién:** principal; panel con `/sf_paso`, que además se lo pide a Claude: el principal se lo pasa al subagente de la tarea.
- **Autorización:** con un encargo nuevo en el chat, el menú de alta (01) pregunta si se añade como paso a la tarea en la que encaja.
- **Repositorio:** nada.
- **Panel:** la cuenta «n/m» crece; una ayuda de prueba no cuenta y se ve con «(opcional)».
- **CLI:** `cola.py paso añadir 92 "texto"`, `cola.py paso añadir 92 "Abrir el panel y mirar X" --prueba`; rechaza el texto de un paso de cierre (253, 174).
- **Sale de:** 067, 072, 080; en el historial, 115 (11).

#### 07 · Marcar un paso

- **De → a:** paso `pendiente` → `en-curso` → `hecho`; al hacerse, el texto pasa a participio.
- **Cuándo:** al empezarlo y al acabarlo.
- **Quién:** principal (un subagente lo dice en su informe).
- **Autorización:** ninguna.
- **Repositorio:** nada.
- **Panel:** ▸ en curso, ✓ hecho; bajo la tarea de arriba, el paso en curso.
- **CLI:** `cola.py paso marcar 92 3 en-curso`, `cola.py paso marcar 92 3 hecho --texto "Redactada la tabla"`. El número cuenta desde 1, como el `n` de cada paso en `ver 92`. Un paso de cierre no cambia de texto, ni otro toma el de uno de cierre (253).
- **Sale de:** 067, 081; en el historial, 115 (11).

#### 08 · Quitar un paso pendiente

- **De → a:** paso `pendiente` → fuera. Los de cierre, «Activar rama para poder probar» y «Cerrar la tarea», no se quitan: cerrar no pide el de prueba y lo marca al cerrar (172, 174).
- **Cuándo:** sobra un paso sin empezar.
- **Quién:** panel con la E; principal.
- **Autorización:** el clic del propietario.
- **Repositorio:** nada.
- **Panel:** desaparece el paso.
- **CLI:** `cola.py paso quitar 92 4`; rechaza los de cierre. En el panel, no llevan la «×».
- **Sale de:** 072 (ampliada), 117, 121.

#### 09 · Renombrar

- **De → a:** sin cambio; `texto` nuevo, mismo número.
- **Cuándo:** el nombre deja de reflejar la tarea; tras un `/sf_paso`, se revisa al acabar el turno.
- **Quién:** principal; propietario.
- **Autorización:** ninguna.
- **Repositorio:** nada.
- **Panel:** nombre nuevo.
- **CLI:** `cola.py renombrar 92 "texto"`. La descripción se cambia con `cola.py redescribir 92 "texto"` (vacía, la quita); cada párrafo, separado por una línea en blanco. `/sf_redescribir 92` en el panel pide a Claude que la vuelva a redactar para que se lea fácilmente, sin quitar ni añadir nada; Claude enseña la propuesta y solo la guarda con esa orden tras el OK del propietario. El tipo (deliberar, documentar, diseñar, implementar, especificar, corregir o investigar), con `cola.py tipo 92 implementar`, anotado en el historial; al crearla, `crear --tipo`. El panel lo pinta tras el título, «(IMPLEMENTAR)», atenuado.
- **Sale de:** 067, 125, 126.

#### 10 · Lanzar un subagente

- **De → a:** `en-curso` → `en-curso`; queda en el historial.
- **Cuándo:** al poner la tarea en curso, también las de diseño o deliberación y las triviales; toda tarea en curso tiene el suyo, que hace todo su trabajo. Al final de cada turno y con TURBO, el principal lanza las en curso que aún no lo tienen. Las de la cola, solo al ponerlas en curso; con TURBO, las que no necesitan al propietario (160).
- **Quién:** principal.
- **Autorización:** ninguna; avisa en una línea. Trabajo de la tarea en el principal, solo con instrucción expresa del propietario.
- **Repositorio:** worktree propio para el subagente, siempre en su rama auxiliar `sub-NN` desde la de la tarea, que se crea con `--sin-activar` (149). En una deliberativa, nada: su subagente lee en la carpeta del proyecto y solo escribe su documento, sin worktree ni `sub-NN`; no se anota (`subagente` se niega) y `encargo` da el suyo sin worktree (256, 278).
- **Panel:** ⚙ en la tarea mientras el subagente trabaja (tarea 145).
- **CLI:** `cola.py subagente 92 --worktree <ruta> [--rama <auxiliar>]`; la ruta, absoluta o relativa al proyecto. Lo anotado es lo que el CLI recoge al dejar la tarea sin subagente (169).
- **Sale de:** 083, 086, 105, 115 (14, 15, 17), 149, 151, 152 (documentos compartidos, también por subagente), 160 (TURBO).

#### 11 · Volver de un subagente

- **De → a:** `en-curso` → `en-curso`; pasos marcados según el informe.
- **Cuándo:** el subagente termina su encargo o espera al propietario. No se para: queda vivo, esperando, hasta el cierre.
- **Quién:** principal, tras revisar el diff y, si se puede, la comprobación.
- **Autorización:** ninguna; lo que pida el subagente, al propietario, y la respuesta, al subagente (SendMessage).
- **Repositorio:** commits del subagente en su rama auxiliar (`sub-NN`); el principal los trae con `git merge --ff-only`. La rama de la tarea queda libre, así que se prueba en la carpeta principal con el worktree puesto: el subagente y su worktree siguen hasta el cierre (149). Al cerrar, el CLI quita el worktree y borra la rama auxiliar (169); el principal detiene el subagente y borra a mano solo una `worktree-agent-<id>` sin commits fuera de la rama de la tarea.
- **Panel:** pasos al día; fuera el ⚙.
- **CLI:** `cola.py informe 92 --terminado|--interrumpido ["qué necesita"]`; los pasos, con `paso marcar`.
- **Sale de:** 083, 115 (15), 135, 149, 151.

#### 12 · Commit de guardado

- **De → a:** sin cambio.
- **Cuándo:** antes de cambiar de rama, antes de que un subagente pare.
- **Quién:** principal o subagente.
- **Autorización:** ninguna.
- **Repositorio:** commit en la rama de la tarea; no llega tal cual a `develop`.
- **Panel:** nada.
- **CLI:** no necesita la cola; `git commit`.
- **Sale de:** 082.

### Prueba

#### 13 · Lista para probar

- **De → a:** sin cambio; se escribe `prueba`. Los pasos de cierre ya están desde que la tarea entró en curso (02, 03, 27; 174); `listo` no los toca. Una tarea en curso de antes de la 174 los recibe al cargar la cola, una vez y al final; un repetido se quita (253).
- **Cuándo:** al acabar el último paso de trabajo. Sin «Cerrar la tarea», ninguna tarea se cierra, con rama o sin ella.
- **Quién:** principal.
- **Autorización:** ninguna. Propone probar, con cómo. Si la tarea no tiene nada que probar (deliberar, investigar, documentar, especificar…), propone cerrarla directamente, enseñando el resultado: el OK del propietario es la aprobación; se cierra (18 o 20), sin pasar por observación, y el cierre marca «Activar rama para poder probar» (172).
- **Repositorio:** nada.
- **Panel:** cuando los pasos de trabajo están hechos, aparecen «Cerrar» (la C) y «A observación», con rama o sin ella (188).
- **CLI:** `cola.py listo 92 --prueba "qué mirar"`.
- **Sale de:** 074, 090, 121, 154, 174.

#### 14 · Anotar lo comprobado

- **De → a:** sin cambio; un paso hecho «Comprobado: …», con lo comprobado y su resultado, antes de los de cierre. No devuelve a pendiente «Activar rama para poder probar».
- **Cuándo:** se comprueba algo en la tarea (las pruebas, la validación, una captura, una prueba a mano), también lo que trae el informe de un subagente.
- **Quién:** principal.
- **Autorización:** ninguna. No saca la tarea de En observación.
- **Repositorio:** nada.
- **Panel:** el paso, en «Pasos».
- **CLI:** `cola.py comprobado 92 "300 pruebas de Python, sin fallos"`.
- **Sale de:** 050, 288 (retira el campo `comprobado`: el de antes pasa a los pasos al cargar).

#### 15 · Probar en su rama (Activar rama)

- **De → a:** `en-cola` → `en-curso`; `en-curso` no cambia.
- **Cuándo:** el propietario pulsa Activar rama: tarea con rama existente que no es la activa.
- **Quién:** panel.
- **Autorización:** el clic, sin confirmar.
- **Repositorio:** `git switch <rama>` y, si `develop` no está en ella, `git merge develop`: se prueba con lo último y el cierre no choca (270). Tras el merge, adelanta la `sub-NN` a la rama de la tarea (`merge --ff-only` en su worktree), para que el siguiente `--ff-only` del principal siga valiendo. No lo hace con cambios sin commit o con la rama en otro worktree. Con choques, `git merge --abort`, vuelve a la rama de antes, no marca el paso y dice qué archivos chocan (`probar-fallido`; en `--json`, `fallo: choques` y `motivo`): lo resuelve el subagente integrando `develop` en su rama. Si una rama auxiliar tiene commits que no están en la de la tarea (el subagente no ha terminado o falta traerlos), ni integra ni activa: se probaría sin ellos. No recarga el plugin.
- **Panel:** aviso «La N, en prueba: rama … activa, con develop integrado» (sin «con develop integrado» si ya estaba al día); la cabecera muestra la rama. Con choques o con trabajo sin traer (`fallo`: `choques` o `sin-traer`), avisa y pasa el caso a Claude, como el cierre fallido, para que lo resuelva el subagente de la tarea y repita `probar` (191).
- **CLI:** `cola.py probar 92`. Activa la rama (si ya lo está, la deja: «ya era la activa», 253) y marca hecho «Activar rama para poder probar»: activar la rama no es darla por buena; el OK del propietario es cerrar (172).
- **Sale de:** 091, 092, 103, 121.

#### 16 · Mirarla ahora

- **De → a:** `en-observacion` → `en-observacion` con `observando: true`.
- **Cuándo:** a la pregunta «¿Cómo va la 66?», el propietario responde «La miro ahora».
- **Quién:** principal.
- **Autorización:** la respuesta del propietario.
- **Repositorio:** nada.
- **Panel:** arriba, en amarillo.
- **CLI:** `cola.py observando 66`.
- **Sale de:** 051, 060.

#### 17 · Seguir en observación

- **De → a:** `en-observacion` → `en-observacion`; quita `observando`.
- **Cuándo:** respuesta «Sigue en observación», o queda a medias de mirarla.
- **Quién:** principal.
- **Autorización:** la respuesta del propietario.
- **Repositorio:** nada.
- **Panel:** vuelve a En observación.
- **CLI:** `cola.py seguir 66`.
- **Sale de:** 051, 060.

### Cierre

#### 18 · Cerrar con la C (squash)

- **De → a:** `en-curso` con rama → fuera de la cola.
- **Cuándo:** tarea en curso con rama existente (sin rama, 20) que tiene el paso «Cerrar la tarea» y ningún otro pendiente salvo «Activar rama para poder probar» y las ayudas de prueba, que quedan como estén (184). Pulsar la C es el OK del propietario, «ciérrala»: «Activar rama para poder probar», si está, queda hecho. También la propuesta que toca un activo: lleva rama y squash, sin pasar por observación.
- **Quién:** panel; principal, con el OK del propietario en el chat.
- **Autorización:** dos clics, o el OK.
- **Repositorio:** antes de nada, se niega si una `sub-NN` tiene commits que no están en la rama de la tarea: el principal no los trajo y el squash los perdería; el mensaje dice cómo traerlos (`git merge --ff-only sub-NN` con la rama activa, `git fetch . sub-NN:<rama>` sin activar). Igual en `a-observacion` (271). Después, `git switch develop`, `git merge --squash <rama>`, commit con los pasos hechos en el cuerpo y el número según el `commits` de `.sf/proyecto.json` («<tarea> (N)» con `libre`; con `conventional` o `propio`, el título «<prefijo>: <tarea>», con el prefijo del tipo de tarea (implementar, `feat`; corregir, `fix`; documentar, especificar, investigar, deliberar y diseñar, `docs`; sin tipo, `chore`, aunque antes de cerrar el principal pregunta el tipo si falta o hay dudas y lo anota con `tipo N T`; decisión 233), y el trailer `SF-Tarea: N` al pie, decisión 207), `git push <remoto> develop` (el `remoto` de la configuración; `origin` si no dice otro), `git branch -D <rama>`. El hash del squash entra en el historial (`cerrada`, «develop <hash>»). Con el remoto público, antes del push revisa lo que sale (`revision_publica.py`, decisión 259): si encuentra algo, no sube. Si el push falla o no se hace, cierra igual, lo anota (`push-fallido`) y avisa; se sube después con `subir`. Después recoge el subagente: `git worktree remove` y `git branch -D sub-NN`, sin forzar; un worktree con cambios sin commit se queda, y una auxiliar con commits que no entraron en `develop` se queda, con su worktree, y se avisa: nunca se borra (`recogida` o `recogida-con-avisos`, 169, 271). El panel no para el subagente: el aviso del mensaje siguiente pide al principal detenerlo y dice lo que quedó (11).
  Con la rama sin cambios respecto a `develop` (sin commits propios, o con lo suyo ya en `develop`), no hay squash ni commit: se borra la rama (antes pasa a `develop` si era la activa), se recoge el subagente y la tarea sale como cerrada, sin commit (`cerrada`, «sin cambios: <rama> borrada»; tarea 345).
- **Panel:** Cerradas, con C y el commit; recuerda el push pendiente.
- **CLI:** `cola.py cerrar 92`; sin «Cerrar la tarea» o con un paso de trabajo sin hacer sale con 1 y dice cómo arreglarlo.
- **Sale de:** 082, 090, 101, 115 (5, 18, 19, 20), 121.

#### 19 · Cierre que falla

- **De → a:** sin cambio: sigue `en-curso`; el fallo queda en el historial (`cierre-fallido`).
- **Cuándo:** el squash choca o falla el commit.
- **Quién:** panel, que lo deshace; después, principal.
- **Autorización:** ninguna.
- **Repositorio:** `git reset --merge` y vuelta a la rama de antes; el panel envía a Claude la tarea, la rama y los archivos en conflicto.
- **Panel:** aviso; la tarea sigue arriba.
- **CLI:** `cola.py cerrar 92` sale con 1, con el error y los archivos; el principal resuelve y repite.
- **Sale de:** 111.

#### 20 · Cerrar sin rama

- **De → a:** `en-curso` sin rama → fuera de la cola.
- **Cuándo:** la tarea no tocó ningún activo (no pasa por observación); siempre, una deliberativa, cuyo único paso de cierre es «Cerrar la tarea» (278). Pide los mismos pasos que 18: «Cerrar la tarea» y ningún otro pendiente salvo «Activar rama para poder probar». Una propuesta que toca un activo lleva rama: se cierra como en 18.
- **Quién:** panel con «Cerrar» (la C); principal.
- **Autorización:** dos clics, o el principal pregunta antes de cerrar.
- **Repositorio:** nada: sin squash ni commit.
- **Panel:** Cerradas, con C, sin commit («○»).
- **CLI:** `cola.py cerrar 87`.
- **Sale de:** 048, 063, 090, 115 (20), 121, 188.

#### 21 · Cerrar y dejar en observación

- **De → a:** `en-curso` → `en-observacion`.
- **Cuándo:** el resultado solo se puede ver funcionando tras el cierre (un commit o una publicación): se cierra y se observa. Lo que no tiene nada que probar no pasa por aquí: se cierra directamente (13). Pide los mismos pasos que 18; «Cerrar la tarea» queda hecho y «Activar rama para poder probar», pendiente.
- **Quién:** panel con «A observación», con rama o sin ella (188); principal.
- **Autorización:** dos clics, o el OK del propietario al cierre.
- **Repositorio:** con rama, el squash en `develop` de 18, con su hash en el historial (`a-observacion`) y en `commit`; la rama se borra. Sin rama, `--commit` anota la versión o el commit del cierre.
- **Panel:** En observación; Cerradas, con O.
- **CLI:** `cola.py a-observacion 92 [--prueba "qué mirar"] [--commit "sf 1.0"]`. Se niega en una deliberativa (se cierra, 20) y con la rama sin cambios respecto a `develop` (se cierra, 18; tarea 345).
- **Sale de:** 050, 054, 074, 115 (4), 121, 154, 188.

#### 22 · Cerrar en observación

- **De → a:** `en-observacion` → fuera de la cola.
- **Cuándo:** va bien: el propietario da el OK («Cerrar» a «¿Cómo va?», o «ciérrala» sin número para la tarea de la rama activa). Si va mal, se revierte (26).
- **Quién:** panel con «Cerrar»; principal.
- **Autorización:** dos clics, o el OK; en duda sobre qué tarea, preguntar.
- **Repositorio:** nada: ya entró en `develop` al pasar a observación.
- **Panel:** Cerradas, con C, aunque se cerrara en otra sesión. Historial: `cerrada`, con «en observación».
- **CLI:** `cola.py cerrar 66`.
- **Sale de:** 042, 050, 051, 064, 095, 115 (4), 204, 215.

#### 22 bis · Volver a observación

- **De → a:** cerrada, fuera de la cola → `en-observacion`, con su commit de `develop`.
- **Cuándo:** se cerró por error y hay que seguir vigilándola, para poder revertirla.
- **Quién:** panel con «A observación», en Cerradas; principal.
- **Autorización:** dos clics, o la petición del propietario.
- **Repositorio:** nada.
- **Panel:** sale de Cerradas y vuelve a En observación, con su Revertir. Historial: `reobservada`.
- **CLI:** `cola.py reobservar 66`; solo una cerrada.
- **Sale de:** la tarea 296.

### Deshacer

#### 23 · Descartar (D)

- **De → a:** `en-cola` o `en-curso` con rama → `descartada`. Una en observación ya entró en `develop`: se revierte (26).
- **Cuándo:** se abandona una tarea con trabajo que no ha entrado en `develop`.
- **Quién:** panel con la D; principal si se lo piden.
- **Autorización:** dos clics, o la petición del propietario. Sin motivo.
- **Repositorio:** si la rama es la activa, `git switch develop`; `git branch -D <rama>`. No lo hace con la rama en otro worktree o con cambios sin commit. Si git falla, no toca la cola. Después recoge el subagente, como al cerrar, salvo que quita todo, también la auxiliar con commits que no entraron y el worktree con cambios sin commit (`git worktree remove --force`): el descarte descarta todo; `limpiar` hace lo mismo con lo que quedó (18, 189).
- **Recogida en el resto:** `a-observacion`, `eliminar`, `revertir` y `limpiar` también recogen el subagente, o lo que quedó de una recogida con avisos, sin forzar (169).
- **Panel:** Cerradas, con D atenuada; fuera de Pendientes y En observación.
- **CLI:** `cola.py descartar 92`.
- **Sale de:** 078, 088, 089, 092, 115 (4).

#### 24 · Limpiar Cerradas

- **De → a:** `descartada` → fuera de la cola. C y R salen solo de la lista de la sesión.
- **Cuándo:** el propietario pulsa «limpiar (N)».
- **Quién:** panel.
- **Autorización:** el clic.
- **Repositorio:** nada.
- **Panel:** desaparecen de Cerradas las C, D y R (las R, de antes de la decisión 134); si una se reabre o se vuelve a cerrar, vuelve.
- **CLI:** `cola.py limpiar` (las descartadas, con `limpiada` en su historial, a `.sf/historial.jsonl`).
- **Sale de:** 057, 087, 088.

#### 25 · Limpiar al empezar sesión

- **De → a:** `descartada` → fuera de la cola.
- **Cuándo:** primera lectura de la cola en una sesión nueva; no con `/reload-plugins`.
- **Quién:** panel.
- **Autorización:** ninguna.
- **Repositorio:** nada.
- **Panel:** no las muestra.
- **CLI:** `cola.py limpiar` (lo llama el panel al arrancar).
- **Sale de:** 078, 088.

#### 26 · Revertir (R)

- **De → a:** cerrada en `develop`, o en observación → eliminada, fuera de la cola sin rastro, como con la E; o `en-cola`, reabierta con su número (`reabierta: true`) y sin rama. Nunca queda en Cerradas con R.
- **Cuándo:** hay que deshacer una tarea ya entrada en `develop`: se abandona (eliminar) o hay que rehacerla (pendiente). La R sale en Cerradas, en las C con un commit en `develop` con su número («… (N)» o el trailer `SF-Tarea: N`) sin un revert posterior, y en En observación, en las que tienen commits en `develop`.
- **Quién:** panel con la R; principal si se lo piden o si hay choques.
- **Autorización:** dos clics: el primero cambia la R por «R eliminar» y «R pendiente»; el segundo, en uno de ellos, revierte y elige el destino. A los 5 s, o con un clic en otro sitio, vuelve a ser la R. O la petición del propietario, que dice el destino.
- **Repositorio:** `git switch develop` si hace falta; `git revert --no-edit <commits>`, el más reciente primero; sin push. Los commits salen del historial (`cerrada`, `a-observacion`); en una tarea sin historial, de los de `develop` con su número («… (N)» o `SF-Tarea: N`); o de `--commit`. Con choques, `git revert --abort`, vuelta a la rama de antes, la cola sin tocar y prompt a Claude. Si ya estaba en `main`, llega en la versión siguiente.
- **Panel:** eliminada, desaparece y no entra en Cerradas; pendiente, vuelve a Pendientes con H y sale en Cerradas como cualquier reabierta, en rojo con su H. Historial: `revertida` y después `eliminada` (con `en-cola` en su detalle) o `reabierta` (con `revertida`).
- **Rama:** en los dos destinos la tarea sale sin rama, y todo limpio para volver a ponerla en curso: si la suya aún existe (no se pudo borrar en el squash), se borra; con commits que nunca entraron en `develop`, u ocupada en otro worktree, queda en git y se avisa. Lo que quede del subagente se recoge (169, 170).
- **CLI:** `cola.py revertir 117 --eliminar | --pendiente [--commit <hash> …]`; el destino es obligatorio. `cola.py restaurar 117` devuelve una eliminada así en cola y reabierta.
- **Sale de:** 078, 107, 115 (4, 18), 134.

#### 27 · Reabrir

- **De → a:** `en-observacion`, `descartada` o fuera de la cola (cerrada, revertida) → `en-curso` o `en-cola`, con su número y `reabierta: true`; los pasos de cierre, pendientes (en curso, los que falten se añaden, 174). Una eliminada se restaura (28); una absorbida, con `/desfusionar` (30). Revertir con «R pendiente» ya la reabre en cola (26).
- **Cuándo:** al probarla o al observarla hay que corregirla, o aparece un bug atribuible a ella.
- **Quién:** principal.
- **Autorización:** ninguna; el bug entra en la cola antes de investigarlo. Una modificación durante la prueba la hace el subagente de la tarea; si ya se paró, se lanza otro.
- **Repositorio:** antes, limpia lo que quedara del subagente anterior, también con cambios sin commit (`git worktree remove --force`), sin avisar: un worktree viejo no se reutiliza nunca (169). En curso, una rama nueva desde `develop`, con el nombre de la anterior o el de `--rama`; en cola, sin rama hasta empezarla (05).
- **Panel:** Cerradas, con su código en rojo y H.
- **CLI:** `cola.py reabrir 66 "qué falla" [--en-cola] [--rama nombre] [--sin-activar]`.
- **Sale de:** 061, 064, 069, 096, 083, 115 (6, 7), 149, 151.

#### 28 · Eliminar (E)

- **De → a:** `en-cola` o `en-curso` sin rama → fuera de la cola y de la vista; su historial, a `.sf/historial.jsonl`.
- **Cuándo:** la tarea no ha cambiado ningún activo.
- **Quién:** panel con la E; principal, que comprueba que no tiene rama.
- **Autorización:** dos clics, o la petición del propietario.
- **Repositorio:** nada.
- **Panel:** desaparece; no entra en Cerradas; su número no se reutiliza.
- **CLI:** `cola.py eliminar 87`; `cola.py restaurar 87` la devuelve a la cola, con su estado.
- **Sale de:** 079, 089, 115 (3, 8).

#### 28 bis · A propuesta

- **De → a:** `en-cola` sin rama → fuera de la cola, como eliminada, y de vuelta en `sf/propuestas.md`: lo contrario de «A Pendientes» en Propuestas.
- **Cuándo:** la tarea aún no está decidida: vuelve a ser una propuesta por aprobar.
- **Quién:** panel con «A propuesta», en Pendientes, en cualquier proyecto que lleve `sf/propuestas.md` (o el `docs/propuestas.md` de antes) con «Propuestas pendientes»; principal.
- **Autorización:** dos clics («¿A propuesta? sí»), o la petición del propietario.
- **Repositorio:** `sf/propuestas.md` (o `docs/propuestas.md`, mientras el proyecto no se ha puesto al día). Si la tarea salió de una propuesta (su «Estado» dice «pasada a la tarea N de la cola», o sin número y con su mismo título), vuelve a «propuesta, pendiente de aprobación»; si no, una nueva al final de «Propuestas pendientes», con el primer número libre, su título, su tipo, su descripción como «Cambio propuesto» y su origen. Sin ese archivo o esa sección, no hace nada: no lo crea. `docs/propuestas.md` vive en `develop`: el cambio va con su propio commit en `develop` («P08 vuelve a propuesta desde la tarea 87 de la cola»), también con otra rama activa, sin cambiar de rama ni tocar su copia de trabajo, que quedaría con cambios sin commit e impediría cerrar su tarea. No lo hace si `develop` está en otro worktree o, siendo la activa, el archivo tiene cambios sin commit. Sin git o sin `develop`, solo escribe el archivo y lo avisa (tarea 273).
- **Panel:** desaparece de Pendientes; no entra en Cerradas; la propuesta sale en Propuestas (la última sección del panel, tras Cerradas), que con otra rama activa lee las propuestas de `develop`. `restaurar` no la devuelve: la propuesta manda.
- **CLI:** `cola.py a-propuesta 87`; la respuesta JSON lleva `propuesta` (P<nn>).
- **Sale de:** la tarea 243.

### Juntar y separar

#### 29 · Fusionar

- **De → a:** varias en `en-cola` o `en-curso` → queda la de número más alto (en curso si alguna lo estaba, con los pasos de cierre una vez y al final, 174); las demás, absorbidas, fuera de la cola.
- **Cuándo:** dos tareas tratan lo mismo. El principal lo sugiere con la orden lista y, a continuación, propone redescribir la tarea resultante (`/sf_redescribir`) (141).
- **Quién:** panel con `/sf_fusionar`; el principal, con `cola.py fusionar`, en la excepción de los documentos.
- **Autorización:** la escribe el propietario. Excepción: dos tareas de actualizar el mismo documento las fusiona el principal directamente (142).
- **Repositorio:** la que queda se lleva la rama de destino: la suya, o si no tiene, la que contiene a las demás. Las otras ramas, integradas en ella o ya inexistentes, se borran. Rechaza si alguna tiene commits fuera de la de destino (integrarla antes), o si una que se borraría está en otro worktree o es la activa. El subagente de cada absorbida se recoge si su worktree está limpio y su `sub-NN` ya está en la de destino; si no, se queda y se avisa. La que queda conserva el suyo (169).
- **Panel:** la que queda, con los pasos de todas; las otras desaparecen sin cerrarse. Historial: `fusion` en la que queda, `absorbida` en las otras.
- **CLI:** `cola.py fusionar 104 105`.
- **Sale de:** 098, 099, 100, 141, 142 y la tarea «fusionar no admite dos tareas con rama aunque una ya esté integrada en la otra» (227).

#### 30 · Deshacer una fusión o una eliminación

- **De → a:** fuera de la cola → `en-cola` o `en-curso`, con su letra de antes. Una eliminada al revertirla («R eliminar»), en cola y reabierta, con H (134).
- **Cuándo:** una absorbida o eliminada vuelve a la cola.
- **Quién:** principal; panel con `/desfusionar`.
- **Autorización:** la del propietario.
- **Repositorio:** nada.
- **Panel:** sin pasar por Cerradas; conserva A o H.
- **CLI:** una eliminada, `cola.py restaurar 87`, desde el historial; una fusión, `/desfusionar` (tarea 135, aún sin orden).
- **Sale de:** 115 (8).

#### 31 · Separar con /sf_split

- **De → a:** `en-cola` o `en-curso` con dos pasos de trabajo o más → la misma, sin esos pasos, y una nueva `en-cola`, sin rama, con esos pasos y el nombre del primero. Los de cierre no se separan: se quedan en la de origen (174).
- **Cuándo:** una tarea junta partes separables. El principal lo sugiere.
- **Quién:** panel con `/sf_split`.
- **Autorización:** la escribe el propietario.
- **Repositorio:** nada; el trabajo de un paso hecho sigue en la rama de origen.
- **Panel:** tarea nueva, con A; la de origen, con menos pasos. Historial: `separada` en la de origen, `nacida` en la nueva.
- **CLI:** `cola.py split 89 2,3`.
- **Sale de:** 097, 098, 100.

### Fuera de una tarea

#### 32 · Publicar

- **De → a:** sin cambio en la cola.
- **Cuándo:** el propietario lo pide.
- **Quién:** principal.
- **Autorización:** el OK del propietario.
- **Repositorio:** `develop` pasa a la rama que hace de `main` (`rama_main`), con el tag `vX.Y.Z`, que es la fuente de la versión; la `version` de cada `manifiesto` de la configuración (en la SF, su `plugin.json`) se sube solo entonces, en un commit `vX.Y.Z` (en la SF, `sf X.Y.Z`); push al `remoto` (decisión 226).
- **Panel:** nada.
- **CLI:** fuera de la cola; candidato a otro comando.
- **Sale de:** 082.

#### 33 · Recuperar una copia

- **De → a:** la cola entera vuelve a una copia anterior.
- **Cuándo:** una escritura ha roto o perdido tareas.
- **Quién:** principal o propietario.
- **Autorización:** la del propietario.
- **Repositorio:** nada (la cola está fuera de git).
- **Panel:** relee la cola.
- **CLI:** `cola.py copias` las lista; `cola.py recuperar n` (o el nombre del archivo) pone una.
- **Sale de:** 113, 115 (12).

Son 34 cambios: 5 de alta y arranque, 7 durante el trabajo, 5 de prueba, 6 de cierre, 6 para deshacer, 3 de juntar y separar y 2 fuera de una tarea.

## 3. Formato de `.sf/peticiones.json`

Fuera de git. Lo escriben el principal y el panel, con el CLI; nunca un subagente, aunque el CLI no lo comprueba (110, 115).

### Raíz

- `ultimo`: el último número de tarea dado. Quien crea una tarea le da el siguiente y lo sube, porque las cerradas, eliminadas y absorbidas salen y sus números no se reutilizan.
- `peticiones`: la lista de tareas.

### Cada tarea

- `id` (número): su código.
- `texto`: el nombre, compacto, empieza por lo que cambia (040).
- `estado`: `en-cola`, `en-curso`, `en-observacion` o `descartada`; en `.sf/historial.jsonl`, el de salida.
- `descripcion`: detalles, sin origen ni autor (063, 098).
- `pasos`: lista de `{texto, estado}`, con estado `hecho`, `en-curso` o `pendiente`.
- `rama`: `feature/NN-nombre`, desde que se crea.
- `prueba`: qué debe comprobar el propietario.
- `observando`: `true` mientras el propietario la mira, en observación.
- `reabierta`: `true` si vuelve a la cola tras haber salido.
- `commit`: hash del squash o versión del cierre; lo pone `a-observacion` (o `reobservar`). La C guarda el commit en el historial y saca la tarea.

El panel ignora los pasos que no entiende y avisa de las tareas sin texto o con otro estado.

### `historial`

Lista de cambios, el más antiguo primero. La escribe el CLI en cada orden; nadie la edita a mano.

```json
"historial": [
  { "evento": "creada", "fecha": "2026-10-29T09:14:02+01:00", "quien": "principal", "via": "cli", "detalle": "en-cola" },
  { "evento": "en-curso", "fecha": "2026-10-29T09:20:11+01:00", "quien": "propietario", "via": "cli" },
  { "evento": "rama", "fecha": "2026-10-29T09:21:40+01:00", "quien": "principal", "via": "cli", "detalle": "feature/92-flujo-tareas" },
  { "evento": "subagente", "fecha": "2026-10-29T09:30:05+01:00", "quien": "principal", "via": "cli", "detalle": ".claude/worktrees/agent-… · feature/92-flujo-tareas-cli" },
  { "evento": "cerrada", "fecha": "2026-10-29T12:02:33+01:00", "quien": "propietario", "via": "panel", "detalle": "develop a1b2c3d" }
]
```

- `evento`: el nombre del cambio de la sección 2: `creada`, `en-curso`, `en-cola`, `rama`, `paso` (añadido, marcado o quitado), `renombrada`, `subagente`, `informe`, `listo`, `comprobado`, `probar` (Activar rama), `probar-fallido` (choques al integrar `develop`), `observando`, `seguir`, `cerrada` (también la de una en observación, con «en observación»), `cierre-fallido`, `push-fallido`, `recogida` (worktree y auxiliar quitados) o `recogida-con-avisos` (lo que quedó o se perdió), `a-observacion`, `reobservada`, `descartada`, `limpiada`, `revertida`, `reabierta`, `eliminada`, `a-propuesta` (con «P<nn> devuelta» o «P<nn> nueva»), `restaurada`, `absorbida`, `fusion` (en la que queda, con las absorbidas), `separada` (en la de origen) y `nacida` (en la nueva, con la de origen).
- `fecha`: ISO 8601 con zona.
- `quien`: `propietario` o `principal` (115, 10).
- `via`: `cli` o `panel`; distingue la C pulsada por el propietario de un cierre del principal.
- `detalle`: lo propio del evento (rama, «develop <hash>» de un squash o un revert, worktree, números de la fusión, motivo del fallo).

### `.sf/historial.jsonl`

Una línea JSON por tarea que sale de la cola (cerrada, limpiada, revertida, eliminada, absorbida), con todos sus campos y su historial. Su `estado` dice cómo salió:

- `cerrada`: por la C, sin rama o en observación (`cerrada`).
- `eliminada`: con la E, con «R eliminar» o con «A propuesta» (su último evento, `a-propuesta`); el evento `eliminada` guarda en `detalle` el estado de antes, el que le devuelve `restaurar` (tras un revert, `en-cola`, y vuelve reabierta).
- `absorbida`: por una fusión.
- `descartada`: limpiada tras descartarse.
- `revertida`: con la R, desde En observación o ya cerrada, antes de la decisión 134. Ahora la R la deja `eliminada` o la devuelve a la cola, sin línea nueva.

Si sale más de una vez, la última línea de su número manda. De aquí salen `reabrir`, `restaurar`, `revertir` y `ver`, y los números ya dados.

Con el historial, el panel deja de deducir (tarea 145): A si `creada` es posterior al inicio de la sesión; H en otro caso o con `reabierta`; Cerradas, las tareas con un evento de cierre en la sesión; ⚙, un `subagente` sin `informe` posterior.

## 4. Copias rotativas

Decisiones 113 y 115:

- **Dónde:** `.sf/copias/peticiones-AAAAMMDD-HHMMSS-mmm.json` (con milésimas, para que dos escrituras seguidas no choquen), fuera de git: `.sf/copias/`, `.sf/historial.jsonl` y `.sf/peticiones.lock` van al `.gitignore`.
- **Cuándo:** el CLI copia la cola entera justo antes de cada escritura, con la cola bloqueada por `.sf/peticiones.lock` (espera hasta 10 s; un bloqueo de más de 2 minutos se da por abandonado). Escribe en un temporal y lo pone en su sitio, para no dejar la cola a medias.
- **Cuántas:** las últimas 50; al pasar de ahí, se borra la más antigua.
- **Cómo se ve:** `cola.py copias` lista número (1, la más reciente), fecha, cantidad de tareas y qué cambió después (altas, bajas, cambios de estado y tareas que cambian).
- **Cómo se recupera:** `cola.py recuperar 3` (o con el nombre del archivo) copia antes la cola actual, que pasa a ser la copia 1 (`recuperar 1` deshace la recuperación), y después pone la elegida. El panel relee. No toca `.sf/historial.jsonl`.

Solo protege lo que escribe el CLI: una escritura a mano no deja copia. El panel también escribe con el CLI (145).
