# Sin línea de estado

- **Origen:** SmartColdBox, 2026-10-27. El propietario, ante la línea `⚠ sf: Sin SF`: «esto ya no tiene sentido porque pasa al panel». En SoftwareFactory, el mismo día, ante `⚠ sf: SF · repositorio de la SF` tras reiniciar: «sigue!!!!!!!!!!!!!!!!».
- **Contexto:** Claude Code pone «⚠ sf:» delante de la línea de estado que escribe un mod, y esa línea repetía la primera de la caja sobre el prompt.
- **Decisión:** el mod de la SF no escribe en la línea de estado. El proyecto, la fase, la devslice y los avisos se ven en la caja sobre el prompt y en `/sf`. La línea de estado queda para el propietario.
- **Consecuencias:** sale de pendientes la propuesta «La línea de estado sobra si está el panel».
- **Aplicada en:** mod de estado (plugin `sf` 0.14.0); `docs/como-funciona-la-software-factory.md`; README del plugin; especificación, 2.
