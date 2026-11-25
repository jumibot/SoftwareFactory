# Las automatizaciones del plugin, configurables y avisando antes que bloquear

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Auditar que la skill de orquestación recoge todo lo ordenado» (216). Al proponer pasar a código las reglas mecánicas de `sf:orquestacion`, el propietario preguntó si eso ayudaría o perjudicaría a distribuir el plugin a terceros.
- **Contexto:** pasar reglas a código las hace cumplirse siempre y adelgaza la skill, pero vuelve el plugin más rígido para quien trabaje de otra forma, y parte de lo hecho asume rutas y herramientas de esta máquina.
- **Decisión:** toda regla que pase a código (mod, panel, `cola.py` o hooks) es configurable con un interruptor en `.sf/proyecto.json`, con un valor por defecto prudente, y no usa rutas fijas de esta máquina. Lo que vigila, avisa antes que bloquear. Se empieza por tres: cargar la skill al empezar, tras /clear y tras compactar; avisar de tareas en curso sin subagente y de subagentes terminados sin recoger; y `cola.py encargo N`.
- **Consecuencias:** el plugin se adopta con menos que aprender sin imponer el flujo del propietario. Cada automatización lleva su interruptor y sus pruebas.
- **Aplicada en:** las tareas 248, 249 y 250.
