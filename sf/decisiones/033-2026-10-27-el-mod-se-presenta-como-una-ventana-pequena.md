# El mod se presenta como una ventana pequeña

- **Origen:** SoftwareFactory, 2026-10-27. El propietario: «quiero que el mod se presente como una "pequeña ventana ascii"».
- **Decisión:** sobre el prompt, el mod dibuja siempre una caja de texto pequeña, con borde, que reúne el estado del proyecto, las peticiones en curso, las cuentas de la cola y de la realimentación, los avisos y la indicación «/sf para el detalle». Sustituye a la franja de una línea, que solo aparecía con peticiones. La norma «diagramas en SVG, nunca ASCII» es de los documentos; no se aplica a la interfaz del mod en el terminal.
- **Aplicada en:** mod de estado; `docs/como-funciona-la-software-factory.md`; plugin `sf` 0.11.0.
