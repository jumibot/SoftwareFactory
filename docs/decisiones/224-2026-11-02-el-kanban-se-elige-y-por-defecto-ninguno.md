# El kanban se elige, y por defecto ninguno

- **Origen:** SoftwareFactory, 2026-11-02. En «Configuración inicial: decidir el mínimo, los commits y la versión, y diseñar .sf/proyecto.json y las preguntas» (263) se preguntó si el kanban es obligatorio. El propietario eligió que se elija, con ninguno por defecto, y añadió: «tengo previsto poder escoger el kanban de GitHub».
- **Contexto:** la incorporación pedía siempre el proyecto de JKanban y lo exigía en `.sf/proyecto.json`. JKanban no está conectado, y un usuario nuevo no lo tiene («Primeros cinco minutos de un usuario nuevo con la SF», 289).
- **Decisión:** el kanban es opcional y se elige al incorporar. Por defecto, ninguno: el proyecto funciona solo con su cola. La configuración guarda qué kanban usa (por ahora JKanban) y su proyecto en él, pensada para que más adelante se pueda elegir también el de GitHub (GitHub Projects).
- **Consecuencias:** `kanban` deja de ser obligatorio en `.sf/proyecto.json`, y el panel y el diagnóstico no fallan sin él. El campo de la configuración nombra el proveedor además del proyecto, para que añadir GitHub sea un valor más y no un cambio de formato. Soportar el kanban de GitHub es una tarea aparte, más adelante.
- **Aplicada en:** pendiente; en la 263 (el diseño) y en «Implementar la configuración inicial» (193).
