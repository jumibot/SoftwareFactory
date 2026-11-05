# La sesión apagada avisa y propone /sf_forzar_activa cuando la activa deja de latir, y avisa de que se trabaja sin la SF

Fecha: 2026-11-05. Decidida por el propietario de la Software Factory.

## Qué se decide

- Cuando la sesión con la SF activa deja de latir, la sesión apagada no toma la SF sola: avisa y propone `/sf_forzar_activa`.
- Una sesión con la SF apagada avisa de que se trabaja sin la SF.

## Por qué

Que la SF salte sola a otra sesión puede encenderla en una que el propietario no mira, o cuando la otra solo estaba colgada un momento. Avisar y proponer la orden deja el cambio en sus manos. Trabajar sin la SF sin saberlo lleva a confusión: hay que verlo.

## Aplicada en

Pendiente: tarea 281.
