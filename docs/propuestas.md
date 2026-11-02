# Propuestas para la Software Factory

Ideas de mejora de la SF **sin decidir**: no son reglas. Al aprobarse, la decisión pasa a [decisiones](decisiones/README.md), se aplica a la [metodología](../plugins/sf/skills/metodologia/references/desarrollo-de-proyectos.md) o a la [especificación](specs/funcional/software-factory.md), y su entrada sale de aquí. Si se descarta, queda en «Descartadas» con el motivo.

Es el registro de la tarea permanente **Mejorar la Software Factory**, activa, pendiente de vincular al kanban cuando se disponga de acceso.

**Cada propuesta lleva un número fijo,** en su título, con dos cifras: `### P<nn> <título>` (P01, P02…), con el primer número libre (el mayor usado más uno). No cambia aunque se decidan otras, y no se reutiliza al decidirse o descartarse (acuerdo del propietario, 2026-10-28). Así se puede nombrar una propuesta por su número («la P07») sin confundirla con una petición.

**Cada propuesta recoge:** origen (proyecto, fecha y palabras del propietario), tipo, observación y evidencia, cambio propuesto, beneficio e impacto, verificación prevista e información que falta, si hay.

**Su tipo** va en su línea `- **Tipo:**`, tras el origen: el de la tarea que haría falta para llevarla a cabo, uno de los de la cola (deliberar, documentar, diseñar, implementar, especificar, corregir o investigar). Lo pone Claude al registrarla, por su contenido. El «→» de Mejoras lo pasa a la tarea que crea; sin tipo, o con otro, la tarea se crea sin él.

**Su estado** va en su línea `- **Estado:**`: «propuesta, pendiente de aprobación» o «de decisión» mientras está por decidir, y así sale en Mejoras del panel. «Pasada a la tarea N de la cola el <fecha>» cuando se ha convertido en la tarea N con el «→» de Mejoras, que lo escribe solo en la SF: su seguimiento sigue en la cola y deja de salir en Mejoras (decisión «Las mejoras de la SF pasan a tarea solo desde la SF»). Lo contrario es «A propuesta» (etiqueta del panel en una tarea en cola, o `cola.py a-propuesta N`): saca la tarea de la cola y devuelve su propuesta a «propuesta, pendiente de aprobación» o, si no salió de ninguna, crea una nueva.

Proyecto de destino en el kanban: **SoftwareFactory**. Tanto la tarea permanente como las tareas concretas de mejora continua pertenecen a ese proyecto.

## Propósito

Identificar y proponer mejoras basadas en la experiencia. Consultar al iniciar o retomar trabajo en la SF y revisar las observaciones al cerrar un entregable relevante.

La tarea permanente permanece activa. Las propuestas concretas pueden aprobarse, implementarse, comprobarse y cerrarse por separado.

## Mejoras detectadas en otros proyectos

La observación de automejora acompaña el uso de la SF en cualquier proyecto consumidor. Aunque una mejora se detecte durante el desarrollo de otra aplicación, su tarea se registra en el proyecto **SoftwareFactory** del kanban.

Conservar el nombre y la referencia del proyecto de origen, la devslice o tarea relacionada cuando exista y la evidencia que motivó la propuesta. Las correcciones propias de la aplicación permanecen en su proyecto; si además revelan una mejora general del método o de sus herramientas, crear una tarea vinculada en **SoftwareFactory**.

Si el kanban no está accesible, guardar la propuesta como pendiente de traslado a **SoftwareFactory** y confirmar después su registro. No afirmar que ya existe una tarjeta. Detectar una mejora desde otro proyecto no autoriza modificar ni distribuir la SF: sigue siendo necesaria la aprobación del propietario.

## Aprobación

Solicitar aprobación explícita del propietario antes de aplicar cada cambio de automejora. Registrar observaciones y preparar propuestas no autoriza su implementación. Los cambios solicitados directamente por el propietario están autorizados dentro del alcance de su petición.

## Propuestas pendientes

### P01 Incorporar lo aprendido en proyectos anteriores

- **Origen:** SoftwareFactory, 2026-10-27. Tras ver que la norma de diagramas en SVG de OncoCore no había llegado a la SF: «Parece que nos hemos dejado algo de trabajo realizado por el camino recorrido hacia la sf...».
- **Tipo:** deliberar.
- **Observación y evidencia:** un inventario de OncoCore (sobre todo su `CLAUDE.md` y la memoria de Claude del proyecto), PoseTracker, SmartColdBox, JKanban, SocratIX, LecturaFàcil y MedRol encontró unas 40 reglas, convenciones y herramientas generales que la SF no recoge o recoge solo en parte. Detalle, con rutas y estado de cada una: [inventario del 2026-10-27](referencias/inventarios/herencia-proyectos-2026-10-27.md).
- **Bloques:**
  - A. Forma de trabajar con el propietario y con Claude: una corrección es ejemplo de una regla y se barre todo; exponer el riesgo antes de cambiar; orden de ataque; crítica honesta; afirmaciones verificadas contra el código; tablas para comparar; perfil y ritmo del propietario; postura de arquitecto; generalizar antes que parchear.
  - B. Documentación y memoria: qué va a memoria, a `CLAUDE.md` o a una skill; plantilla de `CLAUDE.md` de proyecto; documentos de diseño solo con el estado vigente; entregables siempre en `docs/`; documento «dónde estamos» por subproyecto; índice de `docs/` generado; catálogo antes de un cambio masivo; detalles de accesibilidad y color que faltan en la guía de diagramas.
  - C. HTML e informes: principios y ficha de `diseno_documentos`; verificar HTML sin ventana; actualizar y no regenerar un documento repartido; fuentes desde un catálogo; informes plegables.
  - D. Skills y herramientas: versión por skill e historial; hook que no carga en la sesión que lo crea; skills que solo se ejecutan cuando se piden; ejemplos solo de conjuntos cerrados; toda skill aprende de las correcciones; nombres de comandos y archivos (choca con la convención actual de la SF: hay que decidir); línea de estado con contexto y tokens.
  - E. Arquitectura, pruebas y agentes: determinismo antes que inferencia; contrato canónico para el JSON entre fronteras; pruebas de guarda y de arquitectura; matices de MVP; puerta humana en apps con agente; pruebas contra BD real y sin SQL; configuración en `.ini` y secretos en `.env`.
  - F. Git, seguridad y entorno: ramas, `CHANGELOG` y PR que fusiona el propietario; escapar contenido en `innerHTML` y nada confidencial en repos públicos; trucos de Windows y PowerShell.
