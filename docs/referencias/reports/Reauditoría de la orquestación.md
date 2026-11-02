# Reauditoría de la orquestación

Segunda pasada de «Auditar que la skill de orquestación recoge todo lo ordenado» (216). Comprueba los 22 hallazgos del informe «Auditoría de la orquestación» y clasifica cada regla de `sf:orquestacion` en «de criterio» o «de siempre». Fecha: 2026-11-01.

## Base

- `develop` a 2026-11-01, con el plugin publicado 1.2.7: ya lleva la 215 (en Testing) y la poda de la memoria (217, cerrada).
- La rama `feature/246-limpieza-al-cerrar`, sin integrar: cambia `sf:orquestacion` («Probar y cerrar»), `sf:flujo_tareas` y `estados.md` (tarjetas 04, 10, 11, 18, 23, 27 y 29).
- Las decisiones 152 a 170.
- La cola: siguen abiertas la 208, la 218, la 219 y la 220, todas en cola.

## Estado de los hallazgos

**12 resueltos, 3 a medias, 7 pendientes.** Seis de los diez sin resolver dependen de una sola tarea, la 208, que tiene 22 pasos y sigue en cola.

| # | Hallazgo | Estado | Dónde se ve |
| --- | --- | --- | --- |
| 1 | Lanzar solo lo que no necesita al propietario | Resuelto | `orquestacion/SKILL.md` 28 y 40-42; publicado en 1.2.7 |
| 2 | El flujo de tareas manda trabajar en el principal | Resuelto | `estados.md`, tarjetas 10, 11 y 27 |
| 3 | Documentos compartidos en el principal | A medias | La skill (68) y «Documentos compartidos, también por subagente» (152), bien. El `CLAUDE.md`, línea 23, dice aún «en el principal»; la metodología, igual. Pasos 11 de la 208; la marca en la 112, en la 218 |
| 4 | Plantilla y CLAUDE.md: «que no le necesita» | Resuelto | `claude-sf.md` 15; `CLAUDE.md` 22 |
| 5 | La metodología contradice la orquestación | Pendiente | `desarrollo-de-proyectos.md` 50, 54, 56, 66 y 68; `metodologia/SKILL.md` 36. Pasos 1, 6, 8, 9 y 19 de la 208 |
| 6 | Memoria de la SF con normas superadas | Resuelto | 217 cerrada; queda solo «Normas vigentes aún fuera del plugin», que avisa de lo pendiente |
| 7 | `/paso` lo hace el principal | Resuelto | `SKILL.md` 36 |
| 8 | La C del panel deja vivo el subagente | Resuelto | Aviso «Desde el panel» (228); en la 246, `cola.py` recoge worktree y rama (169) y la skill pide solo detenerlo (51) |
| 9 | TURBO y las tareas de la cola | Resuelto | «TURBO pone en curso las tareas que no necesitan al propietario» (160), que sustituye a la 153; `SKILL.md` 40 |
| 10 | Redescribir con el título desfasado | Resuelto | `SKILL.md` 63 |
| 11 | Cerrar directamente lo que no tiene prueba | A medias | Decisión 154; skill 49; `estados.md` 13 y 21. Falta la metodología (paso 9 de la 208) y marcar «Probar antes de cerrar» (074) como precisada (218) |
| 12 | Las reglas de escritura no llegan a los subagentes | A medias | El encargo las lleva (`SKILL.md` 43). Falta «Sin referencias por número…» (150) en «Estructura documental común» (paso 7 de la 208) |
| 13 | Quién escribe el archivo de una decisión | Resuelto | «Las decisiones, a develop en cuanto se toman» (155); `SKILL.md` 42 y 78 |
| 14 | Seis órdenes sin decisión registrada | Pendiente | Ninguna tiene archivo aún. Tarea 218, en cola |
| 15 | Decisiones superadas sin marcar | Pendiente | 083, 086, 105, 048, 074 y 112 sin marca; «Aplicada en» desfasado en 114, 139 y 148. Tarea 218 |
| 16 | Restos en `estados.md` | Resuelto | Sin «salvo primer paso», «¿paso o tarea?» ni auxiliar «si hace falta» |
| 17 | «Cómo funciona» no recoge la skill | Pendiente | Tareas 219 y 220, en cola |
| 18 | El «→» del Registro en la plantilla | Pendiente | `claude-sf.md` 16. Paso 10 de la 208 |
| 19 | Referencias por número en plantilla y CLAUDE.md | Pendiente | `claude-sf.md` 9, 10, 12 y 14; `CLAUDE.md` 19, 21, 24, 27 y 33. Paso 7 de la 208 |
| 20 | El encargo no pide qué documentar | Resuelto | `SKILL.md` 43 |
| 21 | El porqué cita la norma superada | Resuelto | `porque.md`, sin la frase |
| 22 | Registro de uso desfasado | Pendiente | `.sf/registro.json`, entrada 2026-10-29 «Una tarea en curso que no necesita al propietario se lanza…». La borra el propietario desde el panel |

### Pendientes y su arreglo

