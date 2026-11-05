"""Comprueba los diagramas SVG de una página HTML, abierta en un navegador de verdad (skill diagramas).

    python -I -X utf8 comprobar_diagramas.py <página.html> [--anchos 375,1440] [--letra-min 6.5] [--oscuro] [--json]

En cada ancho, para cada <svg> de una <figure> que se vea:
  - geometría: textos que se pisan, que se salen del dibujo o de su caja, cajas con borde que se pisan, una etiqueta
    (rectángulo sin borde con texto) bajo una caja pintada después, una línea que cruza un texto, y la página o el
    dibujo más anchos que la pantalla;
  - letra: ningún texto por debajo de --letra-min píxeles en pantalla (6,5 por defecto: la etiqueta de 8 de diagram-design
    en la horizontal vista desde 800 px, al 83 %; el propietario manda la letra de la original, no el mínimo de 13);
  - contraste WCAG: 4,5:1 el texto (3:1 si es grande), 3:1 las flechas; los bordes de caja por debajo de 3:1, aviso;
  - accesibilidad: nombre accesible, ningún role="img" con hijos que se pulsan, y nodos pulsables de 24 px o más;
  - interacción (figuras data-diagrama): cada nodo se pulsa en su centro, Intro abre su ficha en el HUD (sin salirse de
    la figura por los lados) y resalta su recorrido, y Escape la cierra y devuelve el foco.
Con --oscuro, también con data-theme="dark" en <html> (los temas con «colores-oscuro»). Sale con 1 si hay errores. Requiere Playwright (pip install playwright); sin su Chromium, usa el Chrome o el Edge del
equipo.
"""
import argparse
import json
import sys
from pathlib import Path

# ── Contraste (WCAG 2.x), en Python para poder probarlo sin navegador ──


def lineal(c: float) -> float:
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminancia(rgb) -> float:
    r, g, b = (lineal(x) for x in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b) -> float:
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def componer(arriba, abajo):
    """Pinta un color rgba (alfa 0..1) sobre uno opaco."""
    al = arriba[3] if len(arriba) > 3 else 1.0
    return tuple(arriba[i] * al + abajo[i] * (1 - al) for i in range(3))


def fondo_de(pila, pagina):
    """El color opaco bajo un elemento: la página y, encima, las capas de la pila, en orden de pintado."""
    c = tuple(pagina[:3])
    for capa in pila:
        c = componer(capa, c)
    return c


def coma(x: float, d: int = 2) -> str:
    return f'{x:.{d}f}'.replace('.', ',')


def texto_grande(px: float, peso: int) -> bool:
    return px >= 24 or (px >= 18.66 and peso >= 700)


# ── Lo que se mide en la página ──

