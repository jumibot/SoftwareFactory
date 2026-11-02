# La marca del subagente, verde trabajando y roja en espera

- **Origen:** SoftwareFactory, 2026-11-01, tarea «El ● del subagente, verde trabajando y rojo en espera» (225). El propietario: «pon en verde el botón del agente cuando trabaje y en rojo cuando esté en stop». Al probarlo, la ⚙ salía gris: Windows Terminal la dibuja como emoji y no toma el color; el propietario aceptó cambiarla por ●.
- **Decisión:** la marca del subagente de una tarea es ●, en verde mientras trabaja y en rojo mientras espera instrucciones. Un subagente parado no lleva marca.
- **Consecuencias:** sustituye la ⚙ atenuada (trabajando) y la gris azulada (en espera) de la primera versión de la 225. «Rojo solo para las reabiertas» (159) se refiere a los números de tarea, no a esta marca.
- **Aplicada en:** `plugins/sf/hooks/panel.tsx`, `lectura.ts`, `estilo.ts` (`MARCA_SUBAGENTE`), `cola.ts`, `register.tsx` y sus pruebas (225).
