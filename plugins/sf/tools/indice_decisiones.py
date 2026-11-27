"""Índice de las decisiones de un proyecto: un archivo por decisión en sf/decisiones/, en dos catálogos.

Las decisiones van siempre en sf/decisiones/ («Las decisiones son material de la SF:
siempre en sf/decisiones/», 208). Sin carpeta, se usa sf/decisiones/ o, si solo
existe docs/decisiones/ (el sitio de antes, mientras el proyecto no se ha puesto
al día), esa.

Los catálogos son dos archivos («Vigentes y deprecadas, en dos catálogos distintos con
un punto de entrada común», 389): vigentes.md, las que se aplican, y deprecadas.md, las
superadas, cada una con las que la sustituyen. README.md es el punto de entrada: conserva
lo que hay antes de «## Índice» y debajo enlaza a los dos.

Uso:
  python -I -X utf8 indice_decisiones.py [sf/decisiones]
      Regenera README.md, vigentes.md y deprecadas.md, la más reciente (el número
      más alto) arriba.
  python -I -X utf8 indice_decisiones.py sf/decisiones --html
      Genera README.html, vigentes.html y deprecadas.html, sin tocar los .md, con el
      generador único y el estilo del proyecto, como los demás documentos .html
      (doc_to_html.py de la skill documento_vision), y con los enlaces entre ellos a
      sus .html. Los .md son tablas, que se leen bien en GitHub; los .html salen de
      una variante con los recursos de crear_documentos (tarea 439): el README, con
      una tarjeta por catálogo, y cada catálogo, en fichas con buscador y filtro por
      mes (en las deprecadas, también por cuántas la sustituyen). No se versionan
      (decisión 163). Sale con 1 si no puede (falta el generador o sus paquetes,
      markdown y Pillow, o un .md).
  python -I -X utf8 indice_decisiones.py sf/decisiones --nombre "Título" [--fecha AAAA-MM-DD]
      Dice el nombre del archivo de una decisión nueva, con el siguiente número y la
      fecha de hoy, la del registro; --fecha, solo al pasar decisiones ya registradas
      en otra forma, con la de aquel registro.
  python -I -X utf8 indice_decisiones.py sf/decisiones --migrar docs/decisiones.md
      Parte el registro antiguo (una sección «### Título» por decisión) en un
      archivo por decisión, borra el antiguo y genera el índice. Los enlaces
      relativos se rehacen desde la carpeta nueva.

Cada archivo se llama NNN-AAAA-MM-DD-titulo.md (número de orden total, fecha del
registro, título sin tildes ni signos; «La fecha del nombre de archivo de una decisión
es la de su registro», 390) y empieza por «# Título», con la regla («Las decisiones, en
un solo formato: regla y porqué», 388). Es vigente mientras no lleva estado. La primera
línea bajo el título «Estado: deprecada el AAAA-MM-DD por «…» (NNN)» la lleva a las
deprecadas, y sus «(NNN)» (o sus «…» con el título de otra) dan la columna «Sustituida
por». Las marcas de antes se leen igual: «**Sustituida**» es deprecada, y «**Sustituida
en parte**», vigente con la marca «(sustituida en parte)».
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
README, VIGENTES, DEPRECADAS = 'README.md', 'vigentes.md', 'deprecadas.md'
CATALOGOS = (README, VIGENTES, DEPRECADAS)
INTRO = """# Decisiones

Decisiones tomadas por el propietario, con su porqué.

**Cómo se registra una decisión.** Un archivo por decisión en esta carpeta, `NNN-AAAA-MM-DD-titulo.md`: el número de orden total (el siguiente al más alto), la fecha del registro y el título sin tildes ni signos. Se registra con `cola.py decision "Título" --archivo RUTA` (`tools/` del plugin `sf`), que da el número y el nombre, rehace los catálogos y hace el commit en `develop` sin cambiar la rama activa. La plantilla está en la skill `definicion_tecnica` del plugin (`assets/plantilla-decision.md`). Empieza por `# Título`, que dice la regla decidida y no el tema, y sigue con:

