# Auditoría de la orquestación

Contraste de cada orden del propietario sobre el comportamiento del agente principal con lo que dicen hoy las skills, la metodología, la plantilla de reglas, el CLAUDE.md de la SF, las decisiones y la memoria de la SF. Fecha: 2026-10-31.

## Alcance

**Tareas revisadas.** Las 18 de la cola y las 37 líneas del historial (29 tareas), con descripción, pasos y eventos. De ellas, 22 tocan la orquestación: «Orquestador: prever colisiones entre tareas en curso» (112), «Pasar el panel al CLI y a leer el historial» (145), «Resumir la sección 2 de la metodología» (146), «Borrar las ramas del subagente al volver» (176), las de documentar (177, 178), «Diseñar la configuración inicial» (190), «Tipos de tarea» (192), «Analizar el trabajo con la SF en el desarrollo del panel» (194), «Convertir mejoras en tareas solo desde la SF» (195), «Margen de una columna a la derecha del panel» (196), «Al añadir una tarea, preguntar con menú» (197), las de actualizar documentos (198, 199, 207, 208), «No trabajar sin una tarea en curso» (200), «Tareas deliberativas» (201), «Sin referencias por número» (202), «Skill de orquestación» (205), «Las normas guardadas en la memoria de la SF» (211), «El CLAUDE.md pide cargar sf:orquestacion antes de publicarla» (213) y «La orquestación deja todo el trabajo de la tarea al subagente» (215).

**Antes del historial.** El historial por tarea empieza el 29 de octubre. Las órdenes anteriores se han revisado en sus decisiones (de «Un proyecto por sesión», 030, a «Todo el trabajo de la tarea, a su subagente», 151) y en la memoria de la SF.

**Órdenes contrastadas: 58.** 36 recogidas bien (tabla final), 22 con hallazgo.

**Qué está instalado.** La SF usa el plugin publicado, la 1.2.0, igual a `develop`. La corrección de la 215 está solo en su rama: hasta cerrarla y publicar, el principal de la SF sigue leyendo la línea antigua.

## Resumen por gravedad

### Graves: hacen actuar mal al principal hoy

1. **La skill instalada lanza subagente solo si la tarea «no necesita al propietario».** Corregido en la 215, sin cerrar ni publicar.
2. **El flujo de tareas manda trabajar en el principal.** Las tarjetas «Lanzar un subagente», «Volver de un subagente» y «Reabrir» de `estados.md` dicen que las triviales y las modificaciones durante la prueba se hacen en el principal. Ninguna tarea lo corrige.
3. **Los documentos compartidos se hacen «en el principal».** Lo dicen la skill (también tras la 215), el CLAUDE.md, la metodología y la decisión «Los documentos compartidos se actualizan en una tarea aparte» (112). Choca con «Todo el trabajo de la tarea, a su subagente» (151). Pide decisión.
4. **La plantilla de reglas, ya publicada, y el CLAUDE.md dicen «cada tarea en curso que no le necesita tiene su subagente».** Contradice ya la decisión «Orquestación con un subagente vivo por tarea» (149). La 205 dio por hecho el paso «sin reglas que la contradigan».
5. **La metodología dice lo contrario en orquestación, menú y prueba.** En su referencia y en las «Reglas que se aplican siempre» de su SKILL.md. Cubierto por la 208, pendiente.
6. **La memoria de la SF conserva normas superadas.** Se carga en cada sesión de la SF: «lanzar las que no necesitan al propietario», «en cola salvo primer paso», «lo probado sale de la cola sin pedir confirmación». Ninguna tarea la poda.

### Medios: recogidos a medias o ambiguos

7. **`/paso` lo hace el principal.** La skill dice «hacerlo y seguir»; con un subagente por tarea, debe pasárselo a él.
8. **Cerrar con la C del panel deja vivo el subagente.** Nadie lo para ni quita su worktree.
9. **TURBO pide poner en curso tareas de la cola.** La skill dice «las de la cola, nunca» y solo nombra TURBO como momento de lanzar.
10. **Redescribir no arregla un título desfasado.** `/redescribir` solo cambia la descripción; falta renombrar y el criterio de deriva.
11. **Cerrar directamente lo que no tiene prueba.** Está en la skill, pero la metodología lo contradice, no tiene decisión y se solapa con un paso pendiente de la 201.
12. **Las reglas de escritura no llegan a los subagentes.** Están solo en la skill que el subagente no carga.
13. **Quién escribe el archivo de una decisión.** La skill se lo da al principal; en la práctica lo escribe el subagente, en su rama.
14. **Seis órdenes sin decisión registrada.**
15. **Decisiones superadas sin marcar y «Aplicada en» desfasados.**

