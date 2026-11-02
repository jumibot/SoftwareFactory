"""Carcasa HTML de los documentos de visión: bloques y subsecciones plegables, cabecera y pie.

La hoja de estilos base está en assets/estilo_base.css. Origen y cambios: docs/referencias/procedencia/ del repositorio de la SF.
"""
import re
from pathlib import Path

CSS_PATH = Path(__file__).resolve().parent.parent / "assets" / "estilo_base.css"

_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_ATX_HEADING_RE = re.compile(r"^#{1,6} ")

def ensure_blank_line_before_headings(text: str) -> str:
    """Inserta una línea en blanco antes de cada heading ATX que no la tenga.

    Respeta los bloques de código cercados (``` o ~~~) — un `#` ahí es contenido
    literal, no un heading. No toca un heading que ya esté precedido por línea en
    blanco ni el que abre el documento. Determinista e idempotente.
    """
    out: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if (not in_fence and _ATX_HEADING_RE.match(line)
                and out and out[-1].strip() != ""):
            out.append("")
        out.append(line)
    return "\n".join(out)


# ── Helpers ───────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[àáâãäå]", "a", text)
    text = re.sub(r"[èéêë]",   "e", text)
    text = re.sub(r"[ìíîï]",   "i", text)
    text = re.sub(r"[òóôõö]",  "o", text)
    text = re.sub(r"[ùúûü]",   "u", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "section"


def add_anchors(html: str) -> tuple[str, list]:
    """Añade id a h1-h4 y devuelve la lista (nivel, texto, slug) de h1-h3.

    H4 también recibe id, porque `wrap_subsubsecciones` lo necesita para envolverlo
    en <details>, pero no entra en la lista."""
    used: dict[str, int] = {}
    headings: list[tuple[int, str, str]] = []

    def replace(m):
        lvl   = int(m.group(1))
        inner = m.group(2)
        text  = re.sub(r"<[^>]+>", "", inner).strip()
        # Ancla estable al renumerar: si el encabezado abre con un número de sección
        # (1.1, 2.3, …), se descarta del slug. Así el ancla depende del nombre de la
        # sección, no de su posición, y un enlace interno sobrevive a un renumerado.
        slug_src = re.sub(r"^\d+(?:\.\d+)*\s+", "", text)
        base  = slugify(slug_src)
        n     = used.get(base, 0)
        used[base] = n + 1
        slug  = base if n == 0 else f"{base}-{n}"
        if lvl <= 3:
            headings.append((lvl, text, slug))
        return f'<h{lvl} id="{slug}">{inner}</h{lvl}>'

    html = re.sub(r"<h([1-4])>(.*?)</h\1>", replace, html, flags=re.DOTALL)
    return html, headings


def wrap_subsubsecciones(content: str) -> str:
    """Envuelve cada H4 + su contenido (hasta el siguiente H4) en
    <details class="subsubseccion"> (colapsado por defecto).

    Tercer nivel de plegado: aplica dentro de cada subsección H3.
    """
    pattern = re.compile(
        r'<h4 id="([^"]*)">(.*?)</h4>(.*?)(?=<h4 id="|\Z)',
        re.DOTALL,
    )

    matches = list(pattern.finditer(content))
    if not matches:
        return content

    pieces: list[str] = []
    last_end = 0
    for m in matches:
        slug       = m.group(1)
        title_html = m.group(2)
        body       = m.group(3)
        pieces.append(content[last_end:m.start()])
        pieces.append(
            f'<details id="{slug}" class="subsubseccion">'
            f'<summary class="subsubseccion-summary">{title_html}</summary>'
            f'{body}'
            f'</details>'
        )
        last_end = m.end()

    pieces.append(content[last_end:])
    return ''.join(pieces)


def wrap_subsecciones(content: str) -> str:
    """Envuelve cada H3 y su contenido (hasta el siguiente H3) en <details> cerrado.

    Aplica al contenido de un bloque; el lector abre solo lo que necesita. Las H4
    internas se envuelven en `subsubseccion` (tercer nivel plegable).
    """
    pattern = re.compile(
        r'<h3 id="([^"]*)">(.*?)</h3>(.*?)(?=<h3 id="|\Z)',
        re.DOTALL,
    )

    matches = list(pattern.finditer(content))
    if not matches:
        return content

    pieces: list[str] = []
    last_end = 0
    for m in matches:
        slug       = m.group(1)
        title_html = m.group(2)
        body       = m.group(3)
        # Tercer nivel: envolver H4 internos en <details class="subsubseccion">.
        body = wrap_subsubsecciones(body)
        pieces.append(content[last_end:m.start()])
        pieces.append(
            f'<details id="{slug}" class="subseccion">'
            f'<summary class="subseccion-summary">{title_html}</summary>'
            f'{body}'
            f'</details>'
        )
        last_end = m.end()

    pieces.append(content[last_end:])
    return ''.join(pieces)


def wrap_bloques(html: str) -> str:
    """Envuelve todos los H2 del cuerpo en <details> cerrados.

    Cada bloque H2 tiene botones Expandir y Contraer para sus subsecciones.
    """
    pattern = re.compile(
        r'<h2 id="([^"]*)">(.*?)</h2>(.*?)(?=<h2 id="|\Z)',
        re.DOTALL,
    )

    matches = list(pattern.finditer(html))
    if not matches:
        return html

    pieces: list[str] = []
    last_end = 0
    for i, m in enumerate(matches):
        slug       = m.group(1)
        title_html = m.group(2)
        content    = m.group(3)
        bloque_n   = i + 1

        # Nivel 2: envolver H3 internos en <details> (también cerrados).
        content = wrap_subsecciones(content)

        pieces.append(html[last_end:m.start()])
        pieces.append(
            f'<details id="{slug}" class="bloque bloque-{bloque_n}">'
            f'<summary class="bloque-summary">'
            f'<span class="bloque-chip">'
            f'<span class="bloque-title">{title_html}</span>'
            f'<button type="button" class="bloque-btn" data-action="expand" '
            f'title="Expandir el bloque y todas sus subsecciones">Expandir</button>'
            f'<button type="button" class="bloque-btn" data-action="collapse" '
            f'title="Contraer el bloque y todas sus subsecciones">Contraer</button>'
            f'</span>'
            f'</summary>'
            f'{content}'
            f'</details>'
        )
        last_end = m.end()

    pieces.append(html[last_end:])
    return ''.join(pieces)


# Script de los botones Expandir y Contraer de los bloques
BLOQUE_TOGGLE_SCRIPT = """<script>
document.documentElement.classList.add('js');
document.addEventListener('click', function (e) {
  var btn = e.target.closest('.bloque-btn');
  if (!btn) return;
  e.preventDefault();
  e.stopPropagation();
  var bloque = btn.closest('.bloque');
  if (!bloque) return;
  var open = btn.dataset.action === 'expand';
  bloque.open = open;
  bloque.querySelectorAll('.subseccion, .subsubseccion').forEach(function (s) { s.open = open; });
});
</script>"""

def render_page(title: str, header_main: str, header_sub: str, resumen_html: str, body_html: str,
                extra_head: str = "", extra_body_end: str = "", footer_text: str = "") -> str:
    """Página completa: cabecera, resumen, cuerpo en bloques plegables, pie y script Expandir/Contraer.

    `extra_head` y `extra_body_end` añaden estilos o scripts (tema, CSS del proyecto)."""
    css = CSS_PATH.read_text(encoding="utf-8")

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <style data-kit="skills/documento_vision/assets/estilo_base.css">
{css}
  </style>{extra_head}
</head>
<body>
  <div class="page">

    <header class="site-header">
      <div class="institution">
        <div class="institution-name">{header_main}</div>
        <div class="institution-sub">{header_sub}</div>
      </div>
    </header>

    <div class="report-header">
      {resumen_html}
    </div>

    <div class="report-body">
      {body_html}
    </div>

    <footer class="site-footer">
      {footer_text}
    </footer>

  </div>
{BLOQUE_TOGGLE_SCRIPT}{extra_body_end}
</body>
</html>"""
