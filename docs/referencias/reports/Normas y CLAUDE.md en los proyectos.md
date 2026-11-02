---
antetitulo: Software Factory · Informe de análisis · Octubre 2026
lema: Las normas, en las skills; // las reglas, sin tocar el CLAUDE.md.
subtitulo: Cómo se cargan las reglas y la orquestación en los proyectos con el menor cambio en su CLAUDE.md, dónde van las normas que aún están en la memoria y cómo pasa una norma nueva a su skill.
version: Versión 1.2 · 01/11/2026
estado: Propuesta · Tarea 211
portada: oscura
destino: proyecto
herramientas: buscador lectura cabecera tablas
tipo: Informe de análisis
pie: Propuesta de la tarea 211. Lo comprobado sale de los tipos del motor de mods de Claude Code 2.1.316, del código del mod sf y de la documentación oficial de hooks; lo demás se marca como supuesto. Espera la decisión del propietario.
---
# Normas y CLAUDE.md en los proyectos

## Resumen | El mod entrega las reglas; las normas viven en sus skills | Resumen {#resumen}

Decidido ya: las normas del propietario llegan a los proyectos por el plugin, en la skill donde se aplican («Las normas llegan por el plugin, en sus skills», 156). Queda cómo se cargan en cada proyecto, dónde va cada norma que todavía está en la memoria y cómo pasa a su skill una norma nueva.

La propuesta es que **el mod entregue las reglas y la orquestación** al empezar la sesión y tras compactar, solo en los proyectos con `.sf/proyecto.json`. Así el `CLAUDE.md` de un proyecto nuevo no lleva ninguna línea de la SF, no hay copia que regenerar y cargar `sf:orquestacion` deja de depender de que Claude se acuerde.

## Desde la versión 1.1 | Lo que ya se ha decidido o hecho | Desde la 1.1 {#desde}

- **«Lo que pinta la SF y lo global no son del proyecto» (167).** El mod ya añade esa regla al prompt de sistema con `prompt.compose`, solo en proyectos con SF y no en la propia SF. La forma D ya funciona para una regla corta.
- **El mod ya escucha `classic.SessionStart`.** Lo usa para que el panel note un `/clear`. Falta devolver `additionalContext`.
- **Automatizaciones configurables (171).** Toda regla que pase al mod lleva un interruptor en `.sf/proyecto.json`, con un valor por defecto prudente, y avisa antes que bloquear.
- **La tarea 248** (el mod carga `sf:orquestacion` al empezar, tras `/clear` y tras compactar) espera esta decisión.
- **«El principal solo orquesta»** ya está en `sf:orquestacion` (215) y ha salido de la memoria.
- **Nueva en la memoria:** «Un fallo propio también es bug».

## Lo comprobado | Qué puede hacer el mod al empezar y tras compactar | Comprobado {#comprobado}

El mod de la SF es un módulo de hooks de función (`hooks/hooks.json` = `{ "modules": ["./register.tsx"] }`). Hoy usa `session.start` para registrar comandos y arrancar el panel, pero ese evento **no deja inyectar contexto**: su resultado es solo `{ cwd }`.

Los tipos del motor (`claude-code.d.ts` de la versión 2.1.316) muestran tres vías que sí lo dejan. Las tres están en los tipos; ninguna se ha probado todavía en una sesión.

| Vía | Qué hace | Cuándo |
| --- | --- | --- |
| `classic.SessionStart` | Devuelve `additionalContext`: texto que el modelo recibe con el evento. Es el hook SessionStart de la configuración clásica, accesible desde el módulo. | `source`: `startup`, `resume`, `clear`, `compact` o `fork`. |
| `prompt.context` | Añade, cambia o quita bloques del contexto de la primera petición, incluidos los archivos de instrucciones del `CLAUDE.md` (`instructionFiles`). | Una vez por conversación; se vuelve a leer tras compactar y tras `/clear`. |
| `prompt.compose` | Añade una sección al prompt de sistema (`scope: 'session'`). | En cada petición: no lo borra compactar. |