### Leves: desfases en documentos de apoyo

16. **`estados.md` conserva el «en cola salvo primer paso», el «¿paso o tarea?» y la rama auxiliar «si hace falta».**
17. **Los documentos «Cómo funciona» no recogen la skill de orquestación.**
18. **La plantilla ofrece el «→» del Registro en todos los proyectos.**
19. **Referencias por número en la plantilla y el CLAUDE.md.**
20. **El encargo no pide al subagente qué hay que documentar.**
21. **El porqué de la skill cita aún «lo que no necesita al propietario».**
22. **Una entrada del registro de uso repite la norma superada.**

## Hallazgos graves

### 1. Lanzar solo lo que no necesita al propietario

**La orden.** «Un subagente vivo por tarea en curso, retomado con cada encargo del propietario» y «Todo cambio de una tarea con subagente, por su subagente», pasos de «Skill de orquestación» (205), 2026-10-31. Precisada en «La orquestación deja todo el trabajo de la tarea al subagente, también el análisis» (215): «Dijimos de dejar el agente principal para orquestar salvo instrucción mía expresa».

**Dónde debería estar.** `sf:orquestacion`, secciones «Con cada mensaje», «Poner en curso» y «Subagentes».

**Qué dice hoy.**
- `develop` y la 1.2.0 instalada: «**Lanzar** las tareas en curso que no necesitan al propietario»; «Rama, avisando; y subagente si ya no necesita al propietario»; «Encargo de una tarea con subagente: a su subagente».
- Rama de la 215: «Rama y subagente, avisando: toda tarea en curso tiene el suyo, también las de diseño» y «Todo el trabajo de la tarea, a su subagente». Corregido.

**Arreglo.** Ya en la 215. Tras cerrarla, publicar con el OK del propietario: la SF usa el plugin instalado, no la fuente. Mientras, la memoria «El principal solo orquesta» compensa en la SF, pero no en los demás proyectos.

### 2. El flujo de tareas manda trabajar en el principal

**La orden.** La misma de «Skill de orquestación» (205) y la 215. La decisión «Orquestación con un subagente vivo por tarea» (149) dice que «corrige […] que una modificación durante la prueba se hacía en el principal».

**Dónde debería estar.** `sf:flujo_tareas`, `references/estados.md`. Esta skill se carga siempre que se toca la cola.

**Qué dice hoy.**
- Tarjeta «Lanzar un subagente»: «**Cuándo:** la tarea ya no necesita al propietario» y «En una trivial pregunta, para hacerla en el principal». Su «Sale de» cita «112 (documentos compartidos, en el principal)».
- Tarjeta «Volver de un subagente»: «el subagente termina o se interrumpe porque necesita al propietario». Con la 215, queda vivo esperando.
- Tarjeta «Reabrir»: «Una modificación durante la prueba se hace en el principal».

**Arreglo.** Paso en la 215: «Alinear las tarjetas «Lanzar un subagente», «Volver de un subagente» y «Reabrir» de `estados.md` con «Todo el trabajo de la tarea, a su subagente»». No es documento compartido: puede ir en la 215.

### 3. Documentos compartidos en el principal

**La orden.** «Las tareas de documentos se hacen de una en una, en el principal, sin subagentes en paralelo» (decisión 112, 2026-10-29). Después, «el principal solo orquesta […] el resto, solo con instrucción expresa del propietario» (decisión 151, 2026-10-31).

**Dónde debería estar.** Una sola regla en `sf:orquestacion` («Documentos compartidos»), el CLAUDE.md y la metodología.

**Qué dice hoy.**
- `sf:orquestacion`, también en la rama de la 215: «Se hacen de una en una, en el principal».
- CLAUDE.md: «de una en una y en el principal, como dice `sf:orquestacion`».
- Metodología, «Documentos compartidos, en una tarea aparte»: «Las tareas de documentos se hacen de una en una, en el principal».

