---
antetitulo: Software Factory · Informe de análisis · Noviembre 2026
lema: Una tarea deliberativa no se prueba: // termina cuando cada pregunta tiene destino.
subtitulo: Qué tipos de tarea hay además de implementar, cómo registran las deliberativas sus decisiones y sus dilemas abiertos, si hace falta una skill, cómo se cierran sin prueba, cómo se ven en la cola y en el panel, cómo se escriben y cuándo terminan, y el recorrido completo de las tareas de documentos.
version: Versión 1.6 · 02/11/2026
estado: Propuesta · Tarea 274
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
tipo: Informe de análisis
pie: Propuesta de la tarea «Tareas deliberativas: registrar decisiones y dilemas abiertos» (274), que sigue a la descartada 201 y absorbe «Tipos de tarea: pensar, estudiar y diseñar» (192). Sale de sf:flujo_tareas, sf:orquestacion, cola.py y el panel en develop; las decisiones 145, 151, 154, 157, 172, 174, 184 y 199-204; la metodología (sección 3); la cola y su historial; y los casos «Incorporar un proyecto sin cambiarlo» (222), «Configuración inicial» (263) y su antecesora (190). Espera la decisión del propietario.
---
# Tareas deliberativas

## Resumen | Siete tipos, tres familias, un final claro | Resumen {#resumen}

La cola ya tiene siete tipos («Cada tarea tiene un tipo», 145), pero todos se tratan como si fueran de código: los mismos pasos de cierre, el mismo encargo al subagente («qué mirar en la prueba») y ningún sitio para lo que queda sin decidir.

Desde que hay tipos han salido de la cola 57 tareas de implementar o corregir, 3 de investigar, 2 de diseñar y ninguna de deliberar. Las deliberativas existen (222, 263, 274), pero duran días, se parten (la 190 dio la 191, la 193, la 262 y la 263) o se descartan y renacen (la 201 volvió como esta 274).

La propuesta no añade tipos: agrupa los siete en **tres familias** que deciden cómo se trabaja y cómo se cierra cada tarea.

- **Código** (implementar, corregir): como hoy.
- **Deliberativas** (investigar, deliberar, diseñar): su resultado son decisiones. Un paso por pregunta, las preguntas abiertas en el informe y, al cerrar, cada una con destino: decidida, a otra tarea, a propuesta o descartada.
- **Documentales** (especificar, documentar): su resultado es un documento. Se cierran con «Aprobar el resultado» en lugar de «Activar rama para poder probar».

Casi todo es texto en `sf:flujo_tareas` y en el encargo que genera `cola.py`. Lo único nuevo en el código son los pasos de cierre según la familia y, si se quiere, la cuenta de decisiones en el panel.

La versión 1.1 añade el recorrido completo de las **tareas de documentos**, con «Los documentos nuevos van a develop en cada vuelta y se ofrecen en el navegador» (216) y su matiz: una tarea de documentos solo toca su documento. Los huecos más grandes:

- Las tres tareas «Actualizar…» acumulan 66, 45 y 29 pasos sin empezar desde el 30 y el 31 de octubre.
- Nada impide que una tarea de documentos crezca con pasos ajenos.
- La 216 choca con la recogida del subagente, que hoy mira los commits y no el documento.
- Que el HTML siga al día depende de que alguien lo regenere a mano.

La versión 1.2 incluye en ese recorrido «Antes de sustituir un documento, se respalda en _respaldo/» (217). La 1.3 pone «Decidir» al día con «Una tarea deliberativa da un informe y las tareas que salgan» (218): toda deliberativa produce un informe con el formato de los fundacionales y, si hace falta, otras tareas, y no cambia código ni otros documentos; y con «El tipo de tarea decide cómo se maneja el repositorio» (219). La 1.5 aplica a este mismo informe «En una deliberativa, lo que es de otra tarea se propone separar» (221): la sección «Separar» propone sacar a otras tareas lo que ya no es de esta. Con el matiz de la 218 y la 222, propone además dos familias en lugar de tres: código y documentos.

Lo detalla la sección «Documentos».

## Casos | Cómo han ido hoy la 222 y la 263 | Casos {#casos}

### Lo que funcionó

- **El subagente prepara y el principal pregunta.** Los dos informes acaban en «Decidir»: preguntas numeradas, opciones A, B, C y una recomendación. El principal las llevó de una en una y salieron cuatro decisiones en una mañana (201-204).
- **Cada decisión, registrada al tomarse,** en su archivo y con la tarea en su origen. Ninguna se ha perdido.
- **Un paso «Decidir con el propietario… y registrarlo»** al final del trabajo. Hace visible que la tarea espera al propietario y no al subagente.
- **La descripción de la 190 decía cuándo terminaba:** «La tarea termina con cada acuerdo registrado como decisión.»
- **Partir lo que crece.** La 190 se separó en tareas de decidir (263), de especificar (191) y de implementar (193). Así lo decidido no esperaba a lo pendiente.

### Lo que estorbó

- **Las preguntas cambian y el informe no.** La 222 pasó de seis preguntas a «revisadas con la 201» y a «cuatro ajustadas a 203 y 204». Esas versiones solo están en el resumen del informe en la cola. El documento del worktree sigue en la versión 1.0, con las seis originales y sin saber cuáles se decidieron.
- **Los dilemas abiertos no tienen sitio.** «Dudas: excepción de la 203 en la 201 y si la SF migra docs/decisiones» (222) es una línea del historial. Si la tarea se cierra, se pierde. Lo mismo pasa con «Aplazadas las tres decisiones» (222, paso 2): se aplazaron, pero no se dice a dónde.
- **Preguntas que dependen de otra tarea.** La pregunta 2 de la 263 (quién hace los commits) depende de la 5 de la 222 (formato de commit). La 5 de la 263 depende de los campos que añade la 222. La 191 espera a la 1 de la 222. Esto solo está escrito en los informes. En la cola no se ve, y el propietario lo tiene que recordar al responder.
- **Pasos genéricos y pasos por pregunta, mezclados.** La 263 tiene un paso por decisión (2-5) y además «Decidir con el propietario las seis preguntas» (6): se cuenta lo mismo dos veces. La 222 tiene un solo «Decidir lo que salga», y la cuenta 3/6 no dice cuántas preguntas faltan.
- **Cuándo termina.** La 222 está en curso desde el 31 de octubre. Nada marca cuándo basta con lo decidido y lo demás puede esperar.
- **Qué se «prueba».** Toda tarea en curso lleva «Activar rama para poder probar» (174). En una deliberativa no hay nada que activar. La 154 y la 172 lo resuelven en la práctica: el OK es cerrar y el cierre marca el paso. Pero el paso no dice la verdad, y el encargo pide «pasa las pruebas» y «qué mirar en la prueba».
- **Deliberar y aplicar en la misma tarea.** La 222 empezó corrigiendo la skill de incorporar (paso 1) y luego pasó a deliberar. La 255 investigó, aplicó dos decisiones y pasó por observación. No es malo, pero el tipo deja de decir cómo se cierra.
- **Rama vacía.** La 201 se puso en curso con rama y sin trabajo. No podía volver a la cola, así que se descartó y se creó de nuevo como 274: perdió su número y su historial. Ya está en la cola como «Una tarea en curso con rama vacía no puede volver a la cola» (275).

