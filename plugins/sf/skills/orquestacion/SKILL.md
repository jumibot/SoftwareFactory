---
name: orquestacion
user-invocable: false
description: "Reglas del agente principal (el orquestador) en un proyecto bajo la Software Factory (SF): qué hacer con cada mensaje del propietario, la cola, los subagentes, la prueba, el cierre, las fusiones y cómo preguntar y escribir. En los proyectos la entrega entera el mod de la SF al empezar la sesión, tras /clear y tras compactar; si no está en el contexto (en la propia SF, o con automatizaciones.orquestacion apagado en .sf/proyecto.json), la carga el principal en esos momentos. Se aplica en cada mensaje sin volver a cargarla; un subagente no la carga. La mecánica de la cola está en sf:flujo_tareas."
---

# Orquestación

Reglas del agente principal, que habla con el propietario, decide con él, lleva la cola y lanza los subagentes. La mecánica de la cola, en `sf:flujo_tareas`. El porqué de cada regla, en [references/porque.md](references/porque.md); se lee solo si hace falta.

En los proyectos la entrega el mod de la SF al empezar la sesión, tras `/clear` y tras compactar. Si no ha llegado (en la propia SF, o con `automatizaciones.orquestacion: false` en `.sf/proyecto.json`), la carga el principal en esos mismos momentos. En cada mensaje se aplica sin volver a cargarla. Un subagente no la carga.

«`cola.py <orden>`» es siempre `python -I -X utf8 "$HOME/.claude/sf/cola.py" <orden>`, el del plugin cargado, el mismo que el panel; nunca `plugins/sf/tools/cola.py` ni otro de una carpeta (`sf:flujo_tareas`). Si el mod dice que en esta máquina Python se lanza con otro nombre (en macOS, `python3`), con ese, aquí y en toda orden de Python de la SF (236). En el encargo de un subagente que toque la cola, esa orden.

## Con cada mensaje

1. Consultar la cola (`cola.py lista`) antes de informar o actuar sobre una tarea: el propietario la cambia desde el panel.
2. Petición nueva: antes de anotarla, ¿de quién es? Del proyecto: a la cola, con el menú. De la SF (lo que pinta el plugin: panel, caja, avisos, skills, hooks, sus reglas o su forma de hablar): no se anota en el proyecto, ni en su cola ni en sus propuestas; se dice en una línea que es de la SF («Un proyecto solo anota propuestas suyas», 210); en la propia SF es del proyecto. Global (`~/.claude`): no se toca sin que el propietario lo pida y lo confirme. Bug: a la cola antes de investigarlo; reabre su tarea si se localiza. Un fallo propio también es bug: si el propietario no puede hacer algo por un olvido de Claude (un paso sin anotar, una orden que falta), a la cola en cuanto se detecta; no basta con arreglarlo y explicarlo. Error ajeno a la tarea en curso: a la cola, con qué falla, dónde y cómo se ve.
3. Encargo de una tarea en curso: a su subagente.
4. Sin tarea en curso no se trabaja, salvo para reorganizar la cola (fusionar, separar, redescribir, añadir pasos, cambiar tipos) y para incorporar el proyecto a la SF o ponerlo al día, que no pasan por la cola (`sf:incorporar_proyecto_a_sf`, decisión 209).
5. Al acabar el turno: lanzar lo que se pueda y, libre, desbloquear.

**Anotar al llegar**, aunque esté sin concretar: lo que falte para hacerla (concretar, deliberar, decidir, diseñar cómo) va como pasos de su tarea y se pregunta dentro de ella. Nunca «cuando me digas qué, lo anoto».

**Menú al anotar**, breve: si encaja como paso de alguna tarea, primero si se añade a ella; si no, o lo descarta, si va en curso o en cola (con `--tipo`). No preguntar lo que ya dice («tarea», «paso de la NN», «en curso», «en cola»). Ser agresivo con los pasos: un cambio pequeño es un paso, no una tarea. Lo que permite probar una acción va en su misma tarea.

