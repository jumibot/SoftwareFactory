# Una sola sesión con la SF por proyecto

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Una sola sesión con la SF por proyecto: las demás arrancan con ella apagada» (281). Lo propone el propietario: «muerto el perro, muerta la rabia».
- **Contexto:** una segunda sesión de Claude Code en el mismo proyecto recibía los avisos de subagentes de la primera y llegó a poner en curso una tarea y lanzar su subagente. Además, las dos sesiones comparten copia de trabajo, rama activa, cola y worktrees.
- **Decisión:**
  1. Solo una sesión por proyecto tiene la SF activa. La segunda y las siguientes arrancan con la SF apagada y un aviso.
  2. Cada sesión con la SF activa deja un latido cada minuto. Una sesión sin latido durante unos 3 minutos se da por cerrada, y la siguiente que arranque toma la SF.
  3. `/sf_forzar_activa` activa la SF en la sesión donde se escribe y la apaga en la otra. Sirve para probar en una sesión nueva o tras un cuelgue. `/sf_forzar_inactiva` apaga la SF en la sesión donde se escribe, que deja de dar latido, para que otra la tome.
  4. El mismo latido de cada minuto es el que comprueba si hay que ofrecer REFRESCAR (decisión 177).
- **Consecuencias:** no hay avisos ni órdenes de la SF cruzados entre sesiones. Probar en una sesión nueva exige `/sf_forzar_activa`. Un cuelgue deja la SF bloqueada como mucho unos 3 minutos.
- **Aplicada en:** pendiente: el mod (281); «Cómo funciona el panel» (198).
