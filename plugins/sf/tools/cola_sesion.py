"""Lanzador de la cola para Claude (tarea 252): ejecuta el mismo cola.py que el panel de su sesión.

Al cargar, el panel copia este archivo a ~/.claude/sf/cola.py y el cola.py de su plugin a
~/.claude/sf/cola-<sesión>.py (decisión 136). Claude lanza siempre, en cualquier proyecto y shell:

  python -I -X utf8 "$HOME/.claude/sf/cola.py" <orden> …

y este lanzador pasa la orden a la copia de su sesión (CLAUDE_CODE_SESSION_ID, que Claude Code pone en el entorno de
sus órdenes y hereda cada subagente). Así Claude no usa el cola.py de la copia de trabajo, que cambia con la rama, sino
el del plugin cargado, el mismo que el panel. Sin sesión o sin su copia sale con 2 y dice por qué, sin tocar la cola.

Con CLAUDE_CONFIG_DIR puesta (una configuración de Claude Code aparte, como la de una prueba), el panel deja las
copias en $CLAUDE_CONFIG_DIR/sf y no toca ~/.claude (tarea 269); la orden fija sigue siendo la misma, y el lanzador
busca la copia de la sesión en esa carpeta. Se puede lanzar también el $CLAUDE_CONFIG_DIR/sf/cola.py que deja el panel.
"""
import os
import runpy
import sys
from pathlib import Path


def main() -> None:
    sesion = os.environ.get('CLAUDE_CODE_SESSION_ID', '').strip()
    if not sesion:
        print('cola.py: falta CLAUDE_CODE_SESSION_ID; este lanzador es para las órdenes de Claude Code. '
              'Fuera de Claude, lanza el tools/cola.py del plugin instalado.', file=sys.stderr)
        sys.exit(2)
    config = os.environ.get('CLAUDE_CONFIG_DIR', '').strip()
    carpeta = Path(config) / 'sf' if config else Path(__file__).resolve().parent
    copia = carpeta / f"cola-{''.join(c if c.isalnum() or c in '_-' else '_' for c in sesion)}.py"
    if not copia.is_file():
        print(f'cola.py: no está {copia}, la copia que hace el panel de la SF al cargar. '
              'Con el plugin sf activo, /reload-plugins la vuelve a hacer.', file=sys.stderr)
        sys.exit(2)
    sys.argv[0] = str(copia)
    runpy.run_path(str(copia), run_name='__main__')


if __name__ == '__main__':
    main()
