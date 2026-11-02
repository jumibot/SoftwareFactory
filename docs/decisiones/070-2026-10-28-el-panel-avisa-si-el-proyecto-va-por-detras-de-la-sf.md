# El panel avisa si el proyecto va por detrás de la SF

- **Origen:** SmartColdBox, 2026-10-28. El panel parecía antiguo: el plugin era el 0.32.1, pero el proyecto se había incorporado con la SF 0.13 y su `.sf/` era de entonces.
- **Decisión:** si la versión de `.sf/proyecto.json` es anterior (mayor.menor) a la del plugin, el panel muestra «SF 0.13 → 0.32.3» y un aviso con cómo ponerlo al día: pedir a Claude «pon el proyecto al día con la SF» (skill `sf:incorporar_proyecto_a_sf`). Los arreglos (tercer número) no avisan.
- **Precisada por:** «Un solo aviso de proyecto atrasado en el panel» (161): en el panel lateral, sin «→»; la «→» queda en la caja sobre el prompt.
- **Aplicada en:** `plugins/sf/hooks/lectura.ts` y `panel.tsx`; `docs/como-funciona-la-software-factory.md`.
