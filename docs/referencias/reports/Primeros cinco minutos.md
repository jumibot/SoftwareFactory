---
antetitulo: Software Factory · Informe de diagnóstico · Noviembre 2026
lema: Lo que solo vale aquí, a la vista; // lo que bloquea, antes de la prueba.
subtitulo: Dónde se atasca un usuario nuevo al instalar el plugin sf, incorporar un proyecto y hacer su primera tarea, qué supone de esta máquina o del propietario, qué ha resuelto ya la 1.5.0 y qué decide el propietario antes de la prueba del colega.
version: Versión 1.1 · 02/11/2026
estado: Diagnóstico revisado con la 1.5.0 · Tarea 289
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
tipo: Informe de diagnóstico
pie: Primera tanda de la tarea «Primeros cinco minutos de un usuario nuevo con la SF» (289). Sale de leer plugins/sf en develop (sf 1.4.2), los README, el informe «Plugin en otros proyectos» (171) y el de «Incorporar sin cambiar el proyecto» (222, en su rama), y de un recorrido en una configuración desechable de Claude Code. La versión 1.1 lo revisa contra develop en la sf 1.5.0 («Implementar la configuración inicial», 193, y las decisiones 205-234) y prepara las decisiones del paso 6. La 1.0 está en _respaldo/. Espera la decisión del propietario.
---
# Primeros cinco minutos

## Resumen | Tres cosas bloquean; el resto confunde | Resumen {#resumen}

Un colega que siga hoy las instrucciones no llega a su primera tarea. Se para en tres sitios:

- **No puede instalar.** El repositorio `jumibot/SoftwareFactory` es **privado**: `claude plugin marketplace add` falla sin acceso, y la página da 404 sin sesión.
- **No puede abrir su primera tarea.** Sin rama `develop`, `cola.py rama` responde «No hay rama develop.», y la incorporación no crea ni git ni `develop`. Pasa en una carpeta vacía y en cualquier proyecto que solo tenga `main`.
- **En macOS o Linux, Claude no puede usar la cola.** La orden fija es `python …`. Si en esa máquina solo existe `python3`, falla cada orden de la cola. El panel prueba `python` y `python3`, pero Claude no.

Lo demás no impide avanzar, pero hace dudar. No hay guía para quien empieza, y el README raíz está escrito para el propietario. JKanban sale en la incorporación. Cerrar sin remoto da un aviso que no se entiende. La metodología sigue hablando del registro común y del kanban de la SF, ya retirados («Sin registro ni mejoras de la SF desde otros proyectos», 194).

Casi todo lo que solo vale en esta máquina ya lo inventarió «Plugin en otros proyectos» (171) con la 1.2.0. En la 1.4.2 sigue igual, salvo el registro de uso, que lo retiró la decisión 194.

> **Con la 1.5.0, de los tres bloqueos queda uno seguro y otro según el sistema del colega.** La incorporación ya crea git, `develop` y el remoto en GitHub, y el kanban es opcional y por defecto ninguno. Siguen el repositorio privado y la orden `python` fija. De los 18 atascos, cuatro quedan resueltos, seis a medias y ocho siguen; sale uno nuevo: sin GitHub y `gh` no hay SF.