**Los hooks clásicos fuera del módulo.** La documentación oficial dice que un plugin declara hooks clásicos en `hooks/hooks.json` con la forma `{ "hooks": { "SessionStart": [...] } }`, de tipo `command` o `mcp_tool`, y que SessionStart añade como contexto su `additionalContext` o su salida de texto. No está comprobado que ese archivo acepte a la vez `hooks` y `modules`; tampoco hace falta, porque el módulo llega al mismo evento como `classic.SessionStart`.

**El mod ya sabe qué proyecto es.** `leerEstado` distingue `proyecto` (con `.sf/proyecto.json`), `sf` (el repositorio de la SF) y `sin-sf`, y compara la versión con la que se incorporó el proyecto con la del plugin instalado.

**Lo supuesto.** Según la documentación, SessionStart no salta en los subagentes, que tienen su propio `SubagentStart` (también con `additionalContext`); no se ha visto en la práctica. Tampoco se sabe si `prompt.context` y `prompt.compose` alcanzan a las conversaciones de los subagentes. Y la API de mods está en acceso anticipado: cambia entre versiones de Claude Code.

## Hoy | Una copia por proyecto que se queda atrás | Hoy {#hoy}

`sf:incorporar_proyecto_a_sf` copia `templates/claude-sf.md` a `.sf/claude-sf.md`, con la versión del plugin, y añade al `CLAUDE.md` la línea `@.sf/claude-sf.md`. Al cambiar la SF, hay que volver a pasar la skill en cada proyecto para regenerar la copia.

**La copia ya se ha quedado atrás.** Sprites y sprite_animation tienen la de la 1.1.0 con el plugin en la 1.2.0. JKanban y SmartColdBox, anteriores a la plantilla, tienen un apartado «Software Factory» escrito a mano en su `CLAUDE.md`.

## Cómo se cargan | Cuatro formas de entregar las reglas | Cargar {#cargar}

**A. Como hoy: la línea `@.sf/claude-sf.md`.** Pros: probado; funciona sin el mod. Contras: una línea en el `CLAUDE.md`, una copia por proyecto que hay que regenerar, y la carga de `sf:orquestacion` depende de que Claude cumpla la regla.

**B. `classic.SessionStart` en el mod.** Al empezar, tras `/clear` y tras compactar, en proyectos con `.sf/proyecto.json`, el mod entrega las reglas y el texto de `sf:orquestacion`, leídos del plugin instalado. Pros: cero líneas, nada que regenerar, siempre la versión instalada; cargar la orquestación al empezar y tras compactar lo hace el mod, no Claude. Contras: depende del mod (sin el plugin no hay reglas, pero tampoco skills); unos 2.500 tokens por arranque y por compactación.

**C. `prompt.context` en el mod.** Añade las reglas como un archivo de instrucciones más del `CLAUDE.md`, sin estar escrito en él. Pros: el modelo las recibe igual que hoy y se reenvían tras compactar. Contras: no cubre la orquestación, que hoy se carga como skill; está menos documentado que SessionStart.

**D. `prompt.compose` en el mod.** Las reglas, en el prompt de sistema. Pros: presentes en cada petición. Contras: si alcanza a los subagentes, les llegaría la orquestación, que no deben cargar; cambia el prompt de sistema de todos los turnos.

**Recomendación: la B.** Cubre las dos cosas con un solo mecanismo y es la que mejor documenta la propia Claude Code. Si la API de mods cambiara, el mismo hook se puede declarar como hook clásico de tipo `command` con un script del plugin.

**Orquestación entera o solo la orden.** El mod puede entregar el texto de la skill (unos 7 KB) o solo «carga `sf:orquestacion`». El texto entero no depende de que Claude obedezca, que es justo lo que falla tras compactar; la orden sola gasta menos y deja la carga visible. Se recomienda el texto entero.

