# Botón «Poner en curso» en las tareas de PENDIENTES: un clic, y Claude mira los choques después

Fecha: 2026-11-05. Decidida por el propietario de la Software Factory.

## Qué se decide

- Las tareas de PENDIENTES llevan en el panel el botón «Poner en curso».
- Basta un clic, sin confirmación: se deshace devolviendo la tarea a PENDIENTES.
- Los choques con otras tareas los mira Claude después del clic y avisa si hay alguno.

## Por qué

Poner en curso es lo más frecuente que el propietario pide por el chat. «Poner en curso» es como ya lo dice, un clic basta porque se deshace fácil, y mirar los choques es trabajo de Claude, no un paso más para el propietario.

## Aplicada en

Tarea 373: botón del panel (`panel.tsx`) y aviso al principal.
