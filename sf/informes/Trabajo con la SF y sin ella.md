---
antetitulo: Software Factory · Informe de análisis · Octubre 2026
lema: Seis días con la SF, // y lo que dicen los datos.
subtitulo: Cómo se ha trabajado al desarrollar el panel, y una comparación con OncoCore, que no usa la SF.
version: Versión 1.0 · 31/10/2026
estado: Análisis · Tarea 194
portada: oscura
destino: proyecto
herramientas: buscador lectura fuentes cabecera tablas
tipo: Informe de análisis
pie: Informe de análisis de la Software Factory. Las cifras salen de la cola, git, el registro de uso y las sesiones de Claude Code; las propuestas esperan la decisión del propietario.
---
# El trabajo con la SF

> [!aviso]
> Los proyectos comparados son muy distintos y la SF lleva solo seis días en uso. Las diferencias orientan; no demuestran.

## Resumen | Más orden, más trazas y una fricción nueva | Resumen {#resumen}

Con la SF, el trabajo queda partido en cambios pequeños, cada uno con su tarea y sus decisiones registradas. El coste es el ritual que rodea cada cambio pequeño, unos 3-4 minutos por un retoque de una línea, y unas reglas de orquestación que todavía viven en la memoria de Claude y no llegan a los demás proyectos. Lo que más lo abarata es un subagente vivo por tarea en curso.

::: tarjetas 3

### Commits

**47** líneas por commit
{: .metrica}

La mitad de los commits de la SF tienen 47 líneas o menos. En OncoCore, 1.620.

### Decisiones

**144** registradas
{: .metrica}

Cada una en su archivo, con las palabras del propietario y su porqué. En OncoCore, ninguna.

### Ritmo

**315** commits en 6 días
{: .metrica}

Con el pico el 27 de octubre: 116 commits en un día.

:::

## Propuestas | Lo que se propone a valorar | Propuestas {#propuestas}

Siete propuestas, para que el propietario decida cuáles pasan a la cola. Salen de la valoración, del tamaño de las tareas y del balance que siguen. La primera ya es una tarea y la cuarta está decidida.

1. **Skill de orquestación.** Las reglas de comportamiento, en una skill que llega a los proyectos: un subagente vivo por tarea en curso que hace todos sus cambios, cerrar la tarea para el subagente y quita su worktree, y el principal consulta la cola antes de informar o actuar. Ya es la tarea «Skill de orquestación» (205); que las normas de la memoria lleguen a todos los proyectos, la 211.
2. **Decisiones a develop al momento.** Numeradas al entrar en develop, no al escribirlas: resuelve los choques de números y las decisiones atrapadas en ramas.
3. **Choques con lo previsto.** `choques` con los archivos previstos de las tareas sin commits, no solo los de git.
4. **Documentación, una vez por tarea.** Una tarea por documento, «Actualizar» y su nombre, con un solo paso «Reflejar «título» (NN)» por tarea, no uno por retoque: «Actualizar Cómo funciona el panel» (198) llegó a 19 pasos casi iguales. Decidido: «Documentación, una vez por tarea» (147).
5. **Más fusiones y más pasos.** Ser más agresivo al fusionar tareas y al añadir pasos, para que los cambios pequeños no sean tareas sueltas: paso si es del mismo tema y archivos y el título sigue valiendo; tarea nueva o redescribir si no; a partir de unos 10 pasos o de una sesión, integrar develop antes de probar. Y copias de la cola solo al cambiar de estado. Propuesta del propietario: «muchos commits de tareas muy pequeñas y afines son en realidad un mal uso del método y del panel».
6. **Permisos distribuidos.** Una lista con las órdenes que la SF usa siempre, para que no pidan permiso.
7. **Diagnóstico de incorporación.** En cada proyecto, con la versión de la SF y lo que le falta, a la vista en el panel.

## Comparación | Con la SF y sin ella: mi valoración | Comparación {#comparacion}

