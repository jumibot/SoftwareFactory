# Claude abre las páginas conectadas con una herramienta del mod, siempre a través de sf_proxy

Regla: una página conectada (informe o página de decisión que contesta al chat) nunca se abre directamente desde el disco: se sirve siempre a través de sf_proxy, con su token nuevo por apertura. Claude la abre con una herramienta del mod, que registra la página en sf_proxy y abre el navegador en su dirección; la misma herramienta sirve para mandar avisos a la página abierta. /sf_abrir y el botón Abrir del panel (452) usan el mismo camino.

Porqué: solo servida por el proxy la página puede mandar sus respuestas a la sesión; con una herramienta, Claude la abre cuando la prepara, sin que el propietario tenga que escribir una orden (norma del propietario, 28/11/2026, tarea 475).
