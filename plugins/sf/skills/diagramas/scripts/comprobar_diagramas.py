"""Comprueba los diagramas SVG de una página HTML, abierta en un navegador de verdad (skill diagramas).

    python -I -X utf8 comprobar_diagramas.py <página.html> [--anchos 375,1440] [--letra-min 6.5] [--oscuro] [--json] [--capturas carpeta]

En cada ancho, para cada <svg> de una <figure> que se vea:
  - geometría: textos que se pisan, que se salen del dibujo o de su caja, cajas con borde que se pisan, una etiqueta
    (rectángulo sin borde con texto) bajo una caja pintada después, una línea que cruza un texto, y la página o el
    dibujo más anchos que la pantalla;
  - letra: ningún texto por debajo de --letra-min píxeles en pantalla (6,5 por defecto: la etiqueta de 8 de diagram-design
    en la horizontal vista desde 800 px, al 83 %; el propietario manda la letra de la original, no el mínimo de 13);
  - contraste WCAG: 4,5:1 el texto (3:1 si es grande), 3:1 las flechas; los bordes de caja por debajo de 3:1, aviso;
  - accesibilidad: nombre accesible, ningún role="img" con hijos que se pulsan, y nodos pulsables de 24 px o más;
  - interacción (figuras data-diagrama): cada nodo se pulsa en su centro, Intro abre su ficha en el HUD (sin salirse de
    la figura por los lados) y resalta su recorrido, y Escape la cierra y devuelve el foco; con recorrido (replay),
    «Recorrer» abre el primer paso, → pasa al siguiente e ilumina su nodo o su flecha, y Escape sale.
Con --oscuro, también con data-theme="dark" en <html> (los temas con «colores-oscuro»). Un documento que abre en la
historia (data-al-abrir="historia", el lector de crear_documentos) se mide después de salir de ella, como el lector que
pasa al documento. Sale con 1 si hay errores. Requiere Playwright (pip install playwright); sin su Chromium, usa el
Chrome o el Edge del equipo.
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
    // Flechas que no tocan su caja: cada extremo, en el borde (4 hacia la caja, dentro; 4 hacia fuera, fuera), en el
    // origen y en el destino. No en la secuencia: sus mensajes van entre líneas de vida, no entre cajas.
    if (!svg.querySelector('.d-vida')) svg.querySelectorAll('path[data-de][data-a]').forEach(p => {
      let L = 0; try { L = p.getTotalLength(); } catch (_) { return; }
      if (L < 6 || !visto(p)) return;
      const toca = (id, punto, vecino) => {   // vecino: el punto del camino a 3 del extremo; la caja queda al otro lado
        const c = svg.querySelector(`[data-nodo="${CSS.escape(id)}"] .d-caja`);
        if (!c || !c.isPointInFill) return true;
        const dx = punto.x - vecino.x, dy = punto.y - vecino.y, k = Math.hypot(dx, dy) || 1;
        const en = (x, y) => { const q = svg.createSVGPoint(); q.x = x; q.y = y; return c.isPointInFill(q); };
        return en(punto.x + 4 * dx / k, punto.y + 4 * dy / k) && !en(punto.x - 4 * dx / k, punto.y - 4 * dy / k);
      };
      const ini = p.getPointAtLength(0), fin = p.getPointAtLength(L);
      if (p.classList.contains('d-fl-bloque')) {      // la punta, un polígono aparte: el trazo acaba 14 antes
        const v = p.getPointAtLength(Math.max(0, L - 3)), k = Math.hypot(fin.x - v.x, fin.y - v.y) || 1;
        fin.x += 14 * (fin.x - v.x) / k; fin.y += 14 * (fin.y - v.y) / k;
      }
      const de = toca(p.dataset.de, ini, p.getPointAtLength(Math.min(3, L)));
      const a = toca(p.dataset.a, fin, p.getPointAtLength(Math.max(0, L - 3)));
      if (!de || !a) f.errores.push(`la flecha ${p.dataset.de} → ${p.dataset.a} no toca ${!a ? 'su destino' : 'su origen'}`);
    });
    // Una flecha que se sale del dibujo queda cortada: trocitos sueltos sin recorrido. Y la etiqueta de una flecha, junto
    // a ella (a 16 como mucho); la de una salida de una decisión, cerca de la decisión, no en medio de una vuelta larga.
    svg.querySelectorAll('path[data-de][data-a]').forEach(p => {
      if (!visto(p)) return;
      const c = caja(p);
      if (c.w + c.h > 0 && !dentro(c, R, 1)) f.errores.push(`la flecha ${p.dataset.de} → ${p.dataset.a} se sale del dibujo: queda cortada`);
    });
    if (!svg.querySelector('.d-vida')) svg.querySelectorAll('g.d-et[data-de][data-a]').forEach(g => {
      if (!visto(g)) return;
      const p = svg.querySelector(`path[data-de="${CSS.escape(g.dataset.de)}"][data-a="${CSS.escape(g.dataset.a)}"]`);
      const t = g.querySelector('text'), mk = g.querySelector('rect');
      if (!p || !t || !mk || !visto(p)) return;
      let L = 0; try { L = p.getTotalLength(); } catch (_) { return; }
      const m = p.getScreenCTM(), b = caja(mk), k = escala(mk);
      if (!m || !L) return;
      let mejor = Infinity, en = 0;
      for (let s = 0; s <= L; s += 2) {
        const q = p.getPointAtLength(s), x = m.a * q.x + m.c * q.y + m.e, y = m.b * q.x + m.d * q.y + m.f;
        const d = Math.hypot(Math.max(b.x - x, 0, x - b.x - b.w), Math.max(b.y - y, 0, y - b.y - b.h));
        if (d < mejor) { mejor = d; en = s; }
      }
      if (mejor > 16 * k) f.errores.push(`la etiqueta «${nombreTexto(t)}» queda a ${Math.round(mejor / k)} de su flecha (${g.dataset.de} → ${g.dataset.a}): junto a ella`);
      else if (svg.querySelector(`[data-nodo="${CSS.escape(g.dataset.de)}"].dec`) && L > 240 && en > Math.max(120, L / 3))
        f.avisos.push(`la etiqueta «${nombreTexto(t)}» queda lejos de la decisión de la que sale (${g.dataset.de}): cerca de ella`);
    });
    // Una caja lejos de la única con la que se une: otra caja en medio de las dos (en una columna, una rama que cuelga
    // de un paso del medio acaba al fondo y parece el final). Aviso: puede que una columna más se lea mejor.
    if (!svg.querySelector('.d-vida')) {
      const nodo = {}, vec = {};
      svg.querySelectorAll('[data-nodo]').forEach(g => { const c = g.querySelector('.d-caja'); if (c && visto(c) && caja(c).w) nodo[g.dataset.nodo] = {c: caja(c), nombre: g.querySelector('.d-nn, .d-cl')?.textContent || g.dataset.nodo}; });
      svg.querySelectorAll('path[data-de][data-a]').forEach(p => {
        const a = p.dataset.de, b = p.dataset.a;
        if (!visto(p) || a === b || !nodo[a] || !nodo[b]) return;
        (vec[a] = vec[a] || new Set()).add(b); (vec[b] = vec[b] || new Set()).add(a);
      });
      Object.entries(vec).filter(([, vs]) => vs.size === 1).forEach(([n, vs]) => {
        const v = [...vs][0], A = nodo[n].c, B = nodo[v].c;
        const cx = r => r.x + r.w / 2, cy = r => r.y + r.h / 2;
        const medio = Object.entries(nodo).filter(([k, o]) => k !== n && k !== v && [...Array(41).keys()].some(i => {
          const x = cx(A) + (cx(B) - cx(A)) * i / 40, y = cy(A) + (cy(B) - cy(A)) * i / 40;
          return x > o.c.x + 2 && x < o.c.x + o.c.w - 2 && y > o.c.y + 2 && y < o.c.y + o.c.h - 2;
        }));
        if (medio.length) f.avisos.push(`«${nodo[n].nombre}» queda lejos de «${nodo[v].nombre}», la única con que se une (en medio, «${medio.map(([, o]) => o.nombre).join('», «')}»): ¿al lado, en otra columna?`);
      });
      // Un flujo lineal va recto si cabe: una cadena de tres pasos o más dentro de una zona (cada uno, una entrada y una
      // salida dentro de ella) que no va en una fila ni en una columna, con sitio en la zona para ir recta.
      const zr = [...svg.querySelectorAll('rect.d-zona')].filter(visto).map(caja);
      const zde = {};
      Object.entries(nodo).forEach(([k, o]) => { const x = o.c.x + o.c.w / 2, y = o.c.y + o.c.h / 2;
        const d = zr.filter(z => z.x <= x && x <= z.x + z.w && z.y <= y && y <= z.y + z.h); zde[k] = d.sort((p, q) => p.w * p.h - q.w * q.h)[0]; });
      const ar = [];
      svg.querySelectorAll('path[data-de][data-a]').forEach(p => { const a = p.dataset.de, b = p.dataset.a;
        const sub = k => svg.querySelector(`[data-nodo="${CSS.escape(k)}"]`).dataset.sub;
        if (visto(p) && a !== b && nodo[a] && nodo[b] && zde[a] && zde[a] === zde[b] && sub(a) === sub(b) && !p.classList.contains('d-vuelta')) ar.push([a, b]); });
      const sal = n => ar.filter(([a]) => a === n).map(([, b]) => b), ent = n => ar.filter(([, b]) => b === n).map(([a]) => a);
      const lineal = n => sal(n).length <= 1 && ent(n).length <= 1;
      Object.keys(nodo).forEach(n => {
        if (!lineal(n) || (ent(n).length && lineal(ent(n)[0]) && sal(ent(n)[0]).length === 1)) return;
        const cad = [n];
        while (sal(cad[cad.length - 1]).length === 1 && !cad.includes(sal(cad[cad.length - 1])[0]) && lineal(sal(cad[cad.length - 1])[0])) cad.push(sal(cad[cad.length - 1])[0]);
        if (cad.length < 3) return;
        const cs = cad.map(k => nodo[k].c), cx = c => c.x + c.w / 2, cy = c => c.y + c.h / 2;
        if (cs.every(c => Math.abs(cy(c) - cy(cs[0])) < 2) || cs.every(c => Math.abs(cx(c) - cx(cs[0])) < 2)) return;
        const z = zde[n], suma = k => cs.reduce((t, c) => t + c[k], 0) + 24 * (cs.length - 1);
        if (suma('w') <= z.w - 16 || suma('h') <= z.h - 40)
          f.avisos.push(`el flujo «${cad.map(k => nodo[k].nombre).join(' → ')}» hace requiebros y cabe recto en su zona: en una fila o una columna`);
      });
    }
    // Cada zona, una sola carpeta: su nombre, una vez por dibujo (partida en dos, el lector la toma por dos sitios).
    const zonasN = {};
    svg.querySelectorAll('.d-zona-n').forEach(t => { const k = t.textContent.trim(); zonasN[k] = (zonasN[k] || 0) + 1; });
    Object.entries(zonasN).forEach(([k, n]) => { if (n > 1) f.errores.push(`la zona «${k}» se pinta en ${n} carpetas: una sola`); });
    // La forma de los bloques (decisión 415): un ciclo entre bloques o hermanos que van apilados pudiendo ir de otra forma.
    const bq = svg.dataset.bloques || '';
    if (bq === 'apilado-anillo') f.avisos.push('hay un ciclo entre bloques y va apilado, aunque cabe en anillo: ¿«anillo:» en los datos?');
    if (bq === 'apilado-columnas') (svg.dataset.hermanos || '').split(';').filter(Boolean).forEach(g =>
      f.avisos.push(`«${g.split('|').join('» y «')}» dependen de lo mismo y van uno encima del otro, aunque caben lado a lado: ¿«columnas:» en los datos?`));
    // Desequilibrio: con bloques cerrados, cada fila (lo que se solapa en altura: carpetas de zona y nodos sueltos) que
    // lleva uno debe repartirse respecto a la figura; su centro de masas lejos del centro, con sitio para centrarla, avisa.
    if (svg.querySelector('[data-nodo^="_b"]')) {
      const zs = [...svg.querySelectorAll('.d-carpeta-zona')].map(e => ({b: e.getBBox(), bloque: false}));
      const dentroZ = b => zs.some(z => b.x >= z.b.x - 1 && b.x + b.width <= z.b.x + z.b.width + 1 && b.y >= z.b.y - 1 && b.y + b.height <= z.b.y + z.b.height + 1);
      const us = zs.concat([...svg.querySelectorAll('[data-nodo] > .d-caja')].map(e => ({b: e.getBBox(), id: e.parentNode.dataset.nodo, bloque: e.parentNode.dataset.nodo.startsWith('_b')}))
        .filter(u => !dentroZ(u.b)));
      // un bloque solo en su fila, encima o debajo del paso o el bloque con que se une, ya está en su sitio
      const enSuSitio = u => [...svg.querySelectorAll(`path[data-de="${u.id}"], path[data-a="${u.id}"]`)].some(p => {
        const o = svg.querySelector(`[data-nodo="${CSS.escape(p.dataset.de === u.id ? p.dataset.a : p.dataset.de)}"] > .d-caja`);
        if (!o) return false;
        const b = o.getBBox();
        return Math.abs(b.x + b.width / 2 - (u.b.x + u.b.width / 2)) < 8;
      });
      if (us.length > 1) {
        const F0 = Math.min(...us.map(u => u.b.x)), F1 = Math.max(...us.map(u => u.b.x + u.b.width)), Fc = (F0 + F1) / 2;
        const filas = [];
        us.slice().sort((a, b) => a.b.y - b.b.y).forEach(u => {
          const fl = filas.find(r => u.b.y < r.y1 - 4 && u.b.y + u.b.height > r.y0 + 4);
          if (fl) { fl.us.push(u); fl.y1 = Math.max(fl.y1, u.b.y + u.b.height); } else filas.push({us: [u], y0: u.b.y, y1: u.b.y + u.b.height});
        });
        filas.filter(r => r.us.some(u => u.bloque) && !(r.us.length === 1 && enSuSitio(r.us[0]))).forEach(r => {
          const a = r.us.reduce((t, u) => t + u.b.width * u.b.height, 0);
          const c = r.us.reduce((t, u) => t + (u.b.x + u.b.width / 2) * u.b.width * u.b.height, 0) / a;
          const r0 = Math.min(...r.us.map(u => u.b.x)), r1 = Math.max(...r.us.map(u => u.b.x + u.b.width));
          if (Math.abs(c - Fc) > 0.12 * (F1 - F0) && (F1 - F0) - (r1 - r0) > 24)
            f.avisos.push(`desequilibrio: la fila de «${r.us.filter(u => u.bloque).length} bloque(s)» carga ${c < Fc ? 'a la izquierda' : 'a la derecha'} con sitio para repartirse: centrada o cada uno bajo el paso con que se une`);
        });
      }
    }
    // Centrado: con bloques, cada vista se ajusta a lo que dibuja; márgenes izquierdo y derecho muy distintos, o un
    // hueco grande arriba, es un dibujo descentrado en su espacio (p. ej., el tamaño de otra vista).
    if (svg.closest('.d-vista') && !svg.classList.contains('d-notas-svg')) {
      const vb = svg.viewBox.baseVal, b = svg.getBBox();
      if (vb && vb.width && b.width) {
        const izq = b.x - vb.x, der = vb.x + vb.width - (b.x + b.width), arr = b.y - vb.y;
        if (Math.abs(izq - der) > Math.max(24, 0.06 * vb.width))
          f.errores.push(`descentrado: ${Math.round(izq)} a la izquierda y ${Math.round(der)} a la derecha del dibujo (de ${Math.round(vb.width)}): centrado en su espacio`);
        if (arr > 40) f.errores.push(`hueco de ${Math.round(arr)} arriba del dibujo: ajustado a lo que dibuja`);
      }
    }
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
    // Bloques: empiezan cerrados; pulsar uno lo abre en su sitio, su nombre lo cierra y «Abrir todos» abre el dibujo.
    const vistas = fig.querySelectorAll(':scope > .d-vista');
    if (vistas.length) {
      const vis = () => [...new Set([...vistas].filter(d => !d.hidden).map(d => d.dataset.vista))].join(' ');   // (dos juegos, con chips)
      if (vis() !== 'cerrado') errores.push(`la figura no empieza con los bloques cerrados (se ve «${vis()}»)`);
      const b = [...fig.querySelectorAll('[data-nodo^="_b"]')].find(n => n.getBoundingClientRect().width > 0);
      if (!b) errores.push('bloques cerrados sin una caja que se pulse');
      else {
        b.dispatchEvent(new MouseEvent('click', {bubbles: true})); await espera();
        const k = 'b' + b.dataset.nodo.slice(2);
        if (vis() !== k) errores.push(`pulsar «${b.dataset.nodo}» no abre su bloque (se ve «${vis()}»)`);
        const g = [...fig.querySelectorAll(`.d-vista[data-vista="${k}"] .d-zona-g`)].find(n => n.getBoundingClientRect().width > 0);
        if (!g) errores.push(`el bloque abierto «${k}» no tiene un nombre que lo cierre`);
        else { g.dispatchEvent(new MouseEvent('click', {bubbles: true})); await espera();
          if (vis() !== 'cerrado') errores.push(`el nombre del bloque abierto no lo vuelve a cerrar (se ve «${vis()}»)`); }
      }
      const todo = fig.querySelector('.d-bloques-b[data-ver="todo"]');
      if (!todo) errores.push('bloques sin el botón «Abrir todos»');
      else { todo.click(); await espera(); if (vis() !== 'todo') errores.push('«Abrir todos» no abre el dibujo entero'); }
    }
    const nodo = [...fig.querySelectorAll('[data-nodo][tabindex]')].find(n => n.getBoundingClientRect().width > 0 && !n.dataset.nodo.startsWith('_b'));
    fig.querySelectorAll('[data-nodo][tabindex]').forEach(n => { if (!n.getBoundingClientRect().width) return;
      n.scrollIntoView({block: 'center', behavior: 'instant'}); const r = n.getBoundingClientRect();
      const e = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
      if (!e || !n.contains(e)) errores.push(`«${n.dataset.nodo}» no se pulsa en su centro (falta .d-caja o pointer-events)`); });
    const hud = fig.querySelector('.d-hud');
    if (!nodo) { if (fig.querySelector('[data-ficha]:not([data-ficha^="_b"])')) errores.push('figura con fichas y sin nodos que se pulsen'); continue; }
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
    // Recorrer (replay): el botón abre el primer paso en el HUD, → pasa al siguiente y Escape sale.
    const rec = fig.querySelector('.d-rec'), n = fig.querySelectorAll('.d-pasos > div').length;
    if (n && !rec) errores.push('figura con recorrido y sin el botón «Recorrer»');
    if (rec) {
      const r = rec.getBoundingClientRect();
      if (r.width < 24 || r.height < 24) errores.push(`el botón «Recorrer» mide ${Math.round(r.width)}×${Math.round(r.height)} px (mín. 24×24)`);
      rec.click(); await espera();
      const num = () => (hud.querySelector('.d-paso-n') || {}).textContent || '';
      if (!abierta() || !num().startsWith('Paso 1 de')) errores.push('«Recorrer» no abre el primer paso en el HUD');
      document.activeElement.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowRight', bubbles: true}));
      await espera();
      if (n > 1 && !num().startsWith('Paso 2 de')) errores.push('→ no pasa al paso siguiente del recorrido');
      const on = fig.querySelectorAll('.d-on').length;
      if (!on) errores.push('el paso del recorrido no ilumina su nodo ni su flecha');
      document.activeElement.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
      await espera();
      if (abierta() || fig.classList.contains('d-recorriendo')) errores.push('Escape no sale del recorrido');
    }
  }
  return errores;
}
"""


