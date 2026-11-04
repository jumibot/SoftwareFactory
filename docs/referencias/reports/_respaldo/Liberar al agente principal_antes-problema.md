---
antetitulo: Software Factory · Informe de análisis · Noviembre 2026
lema: Menos idas y vueltas del principal; // órdenes antes que agentes.
subtitulo: Dónde se le va el tiempo al agente principal al abrir, lanzar y recoger una tarea, qué permite Claude Code a los agentes de un plugin, qué ganaría cada opción (órdenes compuestas, agentes por familia, agente de la cola siempre vivo, orquestador delegado) y qué hay que decidir.
version: Versión 1.0 · 04/11/2026
estado: Propuesta · Tarea 358
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
menu: secciones
tipo: Informe de análisis
pie: Informe de la tarea «Liberar antes al agente principal: deliberar qué delegar en agentes del plugin y qué en órdenes de cola.py» (358). Parte de sf:orquestacion, sf:flujo_tareas, cola.py y los avisos del mod en develop (sf 1.8.0), del historial de la cola, de las cinco últimas sesiones del principal en la SF y de la documentación oficial de Claude Code. Decide el propietario de la Software Factory.
---
# Liberar al agente principal

## Resumen | Órdenes compuestas primero, agentes por familia después | Resumen {#resumen}

Se propone liberar al principal con dos piezas, en este orden. Primero, dos órdenes compuestas en `cola.py`: `abrir N`, que hace de una vez lo que hoy son seis o siete llamadas, y `recoger N`, que hace las cuatro o cinco de la recogida. Después, tres agentes del plugin, uno por familia de tarea (código, deliberativas y documentales), con el encargo fijo dentro, para que el principal solo pase lo propio de la tarea.

El tiempo del principal no se va en `cola.py`, que tarda 1,4 s, sino en las idas y vueltas del modelo: cada llamada le cuesta unos 5 s de pensar y escribir, y la mitad de sus llamadas son de la cola. Un agente de la cola, aunque viva toda la sesión, no quita esas idas y vueltas: añade otra, la suya. Por eso la recomendación inicial se mantiene, también con el agente siempre vivo. Un orquestador delegado tampoco sirve: un subagente no puede preguntar al propietario.

