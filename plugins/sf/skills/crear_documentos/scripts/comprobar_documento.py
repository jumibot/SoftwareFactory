"""Comprueba un documento generado con una sola orden (skill crear_documentos, «Comprobación»).

    python -I -X utf8 comprobar_documento.py <documento>.html [--pdf <ruta.pdf>] [--sin-diagramas] [--json]

Abre el HTML en un navegador de verdad, en escritorio (1300 px) y en móvil (390 × 844), en claro y, si el documento
tiene paleta oscura (`:root[data-theme="dark"]`, la del modo oscuro de «Lectura»), también en oscuro; con las secciones
y las tarjetas abiertas, para ver todo lo que el lector puede abrir. En cada vista dice:
  - desplazamiento horizontal y desbordes: la página más ancha que la pantalla y cada elemento que se sale por un lado
    (lo que está dentro de una caja con su propio desplazamiento, como una tabla ancha, no cuenta);
  - errores de JS de la página (los mensajes de error de la consola, como un recurso que no carga, van como aviso);
  - contraste WCAG del texto: 4,5:1 (3:1 el grande) sobre el fondo que tiene debajo; el texto sobre una imagen o un
    degradado no se puede medir y no se mira;
y una vez, en la primera vista: restos de sintaxis en el texto visible (`:::`, `{:`, `[!aviso]`, `**`, fuera del código)
y enlaces internos a un `#id` que no existe.
Luego lo imprime en A4 (el PDF, en --pdf o en la carpeta temporal) y mira, con la hoja de impresión: nada cortado por la
derecha, sin menú ni herramientas, la portada sola en la primera página y ninguna tarjeta ni figura (que no se parten)
más alta que una página.
Por último, si tiene diagramas, pasa la comprobación de la skill diagramas (comprobar_diagramas.py, a 375 y 1440, con
--oscuro si hay paleta oscura). Sale con 1 si hay errores. Requiere Playwright (pip install playwright); sin su
Chromium, usa el Chrome o el Edge del equipo.
"""
import argparse
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    'comprobar_diagramas', AQUI.parents[1] / 'diagramas' / 'scripts' / 'comprobar_diagramas.py')
cd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cd)

VISTAS = (('escritorio', 1300, 900), ('móvil', 390, 844))
# A4 con los márgenes de la hoja de impresión (@page 15mm 15mm 17mm), en px CSS (96 por pulgada).
MM = 96 / 25.4
A4_ANCHO = round((210 - 30) * MM)   # 680
A4_ALTO = round((297 - 32) * MM)    # 1002
# Lo que la hoja de impresión oculta (estilo_documento.css y herramientas.css).
NO_SE_IMPRIME = ('.menu', '.buscador', '.imprimir', '.saltar', '.plegar-tarjetas', '.barra-doc', '.boton-anotar',
                 '.modal-lectura', '.columna-herramientas', '.herramienta', '.abrir-herramienta')
TOPE = 12   # cuántos de cada clase se listan en el informe (el JSON los lleva todos)

# Funciones comunes de las medidas, en la página.
COMUN = r"""
  const rgba = s => { const m = (s || '').match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
  const describir = el => { let d = el.tagName.toLowerCase();
    if (el.id) d += '#' + el.id; else if (el.classList.length) d += '.' + [...el.classList].slice(0, 2).join('.');
    const t = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40); return t ? `${d} «${t}»` : d; };
  const desbordes = () => {
    const W = innerWidth, fuera = [];
    for (const el of document.body.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      if (r.width < 1 || r.height < 1 || (r.right <= W + 1 && r.left >= -1)) continue;
      if (r.right <= 0 || r.left >= W) continue;   // entero fuera: escondido a propósito (un panel lateral cerrado)
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.position === 'fixed' && cs.transform !== 'none') continue;
      let caja = false;   // dentro de algo que recorta o desplaza: no se sale de la página
      for (let p = el.parentElement; p && p !== document.body && p !== document.documentElement; p = p.parentElement)
        if (getComputedStyle(p).overflowX !== 'visible') { caja = true; break; }
      if (caja || fuera.some(f => f.el.contains(el))) continue;
      fuera.push({el, de: Math.round(r.left), a: Math.round(r.right)});
    }
    return fuera.map(f => ({elemento: describir(f.el), de: f.de, a: f.a}));
  };
"""

