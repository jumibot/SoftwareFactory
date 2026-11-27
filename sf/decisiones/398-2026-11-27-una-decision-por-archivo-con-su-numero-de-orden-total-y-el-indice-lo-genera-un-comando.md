# Una decisión por archivo, con su número de orden total, y el índice lo genera un comando

Cada decisión es un archivo de `sf/decisiones/` (208), `NNN-AAAA-MM-DD-titulo.md`: el número de orden total, la fecha del registro (390) y el título sin tildes ni signos. La registra `cola.py decision`, que da el número y hace el commit en `develop`. El índice no se escribe a mano: lo genera `indice_decisiones.py`, sin Claude, con la más alta arriba (389). Sus archivos se juntan con `merge=union` y se regeneran, así que dos ramas que añaden decisiones no chocan.

Un proyecto con su registro en un solo archivo lo parte con `indice_decisiones.py --migrar` al ponerse al día.

Recoge lo que sigue valiendo de «Una decisión por archivo, en `docs/decisiones/`» (108), que queda deprecada.

Porqué: todas las decisiones iban en un solo `docs/decisiones.md`, y dos ramas que añadían decisiones chocaban siempre en él al cerrar con squash. El propietario de la Software Factory: «prefiero que cada decisión se convierta en un md distinto y crear una carpeta de decisiones»; «añade el número de orden total como primera columna» (108).

Aplicada en: `plugins/sf/tools/indice_decisiones.py` y `cola.py` (`decision`); `.gitattributes`; `sf:incorporar_proyecto_a_sf`; metodología, «Decisiones».
