# /redescribir: Claude vuelve a redactar una descripción

- **Origen:** SoftwareFactory, 2026-10-30, tarea 167. El propietario: «redescribir lo quiero para que una descripción que no se entienda la vuelvas a redactar para que se lea fácilmente, usando inferencia».
- **Contexto:** algunas descripciones de tareas se escriben deprisa o se juntan al fusionar y cuestan de leer. `cola.py redescribir` (decisión 125) solo guarda un texto dado.
- **Decisión:** el comando `/redescribir N` del panel pide a Claude que vuelva a redactar la descripción de la tarea N para que se lea fácilmente: frases claras y cortas, sin quitar ni añadir nada, cada idea en su párrafo. Claude enseña la propuesta y espera el OK del propietario; solo entonces la guarda con `cola.py redescribir N`. Sin número, con una tarea que no está en la cola o sin descripción, el panel lo dice y no pide nada.
- **Consecuencias:** el propietario arregla una descripción confusa con un comando; la escritura de la cola sigue pasando por el CLI.
- **Aplicada en:** plugins/sf/hooks/cola.ts, plugins/sf/hooks/register.tsx, plugins/sf/tests/panel.test.tsx y plugins/sf/skills/flujo_tareas/references/estados.md.
