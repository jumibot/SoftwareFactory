# Cómo funcionan los estados

Cómo pasa una tarea de un estado a otro, quién hace cada cambio y qué deja en git, en la cola y en el historial. La regla de cada cambio, con su orden, está en la skill `sf:flujo_tareas`, en [plugins/sf/skills/flujo_tareas/references/estados.md](../plugins/sf/skills/flujo_tareas/references/estados.md). Los botones, en [Cómo funciona el panel](como-funciona-el-panel.html#actuar-desde-el-panel). Cuándo usa Claude cada cambio al hablar contigo, en la skill `sf:orquestacion`.

**Estado:** 5 de noviembre de 2026. Recoge el flujo de tareas con un CLI común, historial por tarea y copias de la cola (113 a 115), la regla de cierre (121) y la etiqueta Activar rama. También: el menú al anotar (139), cerrar directamente lo que no tiene prueba (154), TURBO (160), las órdenes como etiquetas (168), la recogida del subagente (169), los pasos de cierre desde que entra en curso (174) y la skill `sf:orquestacion`. Y lo último: el estado «En observación», que se cierra si va bien o se revierte si va mal («Los estados de las tareas se nombran con el lenguaje de la SF», 204; 212 y 215); «Una tarea en curso con rama no vuelve a la cola» (170), precisada para que vuelva la que aún no tiene trabajo en su rama (tarea 275); volver a observación una cerrada por error (tarea 296); y las deliberativas, sin rama (278).

## Los estados

Cada tarea vive en la cola, `.sf/peticiones.json`, con uno de cuatro estados: en cola, en curso, en observación y descartada. Cuando termina su recorrido, sale de la cola y queda en el historial. En el panel, sus secciones son Pendientes, En observación y Cerradas.

<figure class="vertical" style="margin:1.8rem 0 1.4rem;">
<svg viewBox="0 0 560 550" width="100%" role="img" aria-label="Diagrama de estados de una tarea: se crea en cola y pasa a en curso; solo vuelve a la cola si su rama no tiene trabajo; de en curso va a En observación con A observación o, con Cerrar, directamente a Cerradas; de En observación, con Cerrar, si va bien, a Cerradas. En cola o en curso, sin rama se elimina y con rama se descarta. En observación o cerrada, se revierte, y queda eliminada o vuelve a la cola. Desde En observación, Cerradas o descartada se reabre; una cerrada por error vuelve a observación." style="font-family:var(--fuente-texto);display:block">
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
<text x="208" y="150" font-size="12.5" fill="#555">sin trabajo</text>
<rect x="60" y="170" width="220" height="52" rx="8" fill="none" stroke="#00726b" stroke-width="2.6"/>
<text x="76" y="192" font-size="14.5" font-weight="700" fill="#004d47">En curso</text>
<text x="76" y="211" font-size="12.5" fill="#555">en su rama, con su subagente</text>
<line x1="170" y1="222" x2="170" y2="288" stroke="#00726b" stroke-width="1.6" marker-end="url(#fe-t)"/>
<text x="178" y="260" font-size="12.5" fill="#555">A observación: cerrar y observar</text>
<rect x="60" y="290" width="220" height="52" rx="8" fill="none" stroke="#00726b" stroke-width="1.6"/>
<text x="76" y="312" font-size="14.5" font-weight="700" fill="#004d47">En observación</text>
<text x="76" y="331" font-size="12.5" fill="#555">ya en develop, se vigila</text>
<line x1="170" y1="342" x2="170" y2="408" stroke="#00726b" stroke-width="1.6" marker-end="url(#fe-t)"/>
<text x="178" y="380" font-size="12.5" fill="#555">Cerrar: va bien</text>
<rect x="60" y="410" width="220" height="52" rx="8" fill="none" stroke="#00726b" stroke-width="1.6"/>
<text x="76" y="432" font-size="14.5" font-weight="700" fill="#004d47">Cerradas</text>
<text x="76" y="451" font-size="12.5" fill="#555">fuera de la cola, en el historial</text>
<path d="M60,196 L34,196 L34,436 L58,436" fill="none" stroke="#00726b" stroke-width="1.6" marker-end="url(#fe-t)"/>
<text x="26" y="316" font-size="12.5" fill="#555" text-anchor="middle" transform="rotate(-90 26 316)">Cerrar: sin pasar por observación</text>
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
<text x="120" y="500" font-size="12.5" fill="#555">desde En observación, Cerradas o descartada:</text>
<text x="120" y="518" font-size="12.5" fill="#555">vuelve en curso o en cola, con su número.</text>
<text x="120" y="538" font-size="12.5" fill="#555">Una cerrada por error vuelve a En observación.</text>
</svg>
<figcaption style="font-size:.82rem;color:#555;text-align:center;font-style:italic;margin-top:.3rem;">El camino principal baja por la izquierda; lo que se deshace, a la derecha.</figcaption>
</figure>

Una tarea nace **en cola** y empieza cuando se pone en curso. En curso, trabaja en su rama, con su subagente. **Con trabajo en su rama, ya no vuelve a la cola:** para dejarla, se cierra, se pasa a observación o se descarta. Vuelve la que aún no tiene rama o la tiene sin trabajo.

Al acabar, se cierra por uno de dos caminos. Con Cerrar, entra en `develop` y sale de la cola a la vez. Si solo se puede ver funcionando una vez cerrada, como un commit o una publicación, va con A observación: ya está en `develop` y se vigila con el uso. **En observación, se cierra si va bien o se revierte si va mal.**

A la derecha está lo que se deshace. Una tarea sin rama no ha cambiado nada y se elimina. Con rama, se descarta. Una vez en `develop`, ya no se descarta: se revierte. Cualquiera de las que han salido, salvo la eliminada, se puede reabrir.

En observación también hay una marca, «observando». La pones al contestar «La miro ahora» a «¿Cómo va la N?»: la tarea sube arriba, en amarillo, sin dejar de estar en observación. Con «Sigue en observación», la marca se quita.

## Quién mueve una tarea

Cada cambio lo hace uno de tres: tú, con un botón del panel; Claude, el principal que habla contigo; o el CLI `cola.py`, que ejecuta los dos. Las reglas del principal están en la skill `sf:orquestacion`: qué hace con cada mensaje, cómo lleva la cola, cuándo lanza un subagente y cómo prueba y cierra. **Toda escritura de la cola pasa por el CLI.** Así cada regla está en un solo sitio y la cola nunca se edita a mano.

El principal lanza `cola.py` por Bash. El panel lo lanza igual cuando pulsas un botón o escribes un comando, como propietario, y lee del historial las letras de las tareas y las Cerradas. Toda tarea en curso tiene su subagente, que hace todo su trabajo. Los subagentes no escriben la cola: dicen en su informe lo que han hecho y el principal lo anota.

Algunos cambios piden tu OK y otros no. Crear una tarea, crear su rama o marcar un paso no lo piden. Cerrar, pasar a observación, volver a observación, dejar en cola y descartar esperan tu OK. Antes, Claude te propone probarla y te dice cómo. Las órdenes del panel son etiquetas en la primera fila de la tarea desplegada. Las que cierran o deshacen piden confirmar: «Cerrar» pasa a «¿Cerrar? sí», y ese segundo clic es tu OK. «Revertir» pregunta el destino: «¿Revertir? eliminar | a Pendientes».

## Empezar una tarea

Toda petición entra en la cola en cuanto llega, también un bug antes de investigarlo. Al anotarla, Claude abre un menú breve. Si encaja como paso de una tarea, pregunta primero si se añade a ella. Si no, pregunta si va en curso o se queda en cola. No pregunta lo que ya has dicho, como «tarea», «paso de la NN», «en curso» o «en cola». La «→» de una entrada del registro del panel crea una tarea en cola, sin menú.

Pasa a en curso cuando preguntas por ella o la eliges. Antes, Claude mira si comparte archivos con otra en curso o en observación (`cola.py choques`); si choca, te lo dice y espera tu OK. Con TURBO, Claude pone en curso, cada una con su subagente, las tareas de la cola que puede hacer sin ti, y te dice cuáles. Las que te necesitan se quedan en la cola. Puede haber varias en curso, cada una en su rama.

Al ponerla en curso, `cola.py` le añade los dos pasos de cierre: «Activar rama para poder probar» y «Cerrar la tarea». Así se ve su camino completo desde el principio. Los pasos de trabajo nuevos van antes de ellos. Una deliberativa (investigar, deliberar, diseñar) solo lleva «Cerrar la tarea»: no tiene rama ni se prueba; su documento va directo a `develop` (278).

Antes de tocar el primer archivo del repositorio, Claude crea la rama `feature/NN-nombre` desde `develop` y te avisa. **Desde que tiene rama, la tarea ya no se elimina: se descarta.** Para el subagente, el principal crea la rama sin activarla y la anota antes de lanzarlo. El subagente trabaja en su worktree, en su rama auxiliar `sub-NN`, y el principal trae sus commits. Cómo se lanza, se le pasa cada encargo y se recoge, en `sf:orquestacion`.

Dejar una tarea en cola, con tu OK, solo vale si aún no tiene trabajo (`cola.py en-cola`). Sin rama, vuelve tal cual. Con una rama sin commits propios respecto a `develop`, o ya borrada, la borra y recoge el subagente vacío, y la tarea vuelve sin rama, con su número y su historial (tarea 275). Con commits en su rama o en la del subagente, o con cambios sin commit en su worktree, lo rechaza: se cierra, se pasa a observación o se descarta. Así no quedan ramas de tareas en cola, ni subagentes sin trabajo. Si tiene que esperar a otra cosa, lleva un paso «Esperar a …», y su subagente no trabaja hasta que se cumple.

## Probar y cerrar

Los pasos de cierre ya están desde que la tarea entró en curso. Al acabar el último paso de trabajo, Claude escribe qué debes mirar (`cola.py listo`). Lo que Claude comprueba por su cuenta queda aparte, en `comprobado`, con un «✓» verde en En observación.

La etiqueta Activar rama (`cola.py probar`) pone la tarea en prueba: integra `develop` en su rama, para probar con lo último y que el cierre no choque, la activa con `git switch` y marca «Activar rama para poder probar». Si una tarea en cola ya tiene rama, la pone además en curso. Si `develop` choca, o el subagente tiene commits sin traer, no activa nada y se lo pasa a Claude. Activar la rama no es darla por buena: lo está cuando lo dices o pulsas Cerrar.

**Todo cierre exige el paso «Cerrar la tarea»** y que no quede pendiente ningún otro, salvo «Activar rama para poder probar» y las ayudas de prueba, que son opcionales. Vale con rama o sin ella, también para pasar a observación. Una tarea en curso sin pasos de cierre los recibe al cargar la cola. Por eso, en el panel, Cerrar y A observación solo salen en una tarea en curso que cumple esa regla, con rama o sin ella.

Los pasos de cierre no se quitan. «Activar rama para poder probar» se marca al activar la rama de la tarea. Si sigue pendiente al cerrar, el cierre lo marca, porque Cerrar es tu OK. Si se añade un paso de trabajo con él ya hecho, vuelve a pendiente: hay que probar otra vez.

Pulsar Cerrar, con «¿Cerrar? sí», es tu OK: «ciérrala». El panel pasa a `develop` y hace el squash de la rama en un commit, `<tarea> (N)`, con los pasos en el cuerpo. Después hace push, borra la rama y saca la tarea de la cola. Si la rama no tiene nada que no esté ya en `develop`, no hay squash ni commit: la borra y la tarea sale cerrada, sin commit. Si el squash choca, lo deshace todo, la tarea sigue en curso y Claude lo resuelve. Si el push falla, cierra igual y lo avisa: se sube después con `cola.py subir`.

Al cerrar, `cola.py` quita también el worktree del subagente y borra su rama auxiliar, sin forzar. Antes, se niega si la rama auxiliar tiene commits que no están en la de la tarea: el squash los perdería. Recoge el subagente en toda orden que deja la tarea sin él: cerrar, A observación, dejar en cola, descartar, eliminar, revertir, limpiar, reabrir y fusionar. Si el worktree tiene cambios sin commit, o la rama auxiliar commits que no entraron, se quedan y avisa. Claude solo detiene el subagente.

A observación es el otro camino. Es la etiqueta que sigue a Cerrar en la tarea en curso, con «¿A observación? sí» (`cola.py a-observacion`). Hace el mismo squash, pero la tarea pasa a En observación en lugar de salir. Se usa cuando el resultado solo se ve funcionando tras el cierre, como un commit o una publicación. No se usa en una deliberativa ni con la rama sin cambios: esas se cierran.

En observación, Claude te pregunta «¿Cómo va la N?», con Cerrar, Sigue en observación, La miro ahora y Revertir. Si va bien, la tarea lleva su propia etiqueta Cerrar, con «¿Cerrar? sí» (`cola.py cerrar`). También vale decir «ciérrala»; sin número, es la tarea de la rama activa. Sale de la cola. Si va mal, se revierte.

Si se cerró por error y hay que seguir vigilándola, la etiqueta A observación de una tarea en Cerradas la devuelve a En observación, con su commit de `develop`, para poder revertirla (`cola.py reobservar`).

Si la tarea no tiene nada que probar, como deliberar, investigar o documentar, Claude te propone cerrarla directamente y te enseña el resultado. Con tu OK, se cierra sin pasar por observación: el cierre marca «Activar rama para poder probar».

Una tarea sin rama no tocó ningún archivo. Se cierra, o pasa a observación, sin squash ni commit, con sus pasos de cierre, como cualquier otra. El panel ofrece Cerrar y A observación en cuanto sus pasos de trabajo están hechos (188).

## Deshacer

Hay cuatro formas de deshacer, según lo lejos que haya llegado la tarea:

| Cambio | Cuándo | Qué hace |
| --- | --- | --- |
| Eliminar | En cola o en curso, sin rama | La saca de la cola y de la vista; su número no se reutiliza |
| Descartar | En cola o en curso, con rama | Borra la rama y lo de su subagente; queda descartada hasta limpiar Cerradas |
| Revertir | En observación o cerrada | `git revert` de su squash en `develop`, sin push; la tarea, eliminada o de vuelta en cola |
| Reabrir | Al probarla u observarla falla, o aparece un bug suyo | Vuelve con su número, marcada como reabierta |

La eliminada no pasa por Cerradas, pero su historial se guarda: `cola.py restaurar` la devuelve a la cola. La descartada sigue en la cola hasta que pulsas «limpiar», o hasta la sesión siguiente. Una tarea en cola sin rama que aún no está decidida vuelve a ser propuesta con «A propuesta» (`cola.py a-propuesta`): sale de la cola, como eliminada, y vuelve a `sf/propuestas.md`.

Revertir lee del historial qué commits revertir, del más reciente al más antiguo. Pide el destino: «eliminar» la saca sin rastro, como Eliminar, y «a Pendientes» la devuelve a la cola, reabierta, con H y sin rama. En los dos casos borra la rama de la tarea, si aún existe, y lo que quede de su subagente; solo conserva, con aviso, una rama con commits que nunca entraron en `develop`. Si el revert choca, lo aborta y se lo pasa a Claude. Una tarea que ya estaba en `main` queda revertida en la versión siguiente.

Una reabierta vuelve con su número y con H en el panel, aunque se cerrara en esta sesión. En curso, empieza con una rama nueva desde `develop`; en cola, sin rama hasta empezarla. Una en observación o una descartada se reabren igual.

Fusionar y separar no cambian el estado. `/sf_fusionar` deja la tarea de número más alto y absorbe las demás, que salen de la cola. `/sf_split` saca unos pasos a una tarea nueva, en cola.

## Qué queda de cada cambio

Cada cambio deja rastro en uno o varios sitios, y cada sitio tiene su dueño:

| Dónde | Qué guarda | Quién lo escribe |
| --- | --- | --- |
| git | La rama, el squash `<tarea> (N)` y los revert | El panel o Claude |
| Cola, `.sf/peticiones.json` | Las tareas vivas, cada una con su `historial` | Solo el CLI |
| Historial, `.sf/historial.jsonl` | Una línea por tarea que sale de la cola | Solo el CLI |

El `historial` de cada tarea apunta cada cambio con su fecha, quién lo decidió y por dónde llegó: tú o el principal, desde el panel o desde el CLI. Ahí quedan también el hash del squash y los fallos, como un push que no llegó. Con él, el panel deja de adivinar lo ocurrido comparando lecturas de la cola.

Cuando una tarea sale de la cola, cerrada, limpiada, eliminada o absorbida, pasa entera a `.sf/historial.jsonl`. De ahí la recuperan `reabrir`, `restaurar`, `revertir` y `reobservar`.

La cola está fuera de git, así que tiene sus propias copias. Antes de cada escritura, el CLI guarda la cola entera en `.sf/copias/`, con las 50 últimas. `cola.py copias` las lista y `cola.py recuperar` pone una, guardando antes la actual.
