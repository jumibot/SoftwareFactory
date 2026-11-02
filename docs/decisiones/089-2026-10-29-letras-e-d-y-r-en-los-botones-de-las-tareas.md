# Letras E, D y R en los botones de las tareas

- **Origen:** SoftwareFactory, 2026-10-29, tarea 108, al probarla. El propietario: «vamos a cambiar los símbolos del panel para mayor coherencia E eliminar, D descartar y R revertir».
- **Decisión:** los botones de acción sobre una tarea son letras rojas a la derecha: **E** elimina (antes ✕) y **D** descarta (antes ⊘); al primer clic, «E eliminar» o «D descartar», en negrita. La D va negra y en negrita sobre fondo amarillo, para distinguirla de la E (el propietario: «para mejor diferenciar E y D pon el bg de la D en amarillo»). La D es también la letra de la descartada en Cerradas. **R** será el de revertir: aún no hay botón, va en una tarea aparte. Sustituye los símbolos de «Eliminar una tarea» y del botón de descartar.
- **Aplicada en:** `plugins/sf/hooks/panel.tsx` y sus pruebas; `docs/como-funciona-el-panel.md` y `docs/como-funciona-la-software-factory.md`; metodología, 2; plantilla `claude-sf.md`.
