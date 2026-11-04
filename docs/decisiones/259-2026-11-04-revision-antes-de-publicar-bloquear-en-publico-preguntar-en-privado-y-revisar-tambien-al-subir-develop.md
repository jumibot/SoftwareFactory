# Revisión antes de publicar: bloquear en público, preguntar en privado, y revisar también al subir develop

La revisión de lo que se publica (secretos, datos personales, rutas de la máquina, documentos internos) actúa según el repositorio:
- Repositorio público: RELEASE no publica si encuentra algo nuevo; se corrige o se apunta como permitido en .sf/publicable.txt y se vuelve a pulsar. La misma revisión corre al subir develop al cerrar cada tarea: si encuentra algo, no sube y lo dice.
- Repositorio privado: RELEASE enseña lo encontrado y pregunta si seguir; al cerrar una tarea no se revisa nada.
- Lo sospechoso que ya está subido (en develop del remoto, aunque no en un tag), como las 19 rutas de otros proyectos que hay hoy en develop de la SF, no bloquea: se enseña todo y se pide permiso para continuar.

Por qué: en un repositorio público lo que sale no tiene vuelta atrás, y develop se sube al cerrar cada tarea, antes de RELEASE; en uno privado basta con avisar; y bloquear por algo que ya está fuera no protege nada (concreta la 252, tarea 332).