- **Cambio propuesto:** revisar los bloques con el propietario, uno a uno, y decidir por cada entrada si entra en la metodología, en una skill, en una plantilla o en el perfil del propietario, o si se descarta. Lo propio de un dominio (vault de OncoCore, reglas clínicas, PoseTracker, SQL de JKanban) no entra.
- **Incoherencias encontradas, fuera de la SF:** las de SmartColdBox (enlaces rotos en su `CLAUDE.md` y sin `.sf/`) se corrigieron el 2026-10-27. Dos memorias antiguas de OncoCore describen una política de despliegue anterior.
- **Información que falta:** el orden de revisión y qué bloques interesan primero.

### P02 El detalle, solo cuando está claro

- **Origen:** SoftwareFactory, revisión de la visión (sección «En qué se diferencia de lo que ya existe»), 2026-10-26. El propietario pidió registrarla como propuesta.
- **Tipo:** documentar.
- **Observación y evidencia:** el propietario trabaja en emprendimientos arriesgados que nacen de cero y prefiere «trabajar en profundidad la visión del proyecto antes de realizar especificaciones detalladas de items que no tengo totalmente claros». La visión de la SF ya lo dice (commit `7771582`). La metodología pide una especificación funcional global antes de las devslices (3.2) y solo dice que el detalle no anticipa «cada decisión de implementación». No dice qué hacer con lo que todavía no está claro.
- **Cambio propuesto:**
  1. Principios y 3.1: la visión se trabaja a fondo antes de especificar, sobre todo en proyectos nuevos e inciertos.
  2. 3.2: lo incierto no se especifica en detalle. Queda marcado como **abierto**, con su pregunta, lo que se sabe y cuándo se espera resolverlo (al preparar una devslice concreta o con una devslice de exploración).
  3. 3.4 y 3.5: una devslice no pasa a preparada mientras dependa de un punto abierto. Las devslices de exploración (prototipo o prueba de concepto, con su pregunta y lo que se tira al acabar) son una forma válida de resolverlo.
  4. Especificación de la SF: la skill de especificación funcional, cuando exista, distingue lo cerrado de lo abierto.
- **Beneficio e impacto:** evita especificar con detalle lo que después cambiará y deja visible lo que falta por decidir. Afecta a la metodología (principios, 3.1, 3.2, 3.4 y 3.5) y a la especificación de la SF.
- **Verificación prevista:** releer las secciones cambiadas sin contradicciones con «comprender el proyecto globalmente» (principios). Probarlo en la especificación funcional de LecturaFàcil: debe quedar al menos un punto abierto con su pregunta y su momento de resolución.
- **Estado:** propuesta, pendiente de aprobación.

### P03 Perfil para productos de software y hardware: gemelo digital primero

- **Origen:** SmartColdBox (`D:\Projectes\SmartColdBox`), indicado por el propietario el 2026-10-26: «en algunos casos además mis proyectos son software+hw como la smartcoldbox para la que primero quiero crear un gemelo digital».
- **Tipo:** documentar.
- **Observación y evidencia:** SmartColdBox ya tiene un gemelo digital avanzado (`gemelo_digital/v4.0`, informe de verificación del 2026-10-20): cinco procesos (gateway, gemelo, entorno, planta y control MPC), interfaz React, contratos JSON Schema y 200 pruebas Python, 23 de ellas entre procesos reales. La metodología no tiene ningún perfil ni paso para productos con una parte física. La skill de infografías técnicas ya da la vista del dispositivo.
- **Cambio propuesto:** añadir a la sección 7 un perfil «Producto de software y hardware con gemelo digital», a partir de SmartColdBox:
  1. El gemelo digital es el primer producto que se construye, con sus devslices.
  2. El hardware real queda detrás de la misma interfaz que el gemelo, como el agente simulado en LecturaFàcil. Así se puede cambiar uno por otro.
  3. Las pruebas pasan por niveles: solo el gemelo, el gemelo con piezas reales (*hardware in the loop*) y el dispositivo completo.
  4. La infografía técnica forma parte de la visión o de la definición técnica del dispositivo.
  El perfil concreto se escribirá estudiando SmartColdBox con el propietario, sin dar por buena su estructura actual.
- **Decisión del propietario (2026-10-26):** SmartColdBox será el proyecto prototípico de software, hardware y gemelo digital, como LecturaFàcil lo es del método. Su estructura servirá de referencia para el perfil. Registrada en [decisiones](decisiones/README.md).
- **Estructura revisada el 2026-10-26, antes de su primer push** (el repositorio `jumibot/SmartColdBox` está vacío y es público):
  - La visión está en `docs/fundacion/`, junto con las infografías y un PDF, en vez de en `docs/specs/vision/`.
  - El gemelo es un zip dentro de `gemelo_digital/v4.0/`, que no se puede versionar ni comparar en git. Incluye una base SQLite de telemetría.
  - Faltan `CLAUDE.md` y un lugar previsto para el gemelo, el firmware y el hardware.
  - La SF no preveía carpeta para las infografías técnicas. Resuelto el 2026-10-26 por decisión del propietario: la visión, el manifiesto y las infografías son documentos fundacionales y van juntos en `docs/specs/vision/`, con las infografías en `infografias/`. Aplicado en la metodología (sección 6), en la skill `infografia_tecnica` y en SmartColdBox.
- **Información que falta:** qué hardware hay o habrá (sensores, actuadores, controlador), si ya hay pruebas con piezas reales, qué tecnología usa el firmware y si el gemelo se entregará al cliente o solo sirve para desarrollar.
- **Beneficio e impacto:** el tipo de proyecto queda cubierto por el método y se reutiliza lo aprendido en SmartColdBox. Afecta a la metodología (sección 7 y quizá 3.3 y 8), a la especificación de la SF (perfiles) y a la visión.
- **Verificación prevista:** releer el perfil con el propietario frente al gemelo real de SmartColdBox. Comprobar que las devslices pendientes de SmartColdBox se pueden planificar con él.
- **Estado:** propuesta, pendiente de aprobación y de la información anterior.

### P04 Ciclos estandarizados por tipo de devslice

- **Origen:** SoftwareFactory, idea del propietario (2026-10-26): «usar ciclos y herramientas estandarizadas especializadas para cada devslice. Este podría ser un punto de encaje en lo que ya existe creado».
- **Tipo:** especificar.
- **Observación y evidencia:**
  - La SF ya tiene su parte propia en lo global: la visión, la especificación, la interfaz, la definición técnica y el catálogo de devslices. Ahí está lo que la diferencia de las alternativas (visión del 2026-10-26).
  - Lo que le falta está todo en la escala de una devslice: preparar, probar, desarrollar, revisar y cerrar.
  - En esa escala, las alternativas son fuertes. Superpowers tiene planes en tareas pequeñas, TDD, revisión de código y verificación antes de terminar, y Spec Kit tiene su plan por funcionalidad. La especificación de la SF ya las tiene como candidatas, sin evaluar.
  - Una devslice preparada se parece al caso que esas herramientas suponen: un alcance acotado y criterios claros. La incertidumbre de los proyectos del propietario está sobre todo en la fase global.
