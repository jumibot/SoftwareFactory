# Los repositorios públicos se revisan cada 15 días con la herramienta de la SF y lo encontrado se avisa en el panel

La SF revisa los repositorios públicos del propietario con `revision_publica.py`, ampliado para recorrer cada repositorio y su historial: secretos, datos personales y rutas de la máquina. Además se activa en ellos el escaneo de secretos de GitHub (secret scanning y push protection), que es gratis.

Cada 15 días: el latido del panel mira la fecha de la última revisión y, si venció, avisa; revisar es un clic. No es una tarea periódica de la cola: las tareas periódicas en general van como propuesta aparte.

Lo encontrado lo avisa el panel con la lista corta (repositorio, archivo, motivo) y una orden para ver la completa. Cada repositorio se arregla en una sesión de su proyecto: la SF no escribe en proyectos ajenos.

Opciones: solo GitHub (solo secretos), una rutina en la nube (no ve las rutas ni el usuario de la máquina, que es lo que más se cuela) o tareas periódicas en la cola (choca con el máximo de seis en curso y es un cambio grande). Se elige la herramienta de la SF con aviso del panel.

Porqué: hoy la SF solo revisa lo que sale al subir develop y en RELEASE (259), no lo ya publicado; el propietario da el OK a las recomendaciones del informe «Cuidar lo que se publica» (tarea 331).

Aplicada en: pendiente, en las tareas que salen de la 331.
