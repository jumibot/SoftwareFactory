# Modo prueba en el panel

- **Origen:** SoftwareFactory, 2026-10-28. Para ver un formato del panel había que publicar y actualizar el plugin. El propietario: «podemos crear un "Modo Prueba" y que se active con una etiqueta en el propio panel?»; «al entrar en una sesión el modo prueba quiero que siempre este desactivado»; «El modo prueba del panel solo en sf»; y, al probarlo: «el comando reload no se puede lanzar desde el panel?».
- **Opciones:** `--plugin-dir` al arrancar (no se activa desde el panel); la variable `CLAUDE_CODE_PLUGIN_DIRS` en los ajustes del proyecto (probada: no carga la copia de trabajo); un catálogo local que enlace a `plugins/sf` (Claude Code no acepta enlaces); un catálogo local en la carpeta de arriba, `D:/Projectes` (probado: funciona y recoge los retoques con `/reload-plugins`).
- **Decisión:** catálogo local `softwarefactory-dev` en `D:/Projectes`. En la SF, la etiqueta «prueba»/**PRUEBA** del panel cambia en `.claude/settings.local.json` qué plugin usa este proyecto y lanza `/reload-plugins`. Siempre desactivado al entrar y al cerrar la sesión.
- **Consecuencias:** los cambios del panel se prueban antes de publicar y se agrupan en un commit. Hay que preparar el catálogo local una vez por equipo.
- **Aplicada en:** mod de estado; `docs/como-funciona-la-software-factory.md` (Publicación del plugin); plugin `sf` 0.31.0.
