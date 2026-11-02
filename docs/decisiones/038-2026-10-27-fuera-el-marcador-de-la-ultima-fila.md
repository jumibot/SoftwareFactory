# Fuera el marcador de la última fila

- **Origen:** SoftwareFactory, 2026-10-27. El propietario, ante «19 prompts +++++» en la última fila: «ya lo veo redundante teniendo el panel lateral ... fuera».
- **Contexto:** el panel lateral tiene la sección Sesión, con prompts, peticiones añadidas, hechas, probadas, dejadas y propuestas. La última fila repetía parte de eso, contaba el día y no la sesión, y las dos cifras no cuadraban.
- **Decisión:** el mod deja de dibujar en la última fila y deja de llevar la cuenta del día. Las métricas quedan solo en la sección Sesión del panel. Sustituye a «Marcador del día: terminadas, dejadas y propuestas».
- **Aplicada en:** mod de estado; especificación de la SF; `docs/como-funciona-la-software-factory.md`; plugin `sf` 0.24.0.
