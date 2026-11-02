# Las deliberativas se cierran con «Finalizar deliberación»

- **Origen:** SoftwareFactory, 2026-11-02. Al repasar cómo se cierran las tareas deliberativas en «Tareas deliberativas: registrar decisiones y dilemas abiertos» (274), el propietario: «tendrían un botón de finalizar deliberación que en realidad es un alias para cerrar».
- **Contexto:** una deliberativa no se prueba y se trata como documental («Una tarea deliberativa da un informe y las tareas que salgan», 218). Su cierre es dar por terminada la deliberación con lo decidido, y los temas abiertos salen antes a otras tareas («En una deliberativa, lo que es de otra tarea se propone separar», 221). El botón de cerrar de una tarea de código no lo dice.
- **Decisión:** en el panel, una tarea deliberativa muestra el botón «Finalizar deliberación» en lugar del de cerrar. Hace lo mismo que cerrar (la misma orden de `cola.py`); solo cambia el rótulo. No es un alias de un nombre viejo, sino el nombre de esa acción en ese tipo de tarea, así que no choca con «En observación, sin alias ni rastros» (215).
- **Consecuencias:** el panel elige el rótulo del botón de cierre por el tipo de la tarea. Antes de finalizar, Claude ofrece separar los temas abiertos (221).
- **Aplicada en:** pendiente; en «Documentos nuevos a develop en cada vuelta, y abrirlos en el navegador» (297).
