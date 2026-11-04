/* Lector de libros (.lector) y «Leer la historia completa». Sin librerías; sin JS, el texto se ve seguido. */
(function () {
  var CLAVE_PASO = 'sf-lector-paso';
  function modoPaso() { try { return localStorage.getItem(CLAVE_PASO) === 'hoja' ? 'hoja' : 'tinta'; } catch (e) { return 'tinta'; } }
  function ponerModoPaso(m) { try { localStorage.setItem(CLAVE_PASO, m); } catch (e) {} }
  // La marca en dos tonos: lo que va antes de la primera letra o cifra («/») y el resto («SF»).
  function marcaHTML(m) {
    var k = m.search(/[A-Za-z0-9]/), e = function (x) { return x.replace(/&/g, '&amp;').replace(/</g, '&lt;'); };
    return k > 0 ? e(m.slice(0, k)) + '<b>' + e(m.slice(k)) + '</b>' : e(m);
  }
  function paginar(lector, titulo) {
    var libro = lector.querySelector('.libro'); if (!libro) return null;
    var flujo = document.createElement('div'); flujo.className = 'libro-flujo';
    while (libro.firstChild) flujo.appendChild(libro.firstChild);
    libro.appendChild(flujo);
    var tinta = document.createElement('div'); tinta.className = 'lector-tinta'; tinta.setAttribute('aria-hidden', 'true'); libro.appendChild(tinta);
    var barra = document.createElement('div'); barra.className = 'lector-barra';
    var rotulo = document.createElement('span'); rotulo.className = 'lector-rotulo';
    rotulo.textContent = titulo || lector.getAttribute('data-titulo') || '';
    barra.appendChild(rotulo);
    lector.insertBefore(barra, libro);
    var bPaso = document.createElement('button'); bPaso.type = 'button'; bPaso.className = 'lector-btn lector-paso';
    function rotuloPaso() {
      var hoja = modoPaso() === 'hoja';
      bPaso.setAttribute('aria-pressed', String(hoja));
      bPaso.setAttribute('aria-label', hoja ? 'Pasar página como una hoja (pulsa para tinta electrónica)' : 'Pasar página con refresco de tinta (pulsa para hoja de papel)');
      bPaso.title = hoja ? 'Paso de página: hoja' : 'Paso de página: tinta';
      bPaso.textContent = hoja ? '❏' : '▣';
    }
    bPaso.onclick = function () { ponerModoPaso(modoPaso() === 'hoja' ? 'tinta' : 'hoja'); Array.prototype.forEach.call(document.querySelectorAll('.lector-paso'), function (b) { b._rotulo && b._rotulo(); }); };
    bPaso._rotulo = rotuloPaso; rotuloPaso(); barra.appendChild(bPaso);
    var fuente = lector.getAttribute('data-marca') ? lector : document.querySelector('.lector[data-marca]');
    if (fuente) {
      var marca = document.createElement('span'); marca.className = 'lector-marca'; marca.setAttribute('aria-hidden', 'true');
      marca.innerHTML = marcaHTML(fuente.getAttribute('data-marca'));
      ['--lector-marca', '--lector-marca-claro'].forEach(function (v) { var c = fuente.style.getPropertyValue(v); if (c) lector.style.setProperty(v, c); });
      barra.insertBefore(marca, barra.firstChild);
    }
    var pie = document.createElement('div'); pie.className = 'lector-pie';
    pie.innerHTML = '<button type="button" class="lector-btn ant" aria-label="Página anterior">‹</button>' +
      '<span class="lector-pagina" aria-live="polite"></span>' +
      '<button type="button" class="lector-btn sig" aria-label="Página siguiente">›</button>';
    lector.appendChild(pie);
    ['ant', 'sig'].forEach(function (c) {
      var t = document.createElement('button'); t.type = 'button'; t.className = 'lector-toque ' + c; t.tabIndex = -1;
      t.setAttribute('aria-hidden', 'true'); libro.appendChild(t);
    });
    lector.classList.add('paginado');
    if (!lector.hasAttribute('tabindex')) lector.tabIndex = 0;
    lector.setAttribute('role', 'region');
    if (!lector.hasAttribute('aria-label')) lector.setAttribute('aria-label', 'Lector: ' + (rotulo.textContent || 'libro'));
    var api = { pagina: 0, total: 1, barra: barra, flujo: flujo, alMedir: null };
    var indicador = pie.querySelector('.lector-pagina'), bAnt = pie.querySelector('.ant'), bSig = pie.querySelector('.sig');
    // Paso de página = ancho de columna + hueco, con el ancho fijado en píxeles enteros: así coincide con dónde pone
    // el navegador cada columna (en iOS Safari, column-count con anchos fraccionarios descuadraba el desplazamiento).
    var ancho = 0;
    function hueco() { return Math.round(parseFloat(getComputedStyle(flujo).columnGap) || 0); }
    function paso() { return ancho + hueco(); }
    api.paginaDe = function (el) {
      if (!paso()) return 0;
      var x = el.getBoundingClientRect().left - flujo.getBoundingClientRect().left;
      return Math.max(0, Math.floor((x + 2) / paso()));
    };
    api.ir = function (n) {
      api.pagina = Math.max(0, Math.min(api.total - 1, n));
      var antes = flujo.style.transform, previa = api._previa || 0; api._previa = api.pagina;
      flujo.style.transform = api.pagina ? 'translateX(' + (-api.pagina * paso()) + 'px)' : '';
      // Al cambiar de página, salvo con movimiento reducido: el refresco de la tinta electrónica (un negativo breve)
      // o, si el lector lo ha elegido, la hoja que se pasa.
      // La página nueva se pinta ya; el efecto va encima, con Web Animations (sin forzar el diseño ni esperar a nada),
      // y un toque nuevo corta el anterior.
      if (antes !== flujo.style.transform && !matchMedia('(prefers-reduced-motion: reduce)').matches && libro.animate) {
        if (api._efecto) api._efecto.cancel();
        if (modoPaso() === 'hoja') {
          var g = api.pagina > previa ? -62 : 62;
          libro.style.transformOrigin = g < 0 ? 'left center' : 'right center';
          api._efecto = libro.animate([{ transform: 'perspective(1400px) rotateY(' + g + 'deg)', opacity: .35 }, { transform: 'none', opacity: 1 }],
                                      { duration: 420, easing: 'cubic-bezier(.2,.7,.3,1)' });
        } else {
          api._efecto = tinta.animate([{ opacity: .85 }, { opacity: 0 }], { duration: 130, easing: 'ease-out' });
        }
      }
      indicador.textContent = 'Página ' + (api.pagina + 1) + ' de ' + api.total;
      bAnt.disabled = api.pagina === 0; bSig.disabled = api.pagina === api.total - 1;
    };
    api.medir = function () {
      flujo.style.columnWidth = ''; flujo.style.columnCount = ''; flujo.style.transform = '';
      ancho = Math.floor(flujo.clientWidth); if (!ancho) return;
      flujo.style.width = ancho + 'px'; flujo.style.columnWidth = ancho + 'px'; flujo.style.columnCount = 'auto';
      var actual = api.pagina; libro.scrollLeft = 0;
      api.total = Math.max(1, Math.round((flujo.scrollWidth + hueco()) / paso()));
      if (api.alMedir) api.alMedir();
      api.ir(Math.min(actual, api.total - 1));
    };
    bAnt.onclick = libro.querySelector('.lector-toque.ant').onclick = function () { api.ir(api.pagina - 1); };
    bSig.onclick = libro.querySelector('.lector-toque.sig').onclick = function () { api.ir(api.pagina + 1); };
    lector.addEventListener('keydown', function (e) {
      if (e.target.closest && e.target.closest('.lector-indice')) return;
      if (e.key === 'ArrowRight' || e.key === 'PageDown') { api.ir(api.pagina + 1); e.preventDefault(); }
      else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { api.ir(api.pagina - 1); e.preventDefault(); }
    });
    var x0 = null, y0 = null;
    libro.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
    libro.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0; x0 = null;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) api.ir(api.pagina + (dx < 0 ? 1 : -1));
    });
    libro.addEventListener('scroll', function () { libro.scrollLeft = 0; libro.scrollTop = 0; });
    addEventListener('resize', function () { flujo.style.width = ''; api.medir(); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(api.medir);
    document.addEventListener('toggle', api.medir, true);
    api.medir();
    return api;
  }

  // ── La historia completa: las partes narrativas del documento (.libro, .caso y .escena, salvo data-historia="no"),
  // seguidas y por capítulos, en un lector a pantalla completa. Salen del mismo texto: nada se duplica en el .md.
  function texto(el) { return (el && el.textContent || '').replace(/\s+/g, ' ').trim(); }
  function p(clase, html) { var e = document.createElement('p'); if (clase) e.className = clase; e.innerHTML = html; return e; }
  function historia() {
    var partes = Array.prototype.filter.call(document.querySelectorAll('.report-body .libro, .report-body .caso, .report-body .escena'),
      function (el) { return !el.closest('[data-historia="no"]') && !el.closest('.lector-capa'); });
    if (partes.length < 2) return null;
    var libro = document.createElement('div'); libro.className = 'libro';
    var capitulos = [];
    partes.forEach(function (el) {
      if (el.classList.contains('escena')) {
        var et = el.querySelector('.escena-etiqueta');
        if (et) libro.appendChild(p('libro-ornamento', ''));
        var ctx = el.querySelector('.escena-contexto'); if (ctx) libro.appendChild(p('libro-contexto', ctx.innerHTML));
        Array.prototype.forEach.call(el.querySelectorAll('.turno'), function (t) {
          var quien = t.querySelector('.ponente'), dice = t.querySelector(':scope > p:last-child');
          var nombre = quien ? (quien.childNodes[0] ? quien.childNodes[0].textContent : texto(quien)) : '';
          libro.appendChild(p('libro-dialogo', '<span class="libro-quien">' + nombre.trim() + '</span> ' + (dice ? dice.innerHTML : '')));
        });
        return;
      }
      var cap, tit;
      if (el.classList.contains('libro')) {
        cap = texto(el.querySelector('.libro-capitulo')); tit = texto(el.querySelector('.libro-titulo'));
      } else {
        var eti = texto(el.querySelector('.caso-etiqueta')).replace(/^El caso\s*·\s*/i, '').split(/\s*·\s*/);
        cap = eti[0] || ''; tit = eti.slice(1).join(' · ');
      }
      var c = p('libro-capitulo', cap); c.setAttribute('data-capitulo', ''); libro.appendChild(c);
      libro.appendChild(p('libro-titulo', tit || cap));
      var nom = tit ? cap + ' · ' + tit : cap; capitulos.push({ el: c, nombre: nom.charAt(0).toUpperCase() + nom.slice(1) });
      Array.prototype.forEach.call(el.querySelectorAll(':scope > p, :scope > .libro-flujo > p'), function (q) {
        if (q.classList.contains('libro-capitulo') || q.classList.contains('libro-titulo') || q.classList.contains('caso-etiqueta')) return;
        libro.appendChild(p(q.className.indexOf('libro-') === 0 ? q.className : '', q.innerHTML));
      });
    });
    return { libro: libro, capitulos: capitulos };
  }

  function abrirHistoria(boton) {
    var h = historia(); if (!h) return;
    var capa = document.createElement('div'); capa.className = 'lector-capa';
    capa.setAttribute('role', 'dialog'); capa.setAttribute('aria-modal', 'true'); capa.setAttribute('aria-label', 'La historia completa');
    var lector = document.createElement('div'); lector.className = 'lector lector-completo';
    lector.appendChild(h.libro);
    capa.appendChild(lector); document.body.appendChild(capa);
    document.documentElement.classList.add('lector-abierto');
    var fin1 = document.createElement('div'); fin1.className = 'libro-fin';
    fin1.innerHTML = '<p class="libro-ornamento"></p><button type="button">Ver el documento</button>';
    h.libro.appendChild(fin1);
    var titulo = (document.querySelector('.lector[data-titulo]') || {}).getAttribute ? document.querySelector('.lector[data-titulo]').getAttribute('data-titulo').split('·')[0].trim() : 'La historia';
    var api = paginar(lector, titulo || 'La historia');
    var cerrar = document.createElement('button'); cerrar.type = 'button'; cerrar.className = 'lector-btn lector-cerrar';
    cerrar.setAttribute('aria-label', 'Ir al documento'); cerrar.title = 'Ir al documento'; cerrar.textContent = '×';
    var bIndice = document.createElement('button'); bIndice.type = 'button'; bIndice.className = 'lector-btn lector-btn-indice';
    bIndice.setAttribute('aria-label', 'Índice de capítulos'); bIndice.setAttribute('aria-expanded', 'false'); bIndice.textContent = '☰';
    api.barra.insertBefore(bIndice, api.barra.firstChild); api.barra.appendChild(cerrar);
    var indice = document.createElement('nav'); indice.className = 'lector-indice'; indice.hidden = true;
    indice.setAttribute('aria-label', 'Capítulos');
    var lista = document.createElement('ol'); indice.appendChild(lista);
    lector.insertBefore(indice, lector.querySelector('.libro'));
    api.alMedir = function () {
      lista.innerHTML = '';
      h.capitulos.forEach(function (c) {
        var li = document.createElement('li'), b = document.createElement('button'); b.type = 'button';
        var pg = api.paginaDe(c.el);
        b.innerHTML = '<span>' + c.nombre + '</span><span class="lector-indice-pag">' + (pg + 1) + '</span>';
        b.onclick = function () { api.ir(pg); alternar(false); lector.focus(); };
        li.appendChild(b); lista.appendChild(li);
      });
    };
    function alternar(si) { indice.hidden = !si; bIndice.setAttribute('aria-expanded', String(si)); if (si) { var b = lista.querySelector('button'); if (b) b.focus(); } }
    bIndice.onclick = function () { alternar(indice.hidden); };
    function fin() {
      removeEventListener('resize', api.medir); document.removeEventListener('keydown', tecla, true);
      capa.remove(); document.documentElement.classList.remove('lector-abierto', 'historia-primero');
      var vuelta = boton || document.querySelector('.lector-abrir button'); if (vuelta) vuelta.focus({ preventScroll: !boton });
    }
    function tecla(e) {
      if (e.key === 'Escape') { if (!indice.hidden) alternar(false); else fin(); e.preventDefault(); }
      else if (e.key === 'Tab') {  // el foco no sale de la capa
        var f = Array.prototype.filter.call(capa.querySelectorAll('button, [tabindex="0"]'), function (x) { return !x.disabled && x.offsetParent !== null; });
        if (!f.length) return; var a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { z.focus(); e.preventDefault(); }
        else if (!e.shiftKey && document.activeElement === z) { a.focus(); e.preventDefault(); }
      }
    }
    cerrar.onclick = fin; fin1.querySelector('button').onclick = fin;
    capa.addEventListener('click', function (e) { if (e.target === capa) fin(); });
    document.addEventListener('keydown', tecla, true);
    api.medir(); lector.focus();
    // Pantalla de entrada, al abrir el documento en la historia: el logo grande y la invitación (data-invitacion);
    // al pulsar el logo, la página 1.
    var fuente = document.querySelector('.lector[data-al-abrir="historia"]');
    if (!boton && fuente && fuente.getAttribute('data-marca')) {
      var portada = document.createElement('div'); portada.className = 'lector-portada';
      ['--lector-marca', '--lector-marca-claro'].forEach(function (v) { var c = fuente.style.getPropertyValue(v); if (c) portada.style.setProperty(v, c); });
      var inv = fuente.getAttribute('data-invitacion') || 'Pulsa el logo para entrar en la historia';
      var bp = document.createElement('button'); bp.type = 'button'; bp.className = 'lector-portada-logo';
      bp.innerHTML = marcaHTML(fuente.getAttribute('data-marca')); bp.setAttribute('aria-label', inv);
      // El tema del documento, no la marca: data-tema y data-subtitulo; por defecto, el título del documento,
      // partido por sus dos puntos («Tema: subtítulo»).
      var h1 = document.querySelector('h1'), titulo = (h1 ? h1.textContent : document.title).trim(), dp = titulo.indexOf(':');
      var tema = fuente.getAttribute('data-tema') || (dp > 0 ? titulo.slice(0, dp) : titulo).trim();
      var sub = fuente.hasAttribute('data-subtitulo') ? fuente.getAttribute('data-subtitulo') : (dp > 0 ? titulo.slice(dp + 1).trim() : '');
      var cab = document.createElement('div'); cab.className = 'lector-portada-tema';
      var ht = document.createElement('h2'); ht.textContent = tema; cab.appendChild(ht);
      if (sub) { var hs = document.createElement('p'); hs.className = 'lector-portada-sub'; hs.textContent = sub.charAt(0).toUpperCase() + sub.slice(1); cab.appendChild(hs); }
      var tp = document.createElement('p'); tp.className = 'lector-portada-inv'; tp.textContent = inv; tp.setAttribute('aria-hidden', 'true');
      portada.appendChild(cab); portada.appendChild(bp); portada.appendChild(tp); (lector.querySelector('.libro') || lector).appendChild(portada);
      portada.setAttribute('role', 'group'); portada.setAttribute('aria-label', tema);
      // Aviso de ficción, en letra pequeña abajo, como en los créditos de una novela (data-aviso; vacío, sin aviso).
      var aviso = fuente.hasAttribute('data-aviso') ? fuente.getAttribute('data-aviso') : 'Historia de ficción: personajes y escenas son imaginados.';
      if (aviso) { var pa = document.createElement('p'); pa.className = 'lector-portada-aviso'; pa.textContent = aviso; portada.appendChild(pa); }
      bp.onclick = function () { portada.remove(); api.ir(0); lector.focus(); };
      bp.focus();
    }
  }

  function todos() {
    var lectores = Array.prototype.slice.call(document.querySelectorAll('.report-body .lector'));
    lectores.forEach(function (l) { paginar(l); });
    if (lectores.length && historia()) {
      var caja = document.createElement('p'); caja.className = 'lector-abrir';
      var b = document.createElement('button'); b.type = 'button'; b.textContent = 'Leer la historia completa';
      b.onclick = function () { abrirHistoria(b); };
      caja.appendChild(b); lectores[0].parentNode.insertBefore(caja, lectores[0].nextSibling);
      if (document.querySelector('.lector[data-al-abrir="historia"]')) { abrirHistoria(null); return; }
    }
    document.documentElement.classList.remove('historia-primero');
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', todos); else todos();
})();