Quedan seis preguntas, todas abiertas; salen dos tareas nuevas, la de «Agentes especializados, uno por familia de tarea» (304) pasa a ser la que los implementa, y la de la incorporación (353) se mantiene, detrás de ella.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 590" width="100%" role="img" aria-label="Abrir una tarea de código: hoy siete llamadas (en-curso, choques, rama sin activar, worktree, subagente, encargo y lanzar con encargo largo); propuesto, cola.py abrir N y lanzar el agente de su familia. Recoger: hoy revisar el diff, merge ff-only, informe, marcar pasos y listo; propuesto, revisar el diff y cola.py recoger N." style="font-family:var(--fuente-texto);display:block">
<text x="10" y="24" font-size="18" font-weight="700" style="fill:var(--oscuro)">Hoy</text>
<text x="300" y="24" font-size="18" font-weight="700" style="fill:var(--texto-suave)">Propuesto</text>
<text x="10" y="62" font-size="15" font-weight="700" style="fill:var(--texto-suave)">Abrir una tarea de código</text>
<g font-size="15" style="fill:var(--texto)">
<rect x="10" y="75" width="250" height="30" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="22" y="95">en-curso N</text>
<rect x="10" y="113" width="250" height="30" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="22" y="133">choques N</text>
<rect x="10" y="151" width="250" height="30" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="22" y="171">rama N … --sin-activar</text>
<rect x="10" y="189" width="250" height="30" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="22" y="209">git worktree add -b sub-N</text>
<rect x="10" y="227" width="250" height="30" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="22" y="247">subagente N --worktree …</text>
<rect x="10" y="265" width="250" height="30" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="22" y="285">encargo N</text>
<rect x="10" y="303" width="250" height="30" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="22" y="323">lanzar, con encargo largo</text>
<rect x="300" y="75" width="250" height="220" rx="6" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5" stroke-dasharray="6 4"/><text x="425" y="180" text-anchor="middle" font-weight="700">cola.py abrir N</text><text x="425" y="202" text-anchor="middle" style="fill:var(--texto-suave)">una llamada, sin modelo</text>
<rect x="300" y="303" width="250" height="30" rx="6" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5" stroke-dasharray="6 4"/><text x="312" y="323">lanzar sf:codigo, encargo corto</text>
</g>
<text x="10" y="372" font-size="15" font-weight="700" style="fill:var(--texto-suave)">Recoger su trabajo</text>
<g font-size="15" style="fill:var(--texto)">
<rect x="10" y="385" width="250" height="30" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="22" y="405">revisar el diff</text>
<rect x="10" y="423" width="250" height="30" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="22" y="443">git merge --ff-only sub-N</text>
<rect x="10" y="461" width="250" height="30" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="22" y="481">informe N --terminado</text>
<rect x="10" y="499" width="250" height="30" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="22" y="519">paso marcar N P hecho …</text>
<rect x="10" y="537" width="250" height="30" rx="6" fill="none" style="stroke:var(--primario)" stroke-width="1.5"/><text x="22" y="557">listo N --prueba …</text>
<rect x="300" y="385" width="250" height="30" rx="6" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5" stroke-dasharray="6 4"/><text x="312" y="405">revisar el diff</text>
<rect x="300" y="423" width="250" height="144" rx="6" fill="none" style="stroke:var(--texto-suave)" stroke-width="1.5" stroke-dasharray="6 4"/><text x="425" y="490" text-anchor="middle" font-weight="700">cola.py recoger N</text><text x="425" y="512" text-anchor="middle" style="fill:var(--texto-suave)">la línea la deja el subagente</text>
</g>
</svg>
<figcaption>Lo que hace hoy el principal al abrir y al recoger una tarea de código, y lo que quedaría con las dos órdenes compuestas y el agente de su familia.</figcaption>
</figure>

