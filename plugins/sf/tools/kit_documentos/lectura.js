/* Opciones de lectura del documento (biblioteca tools/kit_documentos/, con herramientas.js, que va antes).
 * Cada opción se elige en <html data-herramientas> (catálogo y valores iniciales en tema_identidad.py). Las que el
 * lector ajusta (el engranaje junto a «Guardar» abre «Lectura») parten del valor del autor y se recuerdan por documento:
 * · modo: claro, oscuro o el del sistema; el documento abre siempre en claro y el oscuro lo elige el lector;
 * · acordeon: un solo bloque abierto a la vez;
 * · cabecera: el título de la sección abierta se queda arriba mientras se lee;
 * · fuentes: al pasar por una referencia [E1], bocadillo con la fuente y la frase que respalda resaltada;
 * · bocadillos: los subapartados de detalle (visión) se abren en un bocadillo, sin desplazar el texto.
 * Las que elige solo el autor: tablas (anchos ajustables) y leyenda («Cómo leer este documento»).
 * Procedencia: docs/referencias/procedencia/kit_documentos.md del repositorio de la SF. */
(function () {
  const api = window.herramientasDocumento;
  if (!api) return;
  const { ACTIVAS, main, raiz, SECCION, ruta, leer, escribir, alCopiar } = api;
  const secciones = [...main.querySelectorAll(SECCION)];
  const refs = [...document.querySelectorAll('a.ref[href^="#"], a[href^="#src-"]')];
  const subDetalle = [...main.querySelectorAll('details.subsubseccion')];
  const tablas = [...main.querySelectorAll('table')].filter(t => !t.closest('svg'));

  // ── Preferencias del lector, con el valor del autor como punto de partida ──
  const CLAVE = 'documento-lectura:' + ruta;
  const guardadas = leer(CLAVE, {}) || {};
  const pref = {
    // Hasta la 1.8 se guardaba «sistema» sin que el lector lo eligiera: solo vale el modo que eligió en «Lectura».
    modo: (guardadas.modoElegido && guardadas.modo) || 'claro',
    modoElegido: !!guardadas.modoElegido,
    acordeon: guardadas.acordeon ?? ACTIVAS.has('acordeon'),
    cabecera: guardadas.cabecera ?? ACTIVAS.has('cabecera'),
    fuentes: guardadas.fuentes ?? ACTIVAS.has('fuentes'),
    bocadillos: guardadas.bocadillos ?? ACTIVAS.has('bocadillos'),
  };
  const guardar = () => escribir(CLAVE, pref);

  // ── Modo claro / oscuro / sistema ──
  const sistema = matchMedia('(prefers-color-scheme: dark)');
  function aplicarModo() { raiz.dataset.modo = pref.modo === 'sistema' ? (sistema.matches ? 'oscuro' : 'claro') : pref.modo; }
  sistema.addEventListener('change', aplicarModo);
  aplicarModo();

  // ── Un solo bloque abierto: al abrir uno se cierran los demás (no al abrir varios a la vez: «Desplegar todo», imprimir) ──
  let abiertos = [];
  secciones.forEach(d => d.addEventListener('toggle', () => {
    if (!pref.acordeon || !d.open) return;
    abiertos.push(d);
    if (abiertos.length > 1) return;
    setTimeout(() => {
      const lote = abiertos; abiertos = [];
      if (lote.length !== 1) return;
      let arriba = false;
      secciones.forEach(o => {
        if (o === d || !o.open) return;
        if (o.compareDocumentPosition(d) & Node.DOCUMENT_POSITION_FOLLOWING) arriba = true;
        o.open = false;
      });
      if (arriba) d.scrollIntoView({ behavior: 'instant', block: 'start' });  // cerrar lo de arriba no debe moverla
    }, 0);
  }));
  function cerrarDemas() { let uno = false; secciones.forEach(d => { if (d.open) { if (uno) d.open = false; uno = true; } }); }
  if (pref.acordeon) cerrarDemas();

  // ── Título de la sección abierta fijo arriba ──
  // El <summary> no admite sticky dentro de <details>: se desplaza con transform mientras se recorre su sección.
  const menu = document.querySelector('.menu');
  const altoMenu = () => menu && getComputedStyle(menu).position === 'sticky' ? menu.getBoundingClientRect().height : 0;
  const opaco = c => c && /^rgb\(/.test(c) || /^rgba\(.*,\s*1\)$/.test(c || '');
  const fondoDe = el => {  // el primer fondo opaco hacia arriba; si no hay, el de la página
    for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
      const c = getComputedStyle(e).backgroundColor;
      if (opaco(c)) return c;
    }
    return getComputedStyle(raiz).getPropertyValue('--pagina').trim() || '#fff';
  };
  const titulos = secciones.map(d => d.querySelector(':scope > summary')).filter(Boolean);
  function seguir() {
    const activo = pref.cabecera && innerWidth >= 700 && innerHeight >= 500;
    const tope = activo ? altoMenu() : 0;
    for (const sm of titulos) {
      const d = sm.parentElement;
      sm.style.transform = '';
      if (!activo || !d.open) { sm.classList.remove('titulo-fijo'); continue; }
      const r = d.getBoundingClientRect(), s = sm.getBoundingClientRect();
      const y = Math.max(0, Math.min(tope - s.top, r.bottom - s.bottom - 8));
      if (y > 0) {
        if (!sm.classList.contains('titulo-fijo')) sm.style.backgroundColor = fondoDe(d);
        sm.classList.add('titulo-fijo'); sm.style.transform = 'translateY(' + y + 'px)';
      } else { sm.classList.remove('titulo-fijo'); sm.style.backgroundColor = ''; }
    }
  }
  let raf = 0;
  const pedir = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(seguir); };
  addEventListener('scroll', seguir, { passive: true });
  addEventListener('resize', pedir);
  document.addEventListener('toggle', pedir, true);
  addEventListener('beforeprint', () => titulos.forEach(sm => { sm.style.transform = ''; sm.classList.remove('titulo-fijo'); }));
  alCopiar.push(c => c.querySelectorAll('summary.titulo-fijo, summary[style]').forEach(sm => {
    sm.classList.remove('titulo-fijo'); sm.style.transform = ''; sm.style.backgroundColor = '';
    if (!sm.getAttribute('style')) sm.removeAttribute('style');
    if (!sm.className) sm.removeAttribute('class');
  }));

  // ── Fuentes: bocadillo con la fuente y la frase que respalda la referencia, resaltada ──
  const bocadillo = document.createElement('div');
  bocadillo.className = 'bocadillo-fuente'; bocadillo.hidden = true; bocadillo.setAttribute('role', 'tooltip');
  bocadillo.id = 'bocadillo-fuente';
  document.body.appendChild(bocadillo);
  let tCerrar = 0, refActiva = null;
  function quitarResalte() {
    main.querySelectorAll('mark.resalta-fuente').forEach(m => { const p = m.parentNode; m.replaceWith(...m.childNodes); p.normalize(); });
  }
  // La frase que respalda: desde el final de la frase anterior hasta la referencia (o hasta el grupo de referencias).
  function resaltar(ref) {
    const bloque = ref.closest('p, li, td, dd, blockquote, figcaption');
    if (!bloque) return;
    const nodos = [];
    const w = document.createTreeWalker(bloque, NodeFilter.SHOW_TEXT, {
      acceptNode: n => n.parentElement.closest('a.ref, a[href^="#src-"], button, .ed-meta') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
    while (w.nextNode()) {
      const n = w.currentNode;
      if (!(ref.compareDocumentPosition(n) & Node.DOCUMENT_POSITION_PRECEDING)) break;
      nodos.push(n);
    }
    let texto = nodos.map(n => n.data).join('');
    let fin = texto.replace(/\s+$/, '').length;
    if (!fin) return;
    const cuerpo = texto.slice(0, fin).replace(/[.!?…]["»”)]*$/, '');
    let inicio = 0;
    const re = /[.!?…]["»”)]*\s+/g;
    for (let m; (m = re.exec(cuerpo));) inicio = m.index + m[0].length;
    let pos = 0;
    for (const n of nodos) {
      const a = pos, b = pos + n.data.length; pos = b;
      const s = Math.max(inicio, a) - a, e = Math.min(fin, b) - a;
      if (e <= s || !n.data.slice(s, e).trim()) continue;
      let nodo = n;
      if (e < nodo.data.length) nodo.splitText(e);
      if (s > 0) nodo = nodo.splitText(s);
      const mk = document.createElement('mark'); mk.className = 'resalta-fuente';
      nodo.parentNode.replaceChild(mk, nodo); mk.appendChild(nodo);
    }
  }
  function abrirBocadillo(ref) {
    if (!pref.fuentes) return;
    let destino = null;
    try { destino = document.getElementById(decodeURIComponent(ref.getAttribute('href').slice(1))); } catch (_) {}
    if (!destino) return;
    clearTimeout(tCerrar);
    if (refActiva === ref) return;
    refActiva = ref;
    quitarResalte(); resaltar(ref);
    const copia = destino.cloneNode(true);
    copia.removeAttribute('id'); copia.querySelectorAll('[id]').forEach(x => x.removeAttribute('id'));
    bocadillo.textContent = ''; bocadillo.appendChild(copia);
    const pista = document.createElement('p'); pista.className = 'bf-pista'; pista.textContent = 'Pulsa la referencia para ir a la lista de fuentes';
    bocadillo.appendChild(pista);
    bocadillo.hidden = false;
    ref.setAttribute('aria-describedby', bocadillo.id);
    const r = ref.getBoundingClientRect(), b = bocadillo.getBoundingClientRect();
    const izq = Math.max(8, Math.min(r.left, innerWidth - b.width - 8));
    const abajo = r.bottom + 8 + b.height < innerHeight || r.top < b.height + 16;
    bocadillo.style.left = (izq + scrollX) + 'px';
    bocadillo.style.top = ((abajo ? r.bottom + 8 : r.top - b.height - 8) + scrollY) + 'px';
  }
  function cerrarBocadillo(ya) {
    clearTimeout(tCerrar);
    const hecho = () => { bocadillo.hidden = true; if (refActiva) refActiva.removeAttribute('aria-describedby'); refActiva = null; quitarResalte(); };
    if (ya) hecho(); else tCerrar = setTimeout(hecho, 220);
  }
  let tAbrir = 0;
  for (const ref of refs) {
    ref.addEventListener('mouseenter', () => { clearTimeout(tAbrir); tAbrir = setTimeout(() => abrirBocadillo(ref), 180); });
    ref.addEventListener('mouseleave', () => { clearTimeout(tAbrir); cerrarBocadillo(); });
    ref.addEventListener('focus', () => abrirBocadillo(ref));
    ref.addEventListener('blur', () => cerrarBocadillo());
    ref.addEventListener('click', () => cerrarBocadillo(true));
  }
  bocadillo.addEventListener('mouseenter', () => clearTimeout(tCerrar));
  bocadillo.addEventListener('mouseleave', () => cerrarBocadillo());
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !bocadillo.hidden) cerrarBocadillo(true); });
  addEventListener('scroll', () => { if (!bocadillo.hidden && !bocadillo.matches(':hover')) cerrarBocadillo(true); }, { passive: true });
  alCopiar.push(c => {
    c.querySelectorAll('.bocadillo-fuente').forEach(x => x.remove());
    c.querySelectorAll('mark.resalta-fuente').forEach(m => m.replaceWith(...m.childNodes));
    c.querySelectorAll('[aria-describedby="bocadillo-fuente"]').forEach(x => x.removeAttribute('aria-describedby'));
  });

  // ── Subapartados de detalle en bocadillo (visión) ──
  subDetalle.forEach(d => {
    if (d.querySelector(':scope > .sub-cuerpo')) return;
    const caja = document.createElement('div'); caja.className = 'sub-cuerpo';
    [...d.childNodes].forEach(n => { if (!(n.nodeType === 1 && n.matches('summary'))) caja.appendChild(n); });
    d.appendChild(caja);
    d.addEventListener('toggle', () => {
      if (!pref.bocadillos || !d.open) return;
      subDetalle.forEach(o => { if (o !== d && o.open) o.open = false; });
    });
  });
  function aplicarBocadillos() { raiz.classList.toggle('sub-en-bocadillo', !!pref.bocadillos && subDetalle.length > 0); }
  document.addEventListener('pointerdown', e => {
    if (!raiz.classList.contains('sub-en-bocadillo')) return;
    subDetalle.forEach(d => { if (d.open && !d.contains(e.target)) d.open = false; });
  });
  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape' || !raiz.classList.contains('sub-en-bocadillo')) return;
    subDetalle.forEach(d => { if (d.open) { d.open = false; d.querySelector(':scope > summary').focus(); } });
  });
  aplicarBocadillos();
  alCopiar.push(c => {
    c.classList.remove('sub-en-bocadillo');
    c.querySelectorAll('details.subsubseccion > .sub-cuerpo').forEach(x => x.replaceWith(...x.childNodes));
  });

  // ── Tablas: ancho de columna ajustable arrastrando el borde de su cabecera; doble clic, el ancho de partida ──
  const CLAVE_T = 'documento-tablas:' + ruta;
  let anchos = leer(CLAVE_T, {}) || {};
  const conTablas = ACTIVAS.has('tablas') && tablas.length > 0;
  function ponerAnchos(t, lista) {
    const ths = [...t.querySelectorAll('tr:first-child > th')];
    if (!lista) { t.style.tableLayout = ''; t.style.width = ''; ths.forEach(th => { th.style.width = ''; }); t.classList.remove('anchos-propios'); return; }
    t.style.tableLayout = 'fixed'; t.style.width = lista.reduce((a, b) => a + b, 0) + 'px'; t.classList.add('anchos-propios');
    ths.forEach((th, i) => { if (lista[i]) th.style.width = lista[i] + 'px'; });
  }
  if (conTablas) {
    const ancho = matchMedia('(min-width: 700px)');
    tablas.forEach((t, k) => {
      const ths = [...t.querySelectorAll('tr:first-child > th')];
      if (ths.length < 2) return;
      ths.forEach((th, i) => {
        const asa = document.createElement('span');
        asa.className = 'redim-th'; asa.title = 'Arrastra para cambiar el ancho de esta columna; doble clic, el ancho de partida';
        asa.setAttribute('aria-hidden', 'true');
        th.appendChild(asa);
        asa.addEventListener('pointerdown', e => {
          if (!ancho.matches) return;
          e.preventDefault(); e.stopPropagation();
          const lista = ths.map(x => Math.round(x.getBoundingClientRect().width));
          ponerAnchos(t, lista);
          const x0 = e.clientX, w0 = lista[i];
          asa.setPointerCapture(e.pointerId); raiz.classList.add('redimensionando');
          const mover = ev => { lista[i] = Math.max(48, Math.round(w0 + ev.clientX - x0)); ponerAnchos(t, lista); };
          const soltar = () => { raiz.classList.remove('redimensionando'); asa.removeEventListener('pointermove', mover); anchos[k] = lista; escribir(CLAVE_T, anchos); };
          asa.addEventListener('pointermove', mover);
          asa.addEventListener('pointerup', soltar, { once: true });
          asa.addEventListener('pointercancel', soltar, { once: true });
        });
        asa.addEventListener('dblclick', e => { e.stopPropagation(); delete anchos[k]; escribir(CLAVE_T, anchos); ponerAnchos(t, null); });
      });
      if (anchos[k] && ancho.matches) ponerAnchos(t, anchos[k]);
    });
    ancho.addEventListener('change', () => tablas.forEach((t, k) => ponerAnchos(t, ancho.matches ? anchos[k] : null)));
  }
  alCopiar.push(c => {
    c.querySelectorAll('.redim-th').forEach(x => x.remove());
    c.querySelectorAll('table.anchos-propios').forEach(t => {
      t.classList.remove('anchos-propios'); t.style.tableLayout = ''; t.style.width = '';
      if (!t.getAttribute('style')) t.removeAttribute('style');
      if (!t.className) t.removeAttribute('class');
      t.querySelectorAll('th[style]').forEach(th => { th.style.width = ''; if (!th.getAttribute('style')) th.removeAttribute('style'); });
    });
  });

  // ── Leyenda «Cómo leer este documento»: solo lo que el documento usa, con una muestra de cada cosa ──
  if (ACTIVAS.has('leyenda')) {
    const items = [];
    const muestra = sel => { const el = document.querySelector(sel); if (!el) return null; const c = el.cloneNode(true); c.removeAttribute('id'); c.querySelectorAll('[id]').forEach(x => x.removeAttribute('id')); c.inert = true; return c; };
    const anadir = (sel, texto, clase) => { const m = sel ? muestra(sel) : null; if (sel && !m) return; items.push([m, texto, clase]); };
    if (secciones.length) items.push([null, 'Cada sección se abre y se pliega tocando su título: ▸ plegada, ▾ abierta.']);
    anadir('.seccion-titulo .etiqueta', 'Etiqueta de sección: el número y de qué trata.');
    anadir('.caso-etiqueta', 'El caso que acompaña todo el documento.');
    anadir('.escena-etiqueta', 'Una escena: cómo se vive el sistema en un momento concreto.');
    anadir('.recuadro-etiqueta', 'Recuadro con algo que conviene tener presente.');
    if (refs.length) anadir('a.ref', 'Referencia a una fuente. Al pasar por ella ves la fuente y la frase que respalda; al pulsarla vas a la lista de fuentes.');
    anadir('a.externo', 'Enlace a otra web: se abre en una pestaña nueva.');
    if (subDetalle.length) items.push([null, 'Los apartados con ▸ más pequeños son detalle: se abren al tocarlos.']);
    if (ACTIVAS.has('buscador')) items.push([null, 'Buscar: «/» abre el buscador; Intro o F3, el siguiente resultado; Mayús, el anterior.']);
    if (ACTIVAS.has('notas')) items.push([null, 'Notas: selecciona un texto y pulsa «Anotar». Quedan en tu navegador; «Guardar» las lleva a un archivo.']);
    if (ACTIVAS.has('edicion')) items.push([null, 'Editar: el lápiz junto a un párrafo lo abre para cambiarlo aquí mismo; «Modificado» dice cuándo y qué ponía antes.']);
    if (ACTIVAS.has('lectura')) items.push([null, 'Lectura: el engranaje junto a «Guardar» abre el modo oscuro y las demás preferencias.']);
    if (ACTIVAS.has('diagramas') && document.querySelector('figure.diagrama')) items.push([null, 'Diagramas: pulsa un elemento para ver su ficha; «Diagramas», en las herramientas, cambia cómo se ven todas las figuras.']);
    const ley = document.createElement('details');
    ley.className = 'leyenda-doc';
    ley.innerHTML = '<summary>Cómo leer este documento</summary><dl></dl>';
    const dl = ley.querySelector('dl');
    for (const [m, texto] of items) {
      const dt = document.createElement('dt'), dd = document.createElement('dd');
      if (m) dt.appendChild(m); else dt.className = 'sin-muestra';
      dd.textContent = texto;
      dl.append(dt, dd);
    }
    const antes = main.querySelector(':scope > .avisos-globales');
    if (antes) antes.after(ley); else main.prepend(ley);
    alCopiar.push(c => c.querySelectorAll('.leyenda-doc').forEach(x => x.remove()));
  }

  // ── Herramienta «Lectura»: lo que el lector ajusta ──
  if (ACTIVAS.has('lectura')) {
    const filas = [];
    const casilla = (clave, texto, ayuda) => filas.push(`<label class="lc-fila" title="${ayuda}"><input type="checkbox" name="lectura-${clave}" data-clave="${clave}"> ${texto}</label>`);
    if (refs.length) casilla('fuentes', 'Ver la fuente al pasar por una referencia', 'Bocadillo con la fuente y la frase que respalda resaltada');
    if (secciones.length) casilla('cabecera', 'Título de la sección fijo arriba', 'El título de la sección abierta se queda arriba mientras la lees');
    if (secciones.length > 1) casilla('acordeon', 'Un solo bloque abierto a la vez', 'Al abrir una sección se cierran las demás');
    if (subDetalle.length) casilla('bocadillos', 'Detalles en bocadillo', 'Los subapartados de detalle se abren encima del texto, sin desplazarlo');
    // Es configuración, no una herramienta de trabajo: va en un modal que abre el engranaje junto a «Guardar».
    // Capa propia (no <dialog>), para que el modo oscuro, que invierte la página, también la invierta.
    const capa = document.createElement('div');
    capa.className = 'modal-lectura'; capa.hidden = true;
    capa.innerHTML = '<div class="ml-caja herr-lectura" tabindex="-1" role="dialog" aria-modal="true" aria-labelledby="ml-titulo">' +
      '<header class="ml-cab"><span id="ml-titulo" class="herr-titulo">Lectura</span>' +
      '<button type="button" class="ml-cerrar" aria-label="Cerrar">✕</button></header><div class="ml-cuerpo">' +
      '<label class="lc-fila lc-modo">Modo <select name="lectura-modo"><option value="claro">Claro</option><option value="oscuro">Oscuro</option>' +
      '<option value="sistema">El del sistema</option></select></label>' + filas.join('') +
      (conTablas ? '<button type="button" class="lc-tablas">Anchos de tabla de partida</button>' : '') +
      '<p class="lc-ayuda">Se recuerda en este navegador, para este documento.</p></div></div>';
    document.body.appendChild(capa);
    // La versión del documento y la del kit no son de trabajo: pasan de la barra al pie del modal
    const verDoc = document.querySelector('.barra-doc .dc-ver');
    if (verDoc) { const pie = document.createElement('p'); pie.className = 'lc-version'; pie.append(verDoc); capa.querySelector('.ml-cuerpo').append(pie); }
    const lec = { el: capa, q: s => capa.querySelector(s) };
    const GEAR = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>';
    const engranaje = document.createElement('button');
    engranaje.type = 'button'; engranaje.className = 'dc-config dc-icono'; engranaje.innerHTML = GEAR;
    engranaje.title = 'Lectura: modo oscuro, otras preferencias y versión'; engranaje.setAttribute('aria-label', 'Preferencias de lectura');
    engranaje.setAttribute('aria-haspopup', 'dialog');
    const barra = document.querySelector('.barra-doc'), bGuardar = barra && barra.querySelector('.dc-guardar');
    // A la izquierda de la barra, separado de los iconos y de «Guardar», que van a la derecha
    if (barra) barra.prepend(engranaje); else if (bGuardar) bGuardar.before(engranaje);
    else (document.querySelector('.menu-dentro') || document.querySelector('.report-header') || document.body).prepend(engranaje);
    const cerrarModal = () => { capa.hidden = true; engranaje.setAttribute('aria-expanded', 'false'); engranaje.focus(); };
    engranaje.addEventListener('click', () => {
      capa.hidden = false; engranaje.setAttribute('aria-expanded', 'true'); lec.q('.ml-caja').focus();
    });
    lec.q('.ml-cerrar').addEventListener('click', cerrarModal);
    capa.addEventListener('mousedown', e => { if (e.target === capa) cerrarModal(); });
    capa.addEventListener('keydown', e => {
      if (e.key === 'Escape') { e.stopPropagation(); cerrarModal(); return; }
      if (e.key !== 'Tab') return;  // el foco no sale del modal
      const f = [...capa.querySelectorAll('button, select, input')], i = f.indexOf(document.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
    });
    alCopiar.push(c => c.querySelectorAll('.modal-lectura, .dc-config').forEach(x => x.remove()));
    const sel = lec.q('select');
    sel.value = pref.modo;
    sel.addEventListener('change', () => { pref.modo = sel.value; pref.modoElegido = true; guardar(); aplicarModo(); });
    lec.el.querySelectorAll('input[data-clave]').forEach(c => {
      c.checked = !!pref[c.dataset.clave];
      c.addEventListener('change', () => {
        pref[c.dataset.clave] = c.checked; guardar();
        if (c.dataset.clave === 'acordeon' && c.checked) cerrarDemas();
        if (c.dataset.clave === 'bocadillos') aplicarBocadillos();
        if (c.dataset.clave === 'fuentes' && !c.checked) cerrarBocadillo(true);
        seguir();
      });
    });
    const bt = lec.q('.lc-tablas');
    if (bt) bt.addEventListener('click', () => { anchos = {}; escribir(CLAVE_T, anchos); tablas.forEach(t => ponerAnchos(t, null)); });
  }
  alCopiar.push(c => { delete c.dataset.modo; });
  seguir();
})();