MEDIR = r"""
([primera]) => {
""" + COMUN + r"""
  const de = document.documentElement, res = {ancho: innerWidth};
  res.scroll = de.scrollWidth > innerWidth + 1 ? de.scrollWidth : 0;
  res.desbordes = desbordes();

  // Textos: el color y las capas de fondo que tiene debajo, de fuera a dentro; el contraste se calcula en Python.
  const visible = el => { const cs = getComputedStyle(el); return cs.display !== 'none' && cs.visibility !== 'hidden'; };
  res.textos = [];
  const vistos = new Set(), w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = w.nextNode(); n; n = w.nextNode()) {
    const el = n.parentElement;
    if (!el || vistos.has(el) || !n.textContent.trim()) continue;
    vistos.add(el);
    if (el.closest('svg, script, style, noscript, template, [aria-hidden="true"], :disabled')) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2 || r.right <= 0 || r.left >= innerWidth || !visible(el)) continue;
    let capas = [], opacidad = 1, medible = true, opaco = false;
    for (let e = el; e; e = e.parentElement) {
      const cs = getComputedStyle(e);
      opacidad *= +cs.opacity;
      if (cs.clipPath !== 'none' || (cs.clip && cs.clip !== 'auto') || cs.filter !== 'none' || cs.mixBlendMode !== 'normal') { medible = false; break; }
      if (!opaco && cs.backgroundImage !== 'none') { medible = false; break; }
      const c = rgba(cs.backgroundColor);
      if (!opaco && c && c[3] > 0) { capas.unshift(c); if (c[3] >= 1) opaco = true; }
    }
    if (!medible || opacidad <= 0) continue;
    const cs = getComputedStyle(el), color = rgba(cs.color);
    if (!color) continue;
    color[3] *= opacidad;
    res.textos.push({elemento: describir(el), color, capas, px: parseFloat(cs.fontSize), peso: parseInt(cs.fontWeight) || 400});
  }

  if (primera) {
    // Restos de sintaxis en el texto visible, fuera del código.
    const texto = [], t = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let n = t.nextNode(); n; n = t.nextNode())
      if (!n.parentElement.closest('pre, code, kbd, samp, script, style, textarea, template')) texto.push(n.textContent);
    const todo = texto.join(' ');
    res.restos = [];
    for (const [patron, nombre] of [[/:::/g, ':::'], [/\{:/g, '{:'], [/\[!\w+\]/g, '[!…]'], [/\*\*/g, '**']]) {
      const m = todo.match(patron);
      if (m) { const i = todo.search(patron); res.restos.push(`${nombre} (${m.length}) en «…${todo.slice(Math.max(0, i - 25), i + 25).replace(/\s+/g, ' ').trim()}…»`); }
    }
    // Enlaces internos a un id que no existe.
    res.enlaces = [...new Set([...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href'))
      .filter(h => h.length > 1 && !document.getElementById(decodeURIComponent(h.slice(1)))))];
  }
  return res;
}
"""

IMPRESION = r"""
([alto, ocultos]) => {
""" + COMUN + r"""
  const res = {desbordes: desbordes(), visibles: [], portada: null, altas: [], partibles: []};
  for (const s of ocultos) document.querySelectorAll(s).forEach(e => {
    const r = e.getBoundingClientRect();
    if (r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden') res.visibles.push(describir(e)); });
  const p = document.querySelector('.portada');
  if (p) {
    const sig = p.nextElementSibling, cs = getComputedStyle(p);
    res.portada = {alto: Math.round(p.getBoundingClientRect().height),
                   salto: cs.breakAfter === 'page' || (sig && getComputedStyle(sig).breakBefore === 'page')};
  }
  // Las tarjetas y las figuras no se parten (break-inside: avoid); si miden más que una página, se cortan igual.
  document.querySelectorAll('.tarjeta, figure').forEach(e => {
    const r = e.getBoundingClientRect(); if (r.height < 1) return;
    if (getComputedStyle(e).breakInside !== 'avoid') res.partibles.push(describir(e));
    else if (r.height > alto) res.altas.push({elemento: describir(e), alto: Math.round(r.height)});
  });
  return res;
}
"""

ABRIR_TODO = """() => { document.querySelectorAll('details').forEach(d => d.open = true);
  document.querySelectorAll('[hidden]').forEach(e => { if (e.matches('.ficha')) e.hidden = false; }); }"""


def coma(x: float, d: int = 1) -> str:
    return cd.coma(x, d)


