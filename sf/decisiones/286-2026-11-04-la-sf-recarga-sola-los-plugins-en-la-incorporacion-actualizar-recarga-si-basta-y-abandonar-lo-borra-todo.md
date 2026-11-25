# La SF recarga sola los plugins en la incorporación; ACTUALIZAR recarga si basta y Abandonar lo borra todo

Fecha: 2026-11-04. Decidida por el propietario de la Software Factory.

- En la incorporación, cuando la versión instalada de la SF es más nueva que la que corre, el mod lanza /reload-plugins al acabar el turno (incorporacion.py recargar) y la incorporación sigue sola donde estaba. Es una excepción acotada a la incorporación a la regla de que el mod no recarga por su cuenta (decisión 103).
- Tras actualizar la SF sin dependencias nuevas basta con recargar: el botón ACTUALIZAR del panel lo dice así («recarga») y solo pide reiniciar Claude Code si se han instalado dependencias nuevas.
- Abandonar la incorporación lo borra todo, sin guardar las respuestas. Solo se guardan cuando el progreso se borra a medias por otra causa, para ofrecer seguir con lo respondido.

Porqué: incorporando PoseTracker con la 1.8.1, la incorporación se paró para pedir /reload-plugins y no siguió sola; el propietario pidió que la recarga y la continuación fueran automáticas. Abandonar es una decisión expresa del usuario y no debe dejar nada atrás.

Aplicada en: la tarea «Que la incorporación vaya de corrido y sin malentendidos…» (366).
