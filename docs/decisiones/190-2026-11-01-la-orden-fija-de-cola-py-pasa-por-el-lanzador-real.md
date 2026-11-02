# La orden fija de cola.py pasa por el lanzador real, también con CLAUDE_CONFIG_DIR

- **Origen:** SoftwareFactory, 2026-11-01, tarea «El panel escribe en la carpeta real de Claude Code aunque se le indique otra» (269). El propietario acepta la opción recomendada.
- **Contexto:** con `CLAUDE_CONFIG_DIR`, el panel deja de escribir en `~/.claude/sf` y usa `$CLAUDE_CONFIG_DIR/sf`. Pero la orden fija de Claude (decisión 185), `python -I -X utf8 "$HOME/.claude/sf/cola.py"`, no puede expandir esa variable igual en bash y en PowerShell.
- **Decisión:** la orden fija no cambia. El lanzador real de `~/.claude/sf` solo se lee y se ejecuta, y pasa la orden a la copia de la sesión en `$CLAUDE_CONFIG_DIR/sf`. Hace falta que ese lanzador sea ya de esta versión: se actualiza la primera vez que una sesión normal carga el plugin.
- **Consecuencias:** una prueba con configuración desechable no escribe en `~/.claude`. Hasta que el lanzador real esté al día, la orden sale con error sin tocar la cola. Se descartan dar a Claude otra ruta y escribir el lanzador en `~/.claude` si falta.
- **Aplicada en:** el mod, `cola_sesion.py` y `registro.py` (269); «Cómo funciona el panel», pendiente (198).
