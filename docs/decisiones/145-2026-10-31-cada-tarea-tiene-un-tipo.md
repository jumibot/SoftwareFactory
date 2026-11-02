# Cada tarea tiene un tipo

- **Origen:** SoftwareFactory, 2026-10-31, tarea 196. El propietario: «al final de una tarea, entre paréntesis y en mayúsculas pon el tipo de tarea: deliberar, documentar, diseñar, implementar, especificar, ...».
- **Contexto:** el título no siempre dice qué clase de trabajo es una tarea, y eso cambia cómo se hace y cómo se cierra: una deliberativa no se prueba como una de código.
- **Decisión:** cada tarea lleva un tipo de una lista cerrada en infinitivo: deliberar, documentar, diseñar, implementar, especificar, corregir e investigar. Claude lo pone al crearla (`cola.py crear --tipo`) y se cambia con `cola.py tipo N T`. El panel lo muestra al final del título, entre paréntesis, en minúsculas y en el color del título: «Analizar el trabajo con la SF (investigar)»; al verlo, el propietario lo prefirió así a en mayúsculas y atenuado. Sin tipo, no sale nada. Las tareas abiertas al tomar la decisión las tipifica Claude.
- **Consecuencias:** el tipo es la base para tratar cada clase de tarea a su manera, como pide la tarea «Tareas deliberativas». Cómo funciona el panel se ajusta en su tarea de actualizar.
- **Aplicada en:** plugins/sf/tools/cola.py, plugins/sf/hooks/panel.tsx, plugins/sf/skills/flujo_tareas/SKILL.md y sus pruebas.
