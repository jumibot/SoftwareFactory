"""Índice de las decisiones de un proyecto: un archivo por decisión en sf/decisiones/.

Las decisiones van siempre en sf/decisiones/ («Las decisiones son material de la SF:
siempre en sf/decisiones/», 208). Sin carpeta, se usa sf/decisiones/ o, si solo
existe docs/decisiones/ (el sitio de antes, mientras el proyecto no se ha puesto
al día), esa.

Uso:
  python -I -X utf8 indice_decisiones.py [sf/decisiones]
      Regenera sf/decisiones/README.md: conserva lo que hay antes de «## Índice»
      y rehace la tabla Nº | Fecha | Decisión, la más reciente (el número más alto) arriba.
  python -I -X utf8 indice_decisiones.py sf/decisiones --html
      Genera sf/decisiones/README.html a partir del README.md, sin tocarlo, con el
      generador y el aspecto de los demás documentos .html de la SF (skill
      documento_vision). No se versiona: lo genera el panel al abrir las decisiones
      (decisión 163). Sale con 1 si no puede (falta el generador o sus paquetes,
      markdown y Pillow, o el README.md).
  python -I -X utf8 indice_decisiones.py sf/decisiones --nombre "Título" [--fecha AAAA-MM-DD]
      Dice el nombre del archivo de una decisión nueva, con el siguiente número.
  python -I -X utf8 indice_decisiones.py sf/decisiones --migrar docs/decisiones.md
      Parte el registro antiguo (una sección «### Título» por decisión) en un
      archivo por decisión, borra el antiguo y genera el índice. Los enlaces
      relativos se rehacen desde la carpeta nueva.

Cada archivo se llama NNN-AAAA-MM-DD-titulo.md (número de orden total, fecha del
origen, título sin tildes ni signos) y empieza por «# Título». Una línea
«**Sustituida…**» bajo el título la marca como sustituida en el índice.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

INDICE = '## Índice'
INTRO = """# Decisiones

Decisiones tomadas por el propietario, con su porqué.

**Cómo se registra una decisión.** Un archivo por decisión en esta carpeta, `NNN-AAAA-MM-DD-titulo.md`: el número de orden total (el siguiente al más alto), la fecha del origen y el título sin tildes ni signos. Se registra con `cola.py decision "Título" --archivo RUTA` (`tools/` del plugin `sf`), que da el número y el nombre, rehace el índice y hace el commit en `develop` sin cambiar la rama activa. Empieza por `# Título` y lleva:

- **Origen:** proyecto, fecha y palabras del propietario cuando las hay.
- **Contexto:** el problema.
- **Opciones:** las que se valoraron, si las hubo.
- **Decisión:** lo decidido y por qué.
- **Consecuencias:** lo que cambia y lo que queda pendiente.
- **Aplicada en:** los documentos, skills o piezas que la recogen.

Si una decisión cambia otra anterior, la nueva lo dice («Sustituye a…») y la antigua se marca, sin borrarla, con una línea bajo el título: «**Sustituida** el AAAA-MM-DD por «…»» (o **Sustituida en parte**).

