# Una tarea que espera y no puede volver a la cola lleva un paso «Esperar a …»

- **Origen:** SoftwareFactory, 2026-11-01, tarea «El panel avisa cuando la sesión usa un plugin más viejo que el instalado» (229). El propietario decidió que esperase al cierre de la 255, pero, con rama, no podía volver a la cola (decisión 170). El propietario: «En caso de no poder volver a la cola añadir un paso de esperando a ...».
- **Contexto:** esperar es estar pendiente, y lo natural es devolver la tarea a la cola; una tarea en curso con rama no vuelve a ella.
- **Decisión:** cuando una tarea en curso tiene que esperar a otra cosa y no puede volver a la cola, se le añade un paso «Esperar a …» que dice a qué espera, y su subagente no trabaja hasta que se cumpla. Al cumplirse, se marca hecho y se sigue.
- **Consecuencias:** en el panel se ve por qué una tarea en curso está parada. Hay que recogerlo en `sf:orquestacion`.
- **Aplicada en:** la 229 (paso «Esperar a que se cierre la 255»); `sf:orquestacion` (258).