- **3, 5, 11, 12, 18 y 19: hacer la 208.** Es el cuello de botella. Mientras, el `CLAUDE.md` de la SF, que se carga en cada sesión, contradice a la skill en «en el principal». La memoria lo compensa.
- **14 y 15: hacer la 218.** Crear los seis archivos y poner las marcas y los «Aplicada en».
- **17: hacer la 219 y la 220.**
- **22: el propietario borra la entrada** desde Registro.

### Desfases nuevos

- **Referencias sueltas en la skill.** La 246 añade «(169)» y «(170)» sin título en `SKILL.md` 51-53. Choca con «Sin referencias por número…» (150). Arreglo: en la propia 246, «(«cola.py recoge el subagente…», 169)» o quitarlas.
- **Reglas que ya cumple el código.** Las líneas 52 y 53 de la 246 («Reabrir limpia…» y «Una tarea en curso con rama no vuelve a la cola») las impone `cola.py`. Son mecánica de `sf:flujo_tareas`. Arreglo: quitarlas de la skill.
- **«Cómo funcionan los estados» contradice la 170.** Su línea 65 dice que una tarea en curso «puede volver a la cola sin perderla», y el diagrama, que vuelve. Arreglo: paso «Reflejar «Una tarea en curso con rama no vuelve a la cola» (170)» en la 220.
- **El paso 19 de la 208 cita la 153, ya sustituida.** Arreglo: que cite «TURBO pone en curso las tareas que no necesitan al propietario» (160).
- **«Cerrar antes que abrir» (157) no está en la skill.** Solo en la memoria. Ya está en el paso 15 de la 208.

## Reglas de la skill: de criterio o de siempre

**De criterio:** necesitan juicio del modelo. **De siempre:** se cumplen igual cada vez y el código puede hacerlas o vigilarlas. Sobre `SKILL.md` de la 246.

| Regla | Clase |
| --- | --- |
| Cargar la skill al empezar y tras compactar | Siempre |
| Consultar la cola antes de informar o actuar | Siempre |
| ¿De quién es la petición? (proyecto, SF, global) | Criterio |
| Lo global (`~/.claude`), no tocarlo sin que lo pida y confirme | Siempre (la vigilancia) |
| Bug y error ajeno, a la cola antes de investigar | Criterio |
| Encargo de una tarea en curso, a su subagente | Criterio (a cuál); siempre (que el principal no escriba) |
| Sin tarea en curso no se trabaja | Siempre |
| Al acabar el turno, lanzar lo que se pueda | Siempre |
| Libre, desbloquear | Criterio |
| Menú al anotar, agresivo con pasos, la prueba en su tarea | Criterio |
| Poner en curso: preguntar si no basta, planificar pasos | Criterio |
| Poner en curso: `choques N` | Siempre |
| Poner en curso: rama y subagente | Siempre |
| Documento compartido: paso en su tarea «Actualizar» | Criterio (detectarlo); siempre (lo demás) |
| Todo lo hecho como paso; infinitivo y participio | Criterio |
| Tareas de definición, dejar madurar | Criterio |
| Mejorar la skill que se usa es un paso | Criterio |
| `/paso`, a su subagente | Siempre |
| Lanzar con «Tarea NN: …»; un subagente vivo por tarea | Siempre |
| Compartir archivos no frena; TURBO: cuáles no necesitan al propietario | Criterio |
| Todo el trabajo, al subagente; el principal solo cola y decisiones | Siempre (la vigilancia) |
| El encargo lleva su lista fija | Siempre |
| Al volver: revisar el diff | Criterio |
| Al volver: `merge --ff-only`, `informe`, marcar pasos | Siempre |
| `listo --prueba` con el último paso hecho | Siempre (el aviso); criterio (qué mirar) |
| Proponer probar o cerrar directamente | Criterio |
| Cierre, Testing, probada, descartar y publicar esperan el OK | Siempre (la vigilancia) |
| Al cerrar, detener el subagente | Siempre (ya hecho: 228 y 246) |
| Reabrir limpia; con rama no vuelve a la cola | Siempre (ya en `cola.py`, 246) |
| «Probada» sin número, la de la rama activa | Siempre |
| Preguntar por las de Testing antes de pasar a otra | Siempre (el aviso); criterio (el momento) |
| Lo comprobado, a `comprobado` | Criterio |
| Un cierre que falla llega del panel | Siempre (ya hecho) |
| Sugerir `/fusionar` y `/split`; título desfasado | Criterio |
| Tras una fusión, proponer `/redescribir` | Siempre |
| `/redescribir`: redactar y guardar con el OK | Criterio (ya lo prepara el mod) |
| Dos «Actualizar» del mismo documento, se fusionan; de una en una | Siempre |
| Preguntar con la herramienta; no preguntar lo dicho | Criterio |
| Decisión: archivo, índice y a `develop` | Siempre (la mecánica); criterio (el texto) |
| Cómo escribir | Criterio |

**Resultado:** 40 reglas; 16 de criterio y 24 de siempre o con parte de siempre. De estas, 3 ya las hace el código.

