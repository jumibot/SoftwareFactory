# Agentes del plugin, uno por familia de tarea

Fecha: 2026-11-04. Decidida por el propietario de la Software Factory.

El plugin lleva un agente por familia de tarea (código, deliberativa y documental), con las reglas fijas del encargo dentro (worktree y rama auxiliar, no escribir la cola, no tocar documentos compartidos, formato de commits, forma del informe) y sus skills precargadas. Lo propio de cada tarea lo leen con «cola.py encargo N»; el principal solo les pasa lo que no está en la cola.

Porqué: medido en las últimas sesiones largas, el 84 % de cada encargo es texto fijo que el principal vuelve a escribir en cada lanzamiento. Con el texto fijo dentro del agente, los encargos son de pocas líneas, el principal queda libre antes y cada agente sabe ya trabajar en su familia de tarea. Descartado un agente solo para la cola o un orquestador aparte: cada operación sería de 2 a 3 veces más lenta que una orden de cola.py, y un subagente no puede preguntar al propietario (informe «Liberar al agente principal», tarea 358).

Aplicada en: la tarea «Agentes especializados, uno por familia de tarea» (304).
