---
antetitulo: SoftwareFactory · Documento fundacional · Octubre 2026
lema: Todas tus sesiones, // un solo puesto de mando.
subtitulo: Una aplicación de la SF para ver, conducir y medir varias sesiones de Claude Code a la vez.
version: Versión 0.1 · 27/10/2026
estado: Objetivo de diseño · Documento de proyecto
destino: proyecto
herramientas: buscador notas nota-texto nota-seccion nota-global lectura fuentes cabecera tablas aviso
pie: Claude Code Commander · Documento de desarrollo de SoftwareFactory. Diferencia hechos publicados, objetivos de diseño y supuestos. Las decisiones las toma el propietario de la SF.
---
# Claude Code Commander

> **Alcance**
> Todo lo que este documento atribuye al Claude Code Commander es un objetivo de diseño: la aplicación no existe todavía. Lo construido es el mod de la SF y JKanban, y se cuenta con sus límites. Los hechos publicados llevan su referencia; los supuestos se marcan como tales.

## Razón para desarrollar | La capa que falta encima de Claude Code | Razón {#razon}

El Claude Code Commander, en corto el CCC, es el puesto de mando de quien trabaja con varias sesiones de Claude Code a la vez. Ve todas las sesiones, las conduce, les lleva las tareas del kanban y mide cómo se trabaja. Su propósito es que una sola persona pueda dirigir varios proyectos sin perder el hilo ni la salud.

