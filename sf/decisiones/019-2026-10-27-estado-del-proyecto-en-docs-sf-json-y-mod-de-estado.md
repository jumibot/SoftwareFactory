# Estado del proyecto en `docs/sf.json` y mod de estado

Estado: deprecada el 2026-11-27 por «Un mod de la SF dice si el proyecto está bajo la SF y en qué punto del método está» (404); lo demás, por «La carpeta `.sf/` identifica el proyecto y guarda su estado» (027), «Sin línea de estado» (037) y «La línea gris del proyecto sale del panel» (166).

- **Origen:** SoftwareFactory, 2026-10-27: «Me gustaría un mod de UI que me diga si el proyecto está bajo sf, en qué fase…»; «creo que el mod me aportará más en este momento fundacional y experimental de sf».
- **Decisión:** cada proyecto bajo la SF declara su estado en `docs/sf.json`. El mod de estado del plugin `sf` lo muestra en la línea de estado y en el panel `/sf`.
- **Consecuencias:** cuando JKanban esté integrado, el estado vivo estará en el kanban y `sf.json` solo resumirá. Sigue abierta la idea del propietario de una carpeta `sf-status` en cada proyecto o de tirar de JKanban (propuesta «Dónde vive el estado de cada proyecto»).
- **Aplicada en:** metodología, 2 y 6; especificación, 2.