def contrastes(textos):
    """Los textos por debajo del mínimo, con el cálculo de la skill diagramas."""
    fallos = []
    for t in textos:
        fondo = cd.fondo_de(t['capas'], (255, 255, 255))
        k = cd.contraste(cd.componer(t['color'], fondo), fondo)
        minimo = 3.0 if cd.texto_grande(t['px'], t['peso']) else 4.5
        if k < minimo - 0.005:
            fallos.append(f"contraste {coma(k, 2)}:1 en {t['elemento']} (mín. {coma(minimo)}:1)")
    return list(dict.fromkeys(fallos))


def tiene_oscuro(html: str) -> bool:
    return '[data-theme="dark"]' in html


def tiene_diagramas(html: str) -> bool:
    """Un <svg> dentro de una <figure>, lo que mira comprobar_diagramas.py (los iconos de las tarjetas no cuentan)."""
    cuerpo = re.sub(r'<(style|script)\b.*?</\1>', '', html, flags=re.S | re.I)
    return bool(re.search(r'<figure\b(?:(?!</figure>).)*?<svg\b', cuerpo, re.S))


def contar_paginas(pdf: Path) -> int:
    return len(re.findall(rb'/Type\s*/Page(?![a-zA-Z])', pdf.read_bytes()))


def comprobar(ruta: Path, pdf: Path, diagramas: bool = True) -> dict:
    from playwright.sync_api import sync_playwright
    html = ruta.read_text(encoding='utf-8', errors='replace')
    modos = ('claro', 'oscuro') if tiene_oscuro(html) else ('claro',)
    res = {'documento': str(ruta), 'vistas': [], 'a4': None, 'diagramas': None}
    with sync_playwright() as pw:
        nav = cd.navegador(pw)
        try:
            primera = True
            for modo in modos:
                for nombre, ancho, alto in VISTAS:
                    p = nav.new_page(viewport={'width': ancho, 'height': alto})
                    js, consola = [], []
                    p.on('pageerror', lambda e, js=js: js.append(str(e)))
                    p.on('console', lambda m, c=consola: c.append(m.text) if m.type == 'error' else None)
                    p.goto(ruta.resolve().as_uri())
                    p.add_style_tag(content='*, *::before, *::after { transition: none !important; animation: none !important; }'
                                            ' html { scroll-behavior: auto !important; }')
                    if modo == 'oscuro':   # lo que hace el modo oscuro de «Lectura» (lectura.js)
                        p.evaluate("document.documentElement.dataset.modo = 'oscuro'; document.documentElement.dataset.theme = 'dark'")
                    p.evaluate('document.fonts.ready')
                    p.evaluate(ABRIR_TODO)
                    p.wait_for_timeout(250)
                    m = p.evaluate(MEDIR, [primera])
                    m.update(vista=nombre, modo=modo, js=js, consola=list(dict.fromkeys(consola)),
                             contraste=contrastes(m.pop('textos')))
                    res['vistas'].append(m)
                    primera = False
                    p.close()
            # A4: el PDF y, con la hoja de impresión al ancho de la caja de la página, lo que se mide.
            p = nav.new_page(viewport={'width': A4_ANCHO, 'height': A4_ALTO})
            p.goto(ruta.resolve().as_uri())
            p.emulate_media(media='print')
            p.evaluate("window.dispatchEvent(new Event('beforeprint'))")
            p.evaluate(ABRIR_TODO)
            p.evaluate('document.fonts.ready')
            p.wait_for_timeout(250)
            a4 = p.evaluate(IMPRESION, [A4_ALTO, list(NO_SE_IMPRIME)])
            pdf.parent.mkdir(parents=True, exist_ok=True)
            p.pdf(path=str(pdf), format='A4', print_background=True)
            a4.update(pdf=str(pdf), paginas=contar_paginas(pdf))
            res['a4'] = a4
            p.close()
        finally:
            nav.close()
    if diagramas and tiene_diagramas(html):
        res['diagramas'] = [{'ancho': m['ancho'], 'modo': m['modo'], 'interaccion': m['interaccion'],
                             'figuras': [{k: f[k] for k in ('n', 'nombre', 'errores', 'avisos')} for f in m['figuras']]}
                            for m in cd.comprobar(ruta, [375, 1440], 6.5, modos)]
    return res


