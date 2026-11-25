# El principal orquesta y lanza cada subagente sin preguntar

El agente principal es el orquestador del desarrollo: habla con el propietario, define y decide con él, lleva la cola y lanza y sigue los subagentes. Qué trabajo hace cada subagente, en «Un subagente vivo por tarea en curso, en su rama auxiliar» (375) y «Todo el trabajo de la tarea, a su subagente» (151).

Solo el principal escribe la cola. Antes de anotar lo que trae un subagente, revisa sus cambios en la rama (el diff y, si se puede, la comprobación). El encargo prohíbe al subagente escribir la cola.

El subagente informa con un formato fijo, que da su encargo: si ha terminado o se ha interrumpido y qué necesita, lo hecho, lo comprobado y lo pendiente. Antes de parar, hace commit de lo hecho en su rama. Una tarea interrumpida se retoma con el mismo subagente, que conserva su contexto; si no se puede, con uno nuevo en la misma rama, a partir del informe.

El subagente se lanza sin pedir permiso, avisando en una línea. Compartir archivos con otra tarea no es motivo para esperar, salvo alto riesgo de pérdidas: el solape se resuelve al juntar. Sí lo es necesitar el resultado de otra. Al final de cada turno, el principal lanza el de las tareas en curso que aún no lo tienen. Las de la cola, solo cuando se ponen en curso; quién las pone, en «TURBO pone en curso las tareas que no necesitan al propietario» (160).

Recoge lo que sigue valiendo de «El principal orquesta; los subagentes ejecutan» (083), «El subagente se lanza sin preguntar» (086) y «Lanzar sin esperar lo que no necesita al propietario» (105), que quedan deprecadas.

Porqué: «el principal, que pasa a orquestador del desarrollo, que lo gestione» (083). «Que el orquestador no pregunte siempre si lanzar el subagente» (086). «No entiendo por qué has esperado tanto a lanzar los subagentes si las tareas estaban en curso y no dependían de mí»; «compartir archivos no es motivo para esperar, a no ser que haya alto riesgo de pérdidas por la colisión» (105).

Aplicada en: `sf:orquestacion` («Subagentes») y `references/porque.md`; metodología, «Orquestación con subagentes»; el mod, `control.ts` («El mod impide que un subagente escriba la cola», 110).
