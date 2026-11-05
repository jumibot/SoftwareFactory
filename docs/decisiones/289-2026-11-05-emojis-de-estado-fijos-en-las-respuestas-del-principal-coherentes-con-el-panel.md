# Emojis de estado fijos en las respuestas del principal, coherentes con el panel

Fecha: 2026-11-05. Decidida por el propietario de la Software Factory.

El principal marca los estados con este juego fijo de emojis, el mismo en todos los proyectos:

- 🟡 tarea en curso
- 🟢 subagente trabajando
- 🔴 subagente terminado
- ⚪ en cola
- 🧪 lista para probar
- 👀 en observación
- 🔒 cerrada
- ✅ comprobado (pruebas pasadas, algo verificado)
- ❔ no comprobado
- ❓ te toca decidir o contestar
- ⭐ la opción recomendada
- ⚠️ aviso o riesgo
- ❌ algo falla

El rojo es «terminado», como el punto de los subagentes en el panel; por eso un fallo va con ❌. ✅ solo marca lo comprobado; lo hecho no lleva emoji. Juego corto: muchos emojis restan.

Para el antes y el después de un texto, y para los pasos y tareas que se añaden o se quitan, un bloque diff: las líneas con «+» salen en verde y las de «-» en rojo. Solo para eso.

Porqué: en el chat no hay colores, y el propietario quiere ver de un vistazo el estado de lo que se le cuenta, con los mismos significados que el panel.

Aplicada en: pendiente, tarea «Que las respuestas del principal usen emojis de estado fijos, coherentes con el panel» (374).
