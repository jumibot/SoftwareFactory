# Lo probado sale de Sin probar

Estado: deprecada el 2026-11-27 por «Una tarea en observación sale solo con el OK del propietario, que se pide tarea a tarea» (372); lo demás, por «Las comprobaciones y pruebas hechas se anotan como pasos de su tarea» (288).

- **Origen:** SoftwareFactory, 2026-10-27. Tras revisar 41 peticiones sin probar, Claude pidió confirmación para sacar las comprobadas; el propietario: «sí, sácalas», y después: «Norma todo lo que esté probado se quita de la lista de Sin Probar».
- **Contexto:** la lista crecía porque lo comprobado esperaba una confirmación aparte; con 41 pendientes, ya no servía para ver qué faltaba.
- **Decisión:** lo probado sale de la cola en el momento, sin pedir confirmación: lo que el propietario dice que funciona y lo que Claude comprueba directamente (una captura, una prueba que ejecuta). Lo sustituido por un cambio posterior también sale. Sin probar queda solo con lo que nadie ha comprobado.
- **Aplicada en:** metodología (2) y skill `sf:metodologia`.