- lo decidido, en párrafos cortos o en lista;
- «Opciones:», solo si hubo alternativas reales;
- si cambia otra, «Sustituye a «Título» (NNN), que queda deprecada» o, si de la otra sigue valiendo algo, «Recoge lo que sigue valiendo de «Título» (NNN), que queda deprecada»;
- «Porqué:», el problema y la razón, con las palabras del propietario cuando las hay;
- «Aplicada en:», dónde se recoge y lo pendiente.

Mientras está vigente no lleva estado. Una decisión superada no se borra ni se reescribe: se depreca entera, con una línea bajo su título, «Estado: deprecada el AAAA-MM-DD por «Título» (NNN)», y lo que siga valiendo va a una decisión nueva, que lo dice.

Los catálogos no se escriben a mano: se regeneran con `python -I -X utf8 tools/indice_decisiones.py sf/decisiones` (`tools/` del plugin `sf`) al añadir una decisión y al juntar ramas. De este archivo se conserva lo que hay antes de «Índice».
"""
NOMBRE = re.compile(r'^(\d+)-(\d{4}-\d{2}-\d{2})-.+\.md$')
# El estado, en la primera línea bajo el título: «Estado: deprecada…» (388) o la marca de antes, «**Sustituida…**».
DEPRECADA = re.compile(r'^(?:> )?(?:\*\*)?Estado:(?:\*\*)? *deprecada\b', re.I)
SUSTITUIDA = re.compile(r'^(?:> )?\*\*(Sustituida(?: en parte)?)\*\*')
# La de la plantilla MADR de antes, en una viñeta antes de la primera sección: «- **Estado:** sustituida por …».
MADR = re.compile(r'^- \*\*Estado:\*\* *sustituida\b', re.I)
NUMERO = re.compile(r'\((\d{1,4})\)')
ENLACE = re.compile(r'\]\(([^)\s]+\.md)\)')


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


def estado(texto: str) -> tuple[str, str]:
    """El estado de una decisión (texto con «\\n») y la línea que lo dice: («vigente», ''), («deprecada», línea) o
    («sustituida en parte», línea), la marca de antes, que sigue en vigentes."""
    lineas = texto.split('\n')
    tras = next((i + 1 for i, x in enumerate(lineas) if x.startswith('# ')), 0)
    # Sin contar un comentario de una línea, como el de la plantilla.
    primera = next((x.strip() for x in lineas[tras:] if x.strip() and not re.match(r'\s*<!--.*-->\s*$', x)), '')
    if DEPRECADA.match(primera):
        return 'deprecada', primera
    s = SUSTITUIDA.match(primera)
    if s:
        return ('deprecada' if s.group(1) == 'Sustituida' else 'sustituida en parte'), primera
    for x in lineas[tras:]:
        if x.startswith('## '):
            break
        if MADR.match(x):
            return 'deprecada', x.strip()
    return 'vigente', ''


def sustituida_por(linea: str, por_numero: dict, por_titulo: dict) -> list[tuple[str, str]]:
    """Las decisiones que cita la línea de estado, en su orden y sin repetir: (título, archivo). Por su «(NNN)»; por
    su enlace, en la plantilla MADR de antes; o, en las marcas de antes sin número, por su «Título» entre comillas."""
    archivos = set(por_numero.values())
    citas = [(m.start(), por_numero.get(int(m.group(1)))) for m in NUMERO.finditer(linea)]
    citas += [(m.start(), Path(m.group(1)).name) for m in ENLACE.finditer(linea)]
    citas += [(i, nombre) for t, nombre in por_titulo.items() if (i := linea.find(f'«{t}»')) >= 0]
    titulos = {v: k for k, v in por_titulo.items()}
    vistos, salida = set(), []
    for _, nombre in sorted((c for c in citas if c[1] in archivos), key=lambda c: c[0]):
        if nombre not in vistos:
            vistos.add(nombre)
            salida.append((titulos[nombre], nombre))
    return salida


def celda(t: str) -> str:
    return t.replace('|', chr(92) + '|')


def filas_de(decisiones) -> list[tuple]:
    """(número, fecha, título, archivo, estado, línea de estado) de cada decisión, la más reciente (el número más
    alto) arriba."""
    filas = []
    for nombre, texto in decisiones:
        m = NOMBRE.match(nombre)
        if not m:
            continue
        texto = texto.replace('\r\n', '\n')
        filas.append((int(m.group(1)), m.group(2), titulo_de(texto) or nombre[:-3], nombre, *estado(texto)))
    filas.sort(key=lambda x: (x[0], x[3]), reverse=True)
    return filas


def intro_de(readme: str | None) -> str:
    """Lo de antes de «## Índice» del README.md o, sin él, la entrada por defecto."""
    if readme is not None and INDICE in readme:
        return readme.replace('\r\n', '\n').split(INDICE)[0].rstrip() + '\n'
    return INTRO


