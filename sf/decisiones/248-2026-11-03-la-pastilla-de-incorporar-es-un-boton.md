# La pastilla de incorporar es un botón

- **Origen:** SoftwareFactory, 2026-11-03. Al ver en la app de escritorio la bienvenida del panel en una carpeta sin SF, el propietario pidió que la pastilla «incorpora este proyecto a la SF» fuera un botón que arranque la incorporación. Aclaró: «Se mantiene el splash y ese mensaje destacado se convierte en un botón. Solo he dicho esto».
- **Contexto:** la bienvenida («Bienvenida del panel publicada y pantalla completa al incorporar», 245) muestra el logo, una frase y la pastilla como texto: el usuario tiene que escribirlo.
- **Decisión:** la bienvenida se mantiene; la pastilla pasa a ser un botón que, al pulsarlo, arranca la incorporación como si se hubiera escrito «incorpora este proyecto a la SF».
- **Consecuencias:** ninguna otra pieza cambia.
- **Aplicada en:** `plugins/sf/hooks/cola.ts` (`pedirIncorporar`), `hooks/panel.tsx` y `hooks/bienvenida.ts` (`ORDEN_EMPEZAR`), con su prueba; pendiente: «Cómo funciona el panel» («Qué es»).