- **Valoración:** es un buen punto de encaje. Reparte el trabajo así: la SF gobierna lo global y las transiciones de cada devslice (preparada, en desarrollo, cerrada, kanban, informe y aprobación); dentro de la devslice, se usa un ciclo estándar tomado de lo que ya existe. Es la aplicación directa del principio «La SF define el método; las técnicas se reutilizan». Además, ahorra construir la mitad de las skills que faltan. Riesgos a controlar:
  - Los flujos ajenos imponen sus reglas. Spec Kit crea una rama y una carpeta numerada por funcionalidad, lo que choca con los nombres descriptivos. Superpowers trae su propio flujo encadenado y sus propios planes. Hay que tomar sus piezas sueltas, no el flujo.
  - El kanban, `docs/` y `reports/` siguen siendo la referencia. Ninguna herramienta puede llevar su propio estado ni integrar sin aprobación.
  - Demasiados tipos de ciclo o demasiadas herramientas dan incoherencia y más mantenimiento. Conviene empezar por uno y añadir tipos solo cuando un proyecto los necesite.
- **Cambio propuesto:**
  1. En la metodología (3.5 a 3.7), cada devslice declara su **tipo** al prepararse, y cada tipo tiene un ciclo estándar con sus herramientas. El ciclo recibe la devslice preparada (alcance, criterios y pruebas previstas) y entrega el código, las pruebas, el informe en `reports/` y la propuesta de cierre.
  2. Tipos iniciales, a confirmar:
     - **Funcional:** lógica y datos primero, TDD, interfaz y recorrido completo.
     - **Exploración:** prototipo para resolver un punto abierto. Su resultado es una respuesta y una decisión, no código que se conserva. Enlaza con la propuesta «El detalle, solo cuando está claro».
     - **Integración con agente:** contrato, agente simulado, pruebas con el agente real y comprobación de las skills cargadas.
     - **Gemelo y hardware:** simulación, después hardware en el bucle. Enlaza con la propuesta anterior.
  3. Una skill de la SF fina, «ciclo de devslice», que elige el ciclo por tipo, conecta con el kanban y los informes, y delega cada paso en la herramienta estándar.
  4. Pilotarlo con un solo tipo, el funcional, en la primera devslice de LecturaFàcil. Antes, evaluar por separado las piezas de Superpowers ya listadas como candidatas (`writing-plans`, `test-driven-development`, `requesting-code-review`, `verification-before-completion`), sin instalar el conjunto.
- **Beneficio e impacto:** menos skills propias que construir, técnicas ya probadas en la parte más mecánica y un sitio claro para cada tipo de proyecto (agente, hardware). Afecta a la metodología (3.4 a 3.7, sección 8), a la especificación de la SF (skills y candidatos) y a la visión.
- **Verificación prevista:** la primera devslice de LecturaFàcil se cierra con el ciclo funcional sin que la herramienta externa cree estado fuera del kanban, ramas o nombres no descriptivos, y deja su informe. Comparar el esfuerzo con el de preparar una skill propia.
- **Estado:** propuesta, pendiente de aprobación. No se ha instalado ni probado ninguna herramienta.

### P05 El factor humano: menos fricción al trabajar con IA

- **Origen:** SoftwareFactory, reflexión del propietario (2026-10-26): «un problema que quiero mitigar con SF es la fricción de los ingenieros/project managers/product owner con el desarrollo usando IA. Por ejemplo la velocidad de diseño, trabajo en paralelo en múltiples tareas e incluso proyectos o visiones nuevas… una sola persona puede llegar a tener que gestionar mucho más… desarrollar de una forma más delegada y con menos control. Todo esto exige adaptaciones del humano y de la IA». Pone como ejemplos JKanban, para tener contexto de cómo van los proyectos, y el documento de visión, para recuperar el rumbo y la estrategia.
- **Tipo:** especificar.
- **Observación y evidencia:** el cuello de botella ya no es escribir código, sino la atención, el contexto y las decisiones de la persona. La SF ya tiene piezas para esto, pero no lo plantea como uno de los problemas que resuelve: el tablero como «ventana permanente» y para retomar (visión, capítulo 6; metodología 4), el orden documental común (metodología 6), el cierre con informe (3.7) y preguntar en lugar de inventar. Las condiciones de aprobación humana y los límites de lo automático siguen sin concretar (metodología 3.7).
- **Cambio propuesto:** declarar el factor humano como un objetivo de la SF y ordenar sus piezas por la necesidad que cubren. Las marcadas como *nueva* no existen todavía.
  1. **Recuperar el contexto:** el tablero muestra cómo va cada proyecto. *Nueva:* un resumen de retorno por proyecto al empezar cada sesión (qué se hizo, qué sigue y qué espera de ti), con el mismo formato en todos.
  2. **Recuperar el rumbo:** la visión es el ancla de la estrategia. *Nueva:* al planificar o cerrar devslices, comprobar si siguen sirviendo a la pregunta de la visión y avisar si el proyecto se desvía.
  3. **Gastar la atención solo donde hace falta.** *Nueva:* las preguntas y decisiones pendientes se agrupan en una sola bandeja por proyecto, en lugar de interrumpir una a una. Claude sigue con lo que no depende de ellas.
  4. **Delegar con confianza en lugar de control:** criterio, prueba y resultado, con el informe enlazado al tablero. Sustituyen a revisar cada línea. *Nueva:* niveles de delegación por tipo de tarea o devslice, que digan qué hace Claude solo y qué necesita tu aprobación. Así se concreta lo pendiente en 3.7.
  5. **Trabajo en paralelo con límite:** *nueva:* un tope de devslices en desarrollo por proyecto y en total (WIP del tablero), ajustado a lo que puedes revisar. La IA puede abrir más frentes de los que una persona puede cerrar.
  6. **Cambiar de proyecto sin coste:** la misma estructura, los mismos pasos y los mismos nombres en todos los proyectos. Ya existe.
  7. **Revisar con rapidez:** *nueva:* cada cierre dice qué ha cambiado y qué conviene mirar, con apoyo visual cuando ayude (bocetos, diagramas, infografías).
- **Alcance:** decidido por el propietario el 2026-10-26: la SF es para una sola persona con muchos proyectos. Los equipos con papeles distintos quedan fuera. Registrado en [decisiones](decisiones/README.md).
- **Beneficio e impacto:** la SF responde al problema que hoy limita el trabajo con IA y da un criterio para valorar sus piezas. Afecta a la visión («Por qué una fábrica»), a la metodología (principios, 3.7 y 4), a la especificación de la SF (tablero, skills) y, quizá, a JKanban (resumen, WIP y bandeja de decisiones).
- **Verificación prevista:** en el piloto, medir con el propietario cuánto tarda en retomar un proyecto tras una pausa y cuántas interrupciones recibe por devslice, antes y después de las piezas nuevas.
- **Estado:** propuesta, pendiente de aprobación y de la información anterior.

