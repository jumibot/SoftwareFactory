/* Herramientas del documento: columna lateral con el buscador y las notas, y barra del documento con su versión.
 * Biblioteca de la SF (tools/kit_documentos/), con lectura.js (opciones de lectura) y edicion.js (párrafos editables).
 * Lo usan documento_vision (.report-body con bloques .bloque) y documento_fundacional (main con secciones .seccion);
 * el estilo está en herramientas.css. Al cambiar cualquiera de estos archivos, se sube VERSION (aquí).
 * Las demás piezas usan window.herramientasDocumento (herramienta(), aplicar(), mostrar()…).
 * Procedencia: docs/referencias/procedencia/kit_documentos.md del repositorio de la SF.
 * · Pantalla grande (≥ 1400 px): cada herramienta va anclada en una columna a la derecha, de ancho ajustable, y se
 *   pliega con su flecha. La chincheta de la barra, a la derecha del engranaje, despega todas las herramientas como
 *   ventanas flotantes (se arrastran por la cabecera, se minimizan, doble clic las devuelve a su sitio) y las vuelve a anclar.
 * · Pantalla pequeña: minimizadas del todo; los botones «Buscar» y «Notas» las abren como panel inferior.
 * · Se recuerda por documento (localStorage con la ruta): modo, posición, ancho y plegado de cada herramienta.
 * Buscador: no distingue mayúsculas ni tildes, resalta, salta con Intro / Mayús+Intro, agrupa por sección y abre la
 *   sección plegada.
 * Notas: personales, de tres clases que el documento activa por separado: sobre un texto seleccionado («Anotar»,
 *   nota-texto), una por sección (nota-seccion) y una general de todo el documento (nota-global). En
 *   la columna se muestra sola la nota de la sección que se lee, plegada si está vacía,
 *   y lo escrito se ve también al final de su sección. Sin columna (ventanas flotantes o pantalla pequeña),
 *   cada nota vuelve a su sitio: una tarjeta editable al final de su sección, y la nota general y «Tus
 *   notas» al principio del documento; la ventana «Notas» no aparece. Si el documento
 *   no nombra ninguna de las tres, van las tres. Se guardan solas en el
 *   navegador; «Guardar» crea un documento anotado (copia del HTML con las notas dentro, en el bloque JSON
 *   #notas-documento) y sube la versión. Esa copia se puede pasar al autor: tools/kit_documentos/extraer_notas.py las lista.
 * Sin JavaScript no aparece nada; no se imprime. */