**Choque.** El motivo de la 112 era no tener dos en paralelo, no que las hiciera el principal. Con la 151, el principal haría la 208 él mismo, que es lo que se acaba de prohibir.

**Arreglo.** Pide decisión del propietario: o excepción expresa («en el principal») o subagente también, de una en una. Después, paso en la 215 (skill) y en la 208 (CLAUDE.md y metodología), y marcar la 112 como precisada.

### 4. Plantilla y CLAUDE.md: «que no le necesita»

**La orden.** Paso de la 205 «Precargar sf:orquestacion: la plantilla claude-sf.md y el CLAUDE.md de la SF la cargan […] sin reglas que la contradigan», marcado hecho el 2026-10-31.

**Dónde debería estar.** `plugins/sf/templates/claude-sf.md` y `CLAUDE.md`, línea «Orquestación con subagentes».

**Qué dice hoy.**
- Plantilla, publicada en la 1.2.0: «cada tarea en curso que no le necesita tiene su subagente, que hace todos sus cambios».
- CLAUDE.md: lo mismo, y lo atribuye a «Orquestación con un subagente vivo por tarea» (149), que no dice eso.

**Arreglo.** Paso de la 208 «Reflejar «La orquestación deja todo el trabajo de la tarea al subagente» (215)», que debe nombrar la plantilla y el CLAUDE.md, no solo la metodología. Hacer la 208 justo tras cerrar la 215. Los proyectos que actualicen a la 1.2.0 reciben ya la línea errónea.

### 5. La metodología contradice la orquestación

**Las órdenes.** «Menú al anotar» («Al añadir una tarea, preguntar con menú si en curso o en cola», 197, 2026-10-30); un subagente por tarea (205, 215); «La metodología y el CLAUDE.md de la SF remiten a la skill nueva» (descripción de la 205).

**Dónde debería estar.** La metodología, en «Una cola y una tarea por petición» y «Orquestación con subagentes», con remisión a `sf:orquestacion`; y su SKILL.md, «Reglas que se aplican siempre».

**Qué dice hoy.**
- Referencia: «en cola, o en curso si ya se ha dado su primer paso»; «**¿Paso o tarea?** Con una tarea en curso […] Claude pregunta si es un paso de esa tarea o una tarea nueva».
- Referencia: «Una tarea pasa a un subagente cuando ya no necesita al propietario»; «Una tarea trivial no necesita subagente: solo en ella Claude pregunta, para hacerla en el principal»; «Una modificación durante la prueba de una tarea se hace en el principal»; «Al final de cada turno, el principal lanza las tareas en curso que no le necesitan».
- SKILL.md: «en cola salvo que ya se haya dado su primer paso»; «antes de cerrar una petición (commit, publicación, paso a Testing), preguntar; un commit por petición; lo cerrado queda en Testing». No remite a `sf:orquestacion`.

**Arreglo.** Ya en la 208: pasos «Menú al anotar…», «Reflejar «Skill de orquestación» (205) en la metodología» y «Reflejar «La orquestación deja todo el trabajo…» (215)». Precisar en el segundo que «Orquestación con subagentes» y «Cuándo lanzar» se sustituyen por una remisión a la skill, y que la regla «Cola de peticiones» del SKILL.md también.

### 6. Memoria de la SF con normas superadas

**Las órdenes.** «Pasar a la skill las reglas de comportamiento que hoy solo están en la memoria local» (descripción de la 205). Las normas ya superadas: menú al anotar (139), subagente por tarea (149, 151), «Sin probar hasta el OK del propietario» (050).

**Dónde debería estar.** La memoria debería quedarse sin las normas ya recogidas o superadas, o remitir a la skill.

**Qué dice hoy** (`~/.claude/projects/D--Projectes-SoftwareFactory/memory/`):
- `lanzar-sin-esperar.md`: «lanzar ya las tareas en curso […] que no necesitan al propietario».
- `libre-desbloquear-tareas.md`: «Lo que no le necesita se lanza a subagentes».
- `preguntar-antes-de-cerrar.md`: «Cada petición nueva entra `en-cola`, salvo que ya se haya dado su primer paso».
- `mod-centro-de-control.md`: «Lo probado (por el propietario o comprobado por Claude…) sale de la cola en el momento, sin pedir confirmación». Contradice la 050.
- `documentar-aparte.md`, en su descripción: «con el paso «Documentar: tarea NN»», sustituido por «Creada la tarea NN…».
- `bugs-son-tareas.md`: «después preguntar si va en curso», hoy el menú.
- Índice `MEMORY.md`: «¿Paso o tarea? — preguntar si es paso o tarea».

