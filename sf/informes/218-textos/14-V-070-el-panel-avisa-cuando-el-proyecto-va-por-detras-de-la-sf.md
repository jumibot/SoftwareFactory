# El panel avisa cuando el proyecto va por detrás de la SF

Si la versión de `.sf/proyecto.json` es anterior (mayor.menor) a la del plugin, el panel avisa de que el proyecto va por detrás y dice cómo ponerlo al día: pedir a Claude «pon el proyecto al día con la SF» (skill `sf:incorporar_proyecto_a_sf`). Los arreglos (tercer número) no avisan.

Dónde se ve el aviso y la versión, en «Un solo aviso de proyecto atrasado en el panel» (161) y «La línea gris del proyecto sale del panel» (166).

Recoge lo que sigue valiendo de «El panel avisa si el proyecto va por detrás de la SF» (070), que queda deprecada.

Porqué: en SmartColdBox, el panel parecía antiguo: el plugin era el 0.32.1, pero el proyecto se había incorporado con la SF 0.13 y su `.sf/` era de entonces.

Aplicada en: `plugins/sf/hooks/lectura.ts` y `panel.tsx`.
