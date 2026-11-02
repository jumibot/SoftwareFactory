# Tras incorporar, el mod entrega las reglas sin reiniciar

- **Origen:** SoftwareFactory, 2026-11-02. En «Primeros cinco minutos de un usuario nuevo con la SF» (289), tras la primera instalación de un colega en Mac, se vio que al incorporar un proyecto las reglas de la SF no entran hasta reiniciar Claude Code. El propietario eligió «El mod las da solo».
- **Contexto:** el mod guarda en caché que la carpeta no es de la SF (`llevaRegla` en `contexto.ts`) hasta que se recarga, así que ni `/clear` entrega las reglas. Se valoró que la incorporación acabara pidiendo `/clear`.
- **Decisión:** el mod no guarda el «no es de la SF». Al detectar que la carpeta ya tiene `.sf/proyecto.json`, entrega las reglas y la orquestación con el siguiente mensaje, sin reiniciar. `/clear` queda como respaldo.
- **Consecuencias:** tras incorporar se sigue en la misma conversación con la SF activa.
- **Aplicada en:** pendiente; en la 289.