**Arreglo.** Tarea nueva «Podar la memoria de la SF de normas superadas o ya en las skills» (corregir). Alternativa: paso en la 211, si el propietario prefiere decidir antes el mecanismo.

## Hallazgos medios

### 7. `/paso` lo hace el principal

**La orden.** «`/paso` escribe el paso y, además, se lo pide a Claude» (decisión «/paso pone a Claude con el paso», 072); «Encargo de una tarea en curso: a su subagente» (215).

**Qué dice hoy.** `sf:orquestacion`, «Pasos»: «`/paso` llega como mensaje del propietario: hacerlo y seguir». Igual en la rama de la 215.

**Arreglo.** Paso en la 215: «`/paso`, a su subagente».

### 8. La C del panel deja vivo el subagente

**La orden.** Paso de la 205: «Al cerrar una tarea, parar su subagente y quitar su worktree y su rama auxiliar; también al cerrar con la C del panel».

**Qué dice hoy.** La skill: «Al cerrar: parar el subagente, quitar su worktree y borrar sus ramas auxiliares». No dice qué hacer cuando cierra el propietario con la C. `cola.py cerrar` no quita el worktree y no puede parar un subagente.

**Arreglo.** Paso en la 215: «Tarea cerrada desde el panel: parar su subagente y quitar su worktree y sus ramas». Lo detecta «Consultar la cola».

### 9. TURBO y las tareas de la cola

**La orden.** Decisión «Cabecera en dos filas y botón TURBO» (120): «revisa la cola y pon en curso las tareas que se pueden hacer sin interacción con el propietario; lánzalas con subagentes».

**Qué dice hoy.** `sf:orquestacion`: «Al final de cada turno y con TURBO. […] Las de la cola, nunca». La metodología: «pide al principal que revise la cola y lance lo que se puede hacer sin el propietario».

**Choque.** El texto de TURBO pide poner en curso tareas de la cola; la skill lo prohíbe y no dice que el clic sea esa autorización.

**Arreglo.** Pide confirmación del propietario. Paso en la 215: «TURBO: poner en curso, con choques, las de la cola que no necesitan al propietario, y lanzar su subagente».

### 10. Redescribir con el título desfasado

**La orden.** Paso de la 205: «Cuando una tarea acumula pasos y su título queda desfasado, sugerir redescribirla». La memoria «Muchos pasos, una sola cosa» (2026-10-31): «proponer pronto `/redescribir` con un título que lo abarque […]; si pierde el foco […] separar o abrir tarea».

**Qué dice hoy.** La skill: «proponer `/redescribir` […] cuando una tarea acumula pasos y su título queda desfasado» y «`/redescribir NN`: redactar de nuevo […] sin quitar ni añadir». Pero `/redescribir` solo cambia la descripción (decisión «Redescribir: Claude vuelve a redactar una descripción», 126); el título se cambia con `renombrar`. Falta el criterio de deriva. La metodología: «Si el nombre de la tarea deja de reflejar lo que es, Claude la renombra».

**Arreglo.** Paso en la 215: «Título desfasado: proponer título nuevo (`renombrar`) y redescribir; si la tarea pierde el foco, `/split`». Que `/redescribir` proponga también el título lo decide el propietario.

### 11. Cerrar directamente lo que no tiene prueba

**La orden.** Paso de la 205: «Proponer cerrar directamente las tareas que no necesitan prueba» (2026-10-31).

**Qué dice hoy.**
- `sf:orquestacion`: recogida («proponer cerrarla directamente, enseñando el resultado»).
- Metodología, «Probar y cerrar»: «solo propone cerrar sin probar si la prueba necesita el cierre». Contradice.
- Decisión «Probar antes de cerrar» (074): igual que la metodología, sin marca de precisada.
- «Tareas deliberativas» (201) tiene pendiente «Cerrar las tareas documentales con un paso de aprobación en lugar de prueba». Se solapa.
- Sin decisión propia: el porqué cita «propietario, 2026-10-31, 205».

