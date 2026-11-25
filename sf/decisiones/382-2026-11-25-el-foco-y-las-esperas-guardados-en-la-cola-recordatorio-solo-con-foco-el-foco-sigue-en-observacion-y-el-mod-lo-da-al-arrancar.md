# El foco y las esperas guardados en la cola: recordatorio solo con foco, el foco sigue en observación y el mod lo da al arrancar

Con el foco y las esperas guardados en la cola (cola.py foco y cola.py espera):

- Sin foco guardado, los avisos del mod van sin recordatorio del foco: la sesión está libre.
- Una tarea que pasa a observación conserva el foco; se va al cerrarla o revertirla, o cuando el propietario cambia de tarea.
- El mod da la línea del foco al empezar la sesión, tras /clear y tras compactar.
- Las esperas antiguas, escritas como paso «Esperar a …», se pasan a dato con cola.py espera.

Porqué: sin foco no hay nada que recordar y una línea fija en cada aviso solo añade ruido; quien prueba una tarea en observación sigue hablando de ella; tras /clear o compactar el principal puede perder cuál era el foco; y una espera solo en texto no la ve el mod, que volvería a pedir el subagente de la tarea que espera. (Tarea 436)
