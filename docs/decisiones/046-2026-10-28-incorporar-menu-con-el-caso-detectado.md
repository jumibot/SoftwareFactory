# Incorporar: menú con el caso detectado

- **Origen:** SoftwareFactory, 2026-10-28. El propietario: «entiendo que la nueva skill solicita cual de las 4 con un menú?». A la propuesta de deducir el caso y presentarlo en un menú, con «Solo diagnosticar» como alternativa: «sí, cámbialo así».
- **Decisión:** la skill `incorporar_proyecto_a_sf` deduce el caso y lo presenta en un menú antes de tocar nada: primero el caso detectado, recomendado y con lo que lo delata, y después «Solo diagnosticar». Si la petición ya nombra el caso, no pregunta.
- **Aplicada en:** skill `sf:incorporar_proyecto_a_sf`; plugin `sf` 0.29.1.