### P06 Vibe design al principio de la interfaz

- **Origen:** SoftwareFactory, indicación del propietario (2026-10-26): «también forma parte del ADN de SF diseñar las interfaces con vibe design y, si es el caso, un apoyo más formal para el vibe design y/o para la posterior implementación, pero quiero que el vibe design sea parte fundamental al inicio al menos».
- **Tipo:** documentar.
- **Observación y evidencia:** la metodología (3.2) y la skill `diseno_interfaz` empiezan por la parte formal: recorridos, inventario, matriz pantalla × estado y criterios. Los bocetos llegan al final, son estáticos (HTML sin JavaScript o SVG), de 2 a 4, y «si chocan, manda la especificación». No hay un paso de diseño rápido y conversacional con prototipos que se ven y se tocan.
- **Cambio propuesto:**
  1. La interfaz empieza con **vibe design**: prototipos visuales e interactivos hechos conversando con la IA, en iteraciones rápidas, con el contenido real del caso y centrados en la persona que usará el producto.
  2. El apoyo formal (`diseno_interfaz`) llega después y solo cuando aporta. Recoge lo que el vibe design ha dejado claro (estados, comportamiento y criterios «Dado / Cuando / Entonces») y lo prepara para implementar. Se aplica también «El detalle, solo cuando está claro».
  3. Se define qué manda en cada momento. En la exploración manda el prototipo. Una vez formalizado, la especificación es el contrato y el prototipo queda como referencia visual.
  4. El prototipo no fija la tecnología. Puede hacerse en web aunque el producto sea de escritorio, como LecturaFàcil con Tkinter. La traducción a la plataforma sigue siendo de la definición técnica.
  5. Ajustar `diseno_interfaz`: aceptar los prototipos del vibe design como entrada, y que los bocetos puedan ser interactivos cuando ayuden.
  6. Herramienta: Claude Design, con el patrón ya probado en OncoCore (ver abajo).
- **Riesgos a controlar:** un prototipo que parece terminado da una falsa sensación de avance. Las variantes rápidas abren frentes (ver «El factor humano»). El código del prototipo se cuela en el producto. Para evitarlo, se marca como desechable o como referencia, salvo decisión expresa.
- **Cómo lo hace hoy el propietario (2026-10-26):** con Claude Design (artifacts de claude.ai). En OncoCore hay dos usos ya probados:
  - **Diseño de la app** (`_docs/front_design/OncoCore_front_design/`): un prototipo de Claude Design exportado como *design handoff*. Incluye `README.md`, `LIBRARIES.md` con la pila recomendada para reconstruirlo («Do not ship that pipeline»), `TWEAKS.md` y un panel de ajustes. El prototipo es la referencia y la app se reconstruye aparte.
  - **Formulario de normalización** (`_docs/subproyectos/normalizacion_caso/`): un lienzo de Claude Design con ocho pantallas y dos casos reales.
    - Sus fuentes están versionadas en el repositorio (`disenio_formulario/project/`, una `.dc.html` por pantalla y `canvas.json`).
    - Hay scripts que generan los datos de las pantallas desde el contrato del caso (`generar_casos_lienzo.py`, `generar_prueba_ngs.py`).
    - Un documento dice dónde está el lienzo, qué pantallas tiene, cómo se mantiene al día y qué falta (`formulario_normalizacion.md`).
    - Convive con la especificación (`especificacion_formulario.md`), que dice qué tiene que hacer el formulario.
  
  Lo que se puede llevar a la SF de estos dos usos:
  - el prototipo se versiona en el proyecto y se publica como artifact;
  - los datos salen del caso real o del contrato, generados por un script, para que no se desfasen;
  - un documento de lienzo lo enlaza con la especificación;
  - la entrega a implementación es un *handoff* con la pila recomendada, que no se lleva al producto.
- **Información que falta:** si algún prototipo de Claude Design ha llegado ya a implementarse, y cómo fue la traducción.
- **Beneficio e impacto:** diseño más rápido y más centrado en las personas, en línea con la forma de trabajar del propietario. Afecta a la metodología (principios y 3.2), a la especificación de la SF, a la skill `diseno_interfaz` y a la visión (sección sobre la interfaz).
- **Verificación prevista:** probarlo en la pantalla de revisión de LecturaFàcil: vibe design primero y formalización después. Comprobar que la especificación resultante recoge lo decidido en el prototipo sin contradicciones.
- **Estado:** pasada a la tarea 280 de la cola el 2026-11-01.

### P07 Skills externas: estudiarlas y adaptarlas, no instalarlas

- **Origen:** SoftwareFactory, idea del propietario (2026-10-26): «tomar las skills abiertas como referencia a estudiar y adaptar a las mías propias, evitando malware y otros peligros. Algo así como una ingeniería inversa para ver el conocimiento que encierran y adoptar el que necesitemos».
- **Tipo:** especificar.
- **Observación y evidencia:**
  - Cuando se escribió, la especificación de la SF copiaba las skills externas enteras, «incluso sin adaptaciones». Desde el 2026-11-01 (decisiones 175 y 176), una externa que se usa tal cual es una dependencia del plugin, y solo viajan en el plugin las versiones nuestras. La visión del método aún dice que «las externas se guardan enteras».
  - El riesgo es real. Según una auditoría de Snyk (febrero de 2026, fuente secundaria), el 13,4 % de 3.984 skills de registros abiertos tenía problemas críticos, como malware, inyección de instrucciones o secretos expuestos ([notas de la investigación](referencias/research_notes/Recursos%20para%20la%20SoftwareFactory/skills_y_plugins.md)).
  - Una skill son instrucciones: leerla dentro de una sesión ya es exponerse a ellas.
  - El método ya funciona así en la práctica: `diseno_interfaz` y `definicion_tecnica` se escribieron estudiando BMAD, Spec Kit y MADR, sin copiar su infraestructura.