def catalogos(readme: str | None, decisiones) -> dict[str, str]:
    """Los tres archivos del índice, {nombre: texto con fines de línea «\\n»}: README.md (lo de antes de «## Índice»,
    conservado, y los enlaces a los dos catálogos), vigentes.md y deprecadas.md. `readme`: el README.md de antes, o
    None; `decisiones`: pares (nombre del archivo, texto). Lo usa también «cola.py decision», que lo calcula sobre
    develop sin tocar la copia de trabajo."""
    intro = intro_de(readme)
    filas = filas_de(decisiones)
    # Con dos archivos del mismo número (dos ramas), cuenta el primero, el de nombre menor.
    por_numero = {f[0]: f[3] for f in filas}
    por_titulo = {f[2]: f[3] for f in filas}
    vigentes = [f for f in filas if f[4] != 'deprecada']
    deprecadas = [f for f in filas if f[4] == 'deprecada']
    nuevo = '\n'.join([
        intro, INDICE, '',
        f'- [Vigentes]({VIGENTES}): las decisiones que se aplican.',
        f'- [Deprecadas]({DEPRECADAS}): las superadas, con las que las sustituyen.', ''])
    aviso = 'Este catálogo no se escribe a mano: lo regenera `indice_decisiones.py` (`tools/` del plugin `sf`).'
    lv = ['# Decisiones vigentes', '',
          f'Las decisiones que se aplican, la más reciente arriba. Las superadas están en [Decisiones deprecadas]'
          f'({DEPRECADAS}); cómo se registra una decisión, en el [índice]({README}). {aviso}', '']
    if vigentes:
        lv += ['| Nº | Fecha | Decisión |', '| --- | --- | --- |']
        for num, fecha, t, nombre, est, _ in vigentes:
            marca = f' ({est})' if est != 'vigente' else ''
            lv.append(f'| {num} | {fecha} | [{celda(t)}]({nombre}){marca} |')
    else:
        lv.append('Ninguna todavía.')
    ld = ['# Decisiones deprecadas', '',
          f'Las decisiones superadas, la más reciente arriba, con las que las sustituyen. No se borran: guardan por qué '
          f'cambió cada regla. Las que se aplican están en [Decisiones vigentes]({VIGENTES}); cómo se registra una '
          f'decisión, en el [índice]({README}). {aviso}', '']
    if deprecadas:
        ld += ['| Nº | Fecha | Decisión | Sustituida por |', '| --- | --- | --- | --- |']
        for num, fecha, t, nombre, _, linea in deprecadas:
            por = '; '.join(f'[{celda(x)}]({n})' for x, n in sustituida_por(linea, por_numero, por_titulo)) or '—'
            ld.append(f'| {num} | {fecha} | [{celda(t)}]({nombre}) | {por} |')
    else:
        ld.append('Ninguna todavía.')
    return {README: nuevo, VIGENTES: '\n'.join(lv) + '\n', DEPRECADAS: '\n'.join(ld) + '\n'}