## Paso 1 | Tipos de tarea: pensar, estudiar y diseñar | Tipos {#tipos}

La descripción nombra estudiar, pensar, dialogar y diseñar. Los siete tipos de la cola ya los cubren: estudiar es investigar, pensar y dialogar son deliberar y diseñar es diseñar. Falta decir qué entrega cada tipo y cómo se trata.

| Tipo | Entrega | Familia |
| --- | --- | --- |
| investigar | Un informe de hallazgos: qué hay, qué pasa, con evidencia | Deliberativa |
| deliberar | Decisiones registradas y dilemas con destino | Deliberativa |
| diseñar | Un diseño (formato, esquema, interfaz, flujo) y las decisiones que lo fijan | Deliberativa |
| especificar | Un documento normativo: especificación, criterios | Documental |
| documentar | Un documento actualizado o nuevo | Documental |
| implementar | Código y pruebas | Código |
| corregir | Un fallo arreglado, con su prueba | Código |

### Las fases del método

Fuera del alcance de esta tarea, por indicación del propietario: qué tipos de tarea y qué skills usa cada fase del método va a «Qué tipos de tarea y skills usa cada fase del método» (298). Lo que había aquí, una tabla de fases con sus tipos y skills, se conserva en el respaldo `_respaldo/Tareas deliberativas_antes-fases.md`, como punto de partida para esa tarea.

### Opciones

- **A. Siete tipos en tres familias** (código, deliberativas, documentales). La familia decide los pasos de cierre, el encargo y el final. *Pros:* no cambia nada de lo que ya tiene tipo; solo añade una tabla. *Contras:* hay que explicar el matiz entre investigar, deliberar y diseñar.
- **B. Tipos nuevos: pensar, estudiar, dialogar.** *Pros:* son las palabras del propietario. *Contras:* se solapan con investigar y deliberar; hay que retipar la cola, las propuestas y el panel.
- **C. Reducir a tres** (deliberar, documentar, implementar). *Pros:* lo más simple. *Contras:* se pierde información útil (corregir frente a implementar, investigar frente a decidir) y hay que deshacer la 145.

**Recomendación: A.**

## Paso 2 | Registrar decisiones y dilemas abiertos | Registro {#registro}

Las decisiones ya tienen su sitio y su orden (`docs/decisiones/`, el principal; la 283 añade `cola.py decision`). Falta el sitio de los **dilemas abiertos**: las preguntas planteadas y no decididas, y las que surgen al decidir otras.

### Dónde viven mientras la tarea dura

- **A. En el informe de la tarea, sección «Decidir», con su estado.** El subagente la mantiene al día con cada respuesta: «Decidida: … (203)», «Aplazada: a la tarea N», «Abierta», «Depende de «…» (N)», «Descartada». Sube la versión del informe. *Pros:* un solo sitio, el que ya se usa; el informe final cuenta la historia completa. *Contras:* hay que mandar al subagente una vez por decisión (ya se hace).
- **B. Un campo `dilemas` en la tarea de la cola** (`cola.py dilema añadir N "…"`). *Pros:* se ve en el panel. *Contras:* otra estructura en la cola y otra orden más; al salir la tarea, queda enterrado en `historial.jsonl`.
- **C. Un archivo propio, `dilemas.md`.** *Pros:* todos los dilemas del proyecto juntos. *Contras:* un registro más, que se solapa con `docs/propuestas.md` (que ya tiene el estado «de decisión»).

### A dónde van al cerrar

Ninguna deliberativa se cierra con una pregunta sin destino. Cada dilema abierto termina en uno de estos sitios:

1. **Una decisión**, registrada.
2. **Una tarea nueva**, deliberativa, por el menú de alta normal, si hay que decidirlo pronto. Es lo que pide la descripción: «si hace falta, abren nuevas tareas deliberativas».
3. **Una propuesta** en `docs/propuestas.md`, con estado «de decisión», si puede esperar.
4. **Descartado**, con su motivo en el informe.

### Preguntas que dependen de otra tarea

- **A. Lo dice el informe y la cola lo refleja.** El paso de esa pregunta pasa a «Esperar a «…» (N)», como ya prevé `sf:orquestacion`. El principal pregunta juntas las que van juntas. *Pros:* usa lo que ya existe. *Contras:* el propietario sigue viendo dos tareas.
- **B. Fusionar las tareas** cuando comparten preguntas (la 222 y la 263). *Pros:* una conversación. *Contras:* tareas grandes, que luego hay que partir.
- **C. Decidir con un supuesto** y marcar la decisión como revisable. *Pros:* no bloquea. *Contras:* decisiones provisionales, que nadie revisa.

**Recomendación:** A en las tres preguntas. El informe es el registro vivo; al cerrar, cada dilema tiene destino; y las dependencias se marcan con «Esperar a…».

**Decidido en buena parte** (221): mientras la tarea dura, los dilemas viven en su informe; si la tarea se quiere cerrar con temas abiertos, cada uno sale a su propia tarea con `/sf_split` y la deliberativa se cierra con lo decidido. Ningún dilema se pierde al cerrar.

## Paso 3 | Una skill por tipo de tarea | Skill {#skill}

El subagente de una deliberativa no carga `sf:orquestacion`. Lo que sabe de cómo trabajar le llega en el encargo, que hoy genera `cola.py encargo` igual para todos los tipos.