- **Cambio propuesto:**
  1. **Regla general:** las skills externas son material de estudio, no piezas instalables. La SF extrae su conocimiento (técnicas, listas de comprobación, plantillas y criterios) y lo reescribe en skills propias, con sus reglas de método.
  2. **Estudio en cuarentena:**
     - El original se descarga en una carpeta aislada, fuera de `~/.claude/skills/` y de cualquier carpeta que Claude Code cargue.
     - Sus scripts nunca se ejecutan.
     - Su texto se trata como datos, no como instrucciones: se lee para analizarlo, y lo que pida no se obedece.
     - El análisis señala lo sospechoso: comandos de red, descargas, rutas fuera del proyecto, ofuscación u órdenes de ignorar reglas.
  3. **Lo que se adopta se reescribe.**
     - Los scripts necesarios se escriben de nuevo y se revisan; no se copian.
     - El texto solo se reutiliza literalmente si la licencia lo permite: MIT o Apache-2.0 con atribución; CC-BY-SA obliga a compartir igual.
     - Sin licencia, o con una de código visible no libre, solo se toman ideas.
  4. **Trazabilidad:** el `ORIGIN.md` de la skill propia anota qué fuentes se estudiaron (repositorio, commit exacto, licencia y fecha), qué se tomó de cada una y qué se descartó. El original estudiado no se guarda en el repositorio: basta el enlace al commit.
  5. **Una skill de la SF para hacerlo,** provisionalmente «estudio de skills». Sigue los pasos anteriores y entrega un informe de lo aprovechable y de los riesgos detectados. El propietario decide qué se adopta.
  6. ~~Las externas ya instaladas se revisan una a una.~~ Resuelto por la decisión 176: las 16 (`oklch-skill`, `gsap-*`, `threejs-*`) pasan a ser dependencias, sin copiarlas.
- **Beneficio e impacto:** menos superficie de ataque, skills coherentes con el método y conocimiento ajeno aprovechado sin depender de su mantenimiento. Afecta a la especificación de la SF (ubicación e instalación de skills, skills externas, procedencia), a la visión del método (sección sobre las herramientas) y a las skills externas instaladas.
- **Verificación prevista:** aplicar el procedimiento a una skill candidata del catálogo (por ejemplo, una de planificación de `mattpocock/skills` o de Superpowers). Comprobar que no se ejecuta nada, que la skill propia resultante funciona y que su `ORIGIN.md` permite rastrear cada idea tomada.
- **Estado:** propuesta, pendiente de aprobación. Superada en parte el 2026-11-01 por las decisiones 175 y 176: una externa que se usa tal cual se instala como dependencia, sin estudiarla en cuarentena ni reescribirla. Queda por decidir el resto (cuarentena, reescritura y skill «estudio de skills») para las externas que se quieran personalizar como versión nuestra.

### P08 Registro de decisiones y pendientes en cada proyecto

- **Origen:** SmartColdBox, 2026-10-26. El propietario respondió en una sola tanda siete preguntas abiertas:
- **Tipo:** implementar.
  - el precio de Hemlibra;
  - el transporte de referencia;
  - el hardware de referencia;
  - los sensores;
  - los 60 días;
  - el formato;
  - la ubicación de la biblioteca.
- **Observación y evidencia:**
  - Las respuestas afectaban a tres documentos y al gemelo a la vez.
  - Varias contradicciones solo se veían al cruzar los documentos con el gemelo.
  - Sin un sitio único, la siguiente sesión tendría que reconstruirlas desde la conversación.
  - Se creó `SmartColdBox/docs/decisiones-y-pendientes.md`, enlazado desde su `CLAUDE.md`.
- **Cambio propuesto:**
  - Que la plantilla de proyecto de la SF incluya `docs/decisiones-y-pendientes.md`, con dos apartados:
    - decisiones fechadas, que mandan sobre los documentos anteriores;
    - pendientes, con el documento o la pieza afectada.
  - Que las skills de documentos lo lean antes de escribir.
  - Encaja con el registro de decisiones técnicas (MADR) de `definicion_tecnica`, que cubre solo la arquitectura.
- **Beneficio e impacto:** las decisiones del propietario no se pierden entre sesiones ni se contradicen entre documentos. Afecta a la plantilla de proyecto y a las skills `documento_vision`, `documento_fundacional` y `definicion_tecnica`.
- **Estado:** en parte decidida el 2026-10-27: cada proyecto tiene `docs/decisiones/`, con todas sus decisiones, no solo las técnicas, una por archivo (decisiones «Propuestas, decisiones, plantillas y ejemplos, cada uno en su sitio» y «Una decisión por archivo, en `docs/decisiones/`»). Los pendientes de cada proyecto van en `.sf/estado.json` y, cuando esté incorporado, en JKanban (decisión «La carpeta `.sf/` identifica el proyecto y guarda su estado»). Queda pendiente y que las skills de documentos lean `docs/decisiones/` antes de escribir.

### P09 Cierre de sesión con `/sf cierre`

- **Origen:** SoftwareFactory, 2026-10-27. Respuesta a «que más podemos hacer para mejorar mi forma de trabajo con la sf?»; el propietario: «sí, regístralas».
- **Tipo:** implementar.
- **Cambio propuesto:** un comando `/sf cierre` que, al acabar, resume lo hecho en la sesión (commits), lo que queda en la cola (en curso, en cola, en Testing) y los cambios sin commit del proyecto.
- **Beneficio:** el propietario retoma el trabajo sin reconstruir el contexto, aunque pase días fuera.
- **Comprobación:** tras una sesión con dos peticiones cerradas y una en Testing, `/sf cierre` las enumera con sus commits.
- **Estado:** propuesta, pendiente de aprobación.

### P10 Las correcciones se convierten en reglas

- **Origen:** SoftwareFactory, 2026-10-27. Misma pregunta y misma respuesta del propietario. Evidencia: las normas de forma de los documentos (prosa, tarjetas, FAQ, diagrama tras una introducción) salieron de correcciones repetidas.
- **Tipo:** documentar.
- **Cambio propuesto:** cuando el propietario corrige algo de forma o de método, Claude propone en ese momento, en una línea, la regla general que se deduce y dónde escribirla; con el visto bueno, la registra como decisión y la aplica.
- **Beneficio:** la misma corrección no hay que repetirla en otro documento ni en otro proyecto.
- **Estado:** propuesta, pendiente de aprobación.

### P11 Lista de sesiones abiertas en `/sf`

- **Origen:** SoftwareFactory, 2026-10-27. El propietario: «desde el mod podria tener una lista de sesiones abiertas?».
- **Tipo:** implementar.
- **Cambio propuesto:** cada sesión deja un archivo propio con su proyecto, su fase y la hora, lo renueva periódicamente y lo borra al cerrarse; `/sf` enumera las sesiones abiertas y descarta las que llevan tiempo sin renovarse. El mod no puede ver las otras sesiones directamente. Falta comprobar si el mod puede escribir fuera de la carpeta del proyecto.
- **Beneficio:** con varios proyectos a la vez, saber qué sesión hay en cada uno.
- **Estado:** absorbida por el Claude Code Commander (decisión del 2026-10-27).

### P12 Procedimiento de instalación del plugin