**Arreglo.** Registrar la decisión (hallazgo 14); paso nuevo en la 208, «Reflejar cerrar directamente lo que no tiene prueba»; el propietario decide si el paso de la 201 la sustituye o la completa.

### 12. Las reglas de escritura no llegan a los subagentes

**La orden.** «Textos compactos» (040), «Las descripciones sin origen» (098), «Sin referencias por número que no se vean en pantalla» (150), esta última «aplicarla a […] las skills que escriben textos para el propietario» (paso de la 205).

**Qué dice hoy.** Están en `sf:orquestacion`, «Cómo escribir», que el subagente no carga. El encargo no las incluye. La metodología, «Estructura documental común», no tiene la regla de referencias por número. La 205 cambió las referencias de las skills de documentos, pero no les dio la regla.

**Arreglo.** Paso en la 215: «El encargo lleva las reglas de «Cómo escribir»». El paso de la 208 «Reflejar en la metodología la decisión «Sin referencias por número…»» debe ir a «Estructura documental común».

### 13. Quién escribe el archivo de una decisión

**La orden.** «El principal solo escribe la cola y las decisiones» (149, 151). Antes, el análisis de la 194 vio que commits del principal en la rama de la tarea rompen el `merge --ff-only` del subagente.

**Qué dice hoy.** La skill da las decisiones al principal. En la 215, la decisión la escribió el subagente, en `sub-215`. Si la escribe el principal en la rama de la tarea mientras el subagente trabaja, vuelve el choque de ramas.

**Arreglo.** Pide decisión: el principal la redacta con el propietario y el subagente la escribe en su rama; o va a `develop` al momento (propuesta «Decisiones a develop al momento» del informe «Trabajo con la SF y sin ella», sin decidir). Después, paso en la 215.

### 14. Órdenes sin decisión registrada

**La orden.** CLAUDE.md: «Registrar cada decisión del propietario en cuanto se tome».

**Qué falta.** El porqué de la skill las cita solo como «propietario, fecha»:
- «Ser más agresivo al fusionar tareas y al añadir pasos» (205, 2026-10-31).
- «Proponer cerrar directamente las tareas que no necesitan prueba» (205, 2026-10-31).
- «Cargar sf:orquestacion al empezar la sesión y tras compactar; solo el principal» (205, 2026-10-31).
- «Tareas de definición: proponer con pros y contras, dejar madurar» (190, 2026-10-30).
- «La tarea incluye lo que permite probarla» (2026-10-29).
- «Muchos pasos, una sola cosa; redescribir ante la deriva» (2026-10-31, solo en la memoria).

**Arreglo.** Tarea nueva «Registrar las decisiones de orquestación sin archivo» (documentar), con el hallazgo 15.

### 15. Decisiones superadas sin marcar

**La orden.** «Una decisión por archivo» (108): cada archivo lleva «la línea de sustituida si toca».

**Qué falta.**
- Sin marca de precisada o sustituida: «El principal orquesta; los subagentes ejecutan» (083), corregida por la 149; «El subagente se lanza sin preguntar» (086), que aún dice «Solo pregunta en las triviales, para hacerlas en el principal»; «Lanzar sin esperar lo que no necesita al propietario» (105); «Preguntar antes de cerrar una petición» (048), con «entra `en-cola`, salvo que ya se haya dado el primer paso», sustituido por el menú (139); «Probar antes de cerrar» (074); la 112, con el paso «Documentar: tarea NN», sustituido por la 116 y la 147.
- «Aplicada en» desfasado: la 114 dice «pendiente, tarea 146» y se hizo en la 170; la 139, la 141, la 142 y la 147 citan `flujo_tareas/SKILL.md`, pero sus reglas pasaron a `sf:orquestacion`; la 148 dice «en la tarea de orquestación o en la propia 208».

**Arreglo.** En la tarea nueva del hallazgo 14.

## Hallazgos leves

### 16. Restos en `estados.md`

**Qué dice hoy.** «Estados guardados en la cola»: «Entra así toda petición nueva, salvo que ya se haya dado su primer paso». «Crear en curso»: «o la petición llega con su primer paso ya dado». «Añadir un paso»: «el propietario lo da en el chat («¿paso o tarea?»)». «Crear la rama» y «Lanzar un subagente»: la rama auxiliar solo «si la rama de la tarea está activa»; con la 149, siempre `sub-NN` y siempre `--sin-activar`.

