# Por qué de cada regla

El porqué de las reglas que la skill y su referencia, [desarrollo-de-proyectos.md](desarrollo-de-proyectos.md), citan por el número de una decisión de la SF, en su orden. Cada entrada cita la decisión con su título y su número entre paréntesis.

## Qué pertenece a cada proyecto consumidor

- **Las reglas las entrega el mod, también en la propia SF** («En la SF, las reglas y sf:orquestacion las entrega el mod, como en los demás proyectos», 298; «La SF se lleva como los demás proyectos: .sf/proyecto.json, documentos en sf/ y sin excepciones», 299): así la SF se prueba exactamente como la reciben los demás proyectos, y no hay reglas que digan una cosa en los proyectos y otra en la SF. Además, una sesión con la SF apagada no sigue leyendo reglas de la SF en el `CLAUDE.md` sin saber que está apagada.

## Ramas y subagentes

- **Una sola sesión con la SF por proyecto** («Una sola sesión con la SF por proyecto», 193): una segunda sesión en el mismo proyecto recibía los avisos de subagentes de la primera y llegó a poner en curso una tarea y lanzar su subagente. Las dos comparten copia de trabajo, rama activa, cola y worktrees. El latido de cada minuto dice cuál la lleva; unos tres minutos sin latido la dan por cerrada.
- **Apagada, sin panel** («Sin la SF activa no hay panel: se avisa al apagarla porque ya hay latido en el proyecto», 296): un panel en versión apagada confunde, porque parece que la SF sigue. Basta con avisar una vez, al apagarla.
- **Apagada, Claude Code sin más** («Una sesión con la SF apagada, y /sf_forzar_inactiva, dejan Claude Code sin más», 297): una SF a medias, con reglas y bloqueos pero sin tareas ni panel, confunde. Apagada quiere decir apagada: ni el control de un proyecto por sesión, ni la regla del prompt de sistema, ni el contexto de la SF.
- **Apagada, el mod no entrega nada** (298): la sesión apagada es Claude Code sin más, también en la propia SF.
