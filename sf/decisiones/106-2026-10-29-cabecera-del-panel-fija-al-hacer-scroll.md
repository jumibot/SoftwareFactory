# Cabecera del panel fija al hacer scroll

- **Origen:** SoftwareFactory, 2026-10-29. El propietario pidió fijar la cabecera: al hacer scroll, se iba.
- **Decisión:** el panel no deja mover su ventana. Con la rueda o las teclas, sube los bloques bajo la cabecera, que queda arriba con sus dos primeras filas: los prompts, la duración, la etiqueta de prueba y el proyecto, y la rama. La tarea en curso sube con los bloques (el propietario, al probarla: «la cabecera son las dos primeras rows no tiene que incluir las tareas en curso»). El motor de mods lo prevé así para un panel con cabecera; el tope de abajo sale del alto del panel.
- **Aplicada en:** `plugins/sf/hooks/panel.tsx` y sus pruebas; `docs/como-funciona-el-panel.md`.