**Arreglo.** En el mismo paso de la 215 del hallazgo 2.

### 17. Los documentos «Cómo funciona» no recogen la skill

**La orden.** CLAUDE.md: «Si cambia una pieza de la SF […] actualizar Cómo funciona la Software Factory».

**Qué dice hoy.** «Cómo funciona la Software Factory», ficha «Skills»: lista el flujo de tareas, no la orquestación. La 205 no creó su tarea «Actualizar». «Cómo funcionan los estados»: «en una rama auxiliar si hace falta».

**Arreglo.** Tarea nueva «Actualizar Cómo funciona la Software Factory», con el paso «Reflejar «Skill de orquestación» (205)». «Cómo funcionan los estados», en su propia tarea «Actualizar», con el paso «Reflejar «Skill de orquestación» (205)».

### 18. El «→» del Registro en la plantilla

**La orden.** «Las mejoras de la SF pasan a tarea solo desde la SF» (146), en «Convertir mejoras en tareas solo desde la SF» (195).

**Qué dice hoy.** La plantilla, que llega a todos los proyectos: «donde el propietario lo borra o, con «→», lo convierte en tarea en cola sin Claude».

**Arreglo.** Paso nuevo en la 208: «Reflejar «Convertir mejoras en tareas solo desde la SF» (195) en la plantilla».

### 19. Referencias por número en la plantilla y el CLAUDE.md

**La orden.** «Sin referencias por número que no se vean en pantalla» (150).

**Qué dice hoy.** Plantilla: «(metodología, 1)», «(metodología, 2)», «(metodología, 6)». CLAUDE.md: lo mismo y «(especificación, sección 1)».

**Arreglo.** Ampliar el paso de la 208 sobre la 150 a la plantilla y el CLAUDE.md.

### 20. El encargo no pide qué documentar

**La orden.** Memoria «Documentar aparte»: «en los encargos a subagentes, prohibir tocar esos documentos y pedir que digan qué hay que documentar».

**Qué dice hoy.** El encargo prohíbe tocarlos; el informe no pide qué documentar.

**Arreglo.** Paso en la 215: «El informe dice qué documentos compartidos hay que actualizar».

### 21. El porqué cita la norma superada

**Qué dice hoy.** `references/porque.md`, «Papel del orquestador», también en la rama de la 215: «Lo que no necesita al propietario no le ocupa («Lanzar sin esperar lo que no necesita al propietario», 105)».

**Arreglo.** Paso en la 215: quitar o reescribir esa frase.

### 22. Registro de uso desfasado

**Qué dice hoy.** Entrada del 2026-10-29: «Una tarea en curso que no necesita al propietario se lanza en cuanto puede empezar».

**Arreglo.** El propietario la borra desde el panel; ya está recogida y superada.

## Pasos y tareas propuestos

**En la 215** «La orquestación deja todo el trabajo de la tarea al subagente, también el análisis»:
- Alinear las tarjetas «Lanzar un subagente», «Volver de un subagente» y «Reabrir» de `estados.md`, y los restos de «salvo primer paso», «¿paso o tarea?» y la rama auxiliar.
- `/paso`, a su subagente.
- Tarea cerrada desde el panel: parar su subagente y quitar su worktree y sus ramas.
- TURBO: poner en curso, con choques, las de la cola que no necesitan al propietario, y lanzar su subagente (tras confirmarlo).
- Título desfasado: renombrar y redescribir; si pierde el foco, `/split`.
- El encargo lleva las reglas de «Cómo escribir» y el informe dice qué documentar.
- Documentos compartidos y archivo de la decisión, según decida el propietario.
- Quitar del porqué «Lo que no necesita al propietario no le ocupa».
- Después: publicar, con el OK del propietario.

**En la 208** «Actualizar las reglas del método: metodología, plantilla y CLAUDE.md», justo tras la 215:
- El paso de la 215, nombrando la plantilla y el CLAUDE.md.
- El de la 205, con «Orquestación con subagentes», «Cuándo lanzar» y la regla «Cola de peticiones» del SKILL.md sustituidos por una remisión.
- Nuevo: cerrar directamente lo que no tiene prueba.
- Nuevo: el «→» del Registro, solo en la SF.
- El de la 150, ampliado a «Estructura documental común», la plantilla y el CLAUDE.md.

