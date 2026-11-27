"""Genera el catálogo de emojis (assets/emojis.md y assets/emojis.html) a partir de la lista oficial de Unicode.

Uso:
  python -I -X utf8 emojis.py [ORIGEN] [DESTINO.md] [--estilo RUTA]

ORIGEN es la ruta o la URL de emoji-test.txt (por defecto, assets/emoji-test.txt, la copia guardada, que permite
regenerar sin red; la última, en https://unicode.org/Public/emoji/latest/emoji-test.txt). DESTINO es el .md
(por defecto, assets/emojis.md); el HTML sale junto a él. --estilo es el estilo.json del proyecto (por defecto,
el que busca el generador subiendo carpetas desde el .md; en la SF, docs/identidad/estilo.json: pasarlo al
regenerar el que viaja en el plugin). Escribe el número de emojis; sale con 1 si no hay ninguno o si el generador falla.

El .md usa el kit de documentos de la SF (skill crear_documentos): portada sobria, una sección plegable por grupo
(nombres en español) y, dentro, un apartado plegable por subgrupo con los emojis totalmente cualificados (sin el
grupo Component) en rejilla de 50 por fila en pantallas anchas. El HTML sale con documento_a_html.py y el perfil
assets/emojis-perfil.json, con el estilo de la SF en claro y oscuro («Lectura»). assets/emojis.js añade la barra fija
con el buscador por nombre en inglés (abre lo que coincide), la casilla de tonos de piel y el copiado al pulsar, y
el nombre en inglés sale al pasar el ratón. Sin más dependencias que el generador (paquete markdown).
"""
from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
GENERADOR = Path(__file__).resolve().parents[2] / 'crear_documentos' / 'scripts' / 'documento_a_html.py'

GRUPOS = {
    'Smileys & Emotion': 'Caras y emociones', 'People & Body': 'Personas y cuerpo',
    'Animals & Nature': 'Animales y naturaleza', 'Food & Drink': 'Comida y bebida',
    'Travel & Places': 'Viajes y lugares', 'Activities': 'Actividades', 'Objects': 'Objetos',
    'Symbols': 'Símbolos', 'Flags': 'Banderas',
}

def leer(origen: str) -> str:
    if origen.startswith(('http://', 'https://')):
        with urllib.request.urlopen(origen, timeout=30) as r:
            return r.read().decode('utf-8')
    return Path(origen).read_text(encoding='utf-8')


def analizar(texto: str) -> list[tuple[str, str, str, str, bool]]:
    """Los emojis totalmente cualificados, sin el grupo Component: (grupo, subgrupo, emoji, nombre, con_tono)."""
    datos = []
    grupo = subgrupo = ''
    for linea in texto.splitlines():
        m = re.match(r'# group: (.*)', linea)
        if m:
            grupo = m.group(1).strip()
            continue
        m = re.match(r'# subgroup: (.*)', linea)
        if m:
            subgrupo = m.group(1).strip()
            continue
        if '; fully-qualified' in linea and grupo != 'Component':
            emoji, resto = linea.split('#', 1)[1].strip().split(' ', 1)
            nombre = resto.split(' ', 1)[1]  # sin la versión de Unicode («E1.0»)
            datos.append((grupo, subgrupo, emoji, nombre, 'skin tone' in nombre))
    return datos


CABECERA = """---
antetitulo: Software Factory · Catálogo
lema: Todos los emojis, por grupos
subtitulo: Para elegir el que va en cada sitio.
pie: Lista oficial de Unicode (emoji-test.txt). Pulsa un emoji para copiarlo; busca por su nombre en inglés.
destino: usuario
herramientas: lectura
---
# Emojis

> **Cómo usarlo**
> %(total)d emojis totalmente cualificados, de la lista oficial de Unicode. Pasa el ratón para ver el nombre, busca abajo por nombre, oculta los tonos de piel y pulsa uno para copiarlo. Pruébalo en el terminal antes de fijarlo: pinta algunos como texto.

"""


def generar(texto: str) -> tuple[str, int]:
    """El .md del catálogo y el número de emojis."""
    datos = analizar(texto)
    partes: list[str] = []
    g0 = s0 = None
    for grupo, subgrupo, emoji, nombre, tono in datos:
        if grupo != g0:
            if s0:
                partes.append('</div>\n')
            partes.append('\n## %s\n' % GRUPOS.get(grupo, grupo))
            g0, s0 = grupo, None
        if subgrupo != s0:
            if s0:
                partes.append('</div>\n')
            partes.append('\n### %s\n\n<div class="emojis">' % subgrupo.replace('-', ' ').capitalize())
            s0 = subgrupo
        n = html.escape(nombre)
        partes.append('<button type="button"%s title="%s" aria-label="%s">%s</button>'
                      % (' class="tono"' if tono else '', n, n, emoji))
    if datos:
        partes.append('</div>\n')
    return (CABECERA % {'total': len(datos)}) + ''.join(partes), len(datos)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description='Catálogo de emojis (.md y .html) desde emoji-test.txt')
    ap.add_argument('origen', nargs='?', default=str(ASSETS / 'emoji-test.txt'))
    ap.add_argument('destino', nargs='?', default=str(ASSETS / 'emojis.md'))
    ap.add_argument('--estilo', help='estilo.json del proyecto')
    a = ap.parse_args(argv)
    md, total = generar(leer(a.origen))
    if not total:
        print('No hay emojis en ' + a.origen, file=sys.stderr)
        return 1
    destino = Path(a.destino)
    destino.write_text(md, encoding='utf-8')
    orden = [sys.executable, '-I', '-X', 'utf8', str(GENERADOR), '--perfil', str(ASSETS / 'emojis-perfil.json'), str(destino)]
    if a.estilo:
        orden[-1:-1] = ['--estilo', a.estilo]
    r = subprocess.run(orden, capture_output=True, text=True, encoding='utf-8')
    sys.stderr.write(r.stderr)
    if r.returncode:
        sys.stderr.write(r.stdout)
        return 1
    print('%d emojis en %s' % (total, destino.with_suffix('.html')))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
