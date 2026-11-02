# La tarea que se prueba es la de la rama activa

- **Origen:** SoftwareFactory, 2026-10-29, tras cerrar la 100. El propietario: «regla: la tarea que se prueba si no se especifica lo contrario es la de la rama activa. En caso de duda preguntar».
- **Contexto:** con la P se cambia de rama al momento, y un «probada» sin número podía referirse a la tarea de la rama activa o a la última de la que se habló.
- **Decisión:** un OK de prueba sin número («probada», «ok») es para la tarea de la rama activa. Si hay duda (la rama activa no es de ninguna tarea, o el contexto apunta a otra), Claude pregunta antes de cerrar.
- **Aplicada en:** metodología, 2 («Cola de peticiones»); plantilla `claude-sf.md`; `CLAUDE.md`.
