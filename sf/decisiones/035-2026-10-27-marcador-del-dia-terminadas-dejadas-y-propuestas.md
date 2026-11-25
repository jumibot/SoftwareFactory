# Marcador del día: terminadas, dejadas y propuestas

- **Sustituida** el 2026-10-27 por «Fuera el marcador de la última fila».
- **Origen:** SoftwareFactory, 2026-10-27. El propietario: «para los tdh como yó quiero que el mod añada un + por tarea terminada y un - por tarea empezada y dejada pendiente», «en la última row alineados a la derecha», «cada propuesta añadida en la sesión un ·» y «tambien un contador de prompts enviados por sesión».
- **Contexto:** con cambios de tarea frecuentes, lo terminado no se percibe como avance y lo dejado a medias pasa desapercibido.
- **Decisión:** en la última fila, a la derecha (las etiquetas de modo), el mod muestra `+` en verde por cada petición en curso que termina, `−` atenuado por cada una dejada a medias (vuelve a la cola o sigue en curso al cerrar la sesión) y `·` en frambuesa por cada propuesta para la SF añadida en la sesión; delante, atenuado, el número de prompts enviados en la sesión. Lo cuenta él mismo a partir de la cola; una dejada que luego se termina pasa a `+`. El `+` y el `−` se guardan por proyecto y se reinician cada día; los `·`, por sesión. Las líneas que enmarcan la zona de escritura no las puede dibujar un mod; la última fila es lo más cercano.
- **Aplicada en:** mod de estado; `docs/como-funciona-la-software-factory.md`; plugin `sf` 0.13.0.
