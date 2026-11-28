/* Diagramas de la SF (skill diagramas): fichas en el HUD al pulsar, resaltado del recorrido y Escape.
 * Al pulsar un nodo, su ficha se abre en el HUD: junto al nodo si la figura mide 800 px o más; si no, a lo ancho, debajo.
 * Contrato del marcado, en references/interaccion.md. En cada <figure class="diagrama" data-diagrama>:
 *   - nodos: <g data-nodo="id"> con su caja principal en class="d-caja";
 *   - flechas: data-de="id" y data-a="id" en el <path> o <line>;
 *   - fichas: <div class="d-fichas" hidden> con un <div data-ficha="id" data-nombre="Nombre"> por nodo.
 *   - recorrido (replay), opcional: <div class="d-pasos" hidden> con un <div data-paso-nodo="id"> o
 *     <div data-paso-de="a" data-paso-a="b"> por paso, con su porqué; la figura lleva data-modo="recorrer".
 * Sin JavaScript, el dibujo se ve entero, sin fichas ni recorrido. Más modos: data-modo en la figura y
 * window.sfDiagramas.modos[nombre](figura). */
(function () {
  'use strict';
  const api = window.sfDiagramas = window.sfDiagramas || { modos: {} };
  // En la copia que guardan las herramientas del documento, sin HUD ni resaltado.
  (window.alCopiarDocumento = window.alCopiarDocumento || []).push(c => {
    c.querySelectorAll('.d-hud, .diagrama .d-barra').forEach(x => x.remove());
    c.querySelectorAll('.d-resaltando, .d-recorriendo, .d-solo-nuevo').forEach(x => x.classList.remove('d-resaltando', 'd-recorriendo', 'd-solo-nuevo'));
    c.querySelectorAll('.d-tapa.d-plegada').forEach(x => x.classList.remove('d-plegada'));
    c.querySelectorAll('.d-on, .d-vecino, .d-visto').forEach(x => x.classList.remove('d-on', 'd-vecino', 'd-visto'));
    c.querySelectorAll('figure.d-gen').forEach(f => f.style.removeProperty('--d-rotulo'));
  });

  // Rótulos (nombres de zona, carriles, antetítulo): el texto tenue del tema, oscurecido hacia el texto lo justo para
  // 4,5:1 sobre el fondo de la figura, con cualquier tema. Sin JavaScript, la mezcla del CSS (a medias), que también llega.
  const rgb = s => { const m = (s || '').match(/rgba?\(([^)]+)\)/); return m ? m[1].split(/[ ,/]+/).filter(Boolean).map(Number) : null; };
  const lum = c => { const l = v => (v /= 255) <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; return .2126 * l(c[0]) + .7152 * l(c[1]) + .0722 * l(c[2]); };
  const contraste = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + .05) / (y + .05); };
  function fondo(el) {
    for (let e = el; e; e = e.parentElement) { const c = rgb(getComputedStyle(e).backgroundColor); if (c && (c.length < 4 || c[3] > 0)) return c; }
    return [255, 255, 255];
  }
  function rotulo(fig) {
    const p = document.createElement('span');
    p.style.cssText = 'position:absolute;visibility:hidden;color:var(--texto-tenue, #666)';
    fig.appendChild(p);
    const tenue = rgb(getComputedStyle(p).color);
    p.style.color = 'var(--texto, #1a1a1a)';
    const texto = rgb(getComputedStyle(p).color);
    p.remove();
    if (!tenue || !texto) return;
    const bajo = fondo(fig);
    let c = tenue;
    for (let t = .05; contraste(c, bajo) < 4.6 && t <= 1.001; t += .05) c = tenue.map((v, i) => Math.round(v + (texto[i] - v) * t));
    fig.style.setProperty('--d-rotulo', `rgb(${c[0]}, ${c[1]}, ${c[2]})`);
  }
  function rotulos(fig) {
    rotulo(fig);
    new MutationObserver(() => rotulo(fig)).observe(fig, { attributes: true, attributeFilter: ['data-d-tema', 'data-d-lienzo'] });
  }
  new MutationObserver(() => document.querySelectorAll('figure.d-gen').forEach(rotulo))
    .observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme', 'data-modo', 'class', 'style'] });

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

    function marca(f, on) {  // la punta de una flecha resaltada, del color del resaltado
      if (!marcaOn || !f.hasAttribute('marker-end')) return;
      if (!f.dataset.marca) f.dataset.marca = f.getAttribute('marker-end');
      // «auto»: cada SVG tiene la suya, con el id de su punta normal y «-on» detrás
      const m = marcaOn === 'auto' ? f.dataset.marca.replace(/\)$/, '-on)') : `url(#${marcaOn})`;
      f.setAttribute('marker-end', on ? m : f.dataset.marca);
    }
    function resalta(id) {
      fig.classList.toggle('d-resaltando', !!id);
      const vecinos = new Set();
      flechas.forEach(f => {
        const on = !!id && (f.dataset.de === id || f.dataset.a === id);
        f.classList.toggle('d-on', on);
        if (on) { vecinos.add(f.dataset.de); vecinos.add(f.dataset.a); }
        marca(f, on);
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
      const tipo = fichas.get(id).dataset.tipo;   // el chip del nodo, como tipo encima del nombre
      if (tipo) { const t = document.createElement('p'); t.className = 'd-tipo'; t.textContent = tipo; cuerpo.appendChild(t); }
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
      const pasa = () => !fijo && !rec && !no('resaltado');
      g.addEventListener('pointerenter', e => { if (pasa() && e.pointerType === 'mouse') resalta(id); });
      g.addEventListener('pointerleave', e => { if (!fijo && !rec && e.pointerType === 'mouse') resalta(null); });
      g.addEventListener('focus', () => { if (pasa()) resalta(id); });
      g.addEventListener('blur', () => { if (!fijo && !rec) resalta(null); });
      // Durante el recorrido, pulsar un nodo salta a su paso (si lo tiene).
      const pulsa = () => { if (rec) { const k = pasos.findIndex(p => p.nodo === id); if (k >= 0) ir(k); return; } abre(fijo === id ? null : id, g); };
      g.addEventListener('click', pulsa);
      g.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pulsa(); }
      });
    });

    hud.querySelector('.d-cerrar').addEventListener('click', () => rec ? salir() : abre(null));
    fig.addEventListener('keydown', e => {
      if (rec) {
        const k = { ArrowRight: paso + 1, ArrowLeft: paso - 1, Home: 0, End: pasos.length - 1 }[e.key];
        if (k !== undefined) { e.preventDefault(); ir(Math.max(0, Math.min(k, pasos.length - 1))); return; }
      }
      if (e.key !== 'Escape') return;
      if (rec) { e.stopPropagation(); salir(); }
      else if (fijo) { e.stopPropagation(); abre(null); }
    });

    // Recorrer (replay): los pasos de .d-pasos, uno a uno, con ← y → o los botones del HUD. Cada paso ilumina su nodo o
    // su flecha (con sus dos extremos) y cuenta en el HUD qué pasa y por qué; sin texto, el de la ficha del nodo. Lo ya
    // recorrido queda a media luz, como en una película; sin movimiento si se pide menos (diagramas.css).
    const pasos = [...fig.querySelectorAll('.d-pasos > div')].map(d => ({ nodo: d.dataset.pasoNodo, de: d.dataset.pasoDe,
      a: d.dataset.pasoA, texto: d.textContent.trim() }));
    let rec = false, paso = -1, boton = null;
    const visible = sel => [...fig.querySelectorAll(sel)].find(e => { const r = e.getBoundingClientRect(); return r.width + r.height > 0; });
    const esDe = (f, p) => !p.nodo && f.dataset.de === p.de && f.dataset.a === p.a;
    function ir(k) {
      paso = k; const p = pasos[k], antes = pasos.slice(0, k);
      fig.classList.add('d-resaltando', 'd-recorriendo');
      const extremos = new Set(p.nodo ? [p.nodo] : [p.de, p.a]);
      const vistos = new Set(antes.flatMap(q => q.nodo ? [q.nodo] : [q.de, q.a]));
      flechas.forEach(f => {
        const on = esDe(f, p);
        f.classList.toggle('d-on', on); marca(f, on);
        f.classList.toggle('d-visto', !on && antes.some(q => esDe(f, q)));
      });
      nodos.forEach(g => {
        const id = g.dataset.nodo;
        g.classList.toggle('d-on', p.nodo === id);
        g.classList.toggle('d-vecino', !p.nodo && extremos.has(id));
        g.classList.toggle('d-visto', !extremos.has(id) && vistos.has(id));
      });
      const cuerpo = hud.querySelector('.d-cuerpo');
      cuerpo.textContent = '';
      const n = document.createElement('p'); n.className = 'd-paso-n'; n.textContent = `Paso ${k + 1} de ${pasos.length}`;
      const h = document.createElement('h4'); h.textContent = p.nodo ? nombre(p.nodo) : `${nombre(p.de)} → ${nombre(p.a)}`;
      cuerpo.append(n);
      const tipo = p.nodo && fichas.get(p.nodo) && fichas.get(p.nodo).dataset.tipo;
      if (tipo) { const t = document.createElement('p'); t.className = 'd-tipo'; t.textContent = tipo; cuerpo.appendChild(t); }
      cuerpo.append(h);
      if (p.texto) { const t = document.createElement('p'); t.textContent = p.texto; cuerpo.appendChild(t); }
      else if (p.nodo && fichas.get(p.nodo)) [...fichas.get(p.nodo).children].forEach(c => cuerpo.appendChild(c.cloneNode(true)));
      const nav = document.createElement('div'); nav.className = 'd-nav';
      nav.innerHTML = '<button type="button" data-ir="-1">← Anterior</button><button type="button" data-ir="1">Siguiente →</button>';
      nav.querySelector('[data-ir="-1"]').disabled = k === 0;
      nav.querySelector('[data-ir="1"]').disabled = k === pasos.length - 1;
      nav.querySelectorAll('button').forEach(b => b.addEventListener('click', () => ir(paso + +b.dataset.ir)));
      cuerpo.appendChild(nav);
      hud.hidden = false;
      // el HUD, junto al nodo del paso o, en una flecha, junto a su destino (así no tapa la flecha)
      const el = visible(`[data-nodo="${p.nodo || p.a}"]`) || visible(`path[data-de="${p.de}"][data-a="${p.a}"]`);
      coloca(el || fig);
      const quieto = matchMedia('(prefers-reduced-motion: reduce)').matches;
      (nav.querySelector('[data-ir="1"]:not(:disabled)') || nav.querySelector('button:not(:disabled)')).focus({ preventScroll: true });
      hud.scrollIntoView({ block: 'nearest', behavior: quieto ? 'auto' : 'smooth' });
    }
    function salir() {
      rec = false; paso = -1;
      fig.classList.remove('d-recorriendo');
      fig.querySelectorAll('.d-visto').forEach(e => e.classList.remove('d-visto'));
      resalta(null); hud.hidden = true; hud.querySelector('.d-cuerpo').textContent = '';
      if (boton) { boton.setAttribute('aria-pressed', 'false'); boton.textContent = '▶ Recorrer paso a paso'; boton.focus(); }
    }
    // «Solo lo nuevo»: con nodos o flechas «nuevo», un botón deja a media luz todo lo demás.
    const nuevo = fig.querySelector('.d-nodo.nuevo, .d-fl.d-nuevo');
    let barra = null;
    const enBarra = b => {
      if (!barra) {
        barra = document.createElement('div'); barra.className = 'd-barra';
        const tras = fig.querySelector(':scope > .d-ayuda') || fig.querySelector(':scope > .d-cabecera');
        if (tras) tras.after(barra); else fig.prepend(barra);
      }
      barra.appendChild(b);
    };
    if (nuevo) {
      fig.querySelectorAll('.d-et[data-de]').forEach(e => {
        if (fig.querySelector(`.d-fl.d-nuevo[data-de="${e.dataset.de}"][data-a="${e.dataset.a}"]`)) e.classList.add('d-nuevo');
      });
      const b = document.createElement('button'); b.type = 'button'; b.className = 'd-rec d-nuevo-b';
      b.setAttribute('aria-pressed', 'false'); b.textContent = 'Solo lo nuevo';
      b.addEventListener('click', () => {
        const on = fig.classList.toggle('d-solo-nuevo'); b.setAttribute('aria-pressed', String(on));
      });
      enBarra(b);
    }
    if (pasos.length) {
      boton = document.createElement('button'); boton.type = 'button'; boton.className = 'd-rec';
      boton.setAttribute('aria-pressed', 'false'); boton.textContent = '▶ Recorrer paso a paso';
      boton.addEventListener('click', () => {
        if (rec) { salir(); return; }
        if (fijo) abre(null);
        rec = true; boton.setAttribute('aria-pressed', 'true'); boton.textContent = '■ Salir del recorrido';
        ir(0);
      });
      enBarra(boton);
      if (barra.firstChild !== boton) barra.prepend(boton);
    }
    document.addEventListener('pointerdown', e => { if (fijo && !rec && !fig.contains(e.target)) abre(null); });

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
    const H = abierta ? +r.dataset.hd : +r.dataset.hp, Y = cy - H / 2, croq = (svg.dataset.formaDibujo || svg.dataset.forma) === 'croqueta';
    const rx = croq ? Math.min(H, W) / 2 : +r.getAttribute('rx') || 0;
    r.setAttribute('y', Y); r.setAttribute('height', H); if (croq) r.setAttribute('rx', rx);
    const dy = Y - y0;
    // el nombre, en una o dos líneas (data-pnn, el paso entre ellas), y el detalle debajo
    const nns = [...g.querySelectorAll('.d-nn')], subs = [...g.querySelectorAll('.d-sb')], fn = +nns[0].getAttribute('font-size');
    const pn = +r.dataset.pn, ps = +r.dataset.ps, extra = (+r.dataset.pnn || 0) * (nns.length - 1);
    const yn = cy - (fn + extra + (abierta && subs.length ? pn + ps * (subs.length - 1) : 0)) / 2 + fn * .8;
    nns.forEach((t, i) => t.setAttribute('y', (yn + (+r.dataset.pnn || 0) * i).toFixed(1)));
    subs.forEach((s, i) => { s.setAttribute('y', (yn + extra + pn + ps * i).toFixed(1)); s.classList.toggle('d-plegado', !abierta); });
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
    // Con cajas que se pliegan (se pulsan), el <svg role="img"> esconde sus hijos al lector de pantalla: pasa a grupo.
    fig.querySelectorAll('svg[role="img"]').forEach(s => { if (s.querySelector('[data-plegar]')) s.setAttribute('role', 'group'); });
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

  // Zonas que se pliegan: pulsar su nombre (o Intro o Espacio en él) pone encima una tapa con su nombre, en su sitio;
  // pulsar la tapa la quita.
  function zonas(fig) {
    fig.querySelectorAll('.d-zona-g').forEach(g => {
      const tapa = g.closest('svg').querySelector(`.d-tapa[data-zona="${g.dataset.zona}"]`);
      if (!tapa) return;
      const pon = on => {
        tapa.classList.toggle('d-plegada', on); g.setAttribute('aria-expanded', String(!on));
        g.setAttribute('aria-label', `${on ? 'Desplegar' : 'Plegar'} la zona ${g.dataset.nombre}`);
      };
      g.addEventListener('click', e => { e.stopPropagation(); pon(!tapa.classList.contains('d-plegada')); });
      g.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pon(!tapa.classList.contains('d-plegada')); } });
      tapa.addEventListener('click', e => { e.stopPropagation(); pon(false); g.focus({ preventScroll: true }); });
    });
  }
  // Bloques (decisión 415): la figura empieza con los bloques cerrados; pulsar uno lo abre en su sitio (su estado) y
  // el nombre de su zona lo vuelve a cerrar. «Abrir todos», el dibujo entero; «Recorrer» también lo abre entero.
  function bloques(fig) {
    const est = [...fig.querySelectorAll(':scope > .d-vista')];
    if (!est.length) return;
    let barra = fig.querySelector(':scope > .d-barra');
    if (!barra) {
      barra = document.createElement('div'); barra.className = 'd-barra';
      const tras = fig.querySelector(':scope > .d-ayuda') || fig.querySelector(':scope > .d-cabecera');
      if (tras) tras.after(barra); else fig.prepend(barra);
    }
    const bt = (texto, estado) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'd-rec d-bloques-b';
      b.dataset.ver = estado; b.textContent = texto; b.addEventListener('click', () => ver(estado, null, [b, null])); barra.appendChild(b); return b; };
    // ancla: lo pulsado (o la barra) se queda donde estaba en la pantalla, para que la página no salte al cambiar
    const visible = sel => sel && [...fig.querySelectorAll(sel)].find(x => x.getBoundingClientRect().width);
    const ver = (e, foco, ancla) => {
      const antes = ancla && ancla[0] ? ancla[0].getBoundingClientRect().top : null;
      est.forEach(d => { const era = d.hidden; d.hidden = d.dataset.vista !== e; if (era && !d.hidden && antes !== null) { d.classList.remove('d-entra'); void d.offsetWidth; d.classList.add('d-entra'); } });
      if (antes !== null) {
        const n = visible(ancla[1]) || (ancla[0].getBoundingClientRect().width ? ancla[0] : null);
        const d = n ? n.getBoundingClientRect().top - antes : 0;
        if (Math.abs(d) > 1) window.scrollBy(0, d);
      }
      fig.dataset.bloque = e;
      barra.querySelectorAll('.d-bloques-b').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.ver === e || (b.dataset.ver === 'cerrado' && e !== 'todo'))));
      if (foco) { const n = [...fig.querySelectorAll(foco)].find(x => x.getBoundingClientRect().width); if (n) n.focus({ preventScroll: true }); }
    };
    bt('Bloques cerrados', 'cerrado'); bt('Abrir todos', 'todo');
    const bloque = t => { const n = t.closest && t.closest('[data-nodo^="_b"]'); return n && fig.contains(n) ? n : null; };
    const nombre = t => { const g = t.closest && t.closest('.d-zona-g'); const d = g && g.closest('.d-vista'); return g && d && /^b\d+$/.test(d.dataset.vista) ? d : null; };
    // el foco sigue al bloque solo con el teclado; con el ratón no se mueve (sin anillo de foco)
    const abre = (n, tecla) => { const z = `.d-vista[data-vista="b${n.dataset.nodo.slice(2)}"] .d-zona-g`; ver('b' + n.dataset.nodo.slice(2), tecla && z, [n, z]); };
    const cierra = (d, tecla) => { const b = `.d-vista[data-vista="cerrado"] [data-nodo="_${d.dataset.vista}"]`;
      ver('cerrado', tecla && b, [[...d.querySelectorAll('.d-zona-g')].find(x => x.getBoundingClientRect().width), b]); };
    fig.addEventListener('click', e => {
      const n = bloque(e.target), d = !n && nombre(e.target);
      if (n) { e.stopPropagation(); abre(n); } else if (d) { e.stopPropagation(); cierra(d); }
      else if (e.target.closest && e.target.closest('.d-rec:not(.d-bloques-b):not(.d-nuevo-b)') && fig.dataset.bloque !== 'todo') ver('todo');
    }, true);
    fig.addEventListener('keydown', e => {
      if (e.key !== 'Enter' && e.key !== ' ') return;
      const n = bloque(e.target), d = !n && nombre(e.target);
      if (n) { e.preventDefault(); e.stopPropagation(); abre(n, true); } else if (d) { e.preventDefault(); e.stopPropagation(); cierra(d, true); }
    }, true);
    ver('cerrado');
  }
  const iniciar = () => { document.querySelectorAll('[data-diagrama]').forEach(montar); document.querySelectorAll('figure.d-gen').forEach(f => { esquinas(f); plegado(f); rotulos(f); zonas(f); bloques(f); }); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar();
})();
