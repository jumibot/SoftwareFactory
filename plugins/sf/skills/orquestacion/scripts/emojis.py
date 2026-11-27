"""Genera el catálogo de emojis (assets/emojis.html) a partir de la lista oficial de Unicode.

Uso:
  python -I -X utf8 emojis.py [ORIGEN] [DESTINO]

ORIGEN es la ruta o la URL de emoji-test.txt (por defecto, assets/emoji-test.txt, la copia guardada, que permite
regenerar sin red; la última, en https://unicode.org/Public/emoji/latest/emoji-test.txt). DESTINO es el HTML
(por defecto, assets/emojis.html). Escribe el número de emojis y sale con 1 si no encuentra ninguno.

La página lleva los emojis totalmente cualificados, sin el grupo Component, por grupo (nombres en español) y
subgrupo, en rejilla de 50 por fila; el nombre en inglés sale al pasar el ratón. Arriba, fijos: un buscador por
nombre, una casilla para ocultar los tonos de piel y el aviso de que al pulsar un emoji se copia. Sigue el tema
claro u oscuro del sistema. Sin dependencias.
"""
from __future__ import annotations

import html
import re
import sys
import urllib.request
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets'

GRUPOS = {
    'Smileys & Emotion': 'Caras y emociones', 'People & Body': 'Personas y cuerpo',
    'Animals & Nature': 'Animales y naturaleza', 'Food & Drink': 'Comida y bebida',
    'Travel & Places': 'Viajes y lugares', 'Activities': 'Actividades', 'Objects': 'Objetos',
    'Symbols': 'Símbolos', 'Flags': 'Banderas',
}

PLANTILLA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Emojis</title>
<style>
:root{color-scheme:light dark;--fondo:#fafafa;--texto:#222;--tenue:#666;--marca:#ffe680}
@media (prefers-color-scheme:dark){:root{--fondo:#1c1c1e;--texto:#eee;--tenue:#aaa;--marca:#5a4a00}}
body{font-family:system-ui,sans-serif;margin:16px;background:var(--fondo);color:var(--texto)}
h2{margin:24px 0 4px}h3{font-size:13px;color:var(--tenue);margin:10px 0 2px;font-weight:500}
.f{display:grid;grid-template-columns:repeat(50,1fr);max-width:1700px}
.f span{font-size:26px;text-align:center;cursor:pointer}.f span:hover{background:var(--marca)}
body.st .t,.oculto{display:none}
.barra{position:sticky;top:0;background:var(--fondo);padding:6px 0;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
input[type=search]{font:inherit;padding:4px 8px;min-width:16em}
#aviso{color:var(--tenue)}
</style></head><body>
<div class="barra">
<input type="search" id="q" placeholder="Buscar por nombre (en inglés)" aria-label="Buscar por nombre">
<label><input type="checkbox" id="st"> Ocultar variantes de tono de piel</label>
<span id="aviso">Pulsa un emoji para copiarlo.</span>
</div>
<p>%(total)d emojis, lista oficial de Unicode. Pasa el ratón para ver el nombre.</p>
%(cuerpo)s
<script>
const q=document.getElementById('q'),aviso=document.getElementById('aviso');
document.getElementById('st').onchange=e=>document.body.classList.toggle('st',e.target.checked);
q.oninput=()=>{const t=q.value.trim().toLowerCase();
 document.querySelectorAll('.f span').forEach(s=>s.classList.toggle('oculto',!!t&&!s.title.toLowerCase().includes(t)));};
function copiar(t){if(navigator.clipboard)return navigator.clipboard.writeText(t);
 const a=document.createElement('textarea');a.value=t;document.body.append(a);a.select();document.execCommand('copy');a.remove();}
document.addEventListener('click',e=>{const s=e.target.closest('.f span');if(!s)return;
 Promise.resolve(copiar(s.textContent)).then(()=>aviso.textContent='Copiado '+s.textContent+' ('+s.title+')');});
</script></body></html>
"""


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


def generar(texto: str) -> tuple[str, int]:
    datos = analizar(texto)
    partes: list[str] = []
    g0 = s0 = None
    for grupo, subgrupo, emoji, nombre, tono in datos:
        if grupo != g0:
            if g0:
                partes.append('</div>')
            partes.append('<h2>%s</h2>' % GRUPOS.get(grupo, html.escape(grupo)))
            g0, s0 = grupo, None
        if subgrupo != s0:
            if s0:
                partes.append('</div>')
            partes.append('<h3>%s</h3><div class="f">' % html.escape(subgrupo))
            s0 = subgrupo
        partes.append('<span%s title="%s">%s</span>' % (' class="t"' if tono else '', html.escape(nombre), emoji))
    if datos:
        partes.append('</div>')
    return PLANTILLA % {'total': len(datos), 'cuerpo': ''.join(partes)}, len(datos)


def main(argv: list[str]) -> int:
    origen = argv[0] if argv else str(ASSETS / 'emoji-test.txt')
    destino = Path(argv[1]) if len(argv) > 1 else ASSETS / 'emojis.html'
    pagina, total = generar(leer(origen))
    if not total:
        print('No hay emojis en ' + origen, file=sys.stderr)
        return 1
    destino.write_text(pagina, encoding='utf-8')
    print('%d emojis en %s' % (total, destino))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