MEDIR = r"""
([letraMin]) => {
  const res = {pagina: null, figuras: []};
  const de = document.documentElement;
  if (de.scrollWidth > innerWidth + 1) res.pagina = `la página mide ${de.scrollWidth} px de ancho en una pantalla de ${innerWidth}`;
  const rgba = s => { const m = (s || '').match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
  const fondoPagina = el => { for (let e = el; e; e = e.parentElement) { const c = rgba(getComputedStyle(e).backgroundColor);
    if (c && c[3] > 0) return c; } return [255, 255, 255, 1]; };
  const opacidad = el => { let o = 1; for (let e = el; e && e.tagName.toLowerCase() !== 'html'; e = e.parentElement) o *= +getComputedStyle(e).opacity; return o; };
  const visible = el => { const cs = getComputedStyle(el); return cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0; };
  const enDefs = el => !!el.closest('defs, marker, symbol, pattern, clipPath, mask');
  const caja = el => { const r = el.getBoundingClientRect(); return {x: r.left, y: r.top, w: r.width, h: r.height}; };
  const corta = (a, b, m = 0) => Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x) > m && Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y) > m;
  const dentro = (a, b, t = 1) => a.x >= b.x - t && a.y >= b.y - t && a.x + a.w <= b.x + b.w + t && a.y + a.h <= b.y + b.h + t;
  const escala = el => { const m = el.getScreenCTM(); return m ? Math.hypot(m.a, m.b) : 1; };
  const nombreTexto = t => (t.textContent || '').trim().slice(0, 40);
  const antes = (a, b) => !!(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING);

  document.querySelectorAll('figure svg').forEach((svg, i) => {
    if (svg.getAttribute('aria-hidden') === 'true' || !visible(svg) || svg.getBoundingClientRect().width < 1) return;
    let vivo = true; for (let e = svg; e; e = e.parentElement) if (getComputedStyle(e).display === 'none') vivo = false;
    if (!vivo) return;
    const f = {n: i + 1, nombre: svg.getAttribute('aria-label') || svg.querySelector('title')?.textContent || '', errores: [], avisos: [], textos: [], trazos: []};
    res.figuras.push(f);
    const R = caja(svg), papel = fondoPagina(svg);
    f.papel = papel;
    if (R.x < -0.5 || R.x + R.w > innerWidth + 0.5) f.errores.push(`el dibujo se sale de la pantalla (${Math.round(R.x)}–${Math.round(R.x + R.w)} px)`);

    // Accesibilidad
    const rol = svg.getAttribute('role');
    if (!(svg.getAttribute('aria-label') || svg.getAttribute('aria-labelledby') || svg.querySelector(':scope > title')))
      f.errores.push('sin nombre accesible: aria-label, aria-labelledby o <title>');
    const pulsables = [...svg.querySelectorAll('[tabindex], a, [role="button"]')].filter(e => e.getAttribute('tabindex') !== '-1');
    if (rol === 'img' && pulsables.length) f.errores.push('role="img" con elementos que se pulsan: el lector de pantalla no los ve');
    pulsables.forEach(e => { const c = caja(e); if (c.w < 24 || c.h < 24) f.errores.push(`«${nombreTexto(e)}» se pulsa en ${Math.round(c.w)}×${Math.round(c.h)} px (mín. 24×24)`); });

    // Visible él y todo lo que lo contiene dentro del svg (un grupo oculto oculta a sus hijos: las notas de otro tamaño).
    const visto = e => { for (let x = e; x && x !== svg; x = x.parentElement) if (!visible(x)) return false; return true; };
    const formas = [...svg.querySelectorAll('rect, circle, ellipse, polygon, path, line, polyline')].filter(e => !enDefs(e) && visto(e));
    const textos = [...svg.querySelectorAll('text')].filter(e => !enDefs(e) && visto(e) && (e.textContent || '').trim());
    const tieneTrazo = e => { const cs = getComputedStyle(e); return cs.stroke !== 'none' && parseFloat(cs.strokeWidth) > 0 && rgba(cs.stroke); };
    const tieneRelleno = e => { const cs = getComputedStyle(e); const c = rgba(cs.fill); return cs.fill !== 'none' && c && c[3] * +cs.fillOpacity > 0; };
    // Una caja de nodo (.d-caja) es una caja aunque no lleve borde (ajuste «Borde: sin borde»): no es una máscara.
    const esCaja = e => tieneTrazo(e) || (e.classList.contains('d-caja') && !e.classList.contains('d-toque'));
    const cajas = formas.filter(e => e.tagName === 'rect' && esCaja(e) && caja(e).w < R.w - 1);
    const mascaras = formas.filter(e => e.tagName === 'rect' && !esCaja(e) && tieneRelleno(e) && caja(e).w < R.w - 1);
    const conectores = formas.filter(e => ['path', 'line', 'polyline'].includes(e.tagName) && tieneTrazo(e) && (e.tagName !== 'path' || getComputedStyle(e).fill === 'none' || e.hasAttribute('marker-end')));

    // Textos: letra, desbordes, solapes, caja
    const T = textos.map(t => ({t, c: caja(t)}));
    T.forEach(({t, c}) => {
      const cs = getComputedStyle(t), px = parseFloat(cs.fontSize) * escala(t);
      if (px < letraMin - 0.05) f.errores.push(`letra de ${px.toFixed(1).replace('.', ',')} px en «${nombreTexto(t)}» (mín. ${letraMin})`);
      if (!dentro(c, R, 0.5)) f.errores.push(`«${nombreTexto(t)}» se sale del dibujo`);
      const centro = {x: c.x + c.w / 2, y: c.y + c.h / 2, w: 0, h: 0};
      const suya = cajas.concat(mascaras).map(e => ({e, b: caja(e)})).filter(o => dentro(centro, o.b, 0)).sort((a, b) => a.b.w * a.b.h - b.b.w * b.b.h)[0];
      if (suya && !dentro(c, suya.b, 1)) f.errores.push(`«${nombreTexto(t)}» se sale de su caja`);
      else if (suya && cajas.includes(suya.e) && !dentro(c, {x: suya.b.x + 4, y: suya.b.y + 2, w: suya.b.w - 8, h: suya.b.h - 4}, 0))
        f.errores.push(`«${nombreTexto(t)}» va pegado al borde de su caja (deja 4 px a los lados)`);
      // Contraste: las formas rellenas pintadas antes que cubren su centro
      const pila = formas.filter(e => antes(e, t) && tieneRelleno(e) && e.tagName !== 'line' && dentro(centro, caja(e), 0))
        .map(e => { const k = rgba(getComputedStyle(e).fill); k[3] *= +getComputedStyle(e).fillOpacity * opacidad(e); return k; });
      const color = rgba(cs.fill); if (color) color[3] *= +cs.fillOpacity * opacidad(t);
      f.textos.push({texto: nombreTexto(t), color, pila, px, peso: parseInt(cs.fontWeight) || 400});
    });
    for (let a = 0; a < T.length; a++) for (let b = a + 1; b < T.length; b++)
      if (corta(T[a].c, T[b].c, 1)) f.errores.push(`«${nombreTexto(T[a].t)}» y «${nombreTexto(T[b].t)}» se pisan`);

    // Cajas que se pisan sin contenerse, y etiquetas bajo una caja pintada después
    const B = cajas.map(e => ({e, c: caja(e)}));
    for (let a = 0; a < B.length; a++) for (let b = a + 1; b < B.length; b++)
      if (corta(B[a].c, B[b].c, 1) && !dentro(B[a].c, B[b].c) && !dentro(B[b].c, B[a].c)) f.errores.push('dos cajas se pisan sin contenerse');
    mascaras.forEach(m => { const mc = caja(m); if (!T.some(o => dentro(o.c, mc, 2))) return;
      B.forEach(o => { if (antes(m, o.e) && corta(mc, o.c, 0.5) && !dentro(mc, o.c)) f.errores.push('una etiqueta queda bajo una caja pintada después'); }); });

    // Líneas que cruzan un texto (salvo si lo tapa una máscara pintada después: eso lo mira la regla de las máscaras)
    const tapados = e => new Set(T.map((o, k) => mascaras.some(mk => antes(e, mk) && dentro(o.c, caja(mk), 2)) ? k : -1).filter(k => k >= 0));
    conectores.forEach(e => {
      let L = 0; try { L = e.getTotalLength(); } catch (_) { return; }
      const m = e.getScreenCTM(); if (!m || !L) return;
      const cs = getComputedStyle(e);
      f.trazos.push({color: rgba(cs.stroke), opacidad: +cs.strokeOpacity * opacidad(e), flecha: e.hasAttribute('marker-end') || e.hasAttribute('data-de')});
      const cruzados = new Set(), tap = tapados(e);
      for (let s = 0; s <= L; s += 2) {
        const p = e.getPointAtLength(s), x = m.a * p.x + m.c * p.y + m.e, y = m.b * p.x + m.d * p.y + m.f;
        T.forEach(({t, c}, k) => { if (tap.has(k)) return; if (x > c.x + 1 && x < c.x + c.w - 1 && y > c.y + 1 && y < c.y + c.h - 1) cruzados.add(k); });
      }
      cruzados.forEach(k => f.errores.push(`una línea cruza «${nombreTexto(T[k].t)}»`));
      // Una máscara de etiqueta pintada después no tapa una línea: entre las dos, 6 o más (regla de diagram-design)
      mascaras.filter(mk => antes(e, mk) && T.some(o => dentro(o.c, caja(mk), 2))).forEach(mk => {
        const b = caja(mk), g = 6 * escala(mk) - 0.5; let tapa = false;
        for (let s = 0; s <= L && !tapa; s += 2) {
          const p = e.getPointAtLength(s), x = m.a * p.x + m.c * p.y + m.e, y = m.b * p.x + m.d * p.y + m.f;
          if (x > b.x - g && x < b.x + b.w + g && y > b.y - g && y < b.y + b.h + g) tapa = true;
        }
        if (tapa) f.errores.push(`la máscara de «${nombreTexto(T.find(o => dentro(o.c, b, 2)).t)}» tapa una línea o queda a menos de 6 de ella`);
      });
    });
    cajas.forEach(e => { const cs = getComputedStyle(e); f.trazos.push({color: rgba(cs.stroke), opacidad: +cs.strokeOpacity * opacidad(e), flecha: false}); });
  });
  return res;
}
"""

