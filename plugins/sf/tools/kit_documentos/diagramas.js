/* Herramienta «diagramas» del documento (biblioteca tools/kit_documentos/, tras herramientas.js y lectura.js).
 * Ajustes de los diagramas de la skill diagramas (decisión 302) en una herramienta de la barra lateral, como el buscador
 * o las notas: se ancla en la columna, flota o, en pantalla pequeña, se abre con su botón. Solo aparece si el documento
 * tiene diagramas (<figure class="diagrama">) y está en <html data-herramientas>. Cada cambio vale para todas las figuras.
 * Cada figura parte de lo que eligió su autor: casillas como clases d-no-<ajuste>, selectores como data-d-<ajuste>,
 * tema como data-d-tema (los colores de cada tema los trae el documento, en .diagrama[data-d-tema]). Lo que cambia el
 * lector se recuerda en su navegador, por documento; la copia guardada lleva lo del autor.
 * Grupos de lo general a lo fino: Aspecto general, Cabecera, Cajas, Flechas y etiquetas, Notas, Interacción y Pie;
 * empiezan plegados y se recuerda cuáles abre el lector. «Por defecto» pone los
 * favoritos del propietario (decisión 302) y el tema con que se generó cada figura (decisión 307); «Como el
 * original», lo que hace diagram-design, con tinta. */