## Los proyectos ya incorporados | La transición | Transición {#transicion}

Con la B, un proyecto con la línea `@.sf/claude-sf.md` recibiría las reglas dos veces, y la copia antigua podría contradecir a la nueva.

**Propuesta.** El caso «actualizar» de `sf:incorporar_proyecto_a_sf` quita la línea y `.sf/claude-sf.md`, y en los proyectos anteriores a la plantilla (JKanban, SmartColdBox) propone quitar el apartado «Software Factory» escrito a mano. Se hace en una sesión abierta en cada proyecto, como manda «Un proyecto por sesión». Hasta entonces, el panel ya avisa de que el proyecto va por detrás de la SF.

**Alternativa.** El mod quita del contexto, con `prompt.context`, el `.sf/claude-sf.md` importado, para que mande siempre la versión instalada sin tocar el proyecto. Es inmediato, pero oculta lo que hay escrito en el proyecto.

**La propia SF no recibe la inyección.** Su `CLAUDE.md` ya dice las reglas desde la fuente, con lo propio de desarrollar la SF; el mod la reconoce como `sf` y no como `proyecto`.

## Las normas vigentes | Dónde va cada una | Normas vigentes {#normas}

Las normas que hoy están en la memoria de la SF, y las dos que el informe ya recogía, con su destino. Ninguna necesita el contexto del mod: la llevan sus skills y documentos, y el mod solo los entrega.

| Norma | Destino | Cómo llega |
| --- | --- | --- |
| Manda `sf:orquestacion` hasta cerrar la 208 | Se queda en la memoria de la SF y se borra al cerrar la 208 | Aviso de transición; ya es paso de la 208 |
| «Cerrar antes que abrir» (157) | `sf:orquestacion`, «Libre» y «Poner en curso»; la metodología | Paso de la 208 |
| Un fallo propio también es bug | `sf:orquestacion`, punto 2: «Bug: a la cola antes de investigarlo, también si la causa es un olvido de Claude» | Paso nuevo de la 211 o de la 208 |
| Herramientas reutilizables al plugin | La metodología, en la automejora, y la regla de mejora continua de la plantilla. Las opciones de lectura ya están en `sf:documento_vision` | Paso de la 208 |
| «Propietario de la Software Factory» | `CLAUDE.md` de la SF, en sus reglas de trabajo. Es de los documentos de la SF | Paso de la 208 |
| Muchos pasos, una sola cosa | `sf:orquestacion`, «Fusionar, separar y redescribir», delante del título desfasado | Paso nuevo; ya no está en la memoria ni en la skill |
| Perfil del propietario | Se queda en la memoria de la SF. Es un dato, no una norma; su forma de aplicarlo (visión antes que detalle, pedir la menor atención) ya está en el método | Nada |

**Lo que queda en la memoria de la SF:** el perfil y el aviso de transición, hasta la 208.


## Una norma nueva | De la memoria a su skill | Norma nueva {#norma-nueva}

Lo que añadiría `sf:orquestacion`, en «Preguntar», junto a las decisiones:

> Una norma del propietario (cómo quiere que se trabaje) va a la skill donde se aplica, no a la memoria. En el mismo turno, paso o tarea «Llevar «<norma>» a <skill>»; si debe valer ya en esta sesión, se guarda también en la memoria con su destino, y al publicar se reduce a una remisión. Surgida en otro proyecto, se anota en el registro común de la SF, donde el panel la convierte en tarea.

**Por qué en «Preguntar».** Es donde la skill dice qué hacer con lo que decide el propietario; una norma es una decisión sobre la forma de trabajar.

**El registro común como canal.** Desde otro proyecto no se puede cambiar la SF ni su memoria. El registro común (`.sf/registro.json` de la SF) ya recoge lo que dice el propietario como `dicho`, y su «→» lo convierte en tarea de la SF sin Claude.

## Lo que habría que implementar | En las tareas 248 y 208 | Implementar {#implementar}