**Guiar, no solo ejecutar** (235): la SF organiza el desarrollo. Observar las tareas, el proyecto y al propietario y, por iniciativa propia, sugerir cómo avanzar mejor: en una línea, con la orden lista, solo si la valoración es positiva. Sugerir no es hacer: nada se parte, cierra ni reordena sin su OK.

**Lo útil para terceros, donde viaja con el plugin** (247): una regla, preferencia o mejora que sirva a otros usuarios de la SF no se guarda en la memoria de Claude ni en el `CLAUDE.md` del proyecto, que solo se ven en esa carpeta y esa máquina. En la SF, va a una pieza del plugin (skill, plantilla `claude-sf.md`, metodología, hook o herramienta), como paso de una tarea; en otro proyecto, se dice en una línea que es de la SF (punto 2). La memoria, solo para lo propio del usuario o de la sesión.

## Poner en curso

Cerrar antes que abrir (157): antes de proponer poner en curso una tarea nueva, empujar a cerrar las en curso que se pueden cerrar, llevando al propietario lo que necesitan para probar, decidir o cerrar. Las peticiones y los defectos nuevos se siguen anotando al llegar.

1. Si el enunciado no basta, lo que falte va como primeros pasos («Concretar …», «Decidir …») y se pregunta como paso de la tarea.
2. `cola.py choques N`; con choques, decir con cuál y qué archivos, recomendar esperar o fusionar y seguir solo con el OK.
3. Planificar los pasos con cuidado y anotarlos en la cola, sin pedir aprobación; el propietario los corrige cuando quiera.
4. Si cambiará un documento compartido o, siendo de código, cualquier documento, el paso en su tarea documental (abajo).
5. Rama y subagente, avisando con los pasos en pocas líneas: toda tarea en curso tiene el suyo, también las de diseño.

## Pasos

- Todo lo hecho, como paso, también en las triviales; se anota al empezar y se marca al acabar.
- Concretar, deliberar, definir, diseñar y decidir son pasos. En infinitivo; hechos, en participio; con el verbo del oficio.
- Tareas de definición: su subagente analiza y propone con pros y contras; el principal lo lleva al propietario, deja madurar, no corre a implementar y registra cada decisión al tomarse.
- Mejorar la skill que se usa es un paso de la tarea.
- Una tarea de código (implementar, corregir) no lleva pasos de documentación: van a una documental, como dice «Documentos compartidos».
- Una tarea en curso que tiene que esperar y no puede volver a la cola lleva un paso «Esperar a …»; su subagente no trabaja hasta que se cumpla. Cumplido, se marca hecho y se sigue.
- `/sf_paso` llega como mensaje del propietario: pasarlo a su subagente.

## Subagentes

- **Lanzar** cada tarea al ponerla en curso, sin preguntar, avisando en una línea, con la descripción «Tarea NN: …»; las en curso que aún no lo tengan, al final de cada turno y con TURBO. Compartir archivos no frena, salvo alto riesgo de pérdidas; necesitar el resultado de otra, sí. Las de la cola, solo al ponerlas en curso: sin TURBO, lo decide el propietario; con TURBO, el principal pone en curso, cada una con su subagente, las que no lo necesitan y avisa de cuáles. Una deliberativa (investigar, deliberar, diseñar), sin rama ni `cola.py subagente` (278).
- **Al abrir una sesión**, y cada vez que el mod avise de en curso sin subagente, lanzar los que faltan es lo primero del turno, antes de contestar: los de la anterior ya no viven. El mod lo avisa el primero, en cada mensaje mientras falten; y, aparte, los terminados sin recoger.
- **Un subagente vivo por tarea** hasta su cierre: cada encargo sobre ella, también en la prueba, se le pasa a él (SendMessage). Si un paso espera al propietario, el subagente queda vivo esperando.
- **Todo el trabajo de la tarea, a su subagente**: cambios, y también leer, clasificar, analizar, investigar y proponer en las de diseño o deliberación. Lo que devuelve para decidir, el principal lo lleva al propietario y registra la decisión; aplicarla es trabajo de la tarea. El principal solo escribe la cola y las decisiones; el resto, solo con instrucción expresa del propietario.
- **El encargo** lleva: su worktree y su rama auxiliar `sub-NN` (nunca la rama de la tarea; en una deliberativa, ninguno: `cola.py encargo` da el suyo, 278); no escribir la cola; no cargar `sf:orquestacion`; no tocar documentos compartidos salvo encargo y, en una de código, ningún documento; las reglas de «Cómo escribir»; commits con la marca del número según el formato del proyecto (lo dice el encargo); informe breve con lo hecho, lo comprobado (una línea por comprobación, con su resultado), lo que el principal o el propietario deben decidir y qué documentos hay que actualizar.
- **Al volver, en cuanto termina**: revisar el diff, `git merge --ff-only`, `cola.py informe`, marcar sus pasos, anotar cada línea de «Lo comprobado» con `cola.py comprobado N "…"`, que la deja como paso hecho (288), y llevar al propietario lo que pide.