(function () {
  const api = window.herramientasDocumento;
  if (!api || !api.ACTIVAS.has('diagramas')) return;
  const figs = [...document.querySelectorAll('figure.diagrama')];
  if (!figs.length) return;
  const { ruta, leer, escribir, alCopiar, herramienta, aplicar } = api;
  const temas = (() => { try { return JSON.parse(document.getElementById('diagramas-temas').textContent); } catch (_) { return []; } })();

  // [clave, texto, grupo, por defecto, como el original]; los selectores llevan además sus opciones. Las etiquetas de los
  // selectores, cortas y de una línea (el grupo ya dice de qué son); las opciones, sin cortar en el ancho de la barra.
  // Solo ajustes que valen en cualquier diagrama: el color y el estilo de cada flecha y etiqueta los dan sus datos.
  const CASILLAS = [
    ['tarjeta', 'Tarjeta: fondo claro, borde fino y esquinas', 'aspecto', true, true],
    ['letra', 'Letra más grande', 'aspecto', false, false],
    ['foco', 'Acento de foco', 'aspecto', true, true],
    ['carriles', 'Carriles con nombre', 'aspecto', false, true],
    ['chips', 'Chips de tipo', 'cajas', false, true],
    ['color', 'Colores de los datos', 'flechas', true, false],
    ['estilos', 'Estilos de los datos (cursiva y discontinua)', 'flechas', true, true],
    ['notas', 'Notas', 'notas', true, false],
    ['resaltado', 'Resaltado del recorrido al pasar', 'interaccion', true, false],
    ['fichas', 'Fichas y HUD al pulsar', 'interaccion', true, false],
    ['regla', 'Línea sobre el pie', 'pie', true, true],
    ['recuento', 'Recuento de nodos y flechas', 'pie', false, true],
  ];
  const SELECTORES = [
    ['tema', 'Tema', 'aspecto', [['documento', 'El del documento']].concat(temas), null, 'tinta'],   // por defecto: el de cada figura
    ['lienzo', 'Fondo', 'aspecto', [['ninguno', 'Sin fondo'], ['papel', 'Claro'], ['tintado', 'Tintado']], 'papel', 'papel'],
    ['orientacion', 'Orientación', 'aspecto', [['auto', 'Automática'], ['vertical', 'Vertical'], ['horizontal', 'Horizontal']], 'auto', 'horizontal'],
    ['antetitulo', 'Antetítulo', 'cabecera', [['oculto', 'Oculto'], ['encima', 'Encima del título'], ['lado', 'Al lado del título']], 'oculto', 'encima'],
    ['titulo', 'Título', 'cabecera', [['sans', 'Sans'], ['serifa', 'Serifa grande'], ['serifa-p', 'Serifa pequeña'], ['mono', 'Mono'], ['oculto', 'Oculto']], 'sans', 'serifa'],
    ['desc', 'Descripción', 'cabecera', [['linea', 'En una línea'], ['completa', 'Completa'], ['corta', 'Primera frase'], ['oculta', 'Oculta']], 'linea', 'completa'],
    ['forma', 'Forma', 'cajas', [['redondeada', 'Redondeada'], ['croqueta', 'Croqueta']], 'redondeada', 'redondeada'],
    ['borde', 'Borde', 'cajas', [['fino', 'Fino'], ['ninguno', 'Sin borde'], ['grueso', 'Grueso']], 'fino', 'fino'],
    ['fondo', 'Fondo', 'cajas', [['ninguno', 'Sin fondo'], ['papel', 'Claro'], ['tintado', 'Tintado']], 'papel', 'papel'],
    ['detalle', 'Detalle', 'cajas', [['sans', 'Sans'], ['mono', 'Mono']], 'sans', 'mono'],
    ['grosor', 'Grosor', 'flechas', [['fino', 'Fino'], ['normal', 'Normal'], ['grueso', 'Grueso']], 'fino', 'fino'],
    ['punta', 'Punta', 'flechas', [['llena', 'Triángulo lleno'], ['abierta', 'Abierta'], ['ninguna', 'Ninguna']], 'llena', 'llena'],
    ['esquinas', 'Esquinas', 'flechas', [['redondeadas', 'Redondeadas'], ['rectas', 'En ángulo recto']], 'redondeadas', 'redondeadas'],
    ['recuadro', 'Recuadro', 'notas', [['sin', 'Sin borde'], ['fino', 'Borde fino'], ['barra', 'Barra de acento']], 'sin', 'sin'],
    ['fondo-nota', 'Fondo', 'notas', [['ninguno', 'Sin fondo'], ['papel', 'Claro'], ['tintado', 'Tintado']], 'tintado', 'tintado'],
    ['tamano-nota', 'Tamaño', 'notas', [['compacto', 'Compacto'], ['normal', 'Normal'], ['amplio', 'Amplio']], 'normal', 'normal'],
    ['lugar-nota', 'Ubicación', 'notas', [['hueco', 'En el hueco libre'], ['debajo', 'Debajo'], ['lado', 'Al lado']], 'hueco', 'hueco'],
    ['cabecera-nota', 'Cabecera', 'notas', [['mono', 'Mono'], ['negrita', 'Negrita']], 'mono', 'mono'],
    ['ayuda', 'Ayuda', 'interaccion', [['encima', 'Encima'], ['debajo', 'Debajo'], ['discreta', 'Debajo, discreta'], ['oculta', 'Oculta']], 'encima', 'oculta'],
    ['cajas', 'Plegado', 'interaccion', [['desplegadas', 'Todas desplegadas'], ['plegadas', 'Todas plegadas'], ['acordeon', 'Máximo una desplegada']], 'desplegadas', 'desplegadas'],
    ['recorrido', 'Recorrido', 'interaccion', [['segundo', 'Segundo color'], ['acento', 'Acento'], ['grueso', 'Más grueso']], 'segundo', 'acento'],
    ['pie', 'Pie', 'pie', [['dos', 'A dos lados'], ['izquierda', 'Todo a la izquierda'], ['derecha', 'Todo a la derecha'], ['centrado', 'Centrado'], ['oculto', 'Oculto']], 'dos', 'dos'],
  ];
  const GRUPOS = [['aspecto', 'Aspecto general'], ['cabecera', 'Cabecera'], ['cajas', 'Cajas'], ['flechas', 'Flechas y etiquetas'],
    ['notas', 'Notas'], ['interaccion', 'Interacción'], ['pie', 'Pie']];
  if (!temas.some(t => t[0] === 'tinta')) SELECTORES[0][5] = 'documento';

  // Lo que eligió el autor en cada figura, para la copia guardada.
  const autor = figs.map(f => ({ clase: f.className, tema: f.getAttribute('data-d-tema'),
    datos: Object.fromEntries(SELECTORES.slice(1).map(([k]) => [k, f.getAttribute('data-d-' + k)])) }));
  const leerFig = (f, k) => k === 'tema' ? (f.getAttribute('data-d-tema') || 'documento') : f.getAttribute('data-d-' + k);
  function poner(f, k, v) {
    if (typeof v === 'boolean') f.classList.toggle('d-no-' + k, !v);
    else if (k === 'tema') { if (v === 'documento') f.removeAttribute('data-d-tema'); else f.setAttribute('data-d-tema', v); }
    else f.setAttribute('data-d-' + k, v);
  }
  const CLAVE = 'documento-diagramas:' + ruta;
  let pref = leer(CLAVE, {}) || {};
  const todo = () => { figs.forEach(f => Object.entries(pref).forEach(([k, v]) => poner(f, k, v))); };
  todo();

  // Carriles y chips solo existen si los datos de la figura los pidieron: si ninguna los lleva, la casilla no se usa.
  const hay = { carriles: !!document.querySelector('.diagrama .d-carril-g'), chips: !!document.querySelector('.diagrama .d-chip'),
    fichas: !!document.querySelector('.diagrama [data-ficha]') };
  const fila = ([k, texto]) => {
    const falta = k in hay && !hay[k];
    return `<label class="lc-fila"${falta ? ' title="Ninguna figura los lleva: se piden en sus datos"' : ''}><input type="checkbox" data-dg="${k}"${falta ? ' disabled' : ''}> ${texto}</label>`;
  };
  const selector = ([k, texto, , ops]) => `<label class="lc-fila lc-modo dg-sel"><span>${texto}</span><select data-dg="${k}">` +
    ops.map(([v, t]) => `<option value="${v}">${t}</option>`).join('') + '</select></label>';
  const grupo = ([g, titulo]) => `<details class="dg-grupo" data-grupo="${g}"><summary>${titulo}</summary>` +
    SELECTORES.filter(x => x[2] === g).map(selector).join('') + CASILLAS.filter(x => x[2] === g).map(fila).join('') + '</details>';
  const t = herramienta('diagramas', 'Diagramas', 'Diagramas',
    '<div class="herr-lectura dg-ajustes"><div class="dg-acciones"><button type="button" class="lc-tablas" data-dg-poner="def">Por defecto</button>' +
    '<button type="button" class="lc-tablas" data-dg-poner="orig">Como el original</button></div>' + GRUPOS.map(grupo).join('') +
    `<p class="lc-ayuda">Vale para las ${figs.length === 1 ? 'figura' : figs.length + ' figuras'} del documento. Se recuerda en este navegador, para este documento.</p></div>`);
  // Los grupos empiezan plegados; el que abra el lector se recuerda, como los ajustes («Por defecto» no los toca).
  const CLAVE_G = 'documento-diagramas-grupos:' + ruta;
  const abiertos = leer(CLAVE_G, []) || [];
  t.el.querySelectorAll('.dg-grupo').forEach(d => {
    d.open = abiertos.includes(d.dataset.grupo);
    d.addEventListener('toggle', () => escribir(CLAVE_G, [...t.el.querySelectorAll('.dg-grupo[open]')].map(x => x.dataset.grupo)));
  });

  const controles = [...t.el.querySelectorAll('[data-dg]')];

  function pintar() {
    const f = figs[0];
    for (const c of controles) {
      const k = c.dataset.dg;
      if (c.type === 'checkbox') c.checked = !f.classList.contains('d-no-' + k) && !c.disabled;
      else c.value = leerFig(f, k) || c.options[0].value;
    }
  }
  controles.forEach(c => c.addEventListener('change', () => {
    pref[c.dataset.dg] = c.type === 'checkbox' ? c.checked : c.value;
    escribir(CLAVE, pref); todo(); pintar();
  }));
  t.el.querySelectorAll('[data-dg-poner]').forEach(b => b.addEventListener('click', () => {
    const orig = b.dataset.dgPoner === 'orig';
    pref = {};
    CASILLAS.forEach(x => { if (!(x[0] in hay) || hay[x[0]]) pref[x[0]] = x[orig ? 4 : 3]; });
    SELECTORES.forEach(x => { pref[x[0]] = x[orig ? 5 : 4]; });
    // «Por defecto», el tema con que se generó cada figura (el del documento si no lleva ninguno: decisión 307);
    // «Como el original», tinta, la piel de diagram-design.
    if (!orig) { delete pref.tema; figs.forEach((f, i) => poner(f, 'tema', autor[i].tema || 'documento')); }
    escribir(CLAVE, pref); todo(); pintar();
  }));
  pintar();
  aplicar();

  // En la copia guardada, cada figura como la dejó su autor.
  alCopiar.push(c => c.querySelectorAll('figure.diagrama').forEach((f, i) => {
    const a = autor[i]; if (!a) return;
    f.className = a.clase;
    if (a.tema) f.setAttribute('data-d-tema', a.tema); else f.removeAttribute('data-d-tema');
    Object.entries(a.datos).forEach(([k, v]) => { if (v == null) f.removeAttribute('data-d-' + k); else f.setAttribute('data-d-' + k, v); });
  }));
})();
