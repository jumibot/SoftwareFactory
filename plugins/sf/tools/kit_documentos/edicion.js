/* Edición de párrafos en su sitio (biblioteca tools/kit_documentos/, tras herramientas.js). Opciones «edicion» y
 * «nota-a-parrafo»: con la segunda sola, solo se pintan «Añadido · fecha» y «Retirar» en los párrafos que vienen de
 * una nota, sin lápiz.
 * Pensada para los artefactos para el usuario, donde el .html es el entregable; en los del proyecto manda el .md.
 * · El lápiz que aparece al pasar por un párrafo lo abre para escribir en él, con una barra debajo: formato básico
 *   (negrita, cursiva, subrayado, tachado, superíndice, subíndice, quitar formato), aplicar (Intro) y cancelar (Esc).
 * · Si el párrafo cambia, lleva al final «Modificado · fecha», uno por cambio; su ayuda muestra el texto de antes.
 *   «Restaurar el original» lo devuelve. Historial en data-modificado (fechas ISO) y data-anteriores (JSON; el primero,
 *   el original). tools/kit_documentos/extraer_notas.py lo lista para llevarlo al .md si hace falta.
 * · Los párrafos añadidos desde una nota («Convertir en párrafo», herramientas.js) llevan «Añadido · fecha» y
 *   «Retirar», que pide confirmación en el propio botón.
 * Lo pintado (lápiz, barra, etiquetas) no viaja en la copia guardada: se vuelve a poner al abrirla.
 * Procedencia: docs/referencias/procedencia/kit_documentos.md del repositorio de la SF. */
