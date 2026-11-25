# Las tareas de investigar no tienen rama

Las tareas de análisis o investigación (tipo investigar) no tienen rama: no cambian el repositorio, sino que devuelven un análisis, y lo que proponen sale como tareas nuevas. Su subagente trabaja leyendo, sin worktree ni rama auxiliar, y se cierran sin squash, sacándolas de la cola.

Por qué: una rama vacía no aporta nada y estorba al cerrar (al cerrar la 325, el squash de una rama sin cambios falló).
