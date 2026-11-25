# redescribir no guarda la descripción anterior

- **Origen:** SoftwareFactory, 2026-10-30, tarea 168. Al redactar de nuevo la descripción de la 162, el propietario: «los párrafos antiguos, que has redactado de nuevo, se pueden quitar»; «deja de guardar el antes».
- **Contexto:** `cola.py redescribir` (decisión 125) anotaba en el historial de la tarea el evento `redescrita` con la descripción entera anterior, «antes: …», que repetía textos largos que ya no sirven.
- **Decisión:** `redescribir` anota el evento `redescrita` sin la descripción anterior.
- **Consecuencias:** el historial dice cuándo y quién cambió la descripción, pero no qué decía; si hace falta, está en las copias de la cola (`.sf/copias/`).
- **Aplicada en:** plugins/sf/tools/cola.py y plugins/sf/tests/test_cola.py.