- **A. Ninguna skill nueva: el encargo cambia con la familia y `sf:flujo_tareas` lleva un apartado «Por tipo».** El encargo de una deliberativa pide el informe con «Decidir» (preguntas, opciones, pros y contras, recomendación, dependencias) y, en lugar de «qué mirar en la prueba», «qué queda abierto». Para especificar o diseñar, nombra la skill del oficio (`diseno_interfaz`, `definicion_tecnica`, `documento_vision`, `documento_fundacional`). *Pros:* es un comando, no inferencia (metodología, 1); no hay que mantener nada más. *Contras:* el encargo crece unas líneas.
- **B. Una skill `sf:deliberar`** para las tres deliberativas: cómo preparar preguntas, el formato del informe y el registro de dilemas. *Pros:* sitio propio, con ejemplos. *Contras:* otra skill que hay que cargar y mantener al día con la orquestación; duplica reglas.
- **C. Una skill por tipo.** *Pros:* máximo detalle. *Contras:* siete skills, mucho mantenimiento. La P04 ya advierte de los demasiados ciclos.

**Recomendación: A.** Si tras unas cuantas deliberativas el encargo no basta, entonces B.

## Paso 4 | Cerrar las documentales con un paso de aprobación | Cierre {#cierre}

Hoy toda tarea en curso recibe «Activar rama para poder probar» y «Cerrar la tarea» (174). En las que no tienen prueba, el OK del propietario es la aprobación y el cierre marca el primero (154, 172). Funciona, pero el paso dice algo que no pasa.

- **A. Pasos de cierre por familia.** Código: «Activar rama para poder probar» y «Cerrar la tarea», como hoy. Deliberativas y documentales: «Aprobar el resultado» y «Cerrar la tarea». La aprobación se marca al cerrar, con el OK, igual que hoy el de activar. Si cambia el tipo y con él la familia, `cola.py tipo` cambia el paso pendiente. *Pros:* el paso dice lo que pasa (el espíritu de la 204); el panel y el encargo saben qué ofrecer. *Contras:* toca `cola.py`, el panel y sus pruebas; una tarea sin tipo se queda con los de código.
- **B. Como hoy.** *Pros:* coste cero. *Contras:* el paso miente, y el principal tiene que recordar cada vez que no se prueba.
- **C. Solo «Cerrar la tarea»** en las que no son de código. *Pros:* lo más corto. *Contras:* rompe la regla «siempre dos pasos de cierre» de la 174 y hay que añadir uno al cambiar a implementar.

Para las deliberativas hay una pieza más: hoy el principal añade a mano «Decidir con el propietario… y registrarlo» en cada una (222, 263, 274). Con A, ese paso de trabajo lo podría poner `cola.py` al poner en curso una deliberativa, igual que pone los de cierre.

Ninguna de las dos familias pasa a observación: su resultado ya lo ha visto el propietario al aprobarlo (154). Activar la rama sigue siendo posible, por ejemplo para ver un HTML generado, pero no es un paso.

**Recomendación: A**, con el paso «Decidir…» automático en las deliberativas.

## Paso 5 | Cola, panel, objetivo, pasos y final | Forma {#forma}

### Cómo se ven en la cola y el panel

- **A. Como hoy (el tipo tras el título) más una cuenta de decisiones.** Al registrar una decisión con `cola.py decision --tarea N` (la orden de la 283), la tarea anota el evento `decision NNN` en su historial. El panel lo cuenta: «· 3 decisiones». *Pros:* se ve el avance real sin campo nuevo; el historial ya es la fuente del panel (145). *Contras:* un argumento más en una orden aún en curso.
- **B. Como hoy.** *Pros:* nada que hacer. *Contras:* la cuenta n/m es lo único que se ve, y en las deliberativas dice poco.
- **C. Una sección propia o un color para las deliberativas.** *Pros:* se distinguen de un vistazo. *Contras:* la letra y el color son el estado (054, 084); mezclarlo confunde.

**Recomendación: A.**

### Cómo se escriben su objetivo y sus pasos

- **Título:** lo que queda decidido o la pregunta, con el verbo del oficio: «Decidir dónde guarda su versión un proyecto», «Diseñar .sf/proyecto.json». Sin prefijos.
- **Descripción:** el primer párrafo, la pregunta y para qué hace falta decidirla; el último, cuándo termina: «Termina con cada pregunta decidida o con destino.» Es lo que funcionó en la 190.
- **Pasos:** al principio, «Analizar…» y «Proponer…». Cuando llega el informe, el principal cambia el «Decidir…» genérico por **un paso por pregunta**: «Decidir quién hace los commits». Hecho, en participio y con su número: «Decidido quién hace los commits: Claude en la rama (205)». Si se aplaza: «Aplazado el formato de commit: a la tarea N». Si espera a otra: «Esperar a «…» (N)».

Opciones para los pasos: **A**, un paso por pregunta, que sustituye al genérico (recomendada: la cuenta dice cuántas faltan y el panel enseña cuál toca); **B**, un solo paso genérico, como en la 222 (menos escrituras, pero no se ve el avance).

### Cuándo terminan

- **A. Cuando cada pregunta del informe tiene destino** (decidida, a otra tarea, a propuesta o descartada) y el informe está al día. Entonces el principal propone cerrar y enseña la tabla final de «Decidir». *Pros:* un criterio comprobable; nada se pierde. *Contras:* obliga a dar destino a todo, aunque sea «propuesta».
- **B. Cuando lo diga el propietario.** *Pros:* flexible. *Contras:* es lo de hoy: la 222 lleva días abierta y la 190 se alargó hasta partirse.
- **C. A, y además un aviso:** si una deliberativa pasa una sesión sin decidir nada, el principal propone cerrarla con lo decidido y pasar lo abierto a tareas o propuestas («Cerrar antes que abrir», 157). *Pros:* evita las deliberativas eternas. *Contras:* una regla más que recordar.

**Recomendación: C.**

**Decidido en buena parte** (221): una deliberativa se cierra cuando se quiere cerrar; lo que siga abierto sale a su tarea, separado. Queda solo si el principal propone cerrar las que se estancan (pregunta 10).

### Aplicar lo decidido

