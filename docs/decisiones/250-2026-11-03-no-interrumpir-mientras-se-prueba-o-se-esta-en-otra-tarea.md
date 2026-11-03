# No interrumpir mientras se prueba o se está en otra tarea

- **Origen:** SoftwareFactory, 2026-11-03. Mientras el propietario probaba «Panel legible en la app de escritorio…» (323), Claude le abrió un menú con dos preguntas de otra tarea («Tareas que crea Claude siempre con descripción…», 326). El propietario lo interrumpió: «estamos probando la 323…», y decidió: «Cuando estamos probando o centrados en otra tarea no me interrumpas. Me avisas en un comentario anexo en tu siguiente respuesta. Si hay rato sin actividad sí que puedes lanzarme un call to action».
- **Contexto:** la orquestación manda llevar al propietario lo que piden los subagentes en cuanto vuelven y preguntar con menús. Un menú corta lo que el propietario esté haciendo, aunque sea de otra tarea.
- **Decisión:** mientras el propietario prueba una tarea o está centrado en otra, Claude no le abre preguntas ni menús de lo demás: lo deja como un comentario anexo, breve, al final de su siguiente respuesta. Solo cuando hay un rato sin actividad, Claude puede lanzarle una llamada a la acción con lo pendiente.
- **Consecuencias:** la regla va a `sf:orquestacion`, que viaja con el plugin (247). Cómo detectar un rato sin actividad y cómo lanzar la llamada a la acción es trabajo de su tarea.
- **Aplicada en:** pendiente; en «No interrumpir al propietario mientras prueba o está en otra tarea».