[Ver la revisión](#revision){: .salto} · [Ver las decisiones](#decidir){: .salto}

## Recorrido | Qué se ha podido hacer y qué no | Recorrido {#recorrido}

Se ha recorrido el camino en una configuración desechable (`CLAUDE_CONFIG_DIR` en el scratchpad), sin tocar `~/.claude` ni los plugins instalados:

1. **Leer el README raíz** como quien no sabe nada. No dice cómo instalar: remite al «propietario» y a «Claude Code». Las órdenes de instalación están en el README del plugin, entre el mod y «Publicar un cambio».
2. **`claude plugin marketplace add jumibot/SoftwareFactory`.** Funciona solo con las credenciales del propietario. La primera vez falló con «Filename too long»: el catálogo clona el repositorio entero, y los nombres de `docs/decisiones/` llegan a 130 caracteres. Con `core.longpaths` (puesto solo en el entorno de la orden) clona bien.
3. **`claude plugin install sf@softwarefactory --scope user`.** Instala la 1.4.2 y sus tres dependencias, sin errores.
4. **Abrir una carpeta vacía.** El mod carga: copia `cola.py` y su lanzador a `$CLAUDE_CONFIG_DIR/sf`. La sesión no sigue: «Not logged in». **No se ha recorrido la conversación** (pantalla completa, petición de incorporar, menús, orquestación) porque iniciar sesión en la configuración desechable necesita al propietario.
5. **Primera tarea sin Claude**, con `cola.py` sobre dos carpetas: una sin git y otra con git y solo `main`. En las dos, `crear --en-curso` funciona y `rama` se para en «No hay rama develop.». Con `develop` creada a mano, el ciclo llega a cerrar. El cierre avisa así: «Aviso: falta el push de develop (and the repository exists.)». Es la última línea del error de git, que sin remoto no se entiende. El commit lleva `Co-Authored-By: Claude Opus 5.5`, sea cual sea el modelo del colega.

## Atascos | Por gravedad, con el arreglo propuesto | Atascos {#atascos}

### Bloquean {#bloquean}

| Atasco | Dónde | Arreglo propuesto |
| --- | --- | --- |
| *Sigue en la 1.5.0.* **1. Repositorio privado.** Sin acceso, el catálogo no se añade. | GitHub `jumibot/SoftwareFactory` | Decide el propietario: hacerlo público, invitar al colega (con `gh auth login` para que git clone por HTTPS) o crear un repositorio público solo de distribución. |
| *Resuelto en la 1.5.0.* **2. Sin `develop` no hay primera tarea.** La incorporación no hace `git init` ni crea `develop`. | `tools/cola.py` (`rama`); `skills/incorporar_proyecto_a_sf/SKILL.md` | Para la prueba basta lo mínimo. En el caso nuevo, `git init`, `main` con un primer commit y `develop` desde ella. En un proyecto existente sin `develop`, crearla desde `main`. Choca con la pregunta de ramas de «Incorporar sin cambiar el proyecto» (222), que propone no crear `develop`: lo decide la 222, o se acepta como arreglo provisional. |
| *Sigue en la 1.5.0.* **3. `python` fijo en la orden de la cola.** En macOS y Linux suele haber solo `python3`. En Windows, `python` puede ser el atajo de la Microsoft Store. | `hooks/constantes.ts`, 32 (`ORDEN_COLA`); `skills/flujo_tareas/SKILL.md` | El panel ya sabe qué intérprete responde (`hooks/cola.ts`, 103). La orden que se da a Claude podría usar ese mismo, o ir a un lanzador `sf-cola` que lo elija. Si el colega usa Windows con Python instalado, no bloquea: basta decirlo en la guía. |

### Confunden {#confunden}

| Atasco | Dónde | Arreglo propuesto |
| --- | --- | --- |
| *Sigue en la 1.5.0.* **4. No hay guía de arranque.** El README raíz da un estado viejo («sf 0.13.1»; va por la 1.4.2) y lo primero que enseña es el aviso de actualizar desde la 1.2.10. Las órdenes de instalación están junto a lo que solo sirve a quien desarrolla la SF. | `README.md`; `plugins/sf/README.md` | El paso 7: la guía de arranque. En el README raíz, un apartado «Probar la SF» que la enlace, y el aviso de la 1.2.10 más abajo. Al publicar, poner al día el estado. |
| *Sigue en la 1.5.0.* **5. Requisitos sin decir.** Una versión reciente de Claude Code con mods (probada la 2.1.316), git con `user.name` y `user.email`, Python 3.10 o posterior (por los tipos `str \| None` de `cola.py`), la pantalla completa (`/tui fullscreen`) para que el panel reciba clics y reiniciar tras instalar. | — | En la guía, como lista de comprobación previa. |
| *Resuelto en la 1.5.0.* **6. JKanban en la incorporación.** Se pregunta `kanban` y la comprobación final lo exige. La descripción «la leen el panel, Claude Code Commander y JKanban». La `description` de la skill nombra «proyecto en JKanban». | `skills/incorporar_proyecto_a_sf/SKILL.md`, 3, 29, 31, 71, 83 | Dejar `kanban` como opcional y no preguntarlo, como propone «Configuración inicial» (190). Para la prueba basta quitarlo de la pregunta y de la comprobación final, y decir «la lee el panel». Esta tanda no toca la skill: se hace con la 222 o la 193, o en el paso 2 de esta. |
| *A medias en la 1.5.0.* **7. Push sin remoto.** El cierre avisa «falta el push de develop (and the repository exists.)». El panel cuenta un push pendiente que nunca se hará. | `tools/cola.py`, 435; `hooks/lectura.ts`, 170-180 | Sin remoto, no hacer push ni avisar de él. Ya está como paso de «Implementar la configuración inicial» (193): «Hacer push al remoto del proyecto…». Además, que el motivo cite la primera línea del error de git, no la última. |
| *Sigue en la 1.5.0.* **8. Enlaces de la metodología a un repositorio privado.** Unos diez enlaces a decisiones, propuestas y la especificación dan 404. | `skills/metodologia/references/*.md`; `skills/orquestacion/references/porque.md` | Se resuelve con el atasco 1. Si el repositorio sigue privado, que el texto se entienda sin abrir el enlace. |
| *Sigue en la 1.5.0.* **9. La metodología contradice la decisión 194.** Siguen el «Registro de uso» en el registro común de la SF y su bloque SF ENHANCE (sección 2), las mejoras «en SoftwareFactory» (7.6) y la automejora con el kanban de la SF (11). El Claude del colega podría intentar escribir en la SF. | `skills/metodologia/references/desarrollo-de-proyectos.md`, 62, 380, 504-508 | En la tarea «Actualizar las reglas del método» (208); texto propuesto en el informe de la tanda. La plantilla y `metodologia/SKILL.md` ya siguen la 194. |
| *A medias en la 1.5.0.* **10. Ejemplos con LecturaFàcil y `kanban`.** El panel de una carpeta sin SF propone un `proyecto.json` de ejemplo con `"kanban": "LecturaFàcil"`. Lo mismo pasa en el README del plugin y en la skill, con `"sf": "0.29.0"`. | `hooks/constantes.ts`, 61-65; `plugins/sf/README.md`, 17-24; skill de incorporación, 35-42 | Un ejemplo neutro («MiProyecto»), sin `kanban` y con la versión actual o `<versión>`. Va al paso 1. |
| *A medias en la 1.5.0.* **11. Todo en español.** Panel, mensajes de `cola.py`, skills y reglas. | Todo el plugin | Decide el propietario según quién sea el colega. Para esta prueba, se supone que lee español. |

### Menores {#menores}

| Atasco | Dónde | Arreglo propuesto |
| --- | --- | --- |
| *Sigue en la 1.5.0.* **12. Rutas de esta máquina.** `claude --plugin-dir D:/Projectes/SoftwareFactory/plugins/sf`; el catálogo local en `D:/Projectes/.claude-plugin/`. El modo prueba reconoce la SF por el nombre de su carpeta. | `plugins/sf/README.md`, 68; `hooks/prueba.ts`, 13 y 103 | `<repositorio de la SF>/plugins/sf` en el README y el comentario sin ruta (paso 1). El modo prueba solo afecta a quien desarrolla la SF. |
| *A medias en la 1.5.0.* **13. Firma fija del cierre.** `COAUTOR = 'Co-Authored-By: Claude Opus 5.5 …'`. | `tools/cola.py`, 74 | Quitar el modelo fijo: firma configurable o ninguna (171, pregunta 4, sin decidir). |
| *A medias en la 1.5.0.* **14. Historia del propietario en el plugin.** Ocho `ORIGIN.md` con rutas `D:/` y proyectos suyos. El kit de documentos menciona OncoCore en sus comentarios. `documento_fundacional` toma como modelo un archivo de SmartColdBox que el colega no tiene. | `skills/*/ORIGIN.md`; `tools/kit_documentos/*`; `skills/documento_fundacional/SKILL.md`, 27; `skills/documento_vision/SKILL.md`, 313 | Paso 1: los `ORIGIN.md` de las skills propias, a `docs/referencias/` de la SF, y en el plugin solo la licencia de lo de terceros. Sacar OncoCore de los comentarios. En el fundacional, el modelo solo «si está disponible», con las reglas escritas en la skill. |
| *Sigue en la 1.5.0.* **15. Rutas largas en Windows.** El catálogo clona el repositorio entero, con `docs/`, `_respaldo/` y los html. Con un perfil de usuario de nombre largo, o una carpeta de configuración profunda, falla con «Filename too long». | `docs/decisiones/` (nombres de hasta 130 caracteres) | En la guía: `git config --global core.longpaths true` si falla. Más adelante, un catálogo más ligero o nombres de decisión más cortos. |
| *Resuelto en la 1.5.0.* **16. La orden de la cola usa `$HOME/.claude`** aunque haya `CLAUDE_CONFIG_DIR`. Sin `~/.claude/sf/cola.py`, falla. En esta máquina no se nota porque existe el del propietario. | `hooks/constantes.ts`, 32 | Solo afecta a configuraciones aparte, como la del ensayo del paso 8. Para que el ensayo sea fiel, hacerlo con un `HOME` (o `USERPROFILE`) desechable, no solo con `CLAUDE_CONFIG_DIR`. |
| *Resuelto en la 1.5.0.* **17. El plugin publicado lleva `tests/`**, con rutas y nombres de prueba (`D:/sf`, JKanban). | `plugins/sf/tests/` | Dejar: Claude no los carga. |
| *A medias en la 1.5.0.* **18. `dataviz`** no es un plugin: la trae el entorno de claude.ai. En Claude Code a secas puede faltar. | README raíz; `skills/documento_vision/SKILL.md` | La skill ya dice qué hacer si falta. Basta mencionarlo en la guía. |

## Revisión | Qué resolvió la 1.5.0 y qué queda | Revisión {#revision}

Revisado leyendo `plugins/sf` en develop (sf 1.5.0), sin sesión y sin tocar otros proyectos ni `~/.claude`. «Resuelto» quiere decir resuelto en el plugin; lo que depende de la conversación queda por ver en el recorrido con sesión (paso 5).

### Resueltos {#resueltos}

| Atasco | Qué lo resuelve | Qué mirar en el recorrido |
| --- | --- | --- |
| **2. Sin `develop`** | La incorporación propone `git init -b main` si no hay repositorio, pregunta si crear `develop` y, si el desarrollador se niega, explica y pide reconfirmar (205, 214). Si `main` o `develop` solo están en el remoto, crea la local sin preguntar (234). | En una carpeta vacía no hay «lo que ya hay» para el primer commit de `main`: ver cómo lo resuelve Claude (commit vacío o el de la incorporación) antes de crear `develop`. |
| **6. JKanban** | `kanban` es opcional y por defecto «Ninguno» (224); la comprobación final no lo exige. | Residuo: «la leen el panel, Claude Code Commander y el kanban» (skill de incorporación, 77) nombra una herramienta del propietario. Va con el 14. |
| **16. `$HOME/.claude` con `CLAUDE_CONFIG_DIR`** | El lanzador real pasa la orden a la copia de la sesión (190). Un usuario nuevo no usa `CLAUDE_CONFIG_DIR`. | Solo afecta al ensayo: hacerlo con un `HOME` desechable, como ya decía el atasco. |
| **17. `tests/` en el plugin** | Se deja: Claude no los carga. | — |

### A medias {#a-medias}

| Atasco | Qué resolvió la 1.5.0 | Qué queda |
| --- | --- | --- |
| **7. Push sin remoto** | Sin remoto en GitHub no hay SF (230): la incorporación lo comprueba y ofrece crearlo con `gh`; el cierre, `decision --push` y RELEASE hacen push al `remoto` configurado. Ya no hay proyectos sin remoto. | El motivo del aviso sigue siendo la última línea del error de git (`tools/cola.py`, `motivo`, 511 y 1552). Arreglo pequeño, en el paso 2: citar la primera línea con `fatal:` o `error:`. |
| **10. Ejemplos** | El ejemplo del panel ya no lleva `kanban` y da la versión actual. | Sigue `LecturaFàcil` en el ejemplo del panel (`hooks/constantes.ts`, 85-96), con la versión «1.5.0» escrita a mano, que envejece. El README del plugin enseña la configuración completa: ahí el ejemplo sirve. Paso 1: «MiProyecto» en el panel. |
| **11. Idioma** | Claude escribe en el idioma del proyecto y del desarrollador (206), guardado en `idioma` y preguntado al incorporar. | Los textos fijos (panel, mensajes de `cola.py`, skills, reglas) siguen en español; la 206 deja ese atasco aquí. Decisión 3. |
| **13. Firma del cierre** | `encargo` y `decision` aceptan `--coautor` o la clave `coautor` de `.sf/proyecto.json`. | El squash del cierre sigue con `COAUTOR` fijo, «Claude Opus 5.5» (`tools/cola.py`, 80 y 191-196). Decisión 4. |
| **14. Historia del propietario** | La 1.5.0 no lo toca. | Siguen los siete `ORIGIN.md` de las skills propias, OncoCore en el kit de documentos y el modelo de SmartColdBox en el fundacional, y se suma la mención a Claude Code Commander del 6. Paso 1, sin decisión. |
| **18. `dataviz`** | La skill de visión dice qué hacer si falta. | Mencionarlo en la guía (paso 7). |

### Siguen {#siguen}

| Atasco | Estado en la 1.5.0 | Cómo se sigue |
| --- | --- | --- |
| **1. Repositorio privado** | `jumibot/SoftwareFactory` sigue privado. | Decisión 1. |
| **3. `python` fijo** | `ORDEN_COLA` sigue siendo `python -I -X utf8 "$HOME/.claude/sf/cola.py"` (`hooks/constantes.ts`, 32), y así la dan `sf:flujo_tareas` y `sf:orquestacion`. El panel sí prueba `python` y `python3` (`hooks/cola.ts`, 105 y 137). | Decisión 2. |
| **4. Guía de arranque** | El README raíz sigue en «27 de octubre de 2026, sf 0.13.1», con el aviso de la 1.2.10 delante. | Paso 7. |
| **5. Requisitos** | Sin lista. Se suman una cuenta de GitHub y `gh` con la sesión iniciada (atasco 19). | Paso 7, en la lista previa de la guía. |
| **8. Enlaces a un repositorio privado** | Sin cambios. | Con la decisión 1. |
| **9. Metodología y 194** | Sigue el «Registro de uso» en el registro común de la SF (`desarrollo-de-proyectos.md`, 62) y lo demás. | En «Actualizar las reglas del método» (208, en cola). Decisión 5. |
| **12. Rutas de esta máquina** | Siguen en el README del plugin (77) y en el comentario de `hooks/prueba.ts` (14). | Paso 1, sin decisión. |
| **15. Rutas largas en Windows** | El nombre de decisión más largo tiene 114 caracteres. | En la guía (paso 7). |

### Nuevo {#nuevo}

| Atasco | Dónde | Arreglo propuesto |
| --- | --- | --- |
| **19. Sin GitHub y `gh` no hay SF.** El colega necesita una cuenta de GitHub. Si su proyecto no tiene remoto, la incorporación ofrece crearlo con `gh`; sin `gh` instalado y con la sesión iniciada, se para y espera (230). En una carpeta vacía, la primera tarea pasa por crear un repositorio en GitHub. | `skills/incorporar_proyecto_a_sf/SKILL.md`, paso 2 | En la guía, como requisito: `gh` instalado y `gh auth login` hecho antes de empezar. Dónde prueba el colega, en la decisión 7. |

## Inventario | Lo que solo vale aquí o para el propietario | Inventario {#inventario}

Búsqueda en `plugins/sf/` (sin `tests/`) de rutas `D:`/`C:`, `Projectes`, el usuario y el correo, los proyectos del propietario, JKanban, Commander, Windows, PowerShell y Python. No aparecen ni el usuario de Windows ni el correo. Lo que sale:

- **Para la prueba** (pasos 1 y 2): los atascos 2, 3, 6, 7, 10 y 12.
- **Ruido, no bloquea:** los atascos 13, 14 y 17.
- **Identidad de la distribución, se deja:** `jumibot` como autor y dueño del catálogo, `sf@softwarefactory`, «SoftwareFactory» en morado para la propia SF.
- **Windows:** el mod ya distingue Windows de los demás sistemas (`hooks/cola.ts`, 115) y prueba `python` y `python3`. Lo que solo funciona en Windows es la orden de Claude (atasco 3).
- **MCP propios:** el plugin no declara ninguno. JKanban aparece solo como texto (atascos 6 y 10, y la metodología).

## Otras tareas | Qué ya está en marcha | Otras {#otras}

- **«Incorporar un proyecto sin cambiarlo» (222)** y **«Configuración inicial» (263)**: cerradas, en observación. Decidieron `develop` siempre (205, 214), el kanban opcional (224), el idioma (206) y el remoto en GitHub (230).
- **«Implementar la configuración inicial» (193)**: cerrada, en observación; es la sf 1.5.0. Resuelve los atascos 2 y 6 y casi todo el 7.
- **«Poner un proyecto al día con la SF sin tarea» (288)**: en observación. El caso «actualizar» no afecta a un usuario nuevo.
- **«Actualizar las reglas del método» (208)**: en cola. Lleva la metodología y la decisión 194 (atasco 9).
- **«Skill y orden de barra para cambiar la configuración del proyecto» (299)**: en curso. Un usuario nuevo no la necesita en sus cinco minutos.

## Decidir | Lo que decide el propietario (paso 6) | Decidir {#decidir}

Siete decisiones, por orden de importancia. Las dos primeras dicen si la prueba es posible.

::: tarjetas 2 plegables

### 1 · Acceso al repositorio (atasco 1, y con él el 8) {: #d1}

Opción A
:   Hacerlo público. Antes, repasar `docs/`, `_respaldo/` y el historial, que pasan a ser públicos.

Opción B
:   Invitar al colega como colaborador. Necesita `gh auth login` para que git clone por HTTPS.

Opción C
:   Un repositorio público solo para distribuir el plugin.

Recomendación
:   **B** para la prueba. Con la 230 el colega ya necesita una cuenta de GitHub y `gh` con la sesión iniciada, así que invitarlo no le pide nada más. A, cuando se haya repasado qué se hace público y limpiado la historia del propietario (atasco 14).

### 2 · Sistema del colega y la orden `python` (atasco 3) {: #d2}

¿Windows, macOS o Linux? En Windows con Python instalado no bloquea. En macOS y en muchas Linux solo hay `python3`, y cada orden de la cola falla.

Opción A
:   El mod da la orden con el intérprete que ya detecta el panel: la línea de convenciones que entrega dice cuál usar, y la orquestación manda esa sobre la fija.

Opción B
:   La guía pide que `python` responda (en Debian y Ubuntu, `python-is-python3`; en macOS, un alias), sin tocar el plugin.

Opción C
:   Cambiar la orden fija a `python3`, que rompería Windows.

Recomendación
:   Preguntar el sistema primero. Si es Windows, **B** basta para la prueba. Si no, **A**, en el paso 2: se cumple con el mod y no con la memoria del colega.

### 3 · Idioma de los textos fijos (atasco 11) {: #d3}

Claude ya escribe en el idioma del proyecto (206). El panel, los mensajes de `cola.py` y las skills siguen en español.

Opción A
:   Dejarlos en español.

Opción B
:   Traducir el panel y los mensajes de `cola.py` según `idioma`, con una tabla es/en.

Opción C
:   Solo la guía en el idioma del colega; lo demás, en español.

Recomendación
:   Preguntar si el colega lee español. Si lo lee, **A**, y B como propuesta para más adelante. Si no, **C** para esta prueba y B como tarea propia: traducir skills y reglas no cabe en esta.

### 4 · Firma del cierre (atasco 13) {: #d4}

El squash del cierre firma siempre «Claude Opus 5.5», sea cual sea el modelo del colega. Es la pregunta 4 de la 171, sin decidir.

Opción A
:   `cerrar` acepta `--coautor`, como `encargo` y `decision`, o toma la clave `coautor` de `.sf/proyecto.json`. Sin ninguna, el squash no lleva la línea. La orquestación le pasa la línea de la sesión.

Opción B
:   Lo mismo, pero sin ninguna se queda la línea fija de ahora.

Opción C
:   Sin coautoría en el squash.

Recomendación
:   **A.** Nunca firma con un modelo que no es, y en los proyectos del propietario no cambia nada si la orquestación pasa la línea.

### 5 · La metodología y la 194 antes de la prueba (atasco 9) {: #d5}

La metodología sigue mandando anotar en el registro común de la SF. El Claude del colega podría intentar escribir en un repositorio que no tiene.

Opción A
:   Hacer antes de la prueba al menos el «Reflejar» de la 194 en la 208.

Opción B
:   Dejarlo para cuando toque la 208.

Recomendación
:   **A** si el colega incorpora con metodología; si la apaga (`metodologia: false`), puede esperar.

### 6 · Recorrido con sesión real (paso 5) {: #d6}

Sin sesión no se ha visto la conversación: la incorporación con sus tres menús, la creación del remoto y la primera tarea.

Opción A
:   El propietario inicia sesión una vez en un `CLAUDE_CONFIG_DIR` y un `HOME` desechables, y el recorrido se hace ahí.

Opción B
:   Dejar la conversación para el ensayo del paso 8.

Recomendación
:   **A.** Los atascos de los menús y del remoto solo salen con sesión, y mejor ahora que en el ensayo.

### 7 · Dónde hace el colega su primera tarea (atasco 19) {: #d7}

Opción A
:   En una carpeta vacía: la incorporación crea git, `develop` y un repositorio privado en su cuenta de GitHub.

Opción B
:   En un proyecto suyo que ya tenga remoto en GitHub.

Recomendación
:   **A.** Recorre el camino más largo (git, `develop` y remoto) y no toca nada suyo. Para que quepa en cinco minutos, `gh` tiene que estar listo antes (guía).

:::

**Qué se arregla antes de la prueba.** Con lo anterior, la propuesta es: los atascos 1 y 3, según las decisiones 1 y 2; la guía con el 4, el 5, el 15, el 18 y el 19 (paso 7); los residuos del 7 y del 10, el 12 y el 14 con la mención a Commander (pasos 1 y 2); el 13, según la decisión 4, y el 9, según la 5. Lo demás, después.

## Prueba | Qué mirar cuando se recorra con sesión | Prueba {#prueba}

En una configuración desechable (`CLAUDE_CONFIG_DIR` y `HOME` en una carpeta temporal), con el plugin instalado desde el catálogo publicado:

1. **Arranque en una carpeta vacía.** El panel dice «Sin SF» y propone «incorpora este proyecto a la SF». Mirar si se abre solo o hay que activar la pantalla completa, y qué entiende de eso alguien nuevo.
2. **«Incorpora este proyecto a la SF».** Mirar los tres menús (identidad, repositorio y convenciones), que el kanban salga como «Ninguno» por defecto, cómo resuelve el primer commit de una carpeta vacía, si crea git, `develop` y el remoto con `gh`, y si el color y el nombre se aplican sin `/color` ni `/rename`.
3. **Primera tarea («añade un README»).** Mirar si va a la cola, si se crea su rama, si lanza un subagente con su worktree, si cierra con el push al remoto y con qué firma.
4. **Cuánto tarda y cuántas preguntas hace** antes de que el colega vea su primera tarea hecha: es la medida de los cinco minutos.