def generar(carpeta: Path) -> tuple[int, int]:
    """Escribe los tres archivos del índice, con los fines de línea del README.md que ya hay. Devuelve cuántas
    vigentes y cuántas deprecadas."""
    readme = carpeta / README
    texto, nl = leer(readme) if readme.exists() else (None, '\n')
    decisiones = [(f.name, leer(f)[0]) for f in carpeta.iterdir() if f.is_file() and NOMBRE.match(f.name)]
    for nombre, nuevo in catalogos(texto, decisiones).items():
        escribir(carpeta / nombre, nuevo, nl)
    deprecadas = sum(1 for _, t in decisiones if estado(t)[0] == 'deprecada')
    return len(decisiones) - deprecadas, deprecadas


# El generador único de los documentos .html, con el perfil de la visión (anclas de siempre), en el mismo plugin:
# tools/ y skills/ viajan juntos.
GENERADOR = Path(__file__).resolve().parent.parent / 'skills' / 'documento_vision' / 'scripts' / 'doc_to_html.py'
SIN_HTML = 'sin los .html del índice'
# Los enlaces entre los tres archivos del índice, de .md a .html, para seguir en html al pasar de uno a otro.
ENTRE_CATALOGOS = re.compile(r'href="(' + '|'.join(re.escape(x[:-3]) for x in CATALOGOS) + r')\.md(#[^"]*)?"')


MESES = ('enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
         'noviembre', 'diciembre')


def mes(fecha: str) -> str:
    """La etiqueta del filtro por mes, que se ordena por fecha: «2026-11 · noviembre»."""
    return f'{fecha[:7]} · {MESES[int(fecha[5:7]) - 1]}'


def cuantas(n: int) -> str:
    """La etiqueta del filtro por cuántas sustituyen a una deprecada."""
    return 'Sin sustituta citada' if n == 0 else f'Sustituida por {n}' if n < 3 else 'Sustituida por 3 o más'