- **Origen:** SoftwareFactory, 2026-10-27. El propietario, al revisar «Cómo funciona»: «quita todo lo de github de momento... ya haremos un procedimiento de instalación desde github. Aquí solo mete ruido».
- **Tipo:** documentar.
- **Cambio propuesto:** las dos guías de la SF que pide la decisión «Guías de instalación y de actualización en cada proyecto»: `docs/guias/instalacion.md` (acceso al repositorio privado en GitHub, catálogo, instalación para el usuario y comprobación) y `docs/guias/actualizacion.md` (actualizar el catálogo y el plugin, reiniciar y comprobar la versión). «Cómo funciona» solo las enlazará.
- **Estado:** pendiente de escribir; antes se prueba el formato con JKanban.

### P13 Historial de versiones del plugin

- **Origen:** SoftwareFactory, 2026-10-27. Pregunta abierta desde el 2026-10-26 («CHANGELOG: sin respuesta»).
- **Tipo:** documentar.
- **Cambio propuesto:** un `CHANGELOG.md` en `plugins/sf/`, con una entrada por versión publicada (0.1.0 → 0.4.0: mod, plugin único, skills dentro, plantillas). Cada entrada dice qué cambia para quien usa la SF y enlaza las decisiones.
- **Estado:** propuesta, pendiente de aprobación.

### P14 Organización del repositorio de la SF

- **Origen:** especificación de la SF, sección 1, «Propuesta inicial de organización» (borrador inicial).
- **Tipo:** deliberar.
- **Propuesta original:**

  ```text
  software-factory/
  ├── CLAUDE.md
  ├── docs/
  ├── skills/
  ├── templates/
  ├── profiles/
  ├── evaluations/
  ├── distribution/
  └── CHANGELOG.md
  ```

- **Lo que ya está decidido:** `skills/` y las plantillas viven en el plugin (`plugins/sf/skills/`, `plugins/sf/templates/`); la distribución es el catálogo de plugins.
- **Lo que sigue abierto:** si hacen falta `profiles/` (los perfiles están hoy en la metodología, 7) y `evaluations/` (casos de evaluación de las skills y del proceso), y dónde va el historial de versiones (propuesta anterior).
- **Estado:** propuesta, pendiente de decisión.

### P15 Estados del kanban

- **Origen:** metodología, 4, «Propuesta de estados, pendiente de contrastar con el kanban existente».
- **Tipo:** deliberar.
- **Propuesta original:** **Planificada → En preparación → Preparada → En desarrollo → En verificación → Terminada**.
- **Observación:** JKanban ya tiene flujos configurables (estados, estado inicial y transiciones asignables a etiquetas; su `docs/flows.md`), y la SF los creará por el MCP con `ensure_flow`. Falta decidir los estados de la SF y sus transiciones.
- **Estado:** propuesta, pendiente de decisión.

### P16 Formato del archivo de procedencia de las skills

- **Origen:** especificación, 2: «Guardar estos datos en un archivo de procedencia… por ejemplo `ORIGIN.md`… Esta convención es una propuesta de formato».
- **Tipo:** deliberar.
- **Observación:** todas las skills de la SF ya llevan `ORIGIN.md`, con fuente, versión o commit, licencia, cambios propios y dependencias.
- **Cambio propuesto:** fijar `ORIGIN.md` como formato, con esos apartados.
- **Estado:** propuesta, pendiente de aprobación.

### P17 Brain de desarrollo en `docs/` y estructura de la KB operativa

- **Origen:** metodología, 7.6.
- **Tipo:** deliberar.
- **Propuesta original:** abrir `docs/` como vault del brain de desarrollo, sin duplicar sus documentos. Añadir `docs/conocimiento/` cuando existan notas duraderas que no sean especificaciones ni decisiones. La configuración de Obsidian es opcional; decidir qué parte de `.obsidian/` compartir. Para la KB operativa: `knowledge/` en el repositorio con la organización y las plantillas, y el vault real fuera del repositorio (por ejemplo, `datos-aplicacion/operational-brain/`), con su ubicación configurada por entorno. La estructura está en la plantilla `plugins/sf/templates/estructuras/brain-y-kb.md`.
- **Estado:** propuesta, pendiente de decisión. Brain y KB son opcionales por proyecto (decisión «Método propio, técnicas reutilizadas»).

### P18 Skills externas candidatas

- **Origen:** especificación, 2, «Estado de la búsqueda».
- **Tipo:** investigar.
- **Observación:** se localizaron candidatas, pero **ninguna se ha instalado ni validado mediante un proyecto piloto**. La lista no es un paquete aprobado.

  | Candidato | Evaluación pendiente |
  | --- | --- |
  | Superpowers: `systematic-debugging` y `verification-before-completion` | Priorizar una evaluación de las piezas individuales. |
  | Anthropic: `mcp-builder` y `skill-creator` | Candidatos para construir el MCP y las skills propias. |
  | Matt Pocock: `tdd` | Adaptar aprobación de interfaces de prueba y su tratamiento de refactorización. |
  | Jeffallan: `code-reviewer` | Evaluar utilidad y encaje con revisión independiente. |
  | Jeffallan: `python-pro` | Revisar imposiciones de cobertura, herramientas y asincronía. |
  | Jeffallan: `fastapi-expert` | Adaptar a SQL nativo; sus ejemplos incluyen SQLAlchemy. |
  | Jeffallan: `sql-pro` | Fuera del paquete inicial propuesto por sus criterios rígidos y falta de ajuste a SQLite. |
  | CodeAtCode: Qt y `pyqt-testing` | Evaluar con la tecnología y versiones elegidas. |
  | zzenx: Tkinter/ttkbootstrap | Considerar solo si se elige esa dependencia. |
  | Anthropic: `frontend-design` y `webapp-testing` | Evaluar para web; diseño visual no cubre toda la especificación UX. |
  | Vercel: React y pautas web | Evaluar cuando haya proyecto React/web. |
  | MKToronto: Python Clean Architecture | Referencia que necesita adaptación; no arquitectura universal. |
  | BMAD: `bmad-ux` y `bmad-architecture` | Técnicas adaptadas en `diseno_interfaz` y `definicion_tecnica` (2026-10-25), sin su infraestructura. Falta validarlas en un piloto. |
  | Spec Kit: plantillas de especificación y de plan | Escenarios «Dado / Cuando / Entonces», campos del contexto técnico y tabla de complejidad, adaptados en las mismas skills. Su plan por funcionalidad es candidato para la preparación de devslices. |
  | MADR 4.0.0 (versión mínima) | Formato de las decisiones (`docs/decisiones/`), adaptado en `definicion_tecnica`. |
  | Superpowers: `writing-plans`, `test-driven-development`, `subagent-driven-development`, `requesting-code-review`, `finishing-a-development-branch` | Candidatas para preparación, desarrollo, revisión y cierre; evaluarlas sin su flujo obligatorio. |

  Fuentes para retomar la evaluación:

  - https://github.com/anthropics/skills
  - https://github.com/obra/superpowers
  - https://github.com/mattpocock/skills
  - https://github.com/Jeffallan/claude-skills
  - https://github.com/CodeAtCode/oss-ai-skills
  - https://github.com/zzenx/tkinter_modern_ui_skill
  - https://github.com/vercel-labs/agent-skills
  - https://github.com/MKToronto/python-clean-architecture
  - Documentación de skills de Claude Code: https://code.claude.com/docs/en/skills

  Las fuentes y sus contenidos pueden cambiar: revisar el estado actual y fijar las versiones seleccionadas antes de incorporarlas. Ver también «Skills externas: estudiarlas y adaptarlas, no instalarlas».
