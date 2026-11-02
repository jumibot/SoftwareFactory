/* Buscador de fichas (skill crear_documentos).
 * Delante de cada bloque «::: fichas» pone un buscador de texto y un filtro por insignia.
 * Una insignia puede dar su propia etiqueta para el filtro, y más de una separadas por «;»
 * ([S2](#S2){: .insignia data-filtro="Conservación; Transporte"}): la ficha sale con cualquiera de ellas.
 * Al buscar un texto, las fichas plegables que coinciden se abren.
 * Sin data-filtro, el filtro se rellena con las insignias de las fichas ([S2](#S2){: .insignia}) y con el título
 * del destino de cada una, si existe en la página. Sin JavaScript, las fichas se ven todas. */
(function () {
  // En la copia que guardan las herramientas del documento, sin buscadores de fichas ni filtros aplicados.
  (window.alCopiarDocumento = window.alCopiarDocumento || []).push(c => {
    c.querySelectorAll('.buscador, .sin-resultados').forEach(x => x.remove());
    c.querySelectorAll('.ficha[hidden]').forEach(x => x.removeAttribute('hidden'));
  });
  const normal = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[  ]/g, ' ').toLowerCase();  // espacio duro o fino = espacio
  // Las entradas del filtro de una insignia: las de su data-filtro o, sin él, su código.
  const claves = a => a.dataset.filtro ? a.dataset.filtro.split(';').map(x => x.trim()).filter(Boolean) : [a.textContent.trim()];
  document.querySelectorAll('.fichas').forEach((caja, k) => {
    const fichas = [...caja.querySelectorAll(':scope > .ficha')];
    const codigos = new Map();
    fichas.forEach(f => f.querySelectorAll('a.insignia').forEach(a => {
      for (const c of claves(a)) {
        if (codigos.has(c)) continue;
        if (a.dataset.filtro) { codigos.set(c, c); continue; }
        const destino = a.getAttribute('href')?.startsWith('#') && document.getElementById(a.getAttribute('href').slice(1));
        const titulo = destino ? (destino.querySelector('h3,h4') || destino).textContent.trim() : '';
        codigos.set(c, titulo && titulo !== c ? `${c} · ${titulo.replace(/^\S+\s·\s/, '')}` : c);
      }
    }));
    const orden = [...codigos.keys()].sort((a, b) => a.localeCompare(b, 'es', { numeric: true }));
    const barra = document.createElement('div');
    barra.className = 'buscador';
    barra.innerHTML =
      `<label>Buscar<input type="search" id="buscar-${k}" name="buscar-${k}" autocomplete="off" placeholder="Nombre, condición, cifra…"></label>` +
      (orden.length ? `<label>Filtrar<select id="filtro-${k}" name="filtro-${k}"><option value="">Todas</option>${orden.map(c => `<option value="${c}">${codigos.get(c)}</option>`).join('')}</select></label>` : '') +
      `<button type="button">Restablecer</button><span class="cuenta" role="status" aria-live="polite"></span>`;
    caja.before(barra);
    const vacio = document.createElement('p');
    vacio.className = 'sin-resultados';
    vacio.textContent = 'Ninguna ficha coincide con la búsqueda.';
    caja.after(vacio);
    const q = barra.querySelector('input'), sel = barra.querySelector('select'), cuenta = barra.querySelector('.cuenta');
    function aplicar() {
      const texto = normal(q.value.trim()), c = sel ? sel.value : '';
      let n = 0;
      for (const f of fichas) {
        const tiene = !c || [...f.querySelectorAll('a.insignia')].some(a => claves(a).includes(c));
        const ok = tiene && (!texto || normal(f.textContent).includes(texto));
        f.hidden = !ok;
        if (ok) n++;
        // La ficha plegable que coincide con un texto buscado se abre, para ver dónde está.
        if (ok && texto && f.tagName === 'DETAILS') f.open = true;
      }
      cuenta.textContent = `${n} de ${fichas.length}`;
      vacio.style.display = n ? 'none' : 'block';
    }
    q.addEventListener('input', aplicar);
    sel && sel.addEventListener('change', aplicar);
    barra.querySelector('button').addEventListener('click', () => { q.value = ''; if (sel) sel.value = ''; aplicar(); });
    aplicar();
  });
})();