**Decidido** («Una tarea deliberativa da un informe y las tareas que salgan», 218). Una deliberativa produce su informe, con el formato de los fundacionales y su HTML. Lo que haya que aplicar lo hacen otras tareas que ella crea (deliberativas, documentales o de implementación), y cuáles se decide con el propietario a medida que avanza. No cambia código ni otros documentos, ni siquiera con retoques de una línea. Es la opción A sin su excepción.

En la práctica, cada tarea que nace de una deliberativa entra por el menú de alta, con su tipo, y en la deliberativa queda un paso hecho: «Creada la tarea N para …». El informe la nombra como destino de su pregunta.

## Documentos | Las tareas de documentos de punta a punta | Documentos {#documentos}

Recorrido de una tarea de documentos con las decisiones de hoy: «Los documentos de la SF van en la carpeta sf/» (203), «Las decisiones son material de la SF: siempre en sf/decisiones/» (208), «Lo que falta por concretar va como pasos de la tarea» (211), «Testing pasa a llamarse «En observación»» (212), «En observación, sin alias ni rastros» (215) y, sobre todo, la 216. Para cada momento: cómo es hoy, el hueco y la sugerencia.

### Clases de documento

| Documento | Dónde vive | Cómo se genera el HTML |
| --- | --- | --- |
| Visión | `docs/specs/vision/`, del proyecto | `documento_vision/scripts/doc_to_html.py` |
| Fundacional | `docs/specs/vision/fundacional-*.md` | `documento_fundacional/scripts/fundacional_to_html.py` |
| Informe de tarea | `docs/referencias/reports/`; con la 203, `sf/informes/` | `fundacional_to_html.py` (por su cabecera `antetitulo`, `lema`, `portada`) |
| Especificación | `docs/specs/funcional/` | Ninguno: no tiene HTML |
| «Cómo funciona…», «Mejora continua» | `docs/` | `doc_to_html.py` |
| README | raíz | `scripts/readme_a_html.py`, que llama a `doc_to_html.py` |
| Compartidos: metodología, plantilla, CLAUDE.md | plugin y raíz | Ninguno |
| Decisiones y su índice | `docs/decisiones/`; con la 208, `sf/decisiones/` | El índice HTML lo genera el panel al abrirlo y no se versiona (163) |
| Propuestas | `docs/propuestas.md`; con la 203, `sf/propuestas.md` | Ninguno |

### Cómo nace

Hoy nace como cualquier tarea, de tipo documentar o especificar. Con la 211, lo que falte por concretar va como pasos.

- **Hueco: las fases de las skills no se ven en la cola.** `documento_vision` sigue cuatro fases (valorar la idea, acordar las secciones, escribir y afinar sobre el HTML); el fundacional, parecidas. La cola no las refleja, y la tarea parece un único bloque.
- **Sugerencia:** al poner en curso una tarea de documentos, el principal planifica los pasos con las fases de la skill del oficio: «Acordar las secciones», «Escribir la primera versión», «Afinar sobre el HTML». Cada vuelta de afinado es la iteración de la 216. No hace falta código: basta con una línea en `sf:orquestacion`.

### Solo su documento

El matiz de la 216: una tarea de documentos no lleva pasos de implementación ni otros que cambien activos distintos de su documento (código, skills, otros documentos).

- **Hueco: hoy nada lo detecta.** La 222 empezó corrigiendo una skill y luego pasó a deliberar. Cualquier `paso añadir` entra sin mirar qué toca, y `cerrar` hace squash de todo lo que haya en la rama.
- **Opciones:**
  - **A. La tarea declara su documento y `cola.py` lo vigila.** `cola.py documento N <ruta>` anota la ruta (el `.md`, su `.html`, su carpeta de imágenes, si la tiene, y sus respaldos `_respaldo/<nombre>_antes-*`, 217). La orden de copia de la 216 solo copia eso. `cerrar` se niega si la rama cambia otros archivos y dice cuáles. El menú al anotar, en una tarea documental, ofrece «tarea nueva» en vez de «paso de esta» cuando lo pedido toca otro activo. *Pros:* se cumple solo, con un comando; lo que entra en `develop` es siempre el documento. *Contras:* un campo nuevo en la tarea; hay que declarar la ruta.
  - **B. Solo la regla, en `sf:orquestacion` y en el encargo.** *Pros:* sin código. *Contras:* depende de que el principal se acuerde, que es lo que falló en la 222.
  - **C. Solo la comprobación al cerrar**, por tipo: en una documentar o especificar, la rama solo puede tocar archivos `.md`, `.html` y de imagen. *Pros:* sin campo nuevo. *Contras:* deja pasar otro documento, o una skill, que también es `.md`.
- **Una decisión que pide cambiar código.** Se registra (`cola.py decision`, que va a `develop` por su cuenta, como las propuestas, y no cuenta como activo de la tarea) y su aplicación va a una tarea nueva por el menú de alta. El documento describe lo que ya es, no lo que será. Si un apartado depende de esa aplicación, su paso pasa a «Esperar a «…» (N)», o el documento lo marca como pendiente.
- **Recomendación: A**, que incluye el menú de B.

### Quién escribe y dónde vive mientras se itera

Hoy escribe el subagente, en su worktree y en `sub-NN` (151). El propietario lo lee yendo al worktree, como en la 222. La 216 cambia esto: en cada vuelta, el documento nuevo se copia a `develop` con un commit, sin cambiar la rama activa.

- **Hueco 1: la recogida del subagente mira los commits.** Con la copia, el documento llega a `develop` en un commit distinto de los de `sub-NN`. Para `cola.py`, la auxiliar «tiene commits que no entraron en develop». Al cerrar, la deja con aviso (`recogida-con-avisos`) y, si la tarea tiene rama, `cerrar` se niega (200).
- **Hueco 2: la rama sobra.** Si la tarea solo crea un documento nuevo y la copia ya lo lleva a `develop`, el squash final no aporta nada, y una rama vacía no puede volver a la cola (275).
- **Opciones:**
  - **A. Documento nuevo, sin rama de tarea.** El worktree del subagente sale de `develop` en `sub-NN`. La copia lleva el documento a `develop` en cada vuelta. Al cerrar, «Cerrar sin rama» (20), y la recogida comprueba que el documento de `sub-NN` es igual al de `develop` (`git diff develop sub-NN -- <ruta>` vacío) en lugar de mirar la ascendencia. *Pros:* coherente con la 216; sin squash vacío ni rama que estorbe. *Contras:* la recogida necesita otra regla para estas tareas.
  - **B. Con rama, como hoy, más la copia por vuelta.** *Pros:* sin cambiar la recogida… salvo el hueco 1, que sigue. *Contras:* squash vacío y avisos en cada cierre.
