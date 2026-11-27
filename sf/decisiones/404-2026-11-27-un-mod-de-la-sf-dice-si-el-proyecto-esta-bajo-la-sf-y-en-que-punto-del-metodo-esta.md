# Un mod de la SF dice si el proyecto está bajo la SF y en qué punto del método está

El plugin `sf` lleva un mod que dice si el proyecto está bajo la SF y, con metodología, su fase y su devslice. Lo lee de `.sf/` (027). Lo enseña en la caja sobre el prompt; no en la línea de estado (037) ni, de momento, en el panel lateral (166).

Recoge lo que sigue valiendo de «Estado del proyecto en `docs/sf.json` y mod de estado» (019), que queda deprecada.

Porqué: el propietario de la Software Factory: «Me gustaría un mod de UI que me diga si el proyecto está bajo sf, en qué fase…»; «creo que el mod me aportará más en este momento fundacional y experimental de sf» (019).

Aplicada en: `plugins/sf/hooks/lectura.ts` y `panel.tsx` (`lineaEstado`, la caja sobre el prompt).
