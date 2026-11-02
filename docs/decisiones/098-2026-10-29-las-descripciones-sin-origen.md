# Las descripciones, sin origen

- **Origen:** SoftwareFactory, 2026-10-29, tarea 106, al definir `/fusionar`. El propietario: «los detalles del origen (fusionada) y de quien ha creado una tarea no me importan y me enredan la descripción. no las pongas nunca (decisión)».
- **Decisión:** la descripción de una tarea no lleva su origen dentro de la cola («Separada de la 89», «Fusionada con la 105») ni quién la creó. Solo dice qué es la tarea.
- **Consecuencias:** `/split` deja de poner «Separada de la N». Sustituye en parte a «/split separa pasos en una tarea nueva».
- **Aplicada en:** metodología, 2 («Pasos de una tarea»); plantilla `claude-sf.md`; `plugins/sf/hooks/cola.ts` y sus pruebas; `docs/como-funciona-el-panel.md`.