Las cifras de los dos lados no se pueden comparar de tú a tú, así que esto es una valoración de Claude, por inferencia sobre los datos y sobre cómo se ha trabajado. Las tablas están al final, en el anexo de datos.

La diferencia de fondo no es de velocidad, sino de **memoria del proyecto**. En OncoCore, el porqué de cada cambio vive en conversaciones de once horas y en commits como «Varios»: quien vuelve al código tiene que reconstruirlo. Con la SF, cada cambio sabe de qué tarea viene y cada decisión tiene su archivo con su porqué. Es lo que más pesa a favor, y crece con la vida del proyecto.

La SF cambia la forma de trabajar: de **una conversación larga que produce código** a **una cola de cambios pequeños, comprobados y probados**. Eso da orden: nada entra en develop sin el OK del propietario y varias líneas avanzan en paralelo sin pisarse. El control y el foco sobre ese trabajo los da el panel, que es su objetivo. En OncoCore, con commits de miles de líneas, revertir un error es casi imposible; con la SF, es una orden.

El precio es **la gestión**. Para cambios de minutos, crear la tarea, su rama, sus pasos, su prueba y su cierre pesa a veces más que el cambio. En los ajustes visuales del 31 de octubre, cada retoque de una línea costaba un paso en su tarea, otro en la del documento, el encargo, la espera, traerlo, marcarlo y avisar: unos 3-4 minutos. Los commits pequeños no son el problema, porque el squash los junta; lo es **el ritual alrededor**. Se mitiga siendo más agresivo al fusionar tareas y al añadir pasos, con la documentación una vez por tarea y con un subagente vivo que encadena los ajustes. Ese coste se nota más en un ejercicio corto, como Sprites, que en un producto largo.

Sobre la calidad del producto, no me atrevo a afirmar nada. Que se pruebe antes de cerrar y que la prueba encuentre errores indica rigor, pero no hay datos de errores en producción en ninguno de los dos lados.

> **Mi valoración**
> La SF compensa en los proyectos del propietario: largos, de riesgo, con varias líneas a la vez y decisiones que hay que recordar meses después. El riesgo es que la SF se dedique más a diseñarse a sí misma que a servir a los proyectos. La prueba de verdad será un producto como OncoCore o SmartColdBox en una fase larga de desarrollo.

## Tamaño | Tareas de pocos pasos y de muchos | Tamaño {#tamano}

Ni las tareas de pocos pasos ni las de muchos salen gratis: las pequeñas multiplican el ritual y las grandes pierden el título y se separan de develop. Entre el 29 y el 30 de octubre, el panel avanzó con tareas de 3 a 5 pasos que se cerraban en una mediana de unos 4 minutos. Cada una pagaba su alta, sus choques, su rama, su prueba, su cierre y su paso en la documentación, aunque fuera un cambio de una línea. De ahí salieron tareas solo para documentar, como «Documentar la copia de cola.py del panel» (182), y fusiones a posteriori.

El 31 se fue al otro extremo. «Margen de una columna a la derecha del panel» (196) acabó con 30 pasos: además del margen, quitó letras, dejó cada tarea en una sola sección, cambió el despliegue y las sangrías, y llevó el tipo de tarea a `cola.py` y a la skill. Con un solo subagente, una rama, un cierre y un squash, el ajuste fue fluido, pero el título dejó de describir la tarea. Además, la rama, abierta desde la tarde anterior, chocó con develop en la skill del flujo de tareas al cerrar. En el término medio, «Mismo diseño de tarea en todas las secciones del panel» (210) nació para un cambio y cerró con 9 ajustes en unos 25 minutos, sin choques ni reaperturas.