def errores(res) -> list:
    """Todos los errores, como líneas «dónde: qué»."""
    salida = []
    for v in res['vistas']:
        donde = f"{v['vista']} ({v['ancho']} px), {v['modo']}"
        if v['scroll']:
            salida.append(f"{donde}: desplazamiento horizontal, la página mide {v['scroll']} px")
        salida += [f"{donde}: se sale de la pantalla {d['elemento']} ({d['de']}–{d['a']} px)" for d in v['desbordes']]
        salida += [f'{donde}: error de JS: {e}' for e in v['js']]
        salida += [f'{donde}: {e}' for e in v['contraste']]
        salida += [f'restos de sintaxis: {r}' for r in v.get('restos', [])]
        salida += [f'enlace interno a {h}, que no existe' for h in v.get('enlaces', [])]
    a4 = res['a4']
    if a4:
        salida += [f"A4: se corta por la derecha {d['elemento']} ({d['de']}–{d['a']} px de {A4_ANCHO})" for d in a4['desbordes']]
        salida += [f'A4: se imprime {e}, que no debería' for e in a4['visibles']]
        if a4['portada'] and not a4['portada']['salto']:
            salida.append('A4: la portada no acaba en un salto de página (break-after: page)')
        if a4['portada'] and a4['portada']['alto'] > A4_ALTO:
            salida.append(f"A4: la portada mide {a4['portada']['alto']} px y no cabe sola en la primera página ({A4_ALTO})")
        salida += [f"A4: {e['elemento']} mide {e['alto']} px, más que una página ({A4_ALTO}): se corta" for e in a4['altas']]
        salida += [f'A4: {e} se puede partir entre dos páginas (sin break-inside: avoid)' for e in a4['partibles']]
    for m in res['diagramas'] or []:
        donde = f"diagramas a {m['ancho']} px, {m['modo']}"
        salida += [f'{donde}: {e}' for e in m['interaccion']]
        for f in m['figuras']:
            salida += [f"{donde}: figura {f['n']}" + (f" ({f['nombre'][:50]})" if f['nombre'] else '') + f': {e}'
                       for e in f['errores']]
    return salida


def informe(res) -> int:
    lista = errores(res)
    print(f"Documento: {res['documento']}")
    vistas = ', '.join(f"{v['vista']} {v['modo']}" for v in res['vistas'])
    print(f'Vistas: {vistas}.')
    a4 = res['a4']
    if a4:
        print(f"A4: {a4['paginas'] or '?'} página(s), en {a4['pdf']}")
    if res['diagramas'] is not None:
        print(f"Diagramas: {max((len(m['figuras']) for m in res['diagramas']), default=0)} figura(s)")
    vistos = {}
    for e in lista:
        clase = e.split(':', 1)[0]
        vistos[clase] = vistos.get(clase, 0) + 1
        if vistos[clase] <= TOPE:
            print(f'  ✕ {e}')
    for clase, n in vistos.items():
        if n > TOPE:
            print(f'  … y {n - TOPE} más en «{clase}» (todos, con --json)')
    for v in res['vistas']:
        for c in v['consola']:
            print(f"  · {v['vista']}, {v['modo']}: consola: {c[:160]}")
    for m in res['diagramas'] or []:
        for f in m['figuras']:
            for a in f['avisos']:
                print(f"  · diagramas a {m['ancho']} px, {m['modo']}: figura {f['n']}: {a}")
    print('Sin errores.' if not lista else f'{len(lista)} error(es).')
    return 1 if lista else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='Comprueba un documento generado: escritorio, móvil, claro y oscuro, A4 y diagramas.')
    ap.add_argument('html', type=Path)
    ap.add_argument('--pdf', type=Path, help='dónde dejar el PDF en A4 (por defecto, en la carpeta temporal)')
    ap.add_argument('--sin-diagramas', action='store_true', help='no pasar la comprobación de los diagramas')
    ap.add_argument('--json', action='store_true', help='salida en JSON')
    a = ap.parse_args(argv)
    if not a.html.is_file():
        print(f'No existe {a.html}', file=sys.stderr)
        return 2
    pdf = a.pdf or Path(tempfile.gettempdir()) / 'sf-comprobar-documento' / (a.html.stem + '.pdf')
    res = comprobar(a.html, pdf, not a.sin_diagramas)
    if a.json:
        res['errores'] = errores(res)
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 1 if res['errores'] else 0
    return informe(res)


if __name__ == '__main__':
    sys.exit(main())