- **Estado:** candidatas, sin evaluar. Por las decisiones 175 y 176 (2026-11-01), una candidata que se adopte tal cual entra como dependencia del plugin `sf`. Si es un plugin de un marketplace, se depende de él; si no, el marketplace de la SF le da una entrada fijada a un commit. Solo se copia al plugin si se personaliza.

### P19 Orden de construcción de la SF

- **Origen:** especificación, 4, «Orden propuesto» (borrador inicial).
- **Tipo:** deliberar.
- **Propuesta original:**
  1. Crear o confirmar el repositorio central de la SF. *(Hecho.)*
  2. Incorporar estos documentos y la skill de visión existente. *(Hecho.)*
  3. Convertir los acuerdos en metodología v0.1 y plantillas mínimas.
  4. Revisar el código y capacidades del kanban existente.
  5. Definir su modelo de devslices/tareas, operaciones MCP y estados.
  6. Concretar el primer perfil: escritorio Python con MVP, SQL nativo, la interfaz que se seleccione y, opcionalmente, agente Claude Code (metodología, 7.7). *(Hecho como perfil 7.7.)*
  7. Crear las skills propias y evaluar selectivamente las externas.
  8. Probar el circuito completo con una aplicación pequeña.
  9. Ajustar y publicar una versión estable instalable.
- **Estado:** propuesta. El orden real lo está marcando el propietario sesión a sesión.

### P20 Prototipos de mods en `~/.claude/dev-mods/`

- **Origen:** SmartColdBox, 2026-10-27. Claude copió a la sesión el prototipo `sf-estado` de otra sesión (`dev-mods/95ea89e5-…/sf-estado`), que lee y propone crear `docs/sf.json`, contra la decisión de usar `.sf/`. El propietario: «teniamos un acuerdo de no crear el sf.json en /docs... no te acuerdas».
- **Tipo:** corregir.
- **Cambio propuesto:** cuando un mod pasa al plugin `sf`, borrar su prototipo de `dev-mods/`. Añadir a la metodología que el mod de estado es solo el del plugin `sf`.
- **Estado:** propuesta, pendiente de aprobación. El prototipo sigue en esa carpeta.

### P21 Claude Code Commander: lo que falta concretar

- **Origen:** SoftwareFactory, 2026-10-27. Decidido el Commander (ver la decisión «Claude Code Commander»); el propietario: «ya se que es impreciso y mucho decir». Sustituye a la propuesta «La ventana del mod, fuera de la terminal».
- **Tipo:** especificar.
- **Lo que se sabe:** según los tipos de la API, el mod puede llamar por HTTP a `localhost` (`$.http.fetch`), lanzar un proceso y leer su salida mientras vive (`$.process.spawn`), escribir archivos con ruta absoluta (`$.fs.write`), repetir algo con un temporizador (`$.clock.every`) y conocer el uso y el coste de su sesión (`$.session.usage`). No tiene cliente de websockets propio. Nada de esto está probado aún en la práctica.
- **Por concretar, con propuesta inicial:**
  0. **Tecnología y dispositivos.** Requisito del propietario: usarlo en el ordenador, la tableta y el móvil («será una ventana flotante del todo»). Tkinter queda descartado. Opciones por valorar: una aplicación web servida por el propio Commander, que se abre en cualquier navegador; una aplicación web instalable (PWA); o apoyarse en las superficies que ya tiene Claude Code (app de escritorio, móvil y control remoto). Falta también cómo se llega desde fuera de casa con seguridad.
  1. **Canal.** El Commander escucha en el equipo, con un token en un archivo del usuario; para la tableta y el móvil tendrá que abrirse a la red local o a un acceso remoto seguro. Cada mod le envía su estado por HTTP al arrancar, al acabar cada turno y al cerrarse, y recoge sus órdenes preguntando cada pocos segundos. Los websockets que pidió el propietario sirven si hace falta empuje inmediato: el mod tendría que mantener un pequeño proceso puente.
  2. **Arranque.** El primer mod que no encuentra el Commander lo lanza; `/sf commander` lo abre o lo trae al frente. Si el Commander cae, las sesiones siguen igual.
  3. **Conducir Claude Code.** Abrir una sesión en un proyecto (un terminal con `claude` en su carpeta) y enviarle un prompt: hay que estudiar qué ofrece Claude Code para hacerlo sin trucos (por ejemplo `claude -p`, el Agent SDK o mensajes entre sesiones).
  4. **Tareas de JKanban.** Elegir una tarea del proyecto y lanzarla en su sesión, con su contexto. Depende del MCP de JKanban.
  5. **Métricas.** Primera lista: sesiones abiertas a la vez, prompts por sesión, peticiones terminadas y dejadas a medias (el marcador del día), tiempo por petición, coste y uso de contexto, propuestas añadidas. Falta decidir cuáles, umbrales y avisos.
  6. **Orden de construcción.** Primero ver todas las sesiones (sustituye a la lista de sesiones en `/sf`); después órdenes; después lanzar sesiones y tareas; las métricas, desde el principio con lo que ya cuenta el mod.
  7. **La caja sobre el prompt.** Si se oculta con el Commander abierto o se queda.
- **Estado:** propuesta, pendiente de decisión.

### P22 Usar más los subagentes

- **Origen:** SoftwareFactory, 2026-10-28. Mientras se decidía el panel de TAREAS, el propietario: «Puedes ir haciendo las 1,2 y 3 en un subagente mientras hablamos de la 4». Después: «Añade una propuesta: Usar más los subagentes».
- **Tipo:** documentar.
- **Observación y evidencia:** Claude trabaja casi siempre en la conversación principal. Mientras escribe código o documentos, el propietario espera o la conversación se interrumpe, aunque haya partes independientes que podrían avanzar a la vez. En esta sesión, un subagente aplicó lo ya decidido del panel mientras se hablaba de lo pendiente.
- **Cambio propuesto:** en la metodología (2), delegar en un subagente el trabajo independiente y bien acotado, para que la conversación con el propietario siga mientras tanto:
  1. aplicar lo ya decidido mientras se discute el resto;
  2. búsquedas y lecturas largas (otros proyectos, documentación, fuentes);
  3. comprobaciones de un cambio (pruebas, revisión de enlaces y documentos).

  El subagente recibe el alcance, los archivos que puede tocar y lo que no debe hacer: no hace commit, no publica y no toca la cola. Cerrar sigue siendo cosa de la sesión principal, preguntando al propietario. Dos subagentes, o un subagente y la sesión principal, no trabajan a la vez en los mismos archivos.
