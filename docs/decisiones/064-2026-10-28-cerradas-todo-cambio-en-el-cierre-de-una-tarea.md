# Cerradas: todo cambio en el cierre de una tarea

- **Origen:** SoftwareFactory, 2026-10-28. Al dar por probadas la 48, la 50, la 52 y la 70, cerradas en otra sesión, no salían en Cerradas. El propietario: «porqué las que he ido probando no han pasado a cerradas?»; «El cambio de estado en cerradas las devuelve a cerradas»; «ojo y las reabiertas por un bug».
- **Decisión:** Cerradas muestra las tareas cuyo cierre cambia en la sesión: las que pasan a Testing (T), las que se dan por probadas (C), aunque se cerraran en otra sesión, y las reabiertas (en rojo), también por un bug después de salir de la cola. Cada cambio la pone arriba y la devuelve a la lista si se había quitado con «quitar las probadas». La reabierta tras salir de la cola vuelve con su número y `reabierta: true`, porque el panel no puede saber que existió en otra sesión.
- **Aplicada en:** mod de estado; metodología (2); especificación; `docs/como-funciona-la-software-factory.md`; plugin `sf` 0.31.3.
