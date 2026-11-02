# Al fusionar, cada descripción en su párrafo

- **Origen:** SoftwareFactory, 2026-10-30, tarea 165. El propietario: «al fusionar y concatenar descripciones deja un punto y aparte entre ellas».
- **Contexto:** al fusionar la 158 y la 160 en la 162, las tres descripciones quedaron seguidas en un solo bloque, difícil de leer. El CLI no tenía forma de cambiar una descripción.
- **Decisión:** al fusionar, en el panel (`/fusionar`) y en `cola.py fusionar`, las descripciones se unen con una línea en blanco: cada una en su párrafo. El panel pinta cada párrafo aparte. La orden nueva `cola.py redescribir N "texto"` cambia la descripción de una tarea (vacía, la quita), con el evento `redescrita` en su historial.
- **Consecuencias:** una tarea fusionada deja ver de qué partes viene sin decir su origen; las descripciones se corrigen sin tocar la cola a mano.
- **Aplicada en:** plugins/sf/tools/cola.py, plugins/sf/hooks/cola.ts, plugins/sf/hooks/panel.tsx, plugins/sf/tests/test_cola.py, plugins/sf/tests/panel.test.tsx y plugins/sf/skills/flujo_tareas/references/estados.md.
