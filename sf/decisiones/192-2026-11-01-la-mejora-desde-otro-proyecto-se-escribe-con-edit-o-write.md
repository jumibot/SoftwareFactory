# La mejora desde otro proyecto se escribe con Edit o Write

**Sustituida** el 2026-11-01 por «Sin registro ni mejoras de la SF desde otros proyectos».

- **Origen:** SoftwareFactory, 2026-11-01, tarea «Registrar una mejora desde otro proyecto deja docs/propuestas.md de la SF sin commit» (276). El propietario acepta la opción recomendada.
- **Contexto:** el mod lleva a `develop`, con su commit, la mejora que Claude escribe en `docs/propuestas.md` de la SF desde otro proyecto (`cola.py propuestas-a-develop`). Solo intercepta Edit y Write: una escritura por terminal no dispara el commit.
- **Decisión:** se acepta. La regla pide escribir la mejora con Edit o Write; si se escribió de otro modo, se lanza después `cola.py --raiz <SF> propuestas-a-develop`. No se prohíbe Edit ni Write en ese archivo.
- **Consecuencias:** el caso normal no deja cambios sin commit en la SF. Una escritura por terminal sí, hasta lanzar la orden.
- **Aplicada en:** sin aplicar: la sustituyó «Sin registro ni mejoras de la SF desde otros proyectos».
