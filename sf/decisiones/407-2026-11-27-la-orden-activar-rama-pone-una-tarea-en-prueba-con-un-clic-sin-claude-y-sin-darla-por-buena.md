# La orden Activar rama pone una tarea en prueba con un clic, sin Claude y sin darla por buena

La orden «Activar rama» del menú de una tarea, en cola, en curso o en observación, activa su rama para probarla. Sale si la rama existe y no es la activa; si ya lo es, la cabecera la enseña en dorado. Con un clic y sin confirmar, el panel lo hace con `cola.py probar`, sin pasar por Claude (092):
- antes integra `develop` en la rama; si choca, o si el subagente tiene trabajo sin traer, no la activa y se lo pasa a Claude (191);
- no cambia de rama si la activa tiene cambios sin commit o si la rama está en otro worktree: lo dice y no hace nada;
- una tarea en cola pasa a en curso, y el paso «Activar rama para poder probar» queda hecho (172);
- abre en el navegador los `.html` que la rama cambia respecto a `develop`.

Activar la rama no da la tarea por buena: el OK del propietario es cerrarla. Tampoco recarga el plugin: eso queda a cargo del propietario.

Recoge lo que sigue valiendo de «Botón P para probar una tarea en su rama» (091), «La P no recarga el plugin» (103) y «La P de probar pasa a T, de Test Mode» (122), que quedan deprecadas.

Porqué: probar una tarea en su rama se pedía a Claude, cuando basta un comando (091, 092). El propietario de la Software Factory: «no hagas el reload, queda bajo mi responsabilidad» (103), y sobre el nombre: la P «sugería que pulsarlo daba la tarea por probada, cuando solo la pone en prueba» (122).

Aplicada en: `plugins/sf/hooks/panel.tsx` (`botonProbar`) y `cola.ts` (`probarTarea`, `probable`, `abrirDocumentos`); `plugins/sf/tools/cola.py` (`probar`); sus pruebas.
