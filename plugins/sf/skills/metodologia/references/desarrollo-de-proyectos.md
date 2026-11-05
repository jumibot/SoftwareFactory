# Metodología de desarrollo de proyectos

Estado del documento: **borrador de trabajo**, pendiente de revisión y aprobación como documento completo.

## Cómo interpretar este documento

- **Acuerdos:** principios y dinámica decididos por el propietario. Su porqué está en las [decisiones de la SF](https://github.com/jumibot/SoftwareFactory/tree/main/docs/decisiones).
- **Preferencias:** opciones favoritas que deben confirmarse para cada proyecto.
- **Pendientes:** decisiones que faltan, reunidas al final.
- **Ejemplos:** empiezan por «Ejemplo:» e ilustran una regla; no mandan nada.

Lo que aún no está decidido no está aquí: vive en las [propuestas](https://github.com/jumibot/SoftwareFactory/blob/main/docs/propuestas.md). Las estructuras de carpetas de los perfiles son plantillas adaptables del plugin `sf` («Estructuras de código»): crear únicamente lo necesario.

Este documento define cómo se quieren construir las aplicaciones con Claude Code: desde la visión hasta la entrega, mediante devslices preparadas, pruebas y seguimiento permanente.

Es la referencia del método. La [especificación de la Software Factory](https://github.com/jumibot/SoftwareFactory/blob/main/docs/specs/funcional/software-factory.md) define las herramientas, skills y distribución necesarias para aplicarlo. Los cambios de instalación o distribución no alteran por sí mismos esta metodología.

## 1. Principios acordados

- Comprender el proyecto globalmente antes de iniciar su implementación, especialmente cuando empieza de cero.
- Diseñar el comportamiento funcional y la interfaz antes de elegir y concretar la solución técnica.
- Construir por incrementos verticales de construcción, denominados **devslices**. No son la lista de funcionalidades: las funcionalidades se definen en la especificación funcional.
- Preparar cada devslice antes de desarrollar: afinar especificación, diseñar, preparar la verificación y crear sus tareas.
- Preferir empezar la implementación de cada devslice por lógica y datos/backend, continuar por la interfaz y verificar el recorrido completo.
- Crear pruebas antes del código cuando sea viable y revisar que representan los requisitos.
- Ajustar arquitectura, documentación y comprobaciones a la complejidad real.
- Todo proyecto se instala de forma sencilla: un solo paso documentado, dependencias con versión fijada, configuración fuera del código y base de datos creada por sus migraciones.
- Usar nombres comprensibles. Evitar identificadores visibles poco mnemónicos como `DS001`.
- **Comandos antes que inferencia:** lo que se pueda hacer con un comando (git, escribir la cola, generar un documento) se hace con el comando, sin pasar por Claude; Claude entra donde hace falta criterio. Un botón del panel ejecuta él mismo su orden y, si el caso pide criterio, dice por qué y no hace nada (acuerdo del propietario, 2026-10-29).
- Mantener el kanban actualizado como referencia del estado del trabajo.
- Registrar decisiones duraderas y evidencias suficientes, evitando duplicaciones y documentación ceremonial.
- La SF define el método; las técnicas se reutilizan. Cómo especificar una interfaz, registrar una decisión, probar o revisar se toma de lo que ya existe (skills y marcos de terceros) y se adapta al método, sin adoptar su flujo. Solo se crea técnica propia cuando no hay equivalente.
- Cada proyecto usa solo las capacidades que necesita. Agente de IA como componente, brain de desarrollo, KB operativa, API separada o interfaz web son opcionales y se deciden en la definición técnica.

## 2. Qué pertenece a cada proyecto consumidor

Cada aplicación conserva su propia visión, especificaciones, diseño, decisiones, código y pruebas. También mantiene su selección de perfil técnico y las excepciones a las preferencias de la SF.

La SF aporta el procedimiento y las herramientas; el proyecto aporta su contenido y contexto concreto.

Un proyecto está bajo la SF cuando tiene (acuerdo del propietario, 2026-10-27):

- `.sf/proyecto.json` en la raíz, con su identidad y su configuración («Estructura documental común», más abajo);
- un repositorio git con `develop`, su rama de publicación (`main`) y un remoto en GitHub;
- la carpeta `sf/`, con los documentos de la SF en el proyecto: sus propuestas, sus decisiones y los informes que escribe Claude;
- si sigue la metodología, una **guía de instalación desde cero** (`docs/guias/instalacion.md`) y una **guía de actualización** (`docs/guias/actualizacion.md`), que permiten instalar el proyecto en un equipo nuevo y pasarlo de una versión a la siguiente sin ayuda de quien lo hizo (acuerdo del propietario, 2026-10-27);
- el plugin `sf` activo: se instala una vez para el usuario desde el catálogo de la SF publicado en GitHub, nunca desde la carpeta de trabajo de la SF.

La metodología es opcional. Sin ella, el proyecto usa solo las tareas, el repositorio y las decisiones de la SF, sin fases ni documentos del método (acuerdo del propietario, 2026-10-30).

**Las reglas las entrega el mod** (acuerdo del propietario, 2026-11-01). El `CLAUDE.md` del proyecto no lleva ninguna línea de la SF: es solo para lo propio del proyecto.

Al empezar la sesión, tras `/clear` y tras compactar, el mod de la SF entrega como contexto las reglas comunes (plantilla `templates/claude-sf.md` del plugin) y, si el proyecto sigue la metodología, las del método (`templates/claude-sf-metodologia.md`). Entrega también una línea con las convenciones del proyecto y el texto entero de la skill `sf:orquestacion`. Siempre en la versión instalada, sin copias que regenerar.

Un proyecto que aún importa la copia antigua (`@.sf/claude-sf.md` en su `CLAUDE.md`) va atrasado: el panel lo avisa, y ponerlo al día quita la línea y la copia.

**Lo de la SF y lo global no son del proyecto** (acuerdos del propietario, 2026-11-01 y 2026-11-02). Lo que se ve de la SF en un proyecto (el panel, sus avisos, las skills, sus reglas o su forma de hablar) es del plugin. Una petición sobre ello no se cambia allí ni entra en la cola del proyecto: Claude dice en una línea que es de la SF («Automejora durante el uso de la SF», más abajo). La configuración global de Claude Code (`~/.claude`) no se toca sin que el propietario lo pida y lo confirme.

**Un proyecto por sesión** (acuerdo del propietario, 2026-10-27). Una sesión de Claude Code trabaja sobre el proyecto de su carpeta. Puede leer otros proyectos: desde la SF, leer un proyecto para llevar a la SF lo que funciona es realimentación.

No modifica otro proyecto: lo dice en una línea y propone hacerlo en una sesión abierta en ese proyecto. El mod de estado bloquea con el motivo las escrituras de archivos en otro proyecto; un worktree de git cuenta como el proyecto de su repositorio (acuerdo del propietario, 2026-10-29). Las órdenes de terminal no las puede analizar y para ellas vale esta regla.

### 2.1. Tareas y cola

**Una cola y una tarea por petición.** Cada petición del propietario entra en la cola del proyecto, `.sf/peticiones.json`, en cuanto llega, aunque esté sin concretar. Lo que falte para hacerla (concretar, deliberar, decidir, diseñar cómo) va como pasos de su tarea y se pregunta dentro de ella (acuerdo del propietario, 2026-11-02).

Al anotarla, Claude abre un menú breve: si encaja como paso de alguna tarea, primero si se añade a ella; si no, si va en curso o en cola. No pregunta lo que el propietario ya ha dicho (acuerdo del propietario, 2026-10-30).

Todo bug, también el que dice el propietario, entra antes de investigarlo: reabre la tarea que lo causó, si se localiza, y si no es una tarea nueva. Un error que Claude detecta fuera de la tarea en curso va a la cola, con qué falla, dónde y cómo se ve; no se arregla de paso.

Sin tarea en curso no se trabaja. La excepción es incorporar el proyecto a la SF, ponerlo al día y cambiar su configuración: son operaciones sin tarea, guiadas por menús («Incorporación», más abajo).

**Toda escritura de la cola pasa por el CLI** `cola.py` del plugin, con una orden fija, la misma que usa el panel (acuerdo del propietario, 2026-11-01). La cola nunca se edita a mano.

Las órdenes de Python de la SF usan el intérprete que el mod detecta en la máquina: el primero de `python`, `python3` o `py` que sea 3.9 o posterior (acuerdo del propietario, 2026-11-02).

**Tipos de tarea** (acuerdo del propietario, 2026-11-02). Hay siete tipos en tres familias:

- **Código:** implementar y corregir.
- **Deliberativas:** investigar, deliberar y diseñar.
- **Documentales:** especificar y documentar.

El tipo decide cómo se maneja el repositorio. Una tarea de código tiene su rama, el worktree de su subagente, el squash en `develop` al cerrar y la observación.

Una deliberativa no tiene rama, y su subagente trabaja sin worktree ni rama auxiliar: solo escribe su documento (su informe y, si la hay, su visión), que va directo a `develop` en cada vuelta, con el respaldo de la versión anterior. Lo demás que haga falta cambiar, como realimentar una skill con lo aprendido, va a una tarea propia, con rama. Su único paso de cierre es «Cerrar la tarea»: se cierra sin squash ni observación (acuerdos del propietario, 2026-11-04).

En una documental, un documento nuevo no tiene rama: cada vuelta se copia a `develop`, con su respaldo previo, y se cierra con la aprobación del propietario, sin observación. Un cambio de documentos existentes tiene su rama y su squash, con la aprobación del propietario.

Una deliberativa da un informe y las tareas que salgan de él; sus dilemas viven en el informe (skill `informe_deliberativa`).

**Cómo se llevan.** Cómo trata el agente principal cada mensaje (el menú al anotar, poner en curso, los pasos, los subagentes, probar y cerrar, fusionar y separar, preguntar y escribir) está en la skill `sf:orquestacion`. La mecánica de la cola (estados, pasos de cierre, ramas, observación, descartar, revertir, reabrir, eliminar, fusionar y separar, botones y órdenes del panel, historial y copias) está en `sf:flujo_tareas`. Aquí quedan los acuerdos:

- **Pasos.** Concretar, definir, diseñar y decidir son pasos, y se anotan en cuanto empiezan. Pendiente o en curso, en infinitivo; hecho, en participio, con el verbo del oficio. Los dos pasos de cierre los pone `cola.py` desde que la tarea entra en curso (acuerdo del propietario, 2026-11-01).
- **Probar y cerrar.** Al terminar una tarea, Claude enseña lo hecho y propone probarla, con cómo. Si no tiene nada que probar (deliberar, investigar, documentar, especificar…), propone cerrarla directamente, enseñando el resultado (acuerdo del propietario, 2026-10-31).
- **En observación.** Una tarea cerrada que espera el OK del propietario queda «en observación». Se cierra si va bien o se revierte si va mal (acuerdo del propietario, 2026-11-02).
- **Comprobaciones, pasos hechos.** Cada comprobación o prueba hecha en una tarea se anota como paso hecho, con lo comprobado y su resultado (`cola.py comprobado`); lo no comprobado se dice como tal (acuerdo del propietario, 2026-11-05).
- **El OK.** El cierre, el paso a observación y la publicación esperan el OK del propietario; los commits de trabajo en la rama de la tarea, no.
- **Cerrar antes que abrir.** El principal empuja primero a cerrar las tareas en curso que se pueden cerrar, llevando al propietario lo que necesitan para probar, decidir o cerrar. Solo después propone poner en curso tareas nuevas. Las peticiones y los defectos nuevos se siguen anotando al llegar (acuerdo del propietario, 2026-10-31).
- **Guiar, no solo ejecutar.** La SF organiza el desarrollo: observa las tareas, el proyecto y al propietario, y sugiere por iniciativa propia cómo avanzar mejor. Por ejemplo, partir o cerrar una tarea que crece mucho en pasos. Sugerir no es hacer: nada se parte ni se cierra sin el OK del propietario (acuerdo del propietario, 2026-11-02).
- **Fusionar y separar.** El principal sugiere fusionar dos tareas que tratan lo mismo y separar las partes de una que junta varias, con la orden lista. Tras una fusión, propone redescribir la tarea resultante.
- **Mejorar la skill que se usa.** En una tarea de documentos, mejorar la skill que los hace con lo aprendido es un paso de esa tarea.
- **Propuestas.** Una petición que solo anota una propuesta se cierra al anotarla, sin observación.
- **Preguntas.** Con la herramienta de preguntas de Claude Code: una pregunta por tarea, cuatro como mucho cada vez.
- **Preguntas legibles.** La pregunta es corta, de una línea. El detalle va antes, en el chat, en palabras llanas: cada cosa en su línea y con para qué sirve; si hay cambios, agrupados en Crea, Cambia, Sube a GitHub y No toca. Cada opción dice lo que hará Claude, y su descripción, la consecuencia. Sin jerga interna ni nombres de campos; los valores, legibles («color verde»). Al pedir el OK para aplicar, además de Aplicar y No aplicar, «Cambiar algo antes» (acuerdo del propietario, 2026-11-04).
- **Textos.** El nombre de una tarea y el título de un commit empiezan por lo que cambia, en pocas palabras, sin prefijos. Las descripciones, sin origen ni autor, y cada idea en su párrafo.
- **Sin referencias por número que no se vean en pantalla.** En los textos para el propietario (mensajes, tareas, pasos, documentos), una sección, una decisión o una tarea se nombra por su título, con el número entre paréntesis si ayuda (acuerdo del propietario, 2026-10-31).
- **No dejar anotado lo que no aporta.** Podar es quitar: ni remisiones a lo que ya está en una skill o un documento, ni rastro de lo borrado. Para recuperar algo están git y los respaldos (acuerdo del propietario, 2026-10-31).

**Documentos compartidos** (acuerdos del propietario, 2026-10-31). Los documentos que describen la SF se actualizan cada uno en su tarea, «Actualizar <documento>».

Una tarea que necesita cambiar uno de ellos no lo cambia: añade a la tarea del documento un solo paso, «Reflejar «<título de la tarea>» (NN)», al ponerse en curso o en cuanto se ve que le afecta. Quien actualiza el documento mira lo que hizo la tarea.

Una tarea de código (implementar, corregir) no lleva pasos de documentación, sea cual sea el documento: lo que haga falta escribir o cambiar por lo que hace va a una tarea documental (especificar, documentar), la de su documento si existe o una nueva. Los comentarios del código y la documentación técnica que va con él (docstrings, README del módulo) son de la tarea de código (acuerdo del propietario, 2026-11-02).

Dos tareas del mismo documento se fusionan directamente. La metodología, la plantilla de reglas y el `CLAUDE.md` de la SF comparten una sola tarea.

Las tareas de documentos tienen su subagente, como cualquier otra, y se hacen de una en una.

### 2.2. Ramas y subagentes

**Ramas por tarea** (acuerdo del propietario, 2026-11-02). El modelo de ramas es fijo. Se desarrolla en `develop`; `main` es lo que usan los proyectos.

Al poner en curso una tarea que lleva rama (las de código y las que cambian documentos existentes), Claude crea su rama `feature/NN-nombre` desde `develop` y avisa, sin pedir autorización. Una rama es de una sola tarea.

La tarea entra en `develop` al cerrarla, con el OK del propietario, por **squash**: un solo commit por tarea, con sus pasos en el cuerpo, que se revierte con un `git revert`. Los commits los hace siempre Claude. Una rama sin cambios respecto a `develop` se cierra sin commit: el cierre la borra, con su worktree y su rama auxiliar, y saca la tarea de la cola (acuerdo del propietario, 2026-11-04).

**Publicar** es pasar `develop` a `main` con el tag `vX.Y.Z`, con el botón RELEASE del panel. La versión se sube solo al publicar, nunca en una feature.

**Revisión antes de publicar** (acuerdos del propietario, 2026-11-03 y 2026-11-04). RELEASE revisa lo que sale en esa versión (archivos y mensajes de los commits) en busca de secretos, datos personales, rutas de la máquina o documentos internos. En un repositorio público, si encuentra algo nuevo no publica: se corrige, o se apunta como permitido en `.sf/publicable.txt`, y se vuelve a pulsar; la misma revisión corre al subir `develop` al cerrar cada tarea. En uno privado, enseña lo encontrado y pregunta si seguir. Lo que ya está subido no bloquea: se enseña y se pide permiso para continuar.

**Cómo se prueba una tarea en su rama.** Con la rama activa en la carpeta principal: «Activar rama» del panel integra `develop` en ella, la activa y adelanta la rama auxiliar del subagente, sin pisar cambios sin commit. Si choca o encuentra trabajo sin traer, pasa el fallo a Claude (acuerdo del propietario, 2026-11-01).

Un documento se prueba abriéndolo. El plugin, en la SF, con sus pruebas (`claude plugin test plugins/sf` para el panel y `python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_*.py"` para las herramientas de Python), con el modo prueba y `/reload-plugins`. Si su efecto se ve en otro proyecto, en una sesión de ese proyecto abierta con `claude --plugin-dir` apuntando a `plugins/sf` de la SF.

En un proyecto, con la aplicación reiniciada; con migraciones, sobre una base de pruebas; con dependencias nuevas, instaladas antes. Hay una sola rama activa por carpeta; antes de cambiarla, Claude hace commit de guardado en la que deja.

Pendiente: probar un catálogo fijado a una versión con `#ref`.

**Orquestación con subagentes** (acuerdos del propietario, 2026-10-31). El agente principal habla con el propietario, decide con él, lleva la cola y registra las decisiones.

Toda tarea en curso tiene su subagente desde que se pone en curso, también las de diseño o deliberación. Él hace todo el trabajo de la tarea: los cambios, y también leer, clasificar, analizar, investigar y proponer. Sigue vivo hasta el cierre; si un paso espera al propietario, espera él.

El principal lanza el subagente sin preguntar, avisando en una línea. El botón TURBO del panel pone en curso, cada una con su subagente, las tareas de la cola que no necesitan al propietario; las demás esperan a que él las ponga en curso (acuerdo del propietario, 2026-10-31).

El subagente trabaja en su propio worktree, en una rama auxiliar desde la de la tarea; el de una deliberativa, sin ninguno de los dos («Tareas y cola»). El principal trae sus commits con `git merge --ff-only`. Solo el principal escribe la cola: el mod bloquea que lo haga un subagente.

Las reglas completas, en la skill `sf:orquestacion`.

### 2.3. Incorporación

**Incorporar un proyecto, ponerlo al día y cambiar su configuración son operaciones sin tarea** (acuerdos del propietario, 2026-11-01 y 2026-11-02). No pasan por la cola ni por el panel.

Claude las guía con menús en la línea de prompts: dice qué va a crear, mover o cambiar, pide el OK del propietario y lo aplica en `develop` del proyecto, con su commit. Lo que salga mal se deshace con git.

**Incorporar no cambia el proyecto.** La SF no renombra carpetas ni archivos, ni cambia de sitio documentos ni ningún otro contenido del proyecto. Lo que necesita lo usa donde ya está o lo añade con lo mínimo. Reorganizar algo del proyecto es una petición aparte.

Lo mínimo que añade es `.sf/proyecto.json`, la carpeta `sf/` y, si faltan, `develop`, `main` y el remoto en GitHub. Sin `develop` ni remoto en GitHub no hay SF: se explica y, si el propietario lo reconfirma, no se incorpora.

**La SF lleva el repositorio a su manera** (acuerdo del propietario, 2026-11-04): `develop`, `main` y una rama por tarea, los commits de Claude, el cierre por squash en `develop`, la subida a GitHub y la publicación con el OK del propietario. La incorporación lo explica una sola vez, en palabras llanas y antes de pedir nada, con lo que hace el propietario (probar y dar el OK). No ofrece opciones que dejen la SF sin poder trabajar, como que los commits los haga el propietario: si no acepta esa forma de trabajar, no se incorpora. Lo aceptado no se vuelve a preguntar: las reglas del proyecto que choquen con ella se adaptan, avisando de qué cambia.

La única excepción a no mover nada son los documentos de la SF que ya tuviera el proyecto (sus propuestas, sus decisiones y los informes de la SF): pasan a `sf/`, con el OK del propietario.

**La skill `incorporar_proyecto_a_sf`** cubre cuatro casos: proyecto nuevo, proyecto existente anterior a la SF, poner al día uno ya incorporado y diagnosticar sin cambiar nada.

Poner al día empieza por el plugin: si hay una versión publicada más nueva, Claude ofrece actualizarlo. Con el plugin actualizado, pide al propietario `/reload-plugins` y que vuelva a pedir la puesta al día. Al terminar, si han cambiado las reglas, pide `/clear` para que entren.

**La configuración** se cambia después con la skill `configurar_proyecto`, pidiéndoselo a Claude o con la orden `/sf_config`. Poner al día también la ofrece.

Si el `CLAUDE.md` de un proyecto es complejo (por ejemplo, con muchas reglas propias sobre ramas, commits o documentos), revisar lo que choca con la SF es una tarea aparte, que estudia cada cambio antes de hacerlo. Si una regla del `CLAUDE.md` del proyecto choca con la SF, manda la del proyecto, y el choque se anota en sus decisiones. La excepción es cómo se lleva el repositorio: ramas, commits, push, cola y publicación. Ahí manda la SF, como se aceptó al incorporarlo. El formato de los commits sigue siendo el de `.sf/proyecto.json` (acuerdo del propietario, 2026-11-05).

**Proyectos anteriores a la SF.** Se incorporan sin rehacer lo que ya funciona:

- con metodología, declaran en `.sf/estado.json` la fase real y, en `hechas`, solo las fases cubiertas de verdad;
- anotan como pendientes los documentos que faltan, por ejemplo la visión o la especificación funcional, sin mover lo que ya tienen.

Primer caso: JKanban, 2026-10-27.

## 3. Ciclo de creación y desarrollo

### 3.1. Documento de visión

Primer documento del proyecto. Presenta la idea desde la perspectiva del emprendedor: explica qué se quiere crear y transmite su sentido y posibilidades de manera fácilmente comprensible y motivadora.

No es una especificación técnica ni un análisis exhaustivo. Su objetivo es introducir las ideas base, despertar interés e implicar al lector.

**El propietario ya dispone de una skill para elaborarlo.** Su incorporación a la SF se recoge en su especificación; esta metodología conserva el enfoque de visión definido por el propietario.

Junto a la visión, cada proyecto tiene un **documento fundacional** (skill `documento_fundacional`). Es su presentación formal y compacta, sin historia conductora: la necesidad documentada, la tesis de desarrollo, qué es el producto, sus escenarios de uso, las evidencias con lo que respaldan y lo que no, qué debe demostrar el piloto y las fuentes. Sirve al autor como descripción de referencia y se puede compartir. Un producto de una familia puede tener el suyo. La visión y el documento fundacional se mantienen coherentes: si uno cambia, se revisa el otro.

**Documentos opcionales** (acuerdo del propietario, 2026-10-27). Junto a la visión, cada proyecto puede tener, si le sirven:

- **visiones desde otras perspectivas**, en `docs/specs/vision/` (skill `documento_vision`): la misma idea contada a otro lector, por ejemplo la del propietario que trabaja solo con la SF;
- **infografías técnicas**, en `docs/specs/vision/infografias/` (skill `infografia_tecnica`): una pieza del producto explicada visualmente;
- **«Cómo funciona la Software Factory»**, en `docs/como-funciona-la-software-factory.md`: el mapa del sistema, con sus componentes, dónde está cada uno y cómo se relacionan, sin reglas.

Las guías de instalación y de actualización no son opcionales («Qué pertenece a cada proyecto consumidor»).

### 3.2. Especificación funcional global y diseño de interfaz

Concretar el comportamiento del conjunto del proyecto. Las funcionalidades se reúnen a partir de la visión, los documentos de referencia, el estudio de mercado y otras fuentes de requisitos disponibles.

- Funcionalidades y reglas de negocio.
- Recorridos de usuario.
- Pantallas, navegación e interacción.
- Estados relevantes: carga, vacío, error y permisos, cuando procedan.
- Criterios funcionales comprobables.
- Endpoints y contratos de API cuando correspondan: operaciones, entradas, salidas, errores y autorización.

Los detalles técnicos de los contratos se ajustarán durante la definición técnica. El detalle debe ser suficiente para comprender el producto completo, sin anticipar cada decisión de implementación.

La interfaz se define en detalle antes de elegir tecnología, con la skill `diseno_interfaz`:

- Recorridos clave con un protagonista con nombre, pasos, momento clave y camino de fallo.
- Inventario de pantallas: desde dónde se llega a cada una y para qué sirve. Cada necesidad tiene su pantalla y cada pantalla su recorrido.
- Matriz pantalla × estado: ideal, vacío, cargando, parcial, error y sin permiso, más los propios del producto. Las celdas que no aplican se justifican.
- Comportamiento de los componentes, interacción, textos y accesibilidad mínima.
- Bocetos estáticos de 2 a 4 pantallas clave. La especificación manda sobre los bocetos.
- Criterios de aceptación con escenarios «Dado / Cuando / Entonces» («Pruebas y criterios de aceptación»).

### 3.3. Definición técnica y arquitectura global

Seleccionar tecnologías, plataforma, arquitectura, persistencia, integraciones y estrategia de pruebas y distribución. Identificar si Claude Code es también un componente del backend y si existen brain de desarrollo, KB operativa o ambos; concretar sus responsabilidades y límites.

Usar perfiles favoritos como punto de partida, confirmar su adecuación y justificar las excepciones. Registrar las decisiones relevantes.

Se hace una vez por proyecto, con la skill `definicion_tecnica`. El documento técnico es corto: fija solo lo que evita que dos partes construidas por separado elijan de forma incompatible (paradigma, decisiones de arquitectura con su regla, convenciones), el stack con versiones verificadas, la estructura de partida y lo que se aplaza con su motivo. Cada decisión no obvia guarda su porqué en `sf/decisiones/` («Estructura documental común»). Cuando ya existe código, la estructura y el stack los manda el código.

### 3.4. Planificación por devslices

Planificar la construcción como una serie de devslices: incrementos verticales completos y comprobables, con prioridad, dependencias y criterios de aceptación. Registrar las devslices en el kanban.

Las devslices no son una copia de la lista de funcionalidades. Una devslice puede tocar varias funcionalidades, y una funcionalidad puede completarse a lo largo de varias devslices. Conservar la relación entre devslices y funcionalidades para comprobar que la planificación cubre la especificación.

Ejemplo: **Crear registro** permite introducir datos, validarlos, guardarlos y ver el resultado. Incluye las partes necesarias de interfaz, lógica, datos y pruebas. Puede completar la funcionalidad de alta y, a la vez, una primera parte de la de consulta, que otra devslice ampliará con filtros.

No planificar la implementación como «todo el backend» seguido de «todo el frontend».

Para preparar la propuesta de plan, seguir estas recomendaciones generales. La propuesta se revisa después con el propietario y se ajusta a cada proyecto.

- **Tamaño.** Cada devslice cabe en una o dos sesiones de trabajo y deja algo que se ve funcionar. Si al prepararla no cabe, se parte en dos.
- **Orden.** Primero va lo que hace falta para comprobar que lo siguiente funciona. Lo básico del dominio (por ejemplo, usuarios, grupos y perfiles) va pronto. Las integraciones caras o inciertas, como un agente de IA o un servicio externo, suelen ir al final. Hasta entonces, un sustituto simulado responde detrás de la misma interfaz, para que el resto se construya y se pruebe sin ellas.

Ejemplo: en LecturaFàcil es lógico dejar la parte del agente para después. Primero se construyen los docentes, los grupos, los perfiles y la revisión de textos con un agente simulado. Después, Claude Code sustituye al simulado.

### 3.5. Preparación de cada devslice

Una devslice planificada todavía no está preparada para implementarse.

Antes de desarrollar:

1. Consultar la visión y las especificaciones globales pertinentes.
2. Afinar alcance, comportamiento, criterios de aceptación, errores y límites.
3. Resolver dudas y dependencias que impidan construir con claridad.
4. Diseñar interfaz, interacción, contratos y cambios de datos correspondientes.
5. Definir ejemplos de aceptación y pruebas previstas.
6. Crear y ordenar las tareas concretas en el kanban, vinculadas a la devslice.
7. Comprobar que dispone de la información necesaria para pasar a preparada y que sigue cabiendo en una o dos sesiones; si no cabe, partirla.

Preparar las devslices próximas a ejecutarse, aprovechando lo aprendido de las anteriores.

### 3.6. Desarrollo y verificación

Secuencia favorita:

1. Crear y revisar las pruebas anticipadas pertinentes.
2. Implementar lógica y persistencia/backend, incluidos endpoints cuando existan.
3. Construir e integrar la interfaz.
4. Comprobar el comportamiento completo.
5. Revisar resultado, código y pruebas; corregir hallazgos.

Cuando se aplique TDD, trabajar en ciclos pequeños: prueba que falla por el motivo esperado, implementación mínima y refactorización manteniendo las pruebas correctas. Preparar los casos de antemano no exige escribir toda la batería antes de implementar.

En escritorio, empezar por el backend significa comenzar por lógica y datos, aunque no exista un servidor separado.

### 3.7. Cierre

- Verificar los criterios de aceptación mediante evidencias apropiadas.
- Registrar comprobaciones realizadas, fallos y limitaciones pendientes.
- Actualizar la documentación y decisiones afectadas.
- Enlazar resultados relevantes desde el kanban y actualizar su estado.
- Integrar o entregar según las reglas del proyecto.

Las condiciones de aprobación humana, permisos de integración y publicación, límites de corrección automática y tratamiento de bloqueos están pendientes de concretar. Este documento no autoriza despliegues ni integraciones automáticas.

## 4. Seguimiento en el kanban

El kanban local multiproyecto será la interfaz humana permanente y la referencia del estado del trabajo. La construcción de su integración MCP se especifica en [la especificación de la SF](https://github.com/jumibot/SoftwareFactory/blob/main/docs/specs/funcional/software-factory.md).

Dos niveles de planificación:

| Nivel | Creación | Contenido |
| --- | --- | --- |
| Devslice | Planificación global | Objetivo funcional, alcance, prioridad y dependencias. |
| Tareas | Preparación de la devslice | Trabajo concreto de implementación, pruebas, revisión y cierre. |

Las tareas pueden ser técnicas. El resultado conjunto de la devslice sigue siendo funcional y comprobable.

Responsabilidades:

- Documentación: especificaciones, diseños y decisiones.
- Kanban: planificación, estados, dependencias, bloqueos y enlaces a evidencias.
- MCP: operaciones para consultar y actualizar el kanban.
- Skills del método: reglas sobre cuándo consultar, actuar y actualizar.

Actualizar el tablero forma parte del procedimiento. Una operación solo se considera registrada cuando la herramienta confirma el resultado. Tras una interrupción debe poder recuperarse el contexto consultando documentación y tablero.

Los estados de la SF y sus transiciones están por decidir (propuesta «Estados del kanban», en [propuestas](https://github.com/jumibot/SoftwareFactory/blob/main/docs/propuestas.md)). JKanban ya permite definirlos como flujos.

Los bloqueos deben mostrar su motivo y la decisión o acción necesaria. Si el sistema requiere identificadores internos, pueden existir, pero los nombres humanos serán descriptivos: «Crear registro».

## 5. Preferencias técnicas

| Área | Preferencia |
| --- | --- |
| Herramienta principal | Claude Code. |
| Escritorio pequeño | Python. |
| Interfaz de escritorio | Tkinter o Qt según interfaz, interacción y graficación. |
| Arquitectura de escritorio pequeño | MVP: Modelo–Vista–Presentador. |
| Frontend web | React como favorita. |
| Backend API | FastAPI como favorita. |
| Persistencia | SQL nativo, sin ORM. |
| Datos locales estructurados | SQLite como candidata cuando encaje. |
| Arquitectura compleja | Clean Architecture cuando esté justificada. |
| Calidad | Pruebas anticipadas, revisión de pruebas y TDD cuando sea viable. |

La persistencia utilizará consultas parametrizadas, transacciones apropiadas, esquema y migraciones versionados y pruebas de integración con el motor elegido. Repositorios o funciones pueden encapsular SQL sin introducir un ORM.

MVP y Clean pueden combinarse: MVP organiza la presentación y Clean las dependencias del conjunto. Clean puede aplicarse solo al backend si el frontend no necesita esa complejidad.

## 6. Estructura documental común

```text
proyecto/
├── CLAUDE.md
├── .sf/
│   ├── proyecto.json
│   ├── estado.json
│   ├── peticiones.json
│   └── subagentes.json
├── sf/
│   ├── propuestas.md
│   ├── decisiones/
│   │   ├── README.md
│   │   └── 001-2026-10-29-titulo-de-la-decision.md
│   └── informes/
├── docs/
│   ├── specs/
│   │   ├── vision/
│   │   │   └── infografias/
│   │   ├── funcional/
│   │   ├── tecnica/
│   │   └── devslices/
│   │       └── crear-registro/
│   │           ├── especificacion.md
│   │           └── diseno.md
│   ├── guias/
│   │   ├── instalacion.md
│   │   └── actualizacion.md
│   ├── identidad/
│   └── referencias/
└── ...
```

Las dos carpetas de la SF conviven con una regla clara: `.sf/` es la máquina y `sf/` los documentos (acuerdo del propietario, 2026-11-02).

- `.sf/`: lo que la SF necesita del proyecto para funcionar, fuera de `docs/` porque no es documentación (acuerdo del propietario, 2026-10-27). Lo lee el mod del plugin `sf`.
  - `proyecto.json`, versionado: dice que el proyecto está bajo la SF y guarda su configuración, en campos sueltos (acuerdo del propietario, 2026-11-02). Son `proyecto` (nombre), `descripcion` (una línea de 120 caracteres como mucho), `color` (el de sus sesiones de Claude Code; `purple` es de la SF), `sf` (versión de la SF con que se incorporó o se puso al día), `metodologia`, `idioma`, `commits` (su formato), `coautor` (la línea de coautoría de los commits; sin ella, van sin firma), `remoto`, `rama_main`, `manifiesto` y, si se apaga alguna, `automatizaciones`. El kanban es opcional y, por defecto, ninguno: si se elige, `kanban` dice su proveedor y su proyecto en él (acuerdo del propietario, 2026-11-02). Lo que falta vale lo de por defecto. Se cambia con `/sf_config` (skill `configurar_proyecto`).
  - `estado.json`, fuera de git, solo con metodología: el estado en el método. Campos: `fase` (`vision`, `especificacion`, `tecnica`, `planificacion`, `preparacion`, `desarrollo` o `cierre`, una por apartado de «Ciclo de creación y desarrollo»), `detalle`, `devslice` (nombre descriptivo de la devslice en curso), `hechas` (fases cubiertas; si falta, se dan por hechas las anteriores a la actual), `actualizado` (fecha) y `pendientes` (lista). Se actualiza al cambiar de fase o de devslice.
  - `peticiones.json`, fuera de git: la cola de tareas del proyecto. Su formato, sus copias y su historial están en la skill `sf:flujo_tareas`; solo se escribe con `cola.py`.
  - `subagentes.json`, fuera de git: la memoria del mod sobre los subagentes de la sesión y los avisos que ya ha dado.

  El estado tiene una sola fuente. Sin kanban, es `estado.json`, y la cola es `peticiones.json`. Con JKanban incorporado, el estado vivirá en el kanban y `estado.json` será su última copia, para cuando no hay conexión. Lo mismo valdrá para la cola: cada tarea pendiente será una tarea del backlog del proyecto en JKanban, y `peticiones.json`, su copia sin conexión (acuerdo del propietario, 2026-10-27).
- `sf/`: los documentos de la SF en el proyecto (acuerdo del propietario, 2026-11-02).
  - `propuestas.md`: lo que no está decidido, con su número fijo (`### P<nn> <título>`). Solo propuestas de este proyecto («Automejora durante el uso de la SF»).
  - `decisiones/`: el registro de decisiones (más abajo).
  - `informes/`: los informes que escribe Claude en el proyecto (análisis, auditorías, diagnósticos, el de cada deliberativa). Se crea con el primero.
- `specs/`: definición del producto y de su solución.
- `specs/vision/`: los documentos fundacionales del proyecto, juntos. Son el documento de visión, el documento fundacional (`fundacional-<proyecto>.md`, y uno por producto si los hay) y las infografías técnicas, en `infografias/`. Los originales que se convirtieron (PDF, HTML) se conservan junto a ellos o en `_respaldo/`.
- `guias/`: la guía de instalación desde cero (`instalacion.md`) y la de actualización (`actualizacion.md`). Cada una es un procedimiento que se sigue paso a paso: requisitos, órdenes en bloques de código con su lenguaje y una comprobación final de que funciona. La de actualización dice, para cada versión, qué cambia y qué hay que hacer (migraciones, configuración, datos).
- `identidad/`: lo propio del proyecto que usan las skills de la SF: tema y logo, reglas del dominio para los documentos y las infografías.
- `referencias/`: materiales importantes que considerar, conservando procedencia.
- `devslices/`: especificación afinada y diseño de cada incremento.

**El registro de decisiones** es obligatorio y es material de la SF: va siempre en `sf/decisiones/`, con el formato de la SF, tenga o no el proyecto otro sitio propio (acuerdos del propietario, 2026-10-30 y 2026-11-02). Recoge todas las decisiones del proyecto: de producto, de interfaz y técnicas.

Cada decisión se registra en cuanto se toma, con su porqué: contexto y problema, opciones, decisión y consecuencias (el formato MADR mínimo). Si una decisión cambia otra, lo dice, y la antigua se marca como sustituida con la línea «**Sustituida** el … por «…»» bajo su título.

**Una decisión por archivo** (acuerdo del propietario, 2026-10-29): `NNN-AAAA-MM-DD-titulo.md`, con la fecha del origen y el título sin tildes ni signos, que empieza por `# Título`.

Se registra con `cola.py decision "Título" --archivo RUTA` (o `--texto`). La orden da el número, escribe el archivo, rehace el índice y hace el commit en `develop`, también si la rama activa es otra, sin cambiarla (acuerdo del propietario, 2026-11-02). Así las decisiones están en `develop` en cuanto se toman y no chocan con las ramas de las tareas (acuerdo del propietario, 2026-10-31). Nunca se escribe a mano en la rama de una tarea.

El índice, `sf/decisiones/README.md`, no se escribe a mano: lo regenera `tools/indice_decisiones.py` del plugin `sf`, y `.gitattributes` lo junta con `merge=union`. Su versión HTML, `README.html`, no se versiona: se genera al abrirla desde el panel (acuerdo del propietario, 2026-11-01).

Un proyecto con decisiones en otro sitio (el antiguo `docs/decisiones/`, un `docs/decisiones.md` u otro registro propio) las pasa a `sf/decisiones/` al incorporarlo o ponerlo al día, con el OK del propietario. Si un archivo mezcla decisiones con otras cosas, sus decisiones pasan a `sf/decisiones/` y su sección se cambia por un enlace a ellas. La skill `definicion_tecnica` trae la plantilla de una decisión.

**Diagramas en SVG, nunca en ASCII** (norma del propietario, 2026-10-27). Todo diagrama de un documento del proyecto o de la SF (un flujo, un recorrido, una estructura, dependencias, arquitectura) se dibuja como SVG inline en el propio `.md`, dentro de `<figure>` y con un `<figcaption>` breve. Se siguen las recomendaciones de la [guía de diagramas en SVG](diagramas-svg.md): vertical y de 560 de ancho para el móvil, estilo ligero, datos reales, color estable, cilindro para lo que almacena, letra del tema, accesibilidad y revisión. No se usan diagramas en ASCII (flechas y cajas hechas con caracteres) ni en mermaid: el HTML de la SF no los dibuja y se leen peor. Los árboles de carpetas no son diagramas y siguen en un bloque de texto.

**Forma de los documentos** (acuerdos del propietario, 2026-10-27):

- **Texto literal y vocabulario estable.** Se dice qué ocurre, sin metáforas («se publica y Claude Code la descarga», no «viaja»). Las piezas de la SF, de un plugin o de una skill son «componentes», no «elementos». Los títulos de los documentos técnicos son formales.
- **Cada documento, a lo suyo.** Lo que pertenece a otro procedimiento (por ejemplo, la instalación del plugin desde GitHub en un documento de funcionamiento) no se mete: se enlaza cuando exista.
- **Tablas de tres columnas como máximo.** Con cuatro o más, el contenido pasa a tarjetas (`.ficha` en una rejilla que se adapta al ancho). Los índices de consulta y las preguntas frecuentes van en estilo FAQ (pregunta y, debajo, la respuesta), no en tabla. Nada de rótulos que describan lo obvio, como «Pregunta» y «Dónde» sobre una lista de preguntas, ni dos franjas de color seguidas (el título de la sección y la cabecera de una tabla).
- **Introducción, diagrama y prosa.** Ninguna sección empieza por un diagrama: primero, una introducción mínima en prosa (una o dos frases que sitúan al lector); después, el diagrama, si describe bien el proceso; y después, el desarrollo en prosa corrida, sin repetir el diagrama en una lista.
- **Prosa para explicar, listas para ejecutar.** Cómo funciona algo se cuenta en prosa. Las listas numeradas quedan para los procedimientos que se siguen paso a paso (instalar, publicar, incorporar un proyecto), y las viñetas, para inventarios de asuntos sueltos.
- **Color con significado.** Además del color del tema, los colores de la serie del tema `colorido` (turquesa, naranja, verde y el acento frambuesa) dan vida a tarjetas y diagramas, pero cada uno significa una sola cosa en todo el documento (por ejemplo, las skills en turquesa y los proyectos en verde) y solo en títulos, bordes y etiquetas, sin fondos de color. Detalle en la [guía de diagramas](diagramas-svg.md).
- **Sin paja.** Un documento no dice cuándo hay que actualizarlo ni otras obviedades sobre sí mismo («Hay que actualizar este documento cuando…»): no aportan nada al lector (norma del propietario, 2026-10-29).
- **Código con su lenguaje.** Cada bloque de órdenes o de datos lleva su lenguaje (`json`, `bash`, `python`…) para que el HTML lo coloree; los árboles de carpetas van en `text`.

**Cómo se hacen los documentos** (acuerdos del propietario, 2026-11-01 y 2026-11-02). Los documentos de la SF se escriben en `.md` y se generan a HTML con la skill `crear_documentos`. Reúne lo común: el generador, los recursos, los temas y la identidad, los diagramas, el respaldo, la impresión A4 y la comprobación en escritorio y móvil.

Encima va la skill de cada tipo de documento, que dice para quién es, qué secciones lleva y con qué tono: `documento_vision`, `documento_fundacional`, `informe_deliberativa` y las que vengan.

Cada cambio de un `.md` regenera su HTML. Al generarlo se dice para quién es y qué herramientas de lectura lleva: el generador no lo elige por el autor, y al autor se le ofrecen siempre las opciones de lectura (norma del propietario, 2026-10-26).

Antes de sustituir un documento por una versión nueva, la anterior se copia a `_respaldo/`, en la misma carpeta, con el nombre `<nombre>_antes-<motivo>.<ext>`. Volver atrás es copiarla de vuelta, sin tocar git.

Usar nombres descriptivos, por ejemplo `crear-registro`, sin códigos visibles como `DS001`. Crear carpetas cuando tengan contenido; las estructuras siguientes son plantillas, no un mandato de crear directorios vacíos.

## 7. Estructuras de código

Las estructuras de carpetas de cada perfil son plantillas adaptables y viven en el plugin `sf` (`plugins/sf/templates/estructuras/`). Aquí quedan las reglas de cada una.

### 7.1. Escritorio con MVP

Plantilla: [`escritorio-mvp.md`](../../../templates/estructuras/escritorio-mvp.md), en el plugin `sf`.

Las vistas muestran resultados y recogen acciones; los presentadores coordinan la interacción; el modelo contiene datos y reglas; persistencia encapsula SQL. `bootstrap.py` conecta los componentes. La lógica de negocio no importa Tkinter ni Qt.

### 7.2. Escritorio con Clean

Mantener estructura exterior, documentación y pruebas; organizar el paquete en dominio, aplicación (casos de uso y puertos), presentación e infraestructura.

Plantilla: [`escritorio-clean.md`](../../../templates/estructuras/escritorio-clean.md), en el plugin `sf`.

Dominio y casos de uso no dependen del framework gráfico ni del controlador de datos. Los casos de uso dependen de interfaces propias, implementadas por infraestructura. Presentación utiliza los casos de uso.

### 7.3. Frontend y backend separados

Plantilla: [`frontend-backend.md`](../../../templates/estructuras/frontend-backend.md), en el plugin `sf`.

MVP no prescribe la estructura del servidor. En React, componentes y hooks presentadores pueden separar vista y coordinación por funcionalidad.

Si se justifica Clean en el frontend, cada funcionalidad puede separar `domain/`, `application/`, `infrastructure/` y `presentation/`. No duplicar allí las reglas de negocio del servidor por simetría. El servidor valida sus reglas y permisos aunque el cliente también valide para facilitar la interacción.

### 7.4. Claude Code como componente del backend

Capacidad adicional compatible con escritorio, frontend/backend separados y arquitecturas MVP o Clean. Distinguir Claude Code como herramienta de desarrollo de Claude Code como componente que ejecuta funcionalidades de la aplicación.

Plantilla: [`agente-en-el-backend.md`](../../../templates/estructuras/agente-en-el-backend.md), en el plugin `sf`.

En escritorio puede ubicarse `agent-runtime/` en la raíz del proyecto, junto a `src/`. Su adaptación se decide en el perfil técnico. Estas carpetas contienen fuentes y recursos versionados; no implican carga automática por Claude Code. El lanzamiento, los directorios de trabajo y la configuración efectiva deben diseñarse y comprobarse según el mecanismo elegido.

- Las instrucciones y skills para desarrollar el proyecto son distintas de las necesarias para ejecutar el producto, aunque compartan piezas con versiones identificables.
- Los linters que comprueban el código pertenecen a la configuración de calidad del proyecto. Los validadores de resultados operativos pertenecen al componente que los ejecuta.
- Especificar entradas, salidas, herramientas, permisos, errores, límites y validación de resultados del agente.
- Versionar instrucciones, skills, hooks y herramientas del producto. Actualizar la SF no debe cambiar inadvertidamente el comportamiento del agente operativo.
- En Clean, el acceso al agente puede implementarse mediante un adaptador de infraestructura detrás de una interfaz de aplicación; no acoplar el dominio al ejecutor.

### 7.5. Scripts SQL de creación y modificación

Guardar creación inicial y modificaciones como migraciones SQL versionadas en la persistencia:

| Perfil | Ubicación |
| --- | --- |
| Escritorio MVP | `src/nombre_app/persistence/migrations/` |
| Escritorio Clean | `src/nombre_app/infrastructure/persistence/migrations/` |
| Backend sencillo | `backend/src/nombre_api/persistence/migrations/` |
| Backend Clean | `backend/src/nombre_api/infrastructure/persistence/migrations/` |

Plantilla: [`migraciones-sql.md`](../../../templates/estructuras/migraciones-sql.md), en el plugin `sf`.

`queries/` contiene consultas de la aplicación; `migrations/` conserva la evolución del esquema. El prefijo ordena la ejecución y el nombre explica el cambio.

- Versionar los scripts en Git y registrar en la base de datos las migraciones aplicadas.
- No editar una migración aplicada en un entorno compartido o entregado: añadir otra correctiva.
- Poder crear una base vacía mediante la secuencia y comprobar actualizaciones desde versiones soportadas.
- Separar datos ficticios de pruebas de datos iniciales obligatorios.
- Documentar modelo y decisiones en `docs/specs/tecnica/`; mantener los scripts ejecutables con persistencia, también si el backend incluye un agente.
- Elegir el ejecutor de migraciones y el tratamiento de fallos y transacciones según el motor. SQL nativo no exige un ORM.

### 7.6. Brain de desarrollo y KB operativa

Son capacidades independientes: un proyecto puede usar una, ambas o ninguna. Obsidian es una opción para consultarlas y editarlas; el acceso del agente debe configurarse explícitamente.

| Brain | Finalidad | Usuarios |
| --- | --- | --- |
| Desarrollo | Construir y modificar el proyecto: visión, especificaciones, decisiones y conocimiento. | Propietario y agentes de desarrollo. |
| Operativo o KB | Guardar y recuperar información durante el funcionamiento del producto. | Agente del backend y usuarios autorizados. |

Cómo organizar el brain de desarrollo y la KB es una propuesta («Brain de desarrollo en `docs/` y estructura de la KB operativa», en [propuestas](https://github.com/jumibot/SoftwareFactory/blob/main/docs/propuestas.md)).

Plantilla: [`brain-y-kb.md`](../../../templates/estructuras/brain-y-kb.md), en el plugin `sf`.

`knowledge/` documenta la organización y contiene plantillas; no duplica el contenido operativo. La ubicación efectiva del vault se configura por entorno. No guardar información operativa real en el repositorio por defecto; definir permisos, historial, copias y conservación propios. El nombre y la ubicación del vault se adaptan a cada proyecto.

Definir durante la especificación qué información se guarda, cómo se busca y actualiza, quién accede, cómo se conserva procedencia y cómo se corrigen contradicciones. Si SQL y KB describen un mismo dato, establecer una referencia principal y la relación entre ambos.

El agente operativo accede a su KB por las herramientas previstas. No incluir automáticamente el brain de desarrollo en sus búsquedas ni tratar notas recuperadas como instrucciones de configuración del agente. La KB guarda información operativa; instrucciones, skills y hooks del agente se mantienen como recursos versionados de ejecución.

El conocimiento transversal del método pertenece a la SF. Si el uso de un brain revela algo de la SF, se dice en una línea y no se anota en el proyecto («Automejora durante el uso de la SF»).

### 7.7. Perfil: escritorio Python con MVP y agente Claude Code

Perfil de partida para una aplicación de escritorio pequeña en la que un agente de IA ejecuta parte de las funcionalidades. Combina «Escritorio con MVP», «Claude Code como componente del backend» y «Scripts SQL de creación y modificación». Como todo perfil, se confirma en la definición técnica y se justifican las excepciones.

**Tecnologías:** Python; Tkinter, o Qt si la interfaz lo pide; SQLite con SQL nativo; Claude Code a través del Claude Agent SDK para Python (`claude-agent-sdk`), con la versión fijada.

**Estructura:** la de «Escritorio con MVP», con dos añadidos.

Plantilla: [`escritorio-mvp-agente.md`](../../../templates/estructuras/escritorio-mvp-agente.md), en el plugin `sf`.

**Reglas:**
- **MVP.** Los presentadores piden el trabajo al agente a través de `port.py`; ni las vistas ni el modelo conocen el SDK. El agente simulado y el real se intercambian en `bootstrap.py`.
- **Los dos Claude, separados.** El agente del producto se ejecuta en su propio directorio de trabajo, fuera del repositorio de desarrollo, con `setting_sources=["project"]` y solo sus skills (copiadas desde `agent-runtime/` al instalar). Así no carga las instrucciones ni las skills de desarrollo. Una prueba comprueba qué skills carga.
- **Credencial intercambiable.** El modo de credencial es un valor de configuración, no de código. Cambiarlo es cambiar una línea, o responder una pregunta del instalador.
  - **El cliente elige** entre clave de API (`ANTHROPIC_API_KEY`), inicio de sesión en la consola de Claude sin clave o un proveedor en la nube (Amazon Bedrock, Google Cloud, Microsoft Foundry). Todas se facturan por uso.
  - **Suscripción, solo en desarrollo:** en la máquina del desarrollador y con su propia suscripción, mediante `CLAUDE_CODE_OAUTH_TOKEN` (el token que genera `claude setup-token`).
  - **Suscripción del cliente desarrollador, opcional:** si el cliente es desarrollador y ya usa Claude Code en su equipo con su propia suscripción, puede elegir que el producto use esa credencial ya configurada. El producto no pide ni gestiona el inicio de sesión de claude.ai: lo hace el propio cliente en Claude Code. Anthropic no permite que un producto de terceros ofrezca ese inicio de sesión sin su aprobación previa (https://code.claude.com/docs/en/agent-sdk/overview.md), y la documentación no trata de forma expresa este caso. Por eso se recomienda confirmarlo con Anthropic antes de distribuir el producto a muchos clientes. A los clientes que no son desarrolladores no se les ofrece.
  - El adaptador quita del entorno del agente las credenciales de los otros modos, porque se aplican por orden de prioridad (la clave de API va antes que el token). Una prueba comprueba qué credencial usa el agente.
  - Ninguna credencial se guarda en el repositorio ni en el código: se leen del entorno o del almacén de credenciales del sistema.
- **Instalación sencilla.** El proyecto se instala con un solo paso documentado, que deja:
  - las dependencias con versión fijada;
  - la base de datos creada con sus migraciones;
  - las skills del agente copiadas a su directorio de trabajo;
  - la configuración, incluido el modo de credencial, en un archivo fuera del código.

  La forma concreta (script, ejecutable empaquetado o instalador) se decide en la definición técnica. Si la instalación es local en la organización (*on premise*), todo se ejecuta en sus equipos y los datos se quedan allí; solo salen las llamadas al modelo.
- **Contrato.** Cada llamada define entradas, salida estructurada (`output_format` con un esquema JSON), herramientas permitidas, permisos, límite de turnos y errores. Los validadores de `agent-runtime/` comprueban el resultado antes de usarlo.
- **Pruebas.** Las pruebas habituales usan el agente simulado. Las evaluaciones con el agente real se lanzan a propósito y su informe recoge el coste.
- **Datos.** Al agente solo se envía lo necesario para la tarea; los datos personales, solo si la tarea los necesita y la decisión está registrada.
- **Orden de construcción.** Según «Planificación por devslices», la integración con el agente real suele ir al final; hasta entonces trabaja el simulado.

## 8. Pruebas y criterios de aceptación

Son conceptos distintos:

| Elemento | Significado | Ubicación |
| --- | --- | --- |
| Criterio de aceptación | Comportamiento exigido, independiente de las ejecuciones. | Especificación de la devslice. |
| Prueba | Forma automática o manual de comprobar el comportamiento. | Código o procedimiento de verificación. |
| Resultado | Qué ocurrió al comprobar una versión concreta. | Informe de ejecución. |

Un criterio puede necesitar varias pruebas. Que una prueba pase aporta evidencia; no define ni modifica el criterio ni demuestra por sí solo toda la aceptación.

Cada criterio tiene un nombre descriptivo y uno o varios escenarios **Dado / Cuando / Entonces**, que sirven de base a las pruebas de aceptación.

Ejemplo:

- Criterio: **Rechazar registros sin nombre y mostrar un mensaje comprensible**.
  - Dado el formulario de alta vacío, cuando se pulsa «Guardar», entonces no se guarda nada y aparece «Falta el nombre» junto al campo.
- Pruebas: rechazo en la lógica y mensaje en la interfaz.
- Resultado: lo observado al ejecutar esas pruebas sobre una versión determinada.

### Clasificación mínima

- `unit/`: reglas o componentes aislados.
- `integration/`: colaboración real entre piezas, como acceso SQL o interacción con la API.
- `acceptance/`: comportamientos esperados por el usuario; indicar si recorren el sistema completo.

En escritorio viven en `tests/`. Con partes separadas, cada parte tiene sus unitarias e integración y las de aceptación del conjunto viven en la raíz.

Añadir clasificación por funcionalidad o categorías especializadas solo cuando facilite localizar y comprender las pruebas.

Cuando haya un agente operativo, comprobar hooks y validadores como componentes, integración con herramientas y KB, y recorridos de aceptación con el agente. Usar datos de prueba aislados; distinguir comprobaciones deterministas de evaluaciones de comportamiento del agente y registrar sus versiones/configuración. Incluir migraciones y recuperación de información operativa en las verificaciones pertinentes, sin crear categorías vacías por anticipado.

### Nombres y trazabilidad

- Archivo: `test_validacion_registro.py`.
- Prueba: `test_rechaza_registro_sin_nombre`.
- Usar `ui`, `api` o `db` cuando aclaren algo que la ruta no muestra.
- Evitar `front` o `back` si la carpeta ya lo indica.
- Evitar códigos poco mnemónicos también en criterios de aceptación.
- Mantener enlaces entre criterios y pruebas en la documentación de la devslice o sus metadatos, sin duplicar pruebas.

Las pruebas pertenecen a la aplicación y siguen vigentes tras cerrar la devslice que las originó.

## 9. Resultados: carpeta reports

`reports/` conserva resultados generados, separados de las especificaciones (`docs/`) y de las pruebas (`tests/`).

```text
reports/
└── tests/
    ├── 2026-10-25_153000_crear-registro/
    │   ├── resultados.html
    │   └── evidencias/
    │       └── mensaje-nombre-obligatorio.png
    └── 2026-10-25_170000_suite-completa/
        └── resultados.html
```

Cada ejecución relevante dispone de un informe legible y no sobrescribe las anteriores. Su nombre incluye fecha, hora y alcance; no toda ejecución corresponde a una devslice.

El informe debe identificar:

- Pruebas y alcance ejecutados.
- Fecha, entorno y versión del código; indicar cambios locales cuando existan.
- Pruebas correctas, fallidas, omitidas y errores de ejecución.
- Nombre y ubicación de las pruebas que fallan y explicación del fallo.
- Evidencias útiles, como capturas o registros, cuando sean necesarias.

El formato exacto se elegirá con las herramientas de pruebas. `resultados.html` representa el informe humano propuesto, no una obligación de introducir herramientas adicionales en todos los proyectos. Los formatos de automatización se generan cuando hagan falta.

El kanban enlaza el informe pertinente para revisión y cierre. Los informes generados quedan fuera de Git por defecto.

Es posible repetir las pruebas, pero una nueva ejecución no reproduce necesariamente la evidencia histórica. Antes de eliminar informes, conservar de forma duradera los vinculados a entregas o cierres que deban seguir siendo consultables. Ubicación y política de conservación pendientes de definir.

## 10. Decisiones pendientes

- Confirmar estados, campos y transiciones del kanban propuestos en este documento.
- Definir condiciones de preparación, revisión y cierre con la precisión necesaria para el piloto.
- Concretar aprobación humana, autonomía, integración, publicación y límites de corrección automática.
- Elegir herramientas y formato de informes de pruebas según el proyecto.
- Fijar conservación y ubicación duradera de evidencias enlazadas desde entregas o cierres.
- Concretar por proyecto ejecución del agente, configuración de hooks y skills, permisos y validación de sus resultados.
- Definir acceso y mantenimiento de los brains, relación SQL/KB y política de copias y conservación operativa.
- Elegir ejecutor de migraciones y versiones de esquema soportadas.
- Revisar y aprobar el documento completo.

La implementación de skills, distribución y MCP se desarrolla en la especificación de la SF. Las dudas que impidan trabajar correctamente se resolverán con el propietario antes de avanzar en la parte afectada.

## 11. Automejora durante el uso de la SF

En un proyecto solo se anotan propuestas de ese proyecto. Sus correcciones y mejoras van a su cola o a sus propuestas, en `sf/propuestas.md`.

Lo que es de la SF no se anota en el proyecto, ni en su cola ni en sus propuestas. Es de la SF el plugin, sus skills, el panel, sus reglas o su forma de hablar.

Claude lo dice en una línea: que es de la SF. Llevarlo a la SF es cosa del propietario, en una sesión de la SF (acuerdo del propietario, 2026-11-02).

Ningún proyecto escribe en la SF: ni registro de uso ni mejoras (acuerdo del propietario, 2026-11-01).

En la propia SF todo es del proyecto. Sus mejoras son tareas y propuestas suyas, y no se aplican sin la aprobación explícita del propietario: detectar la oportunidad no autoriza el cambio.

Una herramienta que sirva a otros proyectos es de la SF. En la SF, va al plugin, versionada y sin nada de ningún proyecto; en otro proyecto, se dice en una línea, como lo demás de la SF (norma del propietario, 2026-10-26).