1. **Mod (tarea 248):** hook `classic.SessionStart` con `source` `startup`, `clear` y `compact` (en `resume` la conversación ya lo tiene), solo con `tipo: 'proyecto'`, que devuelva en `additionalContext` las reglas de la plantilla y el texto de `sf:orquestacion`, leídos con `$.fs` desde `$.plugin.root`. Con el interruptor de `.sf/proyecto.json` (171). Si el `CLAUDE.md` importa `.sf/claude-sf.md`, solo la orquestación.
2. **Subagentes (más adelante):** hook `classic.SubagentStart` con un encargo mínimo común: no cargar la orquestación ni escribir la cola.
3. **Prueba:** test con `$.classic.SessionStart({ source: 'compact' })` en `claude plugin test`; a mano, en un proyecto consumidor, preguntar por las reglas tras `/compact` y comprobar que un subagente no las recibe.
4. **`sf:incorporar_proyecto_a_sf`:** sin copia ni línea en el `CLAUDE.md`; el caso «actualizar» quita las dos; el diagnóstico comprueba que no quedan.
5. **`sf:orquestacion`:** la carga al empezar y tras compactar pasa al mod (se quita de la descripción y de la entrada); la regla de la norma nueva, en «Preguntar»; «Muchos pasos, una sola cosa», en «Fusionar, separar y redescribir».
6. **Documentos compartidos** (la plantilla, la metodología, el `CLAUDE.md` de la SF, «Cómo funciona la Software Factory» y «Cómo funciona el panel»), en sus tareas «Actualizar…»; las normas, como dice la tabla.
7. **Proyectos consumidores:** pasar «actualizar» en Sprites, sprite_animation, JKanban y SmartColdBox, cada uno en su sesión.

## Lo que decide el propietario | Tres preguntas | Decidir {#decidir}

Ya resuelto por otras decisiones: la norma nueva surgida en otro proyecto se registra como mejora de la SF (167); el encargo a los subagentes con `SubagentStart` queda para más adelante; «Propietario de la Software Factory» vale solo en la SF.

**1. Cómo llegan las reglas de la plantilla a cada proyecto.**

- **B. `classic.SessionStart`** al empezar, tras `/clear` y tras compactar. Pro: cero líneas en el `CLAUDE.md` y siempre la versión instalada. Contra: unos 3.000 tokens por arranque, junto con la orquestación.
- **D. `prompt.compose`**, como la regla de la 167. Pro: en cada petición, nunca se pierde. Contra: alarga el prompt de sistema de todos los turnos y quizá llega a los subagentes.
- **A. La línea `@.sf/claude-sf.md`**, como hoy. Pro: probada, sin mod. Contra: una copia por proyecto que se queda atrás.

Recomendación: **B**, y la regla de la 167 sigue en `prompt.compose` por corta.

**2. Qué entrega el mod de `sf:orquestacion` (tarea 248).**

- **El texto entero.** Pro: no depende de que Claude obedezca, justo lo que falla tras compactar. Contra: unos 2.000 tokens más.
- **Solo la orden de cargarla.** Pro: barato y la carga se ve. Contra: puede no cumplirse.

Recomendación: **el texto entero**, con el interruptor `orquestacion` en `.sf/proyecto.json`, encendido por defecto (171).

**3. Los proyectos ya incorporados, con la línea `@.sf/claude-sf.md`.**

- **Se quita en su sesión**, con el caso «actualizar» de `sf:incorporar_proyecto_a_sf`. Pro: el proyecto queda limpio. Contra: hasta entonces recibe las reglas dos veces.
- **El mod la oculta** con `prompt.context`. Pro: inmediato. Contra: esconde lo que está escrito en el proyecto.
- **Las dos a medias:** el mod no entrega la plantilla si ve la línea, sí la orquestación, y el panel avisa de que el proyecto va atrasado. Pro: sin duplicados ni ocultar nada. Contra: la copia antigua manda hasta actualizar.

Recomendación: **la tercera**.
