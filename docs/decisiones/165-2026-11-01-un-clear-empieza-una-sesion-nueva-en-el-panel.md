# Un /clear empieza una sesión nueva en el panel

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Tras un /clear, el panel se queda en «Leyendo el estado…»» (239). Al arreglar la carga del panel tras un /clear, el propietario elige qué pasa con el modo prueba y con el inicio de la sesión.
- **Contexto:** un /clear acaba la conversación sin cerrar el proceso, y Claude Code no relanza el arranque del mod. El arreglo repite la carga tras el /clear; quedaba por decidir si eso cuenta como sesión nueva.
- **Decisión:** tras un /clear, el panel actúa como al empezar una sesión. El modo prueba se apaga y vuelve al plugin publicado. La duración de la sesión y las Cerradas empiezan de cero.
- **Consecuencias:** el panel no arrastra nada de la conversación anterior; para seguir probando la copia de trabajo tras un /clear, hay que volver a encender el modo prueba.
- **Aplicada en:** `plugins/sf/hooks/register.tsx`, con tests en `panel.test.tsx` (239).
