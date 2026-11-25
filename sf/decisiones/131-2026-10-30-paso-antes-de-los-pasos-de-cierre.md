# /paso, antes de los pasos de cierre

- **Origen:** SoftwareFactory, 2026-10-30, tarea 145. Lo propuso el subagente al pasar el panel al CLI; el propietario lo aceptó.
- **Contexto:** `/paso` añadía el paso al final de la tarea, detrás de «Probar la tarea» y «Cerrar la tarea». El CLI `cola.py paso añadir` lo pone delante de ellos, y el panel pasa a usar el CLI.
- **Decisión:** un paso nuevo, también el de `/paso`, entra antes de «Probar la tarea» y «Cerrar la tarea» si la tarea los tiene.
- **Consecuencias:** los pasos de cierre quedan siempre al final, y la C no sale hasta hacer el paso nuevo.
- **Aplicada en:** plugins/sf/tools/cola.py, plugins/sf/hooks/cola.ts y docs/como-funciona-el-panel.md.
