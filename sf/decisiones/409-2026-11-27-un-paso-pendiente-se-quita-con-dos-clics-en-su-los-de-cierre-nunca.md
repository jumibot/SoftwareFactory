# Un paso pendiente se quita con dos clics en su «×»; los de cierre, nunca

En el panel, cada paso pendiente lleva al final una «×» roja que lo quita con dos clics: el primero la cambia por «¿Quitar? sí» (400). Solo se quita si en ese sitio sigue el mismo paso y sin empezar, porque Claude puede haber cambiado la cola entretanto. El «?» de cada paso se queda.

Los pasos de cierre, «Activar rama para poder probar» y «Cerrar la tarea», no se quitan: no llevan «×» y `cola.py paso quitar` los rechaza (174). Un paso hecho o en curso tampoco se quita.

Recoge lo que sigue valiendo de «Pasos de cierre fijos y E con confirmación para quitar pasos» (117), que queda deprecada.

Porqué: cada paso pendiente llevaba un «−» que lo quitaba con un clic, también los de cierre, que el panel necesita para saber que a la tarea solo le falta cerrarse; un clic suelto bastaba para perder un paso (117).

Aplicada en: `plugins/sf/hooks/panel.tsx` y `cola.ts` (quitar un paso) y sus pruebas; `plugins/sf/tools/cola.py` (`paso quitar`).