- **Para los documentos que ya existen**, la 216 mantiene la rama y el cierre normal: el panel abre al activar la rama los HTML que cambia (tarea 206).
- **Recomendación: A.** Vale también para los informes de las deliberativas, que son documentos nuevos: el de la 222 se habría leído en `develop` desde la primera vuelta.

### Cómo se genera y se abre el HTML

Hay tres generadores, y cuál toca depende de la clase de documento. Ninguna regla lo dice fuera de cada skill. Los HTML se versionan, y hoy están al día: ninguno de los trece `.md` con HTML ha cambiado después que su HTML. Pero eso depende de que alguien lo regenere a mano.

- **Hueco 1: nada regenera el HTML cuando cambia el `.md`.** Seis informes de `docs/referencias/reports/` no tienen HTML, entre ellos «Configuración inicial» y «Auditoría de la orquestación».
- **Hueco 2: la 216 ofrece abrir el HTML, pero solo la T lo abre**, al activar la rama (diff `develop...rama`). Un documento nuevo sin rama no la pasa nunca.
- **Opciones para generar:**
  - **A. Una orden única**, `sf_html.py <ruta>.md`, que elige el generador por la cabecera del documento (`antetitulo`/`portada`: fundacional; si no, visión; `README.md`: el suyo). La usan la copia a `develop` y `cerrar` siempre que el `.md` tiene HTML al lado o la cabecera pide uno. *Pros:* comando, no inferencia; el HTML nunca queda atrás. *Contras:* una pieza más en el plugin.
  - **B. No versionar los HTML y generarlos al abrir**, como el índice de decisiones (163). *Pros:* sin choques entre ramas por archivos generados. *Contras:* en GitHub o en otra copia no hay HTML que leer; el panel tendría que generarlos.
  - **C. Como hoy**, con la regla en cada skill. *Pros:* nada que hacer. *Contras:* el hueco sigue.
- **Opciones para abrir:**
  - **A. La orden de copia a `develop` abre el HTML** en el navegador al acabar, igual que la T, y lo dice en su salida. *Pros:* se cumple la 216 sin depender de Claude. *Contras:* abre una ventana en cada vuelta, aunque el propietario no la quiera.
  - **B. El principal lo ofrece en cada vuelta** con la herramienta de preguntas y lo abre con una orden. *Pros:* el propietario elige. *Contras:* una pregunta más por vuelta.
- **Recomendación: A en las dos.**

### Imágenes y SVG

Los diagramas son SVG dentro del `.md` (guía de diagramas): viajan con el documento y no dan problemas. Las capturas son PNG aparte (`docs/capturas/panel/`, `docs/specs/vision/capturas/`), con rutas relativas.

- **Hueco:** la copia de la 216 y la vigilancia de «solo su documento» tienen que incluir la carpeta de imágenes, y la migración a `sf/` tiene que rehacer las rutas relativas.
- **Sugerencia:** el documento de una tarea es su `.md`, su HTML y su carpeta `<nombre>/` o `capturas/`, si la tiene. Las imágenes de un documento van en una carpeta junto a él, nunca compartida con otro documento.

### Respaldo antes de sustituir

La 217: antes de sustituir un documento por una versión nueva, la anterior se copia a `_respaldo/`, en la misma carpeta, como `<nombre>_antes-<motivo>.<ext>`, junto con su HTML. Volver atrás es copiarla de vuelta, sin git. El precedente es `docs/specs/vision/_respaldo/`, con seis copias de la visión de la SF.

Dónde entra en el ciclo:

- **Documento nuevo, en cada vuelta (216).** La primera vuelta no respalda: no hay nada que sustituir. Desde la segunda, la orden de copia respalda la versión de `develop` antes de copiar la nueva, y lleva el respaldo en el mismo commit.
- **Documento que ya existe, con rama.** Lo respalda quien lo reescribe, el subagente con la skill del oficio, en su rama; el respaldo entra con el squash.
- **Volver atrás.** Es una vuelta más: la versión actual se respalda antes de copiar la respaldada encima, para que volver atrás también se pueda deshacer.

Huecos y sugerencias:

- **Nombres repetidos.** Dos vueltas con el mismo motivo darían el mismo nombre, y la segunda pisaría la primera. *Sugerencia:* si el nombre ya existe, la orden añade `-2`, `-3`… Opciones: A, sufijo solo si choca (recomendada: el nombre sigue siendo el de la 217); B, fecha y hora siempre (`_antes-<motivo>-AAAAMMDD-HHMM`), que nunca choca pero alarga todos los nombres.
- **Las búsquedas encuentran texto viejo.** ripgrep, y con él la búsqueda de Claude, no se salta `_respaldo/`: Claude puede citar una versión sustituida como si fuera la vigente. Opciones: A, un archivo `.ignore` en la raíz con `_respaldo/`, que ripgrep respeta y git no (recomendada); B, nada, y que las skills lo adviertan. *Contra de A:* para buscar en los respaldos hay que pedirlo expresamente (`--no-ignore`).
- **Qué documentos se respaldan.** Los registros que crecen por partes, como `propuestas.md`, el índice de decisiones o las decisiones, no se sustituyen: se editan. Opciones: A, solo los documentos que se reescriben como un todo (visión, fundacional, informes, especificación, «Cómo funciona…»); los registros, no (recomendada); B, todo documento que cambie una tarea de documentos.
- **El HTML respaldado, un nivel más abajo.** Sus enlaces relativos (imágenes, otros documentos) dejan de funcionar, aunque el CSS va dentro. *Sugerencia:* aceptarlo; el respaldo es para volver atrás, no para leerlo. Si hace falta, la orden única de HTML lo regenera tras copiarlo de vuelta.
- **Encaje con «solo su documento».** Los respaldos son parte del documento: la vigilancia de la pregunta 2 los admite, y la migración a `sf/` los mueve con él.
- **Crecimiento.** Se versionan siempre y no se borran. En un informe con muchas vueltas pueden ser decenas de copias. Por ahora no hace falta nada: son texto, y git comprime.

### Cómo se revisa y se aprueba