Lo que ya existe cubre partes del problema. Claude Code tiene una vista de agentes para las sesiones en segundo plano [[A1]](#src-A1 "Anthropic · vista de agentes"){: .ref}, un control remoto que lleva una sesión al móvil [[A2]](#src-A2 "Anthropic · control remoto"){: .ref} y mensajes entre sesiones [[A3]](#src-A3 "Anthropic · mensajes entre sesiones"){: .ref}. Los gestores de sesiones aíslan agentes en paralelo [[T1]](#src-T1 "Claude Squad"){: .ref}, y los tableros como Vibe Kanban lanzan un agente por tarjeta [[T7]](#src-T7 "Vibe Kanban"){: .ref}. Ninguno conoce el método de trabajo de cada proyecto, usa un kanban externo como origen de las tareas ni mide cómo dirige la persona.

La tesis es construir esa capa del método encima de las piezas oficiales, no en paralelo. Se apoya en tres hechos: el mod de la SF ya registra en cada sesión su fase, su cola y su marcador [[M4]](#src-M4 "Mod de estado de la SF"){: .ref}; Claude Code ya ofrece canales entre sesiones y hacia el móvil; y la sobrecarga de supervisar agentes está medida [[E2]](#src-E2 "Built In sobre el estudio de BCG, 2026"){: .ref}. Falta saber si una vista común reduce de verdad los frentes abiertos y el trabajo a deshora, y eso es lo que debe medir el piloto.

::: tarjetas 3

### Cada sesión es una isla

Problema observado
{: .etiqueta-tarjeta}

Una sesión de Claude Code no ve a las demás, y el mod de la SF solo conoce la suya. El 27 de octubre de 2026 hubo commits en tres proyectos a la vez entre las 00:08 y las 02:11, sin ninguna vista de conjunto.

[[M6]](#src-M6 "Historial git del 27 de octubre de 2026"){: .ref}

### Más agentes no es más productividad

Sobrecarga medida
{: .etiqueta-tarjeta}

En un estudio de BCG con casi 1.500 trabajadores, la productividad sube con los tres primeros agentes y cae con el cuarto. Quienes sufren ese agotamiento cometen más errores graves.

[[E2]](#src-E2 "Built In sobre el estudio de BCG, 2026"){: .ref}

### El trabajo se va de horario

Consecuencia
{: .etiqueta-tarjeta}

Según datos de Multitudes recogidos por LeadDev, los commits fuera de horario subieron un 19,6 % con la programación agéntica. Retomar una tarea interrumpida, además, cuesta: solo el 10 % de las sesiones estudiadas volvió a editar en menos de un minuto.

[[E3]](#src-E3 "LeadDev sobre Multitudes, 2026"){: .ref} [[E1]](#src-E1 "Parnin y Rugaber, 2010"){: .ref}

:::

## Producto | Qué es el Claude Code Commander | Producto {#producto}

El CCC es una aplicación de la SF que reúne todas las sesiones de Claude Code de una persona y las conduce desde el ordenador, la tableta o el móvil. No escribe en los proyectos: guarda órdenes, abre sesiones y mide. Los cambios los hace Claude dentro de cada sesión, y el mod de esa sesión hace de enlace.

Este reparto mantiene la regla de la SF «un proyecto por sesión», que vive en el mod y bloquea las escrituras en otro proyecto [[M4]](#src-M4 "Mod de estado de la SF"){: .ref}. También hace que las sesiones no dependan del CCC: si se cae, cada una sigue trabajando y solo se pierde el mando a distancia.

::: tarjetas 3

### Cinco capacidades

**5** funciones
{: .metrica}

Ver las sesiones, darles órdenes, abrir y cerrar sesiones, lanzar tareas de JKanban y medir.

### Tres dispositivos

**3** pantallas
{: .metrica}

Ordenador, tableta y móvil, también fuera de casa con un acceso seguro.

### Ninguna escritura

**0** cambios en proyectos
{: .metrica}

El CCC no toca archivos de ningún proyecto; los cambios pasan siempre por la sesión de ese proyecto.

:::

### Cómo se reparte el trabajo

El mod de cada sesión cuenta al CCC el estado de su sesión al arrancar, al acabar cada turno y al cerrarse. El CCC guarda las órdenes por sesión, y el mod de cada una recoge las suyas y las anota en su cola de peticiones. Las tareas de JKanban siguen el mismo camino, a través de su servidor MCP (protocolo de contexto de modelos) [[M5]](#src-M5 "JKanban 1.0.0"){: .ref}.

<figure class="vertical">
<svg viewBox="0 0 560 520" width="100%" role="img" style="font-family:var(--fuente-texto);display:block">
<title>El CCC, el mod de cada sesión y JKanban: lo que existe y lo previsto</title>
<rect x="110" y="14" width="340" height="70" rx="10" fill="none" style="stroke:var(--texto-suave)" stroke-width="2" stroke-dasharray="7 5"/>
<text x="280" y="44" text-anchor="middle" font-size="18" font-weight="700" style="fill:var(--texto-suave)">Claude Code Commander</text>
<text x="280" y="68" text-anchor="middle" font-size="15" style="fill:var(--texto-suave)">previsto · ordenador, tableta y móvil</text>
<line x1="280" y1="84" x2="280" y2="150" style="stroke:var(--texto-suave)" stroke-width="2" stroke-dasharray="6 5"/>
<text x="292" y="122" font-size="15" style="fill:var(--texto-suave)">estado ↑ · órdenes ↓</text>
<rect x="60" y="150" width="440" height="80" rx="10" fill="none" style="stroke:var(--primario)" stroke-width="2"/>
<text x="280" y="182" text-anchor="middle" font-size="18" font-weight="700" style="fill:var(--oscuro)">Mod de la SF, en cada sesión</text>
<text x="280" y="208" text-anchor="middle" font-size="15" style="fill:var(--texto-suave)">existe · fase, cola, marcador y un proyecto por sesión</text>
<line x1="280" y1="230" x2="280" y2="276" style="stroke:var(--primario)" stroke-width="2"/>
<rect x="60" y="276" width="440" height="80" rx="10" fill="none" style="stroke:var(--primario)" stroke-width="2"/>
<text x="280" y="308" text-anchor="middle" font-size="18" font-weight="700" style="fill:var(--oscuro)">Claude, en la sesión del proyecto</text>
<text x="280" y="334" text-anchor="middle" font-size="15" style="fill:var(--texto-suave)">existe · el único que cambia el proyecto</text>
<line x1="280" y1="356" x2="280" y2="402" style="stroke:var(--texto-suave)" stroke-width="2" stroke-dasharray="6 5"/>
<text x="292" y="386" font-size="15" style="fill:var(--texto-suave)">tareas por MCP, previsto</text>
<rect x="60" y="402" width="440" height="80" rx="10" fill="none" style="stroke:var(--primario)" stroke-width="2"/>
<text x="280" y="434" text-anchor="middle" font-size="18" font-weight="700" style="fill:var(--oscuro)">JKanban</text>
<text x="280" y="460" text-anchor="middle" font-size="15" style="fill:var(--texto-suave)">existe · versión 1.0.0 con servidor MCP</text>
</svg>
<figcaption>Trazo continuo, lo que existe; discontinuo, lo previsto. El CCC nunca llega al proyecto sin pasar por su sesión.</figcaption>
</figure>

### Qué hace cada función

La vista de sesiones muestra una tarjeta por sesión, con el color del proyecto, su fase, lo que tiene en curso, su cola y sus avisos; lo que pide atención va primero. Las órdenes se escriben en la tarjeta de una sesión y llegan a su cola como una petición más. Desde el CCC se abre una sesión en la carpeta de un proyecto con un primer prompt, y se cierra cuando ya no toca; al cerrarla, el mod cuenta como dejado a medias lo que seguía en curso.

Las tareas de JKanban se ven en la tarjeta de su proyecto y se lanzan sobre su sesión, con su contexto. La medida junta, por día y por proyecto, los commits, los prompts, las peticiones terminadas y dejadas a medias, el coste y el contexto de cada sesión. Con ella, el CCC avisa cuando se pasa un tope de frentes a la vez o una hora fijada.

### Qué no hace

No escribe código ni cambia archivos: eso es trabajo de cada sesión. No sustituye al mod, que sigue guardando las reglas dentro de cada sesión, ni a JKanban, que sigue siendo el tablero. No aprueba permisos por la persona: cada sesión mantiene su modo de permisos, y las decisiones importantes siguen siendo humanas.

### Cómo crece

Se construye por fases que se usan a diario antes de pasar a la siguiente: primero ver y medir, después las órdenes, después abrir sesiones y lanzar tareas, y por último el uso seguro fuera de casa. La tecnología de la ventana se decide antes de la primera fase, y se valoran una aplicación web servida por el propio CCC, una aplicación web instalable o las superficies que ya tiene Claude Code. El CCC vive dentro del plugin `sf` y se actualiza con la SF [[M2]](#src-M2 "Decisión «Claude Code Commander»"){: .ref}.

## Escenarios de uso | Cinco situaciones en las que el CCC aporta valor | S1–S5 {#escenarios}

El CCC aporta valor cuando hay más de una sesión abierta o cuando la persona no está delante de la terminal. Fuera de esas situaciones, el mod de cada sesión basta. Los cinco escenarios son compatibles: un mismo día puede pasar por todos.

La base de cada escenario es un hecho del propio proyecto o una fuente publicada. El valor que se describe es un objetivo de diseño, y lo que hay que medir es lo que lo confirmará o lo descartará.
{: .texto}

::: tarjetas 2

### S1 · Varias sesiones a la vez {: #S1}

Dos o más proyectos con sesión abierta al mismo tiempo.
{: .nota}

Cuándo aporta valor
:   Cuando hay que saber qué pasa en una sesión que no se está mirando: un aviso, una petición bloqueada o un trabajo terminado.

Límite del argumento
:   Con una o dos sesiones, la terminal y la vista de agentes de Claude Code pueden bastar.

Qué medir
:   Tiempo entre un aviso de una sesión y la respuesta de la persona; veces que se cambia de terminal para preguntar el estado.

Base documental
:   [[M6]](#src-M6 "Historial git del 27 de octubre de 2026"){: .ref} [[A1]](#src-A1 "Anthropic · vista de agentes"){: .ref}

### S2 · Lejos de la mesa {: #S2}

La persona está con la tableta o el móvil, sin terminal.
{: .nota}

Cuándo aporta valor
:   Cuando una sesión espera una decisión o una orden corta, y no hace falta volver al ordenador para darla.

Límite del argumento
:   El control remoto de Claude Code ya lleva una sesión al móvil con avisos; el CCC aporta la vista de todas a la vez.

Qué medir
:   Órdenes dadas desde la tableta o el móvil y tiempo de espera de las sesiones.

Base documental
:   [[A2]](#src-A2 "Anthropic · control remoto"){: .ref}

### S3 · Del kanban a la sesión {: #S3}

Una tarea de JKanban pasa a la sesión de su proyecto.
{: .nota}

Cuándo aporta valor
:   Cuando la tarea ya está preparada y basta con entregarla con su contexto, sin copiarla a mano a una terminal.

Límite del argumento
:   Depende del servidor MCP de JKanban y de que el proyecto tenga su tablero; hoy, SmartColdBox aún no lo tiene.

Qué medir
:   Tareas lanzadas desde el CCC y tareas que vuelven al tablero en su nueva columna sin intervención manual.

Base documental
:   [[M5]](#src-M5 "JKanban 1.0.0"){: .ref} [[T7]](#src-T7 "Vibe Kanban"){: .ref}

### S4 · Retomar un proyecto parado {: #S4}

Un proyecto sin sesión abierta espera una decisión.
{: .nota}

Cuándo aporta valor
:   Cuando abrir la sesión, situarla y darle el primer prompt cuesta más que la propia decisión.

Límite del argumento
:   Retomar exige también recordar el contexto; eso lo da el estado del proyecto en la SF, no el CCC.

Qué medir
:   Tiempo desde que se decide retomar hasta la primera petición en curso.

Base documental
:   [[E1]](#src-E1 "Parnin y Rugaber, 2010"){: .ref}

### S5 · Medir y frenar a tiempo {: #S5}

La persona supera un tope de frentes o trabaja a deshoras.
{: .nota}

Cuándo aporta valor
:   Cuando un aviso a tiempo evita abrir un cuarto frente o seguir a las dos de la madrugada.

Límite del argumento
:   Un aviso que se ignora no cambia nada, y demasiados avisos agobian; el tope lo fija la persona.

Qué medir
:   Frentes a la vez por hora, commits fuera de horario y peticiones dejadas a medias, antes y después.

Base documental
:   [[E2]](#src-E2 "Built In sobre el estudio de BCG, 2026"){: .ref} [[E3]](#src-E3 "LeadDev sobre Multitudes, 2026"){: .ref} [[E4]](#src-E4 "Gonzalez, 2026"){: .ref}

:::

## Alternativas | Qué existe hoy y qué aporta el CCC | Alternativas {#alternativas}

Las alternativas se agrupan en cuatro familias, y todas van por delante del CCC en algo: madurez, comunidad o soporte oficial. Lo de Anthropic sigue las versiones de Claude Code y llega al móvil; los gestores de sesiones llevan meses de uso real y decenas de miles de usuarios. La comparación se revisó el 27 de octubre de 2026.

Lo que ninguna reúne es la capa del método: sesiones vistas por fase y peticiones, un kanban propio como origen de tareas y la medida de cómo dirige la persona. Por eso el CCC se plantea como cliente de las piezas oficiales y como complemento de las demás, no como su sustituto. Dos de los productos revisados, Terragon y Crystal, ya están discontinuados, y la nube de Vibe Kanban cerró en abril de 2026: la sostenibilidad también es un argumento.

::: tarjetas 2

### Lo de Anthropic

Vista de agentes, control remoto y mensajes
{: .etiqueta-tarjeta}

Qué resuelve
:   Ver y lanzar sesiones en segundo plano, llevar una sesión al móvil con avisos y escribir de una sesión a otra.

Qué le falta para el CCC
:   No ve las sesiones interactivas hasta pasarlas a segundo plano ni el coste por sesión; no conoce fases ni kanban propio.

En qué va por delante
:   Es oficial, tiene permisos y seguridad resueltos, y llega al móvil con avisos.

[[A1]](#src-A1 "Anthropic · vista de agentes"){: .ref} [[A2]](#src-A2 "Anthropic · control remoto"){: .ref} [[A3]](#src-A3 "Anthropic · mensajes entre sesiones"){: .ref}

### Gestores de sesiones en paralelo

Claude Squad, CCManager, Conductor, opcode, Happy, Nimbalyst
{: .etiqueta-tarjeta}

Qué resuelve
:   Aíslan cada agente en su copia del repositorio, muestran su estado y ayudan a revisar y fusionar.

Qué le falta para el CCC
:   Ninguno conoce un método por fases ni la regla de un proyecto por sesión; casi todos son de escritorio.

En qué va por delante
:   Comunidad, soporte de varios agentes y años de uso; Happy y Nimbalyst ya llegan al móvil.

[[T1]](#src-T1 "Claude Squad"){: .ref} [[T2]](#src-T2 "CCManager"){: .ref} [[T3]](#src-T3 "Conductor"){: .ref} [[T4]](#src-T4 "opcode"){: .ref} [[T5]](#src-T5 "Happy"){: .ref} [[T6]](#src-T6 "Nimbalyst"){: .ref}

### Tableros kanban de agentes

Vibe Kanban
{: .etiqueta-tarjeta}

Qué resuelve
:   Cada tarjeta lanza un agente en su espacio, con revisión de cambios.

Qué le falta para el CCC
:   El tablero es el suyo, no uno externo por MCP como JKanban; no mide la dirección.

En qué va por delante
:   Probó el concepto con miles de usuarios; sigue como código abierto local.

[[T7]](#src-T7 "Vibe Kanban"){: .ref}

### Métricas de uso

Telemetría oficial y ccusage
{: .etiqueta-tarjeta}

Qué resuelve
:   Tokens, coste, commits, líneas y tiempo activo por sesión.

Qué le falta para el CCC
:   Miden el consumo, no los frentes abiertos ni las peticiones dejadas a medias.

En qué va por delante
:   La telemetría oficial es exhaustiva y estándar; el CCC debe consumirla, no repetirla.

[[A4]](#src-A4 "Anthropic · telemetría"){: .ref} [[T8]](#src-T8 "ccusage"){: .ref}

:::

## Evidencias | Qué respalda cada fuente y qué no | Evidencias {#evidencias}

Las evidencias se buscaron el 27 de octubre de 2026 en la documentación oficial de Claude Code, en los repositorios y páginas de los productos y en la prensa técnica. Respaldan dos cosas: que supervisar varios agentes tiene un coste humano medido, y que las piezas técnicas para construir el CCC ya existen. No respaldan todavía que una vista común reduzca ese coste: eso lo tiene que medir el piloto.

Dos de las cifras proceden de artículos que citan estudios, no de los estudios mismos. Se citan así y se marca en su lectura.
{: .texto}

::: tarjetas 2

### Retomar una tarea cuesta

Estudio · 10.000 sesiones de programación
{: .etiqueta-tarjeta}

Solo el 10 % de las sesiones estudiadas empezó a editar en menos de un minuto tras volver a una tarea; en el 30 %, la primera edición llegó después de media hora.

Escenarios
:   [S1](#S1){: .insignia} [S4](#S4){: .insignia}

Lectura para el proyecto
:   Respalda que cambiar de sesión y retomar tiene un coste. No mide sesiones con agentes de IA.

[[E1]](#src-E1 "Parnin y Rugaber, 2010"){: .ref}

### La productividad cae con el cuarto agente

Estudio de BCG, citado por Built In
{: .etiqueta-tarjeta}

Con casi 1.500 trabajadores, la productividad sube con los tres primeros agentes y cae con el cuarto; el agotamiento se asocia a más errores graves.

Escenarios
:   [S1](#S1){: .insignia} [S5](#S5){: .insignia}

Lectura para el proyecto
:   Respalda un tope de frentes. Es un artículo sobre el estudio, la fecha del estudio no es clara y no se limita a programadores.

[[E2]](#src-E2 "Built In sobre el estudio de BCG, 2026"){: .ref}

### Más commits fuera de horario

Datos de Multitudes, citados por LeadDev
{: .etiqueta-tarjeta}

Con la programación agéntica, los commits fuera de horario subieron un 19,6 %.

Escenarios
:   [S5](#S5){: .insignia}

Lectura para el proyecto
:   Respalda medir el horario y avisar. Es un dato de un proveedor de métricas, recogido en prensa.

[[E3]](#src-E3 "LeadDev sobre Multitudes, 2026"){: .ref}

### Supervisar agentes cansa

Ensayo · julio de 2026
{: .etiqueta-tarjeta}

Describe por qué trabajar con agentes de IA agota: atención dividida, revisión continua y decisiones constantes.

Escenarios
:   [S5](#S5){: .insignia}

Lectura para el proyecto
:   Respalda el problema desde la experiencia. Es una opinión razonada, no una medición.

[[E4]](#src-E4 "Gonzalez, 2026"){: .ref}

### La ironía de la automatización

Artículo clásico · 1983
{: .etiqueta-tarjeta}

Cuanto más automático es un sistema, más exigente es el papel de quien lo supervisa.

Escenarios
:   [S1](#S1){: .insignia} [S5](#S5){: .insignia}

Lectura para el proyecto
:   Respalda que el CCC ayude a supervisar, no que automatice más. Es de control industrial, no de software.

[[E5]](#src-E5 "Bainbridge, 1983"){: .ref}

### Las piezas técnicas existen

Documentación oficial y proyecto
{: .etiqueta-tarjeta}

Claude Code ofrece mensajes entre sesiones, control remoto y telemetría; el mod de la SF ya registra fase, cola y marcador; JKanban 1.0.0 trae servidor MCP.

Escenarios
:   [S1](#S1){: .insignia} [S2](#S2){: .insignia} [S3](#S3){: .insignia}

Lectura para el proyecto
:   Respalda que el CCC es construible sin inventar canales. El mod no se ha probado aún en sesiones reales, y la API de mods puede cambiar.

[[A3]](#src-A3 "Anthropic · mensajes entre sesiones"){: .ref} [[A5]](#src-A5 "Anthropic · API de mods"){: .ref} [[M4]](#src-M4 "Mod de estado de la SF"){: .ref} [[M5]](#src-M5 "JKanban 1.0.0"){: .ref}

:::

## Impacto | Qué cambia si el CCC funciona | Impacto {#impacto}

Si el CCC funciona, cambia cómo se reparte la atención, no cuánto código se escribe. La línea de base ya existe: el historial git de cada proyecto da los frentes por hora y los commits a deshora, y el mod cuenta las peticiones terminadas y dejadas a medias [[M6]](#src-M6 "Historial git del 27 de octubre de 2026"){: .ref}. Ningún cambio se atribuye al CCC sin comparar semanas con y sin él.

::: tarjetas 3

### Atención

Qué puede cambiar
:   Menos horas con más frentes abiertos que el tope fijado.

Indicador
:   Horas al día con tres o más proyectos con actividad.

### Horario

Qué puede cambiar
:   Menos trabajo a deshoras, por aviso y no por voluntad.

Indicador
:   Commits entre las 00:00 y las 07:00 por semana.

### Cierre

Qué puede cambiar
:   Menos peticiones dejadas a medias al cerrar el día.

Indicador
:   Proporción de «−» frente a «+» en el marcador del día.

:::

## Riesgos | Qué puede fallar y cómo se mitiga | Riesgos {#riesgos}

El riesgo principal es que Anthropic resuelva antes buena parte del CCC: su ritmo de lanzamientos es alto y ya cubre la vista de sesiones y el móvil. El plan lo detecta pronto porque cada fase se apoya en piezas oficiales y se revisa qué ha cambiado antes de empezar la siguiente. Lo que quede cubierto por Claude Code se deja de construir.

::: tarjetas 2

### Anthropic lo resuelve antes

Estratégico
{: .etiqueta-tarjeta}

Mitigación
:   Construir encima de las piezas oficiales y quedarse en la capa del método, que Claude Code no conoce.

Se comprueba en
:   La revisión de novedades al inicio de cada fase.

### La API de mods cambia

Técnico
{: .etiqueta-tarjeta}

Mitigación
:   Mantener en el mod solo el enlace, con poca lógica, y probarlo en cada versión de Claude Code.

Se comprueba en
:   [Fase 1](#fases), con las pruebas del mod en sesiones reales.

### Acceso inseguro desde fuera

Seguridad
{: .etiqueta-tarjeta}

Mitigación
:   Escuchar solo en el equipo por defecto, con una clave; abrirlo a la red solo a propósito y con un acceso cifrado.

Se comprueba en
:   [Fase 4](#fases) y la puerta de seguridad.

### Medir de más agobia

Humano
{: .etiqueta-tarjeta}

Mitigación
:   Pocos avisos, con topes que fija la persona, y una vista que se mira cuando se quiere.

Se comprueba en
:   [Fase 1](#fases), con dos semanas de uso propio.

### Proyecto abandonado

Sostenibilidad
{: .etiqueta-tarjeta}

Mitigación
:   Alcance pequeño, dentro del plugin `sf`, sin servidor en la nube que mantener.

Se comprueba en
:   Cada puerta de decisión.

:::

## Qué debe demostrar | Del documento al uso diario | Fases {#fases}

El CCC se demuestra usándolo a diario, por fases. Cada fase tiene una condición para avanzar, y una puerta de decisión separa las que cambian mucho el alcance. El primer usuario es el propietario de la SF; la medida compara semanas con y sin el CCC.

::: tarjetas 2

### Fase 1 · Ver y medir

Circuito
:   Todas las sesiones abiertas en una vista, con sus métricas del día.

Motivo
:   Es la base de todo lo demás y ya se apoya en lo que cuenta el mod.

Condición para avanzar
:   Dos semanas de uso diario y el mod probado en sesiones reales.

### Fase 2 · Órdenes

Circuito
:   Órdenes a una sesión que llegan a su cola de peticiones.

Motivo
:   Evita volver a la terminal para una orden corta.

Condición para avanzar
:   Ninguna orden rodea la regla de un proyecto por sesión.

### Fase 3 · Sesiones y tareas

Circuito
:   Abrir y cerrar sesiones con un primer prompt; lanzar tareas de JKanban.

Motivo
:   Une el tablero con el trabajo y reduce el coste de retomar.

Condición para avanzar
:   Una tarea va del tablero a la sesión y vuelve sin pasos a mano.

### Fase 4 · Fuera de casa

Circuito
:   El CCC en la tableta y el móvil, fuera de la red de casa.

Motivo
:   Es la ventana que flota del todo.

Condición para avanzar
:   Acceso cifrado y con clave, revisado antes de abrirlo.

:::

### Decisiones de avance

Antes de la fase 1 se decide la tecnología de la ventana, con las tres opciones del apartado «Cómo crece». Antes de la fase 3 se decide si el CCC abre las sesiones él mismo o a través de las piezas oficiales de Claude Code. Antes de la fase 4 se revisa la seguridad del acceso remoto.

Se valida en tres planos. El técnico, que el canal entre el mod y el CCC no pierde órdenes ni estado. El operativo, que la vista se usa y los avisos no se ignoran. El de la persona, que bajan los frentes a la vez y el trabajo a deshoras.

> [!decision]
> **Decisión propuesta**
> Construir la fase 1, ver y medir, sobre lo que ya registra el mod y las piezas oficiales de Claude Code, y decidir antes su tecnología. Se medirá con las horas de tres o más frentes y los commits de madrugada, dos semanas antes y dos después.

## Fuentes | Fuentes y referencias | Fuentes {#fuentes}

Fuentes revisadas el 27 de octubre de 2026. E = estudios y evidencias; A = documentación de Anthropic; T = productos comparables; M = documentos y datos del propio proyecto.
{: .nota}

::: fuentes

**E1 · Parnin y Rugaber, 2010** Resumption strategies for interrupted programming tasks.<br>[Abrir fuente ↗](https://sites.cc.gatech.edu/reverse/repository/resumptionstrategies.pdf)
{: #src-E1}

**E2 · Built In, 10 de junio de 2026** AI brain fry, sobre el estudio de BCG. La fecha del estudio no es clara: el artículo dice abril y la página de BCG, 5 de marzo.<br>[Abrir fuente ↗](https://builtin.com/articles/ai-brain-fry-software-developers)
{: #src-E2}

**E3 · LeadDev, 30 de marzo de 2026** Addictive agentic coding has developers losing sleep, con datos de Multitudes.<br>[Abrir fuente ↗](https://leaddev.com/ai/addictive-agentic-coding-has-developers-losing-sleep)
{: #src-E3}

**E4 · Constantin Gonzalez, 16 de julio de 2026** Why working with AI agents is so tiring.<br>[Abrir fuente ↗](https://constantin.glez.de/posts/2026-07-16-why-working-with-ai-agents-is-so-tiring-and-what-to-do-about-it/)
{: #src-E4}

**E5 · Bainbridge, 1983** Ironies of Automation.<br>[Abrir fuente ↗](https://gwern.net/doc/sociology/technology/1983-bainbridge.pdf)
{: #src-E5}

**A1 · Anthropic** Vista de agentes de Claude Code.<br>[Abrir fuente ↗](https://code.claude.com/docs/en/agent-view.md)
{: #src-A1}

**A2 · Anthropic** Control remoto de Claude Code.<br>[Abrir fuente ↗](https://code.claude.com/docs/en/remote-control.md)
{: #src-A2}

**A3 · Anthropic** Mensajes entre sesiones.<br>[Abrir fuente ↗](https://code.claude.com/docs/en/cross-session-messaging.md)
{: #src-A3}

**A4 · Anthropic** Telemetría y monitorización del uso.<br>[Abrir fuente ↗](https://code.claude.com/docs/en/monitoring-usage.md)
{: #src-A4}

**A5 · Anthropic** API de los mods de Claude Code.<br>[Abrir fuente ↗](https://code.claude.com/docs/en/plugins/mods/api.md)
{: #src-A5}

**T1 · Claude Squad** Varios agentes en la terminal, cada uno aislado.<br>[Abrir fuente ↗](https://github.com/smtg-ai/claude-squad)
{: #src-T1}

**T2 · CCManager** Estado de cada sesión y sus copias del repositorio.<br>[Abrir fuente ↗](https://github.com/kbwo/ccmanager)
{: #src-T2}

**T3 · Conductor** Agentes en paralelo para revisar y fusionar, en Mac.<br>[Abrir fuente ↗](https://www.conductor.build)
{: #src-T3}

**T4 · opcode** Interfaz gráfica de sesiones con coste y tokens.<br>[Abrir fuente ↗](https://github.com/winfunc/opcode)
{: #src-T4}

**T5 · Happy** Cliente cifrado para el móvil, la web y el escritorio.<br>[Abrir fuente ↗](https://github.com/slopus/happy)
{: #src-T5}

**T6 · Nimbalyst** Escritorio con app acompañante para el móvil y seguimiento de tareas.<br>[Abrir fuente ↗](https://github.com/Nimbalyst/nimbalyst)
{: #src-T6}

**T7 · Vibe Kanban** Un agente por tarjeta, en local. Su empresa cerró la nube el 10 de abril de 2026.<br>[Abrir fuente ↗](https://github.com/BloopAI/vibe-kanban) · [Anuncio del cierre ↗](https://vibekanban.com/blog/shutdown)
{: #src-T7}

**T8 · ccusage** Tokens y coste por día, sesión y bloque, a partir de los registros locales.<br>[Abrir fuente ↗](https://github.com/ryoppippi/ccusage)
{: #src-T8}

**M1 · Visión del Claude Code Commander** El mismo proyecto contado con una historia.<br>[Abrir documento](claude-code-commander.html)
{: #src-M1}

**M2 · Decisión «Claude Code Commander»** Alcance, dispositivos y lugar en el plugin, en `docs/decisiones/`.<br>[Abrir documento](../../decisiones/036-2026-10-27-claude-code-commander.md)
{: #src-M2}

**M3 · Propuesta «Claude Code Commander: lo que falta concretar»** Canal, arranque, métricas y orden, en `docs/propuestas.md`.<br>[Abrir documento](../../propuestas.md)
{: #src-M3}

**M4 · Mod de estado de la SF, versión 0.13** Fase, cola de peticiones, marcador y un proyecto por sesión, en `plugins/sf/hooks/register.tsx`. Sin probar aún en sesiones reales.<br>[Cómo funciona la SF](../../como-funciona-la-software-factory.html)
{: #src-M4}

**M5 · JKanban 1.0.0** Tablero de la SF, con servidor MCP en `jkanban_mcp/`, preparado el 27 de octubre de 2026.
{: #src-M5}

**M6 · Historial git del 27 de octubre de 2026** Commits por hora de SoftwareFactory (60), SmartColdBox (22) y JKanban (12) hasta las 15:03.
{: #src-M6}

:::

## Anexo A · Comparación | La vista de agentes de Claude Code y el CCC | Anexo A {#anexo-a}

La vista de agentes es la referencia más cercana: oficial, reúne sesiones de todos los proyectos y permite lanzarlas y responderles [[A1]](#src-A1 "Anthropic · vista de agentes"){: .ref}. La comparación separa lo publicado de lo que el CCC tiene como objetivo de diseño, dimensión por dimensión.

::: tarjetas 2

### Qué sesiones ve

::: columnas
Referencia · publicado
{: .etiqueta-tarjeta}

Las sesiones en segundo plano; las interactivas, solo después de pasarlas a segundo plano.
|||
CCC · diseño
{: .etiqueta-tarjeta}

Todas las sesiones con el mod de la SF, interactivas o no.
:::

### Dónde se usa

::: columnas
Referencia · publicado
{: .etiqueta-tarjeta}

En la terminal; el móvil llega por el control remoto, sesión a sesión.
|||
CCC · diseño
{: .etiqueta-tarjeta}

Ordenador, tableta y móvil, con todas las sesiones a la vez.
:::

### Qué muestra de cada sesión

::: columnas
Referencia · publicado
{: .etiqueta-tarjeta}

Estado, resumen de una línea, antigüedad, proyecto y solicitud de cambios.
|||
CCC · diseño
{: .etiqueta-tarjeta}

Fase del método, peticiones en curso y en cola, avisos y marcador.
:::

### Órdenes y tareas

::: columnas
Referencia · publicado
{: .etiqueta-tarjeta}

Lanzar, responder, entrar, parar y borrar sesiones.
|||
CCC · diseño
{: .etiqueta-tarjeta}

Órdenes a la cola de cada sesión y tareas lanzadas desde JKanban.
:::

### Métricas

::: columnas
Referencia · publicado
{: .etiqueta-tarjeta}

No muestra el coste por sesión; la telemetría oficial va aparte.
|||
CCC · diseño
{: .etiqueta-tarjeta}

Frentes a la vez, horario, peticiones terminadas y dejadas, coste y contexto.
:::

### Reglas del método

::: columnas
Referencia · publicado
{: .etiqueta-tarjeta}

No conoce fases ni reglas de proyecto.
|||
CCC · diseño
{: .etiqueta-tarjeta}

Respeta un proyecto por sesión, que guarda el mod.
:::

:::

La comparación debe conservar lo que la vista de agentes hace bien: es oficial, sigue cada versión de Claude Code y no exige instalar nada. El valor añadido del CCC se comprueba en la fase 1: si con él bajan las horas con tres o más frentes y los commits de madrugada, aporta; si no, basta con la vista de agentes y el mod.
