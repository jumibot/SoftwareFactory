# El mod impide que un subagente escriba la cola

- **Origen:** SoftwareFactory, 2026-10-29. «Solo el principal escribe la cola» era una regla escrita, con un pendiente: bloquearlo con un hook.
- **Decisión:** el mod bloquea Write, Edit y NotebookEdit de `.sf/peticiones.json` cuando la llamada viene de un subagente. Lo sabe por el `agentId` de la llamada, que solo llevan las de un subagente; las del principal no lo llevan. Las órdenes de terminal no se controlan: para ellas vale la regla.
- **Aplicada en:** metodología, 2 («Orquestación con subagentes»); mod, `control.ts`; Cómo funciona el panel («Qué controla»); Cómo funciona la Software Factory.
