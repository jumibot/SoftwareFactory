/* Catálogo de emojis: barra con buscador por nombre, ocultar tonos de piel y copiar al pulsar. */
(function(){
  var rejillas=[].slice.call(document.querySelectorAll('.emojis'));
  if(!rejillas.length)return;
  var barra=document.createElement('div');barra.id='barra-emojis';
  barra.innerHTML='<input type="search" name="buscar" id="buscar-emoji" placeholder="Buscar por nombre (en inglés)" aria-label="Buscar emoji por nombre" autocomplete="off">'
   +'<label><input type="checkbox" name="sin-tonos" id="sin-tonos"> Ocultar tonos de piel</label>'
   +'<span class="estado" role="status" aria-live="polite">Pulsa un emoji para copiarlo.</span>';
  document.body.appendChild(barra);
  var q=barra.querySelector('#buscar-emoji'),st=barra.querySelector('#sin-tonos'),estado=barra.querySelector('.estado');
  var sub=[].slice.call(document.querySelectorAll('details.subseccion')),sec=[].slice.call(document.querySelectorAll('details.seccion'));
  var guardado=new Map();
  function filtrar(){
    var t=q.value.trim().toLowerCase(),n=0;
    rejillas.forEach(function(r){[].forEach.call(r.children,function(b){
      var ok=!t||b.title.toLowerCase().indexOf(t)>=0;b.classList.toggle('fuera',!ok);
      if(ok&&!(st.checked&&b.classList.contains('tono')))n++;});});
    [sub,sec].forEach(function(lista){lista.forEach(function(d){
      var hay=!!d.querySelector('.emojis button:not(.fuera)');
      d.classList.toggle('fuera-emojis',!!t&&!hay);
      if(t){if(!guardado.has(d))guardado.set(d,d.open);if(hay)d.open=true;}
      else if(guardado.has(d)){d.open=guardado.get(d);guardado.delete(d);}});});
    estado.textContent=t?(n===1?'1 encontrado':n+' encontrados'):'Pulsa un emoji para copiarlo.';
  }
  q.addEventListener('input',filtrar);
  st.addEventListener('change',function(){document.body.classList.toggle('sin-tonos',st.checked);filtrar();});
  function copiar(t){
    if(navigator.clipboard&&navigator.clipboard.writeText)return navigator.clipboard.writeText(t);
    var a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();
    try{document.execCommand('copy')}finally{a.remove()}return Promise.resolve();
  }
  document.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('.emojis button');if(!b)return;
    copiar(b.textContent).then(function(){estado.textContent='Copiado '+b.textContent+' ('+b.title+')';},
      function(){estado.textContent='No se pudo copiar '+b.textContent;});
  });
})();
