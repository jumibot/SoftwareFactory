# Toda tarea se despliega y lleva su etiqueta «?»

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Etiqueta «?» en el menú de la tarea: Claude explica la tarea al propietario» (254). El propietario pide «añadir un comando a tareas ? para que se explique la tarea al propietario» y, ante si toda tarea pasa a poder desplegarse: «todas desplegables».
- **Contexto:** el menú de etiquetas de la decisión 168 solo se ve al desplegar la tarea, y una tarea sin descripción, pasos ni órdenes no se podía desplegar.
- **Decisión:** el menú de cada tarea lleva una etiqueta «?»: al pulsarla, el panel pide a Claude que explique la tarea al propietario de forma breve y sencilla (qué es, en qué punto está y qué espera de él), sin hacer ni cambiar nada. Toda tarea se puede desplegar, aunque solo tenga esa etiqueta.
- **Consecuencias:** sustituye la consecuencia de la 168 «toda tarea con alguna orden se puede desplegar»: ahora son todas.
- **Aplicada en:** `plugins/sf/hooks/panel.tsx`, `plugins/sf/hooks/cola.ts` y sus pruebas (254).
