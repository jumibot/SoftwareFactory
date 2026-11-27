# Pasos de cierre fijos y E con confirmación para quitar pasos

Estado: deprecada el 2026-11-27 por «Un paso pendiente se quita con dos clics en su «×»; los de cierre, nunca» (409); lo demás, por «Las órdenes de una tarea, como etiquetas en el menú de la tarea desplegada» (400), «El paso de prueba es «Activar rama para poder probar»» (172) y «Los pasos de cierre, desde que la tarea entra en curso» (174).

- **Origen:** SoftwareFactory, 2026-10-29, tarea 138. El propietario decide cómo se quitan los pasos desde el panel.
- **Contexto:** cada paso pendiente llevaba un «−» que lo quitaba con un clic, también «Probar la tarea» y «Cerrar la tarea», que la C necesita para saber que la tarea solo espera cerrarse. Un clic suelto bastaba para perder un paso.
- **Decisión:** «Probar la tarea» y «Cerrar la tarea» no se eliminan: no llevan botón para quitarlos y la orden que quita pasos los rechaza. Los demás pasos pendientes se quitan con una E en lugar del «−», con la letra y el color de la E de las tareas y dos clics, como la D: el primero la cambia por «E eliminar» y el segundo lo quita; a los 5 s, o con un clic en otro botón del panel, vuelve a ser la E. El «?» se queda.
- **Consecuencias:** precisa «Pasos de una tarea» y «Pasos de cierre: probar y cerrar la tarea»; la E de los pasos comparte el mecanismo de confirmación de la E, la D, la C y la R.
- **Aplicada en:** plugins/sf/hooks/panel.tsx, plugins/sf/hooks/cola.ts y sus pruebas.