El kit de documentos ya trae la revisión. El propietario anota en el HTML y «Guardar» crea una copia anotada, `<nombre>.notas-<autor>.html`. Después, `extraer_notas.py` saca las notas por sección para llevarlas al `.md`.

- **Hueco: el recorrido no se cruza con la tarea.** No se dice dónde deja el propietario la copia, cómo le llega al subagente ni que no hay que versionarla: `.gitignore` no tiene `*.notas-*.html`.
- **Opciones:**
  - **A. La copia anotada se guarda junto al documento, fuera de git** (`*.notas-*.html` en `.gitignore`). El propietario dice «notas» o usa `/sf_paso`, y el subagente aplica `extraer_notas.py` en la vuelta siguiente. *Pros:* usa lo que ya existe. *Contras:* el propietario tiene que guardar la copia en el sitio correcto.
  - **B. Las notas, por el chat**, como hoy. *Pros:* nada nuevo. *Contras:* se pierde la cita exacta y el sitio de cada nota.
- **La aprobación** es el paso «Aprobar el resultado» (paso 4): se marca con el OK al cerrar. Un documento nuevo ya está en `develop`. Uno que ya existía se cierra con squash, sin pasar por observación.
- **Recomendación: A.**

### Documentos compartidos y sus tareas «Actualizar…»

Una tarea que cambia la metodología, la plantilla, el CLAUDE.md o «Cómo funciona…» no los toca: añade «Reflejar «…» (NN)» a la tarea «Actualizar <documento>» (142, 147). Estas tareas se hacen de una en una, cada una con su subagente (152).

- **Hueco 1: no se hacen nunca.** «Actualizar Cómo funciona el panel» (198) tiene 66 pasos pendientes desde el 30 de octubre; la de las reglas del método (208), 45; la de «Cómo funciona la Software Factory» (219), 29. Mientras tanto, «Cómo funciona…» no ha cambiado desde el 30 de octubre, y la metodología sigue sin la 154. Quien entra a la SF lee documentos con días de retraso.
- **Hueco 2: se reflejan cosas que aún no han pasado.** La 147 añade el paso al poner la tarea de origen en curso. La 198 ya tiene «Reflejar «Testing pasa a En observación» (291)», y la 291 sigue en cola. Si una tarea se descarta, su paso se queda.
- **Hueco 3: el texto propuesto se pierde.** Los subagentes devuelven «documentos compartidos a actualizar, con el texto propuesto», pero ese texto solo queda en el informe al principal. El paso 30 de la 208 dice «con el texto propuesto en su informe», que nadie guarda.
- **Hueco 4: el CLAUDE.md contradice a la 152.** Dice «de una en una y en el principal»; la 152 y `sf:orquestacion` dicen «cada una con su subagente».
- **Opciones para el hueco 1:**
  - **A. Aviso y umbral.** RELEASE avisa de las tareas «Actualizar…» con pasos pendientes, como avisa de las que están en observación. En «Libre», el principal las propone primero cuando pasan de diez pasos o de una semana. *Pros:* no cambia el mecanismo y publicar con documentos atrasados se ve. *Contras:* sigue dependiendo de que se pongan en curso.
  - **B. Cada tarea actualiza el documento compartido en su rama.** *Pros:* el documento siempre al día. *Contras:* deshace la 142 y la 147: choques entre ramas en los mismos párrafos, que es lo que se quiso evitar.
  - **C. Como hoy.**
- **Opciones para el hueco 2:**
  - **A. El paso «Reflejar» se añade al cerrar la tarea de origen**, no al ponerla en curso. *Pros:* solo se refleja lo que ya está en `develop`. *Contras:* cambia la 147; hay que acordarse al cerrar. Lo puede hacer `cola.py cerrar` si la tarea anota sus documentos afectados.
  - **B. Se añade al empezar, con «Esperar a «…» (N)»** hasta que la de origen se cierre. *Pros:* se ve pronto. *Contras:* pasos que esperan, y la cola crece.
  - **C. Como hoy.**
- **Para el hueco 3:** el paso «Reflejar» se escribe con el texto propuesto en el informe de la tarea de origen (el texto va en su informe, y el paso lo cita por su título). Si la tarea no tiene informe, el texto va en la descripción del squash. No hace falta orden nueva.
- **Para el hueco 4:** corregir el CLAUDE.md en la 208, sin pregunta: lo decidido es la 152.
- **Recomendación: A en el hueco 1 y A en el hueco 2**, con `cola.py cerrar` añadiendo el paso.

### Lo que se cambia en paralelo

La 152 impide que dos tareas del mismo grupo de documentos compartidos vayan a la vez. Las skills, en cambio, las cambian muchas tareas a la vez (`sf:flujo_tareas`, `sf:orquestacion`), y sus choques se resuelven al integrar `develop` (270). Con la 216, un documento nuevo no choca, porque solo lo escribe su tarea. Un documento que ya existe sigue con rama: `choques` lo ve como cualquier otro archivo (130). Los HTML generados chocan siempre que chocan sus `.md`. Con la opción A de «Cómo se genera», se regeneran tras resolver el choque, en lugar de resolverlos a mano.

### La migración a sf/

La 203 y la 208 llevan a `sf/` las propuestas, los informes y las decisiones. Afecta a:

- los enlaces relativos de todos los documentos que los citan, y sus HTML;
- las rutas fijas de `cola.py`, el mod (`lectura.ts` lee `docs/propuestas.md` en `develop`) e `indice_decisiones.py`;
- `.gitignore` (`!docs/referencias/reports/`, `docs/decisiones/README.html`) y `.gitattributes` (`merge=union`);
- las tareas en vuelo: la 222, la 263 y esta tienen su informe en `docs/referencias/reports/` de su worktree. Si la migración entra antes, el informe vuelve al sitio viejo al integrarse.

Opciones: **A**, migrar cuando no haya en curso tareas con informes o documentos de la SF, y que la orden de copia de la 216 escriba en la ruta configurada; **B**, migrar ya y que cada subagente mueva su informe al integrar `develop`. **Recomendación: A.**

Un detalle de nombres: la metodología (9) llama `reports/` a los resultados de las pruebas, fuera de git, y los informes de tarea están en `docs/referencias/reports/`, versionados. Con la 203, el segundo pasa a `sf/informes/`, y la ambigüedad desaparece. Conviene decirlo en la metodología al migrar.

### El diálogo de las skills de documentos

