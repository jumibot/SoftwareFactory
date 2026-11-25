# Orquestación con un subagente vivo por tarea

- **Origen:** SoftwareFactory, 2026-10-31, tarea «Skill de orquestación» (205), a partir del análisis del trabajo con la SF en el desarrollo del panel (194). El propietario: «tener subagentes esperando instrucciones y dejando libre el agente principal lo veo una gran ventaja».
- **Contexto:** los ajustes que pedía el propietario durante la prueba se hacían en el principal, que quedaba ocupado: la «Mismo diseño de tarea en todas las secciones del panel» (210) llevó 9 ajustes en unos 25 minutos, y la 196, 12 ajustes en unas 2,5 horas y unos 360.000 tokens. Además, el panel no reflejaba el trabajo: tareas sin pasos, informes de subagentes sin recoger, la C sin salir y la cola desfasada respecto a lo que el propietario cambiaba desde el panel.
- **Decisión:** el principal se comporta así con las tareas y sus subagentes:
  - **Un subagente vivo por tarea en curso**, retomado con cada encargo del propietario sobre ella, también durante la prueba. Todo cambio de la tarea lo hace su subagente; el principal solo escribe la cola y las decisiones. Corrige «El principal orquesta; los subagentes ejecutan» (083) en que una modificación durante la prueba se hacía en el principal.
  - **Consultar la cola** (`cola.py lista`) antes de informar o actuar sobre una tarea: el propietario la cambia desde el panel.
  - **Recoger el trabajo del subagente y marcar sus pasos en cuanto vuelve.**
  - **Con el último paso hecho, `listo --prueba`** sin esperar, para que el panel muestre la C.
  - **Sugerir `/redescribir NN`** cuando una tarea acumula pasos y su título queda desfasado.
  - **Al poner una tarea en curso, especificar y planificar**: si su enunciado no basta, preguntar; después, sus pasos en la cola.
  - **Sin tarea en curso no se trabaja**, salvo para reorganizar la cola (fusionar, separar, redescribir, añadir pasos, cambiar tipos).
  - **Al cerrar, parar el subagente y quitar su worktree.** El subagente trabaja siempre en su rama auxiliar (`sub-NN`), así que la rama de la tarea queda libre y la T y la C funcionan sin quitar el worktree; la C falló en la 194 porque su worktree tenía activa la propia rama de la tarea.
- **Consecuencias:** el principal queda libre para hablar con el propietario mientras los subagentes esperan instrucciones. La metodología, la plantilla `claude-sf.md` y el CLAUDE.md de la SF se ajustan en su tarea de actualizar.
- **Aplicada en:** plugins/sf/skills/orquestacion/SKILL.md y plugins/sf/skills/flujo_tareas/SKILL.md.
