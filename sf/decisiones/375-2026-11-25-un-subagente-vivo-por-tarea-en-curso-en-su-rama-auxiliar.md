# Un subagente vivo por tarea en curso, en su rama auxiliar

Cada tarea en curso tiene un subagente vivo, al que se le pasa cada encargo del propietario sobre ella, también durante la prueba. Todo cambio de la tarea lo hace él («Todo el trabajo de la tarea, a su subagente», 151).

El subagente trabaja siempre en su rama auxiliar, `sub-NN`. La rama de la tarea queda libre, y Activar rama y Cerrar funcionan sin quitar su worktree. Al cerrar, Claude detiene el subagente; su worktree y su rama auxiliar los recoge `cola.py` («cola.py recoge el subagente al dejar la tarea sin él», 169).

Para que el panel refleje el trabajo:

- Antes de informar o actuar sobre una tarea, el principal mira la cola al día: el propietario la cambia desde el panel, y el mod le trae esos cambios con cada mensaje.
- Recoge el trabajo del subagente y marca sus pasos en cuanto vuelve.
- Con el último paso hecho, `listo --prueba`, sin esperar.
- Al poner una tarea en curso, planifica sus pasos en la cola; lo que falte por concretar va como pasos («Lo que falta por concretar va como pasos de la tarea», 211).
- Sin tarea en curso no se trabaja, salvo para reorganizar la cola (fusionar, separar, redescribir, añadir pasos, cambiar tipos).

Recoge lo que sigue valiendo de «Orquestación con un subagente vivo por tarea» (149), que queda deprecada.

Porqué: los ajustes que pedía el propietario durante la prueba ocupaban al principal: la 196 llevó 12 ajustes en unas 2,5 horas y unos 360.000 tokens. El panel no reflejaba el trabajo: tareas sin pasos, informes sin recoger y la cola desfasada. «Tener subagentes esperando instrucciones y dejando libre el agente principal lo veo una gran ventaja». La C falló en la 194 porque su worktree tenía activa la rama de la tarea.

Aplicada en: `sf:orquestacion` («Con cada mensaje», «Poner en curso», «Subagentes» y «Probar y cerrar») y `references/porque.md`; `sf:flujo_tareas`.
