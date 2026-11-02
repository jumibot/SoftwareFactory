/* Secciones y tarjetas plegables de los documentos del generador común (skill crear_documentos).
 * Cada sección es un <details> que se pliega tocando su título. Este script añade:
 * abrir la sección de destino al seguir un enlace interno (menú, referencias, insignias),
 * el botón «Plegar todo / Desplegar todo» del menú, un botón «Plegar las tarjetas / Desplegar las tarjetas»
 * delante de cada bloque de tarjetas plegables y abrir todo al imprimir.
 * Sin JavaScript, las secciones se ven abiertas y se pliegan igual tocando el título. */
(function () {
  document.documentElement.classList.add('js');
  const secciones = [...document.querySelectorAll('details.seccion')];
  const abrirHasta = el => {
    for (let d = el && el.closest('details'); d; d = d.parentElement && d.parentElement.closest('details')) d.open = true;
  };
  const destino = hash => { try { return hash.length > 1 && document.getElementById(decodeURIComponent(hash.slice(1))); } catch { return null; } };
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const el = destino(a.getAttribute('href'));
    if (el) abrirHasta(el);
  });
  const alCargar = () => { const el = destino(location.hash); if (el) { abrirHasta(el); el.scrollIntoView(); } };
  // Tarjetas plegables («::: tarjetas N plegables»): abiertas en pantallas anchas, plegadas al cargar en el móvil.
  if (matchMedia('(max-width: 640px)').matches)
    document.querySelectorAll('details.tarjeta.plegable').forEach(d => { d.open = false; });

  // «Plegar las tarjetas / Desplegar las tarjetas» delante de cada bloque con tarjetas plegables (también preguntas y fichas).
  (window.alCopiarDocumento = window.alCopiarDocumento || []).push(c => c.querySelectorAll('.plegar-tarjetas').forEach(x => x.remove()));
  document.querySelectorAll('.tarjetas, .fichas').forEach(bloque => {
    const tarjetas = [...bloque.querySelectorAll(':scope > details.tarjeta.plegable')];
    if (tarjetas.length < 2) return;
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'plegar-tarjetas';
    const rotularBloque = () => { b.textContent = tarjetas.some(d => d.open) ? 'Plegar las tarjetas' : 'Desplegar las tarjetas'; };
    b.addEventListener('click', () => { const abrir = !tarjetas.some(d => d.open); tarjetas.forEach(d => { d.open = abrir; }); rotularBloque(); });
    tarjetas.forEach(d => d.addEventListener('toggle', rotularBloque));
    rotularBloque();
    bloque.before(b);
  });

  window.addEventListener('hashchange', alCargar);
  alCargar();  // después de plegar las tarjetas, para que el destino del enlace quede abierto

  const boton = document.querySelector('.plegar');
  const rotular = () => { if (boton) boton.textContent = secciones.some(d => d.open) ? 'Plegar todo' : 'Desplegar todo'; };
  if (boton) boton.addEventListener('click', () => {
    const abrir = !secciones.some(d => d.open);
    secciones.forEach(d => { d.open = abrir; });
    rotular();
  });
  secciones.forEach(d => d.addEventListener('toggle', rotular));
  rotular();

  // Al imprimir se abre todo (secciones y tarjetas); después se recupera cómo estaba.
  let antes = null, plegables = [];
  window.addEventListener('beforeprint', () => {
    plegables = [...document.querySelectorAll('details')];
    antes = plegables.map(d => d.open); plegables.forEach(d => { d.open = true; });
  });
  window.addEventListener('afterprint', () => { if (antes) plegables.forEach((d, i) => { d.open = antes[i]; }); antes = null; });
})();
