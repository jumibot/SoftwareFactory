# Sin develop no hay SF, y las decisiones mezcladas se sacan con enlace

- **Origen:** SoftwareFactory, 2026-11-02. En «Incorporar un proyecto sin cambiarlo: el plugin se adapta al proyecto» (222) quedaban dos casos de la incorporación. El propietario eligió «Sacar las decisiones y dejar un enlace» y, sobre negarse a crear `develop`: «Se para y se indica que no se puede usar SF sin develop. Pedir reconfirmación».
- **Contexto:** «Las decisiones son material de la SF: siempre en sf/decisiones/» (208) manda pasar a `sf/decisiones/` las que tenga el proyecto, pero algunos las tienen mezcladas con otras cosas (SmartColdBox, en `decisiones-y-pendientes.md`). «El manejo del repositorio no se negocia: siempre develop» (205) no decía qué pasa si el desarrollador no quiere `develop`.
- **Decisión:**
  - Un archivo que mezcla decisiones con otras cosas: las decisiones pasan a `sf/decisiones/`, una por archivo, y su sección del archivo original se cambia por un enlace a ellas; el resto (pendientes y demás) se queda donde está.
  - Si el desarrollador no quiere crear `develop`, Claude le explica que la SF no se puede usar sin `develop` y le pide que lo reconfirme con un menú. Si lo reconfirma, la incorporación se para sin cambiar nada.
- **Consecuencias:** ninguna decisión queda duplicada. Nunca hay un proyecto a medio incorporar sin `develop`.
- **Aplicada en:** pendiente; en la 222 (`sf:incorporar_proyecto_a_sf`).
