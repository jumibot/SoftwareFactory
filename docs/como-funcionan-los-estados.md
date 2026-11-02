# Cómo funcionan los estados

Cómo pasa una tarea de un estado a otro, quién hace cada cambio y qué deja en git, en la cola y en el historial. La regla de cada cambio, con su orden, está en la skill `sf:flujo_tareas`, en [plugins/sf/skills/flujo_tareas/references/estados.md](../plugins/sf/skills/flujo_tareas/references/estados.md). Los botones, en [Cómo funciona el panel](como-funciona-el-panel.html#actuar-desde-el-panel). Cuándo usa Claude cada cambio al hablar contigo, en la skill `sf:orquestacion`.

**Estado:** 1 de noviembre de 2026. Recoge el flujo de la tarea 92 (decisiones 113, 114 y 115), la regla de cierre (121) y la T, hoy Activar rama (122). También: el menú al anotar (139), cerrar directamente lo que no tiene prueba (154), TURBO (160), las órdenes como etiquetas (168), la recogida del subagente (169), una tarea en curso con rama no vuelve a la cola (170), los pasos de cierre desde que entra en curso (174), las etiquetas «A Testing» y «Cerrar» (182) y la skill `sf:orquestacion`.

## Los estados

Cada tarea vive en la cola, `.sf/peticiones.json`, con uno de cuatro estados: en cola, en curso, Testing y descartada. Cuando termina su recorrido, sale de la cola y queda en el historial.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 530" width="100%" role="img" aria-label="Diagrama de estados de una tarea: se crea en cola y pasa a en curso; solo vuelve a la cola si aún no tiene rama; de en curso va a Testing con A Testing o, con Cerrar, directamente a Cerradas; de Testing, con Cerrar, probada, a Cerradas. En cola o en curso, sin rama se elimina y con rama se descarta. Son las etiquetas Eliminar, Descartar y Revertir. En Testing o cerrada, se revierte, y queda eliminada o vuelve a la cola. Desde Testing, Cerradas o descartada se reabre." style="font-family:var(--fuente-texto);display:block">
<defs>
<marker id="fe-t" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#00726b"/></marker>
<marker id="fe-n" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#a6501a"/></marker>
</defs>
<line x1="170" y1="8" x2="170" y2="48" stroke="#00726b" stroke-width="1.6" marker-end="url(#fe-t)"/>
<text x="180" y="30" font-size="12.5" fill="#555">crear</text>
<rect x="60" y="50" width="220" height="52" rx="8" fill="none" stroke="#00726b" stroke-width="1.6"/>
<text x="76" y="72" font-size="14.5" font-weight="700" fill="#004d47">En cola</text>
<text x="76" y="91" font-size="12.5" fill="#555">anotada, sin empezar</text>
<line x1="140" y1="102" x2="140" y2="168" stroke="#00726b" stroke-width="1.6" marker-end="url(#fe-t)"/>
<text x="132" y="140" font-size="12.5" fill="#555" text-anchor="end">empezar</text>
<line x1="200" y1="170" x2="200" y2="104" stroke="#00726b" stroke-width="1.6" marker-end="url(#fe-t)"/>
<text x="208" y="134" font-size="12.5" fill="#555">dejar en cola,</text>
<text x="208" y="150" font-size="12.5" fill="#555">solo sin rama</text>
<rect x="60" y="170" width="220" height="52" rx="8" fill="none" stroke="#00726b" stroke-width="2.6"/>
<text x="76" y="192" font-size="14.5" font-weight="700" fill="#004d47">En curso</text>
<text x="76" y="211" font-size="12.5" fill="#555">en su rama, con su subagente</text>
<line x1="170" y1="222" x2="170" y2="288" stroke="#00726b" stroke-width="1.6" marker-end="url(#fe-t)"/>
<text x="178" y="260" font-size="12.5" fill="#555">A Testing: cerrar sin probar</text>
<rect x="60" y="290" width="220" height="52" rx="8" fill="none" stroke="#00726b" stroke-width="1.6"/>
<text x="76" y="312" font-size="14.5" font-weight="700" fill="#004d47">Testing</text>
<text x="76" y="331" font-size="12.5" fill="#555">ya en develop, espera tu OK</text>
<line x1="170" y1="342" x2="170" y2="408" stroke="#00726b" stroke-width="1.6" marker-end="url(#fe-t)"/>
<text x="178" y="380" font-size="12.5" fill="#555">Cerrar: probada</text>
<rect x="60" y="410" width="220" height="52" rx="8" fill="none" stroke="#00726b" stroke-width="1.6"/>
<text x="76" y="432" font-size="14.5" font-weight="700" fill="#004d47">Cerradas</text>
<text x="76" y="451" font-size="12.5" fill="#555">fuera de la cola, en el historial</text>
<path d="M60,196 L34,196 L34,436 L58,436" fill="none" stroke="#00726b" stroke-width="1.6" marker-end="url(#fe-t)"/>
<text x="26" y="316" font-size="12.5" fill="#555" text-anchor="middle" transform="rotate(-90 26 316)">Cerrar: probada y cerrada</text>
<path d="M280,76 L300,76 L300,196 L280,196" fill="none" stroke="#a6501a" stroke-width="1.4"/>
<line x1="300" y1="76" x2="358" y2="76" stroke="#a6501a" stroke-width="1.6" marker-end="url(#fe-n)"/>
<text x="329" y="68" font-size="11" font-weight="700" fill="#a6501a" text-anchor="middle">Eliminar</text>
<line x1="300" y1="196" x2="358" y2="196" stroke="#a6501a" stroke-width="1.6" marker-end="url(#fe-n)"/>
<text x="329" y="188" font-size="11" font-weight="700" fill="#a6501a" text-anchor="middle">Descartar</text>
<rect x="360" y="50" width="180" height="52" rx="8" fill="none" stroke="#a6501a" stroke-width="1.4"/>
<text x="374" y="72" font-size="14.5" font-weight="700" fill="#a6501a">Eliminada</text>
<text x="374" y="91" font-size="12.5" fill="#555">sin rama; al historial</text>
<rect x="360" y="170" width="180" height="52" rx="8" fill="none" stroke="#a6501a" stroke-width="1.4"/>
<text x="374" y="192" font-size="14.5" font-weight="700" fill="#a6501a">Descartada</text>
<text x="374" y="211" font-size="12.5" fill="#555">rama borrada</text>
<path d="M280,316 L300,316 L300,436 L280,436" fill="none" stroke="#a6501a" stroke-width="1.4"/>
<line x1="300" y1="376" x2="358" y2="376" stroke="#a6501a" stroke-width="1.6" marker-end="url(#fe-n)"/>
<text x="329" y="368" font-size="11" font-weight="700" fill="#a6501a" text-anchor="middle">Revertir</text>
<rect x="360" y="350" width="180" height="52" rx="8" fill="none" stroke="#a6501a" stroke-width="1.4"/>
<text x="374" y="372" font-size="14.5" font-weight="700" fill="#a6501a">Revertida</text>
<text x="374" y="391" font-size="12.5" fill="#555">y eliminada o en cola</text>
<text x="34" y="500" font-size="14.5" font-weight="700" fill="#be185d">↺ Reabrir</text>
<text x="120" y="500" font-size="12.5" fill="#555">desde Testing, Cerradas o descartada:</text>
<text x="120" y="518" font-size="12.5" fill="#555">vuelve en curso o en cola, con su número</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El camino principal baja por la izquierda; lo que se deshace, a la derecha.</figcaption>
</figure>

Una tarea nace **en cola** y empieza cuando se pone en curso. En curso, trabaja en su rama, con su subagente. **Con rama, ya no vuelve a la cola:** para dejarla, se cierra, se pasa a Testing o se descarta. Solo vuelve una tarea en curso que aún no tiene rama.

Al acabar, se cierra por uno de dos caminos. Con Cerrar, entra en `develop` y sale de la cola a la vez. Si hace falta cerrarla para poder probarla, va con A Testing: ya está en `develop` y espera tu OK, que es su Cerrar.

A la derecha está lo que se deshace. Una tarea sin rama no ha cambiado nada y se elimina. Con rama, se descarta. Una vez en `develop`, ya no se descarta: se revierte. Cualquiera de las que han salido, salvo la eliminada, se puede reabrir.

Testing también tiene una marca, «probando». La pones al contestar «Probar ahora»: la tarea sube arriba, en amarillo, sin dejar de estar en Testing. Con «Pendiente», la marca se quita.

## Quién mueve una tarea

Cada cambio lo hace uno de tres: tú, con un botón del panel; Claude, el principal que habla contigo; o el CLI `cola.py`, que ejecuta los dos. Las reglas del principal están en la skill `sf:orquestacion`: qué hace con cada mensaje, cómo lleva la cola, cuándo lanza un subagente y cómo prueba y cierra. **Toda escritura de la cola pasa por el CLI.** Así cada regla está en un solo sitio y la cola nunca se edita a mano.

El principal lanza `cola.py` por Bash. El panel lo lanza igual cuando pulsas un botón o escribes un comando, como propietario, y lee del historial las letras de las tareas y las Cerradas. Toda tarea en curso tiene su subagente, que hace todo su trabajo. Los subagentes no escriben la cola: dicen en su informe lo que han hecho y el principal lo anota.

Algunos cambios piden tu OK y otros no. Crear una tarea, crear su rama o marcar un paso no lo piden. Cerrar, pasar a Testing, dar por probada y descartar esperan tu OK. Antes, Claude te propone probarla y te dice cómo. Las órdenes del panel son etiquetas en la primera fila de la tarea desplegada. Las que cierran o deshacen piden confirmar: «Cerrar» pasa a «¿Cerrar? sí», y ese segundo clic es tu OK. «Revertir» pregunta el destino: «¿Revertir? eliminar | a Pendientes».

## Empezar una tarea

Toda petición entra en la cola en cuanto llega, también un bug antes de investigarlo. Al anotarla, Claude abre un menú breve. Si encaja como paso de una tarea, pregunta primero si se añade a ella. Si no, pregunta si va en curso o se queda en cola. No pregunta lo que ya has dicho, como «tarea», «paso de la NN», «en curso» o «en cola». La «→» de una entrada del registro del panel crea una tarea en cola, sin menú.

Pasa a en curso cuando preguntas por ella o la eliges. Con TURBO, Claude pone en curso, cada una con su subagente, las tareas de la cola que puede hacer sin ti, y te dice cuáles. Las que te necesitan se quedan en la cola. La etiqueta Activar rama hace lo mismo con una tarea que ya tiene rama: la activa con `git switch` para que la pruebes. La pone en prueba, pero no la da por probada. Puede haber varias en curso, cada una en su rama.

Al ponerla en curso, `cola.py` le añade los dos pasos de cierre: «Activar rama para poder probar» y «Cerrar la tarea». Así se ve su camino completo desde el principio. Los pasos de trabajo nuevos van antes de ellos.

Antes de tocar el primer archivo del repositorio, Claude crea la rama `feature/NN-nombre` desde `develop` y te avisa. **Desde que tiene rama, la tarea ya no se elimina: se descarta.** Para el subagente, el principal crea la rama sin activarla y la anota antes de lanzarlo. El subagente trabaja en su worktree, en su rama auxiliar `sub-NN`, y el principal trae sus commits. Cómo se lanza, se le pasa cada encargo y se recoge, en `sf:orquestacion`.

Dejar una tarea en cola, con tu OK, solo vale si aún no tiene rama. Con rama, `cola.py en-cola` lo rechaza: se cierra, se pasa a Testing o se descarta. Así no quedan ramas de tareas en cola, ni subagentes sin trabajo. Si tiene que esperar a otra cosa, lleva un paso «Esperar a …», y su subagente no trabaja hasta que se cumple.

## Probar y cerrar

Los pasos de cierre ya están desde que la tarea entró en curso. Al acabar el último paso de trabajo, Claude escribe qué debes mirar (`cola.py listo`). Lo que Claude comprueba por su cuenta queda aparte, en `comprobado`, con un «✓» verde en Testing.

**Todo cierre exige el paso «Cerrar la tarea»** y que no quede pendiente ningún otro, salvo «Activar rama para poder probar» y las ayudas de prueba, que son opcionales. Vale con rama o sin ella, también para pasar a Testing. Una tarea en curso sin pasos de cierre los recibe al cargar la cola. Por eso, en el panel, Cerrar y A Testing solo salen en una tarea en curso que cumple esa regla, con rama o sin ella.

Los pasos de cierre no se quitan. «Activar rama para poder probar» se marca al activar la rama de la tarea. Si sigue pendiente al cerrar, el cierre lo marca, porque Cerrar es tu OK. Si se añade un paso de trabajo con él ya hecho, vuelve a pendiente: hay que probar otra vez.

Pulsar Cerrar, con «¿Cerrar? sí», es decir «probada, ciérrala». El panel pasa a `develop` y hace el squash de la rama en un commit, `<tarea> (N)`, con los pasos en el cuerpo. Después hace push, borra la rama y saca la tarea de la cola. Si el squash choca, lo deshace todo, la tarea sigue en curso y Claude lo resuelve.

Al cerrar, `cola.py` quita también el worktree del subagente y borra su rama auxiliar, sin forzar. Lo hace en toda orden que deja la tarea sin subagente: cerrar, A Testing, probada, descartar, eliminar, revertir, limpiar, reabrir y fusionar. Si el worktree tiene cambios sin commit, o la rama auxiliar commits que no entraron, se quedan y avisa. Claude solo detiene el subagente.

A Testing es el otro camino. Es la etiqueta que sigue a Cerrar en la tarea en curso, con «¿A Testing? sí» (`cola.py a-testing`). Hace el mismo squash, pero la tarea pasa a Testing en lugar de salir. Se usa cuando el cierre hace falta para probar, como un commit o una publicación.

En Testing, la tarea lleva su propia etiqueta Cerrar, con «¿Cerrar? sí» (`cola.py probada`): darla por probada es cerrarla. También vale decir «probada»; sin número, es la tarea de la rama activa. En los dos casos, sale de la cola.

Si la tarea no tiene nada que probar, como deliberar, investigar o documentar, Claude te propone cerrarla directamente y te enseña el resultado. Con tu OK, se cierra sin probar: el cierre marca «Activar rama para poder probar».

Una tarea sin rama no tocó ningún archivo. Se cierra, o pasa a Testing, sin squash ni commit, con sus pasos de cierre, como cualquier otra. El panel ofrece Cerrar y A Testing en cuanto sus pasos de trabajo están hechos (188).

Entrar en prueba no es estar probada. Activar rama activa la rama y marca «Activar rama para poder probar», pero no da la tarea por probada. Lo está cuando lo dices o pulsas Cerrar.

## Deshacer

Hay cuatro formas de deshacer, según lo lejos que haya llegado la tarea:

| Cambio | Cuándo | Qué hace |
| --- | --- | --- |
| Eliminar | En cola o en curso, sin rama | La saca de la cola y de la vista; su número no se reutiliza |
| Descartar | En cola o en curso, con rama | Borra la rama; queda descartada hasta limpiar Cerradas |
| Revertir | En Testing o cerrada | `git revert` de su squash en `develop`, sin push; la tarea, eliminada o de vuelta en cola |
| Reabrir | Al probarla falla, o aparece un bug suyo | Vuelve a la cola con su número, marcada como reabierta |

La eliminada no pasa por Cerradas, pero su historial se guarda: `cola.py restaurar` la devuelve a la cola. La descartada sigue en la cola hasta que pulsas «limpiar», o hasta la sesión siguiente.

Revertir lee del historial qué commits revertir, del más reciente al más antiguo. Pide el destino: «eliminar» la saca sin rastro, como Eliminar, y «a Pendientes» la devuelve a la cola, reabierta, con H y sin rama. En los dos casos borra la rama de la tarea, si aún existe, y lo que quede de su subagente; solo conserva, con aviso, una rama con commits que nunca entraron en `develop`. Si el revert choca, lo aborta y se lo pasa a Claude. Una tarea que ya estaba en `main` queda revertida en la versión siguiente.

Una reabierta vuelve con su número y con H en el panel, aunque se cerrara en esta sesión. En curso, empieza con una rama nueva desde `develop`; en cola, sin rama hasta empezarla. Una descartada se reabre igual.

Fusionar y separar no cambian el estado. `/fusionar` deja la tarea de número más alto y absorbe las demás, que salen de la cola. `/split` saca unos pasos a una tarea nueva, en cola.

## Qué queda de cada cambio

Cada cambio deja rastro en uno o varios sitios, y cada sitio tiene su dueño:

| Dónde | Qué guarda | Quién lo escribe |
| --- | --- | --- |
| git | La rama, el squash `<tarea> (N)` y los revert | El panel o Claude |
| Cola, `.sf/peticiones.json` | Las tareas vivas, cada una con su `historial` | Solo el CLI |
| Historial, `.sf/historial.jsonl` | Una línea por tarea que sale de la cola | Solo el CLI |

El `historial` de cada tarea apunta cada cambio con su fecha, quién lo decidió y por dónde llegó: tú o el principal, desde el panel o desde el CLI. Ahí quedan también el hash del squash y los fallos, como un push que no llegó. Con él, el panel deja de adivinar lo ocurrido comparando lecturas de la cola.

Cuando una tarea sale de la cola, cerrada, probada, limpiada, eliminada o absorbida, pasa entera a `.sf/historial.jsonl`. De ahí la recuperan `reabrir`, `restaurar` y `revertir`.

La cola está fuera de git, así que tiene sus propias copias. Antes de cada escritura, el CLI guarda la cola entera en `.sf/copias/`, con las 50 últimas. `cola.py copias` las lista y `cola.py recuperar` pone una, guardando antes la actual.