| Aspecto | Pocos pasos (29-30 de octubre) | Muchos pasos (31 de octubre) |
|---|---|---|
| Ritmo | 3-5 pasos y unos 4 min por tarea; el ritual pesa tanto como el cambio | 9 pasos en 25 min (210) y 30 en una tarde (196), con un subagente que conserva el contexto |
| Documentación | Una tarea de documentación por cambio; luego, fusionarlas | Un paso por retoque: 19 casi iguales en la 198, hasta la decisión «Documentación, una vez por tarea» (147) |
| Trazas | Un squash por cambio, fácil de revertir | Un squash con 30 cambios; el título ya no dice lo que hay dentro |
| Riesgo | 2 de 8 se reabrieron en la prueba | La rama se separa de develop: un cierre fallido por choque y una prueba de la 195 con el diseño viejo |
| Fusiones | 3 en un día: la 200 en la 205, la 199 y la 207 en la 208, con los mismos 4 pasos triplicados | El propietario no fusionó la 205 con la 211: «se harán muy largas» |

La regla práctica que sale de estos casos es sencilla. **Mismo tema y mismos archivos, y el título lo sigue describiendo: paso.** Si el título deja de describirla, se separa o se redescribe. Y si la tarea pasa de unos 10 pasos o de una sesión, se integra develop en la rama antes de probarla. El límite es orientativo: sale de pocas tareas, en un solo proyecto.

## El panel | Desarrollado con la propia SF | El panel {#panel}

El panel fue a la vez lo que se construía y la primera prueba del método. Su objetivo, distinto del de la SF, es **el control y el foco**: tener a la vista qué está en curso, qué espera prueba y qué toca ahora. Se hizo con tareas muy pequeñas: de la creación al cierre, una mediana de 6 minutos y 4 pasos.

::: tarjetas 3

### Tareas

**42** creadas
{: .metrica}

17 cerradas, 4 eliminadas, 3 absorbidas por una fusión, 2 descartadas y 1 revertida. Quedan 21 abiertas: 13 en cola, 6 en curso y 2 en Testing.

### Quién mueve la cola

**283** cambios de Claude
{: .metrica}

Frente a 134 del propietario. Por el CLI, 354; desde el panel, 63.

### Pasos

**164** movimientos
{: .metrica}

Añadir, marcar y quitar pasos es, con diferencia, lo que más se hace en la cola.

:::

### Lo que ha funcionado

La base funciona: **el CLI de la cola** reconstruye solo el historial de cada tarea, y sus copias y sus choques evitan pérdidas. **Las decisiones se registran al momento**, con las palabras del propietario y su porqué: el 30 de octubre salieron cuatro, cada una trazable a su tarea, y el 31, en plena tarea, «Cada tarea, en una sola sección del panel» (144) y «Cada tarea tiene un tipo» (145).

Los subagentes trabajan en su propio worktree, y lo que mejor ha funcionado es **un subagente vivo por tarea en curso**: el principal le pasa cada encargo del propietario con `SendMessage` y el subagente conserva el contexto del código y de las pruebas. En «Margen de una columna a la derecha del panel» (196), uno solo hizo unos 12 ajustes seguidos en unas 2,5 horas, con unos 360.000 tokens; en «Mismo diseño de tarea en todas las secciones del panel» (210), 9 ajustes en unos 25 minutos, con unos 130.000. Mientras, el principal queda libre para la cola, las decisiones y el propietario, que lo valora como «una gran ventaja».

La calidad se cuida desde el principio, porque **se prueba antes de cerrar**. Todas las tareas cerradas desde el 29 de octubre se cerraron con el OK del propietario, y 11 de las 12 reales, con la comprobación de Claude antes. En 5, el propietario activó la rama con T y la probó él, y dos de esas cinco se reabrieron: la prueba encuentra lo que la comprobación no ve. En los ajustes visuales, activar con T y recargar el panel dio un ciclo de prueba muy corto.

Y la herramienta mejora con el uso, porque **las fricciones se detectan y se corrigen**. El registro de uso recoge las de otros proyectos, y SpriteAnimation y Sprites aportan 9 de sus 12 entradas. En este mismo análisis, los menús que cansan y las tareas de documentación en serie quedaron resueltos el mismo día, en la tarea 197. Cuatro decisiones del 30 y el 31 de octubre salieron de fricciones del uso: el menú al anotar, redescribir tras una fusión, una tarea por documento y la documentación una vez por tarea.