- **Beneficio e impacto:** menos espera y menos interrupciones; la conversación se centra en decidir. Afecta a la metodología (2) y a la plantilla `templates/claude-sf.md`.
- **Verificación prevista:** en las próximas sesiones, contar cuántas veces se delega y si hay choques entre el subagente y la sesión principal.
- **Estado:** propuesta, pendiente de aprobación.

### P23 De planificada en JKanban a la cola

- **Origen:** SoftwareFactory, 2026-10-28, punto 4 de la propuesta del bloque TAREAS (decisión «Bloque TAREAS con A y H»). El propietario: «una tarea planificada puede pasar a estar en curso y por lo tanto pendiente de la sesión actual o incluso de históricas»; «no sale de planificadas sino que cambia de estado ya que pasa a ser planificada en curso»; para las que no han empezado: «No tienen número una P de pendiente»; para las empezadas: «en lugar de una C la A y su número. Me parece más consistente». Y: «En realidad hasta tener le jkanban pasa a propuesta».
- **Tipo:** especificar.
- **Observación y evidencia:** con JKanban, el panel tendrá Planificadas en el bloque PROYECTO, y falta decir cómo se relaciona lo planificado con la cola.
- **Cambio propuesto:**
  1. Planificadas refleja JKanban. Una planificada sin empezar lleva «P», sin número.
  2. Al empezar, entra en la cola en curso, con su número de la cola y la A. En Planificadas no sale: pasa de «P» a «63A», y en las sesiones siguientes es H en los dos sitios. El número de su tarjeta queda en el campo `kanban` de la petición.
  3. Si se aparca y vuelve al plan, sale de la cola y vuelve a «P».
  4. Al cerrarse va a Testing; con el OK del propietario sale de la cola y su tarjeta pasa a hecha, con lo que deja Planificadas.
  5. Claude mueve la tarjeta con el MCP de JKanban cuando esté conectado; hasta entonces, no da ningún movimiento por hecho.
- **Beneficio e impacto:** el plan y el trabajo de la sesión se ven juntos sin duplicar tareas, con la misma letra y número en todos los sitios. Afecta al mod de estado, a la especificación y a la metodología (2).
- **Verificación prevista:** al incorporar JKanban, empezar una planificada y ver «A-n» en Planificadas y en TAREAS; cerrarla y darle el OK, y ver que la tarjeta pasa a hecha.
- **Estado:** propuesta, pendiente de decisión al incorporar JKanban.

### P24 La daily ordena el día por tipo de trabajo

- **Origen:** SoftwareFactory, 2026-10-26. El propietario se define como «hombre orquesta» y nombra sus trabajos de cada día: desarrollar, investigar, crear proyectos y visiones, enseñar, aprender y estar al día. «No es lo mismo crear una nueva idea que avanzar en un desarrollo.» «Todo es sobre crear software, de ahí que el punto de encuentro es la SF.»
- **Tipo:** especificar.
- **Observación y evidencia:** esos trabajos piden formas de pensar distintas, y pasar de uno a otro cuesta más que cambiar de proyecto. Las herramientas de IA están dispersas: LecturaFàcil empezó en ChatGPT Work y en su repositorio no queda rastro; el formulario de OncoCore está en un lienzo de Claude Design. La visión «El taller del hombre orquesta» lo desarrolla y marca el día por tipo de trabajo como propuesta, no como horario.
- **Cambio propuesto:**
  1. Una daily al empezar el día que lo ordena por tipo de trabajo, no solo por proyecto, con la docencia como ancla fija.
  2. Un solo centro: Claude Code, con la SF como arnés. Lo hecho fuera (ChatGPT, Claude Design, una conversación) se trae al proyecto, a `docs/referencias/` o a `docs/decisiones/`.
  3. Un catálogo de instrumentos (qué herramientas se usan y para qué) y un banco de pruebas para lo nuevo antes de adoptarlo.
- **Beneficio e impacto:** menos coste al cambiar de trabajo y nada perdido en otras herramientas. Afecta a la especificación de la SF (daily, tablero) y a la metodología (dónde se guarda lo hecho fuera).
- **Verificación prevista:** durante una semana, la daily propone el orden del día y el propietario dice si lo sigue y si ahorra cambios de contexto.
- **Estado:** propuesta, pendiente de aprobación.

### P25 Añadir ayudas de prueba a las tareas listas para probar

- **Origen:** SoftwareFactory, 2026-11-01. Devuelta a propuesta desde la tarea 267 de la cola.
- **Tipo:** implementar.
- **Cambio propuesto:** Con la 266 ya cargada en el panel, añadir con paso añadir --prueba ayudas de prueba, tras «Activar rama», a las tareas listas para probar.

  Antes no se puede: el panel cargado no conoce las ayudas y las tomaría por pasos obligatorios, que bloquean Cerrar.
- **Estado:** pasada a la tarea 272 de la cola el 2026-11-01.

## Descartadas

- **Montar el método como *preset* de Spec Kit** (2026-10-25): arrastraría su programa, una rama por funcionalidad y su orden fijo de pasos, sin aprobación humana. Ver la decisión «Método propio, técnicas reutilizadas».
- **Un plugin por pieza de la SF** (2026-10-27): se eligió un solo plugin, `sf`. Ver la decisión «Un solo plugin, `sf`…».

## Vinculación al kanban

Al disponer de acceso, localizar el proyecto **SoftwareFactory** y, dentro de él, localizar o crear la tarea **Mejorar la Software Factory**. Asociar también a **SoftwareFactory** cada tarea concreta de mejora, enlazar este registro y confirmar la operación. Si el proyecto no existe, solicitar su creación o la información necesaria; no asociar las tareas a otro proyecto por defecto. El kanban será la referencia de estado; conservar aquí el contexto útil sin mantener estados contradictorios.

Cada propuesta trasladada lleva una línea `- **Kanban:**` con su tarea (por ejemplo, `- **Kanban:** SoftwareFactory #12`). El mod de estado cuenta como «sin pasar al kanban» las que no la tienen, y como «por revisar» las que su «Estado» dice «pendiente de aprobación» o «pendiente de decisión».
