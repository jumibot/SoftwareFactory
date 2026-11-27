/* Plegado y botón «Copiar» de los bloques de código (skill crear_documentos, recurso «Bloques de código»).
 * Cada caja .codigo (scripts/resaltar_codigo.py) recibe en su barra:
 *  - el botón de plegar, que es la propia barra: el nombre del lenguaje con su flecha (aria-expanded, aria-controls);
 *    desplegado al cargar, y plegado deja a la vista la barra con el número de líneas;
 *  - el botón «Copiar», que copia el código tal cual, sin el coloreado y entero, aunque haya ámbitos plegados;
 *  - en el margen, una flecha en cada línea que abre un ámbito (.amb, de resaltar_codigo.py), que pliega su cuerpo.
 * Un bloque sin lenguaje recibe una barra mínima con el rótulo «Código», para plegarse igual que los demás.
 * Sin JavaScript, el bloque se ve entero, con su lenguaje y sin botones. Al imprimir, todo desplegado, sin botones ni la
 * barra mínima (estilo_documento.css). */
(function () {
  // En la copia que guardan las herramientas del documento, el bloque como lo deja el generador: este script vuelve a
  // poner los botones al abrirla.
  (window.alCopiarDocumento = window.alCopiarDocumento || []).push(c => {
    c.querySelectorAll('.codigo-copiar, .codigo-lineas, .codigo-generico, .amb-flecha').forEach(x => x.remove());
    c.querySelectorAll('.amb-cuerpo').forEach(x => { x.hidden = false; x.removeAttribute('id'); });
    c.querySelectorAll('.amb.plegado').forEach(x => x.classList.remove('plegado'));
    c.querySelectorAll('pre.con-ambitos').forEach(x => x.classList.remove('con-ambitos'));
    c.querySelectorAll('.codigo-plegar').forEach(b => {
      const nombre = b.querySelector('.codigo-lenguaje');
      nombre ? b.replaceWith(nombre) : b.remove();
    });
    c.querySelectorAll('.codigo-barra:empty').forEach(x => x.remove());
    c.querySelectorAll('.codigo > pre').forEach(p => { p.hidden = false; if (/^codigo-bloque-/.test(p.id)) p.removeAttribute('id'); });
    c.querySelectorAll('.codigo.plegado').forEach(x => x.classList.remove('plegado'));
  });
  const copiar = texto => {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(texto);
    return new Promise((bien, mal) => {  // file:// en algunos navegadores, o sin permiso del portapapeles
      const area = document.createElement('textarea');
      area.value = texto;
      area.setAttribute('readonly', '');
      area.style.cssText = 'position:fixed;top:0;left:0;opacity:0;pointer-events:none';
      document.body.appendChild(area);
      area.select();
      let hecho = false;
      try { hecho = document.execCommand('copy'); } catch (_) { hecho = false; }
      area.remove();
      hecho ? bien() : mal(new Error('sin portapapeles'));
    });
  };
  let n = 0;
  document.querySelectorAll('.codigo').forEach(caja => {
    const pre = caja.querySelector(':scope > pre');
    const codigo = pre && pre.querySelector(':scope > code');
    if (!codigo || caja.querySelector('.codigo-plegar')) return;
    const texto = () => codigo.textContent.replace(/\n$/, '');
    let barra = caja.querySelector(':scope > .codigo-barra');
    if (!barra) {
      barra = document.createElement('div');
      barra.className = 'codigo-barra';
      caja.insertBefore(barra, caja.firstChild);
    }
    let nombre = barra.querySelector('.codigo-lenguaje');
    if (!nombre) {  // sin lenguaje: la barra mínima, con un rótulo genérico
      nombre = document.createElement('span');
      nombre.className = 'codigo-lenguaje codigo-generico';
      nombre.textContent = 'Código';
    }
    do { n += 1; } while (document.getElementById('codigo-bloque-' + n));
    if (!pre.id) pre.id = 'codigo-bloque-' + n;
    // Plegar y desplegar: la barra entera es el botón, salvo «Copiar».
    const plegar = document.createElement('button');
    plegar.type = 'button';
    plegar.className = 'codigo-plegar';
    plegar.setAttribute('aria-expanded', 'true');
    plegar.setAttribute('aria-controls', pre.id);
    plegar.title = 'Plegar o desplegar el código';
    const lineas = document.createElement('span');
    lineas.className = 'codigo-lineas';
    const cuantas = texto().split('\n').length;
    lineas.textContent = cuantas === 1 ? '1 línea' : cuantas + ' líneas';
    plegar.append(nombre, lineas);
    barra.insertBefore(plegar, barra.firstChild);
    plegar.addEventListener('click', () => {
      const abierto = plegar.getAttribute('aria-expanded') === 'true';
      plegar.setAttribute('aria-expanded', String(!abierto));
      pre.hidden = abierto;
      caja.classList.toggle('plegado', abierto);
    });
    // Copiar
    const boton = document.createElement('button');
    boton.type = 'button';
    boton.className = 'codigo-copiar';
    boton.textContent = 'Copiar';
    boton.title = 'Copiar el código';
    boton.setAttribute('aria-live', 'polite');  // «Copiado» se anuncia al lector de pantalla
    let reloj = 0;
    const avisar = t => {
      boton.textContent = t;
      clearTimeout(reloj);
      reloj = setTimeout(() => { boton.textContent = 'Copiar'; }, 1800);
    };
    boton.addEventListener('click', () => {
      copiar(texto()).then(() => avisar('Copiado'), () => avisar('No se pudo copiar'));
    });
    barra.appendChild(boton);
    // Ámbitos (scripts/resaltar_codigo.py): una flecha en el margen de cada línea que abre uno pliega su cuerpo; plegado,
    // la línea de apertura lleva «…» (estilo_documento.css) y sigue a la vista la de cierre. Las flechas no tienen
    // texto: «Copiar» copia siempre el código entero, también lo plegado.
    const ambitos = codigo.querySelectorAll('.amb');
    if (ambitos.length) pre.classList.add('con-ambitos');
    ambitos.forEach((amb, k) => {
      const cabeza = amb.querySelector(':scope > .amb-cabeza');
      const cuerpo = amb.querySelector(':scope > .amb-cuerpo');
      if (!cabeza || !cuerpo) return;
      cuerpo.id = pre.id + '-ambito-' + (k + 1);
      const flecha = document.createElement('button');
      flecha.type = 'button';
      flecha.className = 'amb-flecha';
      flecha.setAttribute('aria-expanded', 'true');
      flecha.setAttribute('aria-controls', cuerpo.id);
      flecha.setAttribute('aria-label', 'Plegar o desplegar: ' + cabeza.textContent.trim().slice(0, 60));
      flecha.addEventListener('click', () => {
        const abierto = flecha.getAttribute('aria-expanded') === 'true';
        flecha.setAttribute('aria-expanded', String(!abierto));
        cuerpo.hidden = abierto;
        amb.classList.toggle('plegado', abierto);
      });
      cabeza.insertBefore(flecha, cabeza.firstChild);
    });
  });
})();