(function () {
  const api = window.herramientasDocumento;
  const EDITA = api && api.ACTIVAS.has('edicion');
  if (!api || !(EDITA || api.CONVIERTE)) return;
  const { alCopiar } = api;
  const SEL = 'main p, .report-header p, .report-body p';
  const FUERA = '.nt-sitio, .nt-sitio-inicio, .herramienta, .leyenda-doc, .bocadillo-fuente, .barra-doc, svg, figure, nav, header.site-header, footer, .ed-barra, .fuentes, summary';
  const CONTROL = '.ed-meta, .btn-editar';
  const cambiado = () => { if (window.marcarCambiosDocumento) window.marcarCambiosDocumento(); };
  const fecha = iso => new Date(iso).toLocaleString('es-ES', { dateStyle: 'short', timeStyle: 'short' });
  const norm = s => String(s).replace(/&nbsp;| /g, ' ').replace(/\s+/g, ' ').trim();
  const textoDe = h => new DOMParser().parseFromString(h || '', 'text/html').body.textContent.trim();
  const editable = p => p.matches(SEL) && !p.closest(FUERA) && !/etiqueta|procedencia|pista/.test(p.className) && p.textContent.trim();
  let activo = null;

  function limpiarMarcas(raiz) {  // marcas de otras herramientas (buscador, notas, fuentes)
    raiz.querySelectorAll('mark').forEach(m => m.replaceWith(...m.childNodes));
    raiz.normalize();
  }
  function contenido(p) {  // el HTML del párrafo sin lo pintado
    const d = p.cloneNode(true);
    d.querySelectorAll(CONTROL).forEach(x => x.remove());
    limpiarMarcas(d);
    return norm(d.innerHTML);
  }
  function historial(p) {
    let antes = null;
    try { antes = JSON.parse(p.dataset.anteriores || 'null'); } catch (_) {}
    return { fechas: (p.dataset.modificado || '').split(/\s+/).filter(Boolean), antes: Array.isArray(antes) ? antes : [] };
  }
  function guardarHistorial(p, h) {
    if (!h.fechas.length) { delete p.dataset.modificado; delete p.dataset.anteriores; return; }
    p.dataset.modificado = h.fechas.join(' '); p.dataset.anteriores = JSON.stringify(h.antes);
  }
  function etiqueta(texto, ayuda) {
    const t = document.createElement('span'); t.className = 'ed-meta ed-traza'; t.tabIndex = 0; t.textContent = texto; t.title = ayuda; return t;
  }
  // Lo pintado va al final del párrafo, como un punto y seguido: Añadido, Modificado…, Retirar y el lápiz.
  function pintar(p) {
    p.querySelectorAll(CONTROL).forEach(x => x.remove());
    if (p.classList.contains('parrafo-anadido') && p.dataset.anadido) {
      p.append(etiqueta('Añadido · ' + fecha(p.dataset.anadido), 'Añadido el ' + fecha(p.dataset.anadido) + ' (nota convertida en párrafo)'));
      const b = document.createElement('button'); b.type = 'button'; b.className = 'ed-meta btn-retirar'; b.textContent = '✕ Retirar';
      b.title = 'Quita este párrafo del documento';
      let confirmar = 0;
      b.addEventListener('click', () => {
        if (!confirmar) { b.textContent = '¿Retirar el párrafo?'; confirmar = setTimeout(() => { confirmar = 0; b.textContent = '✕ Retirar'; }, 3000); return; }
        clearTimeout(confirmar); p.remove(); cambiado();
      });
      p.append(b);
    }
    const h = historial(p), n = h.fechas.length;
    h.fechas.forEach((iso, i) => p.append(etiqueta('Modificado · ' + fecha(iso),
      (n > 1 ? 'Cambio ' + (i + 1) + ' de ' + n + ', el ' : 'Modificado el ') + fecha(iso) + '. Texto ' + (i ? 'de antes de este cambio' : 'original') + ':\n«' + textoDe(h.antes[i] ?? h.antes[0]) + '»')));
    if (!EDITA) return;
    const lapiz = document.createElement('button'); lapiz.type = 'button'; lapiz.className = 'btn-editar';
    lapiz.title = 'Editar este párrafo aquí mismo'; lapiz.setAttribute('aria-label', 'Editar este párrafo'); lapiz.textContent = '✎';
    lapiz.addEventListener('click', e => { e.preventDefault(); e.stopPropagation(); editar(p); });
    p.appendChild(lapiz);
    p.classList.add('editable');
  }

  const FORMATO = [['bold', 'N', 'Negrita (Ctrl+B)'], ['italic', 'K', 'Cursiva (Ctrl+I)'], ['underline', 'S', 'Subrayado (Ctrl+U)'],
    ['strikeThrough', 'T', 'Tachado'], ['superscript', 'x²', 'Superíndice'], ['subscript', 'x₂', 'Subíndice'], ['removeFormat', '⌫ Formato', 'Quita el formato del texto seleccionado']];
  function boton(txt, clase, ayuda, fn) {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'ed-btn ' + clase; b.textContent = txt; b.title = ayuda;
    b.addEventListener('mousedown', e => e.preventDefault());  // el cursor se queda en el texto
    b.addEventListener('click', fn); return b;
  }
  function estadoFormato() {
    if (!activo) return;
    activo.barra.querySelectorAll('.ed-fmt').forEach(c => {
      if (c.dataset.cmd === 'removeFormat') return;
      let on = false; try { on = document.queryCommandState(c.dataset.cmd); } catch (_) {}
      c.setAttribute('aria-pressed', String(on));
    });
  }
  document.addEventListener('selectionchange', () => { const s = getSelection(); if (activo && s.rangeCount && activo.ed.contains(s.anchorNode)) estadoFormato(); });
  function barra(p) {
    const b = document.createElement('div'); b.className = 'ed-barra'; b.setAttribute('role', 'toolbar'); b.setAttribute('aria-label', 'Editar el párrafo');
    const g1 = document.createElement('div'); g1.className = 'ed-grupo';
    FORMATO.forEach(f => {
      const c = boton(f[1], 'ed-fmt', f[2], () => { activo.ed.focus(); document.execCommand(f[0], false, null); estadoFormato(); });
      c.dataset.cmd = f[0]; c.setAttribute('aria-label', f[2]); g1.appendChild(c);
    });
    const g2 = document.createElement('div'); g2.className = 'ed-grupo ed-acciones';
    const pista = document.createElement('span'); pista.className = 'ed-pista'; pista.textContent = 'Intro aplica · Esc cancela';
    g2.appendChild(pista);
    if (historial(p).fechas.length) g2.appendChild(boton('Restaurar el original', 'ed-restaurar', 'Devuelve el párrafo a su texto original y quita las marcas «Modificado»', restaurar));
    g2.appendChild(boton('Cancelar', 'ed-cancelar', 'Deja el párrafo como estaba (Esc)', cancelar));
    g2.appendChild(boton('✓ Aplicar', 'ed-aplicar', 'Aplica el cambio (Intro)', aplicar));
    b.append(g1, g2);
    return b;
  }
  function sanear(raiz) {  // a etiquetas simples y sin estilos
    const MAPA = { STRONG: 'b', EM: 'i', STRIKE: 's', DEL: 's' };
    raiz.querySelectorAll('strong, em, strike, del').forEach(x => { const n = document.createElement(MAPA[x.tagName]); n.append(...x.childNodes); x.replaceWith(n); });
    raiz.querySelectorAll('font, span:not([class])').forEach(x => x.replaceWith(...x.childNodes));
    raiz.querySelectorAll('[style]').forEach(x => x.removeAttribute('style'));
    raiz.querySelectorAll('br').forEach(x => x.replaceWith(' '));
    raiz.querySelectorAll('div, p').forEach(x => x.replaceWith(' ', ...x.childNodes));
    raiz.querySelectorAll('b, i, u, s, sup, sub').forEach(x => { if (!x.textContent) x.remove(); });
  }

  function editar(p) {
    if (activo && activo.p === p) return;
    if (activo) aplicar();
    const html0 = contenido(p);
    activo = { p, nodos: [...p.childNodes], html0 };
    p.textContent = ''; p.classList.add('editando'); p.dataset.editando = '1';
    const ed = activo.ed = document.createElement('span'); ed.className = 'ed-texto'; ed.contentEditable = 'true';
    ed.setAttribute('role', 'textbox'); ed.setAttribute('aria-label', 'Texto del párrafo');
    ed.innerHTML = html0; p.appendChild(ed);
    ed.addEventListener('keydown', e => {
      if (e.key === 'Enter') { e.preventDefault(); aplicar(); }
      else if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); cancelar(); }
    });
    ed.addEventListener('paste', e => {  // se pega solo el texto
      e.preventDefault();
      document.execCommand('insertText', false, (e.clipboardData || window.clipboardData).getData('text/plain').replace(/\s+/g, ' '));
    });
    activo.barra = barra(p); p.after(activo.barra);
    try { document.execCommand('styleWithCSS', false, false); } catch (_) {}
    ed.focus();
    const r = document.createRange(); r.selectNodeContents(ed); r.collapse(false);
    const s = getSelection(); s.removeAllRanges(); s.addRange(r);
    estadoFormato();
  }
  function cerrar() {
    const a = activo; activo = null;
    a.barra.remove(); a.p.classList.remove('editando'); delete a.p.dataset.editando;
    return a;
  }
  function cancelar() { const a = cerrar(); a.p.textContent = ''; a.p.append(...a.nodos); }
  function poner(p, html) { p.innerHTML = html; pintar(p); }
  function aplicar() {
    if (!activo) return;
    const d = document.createElement('div'); d.innerHTML = activo.ed.innerHTML; limpiarMarcas(d); sanear(d);
    const nuevo = norm(d.innerHTML), a = activo;
    if (nuevo === a.html0) { cancelar(); return; }
    if (!textoDe(nuevo)) { cancelar(); return; }  // un párrafo vacío no se aplica: para quitarlo, «Retirar» o el .md
    cerrar();
    const p = a.p;
    let h = historial(p);
    if (h.fechas.length && nuevo === norm(h.antes[0])) h = { fechas: [], antes: [] };  // vuelve a ser el original
    else { h.fechas.push(new Date().toISOString()); h.antes.push(a.html0); }
    guardarHistorial(p, h);
    poner(p, nuevo);
    cambiado();
  }
  function restaurar() {
    const a = cerrar(), p = a.p, original = historial(p).antes[0];
    guardarHistorial(p, { fechas: [], antes: [] });
    poner(p, original ?? a.html0);
    cambiado();
  }

  document.querySelectorAll(EDITA ? SEL : 'p.parrafo-anadido').forEach(p => { if (editable(p)) pintar(p); });
  // Los párrafos que llegan después (una nota convertida en párrafo) también se editan.
  new MutationObserver(cs => cs.forEach(c => c.addedNodes.forEach(n => {
    if (n.nodeType !== 1 || n.closest('.ed-barra')) return;
    if (n.matches('p.parrafo-anadido') && !n.querySelector('.btn-editar, .btn-retirar')) pintar(n);
  }))).observe(document.body, { childList: true, subtree: true });

  alCopiar.push(c => {
    c.querySelectorAll('[data-editando]').forEach(p => {
      if (activo) p.innerHTML = activo.html0;
      p.classList.remove('editando'); p.removeAttribute('data-editando');
    });
    c.querySelectorAll('.ed-barra, .ed-meta, .btn-editar').forEach(x => x.remove());
    c.querySelectorAll('.editable').forEach(p => { p.classList.remove('editable'); if (!p.className) p.removeAttribute('class'); });
    c.querySelectorAll('[contenteditable]').forEach(x => x.removeAttribute('contenteditable'));
  });
})();