> «Noto mejor ordenamiento y control.» El propietario, sobre el panel, en el registro de uso.

### Deficiencias

Diez deficiencias, cada una con su medida y en qué punto está. Dos ya están resueltas y tres van en la tarea «Skill de orquestación» (205).

| Deficiencia | Medida | Estado |
|---|---|---|
| **Las reglas no viajan.** Salen en el chat y acaban repartidas entre la memoria de Claude, `CLAUDE.md`, la metodología y la skill del flujo de tareas. La memoria va por proyecto: las normas guardadas en la de la SF no se aplican en los demás. | Una skill de orquestación que viaja en el plugin y se aplica en cada mensaje; las normas de la memoria, en todos los proyectos. | Tareas 205 y 211, en cola |
| **El principal y el subagente en la misma rama.** Si el principal hace commits en la rama de la tarea mientras el subagente trabaja, la rama auxiliar ya no se trae con fast-forward: 3 rebases o resets en la 196. Cerrar la tarea tampoco paraba el subagente ni quitaba su worktree: se hizo a mano. | Todo cambio de una tarea con subagente, por su subagente; cerrar la tarea lo para y quita su worktree. | Pasos de la 205 |
| **El principal no mira la cola.** Dos veces actuó sobre tareas que el propietario ya había cerrado desde el panel: avisó de un choque con la 195 y llevó una decisión a la rama de la 210. Y un subagente terminó sin que el principal trajera su trabajo ni marcara sus pasos, los 4 y 5 de la 195, hasta que el propietario lo vio en el panel. | Consultar la cola antes de informar o actuar, y recoger el trabajo del subagente en cuanto termina. | Paso de la 205 |
| **Menús que cansan.** El propietario rechazó dos el 30 de octubre. | Menú breve, sin preguntar lo que el propietario ya ha dicho. | Resuelta en la 197 |
| **Tareas de documentación en serie.** Cada cambio abría la suya y luego había que fusionarlas; con una tarea por documento, cada retoque seguía siendo un paso: la 198 llegó a 19 casi iguales. | Una tarea por documento, con un solo paso por tarea. | Resuelta en la 197 y en «Documentación, una vez por tarea» (147) |
| **Una rama de prueba desfasada.** La rama de la 195 era anterior al cierre de la 196, y al probarla el panel volvió al diseño viejo: una recarga confusa. | Integrar develop en la rama antes de probarla. | Sin tarea |
| **Números de decisión que chocan.** Cada rama numera con lo que ve y el índice se regenera en todas. | En la rama, la decisión va sin número; se numera al entrar en develop. | Sin tarea |
| **Choques que no se ven.** `choques` no ve los archivos de una tarea sin commits. | Que `choques` use también los archivos previstos de cada tarea. | Sin tarea |
| **Windows.** Una rama no puede llamarse `aux/…` y un worktree no se borra si el shell sigue dentro. | Evitar los nombres reservados al crear ramas y salir del worktree antes de quitarlo. | Sin tarea |
| **El ciclo probado sobre sí mismo.** 7 reversiones y 6 reaperturas, la mitad en tareas de prueba del botón R. | Probar el ciclo en una copia de la cola, no en la de verdad. | Sin tarea |

## Observaciones | Lo nuevo que sale de la comparación | Observaciones {#observaciones}

La comparación saca a la luz cinco fricciones que el análisis del panel no veía.

::: tarjetas 2

#### Recargar el plugin, solo en la SF

Es la mayor fricción mecánica de la SoftwareFactory, pero solo mientras se desarrolla el propio plugin: los proyectos que lo usan no lo recargan. En sus sesiones aparecen unas 705 veces `/reload-plugins`, 254 `/rename` y 100 `/color`, frente a 34 `/paso`, 26 `/fusionar` y 14 `/split`. Las cifras pueden contar repeticiones, pero el orden de magnitud es claro.