## Propuestas para pasar a código

Ordenadas por beneficio y coste. **Coste:** bajo, unas horas con pruebas; medio, un día; alto, más. Los ganchos citados existen ya en `plugins/sf/hooks/register.tsx`.

1. **Cargar la skill al empezar y tras compactar.** Mod, `classic.SessionStart` con `source` startup, clear o compact: añade al contexto el texto de `sf:orquestacion`, o la orden de cargarla. La 211 ya comprobó que se puede. Beneficio muy alto: sin ella, ninguna otra regla se aplica. Coste bajo. Depende de la decisión pendiente de la 211 (paso 3).
2. **Aviso de subagentes por lanzar o por recoger.** Mod, en `prompt.submit` y `turn.complete`: «La NN está en curso sin subagente: lánzalo» y «El subagente de la NN ha terminado: recógelo». El panel ya sabe qué subagentes viven (rueda verde y roja, 162). Beneficio alto: «lanzar al acabar el turno» y «recoger en cuanto vuelve» son los olvidos más caros. Coste bajo.
3. **El encargo, generado.** `cola.py encargo N` imprime el bloque fijo: worktree, `sub-NN`, no escribir la cola, no cargar `sf:orquestacion`, no tocar documentos compartidos, «Cómo escribir», commits con «(NN)» y formato del informe. O el mod lo añade en `agent.spawn` si la descripción empieza por «Tarea NN». Beneficio alto: hoy cada encargo se redacta y se olvidan piezas. Coste bajo.
4. **Poner en curso en una orden.** `cola.py en-curso N --rama nombre`: pasa `choques` y se para si los hay (salvo `--con-choques`), crea la rama sin activar, el worktree y `sub-NN`, y anota el subagente. Al principal solo le queda lanzar el Agent con el encargo de la propuesta 3. Beneficio alto: hoy son cuatro órdenes y fallan por la ruta o la rama activa. Coste medio.
5. **Recoger en una orden.** `cola.py recoger N --terminado "texto"`: `merge --ff-only` de `sub-NN` en la rama de la tarea sin activarla, e `informe`. Revisar el diff y marcar pasos siguen en Claude. Beneficio alto. Coste medio.
6. **Guardia de escritura del principal.** Mod, `tool.call` de Write y Edit sin `agentId`: si no hay tarea en curso, o la tarea tiene subagente, avisa o bloquea con el motivo. Se libran `.sf/` y `docs/decisiones/`. Cubre «sin tarea no se trabaja» y «todo el trabajo, al subagente», la regla más incumplida (215). Beneficio alto. Coste medio; riesgo de falsos bloqueos con «instrucción expresa del propietario». Empezar como aviso, no como bloqueo.
7. **Documentos compartidos.** `cola.py crear` rechaza una segunda «Actualizar X» y propone `paso añadir`; `en-curso` rechaza una segunda «Actualizar» en curso. El mod bloquea escribir esos documentos desde un worktree cuya tarea no es su «Actualizar». Beneficio medio-alto. Coste bajo para `cola.py`, medio para el mod.
8. **Decisiones a `develop` sin cambiar de rama.** `decision.py "título"`: crea el archivo con su plantilla, regenera el índice y hace el commit en `develop` desde un worktree propio. Además, el mod regenera el índice tras escribir en `docs/decisiones/`. Beneficio medio: hoy obliga a cambiar de rama o a tocar la de otra tarea. Coste medio.
9. **Detalles de coste muy bajo.** Cada uno, una línea en el mod o en `cola.py`:
   - `/paso` responde «pásalo al subagente de la NN» con su worktree.
   - El aviso de una fusión añade «propón `/redescribir` la NN».
   - `probada` sin número toma la tarea de la rama activa.
   - `paso marcar` avisa cuando solo quedan los pasos de cierre: «falta `listo --prueba`».
   - `en-curso` recuerda las tareas en Testing sin preguntar.
   - `agent.spawn` avisa si la descripción no empieza por «Tarea NN» (sin ella no sale la rueda) o si la tarea ya tiene subagente vivo («usa SendMessage»).
   - El control de escrituras bloquea `~/.claude` salvo con confirmación.

   Beneficio bajo o medio cada uno; juntos quitan una decena de líneas de la skill.
10. **No recomendado: pedir permiso para cerrar.** Una regla `ask` sobre `cola.py cerrar|a-testing|probada|descartar` duplica el OK que ya se da en el chat. Beneficio bajo y molestia diaria.

**Al pasar cada una a código**, la regla sale de la skill o se queda en una línea que remite al aviso. Ejemplo ya hecho: con la 246, «Al cerrar» pide solo detener el subagente.

## Para decidir

- ¿Qué propuestas se convierten en tareas y en qué orden? La recomendación: 1, 2 y 3 juntas, después 4 y 5.
- La 1 necesita antes el paso 3 de la 211: cómo se cargan las reglas.
- La 6: ¿aviso o bloqueo?
- ¿Se hace ya la 208, que resuelve seis de los diez hallazgos sin resolver?