`documento_vision` empieza con «valorar la idea en conversación». Con la 151, la conversación la tiene el principal y el trabajo, el subagente.

- **A. El subagente prepara las preguntas de cada fase en tanda** (como las de «Decidir») y el principal las lleva al propietario. *Pros:* respeta la 151. *Contras:* la conversación es menos fluida.
- **B. El principal hace la fase de diálogo**, con la instrucción expresa del propietario que admite la 151, y el subagente escribe. *Pros:* conversación natural. *Contras:* el principal trabaja en la tarea.
- **Recomendación: A**, y B cuando el propietario lo pida.

### Encaje con las familias

- **Documentales** (especificar, documentar): son estas tareas. Pasos de cierre «Aprobar el resultado» y «Cerrar la tarea» (paso 4). Solo su documento, con sus respaldos. Sin rama si el documento es nuevo; con rama si ya existía. Nunca pasan por observación.
- **Deliberativas:** su único documento es su informe (218). Es un documento nuevo, así que la 216 y la 217 valen para él: copia a `develop` en cada vuelta, respaldo antes de sustituir y apertura en el navegador. Las decisiones, las propuestas y las tareas que crea van por su propia orden, sin rama. «Solo su documento» vale igual que en las documentales: nada de código ni de otros documentos.
- **Código:** sin cambios. Si su tarea cambia un documento compartido, el paso «Reflejar» en la «Actualizar…», al cerrarse.

## Separar | Lo que ya es de otra tarea | Separar {#separar}

Aplicando la 221 a esta tarea: la sección «Documentos» (paso 7) empezó como «ya que estás» y ya es otra deliberación, el ciclo de las tareas de documentos. Parte de ella, además, solo da forma a la orden que implementa «Documentos nuevos a develop en cada vuelta, y abrirlos en el navegador» (297). Propuesta concreta, con el OK del propietario:

1. **`/sf_split 274 7`**: nace una deliberativa, «Ciclo de las tareas de documentos: solo su documento, Actualizar… y revisión», con el paso 7 y la sección «Documentos». Su informe propio sale de esa sección, y en este queda un enlace. Se lleva las preguntas 2, 3, 5, 14, 15 y 16.
2. **Pasos «Decidir…» en la 297** («Lo que falta por concretar va como pasos de la tarea», 211), porque solo dan forma a su orden: las preguntas 4, 7, 11, 12 y 13.
3. **En la 274 quedan** las de tipos, pasos y cierre: 1, 6, 8, 9, 10, 17 y 18.
4. **Fases del método:** ya separadas, a «Qué tipos de tarea y skills usa cada fase del método» (298), por indicación del propietario. Ninguna pregunta de la lista depende de ellas.

Opciones: A, las tres a la vez (recomendada: cada tarea conserva su foco y la 274 se cierra antes); B, solo el split, dejando en la nueva también las de la 297; C, no separar y decidirlo todo aquí.

## Decidir | Lo que decide el propietario | Decidir {#decidir}

**Ya decidido.**

- Una tarea de documentos solo toca su documento; un documento nuevo va a `develop` en cada vuelta y se ofrece en el navegador (216).
- Antes de sustituir un documento, se respalda (217).
- Una deliberativa da un informe con el formato de los fundacionales y las tareas que salgan, y no cambia código ni otros documentos (218).
- El tipo decide cómo se maneja el repositorio: código, con rama, worktree, squash y observación; documento nuevo (también el informe de una deliberativa), sin rama, con copia a `develop` en cada vuelta y respaldo, y cierre con aprobación; documento existente, con rama, squash y cierre con aprobación. El modelo `develop`/`main` no cambia (219).
- Cada cambio de un `.md` que tiene o debe tener HTML regenera su HTML en el mismo cambio, con una orden única que elige el generador (220).
- Lo que es de otra tarea se propone separar; si una deliberativa se cierra con temas abiertos, salen con `/sf_split` (221).
- Una deliberativa solo cambia documentos y se maneja en todo como una documental (218, matiz).
- En el panel, una deliberativa se cierra con «Finalizar deliberación», que es la misma orden que cerrar (222).

Con la 218, la antigua pregunta «Aplicar lo decidido» queda resuelta. Con la 219, las familias y el camino de un documento nuevo quedan encaminados, y el cierre de las tareas sin código es con aprobación. Con la 220, la pregunta de regenerar el HTML queda resuelta con su opción A. Las de cuándo termina, dilemas, skill y «solo su documento» se acotan.

Con la 221, la antigua «Cuándo termina una deliberativa» se reduce a la pregunta 10, y «Dónde viven los dilemas abiertos» queda resuelta: en el informe, y al cerrar, a su tarea.

Lo que queda, por orden de importancia. Entre corchetes, a dónde iría con la separación: [274], [nueva] o [297].