INTERACCION = r"""
async () => {
  const errores = [];
  const espera = () => new Promise(r => setTimeout(r, 30));
  for (const fig of document.querySelectorAll('[data-diagrama]')) {
    // En un documento, la figura puede estar en una sección plegada: se abre (y las que la contienen) antes de probarla.
    for (let d = fig.closest('details'); d; d = d.parentElement && d.parentElement.closest('details')) d.open = true;
    await espera(); await espera();
    const nodo = [...fig.querySelectorAll('[data-nodo][tabindex]')].find(n => n.getBoundingClientRect().width > 0);
    fig.querySelectorAll('[data-nodo][tabindex]').forEach(n => { if (!n.getBoundingClientRect().width) return;
      n.scrollIntoView({block: 'center', behavior: 'instant'}); const r = n.getBoundingClientRect();
      const e = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      if (!e || !n.contains(e)) errores.push(`«${n.dataset.nodo}» no se pulsa en su centro (falta .d-caja o pointer-events)`); });
    const hud = fig.querySelector('.d-hud');
    if (!nodo) { if (fig.querySelector('[data-ficha]')) errores.push('figura con fichas y sin nodos que se pulsen'); continue; }
    nodo.focus();
    nodo.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', bubbles: true}));
    await espera();
    // La ficha sale en el HUD, en cualquier ancho; en una figura estrecha, sin salirse de ella por los lados.
    const abierta = () => hud && !hud.hidden;
    if (!abierta()) errores.push(`Intro en «${nodo.dataset.nodo}» no abre su ficha en el HUD`);
    else { const f = fig.getBoundingClientRect(), h = hud.getBoundingClientRect();
      if (h.left < f.left - 1 || h.right > f.right + 1) errores.push('el HUD se sale de la figura por un lado'); }
    if (!fig.classList.contains('d-resaltando')) errores.push(`«${nodo.dataset.nodo}» no resalta su recorrido`);
    nodo.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
    await espera();
    if (abierta()) errores.push('Escape no cierra la ficha');
    if (document.activeElement !== nodo) errores.push('al cerrar la ficha, el foco no vuelve al nodo');
  }
  return errores;
}
"""


