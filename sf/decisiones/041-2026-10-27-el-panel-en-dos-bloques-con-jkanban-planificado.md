# El panel, en dos bloques; con JKanban, Planificado

- **Origen:** SoftwareFactory, 2026-10-27. El propietario: «tengo dudas de que tiene que mostrar y su uso… como se combinara con el JKanban?», y sobre Sin probar, Lo último hecho y Realimentación: «no son de la sesión». A la propuesta: «1 ok, 2 depende para nimiedades como cambia este color no merece la pena backlog más aún si no queda pendiente y 3 cuando este el jkanban dejamos un apartado de planificado y ok a quitar las fases. De los pendientes si se han pasado a backlog se quitan sino no». Y: «y el apartado de realimentación????».
- **Contexto:** el panel mezclaba lo de la sesión con lo del proyecto. Con JKanban, el tablero será la fuente del trabajo y el panel no debe repetirlo.
- **Decisión:**
  1. El panel se ordena en dos bloques: **Esta sesión** (En curso, En cola, Marcador y Hecho en esta sesión, con los commits desde que empezó) y **Proyecto** (Sin probar, Fases, Pendientes, Realimentación y Documentos).
  2. Realimentación va en Proyecto solo en la SF, donde son las propuestas que esperan decisión. En otro proyecto se quita: las mejoras registradas ya las cuenta el marcador.
  3. Con JKanban, una petición pasa al backlog solo si queda pendiente; las menores que se resuelven en el momento, no.
  4. Con JKanban, el panel añade una sección Planificado y deja de mostrar Fases. Pendientes sale cuando sus elementos están en el backlog; si no, se queda.
- **Consecuencias:** JKanban es la fuente del trabajo planificado y el panel, la ventana de la sesión. Los puntos 3 y 4 se aplican al incorporar JKanban; las propuestas pasarán a ser tareas del proyecto SoftwareFactory.
- **Aplicada en:** mod de estado (puntos 1 y 2); metodología (6) y skill `sf:metodologia`; especificación de la SF; `docs/como-funciona-la-software-factory.md`; plugin `sf` 0.26.0.
