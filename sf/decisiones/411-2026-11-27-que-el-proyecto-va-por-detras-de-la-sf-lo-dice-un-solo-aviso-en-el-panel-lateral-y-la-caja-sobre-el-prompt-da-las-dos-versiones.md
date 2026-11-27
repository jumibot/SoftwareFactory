# Que el proyecto va por detrás de la SF lo dice un solo aviso en el panel lateral, y la caja sobre el prompt da las dos versiones

En el panel lateral, que el proyecto va por detrás de la SF lo dice solo su aviso, en la cabecera con los demás (164): «incorporado con la SF 1.1.0; va por la 1.2.2: pide a Claude «pon el proyecto al día con la SF»». El panel lateral no lo repite en otra línea (166).

La caja pequeña sobre el prompt, que sale cuando no está el panel lateral, no lleva ese aviso: da las dos versiones en su primera línea, «SF 1.1.0 → 1.2.2 · Proyecto · …».

Recoge lo que sigue valiendo de «Un solo aviso de proyecto atrasado en el panel» (161), que queda deprecada.

Porqué: en SmartColdBox y sprite_animation, el panel lateral decía lo mismo dos veces, en la línea gris «SF 1.1.0 → 1.2.2 · 1/7 Visión» y en el aviso; el propietario de la Software Factory, al ver el arreglo: «mantenla» (161).

Aplicada en: `plugins/sf/hooks/panel.tsx` (`lineaEstado` y los avisos) y sus pruebas.