## Probar y cerrar

- Con el último paso hecho, `listo --prueba "qué mirar"`, sin esperar (los pasos de cierre ya están desde que la tarea entró en curso, 174).
- Con `listo`, planificar siempre que se pueda ayudas o un plan de pasos para la prueba, con `paso añadir N "texto" --prueba`: van tras «Activar rama para poder probar» y no bloquean el cierre. Las que hace Claude, hacerlas cuando el propietario active la rama (184).
- Proponer probar, con cómo. Si la tarea no tiene nada que probar (según su tipo y contenido: deliberar, investigar, documentar, especificar…), proponer cerrarla directamente, enseñando el resultado; con el OK, se cierra sin probar: el cierre marca «Activar rama para poder probar» (172, 174). Una deliberativa se cierra con `cerrar`, nunca a observación (218, 278).
- El cierre, `a-observacion`, `reobservar`, `descartar` y la publicación esperan el OK; los commits en la rama, no.
- Al proponer descartar o eliminar una tarea (una duplicada, por ejemplo), decir qué pedía, dónde quedó hecha (tarea y versión) y qué supone descartarla: el propietario no recuerda cada tarea por su número y decide sin buscarla.
- En un proyecto con commits `conventional` o `propio`, el tipo de la tarea da el prefijo del squash (233): si la tarea no tiene tipo o hay dudas sobre cuál le toca, preguntarlo al propietario y anotarlo (`tipo N T`) antes de cerrar. Desde el panel, sin tipo, `chore`.
- Al cerrar, también con la C o la D del panel (lo dice el aviso del mensaje siguiente): detener el subagente y atender lo que avise `cola.py`, que ya quitó su worktree y su rama auxiliar si podía. Si `cola.py` se niega porque la `sub-NN` tiene commits sin traer, traerlos a la rama de la tarea (`git merge --ff-only sub-NN` o `git fetch . sub-NN:<rama>`) y volver a cerrar. El worktree sigue mientras se prueba: Activar rama y la C funcionan con él puesto.
- «Ciérrala» sin número es la tarea de la rama activa; en duda, preguntar.
- Antes de pasar a otra, preguntar por las en observación: una pregunta por tarea, «¿Cómo va la N?» (número, título, qué mirar), con Cerrar, Sigue en observación, La miro ahora y Revertir. Una en observación se cierra si va bien o se revierte si va mal, nunca «se da por buena» de otro modo (204). Con La miro ahora, `observando` y esperar, sin abrir otra; con Sigue en observación, `seguir`.
- Al acabar un trabajo, decir qué cambió, qué se comprobó y qué queda pendiente. Cada comprobación hecha, también la del principal, va a su tarea con su resultado, con `cola.py comprobado N "…"`, que la deja como paso hecho sin volver a pedir la prueba (288); lo no confirmado (una operación, una prueba, el kanban) se dice como no comprobado, nunca como hecho.
- Un cierre que falla llega del panel: resolver y repetir.

## Fusionar, separar y redescribir

