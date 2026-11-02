# La P de probar pasa a T, de Test Mode

- **Origen:** SoftwareFactory, 2026-10-29, tarea 157. El propietario: «deberíamos cambiar la P por una T que signifique Test Mode».
- **Contexto:** el botón P del panel activa con git la rama de una tarea para probarla. La P sugería que pulsarlo daba la tarea por probada, cuando solo la pone en prueba.
- **Decisión:** el botón pasa a ser T, de Test Mode, en Pendientes, arriba y en Testing, con el mismo color verde en negrita y el mismo ancho. Pulsarlo pone la tarea en prueba, no la da por probada. Los avisos del botón empiezan por «T:».
- **Consecuencias:** la T coincide con la letra de los códigos de las tareas en Testing («4T»); el propietario acepta la coincidencia. Las claves internas (`probar-tarea:…`) y las funciones (`probarTarea`, `probable`) no cambian.
- **Aplicada en:** plugins/sf/hooks/panel.tsx, plugins/sf/hooks/cola.ts y sus pruebas.