Medida
:   Que el panel avise cuando cambian los archivos del plugin, y recargar solo entonces.

Estado
:   No afecta a los proyectos: es propio del desarrollo de la SF.

#### Rechazos de herramientas

26 en la SoftwareFactory frente a 8 en OncoCore. Conviene revisar qué órdenes de la SF, como git, `cola.py` o escribir en `.sf/`, piden permiso.

Medida
:   Una lista de permisos con las órdenes que la SF usa siempre, distribuida con el plugin.

Estado
:   Sin tarea.

#### Decisiones atrapadas en ramas

Sprites tiene 4 decisiones en dos ramas de tarea y ninguna en develop, además de una rama auxiliar sin borrar. Con tareas en paralelo, una decisión no se ve hasta que su tarea se prueba.

Medida
:   Llevar cada decisión a develop en cuanto se toma.

Estado
:   Sin tarea; va con los números de decisión que chocan.

#### Trabajo muy troceado

El 19 % de las tareas de la SoftwareFactory acabó absorbida, eliminada o descartada, 11 se redescribieron y se guardaron 50 copias de la cola en un día. Gestionar tareas cuesta mucho para cambios pequeños.

Medida
:   Más fusiones de tareas y más cambios como pasos.

Estado
:   En parte, la tarea 197, con menús más breves, y la decisión «Documentación, una vez por tarea» (147). La medida la propone el propietario.

#### Incorporaciones a medias

SmartColdBox sigue en la versión 0.13 de la SF, JKanban no tiene `docs/decisiones/` y la propia SoftwareFactory no tiene `.sf/proyecto.json`.

Medida
:   Un diagnóstico de cada proyecto, con su versión de la SF y lo que le falta, a la vista en el panel.

Estado
:   En parte, la tarea 47, «Incorporar proyecto: menú con el caso detectado», en Testing. No muestra en el panel qué le falta a cada proyecto.

:::

## Límites | Lo que no se puede concluir | Límites {#limites}

La comparación orienta, pero no prueba que la SF sea la causa de las diferencias.

- **Proyectos distintos:** OncoCore es un producto clínico con datos pesados, de ahí sus commits enormes. La SoftwareFactory se construye a sí misma, y Sprites y sprite_animation son ejercicios docentes.
- **Muy poco tiempo con la SF:** 6 días en la SoftwareFactory y 1 en el resto. Ningún proyecto con la SF tiene aún una fase larga de desarrollo y mantenimiento.
- **Faltan datos de OncoCore:** sus sesiones empiezan el 23 de septiembre: de abril a junio no hay ninguna, y de OncoCore_app no hay mensajes legibles.
- **El caso más sesgado:** en la SoftwareFactory, el propietario usa el método y lo diseña a la vez, y muchos mensajes tratan del propio método.
- **La calidad no se ha medido:** no hay datos de pruebas ni de errores en producción en ningún proyecto.

## Anexo A · Datos | Las cifras de la comparación | Datos {#datos}

Las cifras de cada proyecto, para consultarlas. Los proyectos son muy distintos: las tablas informan la valoración, no la demuestran.

### git

| Proyecto | Commits / días activos | Commits al día |
|---|---|---|
| OncoCore (sin SF) | 41 / 16, de abril a octubre | 2,6 |
| OncoCore_app (sin SF) | 12 / 8, de mayo a junio | 1,5 |
| SoftwareFactory | 320 / 6 | 53 |
| SmartColdBox, antes → después | 78 / 4 → 22 / 1 | 20 |
| JKanban, antes → después | 42 / 4 → 10 / 1 | 10 |
| Sprites / sprite_animation | 9 / 1 y 7 / 1 | 8 |

| Proyecto | Líneas por commit (mediana) | Commits de corrección |
|---|---|---|
| OncoCore | 1.620 (media 59.000) | 15 % |
| OncoCore_app | 32.000 | 25 % |
| SoftwareFactory | 47 | 3 % |
| JKanban, antes → después | 78 → 306 | 26 % → 10 % |
| SmartColdBox | 117 | 1 % |
| Sprites / sprite_animation | 58 / 72 | 0 % |

