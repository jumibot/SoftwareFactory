# Lo último tocado, arriba; la tarea principal, la última tocada

- **Origen:** SoftwareFactory, 2026-10-30, tarea 166. El propietario: «por defecto lo último tocado arriba. Esto hará que las tareas con las que se haga algo sean más visibles. En cualquier cola»; y, sobre la tarea principal: «que la principal sea la última tocada».
- **Contexto:** las listas del panel salían en el orden del archivo o de número más alto a más bajo, y la tarea principal (la primera de arriba, que da nombre a la sesión) era la en curso de número más alto. Las tareas con las que se trabaja no destacaban.
- **Decisión:** en cada lista de tareas del panel (arriba, Pendientes, Testing y Cerradas), la que ha cambiado la última va arriba. El último cambio es la fecha más reciente del `historial` de la tarea; en Cerradas cuenta también la hora de cierre en la sesión, la más reciente de las dos. Las tareas sin historial van detrás, de número más alto a más bajo. En Pendientes, las en curso siguen arriba. La tarea principal es la en curso tocada la última, así que anotar un paso en otra en curso la cambia.
- **Consecuencias:** el panel sigue lo que se está haciendo; el nombre de la sesión puede cambiar entre tareas en curso.
- **Aplicada en:** plugins/sf/hooks/cola.ts, plugins/sf/hooks/lectura.ts, plugins/sf/types/index.d.ts y plugins/sf/tests/panel.test.tsx.