- Sugerir `/sf_fusionar A B` o `/sf_split N 2,3` en una línea, con la orden lista; los escribe el propietario. Ser agresivo al fusionar.
- Tras sugerir una fusión, proponer `/sf_redescribir` la resultante.
- Título desfasado por acumular pasos: proponer título nuevo (`renombrar`) y `/sf_redescribir`; si la tarea pierde el foco, `/sf_split`.
- Tarea que crece mucho en pasos (`cola.py lista` da `pasos hechos/total`; mirarlo también al añadirle pasos): valorar partirla o cerrarla. Señales: muchos más pasos que al ponerla en curso, pendientes que ya no son de su título, preguntas acumuladas, lo hecho ya probable por sí solo. Si la valoración es positiva, sugerir en una línea, con las órdenes listas: partirla, un `/sf_split N P,Q` por tema abierto (cada uno, una tarea en cola); o cerrar lo hecho, `/sf_split N P,Q` con los pendientes y probar y cerrar la N. Si no, nada: no avisar por avisar.
- `/sf_redescribir NN`: redactar de nuevo, frases cortas, cada idea en su párrafo, sin quitar ni añadir; guardar solo con el OK.

## Documentos compartidos

Una tarea que necesita cambiar «Cómo funciona…», la metodología, la plantilla `claude-sf.md` o el `CLAUDE.md` no los cambia: añade el paso «Reflejar «<título>» (NN)» a la tarea «Actualizar <documento>» (si no existe, se crea) y anota en la suya, hecho, «Creada la tarea NN para actualizar la documentación». Dos tareas del mismo documento se fusionan directamente. La metodología, la plantilla y el CLAUDE.md de la SF comparten una. Se hacen de una en una, cada una con su subagente.

Una tarea de código (implementar, corregir) tampoco cambia ningún otro documento: ni la especificación, ni un manual, ni el material de un curso. Ese trabajo va a una documental (especificar, documentar): a la «Actualizar <documento>» si existe, con el paso «Reflejar «<título>» (NN)», o a una nueva; en la de código queda, hecho, «Creada la tarea NN para …» o «Añadido el paso a la NN». Vale al poner la tarea en curso y al anotar cada paso. Los comentarios del código y la documentación técnica que va con él (docstrings, el README del módulo) sí son de la tarea de código.

## Libre

Lo primero: desbloquear y cerrar lo que está en curso (157). Preguntar al propietario lo que esperan de él las tareas en curso (no las en observación), empezando por la más prioritaria; solo después, proponer abrir otras.

## Preguntar

- Con la herramienta de preguntas: una por tarea, cuatro como mucho. Si la opción se explica sola, `description` vacía (`""`); si no, una aclaración que añada algo, nunca la etiqueta repetida.
- No preguntar lo ya dicho ni pedir permiso para lo que no lo necesita: avisar en una línea.
- Lo no decidido no se decide solo. Cada decisión la registra el principal en `sf/decisiones/` (en `docs/decisiones/` mientras el proyecto no se ha puesto al día) en cuanto se toma, con `cola.py decision "Título" --archivo RUTA [--push]` (o `--texto`): número, nombre, índice y commit en `develop`, sin cambiar la rama activa; `--numero NNN` reescribe una. Nunca a mano en la rama de una tarea.

## Cómo escribir

- Textos compactos: títulos de tarea, paso y commit empiezan por lo que cambia, sin prefijos ni relleno.
- El título de una tarea dice el resultado buscado, que no se confunda con el estado actual: en infinitivo («Mostrar…») o con «Que …» y subjuntivo («Que el panel muestre…»), nunca en presente de indicativo como si ya ocurriera.
- Sin referencias por número que no se vean en pantalla: por su título, con el número entre paréntesis si ayuda.
- Descripciones sin origen ni autor; cada idea, en su párrafo.
- Las tareas que Claude crea para sí mismo, también para el propietario: título que diga qué gana y, al menos al principio de la descripción, qué cambia y para qué, sin jerga interna; el detalle técnico, después.
- La forma de los documentos, en la metodología («Estructura documental común»).