**Tareas nuevas:**
- «Podar la memoria de la SF de normas superadas o ya en las skills» (corregir).
- «Registrar las decisiones de orquestación sin archivo» (documentar), con las marcas de precisada y los «Aplicada en».
- «Actualizar Cómo funciona la Software Factory» (documentar).
- «Actualizar Cómo funcionan los estados» (documentar).

## Lo que debe decidir el propietario

- **Documentos compartidos:** ¿excepción en el principal o subagente, de una en una?
- **TURBO:** ¿su clic autoriza poner en curso tareas de la cola?
- **Cerrar sin prueba:** ¿cerrar directamente o con el paso de aprobación de la 201?
- **Archivo de la decisión:** ¿lo escribe el subagente en su rama o va a `develop` al momento?
- **Memoria:** ¿podarla ahora o esperar al mecanismo de la 211?
- **Orden:** cerrar la 215, publicar y hacer la 208 enseguida, o dejar que la 215 corrija ya las dos líneas de la plantilla y el CLAUDE.md.

## Órdenes recogidas bien

| Orden | Origen | Dónde está |
| --- | --- | --- |
| Toda petición, bug o error, a la cola al llegar | 031, 077, 096 | Skill, plantilla, CLAUDE.md |
| Bug: reabrir su tarea si se localiza | 061, 096 | Skill y `estados.md` |
| Menú al anotar: paso, en curso o en cola | 197, 139 | Skill y `estados.md` |
| Menú breve, sin preguntar lo ya dicho | 197, 2026-10-31 | Skill y `estados.md` |
| Tipo al crear la tarea | 196, 145 | Skill y flujo de tareas |
| Agresivo con pasos y fusiones | 205 | Skill (falta decisión) |
| La tarea incluye lo que permite probarla | 2026-10-29 | Skill (falta decisión) |
| Sin tarea en curso no se trabaja, salvo reorganizar | 200, 205 | Skill y flujo de tareas |
| Consultar la cola antes de informar o actuar | 205, 149 | Skill |
| Especificar y planificar al poner en curso | 205, 149 | Skill |
| Choques al poner en curso | 112, 130 | Skill y flujo de tareas |
| Todo lo hecho, como paso | 205, 2026-10-31 | Skill |
| Definir y decidir son pasos; participio | 080, 081 | Skill y metodología |
| Mejorar la skill que se usa es un paso | 094 | Skill y metodología |
| Subagente vivo hasta el cierre, también en la prueba | 205, 149 | Skill |
| Encargo con descripción «Tarea NN: …» | 119, 146 | Skill y metodología |
| Compartir archivos no frena; las de la cola, no se lanzan | 105 | Skill y metodología |
| Rama auxiliar `sub-NN` y `merge --ff-only` | 115, 149 | Skill y flujo de tareas |
| Recoger al subagente en cuanto vuelve | 205, 149 | Skill |
| Solo el principal escribe la cola | 083, 110 | Skill y flujo de tareas |
| Borrar las ramas del subagente | 176, 135 | Skill y flujo de tareas |
| `listo --prueba` sin esperar | 205, 149 | Skill |
| Proponer probar, con cómo | 074 | Skill y metodología |
| Cierre, Testing, probada y publicación esperan el OK | 048, 050 | Skill y flujo de tareas |
| Commits en la rama, sin preguntar | 2026-10-29 | Skill y metodología |
| «Probada» sin número: la rama activa | 095 | Skill y metodología |
| Pregunta de Testing: Probada, Pendiente, Probar ahora | 050, 051 | Skill |
| Lo comprobado por Claude, a `comprobado` | 050 | Skill y flujo de tareas |
| Un cierre que falla llega del panel | 111 | Skill y flujo de tareas |
| Sugerir `/fusionar` y `/split` con la orden lista | 100 | Skill y flujo de tareas |
| Tras sugerir una fusión, proponer redescribir | 197, 141 | Skill |
| Una tarea por documento, un paso por tarea | 197, 142, 147 | Skill |
| Las tres reglas del método, en una tarea | 148 | Skill y CLAUDE.md |
| Libre: desbloquear las en curso, no las de Testing | 102 | Skill y metodología |
| Preguntas: una por tarea, cuatro como mucho | 051 | Skill y metodología |
| Cargar la skill al empezar y tras compactar, solo el principal | 205 | Skill, plantilla, CLAUDE.md |