Este índice no se escribe a mano: se regenera con `python -I -X utf8 tools/indice_decisiones.py sf/decisiones` (`tools/` del plugin `sf`) al añadir una decisión y al juntar ramas. Lo que hay antes de «Índice» se conserva.
"""
NOMBRE = re.compile(r'^(\d+)-(\d{4}-\d{2}-\d{2})-.+\.md$')
SUSTITUIDA = re.compile(r'^(?:> )?\*\*(Sustituida(?: en parte)?)\*\*', re.M)


def kebab(titulo: str) -> str:
    s = unicodedata.normalize('NFKD', titulo)
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-') or 'decision'


def ancla(titulo: str) -> str:
    """Ancla de un título como la calcula GitHub."""
    s = re.sub(r'[^\w\- ]', '', titulo.lower())
    return s.replace(' ', '-')


def leer(ruta: Path) -> tuple[str, str]:
    crudo = ruta.read_bytes().decode('utf-8')
    return crudo.replace('\r\n', '\n'), '\r\n' if '\r\n' in crudo else '\n'


def escribir(ruta: Path, texto: str, nl: str) -> None:
    ruta.write_bytes(texto.replace('\n', nl).encode('utf-8'))


def titulo_de(texto: str) -> str:
    m = re.search(r'^# (.+)$', texto, re.M)
    return m.group(1).strip() if m else ''


def indice(readme: str | None, decisiones) -> tuple[str, int]:
    """El README.md con la tabla rehecha, con fines de línea «\\n», y cuántas decisiones lleva. `readme`: el texto de
    antes, o None; `decisiones`: pares (nombre del archivo, texto). Lo usa también «cola.py decision», que lo calcula
    sobre develop sin tocar la copia de trabajo."""
    intro = INTRO
    if readme is not None and INDICE in readme:
        intro = readme.replace('\r\n', '\n').split(INDICE)[0].rstrip() + '\n'
    filas = []
    for nombre, texto in decisiones:
        m = NOMBRE.match(nombre)
        if not m:
            continue
        texto = texto.replace('\r\n', '\n')
        t = titulo_de(texto) or nombre[:-3]
        s = SUSTITUIDA.search(texto)
        filas.append((int(m.group(1)), m.group(2), t, nombre, s.group(1).lower() if s else ''))
    # La más reciente, el número más alto, arriba.
    filas.sort(key=lambda x: (x[0], x[3]), reverse=True)
    lineas = [intro, INDICE, '', '| Nº | Fecha | Decisión |', '| --- | --- | --- |']
    for num, fecha, t, nombre, sust in filas:
        marca = f' ({sust})' if sust else ''
        lineas.append(f"| {num} | {fecha} | [{t.replace('|', chr(92) + '|')}]({nombre}){marca} |")
    return '\n'.join(lineas) + '\n', len(filas)


def generar(carpeta: Path) -> int:
    readme = carpeta / 'README.md'
    texto, nl = leer(readme) if readme.exists() else (None, '\n')
    decisiones = [(f.name, leer(f)[0]) for f in carpeta.iterdir() if f.is_file() and NOMBRE.match(f.name)]
    nuevo, n = indice(texto, decisiones)
    escribir(readme, nuevo, nl)
    return n


# El generador de los documentos .html de la SF, en el mismo plugin: tools/ y skills/ viajan juntos.
GENERADOR = Path(__file__).resolve().parent.parent / 'skills' / 'documento_vision' / 'scripts' / 'doc_to_html.py'


def generar_html(carpeta: Path) -> str:
    """README.html junto al README.md, como los demás documentos .html de la SF. Devuelve lo que pasó."""
    readme = carpeta / 'README.md'
    if not readme.is_file():
        return f'sin README.html: no está {readme}'
    if not GENERADOR.is_file():
        return f'sin README.html: no está el generador {GENERADOR}'
    r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(GENERADOR), str(readme), '--tipo', 'Índice',
                        # Un índice generado por comando: se elige aquí, a la vista, y no en el generador.
                        '--destino', 'proyecto', '--herramientas', 'recomendadas'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    html = carpeta / 'README.html'
    if r.returncode != 0 or not html.is_file():
        error = (r.stderr.strip() or r.stdout.strip()).splitlines()
        return f'sin README.html: {error[-1] if error else "el generador falló"}'
    # En un índice, todas las secciones abiertas, como en el README.html de la SF.
    texto = html.read_text(encoding='utf-8')
    html.write_text(re.sub(r'(<details id="[^"]*" class="bloque[^"]*")(?! open)>', r'\1 open>', texto), encoding='utf-8')
    return str(html)


def siguiente(carpeta: Path) -> int:
    nums = [int(m.group(1)) for f in carpeta.glob('*.md') if (m := NOMBRE.match(f.name))] if carpeta.exists() else []
    return max(nums, default=0) + 1


def reubicar(enlace: str, origen: Path, carpeta: Path) -> str:
    """Un enlace relativo del registro antiguo (en la carpeta de `origen`), visto desde `carpeta`."""
    if re.match(r'^(?:[a-z]+:|#|/)', enlace):
        return enlace
    ruta, almohadilla, ancla_ = enlace.partition('#')
    nuevo = os.path.relpath(os.path.join(os.path.abspath(origen.parent), ruta), os.path.abspath(carpeta))
    return nuevo.replace(os.sep, '/') + almohadilla + ancla_


def migrar(carpeta: Path, origen: Path) -> int:
    texto, nl = leer(origen)
    partes = re.split(r'^### ', texto, flags=re.M)[1:]
    if not partes:
        sys.exit(f'{origen}: no hay secciones «### Título».')
    fechas_indice = dict(
        (t, d) for d, t in re.findall(r'^\| (\d{4}-\d{2}-\d{2}) \| \[(.+?)\]\(#', texto, re.M))
    decisiones = []
    # El registro antiguo lleva la más reciente arriba: se numera desde abajo.
    num = siguiente(carpeta) + len(partes) - 1
    for parte in partes:
        titulo, _, cuerpo = parte.partition('\n')
        titulo = titulo.strip()
        # Fuera las líneas en blanco y los separadores «---» del final.
        cuerpo = re.sub(r'(?:\n[ \t]*(?:---)?[ \t]*)+$', '', '\n' + cuerpo).strip('\n')
        m = re.search(r'\*\*Origen:\*\*[^\n]*?(\d{4}-\d{2}-\d{2})', cuerpo)
        fecha = m.group(1) if m else fechas_indice.get(titulo)
        if not fecha:
            sys.exit(f'«{titulo}»: sin fecha en el origen ni en el índice.')
        nombre = f'{num:03d}-{fecha}-{kebab(titulo)}.md'
        num -= 1
        decisiones.append((titulo, nombre, cuerpo))
    anclas = {ancla(t): nombre for t, nombre, _ in decisiones}

    def enlace(m: re.Match) -> str:
        destino = m.group(2)
        if destino.startswith('#'):
            destino = anclas.get(destino[1:], destino)
        else:
            destino = reubicar(destino, origen, carpeta)
        return f'{m.group(1)}({destino})'

    carpeta.mkdir(parents=True, exist_ok=True)
    for titulo, nombre, cuerpo in decisiones:
        cuerpo = re.sub(r'(\])\(([^)\s]+)\)', enlace, cuerpo)
        escribir(carpeta / nombre, f'# {titulo}\n\n{cuerpo}\n', nl)
    readme = carpeta / 'README.md'
    if not readme.exists():
        escribir(readme, INTRO, nl)
    origen.unlink()
    return len(decisiones)


CARPETA = Path('sf/decisiones')
CARPETA_ANTES = Path('docs/decisiones')


def carpeta_por_defecto() -> Path:
    """sf/decisiones; docs/decisiones si solo existe esa (proyecto sin poner al día, decisión 208)."""
    return CARPETA_ANTES if not CARPETA.is_dir() and CARPETA_ANTES.is_dir() else CARPETA


def main() -> None:
    p = argparse.ArgumentParser(description='Índice de sf/decisiones/, un archivo por decisión.')
    p.add_argument('carpeta', type=Path, nargs='?',
                   help='la carpeta de las decisiones; sin ella, sf/decisiones (o docs/decisiones, la de antes)')
    p.add_argument('--migrar', type=Path, metavar='DECISIONES_MD',
                   help='parte el registro antiguo en un archivo por decisión y lo borra')
    p.add_argument('--nombre', metavar='TITULO', help='dice el nombre del archivo de una decisión nueva')
    p.add_argument('--fecha', metavar='AAAA-MM-DD', help='con --nombre, la fecha del origen (hoy, si falta)')
    p.add_argument('--html', action='store_true', help='genera README.html a partir del README.md, sin tocarlo')
    a = p.parse_args()
    a.carpeta = a.carpeta or carpeta_por_defecto()
    if a.html:
        hecho = generar_html(a.carpeta)
        print(hecho)
        sys.exit(1 if hecho.startswith('sin README.html') else 0)
    if a.nombre:
        import datetime
        fecha = a.fecha or datetime.date.today().isoformat()
        print(a.carpeta / f'{siguiente(a.carpeta):03d}-{fecha}-{kebab(a.nombre)}.md')
        return
    if a.migrar:
        print(f'{migrar(a.carpeta, a.migrar)} decisiones migradas a {a.carpeta}')
    a.carpeta.mkdir(parents=True, exist_ok=True)
    print(f'{generar(a.carpeta)} decisiones en {a.carpeta / "README.md"}')


if __name__ == '__main__':
    main()