def variantes_html(readme: str | None, decisiones) -> dict[str, str]:
    """Las variantes de los tres catálogos para sus .html, {nombre del .md: texto}, con los recursos de
    crear_documentos (tarea 439): el README, con una tarjeta por catálogo; cada catálogo, en fichas con buscador y
    filtro por mes y, en las deprecadas, por cuántas la sustituyen, con su lista «Sustituida por» dentro. Los .md
    siguen en tablas, que GitHub lee bien y estos bloques no."""
    filas = filas_de(decisiones)
    por_numero = {f[0]: f[3] for f in filas}
    por_titulo = {f[2]: f[3] for f in filas}
    numero_de = {f[3]: f[0] for f in filas}
    vigentes = [f for f in filas if f[4] != 'deprecada']
    deprecadas = [f for f in filas if f[4] == 'deprecada']
    aviso = 'Este catálogo no se escribe a mano: lo regenera `indice_decisiones.py` (`tools/` del plugin `sf`).'

    # La entrada: el título y el primer párrafo de su cabecera, las dos tarjetas y, después, el resto de la cabecera.
    intro = intro_de(readme).strip('\n').split('\n')
    i = next((k for k, x in enumerate(intro) if x.startswith('# ')), None)
    titulo = intro[i] if i is not None else '# Decisiones'
    cuerpo = '\n'.join(intro[i + 1:] if i is not None else intro).strip('\n')
    primero, _, resto = cuerpo.partition('\n\n')
    if primero.startswith(('#', '-', '|', '>', '*')):
        primero, resto = '', cuerpo
    ultima = f'la más reciente, la {vigentes[0][0]}, del {vigentes[0][1]}' if vigentes else 'ninguna todavía'
    entrada = [titulo, '', primero, '', '## Catálogos {#catalogos}', '',
               f'{len(vigentes)} decisiones vigentes ({ultima}) y {len(deprecadas)} deprecadas, cada grupo en su '
               f'catálogo, con buscador.', '',
               '::: tarjetas 2', '',
               '### Vigentes {color=correcto icono=check}', '',
               f'**{len(vigentes)}** decisiones', '{: .metrica}', '',
               'Las que se aplican, la más reciente arriba.', '',
               f'[Ver las vigentes]({VIGENTES}){{: .salto}}', '',
               '### Deprecadas {color=aviso icono=documento}', '',
               f'**{len(deprecadas)}** decisiones', '{: .metrica}', '',
               'Las superadas, cada una con las que la sustituyen.', '',
               f'[Ver las deprecadas]({DEPRECADAS}){{: .salto}}', '', ':::', '']
    if resto.strip():
        if not resto.lstrip().startswith('## '):
            entrada += ['## Cómo se llevan {#registro}', '']
        entrada += [resto.strip('\n'), '']

    def ficha(num, fecha, t, nombre, filtros, campos=()):
        # La fecha, en una insignia que no se parte, con las etiquetas del filtro; el título, enlazado a su archivo.
        return [f'### {num} · [{t}]({nombre}) {{: #d{num}}}', '',
                f'[{fecha}](#d{num}){{: .insignia data-filtro="{"; ".join(filtros)}"}}', '', *campos]

    lv = ['# Decisiones vigentes', '', '## Vigentes | Las que se aplican {#vigentes}', '',
          f'{len(vigentes)} decisiones, la más reciente arriba. Se buscan por número, título o fecha, y se filtran '
          f'por mes. Las superadas están en [Decisiones deprecadas]({DEPRECADAS}); cómo se registra una decisión, en '
          f'el [índice]({README}).', '', aviso, '{: .nota}', '']
    if vigentes:
        lv += ['::: fichas 2', '']
        for num, fecha, t, nombre, est, _ in vigentes:
            parte = est != 'vigente'
            lv += ficha(num, fecha, t, nombre, [mes(fecha)] + (['Sustituida en parte'] if parte else []),
                        ['Estado', ':   sustituida en parte', ''] if parte else [])
        lv += [':::', '']
    else:
        lv += ['Ninguna todavía.', '']
    ld = ['# Decisiones deprecadas', '', '## Deprecadas | Las superadas {#deprecadas}', '',
          f'{len(deprecadas)} decisiones superadas, la más reciente arriba, cada una con las que la sustituyen. No se '
          f'borran: guardan por qué cambió cada regla. Se buscan por número, título o fecha, y se filtran por mes o '
          f'por cuántas la sustituyen. Las que se aplican están en [Decisiones vigentes]({VIGENTES}); cómo se '
          f'registra una decisión, en el [índice]({README}).', '', aviso, '{: .nota}', '']
    if deprecadas:
        ld += ['::: fichas 2', '']
        for num, fecha, t, nombre, _, linea in deprecadas:
            por = sustituida_por(linea, por_numero, por_titulo)
            lista = [f'{"    " if k else ":   "}- [{x}]({n}) ({numero_de[n]})' for k, (x, n) in enumerate(por)]
            ld += ficha(num, fecha, t, nombre, [mes(fecha), cuantas(len(por))],
                        ['Sustituida por', *(lista or [':   ninguna citada en su línea de estado']), ''])
        ld += [':::', '']
    else:
        ld += ['Ninguna todavía.', '']
    return {README: '\n'.join(entrada), VIGENTES: '\n'.join(lv), DEPRECADAS: '\n'.join(ld)}


