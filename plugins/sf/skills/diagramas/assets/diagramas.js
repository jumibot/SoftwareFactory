/* Diagramas de la SF (skill diagramas): fichas en el HUD al pulsar, resaltado del recorrido y Escape.
 * Al pulsar un nodo, su ficha se abre en el HUD: junto al nodo si la figura mide 800 px o más; si no, a lo ancho, debajo.
 * Contrato del marcado, en references/interaccion.md. En cada <figure class="diagrama" data-diagrama>:
 *   - nodos: <g data-nodo="id"> con su caja principal en class="d-caja";
 *   - flechas: data-de="id" y data-a="id" en el <path> o <line>;
 *   - fichas: <div class="d-fichas" hidden> con un <div data-ficha="id" data-nombre="Nombre"> por nodo.
 * Sin JavaScript, el dibujo se ve entero, sin fichas. Hueco reservado: data-modo en la figura
 * (p. ej. «replay», por decidir) y window.sfDiagramas.modos para registrarlo más adelante. */
(function () {
  'use strict';
  const api = window.sfDiagramas = window.sfDiagramas || { modos: {} };
  // En la copia que guardan las herramientas del documento, sin HUD ni resaltado.
  (window.alCopiarDocumento = window.alCopiarDocumento || []).push(c => {
    c.querySelectorAll('.d-hud').forEach(x => x.remove());
    c.querySelectorAll('.d-resaltando').forEach(x => x.classList.remove('d-resaltando'));
    c.querySelectorAll('.d-on, .d-vecino').forEach(x => x.classList.remove('d-on', 'd-vecino'));
  });

  const ANCHA = 800;  // px de figura desde los que se dibuja la forma horizontal (como @container en diagramas.css)
  let n = 0;
  function montar(fig) {
    const k = ++n;
    const fichas = new Map([...fig.querySelectorAll('[data-ficha]')].map(d => [d.dataset.ficha, d]));
    const nodos = [...fig.querySelectorAll('[data-nodo]')];
    const flechas = [...fig.querySelectorAll('[data-de]')];
    const marcaOn = fig.dataset.marcaOn;  // id de un <marker> para las flechas resaltadas, o «auto»; opcional
    let fijo = null, desde = null;

    // Un <svg role="img"> esconde sus hijos al lector de pantalla: con nodos que se pulsan, pasa a grupo.
    fig.querySelectorAll('svg[role="img"]').forEach(s => { if (s.querySelector('[data-nodo]')) s.setAttribute('role', 'group'); });

    const hud = document.createElement('div');
    hud.className = 'd-hud'; hud.id = 'd-hud-' + k; hud.hidden = true;
    hud.setAttribute('role', 'region'); hud.setAttribute('aria-live', 'polite'); hud.setAttribute('aria-label', 'Ficha');
    hud.innerHTML = '<button type="button" class="d-cerrar" aria-label="Cerrar la ficha">✕</button><div class="d-cuerpo"></div>';
    fig.appendChild(hud);

    function resalta(id) {
      fig.classList.toggle('d-resaltando', !!id);
      const vecinos = new Set();
      flechas.forEach(f => {
        const on = !!id && (f.dataset.de === id || f.dataset.a === id);
        f.classList.toggle('d-on', on);
        if (on) { vecinos.add(f.dataset.de); vecinos.add(f.dataset.a); }
        if (marcaOn && f.hasAttribute('marker-end')) {
          if (!f.dataset.marca) f.dataset.marca = f.getAttribute('marker-end');
          // «auto»: cada SVG tiene la suya, con el id de su punta normal y «-on» detrás
          const marca = marcaOn === 'auto' ? f.dataset.marca.replace(/\)$/, '-on)') : `url(#${marcaOn})`;
          f.setAttribute('marker-end', on ? marca : f.dataset.marca);
        }
      });
      nodos.forEach(g => {
        g.classList.toggle('d-on', g.dataset.nodo === id);
        g.classList.toggle('d-vecino', g.dataset.nodo !== id && vecinos.has(g.dataset.nodo));
      });
    }

    function nombre(id) { const d = fichas.get(id); return (d && d.dataset.nombre) || id; }

    const ancha = () => fig.clientWidth >= ANCHA;
    const no = k => fig.classList.contains('d-no-' + k);  // ajustes apagados (d-no-fichas, d-no-resaltado)
    function coloca(nodo) {  // a la altura del nodo, fuera del dibujo si cabe (derecha, izquierda); si no, a su lado.
      const f = fig.getBoundingClientRect(), r = nodo.getBoundingClientRect(), w = hud.offsetWidth, h = hud.offsetHeight;
      const d = (nodo.closest('svg') || fig).getBoundingClientRect();
      if (!ancha()) {  // estrecha: a lo ancho, debajo del nodo (o encima si no cabe debajo)
        let y = r.bottom - f.top + 8;
        if (y + h > fig.offsetHeight - 8 && r.top - f.top - 8 - h >= 8) y = r.top - f.top - 8 - h;
        hud.style.left = '8px'; hud.style.top = Math.max(8, Math.min(y, fig.offsetHeight - h - 8)) + 'px';
        return;
      }
      let x;
      if (f.right - d.right >= w + 16) x = d.right - f.left + 12;
      else if (d.left - f.left >= w + 16) x = d.left - f.left - 12 - w;
      else { x = r.right - f.left + 12; if (x + w > f.width - 8) x = r.left - f.left - 12 - w; }
      x = Math.max(8, Math.min(x, f.width - w - 8));
      const y = Math.max(8, Math.min(r.top - f.top, fig.offsetHeight - h - 8));
      hud.style.left = x + 'px'; hud.style.top = y + 'px';
    }
    function abre(id, nodo) {
      if (id && no('fichas')) return;  // fichas apagadas: el nodo solo resalta
      fijo = id; resalta(id);
      nodos.forEach(g => g.hasAttribute('tabindex') && g.setAttribute('aria-expanded', String(g.dataset.nodo === id)));
      const cuerpo = hud.querySelector('.d-cuerpo');
      if (!id) {
        hud.hidden = true; cuerpo.textContent = '';
        if (desde) { desde.focus(); desde = null; }
        return;
      }
      if (nodo) desde = nodo;
      cuerpo.textContent = '';
      const h = document.createElement('h4'); h.textContent = nombre(id); cuerpo.appendChild(h);
      [...fichas.get(id).children].forEach(c => cuerpo.appendChild(c.cloneNode(true)));
      hud.hidden = false; coloca(desde || fig);
    }

    nodos.forEach(g => {
      const id = g.dataset.nodo;
      if (!fichas.has(id)) return;  // un nodo sin ficha no se pulsa
      g.setAttribute('tabindex', '0'); g.setAttribute('role', 'button');
      g.setAttribute('aria-expanded', 'false'); g.setAttribute('aria-controls', hud.id);
      g.setAttribute('aria-label', nombre(id) + ': ver su ficha');
      const pasa = () => !fijo && !no('resaltado');
      g.addEventListener('pointerenter', e => { if (pasa() && e.pointerType === 'mouse') resalta(id); });
      g.addEventListener('pointerleave', e => { if (!fijo && e.pointerType === 'mouse') resalta(null); });
      g.addEventListener('focus', () => { if (pasa()) resalta(id); });
      g.addEventListener('blur', () => { if (!fijo) resalta(null); });
      g.addEventListener('click', () => abre(fijo === id ? null : id, g));
      g.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); abre(fijo === id ? null : id, g); }
      });
    });

    hud.querySelector('.d-cerrar').addEventListener('click', () => abre(null));
    fig.addEventListener('keydown', e => {
      if (e.key !== 'Escape') return;
      if (fijo) { e.stopPropagation(); abre(null); }
    });
    document.addEventListener('pointerdown', e => { if (fijo && !fig.contains(e.target)) abre(null); });

    const modo = fig.dataset.modo;
    if (modo && api.modos[modo]) api.modos[modo](fig);
  }

  // Plegar y desplegar cajas sueltas (figuras del generador). Ajuste «Plegadas» (data-d-cajas): desplegadas, plegadas
  // (el dibujo compacto) o acordeón (el compacto con una sola desplegada). La caja cambia de alto en su sitio, centrada;
  // sus textos, su marca de fin, su circulito y los extremos de sus flechas la siguen, tocando su contorno.
  // Esquinas de las flechas (ajuste «Esquinas»): redondeadas (el d que trae) o rectas (su data-da).
  function dBase(p) {
    if (!p.dataset.dr) p.dataset.dr = p.getAttribute('d');
    const fig = p.closest('figure');
    return fig && fig.dataset.dEsquinas === 'rectas' && p.dataset.da ? p.dataset.da : p.dataset.dr;
  }
  function caminos(fig) { fig.querySelectorAll('path[data-da]').forEach(p => p.setAttribute('d', dBase(p))); }
  function esquinas(fig) {
    caminos(fig);
    new MutationObserver(() => caminos(fig)).observe(fig, { attributes: true, attributeFilter: ['data-d-esquinas'] });
  }
  function borde(v, a, b, r) { let d = v < a + r ? a + r - v : v > b - r ? v - (b - r) : 0; d = Math.min(Math.max(d, 0), r); return r - Math.sqrt(r * r - d * d); }
  function ponerCaja(svg, id, abierta) {
    const g = svg.querySelector(`[data-nodo="${id}"]`), r = g && g.querySelector('rect.d-caja[data-hd]');
    if (!r) return;
    if (!r.dataset.y0) { r.dataset.y0 = r.getAttribute('y'); r.dataset.h0 = r.getAttribute('height'); }
    const X = +r.getAttribute('x'), W = +r.getAttribute('width'), y0 = +r.dataset.y0, h0 = +r.dataset.h0, cy = y0 + h0 / 2;
    const H = abierta ? +r.dataset.hd : +r.dataset.hp, Y = cy - H / 2, croq = svg.dataset.forma === 'croqueta';
    const rx = croq ? Math.min(H, W) / 2 : +r.getAttribute('rx') || 0;
    r.setAttribute('y', Y); r.setAttribute('height', H); if (croq) r.setAttribute('rx', rx);
    const dy = Y - y0;
    const nn = g.querySelector('.d-nn'), subs = [...g.querySelectorAll('.d-sb')], fn = +nn.getAttribute('font-size');
    const pn = +r.dataset.pn, ps = +r.dataset.ps;
    const yn = cy - (fn + (abierta && subs.length ? pn + ps * (subs.length - 1) : 0)) / 2 + fn * .8;
    nn.setAttribute('y', yn.toFixed(1));
    subs.forEach((s, i) => { s.setAttribute('y', (yn + pn + ps * i).toFixed(1)); s.classList.toggle('d-plegado', !abierta); });
    const mueve = (e, a) => { const k = 'o' + a; if (!e.dataset[k]) e.dataset[k] = e.getAttribute(a); e.setAttribute(a, +e.dataset[k] + dy); };
    g.querySelectorAll('.d-fin-a, .d-fin').forEach(c => mueve(c, 'cy'));
    g.querySelectorAll('.d-chip, .d-chip-c').forEach(t => mueve(t, 'y'));
    const t = svg.querySelector(`[data-plegar="${id}"]`);
    if (t) { t.querySelectorAll('circle').forEach(c => mueve(c, 'cy')); t.setAttribute('aria-expanded', String(abierta)); }
    // Flechas: el extremo que toca esta caja, otra vez sobre su contorno.
    svg.querySelectorAll(`path[data-de="${id}"], path[data-a="${id}"]`).forEach(p => {
      const d = dBase(p), pares = [...d.matchAll(/(-?[\d.]+),(-?[\d.]+)/g)];
      if (pares.length < 2) return;
      const cambios = [];
      const extremo = (i, j, hueco) => {
        const x = +pares[i][1], y = +pares[i][2], qx = +pares[j][1], qy = +pares[j][2];
        let nx = x, ny = y;
        if (Math.abs(qx - x) < .01) {  // vertical: por arriba o por abajo
          if (y < cy) ny = Y + borde(x, X, X + W, rx) - hueco; else ny = Y + H - borde(x, X, X + W, rx) + hueco;
        } else if (Math.abs(qy - y) < .01 && croq) {  // horizontal, en una croqueta: el lado redondo
          if (x < X + W / 2) nx = X + borde(y, Y, Y + H, rx) - hueco; else nx = X + W - borde(y, Y, Y + H, rx) + hueco;
        } else return;
        cambios.push([pares[i].index, pares[i][0].length, `${+nx.toFixed(2)},${+ny.toFixed(2)}`]);
      };
      if (p.dataset.de === id) extremo(0, 1, 0);
      if (p.dataset.a === id) extremo(pares.length - 1, pares.length - 2, 2);
      let nueva = d;
      cambios.sort((a, b) => b[0] - a[0]).forEach(([i, n, txt]) => { nueva = nueva.slice(0, i) + txt + nueva.slice(i + n); });
      p.setAttribute('d', nueva);
    });
    svg.querySelectorAll(`line.d-vida[data-de="${id}"]`).forEach(l => { mueve(l, 'y1'); l.setAttribute('y1', +l.dataset.oy1 + (Y + H - y0 - h0)); });
  }
  function plegado(fig) {
    const ids = [...new Set([...fig.querySelectorAll('[data-plegar]')].map(t => t.dataset.plegar))];
    if (!ids.length) return;
    fig.classList.add('d-js');
    let abiertas = new Set();
    const pinta = () => fig.querySelectorAll('svg').forEach(s => ids.forEach(id => ponerCaja(s, id, abiertas.has(id))));
    const modo = () => {
      const m = fig.dataset.dCajas;
      abiertas = new Set(m === 'plegadas' || m === 'acordeon' ? [] : ids);   // «Máximo una desplegada»: empiezan plegadas
      pinta();
    };
    fig.querySelectorAll('[data-plegar]').forEach(t => {
      const id = t.dataset.plegar, nodo = fig.querySelector(`[data-nodo="${id}"] .d-nn`);
      t.setAttribute('tabindex', '0'); t.setAttribute('role', 'button');
      t.setAttribute('aria-label', 'Plegar o desplegar ' + (nodo ? nodo.textContent : id));
      const cambia = e => {
        e.stopPropagation();
        if (fig.dataset.dCajas === 'acordeon') abiertas = new Set(abiertas.has(id) ? [] : [id]);
        else if (abiertas.has(id)) abiertas.delete(id); else abiertas.add(id);
        pinta();
      };
      t.addEventListener('click', cambia);
      t.addEventListener('pointerdown', e => e.stopPropagation());
      t.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); cambia(e); } });
    });
    new MutationObserver(l => (l.some(x => x.attributeName === 'data-d-cajas') ? modo : pinta)())
      .observe(fig, { attributes: true, attributeFilter: ['data-d-cajas', 'data-d-esquinas'] });
    modo();
  }

  const iniciar = () => { document.querySelectorAll('[data-diagrama]').forEach(montar); document.querySelectorAll('figure.d-gen').forEach(f => { esquinas(f); plegado(f); }); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar();
})();
