# Origen de la skill `configurar_proyecto`

- **Creada:** 2026-11-02, en la SF, en la tarea «Skill y orden de barra para cambiar la configuración del proyecto» (299).
- **Decisiones del propietario (2026-11-02):** la configuración de un proyecto se cambia pidiéndoselo a Claude, con menús, sin tarea y fuera del panel; tiene su propia skill y su orden de barra, y se ofrece al poner al día el proyecto («La configuración se cambia pidiéndoselo a Claude, con menús», 228, corregida el mismo día). Los comandos de la SF empiezan por `sf_` (198). El esquema de `.sf/proyecto.json` (227) y lo fijo, lo detectado y lo elegido, del informe «Configuración inicial» (263) y de las decisiones 224 a 226, 229, 230, 233 y 234.
- **Referencias de partida:** los menús y las detecciones de `sf:incorporar_proyecto_a_sf` (tarea 193), y las lecturas de la configuración de `cola.py` (`leer_configuracion`) y del mod (`configuracion.ts`).
- **Código:** `tools/configuracion.py` (ver y detectar, solo lee) y la orden `/sf_config` en `hooks/register.tsx`, que pasa el encargo a Claude.