def revisar(medida, letra_min):
    """Añade a cada figura los errores y avisos de contraste, con el cálculo de Python."""
    for f in medida['figuras']:
        papel = f['papel']
        for t in f['textos']:
            if not t['color']:
                continue
            fondo = fondo_de(t['pila'], papel)
            k = contraste(componer(t['color'], fondo), fondo)
            minimo = 3.0 if texto_grande(t['px'], t['peso']) else 4.5
            if k < minimo - 0.005:
                f['errores'].append(f"contraste {coma(k)}:1 en «{t['texto']}» (mín. {coma(minimo, 1)}:1)")
        for s in f['trazos']:
            if not s['color']:
                continue
            c = list(s['color'])
            c[3] *= s['opacidad']
            fondo = tuple(papel[:3])
            k = contraste(componer(c, fondo), fondo)
            if k < 3 - 0.005:
                (f['errores'] if s['flecha'] else f['avisos']).append(
                    f"{'flecha' if s['flecha'] else 'borde de caja'} con contraste {coma(k)}:1 (mín. 3:1)")
        f['errores'] = list(dict.fromkeys(f['errores']))
        f['avisos'] = list(dict.fromkeys(f['avisos']))
        for clave in ('textos', 'trazos', 'papel'):
            f.pop(clave, None)
    return medida


