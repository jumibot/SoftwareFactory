# La línea gris del proyecto sale del panel

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Los avisos del panel, en la cabecera con fondo blanco» (244), vista en sprite_animation con la 1.2.5. El propietario, señalando «SF 1.1.0 · 1/7 Visión»: «esto fuera».
- **Contexto:** bajo la cabecera, el panel lateral pintaba una línea gris con la versión de la SF con que se incorporó el proyecto, la fase y la devslice. Con el aviso de proyecto atrasado ya en la cabecera, la línea repetía parte de lo mismo.
- **Decisión:** la línea gris del proyecto, de momento, no sale en el panel lateral. La caja sobre el prompt conserva la suya.
- **Consecuencias:** sustituye, en el panel lateral, lo que «Un solo aviso de proyecto atrasado en el panel» (161) decía de la línea gris; la fase y la devslice dejan de verse en el panel lateral hasta que se decida dónde van.
- **Aplicada en:** `plugins/sf/hooks/panel.tsx` y sus pruebas (244).