def generar_html(carpeta: Path) -> str:
    """README.html, vigentes.html y deprecadas.html junto a sus .md, como los demás documentos .html de la SF, desde
    sus variantes con recursos (variantes_html). Devuelve sus rutas o, si no puede, por qué, tras SIN_HTML."""
    if not GENERADOR.is_file():
        return f'{SIN_HTML}: no está el generador {GENERADOR}'
    for nombre in CATALOGOS:
        if not (carpeta / nombre).is_file():
            return f'{SIN_HTML}: no está {carpeta / nombre}'
    decisiones = [(f.name, leer(f)[0]) for f in carpeta.iterdir() if f.is_file() and NOMBRE.match(f.name)]
    variantes = variantes_html(leer(carpeta / README)[0], decisiones)
    hechos = []
    for nombre in CATALOGOS:
        # La variante, junto al .md para que valgan sus enlaces y el estilo del proyecto; al terminar, fuera.
        md = carpeta / f'.{nombre[:-3]}.variante.md'
        html = carpeta / f'{nombre[:-3]}.html'
        md.write_text(variantes[nombre], encoding='utf-8')
        try:
            r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(GENERADOR), str(md), '--tipo', 'Índice',
                                # Un índice generado por comando: se elige aquí, a la vista, y no en el generador.
                                '--destino', 'proyecto', '--herramientas', 'recomendadas'],
                               capture_output=True, text=True, encoding='utf-8', errors='replace')
            salida = md.with_suffix('.html')
            if r.returncode != 0 or not salida.is_file():
                error = (r.stderr.strip() or r.stdout.strip()).splitlines()
                return f'{SIN_HTML}: {error[-1] if error else "el generador falló"}'
            salida.replace(html)
        finally:
            md.unlink(missing_ok=True)
            md.with_suffix('.html').unlink(missing_ok=True)
        # En un índice, todas las secciones abiertas, como en el README.html de la SF.
        texto = html.read_text(encoding='utf-8')
        texto = re.sub(r'(<details class="seccion[^"]*" id="[^"]*")(?! open)>', r'\1 open>', texto)
        html.write_text(ENTRE_CATALOGOS.sub(lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', texto),
                        encoding='utf-8')
        hechos.append(str(html))
    return ', '.join(hechos)


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
    readme = carpeta / README
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
    p = argparse.ArgumentParser(description='Índice de sf/decisiones/, un archivo por decisión, en dos catálogos.')
    p.add_argument('carpeta', type=Path, nargs='?',
                   help='la carpeta de las decisiones; sin ella, sf/decisiones (o docs/decisiones, la de antes)')
    p.add_argument('--migrar', type=Path, metavar='DECISIONES_MD',
                   help='parte el registro antiguo en un archivo por decisión y lo borra')
    p.add_argument('--nombre', metavar='TITULO', help='dice el nombre del archivo de una decisión nueva')
    p.add_argument('--fecha', metavar='AAAA-MM-DD', help='con --nombre, la fecha del registro: hoy, si falta; al pasar decisiones '
                        'ya registradas en otra forma, la de aquel registro')
    p.add_argument('--html', action='store_true', help='genera los .html del índice a partir de sus .md, sin tocarlos')
    a = p.parse_args()
    a.carpeta = a.carpeta or carpeta_por_defecto()
    if a.html:
        hecho = generar_html(a.carpeta)
        print(hecho)
        sys.exit(1 if hecho.startswith(SIN_HTML) else 0)
    if a.nombre:
        import datetime
        fecha = a.fecha or datetime.date.today().isoformat()
        print(a.carpeta / f'{siguiente(a.carpeta):03d}-{fecha}-{kebab(a.nombre)}.md')
        return
    if a.migrar:
        print(f'{migrar(a.carpeta, a.migrar)} decisiones migradas a {a.carpeta}')
    a.carpeta.mkdir(parents=True, exist_ok=True)
    vigentes, deprecadas = generar(a.carpeta)
    print(f'{vigentes} vigentes y {deprecadas} deprecadas en {a.carpeta / VIGENTES} y {a.carpeta / DEPRECADAS}, '
          f'con su entrada en {a.carpeta / README}')


if __name__ == '__main__':
    main()
