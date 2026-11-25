# Etiquetas «A Testing» en las tareas en curso y «Cerrar» en las de Testing

- **Origen:** SoftwareFactory, 2026-11-01, tarea 241. Ante si quería un botón para pasar a Testing o para dar por probada, el propietario: «en realidad ambas cosas. el botón para dar por probada una tarea de testing sería CERRAR».
- **Contexto:** el menú de etiquetas de la decisión 168 no tenía forma de pasar una tarea a Testing ni de darla por probada desde el panel; las de Testing solo podían revertirse.
- **Decisión:** la tarea en curso que se puede cerrar lleva, tras Cerrar, la etiqueta «A Testing» («¿A Testing? sí»), que la pasa a Testing con `cola.py a-testing`. La tarea en Testing lleva la etiqueta «Cerrar» («¿Cerrar? sí»), que la da por probada con `cola.py probada`: para el propietario, dar por probada una tarea de Testing es cerrarla. Revertir sigue al final, en rojo.
- **Consecuencias:** amplía la 168. El propietario pasa a Testing y da por probadas las tareas sin pasar por Claude.
- **Aplicada en:** `plugins/sf/hooks/panel.tsx`, `plugins/sf/hooks/cola.ts` y sus pruebas (241).
