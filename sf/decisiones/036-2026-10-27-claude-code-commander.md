# Claude Code Commander

- **Origen:** SoftwareFactory, 2026-10-27. El propietario, sobre la ventana del mod fuera de la terminal: «una aplicación a parte en python o lo que sea ;-) y websockets», «será el claudecode driver» y, sobre su alcance: «todo lo que propones además permtir lanzar tareas del jkanban del proyecto sobre claude code. Todo y ya se que es impreciso y mucho decir pero creo que va ha ser una pieza clave de sf. Además de llevar métricas para poner control a los descontrolados hombres orquesta del software». Tecnología: «python y tkinter». Después, el mismo día: «espera antes de decidir como desarrollamos el ccd quiero que se pueda usar en tabley y móvil asi será una ventana flotante del todo (ajajaja)». Y el nombre: «en lugar de ccd que sea ccc (commander)».
- **Contexto:** el mod solo se dibuja dentro de Claude Code y ve una sesión: la suya. Con varios proyectos a la vez falta una vista y un mando de todas las sesiones, y nada mide cómo se trabaja con ellas.
- **Opciones:** una página HTML por sesión, abierta en el navegador (solo muestra); una aplicación aparte que reúne todas las sesiones.
- **Decisión:** la SF tendrá una aplicación aparte, el **Claude Code Commander**, como pieza clave. Alcance, que se irá concretando:
  1. ver todas las sesiones abiertas, con su proyecto, fase, peticiones y avisos;
  2. dar órdenes a las sesiones (por ejemplo, cambiar el estado de una petición o dejar texto en su prompt);
  3. conducir Claude Code: abrir y cerrar sesiones, lanzar tareas y enviar prompts;
  4. lanzar sobre Claude Code las tareas del proyecto en JKanban;
  5. llevar métricas del trabajo, para poner control al desarrollador que lo hace todo a la vez.

  Vive dentro del plugin `sf`. Se usa desde el ordenador, la tableta y el móvil. La tecnología se decidirá más adelante: Python con tkinter, que se eligió primero, queda descartado porque no llega a la tableta ni al móvil. Porque una sola pieza fuera de la terminal puede ver y mover todas las sesiones, y medir, cosa que ningún mod puede hacer por sí solo.
- **Consecuencias:** el mod de cada sesión pasa a ser el enlace con el Commander: le envía su estado y ejecuta las órdenes que le tocan, de modo que se respeta «Un proyecto por sesión». Absorbe la propuesta «Lista de sesiones abiertas en `/sf`». El lanzamiento de tareas de JKanban depende de incorporar su MCP. Quedan por concretar, en la propuesta «Claude Code Commander: lo que falta concretar»: la tecnología, el canal entre sesiones y Commander, cómo se llega a él desde la tableta y el móvil, qué métricas, cómo se lanzan sesiones y tareas, y el orden de construcción.
- **Aplicada en:** especificación, 2 («Claude Code Commander — acuerdo»); `docs/propuestas.md`.