1. **Dos familias en lugar de tres** [274]. Con el matiz de la 218, una deliberativa solo cambia documentos y se maneja como una documental. A, dos familias, código (implementar, corregir) y documentos (los otros cinco tipos), y dentro de documentos el camino lo decide si el documento declarado ya existe; investigar, deliberar y diseñar se distinguen solo por su proceso: sección «Decidir», «Decidir…» automático y separaciones (recomendada); B, mantener tres familias, con la deliberativa aparte; C, tipos separados para crear y para cambiar un documento.
2. **Cómo se cumple «solo su documento»** [nueva], en documentales y deliberativas. A, la tarea declara su documento (en una deliberativa, su informe); la orden de copia solo copia eso, `cerrar` se niega si la rama toca otros archivos y el menú ofrece tarea nueva (recomendada); B, solo la regla en la orquestación y el encargo; C, solo una comprobación por tipo al cerrar.
3. **Las tareas «Actualizar…» atascadas** [nueva]. A, RELEASE avisa y en «Libre» se proponen primero pasado un umbral (recomendada); B, cada tarea actualiza el documento compartido en su rama; C, como hoy.
4. **El subagente de un documento nuevo** [297]. La 219 ya quita la rama de la tarea. A, worktree desde `develop` en `sub-NN`; la recogida compara el documento con el de `develop`, no los commits (recomendada); B, sin worktree: el subagente escribe en una carpeta temporal y la orden de copia lo lleva a `develop` desde allí.
5. **Cuándo se añade «Reflejar»** [nueva]. A, al cerrar la tarea de origen, y lo añade `cola.py cerrar` (recomendada); B, al empezar, con «Esperar a…» hasta su cierre; C, como hoy.
6. **Pasos de cierre de la familia de documentos** [274]. La 219 y la 218 ya dicen que se cierran con aprobación, sin prueba ni observación; queda cómo se ve en la cola, igual para documentales y deliberativas. En las deliberativas, el botón ya se llama «Finalizar deliberación» y hace lo mismo que cerrar (222). A, en toda la familia, «Aprobar el resultado» y «Cerrar la tarea», con los textos de los pasos fijos, como hoy, y solo el botón cambia (recomendada); B, igual, pero en las deliberativas el último paso dice «Finalizar la deliberación», como su botón; C, solo «Cerrar la tarea», cuyo OK es la aprobación.
7. **Abrir el HTML en cada vuelta** [297]. A, lo abre la orden de copia a `develop`, como la T (recomendada); B, el principal lo ofrece con una pregunta en cada vuelta.
8. **Pasos de decisión** [274]. A, `cola.py` pone «Decidir con el propietario… y registrarlo» al poner en curso una investigar, deliberar o diseñar; al llegar el informe se sustituye por uno por pregunta, más «Creada la tarea N para …» por cada tarea que salga (recomendada); B, uno por pregunta, puesto a mano; C, un solo paso genérico.
9. **Preguntas que dependen de otra tarea** [274]. A, «Esperar a «…» (N)» y preguntarlas juntas (recomendada); B, fusionar las tareas; C, decidir con un supuesto revisable.
10. **Deliberativas estancadas** [274]. A, si una pasa una sesión sin decidir nada, el principal propone cerrarla y sacar lo abierto con splits (221) (recomendada); B, nada: lo decide el propietario cuando quiera.
11. **Respaldo con nombres repetidos** [297]. A, añadir `-2`, `-3`… solo si el nombre ya existe (recomendada); B, fecha y hora siempre en el nombre.
12. **Búsquedas y respaldos** [297]. A, `.ignore` en la raíz con `_respaldo/`, para que ripgrep y Claude no citen versiones viejas (recomendada); B, nada.
13. **Qué se respalda** [297]. A, solo los documentos que se reescriben enteros; los registros (propuestas, decisiones, índice), no (recomendada); B, todo documento que cambie una tarea de documentos.
14. **Migración a sf/** [nueva]. El informe va en `sf/informes/` (203, 218). A, migrar cuando no haya en curso tareas con informes o documentos de la SF, con la copia escribiendo en la ruta configurada (recomendada); B, ya, y cada subagente mueve su informe al integrar.
15. **Revisión con notas** [nueva]. A, copia anotada junto al documento y fuera de git; el subagente aplica `extraer_notas.py` (recomendada); B, las notas por el chat.
16. **Diálogo de las skills de documentos** [nueva]. A, el subagente prepara las preguntas en tanda y el principal las lleva (recomendada); B, el principal hace el diálogo con la instrucción del propietario.
17. **Skill** [274]. El formato del informe ya es el de `sf:documento_fundacional` (218). A, ninguna skill nueva: el encargo de una deliberativa nombra esa skill, pide la sección «Decidir» y que señale los temas ajenos para separarlos (221) (recomendada); B, una skill `sf:deliberar` con el proceso de preguntas, dilemas y separaciones.
18. **Panel** [274]. A, el tipo como hoy y una cuenta de decisiones sacada del historial (recomendada); B, como hoy; C, una sección o un color propio.

## Tareas | Qué sale de aquí y qué cambia en otras | Tareas {#tareas}

- **Aplicar las familias** (implementar): `cola.py` (pasos de cierre por familia, «Decidir…» automático, encargo por familia, `tipo` que cambia el paso), el panel si se aprueba la 18, y sus pruebas.
- **La orden de copia de la 216**, en «Documentos nuevos a develop en cada vuelta, y abrirlos en el navegador» (297), con lo que se apruebe de las preguntas 2, 4 y 7: el documento declarado, la recogida por contenido y la apertura en el navegador; y la regeneración del HTML de la 220. Y `*.notas-*.html` en `.gitignore` si se aprueba la 15. El respaldo de la 217 antes de cada copia, con lo que se apruebe de la 11 a la 13.
- **`sf:flujo_tareas` y `sf:orquestacion`** (documentar): el apartado «Por tipo» de abajo; en la orquestación, «Tareas de definición» y «Probar y cerrar» remiten a él.
- **«Las decisiones se guardan en develop…» (283):** si se aprueba la 18, `cola.py decision` admite `--tarea N` y anota el evento.
- **«Los estados de las tareas dicen lo que pasa» (291):** la 204 y este informe tocan los mismos textos; conviene que «Aprobar el resultado» entre con ese vocabulario.
- **222 y 263, ahora:** sin esperar a la implementación, sus subagentes pueden poner la sección «Decidir» al día con lo decidido (201-204) y con las dependencias entre ellas.

### Texto propuesto para `sf:flujo_tareas` (apartado «Por tipo»)

> **Por tipo.** El tipo de la tarea decide su familia, y la familia decide cómo se maneja el repositorio y cómo se cierra (219).
>
> - **Código** (implementar, corregir): rama de la tarea, worktree del subagente, squash en `develop` y observación. Pasos de cierre «Activar rama para poder probar» y «Cerrar la tarea».
> - **Documentos** (documentar, especificar, investigar, deliberar, diseñar): solo cambian su documento. Un documento nuevo va sin rama: en cada vuelta se respalda la versión anterior en `_respaldo/`, se copia a `develop`, se regenera su HTML y se ofrece abrirlo. Uno que ya existe se cambia en su rama y entra por squash. Se cierran con la aprobación del propietario, sin observación: pasos de cierre «Aprobar el resultado» y «Cerrar la tarea» (216, 217, 220).
> - **Investigar, deliberar y diseñar** son documentos con preguntas: su documento es un informe con el formato de los fundacionales, con una sección «Decidir» (una pregunta por decisión, con opciones, pros y contras, recomendación y de qué depende). El principal pone un paso por pregunta y registra cada decisión al tomarse; lo que haya que aplicar lo hacen las tareas que crean (218). Lo que es de otra tarea se propone separar en cuanto aparece y, si se cierran con temas abiertos, cada uno sale a su tarea con `/sf_split` (221). En el panel se cierran con «Finalizar deliberación» (222).