(function () {
  const VERSION = '1.10.0';
  const main = document.querySelector('main, .report-body');
  if (!main) return;
  const SECCION = 'details.seccion, details.bloque', TITULO = '.etiqueta, .bloque-title';
  const raiz = document.documentElement;
  const grande = matchMedia('(min-width: 1400px)');
  const suave = matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';
  const ruta = location.pathname;
  const leer = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (_) { return d; } };
  const escribir = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (_) {} };
  const CLAVE = 'documento-herramientas:' + ruta;
  let pref = leer(CLAVE, {});
  if (!pref || typeof pref !== 'object') pref = {};
  if (pref.modo && !pref.h) pref = { ancho: pref.ancho, h: { buscador: { modo: pref.modo, plegado: pref.plegado, minimizado: pref.minimizado, x: pref.x, y: pref.y } } };
  pref.h = pref.h || {};
  const guardarPref = () => escribir(CLAVE, pref);
  const abiertosAlCargar = [...document.querySelectorAll('details')].map(d => d.hasAttribute('open'));
  // Herramientas activas: las que pide el documento en <html data-herramientas="buscador notas …"> (catálogo en
  // tema_identidad.py); sin el atributo, las recomendadas para un documento del proyecto.
  const ACTIVAS = new Set((raiz.dataset.herramientas || 'buscador notas lectura fuentes cabecera tablas aviso').split(/[\s,]+/).filter(Boolean));
  if (ACTIVAS.has('ninguna')) return;
  // Cada herramienta (también plegado.js o fichas.js) puede registrar aquí cómo limpiar su estado de la copia guardada.
  const alCopiar = window.alCopiarDocumento = window.alCopiarDocumento || [];
  const datos = (() => { try { return JSON.parse(document.getElementById('notas-documento').textContent) || {}; } catch (_) { return {}; } })();

  // ── Columna y botones de pantalla pequeña ──
  const col = document.createElement('aside');
  col.className = 'columna-herramientas';
  col.setAttribute('aria-label', 'Herramientas del documento');
  col.innerHTML = '<div class="redim" title="Arrastra para cambiar el ancho" aria-hidden="true"></div>';
  document.body.appendChild(col);
  if (pref.ancho) raiz.style.setProperty('--ancho-columna', pref.ancho + 'px');
  let botones = document.querySelector('.menu-botones');
  if (!botones) { botones = document.createElement('div'); botones.className = 'botones-herramientas'; document.body.appendChild(botones); }

  const PIN = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" ' +
    'stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="17" x2="12" y2="22"/><path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9' +
    'A2 2 0 0 1 15 10.76V6h1a2 2 0 0 0 0-4H8a2 2 0 0 0 0 4h1v4.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24Z"/></svg>';
  const lista = [];
  let abiertaEstrecha = null;
  // Una sola chincheta para toda la barra de herramientas: ancla todas en la columna o las despega todas.
  const pinB = document.createElement('button');
  pinB.type = 'button'; pinB.className = 'dc-icono dc-anclar'; pinB.innerHTML = PIN;
  const enColumna = () => lista.some(t => modo(t) === 'columna');
  pinB.addEventListener('click', () => {
    const anclar = !enColumna();
    for (const t of lista) {
      if (!anclar && modo(t) === 'columna') {  // se despega donde estaba, para que no se tapen entre ellas
        const r = t.el.getBoundingClientRect();
        t.p.x = Math.max(8, Math.min(r.left - 24, innerWidth - 380)); t.p.y = Math.max(8, r.top);
      }
      t.p.modo = anclar ? 'columna' : 'flotante'; t.p.minimizado = false;
    }
    guardarPref(); aplicar();
  });
  // Va en la barra del documento, justo a la derecha del engranaje; sin barra, junto a los botones del menú.
  queueMicrotask(() => { if (!pinB.parentElement) botones.prepend(pinB); });

  function herramienta(id, titulo, rotulo, cuerpo) {
    const p = pref.h[id] = pref.h[id] || {};
    const el = document.createElement('section');
    el.className = 'herramienta herr-' + id;
    el.id = 'herr-' + id;
    el.setAttribute('aria-label', titulo);
    el.innerHTML =
      '<header class="herr-cabecera"><span class="herr-asa" aria-hidden="true" title="Arrastra para reubicar"></span><span class="herr-titulo">' + titulo + '</span><span class="herr-acciones">' +
      '<button type="button" class="herr-min" aria-label="Minimizar">–</button>' +
      '<button type="button" class="herr-plegar" aria-label="Plegar o desplegar"></button></span></header>' +
      '<div class="herr-cuerpo">' + cuerpo + '</div>';
    const abrir = document.createElement('button');
    abrir.type = 'button';
    abrir.className = 'abrir-herramienta';
    abrir.textContent = rotulo;
    abrir.setAttribute('aria-controls', el.id);
    const tras = [...botones.querySelectorAll(':scope > .abrir-herramienta')].pop();
    if (tras) tras.after(abrir); else botones.prepend(abrir);
    const t = { id, p, el, abrir, cab: el.querySelector('.herr-cabecera'), 
      minB: el.querySelector('.herr-min'), plegarB: el.querySelector('.herr-plegar'), q: s => el.querySelector(s) };
    t.minB.addEventListener('click', () => {
      if (!grande.matches) { abiertaEstrecha = null; aplicar(); abrir.focus(); return; }
      p.minimizado = !p.minimizado; guardarPref(); aplicar();
    });
    const plegar = () => { p.plegado = !p.plegado; guardarPref(); aplicar(); };
    t.plegarB.addEventListener('click', plegar);
    t.cab.addEventListener('click', e => { if (el.dataset.modo === 'columna' && !e.target.closest('button')) plegar(); });
    abrir.addEventListener('click', () => { abiertaEstrecha = abiertaEstrecha === t ? null : t; aplicar(); if (abiertaEstrecha === t && t.alAbrir) t.alAbrir(); });
    // Arrastrar la ventana flotante por su cabecera; doble clic la devuelve a su sitio.
    t.cab.addEventListener('pointerdown', e => {
      if (el.dataset.modo !== 'flotante' || !grande.matches || e.target.closest('button')) return;
      const r = el.getBoundingClientRect(), dx = e.clientX - r.left, dy = e.clientY - r.top;
      t.cab.setPointerCapture(e.pointerId);
      el.classList.add('arrastrando');
      const mover = ev => { p.x = ev.clientX - dx; p.y = ev.clientY - dy; colocar(t); };
      const soltar = () => { el.classList.remove('arrastrando'); t.cab.removeEventListener('pointermove', mover); guardarPref(); };
      t.cab.addEventListener('pointermove', mover);
      t.cab.addEventListener('pointerup', soltar, { once: true });
      t.cab.addEventListener('pointercancel', soltar, { once: true });
    });
    t.cab.addEventListener('dblclick', e => {
      if (el.dataset.modo !== 'flotante' || e.target.closest('button')) return;
      delete p.x; delete p.y; guardarPref(); colocar(t);
    });
    lista.push(t);
    return t;
  }
  // Una herramienta «en su sitio» (las notas) no flota: sin columna, su contenido va dentro del documento.
  const enSitio = t => !!t.enSitio && (!grande.matches || t.p.modo === 'flotante');
  const modo = t => enSitio(t) ? 'oculto' : grande.matches ? (t.p.modo || 'columna') : (abiertaEstrecha === t ? 'flotante' : 'oculto');
  let colocarBarra = () => {}, trasAplicar = () => {};
  function aplicar() {
    raiz.classList.toggle('herr-estrecho', !grande.matches);
    const enCol = lista.filter(t => modo(t) === 'columna');
    const actuales = [...col.querySelectorAll(':scope > .herramienta')];
    if (enCol.some((t, i) => actuales[i] !== t.el) || actuales.length !== enCol.length) enCol.forEach(t => col.appendChild(t.el));
    for (const t of lista) {
      const m = modo(t), el = t.el;
      el.dataset.modo = m;
      if (m !== 'columna' && el.parentElement !== document.body) document.body.appendChild(el);
      el.classList.toggle('plegada', m === 'columna' && !!t.p.plegado);
      el.classList.toggle('minimizada', m === 'flotante' && grande.matches && !!t.p.minimizado);
      t.plegarB.setAttribute('aria-expanded', String(!el.classList.contains('plegada')));
      t.minB.title = t.minB.ariaLabel = el.classList.contains('minimizada') ? 'Restaurar' : 'Minimizar';
      t.minB.textContent = el.classList.contains('minimizada') ? '+' : '–';
      t.abrir.setAttribute('aria-expanded', String(m === 'flotante'));
      t.abrir.hidden = enSitio(t);
      colocar(t);
    }
    raiz.classList.toggle('con-columna', enCol.length > 0);
    pinB.setAttribute('aria-pressed', String(enCol.length > 0));
    pinB.title = enCol.length ? 'Despegar las herramientas: ventanas flotantes' : 'Anclar las herramientas en la columna';
    pinB.setAttribute('aria-label', pinB.title);
    colocarBarra();
    trasAplicar();
  }
  // Posición de la ventana flotante: la guardada, dentro de la pantalla; si no hay, la de la hoja de estilos.
  function colocar(t) {
    const el = t.el, p = t.p;
    el.style.maxHeight = '';
    if (el.dataset.modo !== 'flotante' || !grande.matches || typeof p.x !== 'number') { el.style.left = el.style.top = ''; return; }
    const r = el.getBoundingClientRect(), arriba = Math.max(8, Math.min(p.y, innerHeight - 120));
    el.style.left = Math.max(8, Math.min(p.x, innerWidth - r.width - 8)) + 'px';
    el.style.top = arriba + 'px';
    el.style.maxHeight = (innerHeight - arriba - 16) + 'px';
  }
  // Mostrar una herramienta abierta y desplegada (para el atajo «/» o al crear una nota).
  function mostrar(t) {
    if (!grande.matches) abiertaEstrecha = t;
    else if (t.p.plegado || t.p.minimizado) { t.p.plegado = t.p.minimizado = false; guardarPref(); }
    aplicar();
  }
  grande.addEventListener('change', () => { abiertaEstrecha = null; aplicar(); });
  addEventListener('resize', () => lista.forEach(colocar));
  col.querySelector('.redim').addEventListener('pointerdown', e => {
    const tira = e.currentTarget;
    tira.setPointerCapture(e.pointerId); tira.classList.add('activo'); raiz.classList.add('redimensionando');
    const mover = ev => { pref.ancho = Math.round(Math.max(280, Math.min(560, innerWidth - ev.clientX))); raiz.style.setProperty('--ancho-columna', pref.ancho + 'px'); };
    const soltar = () => { tira.classList.remove('activo'); raiz.classList.remove('redimensionando'); tira.removeEventListener('pointermove', mover); guardarPref(); };
    tira.addEventListener('pointermove', mover);
    tira.addEventListener('pointerup', soltar, { once: true });
    tira.addEventListener('pointercancel', soltar, { once: true });
  });

  // ── Utilidades de texto y secciones ──
  const sinTildes = /[̀-ͯ]/g;
  const norm = s => s.normalize('NFD').replace(sinTildes, '').replace(/[  ]/g, ' ').toLowerCase();  // espacio duro o fino = espacio
  const corta = (s, n) => s.length > n ? s.slice(0, n - 1).trimEnd() + '…' : s;
  const tituloSec = s => s ? (s.querySelector(TITULO)?.textContent || '').trim() : 'Inicio';
  const abrirHasta = el => { for (let d = el.closest('details'); d; d = d.parentElement && d.parentElement.closest('details')) d.open = true; };
  function destellar(el) {  // marca un momento la sección a la que se salta
    const sec = el.closest(SECCION) || el.closest('details');
    if (!sec) return;
    sec.classList.remove('destello-seccion'); void sec.offsetWidth; sec.classList.add('destello-seccion');
    setTimeout(() => sec.classList.remove('destello-seccion'), 1300);
  }
  // Un enlace interno o un #ancla en la dirección abren la sección de destino (el fundacional ya lo hace en plegado.js).
  const destino = h => { try { return h.length > 1 && document.getElementById(decodeURIComponent(h.slice(1))); } catch (_) { return null; } };
  document.addEventListener('click', e => { const a = e.target.closest && e.target.closest('a[href^="#"]'); const d = a && destino(a.getAttribute('href')); if (d) abrirHasta(d); });
  const alAncla = () => { const d = destino(location.hash); if (d) { abrirHasta(d); d.scrollIntoView(); } };
  addEventListener('hashchange', alAncla);
  alAncla();
  // Impresión con todo abierto, si el documento no lo resuelve ya (el fundacional lo hace en plegado.js).
  if (!document.querySelector('.plegar')) {
    let antes = null;
    const todos = () => [...document.querySelectorAll('details')];
    addEventListener('beforeprint', () => { antes = todos().map(d => d.open); todos().forEach(d => { d.open = true; }); });
    addEventListener('afterprint', () => { if (antes) todos().forEach((d, i) => { d.open = antes[i] ?? d.open; }); antes = null; });
  }
  const fuera = n => n.parentElement.closest('script, style, button, .herramienta, .buscador, .leyenda-doc, .ed-meta, .ed-barra, .bocadillo-fuente, .nota-espejo, .nt-sitio, .nt-sitio-inicio');
  function mapa(el) {  // el texto de un elemento y, por cada nodo de texto, dónde empieza
    const nodos = []; let texto = '';
    const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, { acceptNode: n => fuera(n) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
    while (w.nextNode()) { nodos.push([w.currentNode, texto.length]); texto += w.currentNode.data; }
    return { texto, nodos };
  }

  // ── Buscador ──
  if (ACTIVAS.has('buscador')) {
  const bus = herramienta('buscador', 'Buscar en el documento', 'Buscar',
    '<label class="bd-campo"><span class="bd-oculto">Texto que buscar</span>' +
    '<input type="search" name="buscar-documento" autocomplete="off" spellcheck="false" placeholder="Palabra, nombre o cifra…"></label>' +
    '<div class="bd-navegar"><span class="bd-cuenta" role="status" aria-live="polite"></span>' +
    '<button type="button" class="bd-ant" aria-label="Resultado anterior" disabled>↑</button>' +
    '<button type="button" class="bd-sig" aria-label="Resultado siguiente" disabled>↓</button></div>' +
    '<p class="bd-ayuda">/ para buscar · Intro, siguiente · Mayús+Intro, anterior · Esc, borrar</p>' +
    '<ol class="bd-resultados"></ol>');
  bus.el.classList.add('buscador-doc');
  const campo = bus.q('input'), cuenta = bus.q('.bd-cuenta'), ant = bus.q('.bd-ant'), sig = bus.q('.bd-sig'), resultados = bus.q('.bd-resultados');
  bus.alAbrir = () => campo.focus();
  const MAX = 500;
  let marcas = [], actual = -1;
  function limpiar() {
    for (const m of main.querySelectorAll('mark.bd-hit')) {
      const padre = m.parentNode;
      padre.replaceChild(document.createTextNode(m.textContent), m);
      padre.normalize();
    }
    marcas = []; actual = -1;
  }
  function buscar() {
    limpiar();
    const q = norm(campo.value.trim());
    if (q.length >= 2) {
      for (const [nodo] of mapa(main).nodos) {
        if (marcas.length >= MAX) break;
        if (!nodo.data.trim()) continue;
        // Texto normalizado con el mapa a las posiciones originales (una letra con tilde puede ocupar dos).
        let n = '';
        const pos = [];
        for (let i = 0; i < nodo.data.length; i++) for (const c of norm(nodo.data[i])) { n += c; pos.push(i); }
        const trozos = [];
        for (let p = n.indexOf(q); p !== -1; p = n.indexOf(q, p + q.length)) trozos.push([pos[p], pos[p + q.length - 1] + 1]);
        const nuevas = [];
        for (let k = trozos.length - 1; k >= 0; k--) {
          const [a, b] = trozos[k];
          const trozo = nodo.splitText(a);
          trozo.splitText(b - a);
          const m = document.createElement('mark');
          m.className = 'bd-hit';
          trozo.parentNode.replaceChild(m, trozo);
          m.appendChild(trozo);
          nuevas.unshift(m);
        }
        marcas.push(...nuevas);
      }
    }
    pintar();
  }
  function pintar() {
    const n = marcas.length;
    cuenta.textContent = !campo.value.trim() ? '' : n ? `${n}${n >= MAX ? '+' : ''} resultados` : 'Sin resultados';
    cuenta.classList.toggle('vacia', !!campo.value.trim() && !n);
    ant.disabled = sig.disabled = !n;
    resultados.textContent = '';
    const grupos = new Map();
    marcas.forEach((m, i) => {
      const sec = m.closest(SECCION);
      if (!grupos.has(sec)) grupos.set(sec, []);
      grupos.get(sec).push(i);
    });
    for (const [sec, idx] of grupos) {
      const li = document.createElement('li'), b = document.createElement('button');
      b.type = 'button';
      const titulo = document.createElement('span');
      titulo.className = 'bd-seccion';
      titulo.textContent = `${tituloSec(sec)} · ${idx.length}`;
      b.append(titulo, fragmento(marcas[idx[0]]));
      b.dataset.desde = idx[0]; b.dataset.hasta = idx[idx.length - 1];
      b.addEventListener('click', () => { ir(idx[0]); if (!grande.matches) { abiertaEstrecha = null; aplicar(); } });
      li.appendChild(b);
      resultados.appendChild(li);
    }
  }
  function fragmento(m) {
    const bloque = m.closest('p, li, dd, dt, h2, h3, h4, td, blockquote') || m.parentElement;
    const antes = document.createRange(), despues = document.createRange();
    antes.setStart(bloque, 0); antes.setEndBefore(m);
    despues.setStartAfter(m); despues.setEnd(bloque, bloque.childNodes.length);
    const a = antes.toString(), d = despues.toString();
    const f = document.createElement('span');
    f.className = 'bd-fragmento';
    const fuerte = document.createElement('b');
    fuerte.textContent = m.textContent;
    f.append(a.length > 60 ? '…' + a.slice(-60) : a, fuerte, d.length > 80 ? d.slice(0, 80) + '…' : d);
    return f;
  }
  function ir(i) {
    if (!marcas.length) return;
    actual = (i + marcas.length) % marcas.length;
    marcas.forEach((m, k) => m.classList.toggle('actual', k === actual));
    const m = marcas[actual];
    abrirHasta(m);
    m.scrollIntoView({ block: 'center', behavior: suave });
    destellar(m);
    for (const b of resultados.querySelectorAll('button')) {  // el grupo del resultado actual, marcado y a la vista
      const activo = actual >= +b.dataset.desde && actual <= +b.dataset.hasta;
      b.classList.toggle('activo', activo);
      if (activo) b.scrollIntoView({ block: 'nearest' });
    }
    cuenta.textContent = `${actual + 1} de ${marcas.length}${marcas.length >= MAX ? '+' : ''}`;
  }
  let espera;
  campo.addEventListener('input', () => { clearTimeout(espera); espera = setTimeout(buscar, 150); });
  campo.addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); clearTimeout(espera); if (!marcas.length) buscar(); ir(actual + (e.shiftKey ? -1 : 1)); }
    else if (e.key === 'Escape') {
      if (campo.value) { campo.value = ''; buscar(); }
      else if (!grande.matches) { abiertaEstrecha = null; aplicar(); bus.abrir.focus(); }
    }
  });
  ant.addEventListener('click', () => ir(actual - 1));
  sig.addEventListener('click', () => ir(actual + 1));
  document.addEventListener('keydown', e => {
    // F3 / Mayús+F3 y Ctrl+G / Ctrl+Mayús+G: resultado siguiente o anterior, desde cualquier sitio.
    if (e.key === 'F3' || ((e.ctrlKey || e.metaKey) && (e.key === 'g' || e.key === 'G'))) {
      if (!campo.value.trim()) return;
      e.preventDefault();
      if (!marcas.length) buscar();
      ir(actual + (e.shiftKey ? -1 : 1));
      return;
    }
    if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.target.closest && e.target.closest('input, textarea, select, [contenteditable]')) return;
    e.preventDefault();
    mostrar(bus);
    campo.focus();
    campo.select();
  });
  alCopiar.push(c => c.querySelectorAll('mark.bd-hit').forEach(m => m.replaceWith(...m.childNodes)));
  }

  // ── Notas y barra del documento (la barra también sirve a la edición de párrafos) ──
  const CON_NOTAS = ACTIVAS.has('notas');
  // Clases de nota. Un documento que no nombra ninguna (anterior a la 1.3.0) las tiene todas.
  const CLASES = ['nota-texto', 'nota-seccion', 'nota-global'];
  const TODAS = !CLASES.some(c => ACTIVAS.has(c));
  const N_TEXTO = TODAS || ACTIVAS.has('nota-texto'), N_SECCION = TODAS || ACTIVAS.has('nota-seccion'), N_GLOBAL = TODAS || ACTIVAS.has('nota-global');
  // «Convertir en párrafo» es su propia opción (nota-a-parrafo); en los documentos anteriores a la 1.3.0 iba con «edicion».
  const ANTIGUO = TODAS && !ACTIVAS.has('nota-a-parrafo');
  const CONVIERTE = CON_NOTAS && (ACTIVAS.has('nota-a-parrafo') || (ANTIGUO && ACTIVAS.has('edicion')));
  let notasT = null, autorEl = null;
  if (CON_NOTAS || ACTIVAS.has('edicion')) {

  // ── Barra del documento: versión, estado de las notas, versión de las herramientas y «Guardar» ──
  let version = Number(datos.version) || 1;
  const TITULO_GUARDAR = ACTIVAS.has('mismo-archivo') ? 'Guarda el documento con tus cambios en el mismo archivo' : 'Guarda una copia del documento con tus notas y cambios, para conservarla o compartirla';
  const barra = document.createElement('div');
  barra.className = 'barra-doc';
  barra.innerHTML = '<span class="dc-ver">versión <b>v' + version + '</b>' +
    '<span class="dc-kit" title="Versión del kit de herramientas del documento (buscador, notas, lectura…) con que funciona esta página">kit v' + VERSION + '</span></span>' +
    '<span class="dc-estado" role="status" aria-live="polite"></span>' +
    '<button type="button" class="dc-guardar" title="' + TITULO_GUARDAR + '">Guardar</button>';
  barra.prepend(pinB);  // lectura.js pone el engranaje delante: queda engranaje, chincheta

  // Con la columna, «Plegar todo» e «Imprimir / PDF» del menú pasan a la barra como iconos, a la izquierda de «Guardar»
  // (el menú se queda vacío y se oculta). Son atajos a los botones originales, que siguen en el menú sin columna.
  const iconos = document.createElement('span');
  iconos.className = 'dc-iconos';
  barra.querySelector('.dc-guardar').before(iconos);
  const SVG = d => '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>';
  const atajo = (orig, svg) => {
    if (!orig) return null;
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'dc-icono dc-atajo'; b.innerHTML = svg;
    b.addEventListener('click', () => orig.click());
    iconos.append(b);
    return b;
  };
  const oPlegar = document.querySelector('.menu .plegar'), oImprimir = document.querySelector('.menu .imprimir');
  const PLEGADO = SVG('<path d="m7 20 5-5 5 5"/><path d="m7 4 5 5 5-5"/>'), DESPLEGADO = SVG('<path d="m7 15 5 5 5-5"/><path d="m7 9 5-5 5 5"/>');
  const aPlegar = atajo(oPlegar, PLEGADO);
  if (aPlegar) {
    const rotular = () => { const t = oPlegar.textContent.trim(); aPlegar.title = t; aPlegar.setAttribute('aria-label', t);
      aPlegar.innerHTML = /^Desplegar/.test(t) ? DESPLEGADO : PLEGADO; };
    new MutationObserver(rotular).observe(oPlegar, { childList: true, characterData: true, subtree: true });
    rotular();
  }
  const aImprimir = atajo(oImprimir, SVG('<path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>'));
  if (aImprimir) { aImprimir.title = 'Imprimir / PDF'; aImprimir.setAttribute('aria-label', 'Imprimir o guardar como PDF'); }
  const menu = document.querySelector('.menu-dentro');
  // Sin columna, la barra va al menú o a la franja bajo la cabecera; si el documento no tiene franja (no lleva
  // línea de estado), se crea una para la barra, de modo que la chincheta y «Guardar» siguen arriba, a la vista.
  const franja = () => {
    let f = document.querySelector('.report-header');
    if (!f) {
      f = document.createElement('div'); f.className = 'report-header franja-barra';
      const cab = document.querySelector('.site-header');
      if (cab) cab.after(f); else document.body.prepend(f);
    }
    return f;
  };
  const casa = () => { if (menu) menu.prepend(barra); else franja().append(barra); };
  const nav = document.querySelector('nav.menu');
  colocarBarra = () => {
    // Con la columna, si al menú no le quedan enlaces (plegar e imprimir pasan a la barra), se oculta.
    if (nav) nav.classList.toggle('menu-vacio', raiz.classList.contains('con-columna') && !nav.querySelector('a'));
    if (raiz.classList.contains('con-columna')) { if (barra.parentElement !== col) col.insertBefore(barra, col.querySelector(':scope > .herramienta')); }
    else if (barra.parentElement === col || !barra.parentElement) casa();
  };
  colocarBarra();
  const verEl = barra.querySelector('.dc-ver b'), estadoEl = barra.querySelector('.dc-estado');

  // ── Notas ──
  const CLAVE_NOTAS = 'documento-notas:' + ruta, CLAVE_AUTOR = 'documento-notas:autor';
  const local = (CON_NOTAS && leer(CLAVE_NOTAS, null)) || {};
  const incrustadas = CON_NOTAS && Array.isArray(datos.notas) ? datos.notas : [];
  const borradas = new Set(local.borradas || []);
  const porId = new Map();
  for (const n of incrustadas) if (!borradas.has(n.id)) porId.set(n.id, n);
  for (const n of local.notas || []) { const o = porId.get(n.id); if (!o || (n.modificada || '') >= (o.modificada || '')) porId.set(n.id, n); }
  // Una nota sin texto ni cita no es un cambio: no cuenta para el led y no se conserva al recargar
  const util = n => !!((n.texto || '').trim() || n.cita);
  let notas = [...porId.values()].filter(util);
  const firma = l => JSON.stringify(l.filter(util).map(n => [n.id, n.texto, n.cita || '', n.seccion || '', n.global ? 1 : 0]).sort());
  let guardado = local.guardado && local.guardado.firma ? local.guardado : { firma: firma(incrustadas), fecha: datos.guardado || '', version };
  const fecha = iso => { try { return new Date(iso).toLocaleString('es-ES', { dateStyle: 'short', timeStyle: 'short' }); } catch (_) { return iso; } };
  let otrosCambios = false;  // otras herramientas que cambian el documento llaman a marcarCambiosDocumento()
  window.marcarCambiosDocumento = () => { otrosCambios = true; estado(); };
  // Aviso al cerrar: solo si hay cambios que se perderían (las notas ya quedan en el navegador; los párrafos, no).
  if (ACTIVAS.has('aviso')) addEventListener('beforeunload', e => { if (otrosCambios) { e.preventDefault(); e.returnValue = ''; } });
  function estado() {
    const sucio = otrosCambios || firma(notas) !== guardado.firma;
    barra.classList.toggle('sucio', sucio);
    // Con cambios, el aviso es el led rojo del botón; el texto queda solo para lectores de pantalla
    const bt = barra.querySelector('.dc-guardar');
    bt.setAttribute('aria-label', sucio ? 'Guardar: hay cambios sin guardar' : 'Guardar');
    estadoEl.textContent = sucio ? 'Hay cambios sin guardar'
      : guardado.fecha ? `Guardado${guardado.version !== version ? ' como v' + guardado.version : ''} el ${fecha(guardado.fecha)}` : 'Sin cambios pendientes';
    bt.title = estadoEl.textContent + ' · ' + TITULO_GUARDAR;  // en la columna el estado solo se ve aquí
  }
  function persistir() { if (CON_NOTAS) escribir(CLAVE_NOTAS, { notas, borradas: [...borradas], guardado }); estado(); }

  if (CON_NOTAS) {
  // Sin botones para crear notas. La columna muestra sola la nota de la
  // sección que se lee (y las de las secciones que la contienen), cada una con su cabecera, plegada si está vacía; lo
  // escrito se ve también, solo para leer, al final de su sección. La nota general va arriba y «Todas las notas»
  // resume las demás.
  notasT = herramienta('notas', 'Notas personales', 'Notas',
    '<div class="nt-general-zona"></div><div class="nt-foco"></div>' +
    '<p class="nt-vacio">' + (N_SECCION ? 'Abre o lee una sección para anotarla.' : 'Selecciona un texto de la sección y pulsa «Anotar» para comentarlo.') + '</p>' +
    '<section class="nt-tarjeta nt-todas plegada"><button type="button" class="nt-tarjeta-cab" aria-expanded="false" title="Tu nombre y todas tus notas">' +
    '<span class="herr-titulo">Tus notas <span class="nt-cuantas"></span></span><span class="nt-flecha" aria-hidden="true"></span></button>' +
    '<div class="nt-tarjeta-cuerpo">' +
    '<label class="nt-campo">Tu nombre <input type="text" name="autor-notas" autocomplete="name" placeholder="Para firmar tus notas"></label>' +
    '<ol class="nt-resumen"></ol>' +
    '<p class="nt-ayuda">' + (N_TEXTO ? 'Para comentar un texto, selecciónalo y pulsa «Anotar». ' : '') +
    'Las notas quedan en este navegador; con «Guardar» las llevas a una copia del documento para conservarlas o compartirlas.</p></div></section>');
  autorEl = notasT.q('input');
  notasT.enSitio = true;
  const generalEl = notasT.q('.nt-general-zona'), focoEl = notasT.q('.nt-foco'), vacioEl = notasT.q('.nt-vacio');
  const todasEl = notasT.q('.nt-todas'), resumenEl = notasT.q('.nt-resumen'), cuantasEl = notasT.q('.nt-cuantas');
  autorEl.value = leer(CLAVE_AUTOR, '');
  todasEl.querySelector('.nt-tarjeta-cab').addEventListener('click', e => {
    const v = todasEl.classList.toggle('plegada'); e.currentTarget.setAttribute('aria-expanded', String(!v));
  });
  autorEl.addEventListener('input', () => escribir(CLAVE_AUTOR, autorEl.value.trim()));
  // Sin columna, las notas van en su sitio: la general y «Tus notas», al principio del documento.
  function sitio() { return enSitio(notasT); }  // función: la usa también el arranque, fuera de este bloque
  const inicioSitio = document.createElement('div');
  inicioSitio.className = 'nt-sitio-inicio';
  function moverZonas() {
    if (sitio()) { main.prepend(inicioSitio); inicioSitio.append(generalEl, todasEl); return; }
    const cuerpo = notasT.q('.herr-cuerpo');
    cuerpo.prepend(generalEl); cuerpo.append(todasEl);
    inicioSitio.remove();
    main.querySelectorAll('.nt-sitio').forEach(x => x.remove());
  }
  alCopiar.push(c => c.querySelectorAll('.nt-sitio, .nt-sitio-inicio').forEach(x => x.remove()));

  const secciones = () => [...main.querySelectorAll(SECCION)];
  const raizNota = n => (n.seccion && document.getElementById(n.seccion)?.matches(SECCION)) ? document.getElementById(n.seccion) : main;
  function envolver(r, a, b, id) {  // marca el texto entre las posiciones a y b de r, nodo a nodo
    for (const [n, ini] of mapa(r).nodos) {
      const fin = ini + n.data.length;
      if (fin <= a || ini >= b) continue;
      const s = Math.max(a, ini) - ini, e = Math.min(b, fin) - ini;
      if (!n.data.slice(s, e).trim()) continue;  // sin marcas en los huecos entre celdas o elementos
      let nodo = n;
      if (e < nodo.data.length) nodo.splitText(e);
      if (s > 0) nodo = nodo.splitText(s);
      const m = document.createElement('mark');
      m.className = 'nota-cita'; m.dataset.nota = id;
      nodo.parentNode.replaceChild(m, nodo); m.appendChild(nodo);
    }
  }
  function localizar(n) {
    if (!n.cita) return true;
    const r = raizNota(n), { texto } = mapa(r), pos = [];
    for (let p = texto.indexOf(n.cita); p !== -1; p = texto.indexOf(n.cita, p + 1)) pos.push(p);
    if (!pos.length) return false;
    const a = pos[Math.min(n.ocurrencia || 0, pos.length - 1)];
    envolver(r, a, a + n.cita.length, n.id);
    return true;
  }
  const perdidas = new Set();
  for (const n of notas) if (!localizar(n)) perdidas.add(n.id);
  const quitarMarcas = id => main.querySelectorAll(`mark.nota-cita[data-nota="${id}"]`).forEach(m => { const p = m.parentNode; m.replaceWith(...m.childNodes); p.normalize(); });

  // ── La sección en foco: la que se abre o se pulsa; al desplazarse, la que ocupa la parte alta de la pantalla ──
  let secActual = null;
  const cadena = s => { const c = []; for (let x = s; x; x = x.parentElement && x.parentElement.closest(SECCION)) c.unshift(x); return c; };
  const enFoco = () => secActual ? cadena(secActual).map(x => x.id).join('|') : '';
  let pintado = null;
  const escribiendo = () => focoEl.contains(document.activeElement) || generalEl.contains(document.activeElement);
  notasT.el.classList.add('por-seccion');  // en la columna, cada nota es su propia tarjeta
  function actualizarFoco() { if (!sitio() && enFoco() !== pintado && !escribiendo()) pintarNotas(); }
  function seguirSeccion() {
    let s = null;
    const todas = secciones().filter(x => !x.parentElement.closest('details:not([open])'));
    for (const x of todas) { if (x.getBoundingClientRect().top < innerHeight * 0.35) s = x; else break; }
    if (!s) s = todas.find(x => x.getBoundingClientRect().top < innerHeight) || null;  // la primera ya a la vista
    if (s && s.tagName === 'DETAILS' && !s.open) s = s.parentElement && s.parentElement.closest(SECCION);
    secActual = s;
    actualizarFoco();
  }
  let rafSec = 0;
  addEventListener('scroll', () => { cancelAnimationFrame(rafSec); rafSec = requestAnimationFrame(seguirSeccion); }, { passive: true });
  const enfocarSeccion = s => { if (!s) return; secActual = s; actualizarFoco(); };
  main.addEventListener('click', e => { if (!e.target.closest('.nota-espejo')) enfocarSeccion(e.target.closest(SECCION)); });
  main.addEventListener('toggle', e => { if (e.target.matches && e.target.matches(SECCION)) { if (e.target.open) enfocarSeccion(e.target); else seguirSeccion(); } }, true);

  // ── Tarjetas de nota ──
  const abiertas = new Map();  // cabecera de tarjeta → desplegada; sin dato, desplegada si tiene texto
  const conTexto = n => !!(n.texto || '').trim();
  function pie(n, ref) {  // ref() da la nota cuando se crea al escribir
    const pie = document.createElement('div');
    pie.className = 'nt-pie';
    const quien = document.createElement('span');
    if (n && n.cita) quien.textContent = [n.autor, n.creada && fecha(n.creada)].filter(Boolean).join(' · ');
    pie.append(quien);
    const acciones = document.createElement('span');
    acciones.className = 'nt-acciones';
    if (CONVIERTE && !(n ? n.global : ref.molde.global)) {
      const cv = document.createElement('button');
      cv.type = 'button'; cv.className = 'nt-convertir'; cv.textContent = 'Convertir en párrafo';
      cv.title = 'Añade la nota al documento como párrafo, con la fecha de hoy, tras el texto anotado o al final de la sección; la nota se borra';
      cv.disabled = !(n && conTexto(n));
      cv.addEventListener('click', () => { const x = ref.nota(); if (x) convertir(x); });
      acciones.append(cv);
    }
    if (!n || !n.cita) { pie.append(acciones); return acciones.children.length ? pie : null; }
    const bo = document.createElement('button');
    bo.type = 'button'; bo.className = 'nt-borrar'; bo.textContent = 'Borrar';
    let confirmar = 0;
    bo.addEventListener('click', () => {
      if (!confirmar) { bo.textContent = '¿Borrar la nota?'; confirmar = setTimeout(() => { confirmar = 0; bo.textContent = 'Borrar'; }, 3000); return; }
      clearTimeout(confirmar); borrar(n.id);
    });
    acciones.append(bo);
    pie.append(acciones);
    return pie;
  }
  // Una nota en su tarjeta. La nota propia de una sección (o la general) puede no existir aún: se crea al escribir.
  function nota(n, molde) {
    const li = document.createElement('li');
    li.className = 'nt-nota';
    if (n) li.dataset.id = n.id;
    if (n && n.cita) {
      const c = document.createElement('button');
      c.type = 'button';
      c.className = 'nt-cita' + (perdidas.has(n.id) ? ' perdida' : '');
      c.textContent = '«' + corta(n.cita.replace(/\s+/g, ' '), 160) + '»';
      c.title = perdidas.has(n.id) ? 'Este texto ya no está en esta versión del documento' : 'Ir al texto anotado';
      c.addEventListener('click', () => irNota(n.id));
      li.appendChild(c);
    }
    const ta = document.createElement('textarea');
    ta.name = 'nota-' + (n ? n.id : (molde.global ? 'general' : molde.seccion || 'inicio'));
    ta.rows = 3;
    ta.setAttribute('aria-label', n && n.cita ? 'Comentario sobre el texto' : molde && molde.global ? 'Nota general del documento' : 'Nota de la sección');
    ta.placeholder = n && n.cita ? 'Tu comentario sobre este texto' : (n || molde).global ? 'Tu valoración de todo el documento' : 'Tu nota sobre esta sección';
    ta.value = n ? n.texto || '' : '';
    ta.addEventListener('input', () => {
      if (!n) { n = nueva(molde); li.dataset.id = n.id; }
      n.texto = ta.value; n.modificada = new Date().toISOString(); n.autor = autorEl.value.trim() || n.autor || '';
      const cv = li.querySelector('.nt-convertir'); if (cv) cv.disabled = !ta.value.trim();
      persistir(); espejo(n); pintarResumen();
    });
    ta.addEventListener('blur', () => {
      if (n && !ta.value.trim() && !n.cita) {
        if (sitio() && molde) { quitar(n.id); n = null; delete li.dataset.id; }  // sin repintar: el foco puede estar ya en otra nota
        else borrar(n.id);
      } else if (enFoco() !== pintado) setTimeout(actualizarFoco);
    });
    if (!(n && n.cita)) ta.classList.add('nt-amplia');
    li.appendChild(ta);
    const pp = pie(n, { molde, nota: () => n });
    if (pp) li.appendChild(pp);
    return li;
  }
  function tarjeta(clave, titulo, items, ayuda) {
    const t = document.createElement('section');
    t.className = 'nt-tarjeta';
    const cab = document.createElement('button');
    cab.type = 'button'; cab.className = 'nt-tarjeta-cab'; cab.title = ayuda;
    const tt = document.createElement('span'); tt.className = 'herr-titulo'; tt.textContent = titulo;
    const fl = document.createElement('span'); fl.className = 'nt-flecha'; fl.setAttribute('aria-hidden', 'true');
    cab.append(tt, fl);
    const cuerpo = document.createElement('ol');
    cuerpo.className = 'nt-lista nt-tarjeta-cuerpo';
    items.forEach(x => cuerpo.appendChild(x));
    const lleno = items.some(li => li.dataset.id && conTexto(notas.find(n => n.id === li.dataset.id) || {}));
    const abierta = abiertas.has(clave) ? abiertas.get(clave) : lleno;
    t.classList.toggle('plegada', !abierta);
    cab.setAttribute('aria-expanded', String(abierta));
    cab.addEventListener('click', () => {
      const v = t.classList.toggle('plegada'); abiertas.set(clave, !v); cab.setAttribute('aria-expanded', String(!v));
      if (!v) { const ta = t.querySelector('textarea'); if (ta && !ta.value) ta.focus(); }
    });
    t.append(cab, cuerpo);
    return t;
  }
  function pintarNotas() {
    if (sitio()) { pintarEnSitio(); return; }
    pintado = enFoco();
    notasT.el.classList.toggle('con-notas', notas.length > 0);
    generalEl.textContent = '';
    if (N_GLOBAL) {
      const g = notas.filter(n => n.global);
      generalEl.appendChild(tarjeta('\u0000global', 'Nota general del documento', g.length ? g.map(n => nota(n)) : [nota(null, { global: true, seccion: '', titulo: 'Todo el documento' })],
        'La valoración de conjunto, que no es de ninguna sección'));
    }
    focoEl.textContent = '';
    const enCadena = secActual ? cadena(secActual) : [];
    for (const s of enCadena) {
      const propias = notas.filter(n => !n.global && !n.cita && n.seccion === s.id);
      const citas = notas.filter(n => n.cita && n.seccion === s.id);
      const items = [];
      if (N_SECCION) items.push(...(propias.length ? propias.map(n => nota(n)) : [nota(null, { seccion: s.id, titulo: tituloSec(s) })]));
      else items.push(...propias.map(n => nota(n)));  // notas de sección de copias que aún las tenían
      items.push(...citas.sort((a, b) => (a.creada || '').localeCompare(b.creada || '')).map(n => nota(n)));
      if (!items.length) continue;
      focoEl.appendChild(tarjeta(s.id, 'Nota · ' + corta(tituloSec(s), 60), items, 'La nota de esta sección y lo anotado en ella'));
    }
    vacioEl.hidden = focoEl.children.length > 0;
    pintarResumen();
    espejos();
  }
  // Sin columna: un rótulo pequeño, el campo abierto y las acciones; sin caja ni plegado.
  function bloqueSitio(titulo, items) {
    const b = document.createElement('section');
    b.className = 'nt-sitio-bloque';
    const t = document.createElement('div');
    t.className = 'nt-sitio-t'; t.textContent = titulo;
    const ol = document.createElement('ol');
    ol.className = 'nt-lista';
    items.forEach(x => ol.appendChild(x));
    b.append(t, ol);
    return b;
  }
  function pintarEnSitio() {
    pintado = null;
    notasT.el.classList.toggle('con-notas', notas.length > 0);
    generalEl.textContent = '';
    if (N_GLOBAL) {
      const g = notas.filter(n => n.global), molde = { global: true, seccion: '', titulo: 'Todo el documento' };
      generalEl.appendChild(bloqueSitio('Nota general del documento', g.length ? g.map(n => nota(n, molde)) : [nota(null, molde)]));
    }
    main.querySelectorAll('.nt-sitio').forEach(x => x.remove());
    for (const s of secciones()) {
      const molde = { seccion: s.id, titulo: tituloSec(s) };
      const propias = notas.filter(n => !n.global && !n.cita && n.seccion === s.id);
      const citas = notas.filter(n => n.cita && n.seccion === s.id);
      const items = [];
      if (N_SECCION) items.push(...(propias.length ? propias.map(n => nota(n, molde)) : [nota(null, molde)]));
      else items.push(...propias.map(n => nota(n, molde)));
      items.push(...citas.sort((a, b) => (a.creada || '').localeCompare(b.creada || '')).map(n => nota(n)));
      if (!items.length) continue;
      const z = document.createElement('div');
      z.className = 'nt-sitio';
      z.appendChild(bloqueSitio('Nota · ' + corta(tituloSec(s), 60), items));
      (s.querySelector(':scope > .seccion-cuerpo, :scope > .bloque-content') || s).appendChild(z);
    }
    pintarResumen();
    espejos();
  }
  // «Todas las notas»: las que tienen texto o cita, fuera de la nota general, para ir a cada una.
  function pintarResumen() {
    const pos = (() => { const idx = new Map(secciones().map((s, i) => [s.id, i])); return n => idx.has(n.seccion) ? idx.get(n.seccion) : -1; })();
    const lista = notas.filter(n => !n.global && (conTexto(n) || n.cita)).sort((a, b) => pos(a) - pos(b) || (a.creada || '').localeCompare(b.creada || ''));
    cuantasEl.textContent = lista.length ? '· ' + lista.length : '';
    resumenEl.textContent = '';
    let grupo = null;
    for (const n of lista) {
      if ((n.seccion || '') !== grupo) {
        grupo = n.seccion || '';
        const g = document.createElement('li'); g.className = 'nt-grupo';
        const sec = n.seccion && document.getElementById(n.seccion);
        g.textContent = sec ? tituloSec(sec) : (n.titulo || 'Inicio');
        resumenEl.appendChild(g);
      }
      const li = document.createElement('li');
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'nt-ir';
      b.textContent = (n.cita ? '«' + corta(n.cita.replace(/\s+/g, ' '), 60) + '» ' : '') + corta((n.texto || '').replace(/\s+/g, ' ') || '(sin comentario)', 90);
      b.title = 'Ir a esta nota';
      b.addEventListener('click', () => ir(n));
      li.appendChild(b); resumenEl.appendChild(li);
    }
  }
  function ir(n) {
    const sec = n.seccion && document.getElementById(n.seccion);
    if (n.cita && main.querySelector(`mark.nota-cita[data-nota="${n.id}"]`)) irNota(n.id);
    else if (sec) { abrirHasta(sec); sec.scrollIntoView({ block: 'start', behavior: suave }); destellar(sec); }
    if (sec) { secActual = sec; abiertas.set(sec.id, true); pintarNotas(); enfocarNota(n.id); }
  }

  // ── Lo escrito en una nota de sección se ve también al final de su sección, solo para leer ──
  function espejo(n) {
    if (n.global || n.cita) return;
    const sec = n.seccion && document.getElementById(n.seccion);
    let e = main.querySelector(`.nota-espejo[data-nota="${n.id}"]`);
    if (!sec || !conTexto(n) || sitio()) { if (e) e.remove(); return; }
    if (!e) {
      e = document.createElement('aside');
      e.className = 'nota-espejo'; e.dataset.nota = n.id; e.tabIndex = 0;
      e.title = 'Tu nota de esta sección: se escribe en la columna de notas';
      e.innerHTML = '<div class="nota-espejo-t"></div><div class="nota-espejo-x"></div>';
      e.addEventListener('click', () => { mostrar(notasT); secActual = sec; abiertas.set(sec.id, true); pintarNotas(); enfocarNota(n.id); });
      (sec.querySelector(':scope > .seccion-cuerpo, :scope > .bloque-content') || sec).appendChild(e);
    }
    e.querySelector('.nota-espejo-t').textContent = 'Tu nota' + (n.autor ? ' · ' + n.autor : '');
    e.querySelector('.nota-espejo-x').textContent = n.texto.trim();
  }
  function espejos() {
    main.querySelectorAll('.nota-espejo').forEach(e => { if (!notas.some(n => n.id === e.dataset.nota)) e.remove(); });
    notas.forEach(espejo);
  }
  alCopiar.push(c => c.querySelectorAll('.nota-espejo').forEach(x => x.remove()));

  function quitar(id) {
    notas = notas.filter(n => n.id !== id);
    borradas.add(id); perdidas.delete(id); quitarMarcas(id);
    main.querySelectorAll(`.nota-espejo[data-nota="${id}"]`).forEach(x => x.remove());
    persistir(); pintarResumen();
  }
  function borrar(id) { quitar(id); pintarNotas(); }
  // Nota → párrafo del documento (opción nota-a-parrafo): tras el bloque del texto anotado o al final de su sección.
  function convertir(n) {
    const texto = (n.texto || '').trim();
    if (!texto) { enfocarNota(n.id); return; }
    const m = main.querySelector(`mark.nota-cita[data-nota="${n.id}"]`);
    const sec = n.seccion && document.getElementById(n.seccion);
    const tras = m && m.closest('p, li, blockquote, aside, table, .tarjeta, .caso');
    const p = document.createElement('p');
    p.className = 'parrafo-anadido'; p.dataset.anadido = new Date().toISOString();
    texto.split(/\n\s*\n/).forEach((b, i) => { if (i) p.append(document.createElement('br'), document.createElement('br')); p.append(b.replace(/\s*\n\s*/g, ' ')); });
    if (tras) tras.after(p);
    else {
      const cuerpo = sec ? (sec.querySelector(':scope > .seccion-cuerpo, :scope > .bloque-content') || sec) : main;
      const e = cuerpo.querySelector(':scope > .nota-espejo, :scope > .nt-sitio');
      if (e) e.before(p); else cuerpo.appendChild(p);
    }
    borrar(n.id);
    abrirHasta(p); p.scrollIntoView({ block: 'center', behavior: suave }); destellar(p);
    window.marcarCambiosDocumento();
  }
  function enfocarNota(id) {
    const li = (sitio() ? main : notasT.el).querySelector(`li.nt-nota[data-id="${id}"]`);
    if (!li) return;
    if (sitio()) abrirHasta(li);
    const t = li.closest('.nt-tarjeta');
    if (t && t.classList.contains('plegada')) t.querySelector('.nt-tarjeta-cab').click();
    notasT.el.querySelectorAll('.actual').forEach(x => x.classList.remove('actual'));
    li.classList.add('actual');
    li.scrollIntoView({ block: sitio() ? 'center' : 'nearest' });
    li.querySelector('textarea').focus({ preventScroll: true });
  }
  function irNota(id) {
    const m = main.querySelector(`mark.nota-cita[data-nota="${id}"]`);
    if (!m) return;
    abrirHasta(m);
    m.scrollIntoView({ block: 'center', behavior: suave });
    destellar(m);
    main.querySelectorAll(`mark.nota-cita[data-nota="${id}"]`).forEach(x => { x.classList.add('destello'); setTimeout(() => x.classList.remove('destello'), 1600); });
    if (!grande.matches) { abiertaEstrecha = null; aplicar(); }
  }
  function nueva(n) {  // una nota nueva, sin volver a pintar el panel (se está escribiendo en ella)
    n.id = Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
    n.autor = autorEl.value.trim();
    n.creada = n.modificada = new Date().toISOString();
    n.texto = '';
    notas.push(n);
    return n;
  }
  function crear(n) {  // una nota sobre un texto: se abre su tarjeta y se escribe en ella
    nueva(n);
    const sec = n.seccion && document.getElementById(n.seccion);
    if (sec) { secActual = sec; abiertas.set(sec.id, true); }
    persistir(); pintarNotas(); if (!sitio()) mostrar(notasT); enfocarNota(n.id);
  }
  main.addEventListener('click', e => {
    const m = e.target.closest('mark.nota-cita');
    if (!m || !getSelection().isCollapsed) return;
    const n = notas.find(x => x.id === m.dataset.nota), sec = n && n.seccion && document.getElementById(n.seccion);
    if (sec) { secActual = sec; abiertas.set(sec.id, true); pintarNotas(); }
    if (!sitio()) mostrar(notasT);
    enfocarNota(m.dataset.nota);
  });

  // «Anotar»: aparece junto al texto seleccionado.
  const anotar = document.createElement('button');
  anotar.type = 'button';
  anotar.className = 'boton-anotar';
  anotar.textContent = 'Anotar';
  anotar.hidden = true;
  document.body.appendChild(anotar);
  let rango = null, tSel = 0;
  function revisarSeleccion() {
    const s = getSelection();
    const r = s.rangeCount && !s.isCollapsed ? s.getRangeAt(0) : null;
    const comun = r && (r.commonAncestorContainer.nodeType === 1 ? r.commonAncestorContainer : r.commonAncestorContainer.parentElement);
    if (!r || !main.contains(comun) || comun.closest('.herramienta, button, input, textarea, select') || !r.toString().trim()) { anotar.hidden = true; rango = null; return; }
    rango = r.cloneRange();
    const caja = [...r.getClientRects()].pop() || r.getBoundingClientRect();
    anotar.hidden = false;
    anotar.style.left = Math.max(8, Math.min(caja.right + scrollX - 36, scrollX + innerWidth - 96)) + 'px';
    anotar.style.top = (caja.bottom + scrollY + 8) + 'px';
  }
  if (N_TEXTO) document.addEventListener('selectionchange', () => { clearTimeout(tSel); tSel = setTimeout(revisarSeleccion, 150); });
  anotar.addEventListener('pointerdown', e => e.preventDefault());  // que no se pierda la selección
  anotar.addEventListener('click', () => {
    const r = rango;
    anotar.hidden = true; rango = null;
    if (!r) return;
    const inicio = r.startContainer.nodeType === 1 ? r.startContainer : r.startContainer.parentElement;
    const sec = inicio.closest(SECCION);
    const raizSel = sec && sec.contains(r.endContainer) ? sec : main;
    const { texto, nodos } = mapa(raizSel);
    let a = -1, b = -1;
    for (const [n, ini] of nodos) {
      if (!r.intersectsNode(n)) continue;
      if (a < 0) a = ini + (n === r.startContainer ? r.startOffset : 0);
      b = ini + (n === r.endContainer ? r.endOffset : n.data.length);
    }
    if (a < 0) return;
    while (a < b && /\s/.test(texto[a])) a++;
    while (b > a && /\s/.test(texto[b - 1])) b--;
    if (a >= b) return;
    const cita = texto.slice(a, b);
    let ocurrencia = 0;
    for (let p = texto.indexOf(cita); p !== -1 && p < a; p = texto.indexOf(cita, p + 1)) ocurrencia++;
    getSelection().removeAllRanges();
    const n = { seccion: raizSel === main ? '' : raizSel.id, titulo: raizSel === main ? 'Inicio' : tituloSec(raizSel), cita, ocurrencia };
    crear(n);
    envolver(raizSel, a, b, n.id);
  });
  }

  // «Guardar»: copia limpia del documento, con las notas dentro y la versión siguiente.
  function copiaLimpia(d) {
    const c = raiz.cloneNode(true);
    c.querySelectorAll('.columna-herramientas, .herramienta, .abrir-herramienta, .botones-herramientas, .boton-anotar, .barra-doc, .dc-anclar, .franja-barra')
      .forEach(x => x.remove());
    c.querySelectorAll('mark.nota-cita').forEach(m => m.replaceWith(...m.childNodes));
    c.querySelectorAll('.destello-seccion').forEach(x => x.classList.remove('destello-seccion'));
    for (const limpiar of alCopiar) { try { limpiar(c); } catch (_) {} }  // cada herramienta deja la copia sin su estado
    c.classList.remove('js', 'con-columna', 'herr-estrecho', 'redimensionando');
    if (!c.classList.length) c.removeAttribute('class');
    c.style.removeProperty('--ancho-columna');
    if (!c.getAttribute('style')) c.removeAttribute('style');
    c.querySelectorAll('details').forEach((x, i) => x.toggleAttribute('open', !!abiertosAlCargar[i]));
    const cuerpo = c.querySelector('body');
    let s = c.querySelector('#notas-documento');
    if (!s) { s = document.createElement('script'); s.type = 'application/json'; s.id = 'notas-documento'; cuerpo.prepend(s); }
    s.textContent = JSON.stringify(d, null, 1).replace(/</g, '\\u003c');
    return '<!DOCTYPE html>\n' + c.outerHTML;
  }
  const slug = s => norm(s).replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 30);
  // «mismo-archivo»: el archivo elegido la primera vez se recuerda (IndexedDB) y los guardados siguientes lo
  // sobrescriben sin preguntar, si el navegador mantiene el permiso. Sin la API (Firefox), se descarga.
  const MISMO = ACTIVAS.has('mismo-archivo');
  const almacen = modo => new Promise((ok, mal) => {
    const r = indexedDB.open('documento-archivos', 1);
    r.onupgradeneeded = () => r.result.createObjectStore('archivos');
    r.onsuccess = () => ok(r.result.transaction('archivos', modo).objectStore('archivos'));
    r.onerror = () => mal(r.error);
  });
  const recordado = () => almacen('readonly').then(s => new Promise(ok => { const q = s.get(ruta); q.onsuccess = () => ok(q.result || null); q.onerror = () => ok(null); })).catch(() => null);
  const recordar = h => almacen('readwrite').then(s => s.put(h, ruta)).catch(() => {});
  barra.querySelector('.dc-guardar').addEventListener('click', async () => {
    const siguiente = Math.max(version, guardado.version || 0) + 1, ahora = new Date().toISOString();
    const html = copiaLimpia({ version: siguiente, guardado: ahora, herramientas: VERSION, documento: document.title, notas });
    const base = decodeURIComponent(ruta.split('/').pop() || 'documento.html').replace(/\.html?$/i, '').replace(/\.notas(-[^.]*)?$/, '');
    const autor = CON_NOTAS ? slug(autorEl.value) : '';
    const nombre = MISMO ? decodeURIComponent(ruta.split('/').pop() || 'documento.html') : base + '.notas' + (autor ? '-' + autor : '') + '.html';
    try {
      if (window.showSaveFilePicker) {
        let h = MISMO ? await recordado() : null;
        if (h && (await h.requestPermission({ mode: 'readwrite' })) !== 'granted') h = null;
        if (!h) h = await window.showSaveFilePicker({ suggestedName: nombre, id: MISMO ? 'documento-mismo' : 'documento-notas', types: [{ description: 'Documento HTML', accept: { 'text/html': ['.html'] } }] });
        const w = await h.createWritable(); await w.write(html); await w.close();
        if (MISMO) recordar(h);
      } else {
        const a = document.createElement('a');
        a.href = URL.createObjectURL(new Blob([html], { type: 'text/html;charset=utf-8' }));
        a.download = nombre; document.body.appendChild(a); a.click(); a.remove();
        setTimeout(() => URL.revokeObjectURL(a.href), 10000);
      }
      guardado = { firma: firma(notas), fecha: ahora, version: siguiente };
      otrosCambios = false;
      if (MISMO || ruta.endsWith(nombre)) { version = siguiente; verEl.textContent = 'v' + version; }
      persistir();
    } catch (err) {
      if (!err || err.name !== 'AbortError') estadoEl.textContent = 'No se ha podido guardar' + (err && err.message ? ': ' + err.message : '');
    }
  });

  if (CON_NOTAS) {
    let ultimoSitio = sitio();
    if (ultimoSitio) moverZonas();
    trasAplicar = () => { const s = sitio(); if (s !== ultimoSitio) { ultimoSitio = s; moverZonas(); seguirSeccion(); pintarNotas(); } };
    seguirSeccion(); pintarNotas();
  }
  estado();
  }

  // Lo que usan las demás piezas del kit (lectura.js, edicion.js).
  window.herramientasDocumento = { VERSION, ACTIVAS, CONVIERTE, main, raiz, SECCION, TITULO, grande, suave, ruta, leer, escribir,
    herramienta, aplicar, mostrar, abrirHasta, destellar, alCopiar, norm, tituloSec };
  aplicar();
})();
