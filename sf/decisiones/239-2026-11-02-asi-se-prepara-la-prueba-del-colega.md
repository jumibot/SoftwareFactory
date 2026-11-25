# Así se prepara la prueba del colega

- **Origen:** SoftwareFactory, 2026-11-02. En «Primeros cinco minutos de un usuario nuevo con la SF» (289), el diagnóstico de lo que atasca a un usuario nuevo dejó decisiones para el propietario, que eligió la opción recomendada.
- **Contexto:** antes de que un colega pruebe la SF hay que resolver el acceso al plugin (el repositorio es privado), la metodología que aún contradice «Sin registro ni mejoras de la SF desde otros proyectos» (194), cómo recorrer la instalación como usuario nuevo y dónde hace su primera tarea.
- **Decisión:**
  - Acceso: se invita al colega al repositorio de la SF en GitHub. No se hace público por ahora; ya necesita GitHub y `gh` («Sin remoto en GitHub no hay SF», 230).
  - Metodología: la corrección de la 194 se hace antes de la prueba, adelantada de «Actualizar las reglas del método» (208).
  - Recorrido: el propietario inicia sesión una vez en una configuración y un HOME desechables, y Claude recorre la instalación y la incorporación como un usuario nuevo.
  - Primera tarea: en una carpeta vacía, con un repositorio privado nuevo en GitHub que crea la incorporación.
- **Corregida el mismo día:** el propietario: «Prepara para dejar el repo público ya». En lugar de invitar al colega, el repositorio de la SF se hace público, después de revisar secretos, datos privados e historia y de poner licencia («Dejar público el repositorio de la SF», 317). Cambiar la visibilidad necesita su OK.
- **Consecuencias:** la guía de arranque pide cuenta de GitHub, `gh` con la sesión iniciada y aceptar la invitación.
- **Aplicada en:** el repositorio público `jumibot/SoftwareFactory`, con `LICENSE`, `README.md` y `README.es.md`; `plugins/sf/README.md` («Requisitos»); `sf:comprobar_instalacion`; `hooks/lectura.ts` (configuración desechable con `CLAUDE_CONFIG_DIR`); `sf:metodologia` y metodología, «Automejora durante el uso de la SF»; pendiente: recorrer la conversación como usuario nuevo y la primera tarea en una carpeta vacía.