# Salir de la historia completa (lector.js): con data-al-abrir="historia", el documento queda oculto debajo de la capa
# hasta que el lector sale de ella; se sale con Escape, como el lector, y si no, se quita la capa.
SALIR_HISTORIA = """() => {
  if (document.querySelector('.lector-capa')) document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', bubbles: true}));
  document.querySelectorAll('.lector-capa').forEach(c => c.remove());
  document.documentElement.classList.remove('lector-abierto', 'historia-primero');
}"""


# Los puntos clave (decisión 385): cada nodo, zona o flecha de los que dice dónde se ve tiene que estar en el dibujo y
# verse; si solo se ve al abrir un bloque, se avisa. El glosario no se comprueba: inspira, no obliga (decisión 426).
PUNTOS = r"""
() => {
  const out = [];
  const visto = e => { if (!e.getClientRects().length) return false; const r = e.getBoundingClientRect(); return r.width > 0 || r.height > 0; };
  document.querySelectorAll('figure.d-gen[data-puntos-clave]').forEach((fig, i) => {
    const f = {n: i + 1, nombre: 'puntos clave · ' + (fig.querySelector('.d-titulo')?.textContent.trim() || ''), errores: [], avisos: []};
    const inicial = fig.querySelector('.d-vista[data-vista="cerrado"]');
    const svgs = [...fig.querySelectorAll('svg')].filter(visto);
    const busca = (sel, en) => en.filter(s => [...s.querySelectorAll(sel)].some(visto));
    const zona = (n, en) => en.filter(s => [...s.querySelectorAll('text')].some(t => visto(t) && t.textContent.trim().toLowerCase() === n.toLowerCase()));
    for (const p of JSON.parse(fig.dataset.puntosClave)) {
      const cosas = [...p.nodos.map(n => [`«${n}»`, en => busca(`[data-nodo="${n}"] .d-caja`, en)]),
                     ...p.zonas.map(n => [`la zona «${n}»`, en => zona(n, en)]),
                     ...p.flechas.map(([a, b]) => [`«${a} > ${b}»`, en => busca(`path.d-fl[data-de="${a}"][data-a="${b}"]`, en)])];
      for (const [que, donde] of cosas) {
        const hay = donde(svgs);
        if (!hay.length) f.errores.push(`el punto clave «${p.texto}» no se ve: ${que} no está en el dibujo`);
        // con los bloques cerrados al empezar (decisión 415), se ve su bloque: cuenta como visible
        else if (inicial && !inicial.querySelector('.d-nodo.bloque') && !hay.some(s => inicial.contains(s)))
          f.avisos.push(`el punto clave «${p.texto}»: ${que} solo se ve al abrir su bloque`);
      }
    }
    if (f.errores.length || f.avisos.length) out.push(f);
  });
  return out;
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


def comprobar(ruta: Path, anchos, letra_min: float, modos=('claro',), capturas: Path = None):
    """Con capturas, guarda allí la de cada figura que se ve, en cada ancho y modo (para mirarla en el bucle de afinado)."""
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
                pagina.evaluate(SALIR_HISTORIA)
                if modo == 'oscuro':
                    # Sin transiciones: en una figura oculta (la otra orientación) no avanzan y el color medido sería el
                    # del claro.
                    pagina.add_style_tag(content='*, *::before, *::after { transition: none !important; }')
                    pagina.evaluate("document.documentElement.setAttribute('data-theme', 'dark')")
                    pagina.wait_for_timeout(400)
                pagina.evaluate('document.fonts.ready')
                # Con bloques (decisión 415), cada vista (cerrados, uno abierto, todos abiertos) se mide: todas a la vez.
                pagina.evaluate("document.querySelectorAll('.d-gen > .d-vista').forEach(d => { d.hidden = false; })")
                medida = revisar(pagina.evaluate(MEDIR, [letra_min]), letra_min)
                medida['ancho'], medida['modo'] = ancho, modo
                # Con chips en los datos, la figura lleva dos dibujos (apagados y encendidos): también se mide el otro.
                cambia = "document.querySelectorAll('figure.d-gen').forEach(f => { if (f.querySelector('[data-chips]')) f.classList.toggle('d-no-chips'); })"
                if pagina.evaluate("!!document.querySelector('figure.d-gen [data-chips]')"):
                    pagina.evaluate(cambia)
                    otra = revisar(pagina.evaluate(MEDIR, [letra_min]), letra_min)
                    pagina.evaluate(cambia)
                    for f in otra['figuras']:
                        if f['errores'] or f['avisos']:
                            f['nombre'] = 'con los chips cambiados · ' + (f['nombre'] or '')
                            medida['figuras'].append(f)
                medida['figuras'] += pagina.evaluate(PUNTOS)
                if capturas:
                    capturas.mkdir(parents=True, exist_ok=True)
                    figs = pagina.locator('figure.diagrama')
                    for i in range(figs.count()):
                        if figs.nth(i).is_visible():
                            destino = capturas / f'{ruta.stem}-{ancho}-{modo}-{i + 1}.png'
                            figs.nth(i).screenshot(path=str(destino))
                            medida.setdefault('capturas', []).append(str(destino))
                pagina.evaluate("document.querySelectorAll('.d-gen > .d-vista').forEach(d => { d.hidden = d.dataset.vista !== 'cerrado'; })")
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
        for c in m.get('capturas', []):
            print(f'  · captura: {c}')
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
    ap.add_argument('--capturas', type=Path, help='carpeta donde guardar la captura de cada figura, en cada ancho y modo')
    a = ap.parse_args(argv)
    if not a.html.is_file():
        print(f'No existe {a.html}', file=sys.stderr)
        return 2
    salida = comprobar(a.html, [int(x) for x in a.anchos.split(',') if x.strip()], a.letra_min,
                       ('claro', 'oscuro') if a.oscuro else ('claro',), a.capturas)
    if a.json:
        print(json.dumps(salida, ensure_ascii=False, indent=1))
        return 1 if any(f['errores'] for m in salida for f in m['figuras']) or any(m['pagina'] or m['interaccion'] or m['js'] for m in salida) else 0
    return informe(salida)


if __name__ == '__main__':
    sys.exit(main())
