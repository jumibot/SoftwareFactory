# Cerrar se niega si el subagente tiene trabajo sin traer

- **Origen:** SoftwareFactory, 2026-11-01. Al preguntarle si el panel debía pasar a Claude el trabajo sin traer al cerrar, el propietario eligió «Dejarlo como está».
- **Contexto:** al cerrar una tarea, la rama auxiliar `sub-NN` de su subagente puede tener commits que aún no han entrado en la rama de la tarea. Hoy el cierre se niega en ese caso. Se valoró que el panel se lo pasara a Claude para traerlo, revisarlo y decir si había algo nuevo que probar, como ya hace «Activar rama» (decisión 191), o que se trajera solo y se cerrara.
- **Decisión:** se deja como está. Si la rama auxiliar tiene trabajo sin traer, el cierre se niega y el aviso lo dice. El propietario se lo pide a Claude, que lo trae, lo revisa y, si hace falta, lo prueba antes de volver a cerrar.
- **Consecuencias:** nunca entra en `develop` código que no se haya visto ni probado. A cambio, cerrar exige a veces un paso más, que pide el propietario. No hace falta cambiar nada.
- **Aplicada en:** sin cambios; es el comportamiento actual de `cola.py cerrar` y del panel.