[Ver las seis preguntas](#por-decidir){: .salto} [Ver las tareas que salen](#tareas){: .salto}

## Medición | Dónde se le va el tiempo al principal | Medición {#medicion}

La mitad de lo que hace el principal es llevar la cola, y cada llamada cuesta más por el modelo que por la orden. Se midieron las cinco últimas sesiones largas del principal en la SF (sus transcripciones, sin las de los subagentes) y el historial de las 129 tareas que ya salieron de la cola.

::: columnas

**51 %**  de sus llamadas
{: .metrica}

Son órdenes de `cola.py`: 1.126 de 2.209. Otro 24 % son órdenes de git (535), casi todas de worktrees, merges y diffs de subagentes.

|||

**≈ 5 s**  por llamada
{: .metrica}

`cola.py` tarda 1,4 s de mediana; el modelo, entre el resultado de una llamada y la siguiente, 3,7 s de mediana y 4,7 de media, sin contar lo que escribe.

|||

**84 %**  del encargo, fijo
{: .metrica}

Un encargo mide 2.243 caracteres de mediana (134 lanzamientos); la parte que da `cola.py encargo`, 1.883. El principal la vuelve a escribir entera cada vez.

:::

### Qué cuesta cada momento

El historial confirma que el principal ya encadena las órdenes de la cola en una sola llamada cuando puede: entre poner en curso y anotar el subagente pasan 4,5 s de mediana, y entre el informe y `listo`, 1 s. Lo caro no es esperar a `cola.py`, sino componer cada vez la cadena correcta, leer su salida y, cuando falla, repetirla.

| Momento | Órdenes hoy | Llamadas del principal | Con la propuesta |
| --- | --- | --- | --- |
| Abrir una de código | `en-curso`, `choques`, `rama --sin-activar`, `git worktree add -b sub-N`, `subagente`, `encargo`, lanzar | 4 a 7, más un encargo de ≈ 600 tokens | `abrir N` y lanzar con un encargo corto: 2 |
| Abrir una deliberativa | `en-curso`, `encargo`, lanzar | 2 o 3 | `abrir N` y lanzar: 2 |
| Recoger | revisar el diff, `merge --ff-only`, `informe`, `paso marcar` por paso, `listo` | 3 a 6 | revisar el diff y `recoger N …`: 2 |
| Cerrar | `cerrar` (ya recoge worktree y rama auxiliar) | 1 | igual |
| Encargos sobre la tarea | `SendMessage` al subagente vivo | 1 | igual |

Los fallos de sintaxis existen pero no son el grueso: 30 órdenes de `cola.py` fallidas en esas sesiones (un 2,7 %), cada una con su vuelta extra. En total, abrir y recoger una tarea de código le cuestan al principal entre medio minuto y un minuto de idas y vueltas, más los ≈ 600 tokens del encargo; con veinte tareas en una sesión, son de diez a veinte minutos en los que no atiende al propietario.

> **Lo que no se midió**
> El coste en tokens por orden no sale de las transcripciones separado por llamada; las cifras de tiempo son medianas de las cinco sesiones y sirven para comparar opciones, no como presupuesto.

## Agentes | Qué permite Claude Code a los agentes de un plugin | Agentes {#agentes}

Un plugin puede traer agentes (`agents/*.md`) con su propio prompt, sus skills precargadas, su modelo y sus herramientas. Lo que no puede ningún subagente es preguntar al propietario, y no hay un agente «siempre vivo» como pieza de Claude Code: un subagente parado se reanuda con `SendMessage`, pero no espera ni escucha por sí mismo.

::: tarjetas 2 plegables

### Definición {icono=documento}

`agents/<nombre>.md` en el plugin; se lanza como `sf:<nombre>`. El cuerpo es su prompt de sistema (sin el de Claude Code) y recibe el `CLAUDE.md` salvo con `omitClaudeMd`. En el frontmatter: `description`, `tools`, `disallowedTools`, `model`, `effort`, `skills`, `memory`, `background`, `isolation`, `maxTurns`, `autoCompactWindow` y `color`.

### Lo que un plugin no puede {icono=aviso}

Por seguridad, en los agentes de un plugin se ignoran `hooks`, `mcpServers` y `permissionMode`. Los hooks de la SF siguen siendo los del mod, que ya distinguen a un subagente por su `agentId`.

### Skills y encargo fijo {icono=check}

`skills:` inyecta el contenido entero de hasta 32 skills al arrancar. El agente de las deliberativas puede llevar ya `informe_deliberativa` y `crear_documentos`, que hoy carga cada subagente con dos llamadas.

### Preguntar y anidar {icono=dialogo}

`AskUserQuestion` se quita a todo subagente: no puede preguntar al propietario. Sí puede lanzar otros agentes, hasta tres niveles por debajo del principal.

### Vivir y recibir mensajes {icono=rama}

Un subagente terminado o parado conserva su historia y se reanuda con `SendMessage`; trabaja en segundo plano mientras el principal sigue. Se compacta en su propia ventana. No está documentado qué le pasa con `/clear` ni al cerrar la sesión, ni que reciba mensajes mientras trabaja fuera de los equipos de agentes.

### Equipos y agente principal {icono=lupa}

Los equipos de agentes (compañeros que siguen vivos y se escriben) son experimentales, van apagados por defecto y no se recuperan al reanudar la sesión. El ajuste `agent`, que un plugin puede fijar en su `settings.json`, hace que el principal arranque como uno de sus agentes, con su prompt.

:::

Dos datos más pesan en la comparación. La caché de un subagente es suya, no la del principal, y dura 5 minutos por defecto: un agente que se despierta de tarde en tarde paga su contexto entero cada vez. Y `isolation: worktree` crea un worktree desde la rama por defecto con un nombre de rama no documentado, así que no sirve para la `sub-N` que sale de la rama de la tarea: el worktree lo sigue haciendo `cola.py`.

## Opciones | Qué ganaría cada una | Opciones {#opciones}

Las órdenes compuestas quitan idas y vueltas sin poner ningún modelo en medio; los agentes por familia quitan el texto repetido del encargo. Las otras dos opciones mueven el trabajo de sitio sin quitarlo, y añaden un salto.

::: tarjetas 2 plegables

### Órdenes compuestas en cola.py {icono=codigo} {: #o-compuestas}

`abrir N` (en curso, choques, rama sin activar, worktree y rama `sub-N`, anotar el subagente y dar el encargo; en una deliberativa, solo en curso y encargo) y `recoger N --pasos 2,3 --listo "qué mirar"` (traer `sub-N` con `--ff-only`, anotar el informe, marcar pasos y dejar lista).

Gana
:   De 4-7 llamadas a 1 al abrir y de 3-6 a 1 al recoger; sin errores de sintaxis en cadenas largas; lo mismo sirve al panel.

Cuesta
:   Una tarea de código mediana, con pruebas; las reglas que hoy dice la orquestación pasan al CLI. Abrir sigue pidiendo `choques` antes y parando si los hay.

### Agentes del plugin por familia {icono=rama} {: #o-familias}

`sf:codigo`, `sf:deliberativa` y `sf:documental`, con las reglas fijas del encargo en su cuerpo, sus skills precargadas y, como primer paso, leer `cola.py encargo N` para lo variable (worktree, coautoría, convenciones, Python).

Gana
:   El encargo del principal baja de ≈ 2.200 a ≈ 400 caracteres; las reglas viven en un sitio y se versionan con el plugin; cada familia, su forma de trabajar (decisión «Siete tipos de tarea en tres familias», 223).

Cuesta
:   Una tarea mediana. Las reglas no pueden repetirse en tres sitios: el encargo fijo queda en el cuerpo de cada agente y `cola.py encargo` da solo lo variable.

### Agente de la cola, siempre vivo {icono=dialogo} {: #o-cola}

Un subagente lanzado al empezar la sesión que recibe por `SendMessage` cada operación de la cola y la ejecuta.

Gana
:   Sin coste de arrancar ni de explicarle el contexto en cada operación; puede trabajar en segundo plano mientras el principal habla.

Cuesta
:   Cada operación sigue pidiendo una llamada del principal, más uno o dos turnos del agente y la notificación de vuelta: de 2 a 3 veces más lento que llamar a `cola.py`. Su contexto crece con cada salida y se compacta; tras 5 minutos sin uso, paga su caché entera. Si muere, hay que relanzarlo y avisarlo, como hoy los de las tareas. Y rompe «solo el principal escribe la cola» (decisión «El mod impide que un subagente escriba la cola», 110).

### Orquestador delegado {icono=lupa} {: #o-orquestador}

Un subagente que lleva la cola, lanza los de las tareas y los recoge; el principal solo conversa.

Gana
:   El principal tendría el contexto limpio para el propietario.

Cuesta
:   No puede preguntar al propietario: todo lo que decide pasa dos veces, del orquestador al principal y del principal al propietario. Los subagentes de tarea serían nietos y sus avisos del mod no llegan igual. Es el salto más caro de todos.

:::

### El agente de la cola, aunque viva toda la sesión

Que el agente esté vivo todo el rato quita su arranque y la explicación del contexto, que era la objeción más fácil. No quita la objeción de fondo: entre el principal y `cola.py` sigue habiendo un modelo más.

| | `cola.py abrir N` | Agente de la cola vivo |
| --- | --- | --- |
| Llamadas del principal | 1 | 1 (`SendMessage`) y leer la notificación |
| Turnos de modelo en medio | 0 | 1 o 2 del agente |
| Tiempo por operación | ≈ 1,4 s de orden | ≈ 10-15 s y vuelve en otro turno |
| Contexto que acumula | ninguno | crece con cada salida; compactación y caché de 5 min |
| Si muere | nada que relanzar | relanzarlo; `/clear` y cierre no documentados |
| Trabajar mientras el principal habla | sí, si se lanza en segundo plano | sí |
| Reglas de la cola | igual que hoy | cambia quién escribe la cola |

Su única ventaja propia, trabajar en segundo plano, no compensa: casi toda operación de la cola da algo que el principal necesita al momento (el número nuevo, un choque, un rechazo), y una orden de 1,4 s no merece ir aparte. La recomendación inicial del principal se mantiene.

### El principal como agente del plugin

Hay una variante que no delega nada: fijar en el `settings.json` del plugin el ajuste `agent`, para que el principal arranque como un agente `sf:orquestador` con la orquestación en su prompt. Ahorraría que el mod la entregue al empezar, tras `/clear` y tras compactar. Pero sustituye el prompt de sistema de Claude Code, se impondría en todos los proyectos que instalen la SF y no está documentado del todo: si se quiere, es una investigación aparte, no parte de esta propuesta.

## Por decidir | Las preguntas para el propietario | Por decidir {#por-decidir}

Seis preguntas, por importancia. Las dos primeras dan las tareas que salen; las otras fijan sus límites.

::: preguntas 2 plegables

### 1 · Órdenes compuestas para abrir y recoger {recomendada=A icono=codigo} {: #p1}

Hoy abrir una tarea de código son 4-7 llamadas del principal y recogerla, 3-6.

Opción A
:   `cola.py abrir N` y `cola.py recoger N --pasos … --listo "…"`, en una tarea de implementar.

Opción B
:   Solo `abrir N`; la recogida sigue a mano, porque revisar el diff es criterio.

Opción C
:   Como hoy.

Recomendación
:   **A.** Es lo que más tiempo libera y no pone ningún modelo en medio («Comandos antes que inferencia»). Revisar el diff sigue antes de `recoger`.

### 2 · Agentes del plugin por familia de tarea {recomendada=A icono=rama} {: #p2}

El encargo fijo es el 84 % de lo que el principal escribe al lanzar.

Opción A
:   Tres agentes (`sf:codigo`, `sf:deliberativa`, `sf:documental`) con las reglas fijas en su cuerpo y sus skills precargadas; leen `cola.py encargo N` para lo variable.

Opción B
:   Un solo agente `sf:tarea` que se adapta por el tipo que le da `cola.py encargo`.

Opción C
:   Como hoy: `cola.py encargo N` y un subagente general.

Recomendación
:   **A.** Es lo decidido en «Siete tipos de tarea en tres familias» (223) y permite skills y modelo propios de cada familia.

### 3 · La línea de recogida, del subagente {recomendada=A icono=check} {: #p3}

Para recoger, el principal tiene que deducir qué pasos marcar y qué probar.

Opción A
:   El informe del subagente acaba con la orden lista, `cola.py recoger N --pasos 2,3 --listo "…"`, que el principal revisa y lanza.

Opción B
:   El principal la compone, como hoy.

Recomendación
:   **A.** El subagente sabe qué hizo; el principal solo comprueba el diff y la línea.

### 4 · Un agente de la cola siempre vivo {recomendada=A icono=dialogo} {: #p4}

Lanzado al empezar la sesión y vivo hasta el final, recibiría cada operación por mensaje.

Opción A
:   No: las órdenes compuestas dan lo mismo sin un modelo en medio.

Opción B
:   Sí, como prueba en una tarea aparte, con la regla de quién escribe la cola cambiada.

Recomendación
:   **A.** Cada operación sería de 2 a 3 veces más lenta y su contexto crecería sin aportar nada que el CLI no dé.

### 5 · Un orquestador fuera del principal {recomendada=A icono=lupa} {: #p5}

El principal sigue hablando con el propietario en cualquier caso.

Opción A
:   No: el principal orquesta, como hoy, con menos órdenes.

Opción B
:   Investigar en una tarea aparte el principal como agente del plugin (ajuste `agent`), sin delegar.

Opción C
:   Un orquestador subagente vivo que lleva la cola y los subagentes.

Recomendación
:   **A.** Un subagente no puede preguntar al propietario; la B no libera tiempo, solo cambia cómo llegan las reglas.

### 6 · Qué hacer con las tareas 304 y 353 {recomendada=A icono=documento} {: #p6}

«Agentes especializados, uno por familia de tarea» (304) y «Valorar un agente del plugin para la incorporación de proyectos a la SF» (353) están en cola, las dos de deliberar.

Opción A
:   La 304 pasa a implementar los agentes por familia con lo que fije la pregunta 2; la 353 se mantiene, detrás de la 304, para reutilizar su forma.

Opción B
:   Fusionar la 353 en la 304.

Opción C
:   Absorber las dos en esta tarea.

Recomendación
:   **A.** La 304 ya tiene su deliberación aquí; la 353 es otro alcance (sin tarea y con menús al propietario, que un agente no puede hacer).

:::

## Tareas | Las tareas que salen | Tareas {#tareas}

Si se aceptan las recomendaciones, salen estas tareas. Van en este orden: los agentes leen el encargo que da la primera.

| Tarea | Tipo | Qué hace |
| --- | --- | --- |
| Abrir y recoger una tarea con una sola orden | implementar | `cola.py abrir N` y `recoger N --pasos --listo` ([pregunta 1](#p1)); el encargo pide al subagente la línea de recogida ([pregunta 3](#p3)); pone al día `sf:flujo_tareas`, `estados.md`, `sf:orquestacion` y el aviso del mod que dice cómo recoger. |
| Agentes especializados, uno por familia de tarea (304) | implementar | Pasa de deliberar a implementar: `agents/codigo.md`, `deliberativa.md` y `documental.md`; `cola.py encargo` da solo lo variable; la orquestación lanza el de la familia ([pregunta 2](#p2)). |
| Valorar un agente del plugin para la incorporación de proyectos a la SF (353) | deliberar | Sigue, detrás de la 304 ([pregunta 6](#p6)). |
| Actualizar Cómo funciona la Software Factory | documentar | Paso «Reflejar «Liberar al agente principal» (358)»: la pieza `agents/` y las dos órdenes. |
| Actualizar la metodología, la plantilla y el CLAUDE.md | documentar | El mismo paso, con el texto del anexo. |

## Anexo | Texto propuesto para los documentos compartidos | Anexo {#anexo}

Para las tareas «Actualizar…», una vez hechas las dos de implementar.

#### Cómo funciona la Software Factory (piezas del plugin)

> **Agentes del plugin**
> `agents/` trae un agente por familia de tarea: `sf:codigo`, `sf:deliberativa` y `sf:documental`. Cada uno lleva en su prompt las reglas fijas del encargo y sus skills precargadas, y lee lo variable con `cola.py encargo N`. El principal los lanza al poner la tarea en curso, con `cola.py abrir N`, y los recoge con `cola.py recoger N`.

#### CLAUDE.md de la SF (regla «Orquestación con subagentes»)

> Orquestación con subagentes: el principal habla con el propietario y lleva la cola; toda tarea en curso tiene su subagente, el agente del plugin de su familia, que hace todo su trabajo. Abrir y recoger una tarea son una orden de `cola.py` cada uno (`abrir N`, `recoger N`). Las reglas, en `sf:orquestacion`.

#### Metodología («Ramas y subagentes»)

> Cada tarea en curso se trabaja con el agente del plugin de su familia (código, deliberativas o documentales). `cola.py abrir N` la pone en curso con su rama, su worktree y su rama auxiliar, y da el encargo; `cola.py recoger N` trae el trabajo, anota el informe y marca los pasos.

::: fuentes

**Sub-agents.** Claude Code Docs, consultado el 04/11/2026. code.claude.com/docs/en/sub-agents
{: #src-E1}

**Plugin components y manifest reference.** Claude Code Docs, consultado el 04/11/2026. code.claude.com/docs/en/plugins/components
{: #src-E2}

**Agent teams.** Claude Code Docs, consultado el 04/11/2026. code.claude.com/docs/en/agent-teams
{: #src-E3}

**Prompt caching y worktrees.** Claude Code Docs, consultado el 04/11/2026. code.claude.com/docs/en/prompt-caching, code.claude.com/docs/en/worktrees
{: #src-E4}

:::
