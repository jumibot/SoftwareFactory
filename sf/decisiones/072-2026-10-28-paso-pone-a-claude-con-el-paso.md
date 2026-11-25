# /paso pone a Claude con el paso

- **Origen:** SoftwareFactory, 2026-10-28. Tras un `/paso`, la tarea no seguía hasta que el propietario decía «continúa».
- **Decisión:** `/paso` escribe el paso y, además, se lo pide a Claude como un mensaje del propietario: al momento si Claude está parado y, si está trabajando, al acabar el turno. Claude lo hace y sigue hasta terminar o hasta necesitar el feedback del propietario.
- **Aplicada en:** `plugins/sf/hooks/register.tsx`; metodología, 2; plantilla `claude-sf.md`; `docs/como-funciona-la-software-factory.md`.
- **Ampliada:** un paso pendiente (no los hechos ni el en curso) se quita con el «−» que lleva al final en el panel; con todos hechos, arriba sigue «6/6 pasos hechos», desplegable; cada tarea en curso de arriba despliega sus pasos; cada paso lleva «?», que pide a Claude que lo explique sin tocar nada; cada tarea de arriba con descripción se despliega para verla; con varias en curso, `/paso` pregunta a cuál va, salvo que empiece por su número (`/paso 64 texto`).
