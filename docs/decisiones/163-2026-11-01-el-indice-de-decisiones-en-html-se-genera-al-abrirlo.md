# El índice de decisiones en html se genera al abrirlo

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Las decisiones del proyecto, en DOCUMENTOS y en html» (203). Ante el choque en git del `README.html` de las decisiones entre ramas paralelas, el propietario: «que se materialice on the fly».
- **Contexto:** el índice en html pesa unos 195 KB y cambia con cada decisión nueva; versionado, dos ramas que añaden decisiones chocan en él.
- **Decisión:** `docs/decisiones/README.html` no se versiona. Se genera en el momento de abrirlo, al pulsar «Decisiones» en DOCUMENTOS, a partir de los archivos de decisión; el `README.md` sigue versionado.
- **Consecuencias:** no hay choques por el html; una copia nueva del repositorio no lo trae, pero el panel lo crea al primer clic.
- **Aplicada en:** `plugins/sf/hooks/cola.ts` (`abrirDecisiones`), `lectura.ts` y `panel.tsx`; `plugins/sf/tools/indice_decisiones.py` (`--html`); `.gitignore`; `sf:incorporar_proyecto_a_sf`, en el `.gitignore` de los proyectos (203).