def navegador(pw):
    for canal in (None, 'chrome', 'msedge'):
        try:
            return pw.chromium.launch(channel=canal) if canal else pw.chromium.launch()
        except Exception:  # noqa: BLE001 — se prueba el siguiente
            continue
    raise SystemExit('No hay navegador: instala el Chromium de Playwright (python -m playwright install chromium) o Chrome.')


def comprobar(ruta: Path, anchos, letra_min: float, modos=('claro',)):
    from playwright.sync_api import sync_playwright
    salida = []
    with sync_playwright() as pw:
        nav = navegador(pw)
        try:
            for modo, ancho in [(m, a) for m in modos for a in anchos]:
                pagina = nav.new_page(viewport={'width': ancho, 'height': 844 if ancho < 800 else 900})
                errores_js = []
                pagina.on('pageerror', lambda e: errores_js.append(str(e)))
                pagina.goto(ruta.resolve().as_uri())
                if modo == 'oscuro':
                    pagina.evaluate("document.documentElement.setAttribute('data-theme', 'dark')")
                    pagina.wait_for_timeout(400)  # que acaben las transiciones de color
                pagina.evaluate('document.fonts.ready')
                medida = revisar(pagina.evaluate(MEDIR, [letra_min]), letra_min)
                medida['ancho'], medida['modo'] = ancho, modo
                medida['interaccion'] = pagina.evaluate(INTERACCION)
                medida['js'] = errores_js
                salida.append(medida)
                pagina.close()
        finally:
            nav.close()
    return salida


def informe(salida) -> int:
    fallos = 0
    for m in salida:
        print(f"── {m['ancho']} px, {m.get('modo', 'claro')}: {len(m['figuras'])} figura(s)")
        for e in ([m['pagina']] if m['pagina'] else []) + [f'error de la página: {x}' for x in m['js']] + m['interaccion']:
            print(f'  ✕ {e}')
            fallos += 1
        for f in m['figuras']:
            titulo = f"figura {f['n']}" + (f" ({f['nombre'][:50]})" if f['nombre'] else '')
            if not f['errores'] and not f['avisos']:
                print(f'  ✓ {titulo}')
            for e in f['errores']:
                print(f'  ✕ {titulo}: {e}')
            for a in f['avisos']:
                print(f'  · {titulo}: {a}')
            fallos += len(f['errores'])
    print('Sin errores.' if not fallos else f'{fallos} error(es).')
    return 1 if fallos else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='Comprueba los diagramas SVG de una página HTML.')
    ap.add_argument('html', type=Path)
    ap.add_argument('--anchos', default='375,1440', help='anchos de pantalla en px, separados por comas')
    ap.add_argument('--letra-min', type=float, default=6.5, help='letra mínima en pantalla, en px')
    ap.add_argument('--oscuro', action='store_true', help='comprobar también con data-theme="dark"')
    ap.add_argument('--json', action='store_true', help='salida en JSON')
    a = ap.parse_args(argv)
    if not a.html.is_file():
        print(f'No existe {a.html}', file=sys.stderr)
        return 2
    salida = comprobar(a.html, [int(x) for x in a.anchos.split(',') if x.strip()], a.letra_min,
                       ('claro', 'oscuro') if a.oscuro else ('claro',))
    if a.json:
        print(json.dumps(salida, ensure_ascii=False, indent=1))
        return 1 if any(f['errores'] for m in salida for f in m['figuras']) or any(m['pagina'] or m['interaccion'] or m['js'] for m in salida) else 0
    return informe(salida)


if __name__ == '__main__':
    sys.exit(main())
