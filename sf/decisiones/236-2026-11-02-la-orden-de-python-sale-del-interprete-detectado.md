# La orden de Python sale del intérprete que se detecta, no de `python` fijo

- **Origen:** SoftwareFactory, 2026-11-02. En «Primeros cinco minutos de un usuario nuevo con la SF» (289), el diagnóstico de lo que atasca a un usuario nuevo dejó decisiones para el propietario, que eligió la opción recomendada.
- **Contexto:** la SF llama siempre a `python` (el lanzador fijo de cola.py y las órdenes que entrega el mod). En macOS y Linux suele no existir, y allí es `python3`; el panel ya detecta qué intérprete hay.
- **Decisión:** el mod da las órdenes de Python con el intérprete que detecta en la máquina, no con `python` fijo. Se descartó pedir en la guía que `python` responda (solo basta en Windows) y cambiar a `python3` (rompe Windows).
- **Consecuencias:** la SF funciona igual en Windows, macOS y Linux sin preparar nada. Lo que hoy escribe `python -I -X utf8 …` (reglas, encargos, skills) pasa a usar la orden que entrega el mod.
- **Precisada el mismo día:** el mínimo es Python 3.9, el que trae macOS sin instalar nada; el mod prueba `python`, `python3` y `py` y se queda con el primero que sea 3.9 o posterior (propietario, en la 314).
- **Aplicada en:** `plugins/sf/hooks/python.ts` y `hooks/contexto.ts` (`contextoPython`); `plugins/sf/tools/cola.py` (`orden_python`, en el encargo); pruebas del panel y `tests/test_plataformas.py`; `sf:orquestacion`; `sf:flujo_tareas`; `plugins/sf/README.md` («Requisitos»); pendiente: «Cómo funciona la Software Factory».