OncoCore y OncoCore_app tienen 5 ramas cada uno, sin ramas de tarea ni tags, y mensajes como «Varios» o «Disconf Varias». La SoftwareFactory tiene 5 ramas de tarea y los tags v1.0.0 y v1.1.0, y sus mensajes dicen lo que cambia y llevan la tarea. De sus 5 reversiones de git, 3 deshacen pruebas del botón R: las de trabajo real son 2, menos del 1 %.
{: .texto}

### Documentación

| Proyecto | docs/ y CLAUDE.md | Decisiones |
|---|---|---|
| OncoCore | `_docs/` con 453 archivos sin estructura común; CLAUDE.md de 553 líneas | Sin registro; repartidas por catálogos |
| OncoCore_app | `doc/` técnica; sin CLAUDE.md | Ninguna |
| SoftwareFactory | 198 archivos: specs, guías, propuestas; CLAUDE.md de 37 líneas | 144, una por archivo |
| SmartColdBox | Specs e identidad; CLAUDE.md de 40 líneas | Un archivo antiguo sin migrar |
| JKanban | 55 archivos técnicos; CLAUDE.md de 115 líneas | Sin `docs/decisiones/` |
| Sprites / sprite_animation | Esqueleto de la SF; CLAUDE.md de 5 líneas | Ninguna en develop: están en ramas |

### Sesiones de Claude Code

| Proyecto | Sesiones · mensajes del propietario | Duración por sesión (mediana) |
|---|---|---|
| OncoCore | 10 · 673 | 11,1 h |
| SmartColdBox | 6 · 163 | 11,5 h |
| SoftwareFactory | 15 · 927 | 1,9 h |
| JKanban | 4 · 34 | 1,3 h |
| Sprites / sprite_animation | 2 · 12 y 1 · 17 | 0,5 h y 1,5 h |

| Proyecto | Correcciones / avisos de fallo | Interrupciones / rechazos |
|---|---|---|
| OncoCore | 0,6 % / 2,1 % | 2,7 % / 8 |
| SmartColdBox | 0,6 % / 1,8 % | 0,6 % / 5 |
| SoftwareFactory | 1,1 % / 1,1 % | 1,9 % / 26 |
| sprite_animation | 1 de 17 / 0 | 0 / 1 |

Las correcciones y los avisos se cuentan con filtros de texto estrictos, como «No,…», «te he dicho», «no funciona» o «falla»: son una aproximación. Peticiones repetidas: OncoCore 16, SoftwareFactory 8, SmartColdBox 4.
{: .nota}

## Anexo B · Fuentes | De dónde salen las cifras | Fuentes {#fuentes}

Todas las cifras salen de lo que los proyectos ya guardan: no se ha preguntado nada ni se ha medido nada aparte.

- **Cola e historial de tareas:** `.sf/peticiones.json` y `.sf/historial.jsonl` de cada proyecto con la SF. El historial por tarea solo existe desde la tarea 161 de la SF, el 29 de octubre.
- **git:** commits, ramas, tags, tamaño de cada cambio y mensajes.
- **Decisiones y documentos:** `docs/decisiones/` y la estructura de `docs/`.
- **Registro de uso:** `.sf/registro.json` de la SF: 12 entradas, 10 fricciones, 1 acierto y 1 dicho del propietario.
- **Sesiones de Claude Code:** las guardadas por Claude Code para cada proyecto: sesiones, mensajes del propietario, duración y señales de fricción.

Sin la SF se comparan **OncoCore** y **OncoCore_app**. Con la SF, **SoftwareFactory**, **SmartColdBox**, **JKanban**, **Sprites** y **sprite_animation**. SmartColdBox y JKanban se incorporaron el 27 de octubre, así que tienen un antes y un después.
{: .texto}
