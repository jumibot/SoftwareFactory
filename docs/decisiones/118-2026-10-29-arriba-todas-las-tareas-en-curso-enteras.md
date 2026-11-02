# Arriba, todas las tareas en curso enteras

- **Origen:** SoftwareFactory, 2026-10-29, al probar la tarea 148. El propietario, ante la 92 recortada con «…»: «podemos usar varias rows si el título de la tarea en curso lo necesita».
- **Contexto:** arriba, la primera tarea en curso iba entera y las demás en una línea, recortadas con «…», para que la cabecera no creciera con varias en curso (decisión de 2026-10-28). El recorte escondía justo lo que se quiere leer de una tarea en curso.
- **Decisión:** todas las tareas en curso de arriba van enteras, en varias líneas si el título lo necesita. Su número sigue subrayado si tienen descripción o rama, y un clic las despliega.
- **Consecuencias:** con varias en curso, la parte de arriba ocupa más; el cuerpo sube con el scroll bajo la cabecera fija.
- **Aplicada en:** plugins/sf/hooks/panel.tsx (tareaArriba) y su prueba.
