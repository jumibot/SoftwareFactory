# Un juego fijo de emojis de estado en las respuestas del principal, coherente con el panel

El principal marca los estados con este juego fijo de emojis, el mismo en todos los proyectos y sin añadir otros:

- 🟡 tarea puesta en curso
- 🟢 subagente trabajando
- 🔴 subagente terminado
- ⚪ en cola
- ▶️ lista para probar (te toca ponerla en marcha)
- 👀 en observación
- 🔒 cerrada
- ✅ comprobado
- ❔ no comprobado
- ❓ decisión del propietario sobre una tarea
- ⭐ la opción recomendada
- ⚠️ aviso o riesgo
- ❌ algo falla

🟡 solo al poner una tarea en curso, no al mencionar una que ya lo está. ❓ solo en la pregunta que espera una decisión del propietario sobre una tarea, al final y en lugar del signo de cierre. El rojo es «terminado», como el punto de los subagentes en el panel; por eso un fallo va con ❌. ✅ solo marca lo comprobado; lo hecho no lleva emoji.

Para el antes y el después de un texto, y para los pasos y tareas que se añaden o se quitan, un bloque `diff`: las líneas con «+» salen en verde y las de «-» en rojo. Sus líneas, sin emojis: el color ya marca el estado.

Dónde va cada emoji en la línea y sus excepciones, en «La línea del foco es una excepción al juego fijo de emojis» (336), «Reglas del foco y del off-topic: las once recomendaciones del informe de la 431» (357) y «Las respuestas del principal, legibles en el terminal» (370).

Recoge lo que sigue valiendo de «Emojis de estado fijos en las respuestas del principal, coherentes con el panel» (289), que queda deprecada.

Porqué: en el chat no hay colores, y el propietario quiere ver de un vistazo el estado de lo que se le cuenta, con los mismos significados que el panel. Juego corto: muchos emojis restan.

Aplicada en: `sf:orquestacion` («Cómo escribir») y `references/porque.md`.
