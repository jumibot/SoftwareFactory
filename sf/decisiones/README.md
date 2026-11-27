# Decisiones de la Software Factory

Decisiones tomadas por el propietario sobre la SF, con su porqué. Las reglas vigentes que salen de ellas están en la [metodología](../../plugins/sf/skills/metodologia/references/desarrollo-de-proyectos.md) y en la [especificación](../../docs/specs/funcional/software-factory.md). Las ideas aún sin decidir están en [propuestas](../propuestas.md). Cómo se registra una decisión, dónde se aplica y cómo llega a los proyectos se explica en [Mejora continua a la Software Factory](../../docs/mejora-continua-a-la-software-factory.md).

**Cómo se escribe una decisión** (388). Un archivo por decisión en esta carpeta, `NNN-AAAA-MM-DD-titulo.md`: el número de orden total (el siguiente al más alto), la fecha del registro (390) y el título sin tildes ni signos. El título dice la regla decidida, no el tema. Debajo:

- lo decidido, en párrafos cortos o en lista;
- «Opciones:», solo si hubo alternativas reales;
- «Sustituye a…» o «Recoge lo que sigue valiendo de «…» (NNN), que queda deprecada», si cambia otra;
- «Porqué:», el problema y la razón;
- «Aplicada en:», dónde se recoge y lo pendiente.

**Vigentes y deprecadas** (389). Una decisión vigente no lleva estado. Si otra la supera, no se borra: lleva bajo el título «Estado: deprecada el AAAA-MM-DD por «…» (NNN)». El índice las reparte en dos catálogos, [vigentes](vigentes.md) y [deprecadas](deprecadas.md), con esta página como entrada común. Las antiguas no se reescriben.

**Cómo se registra.** Con `cola.py decision "Título" --archivo RUTA [--push]`, que da el número y el nombre, rehace el índice y hace el commit en `develop` sin cambiar la rama activa; `--numero NNN` reescribe una. El índice no se escribe a mano: `python -I -X utf8 plugins/sf/tools/indice_decisiones.py` lo regenera, también al juntar ramas, y con `--html` saca además las páginas con buscador (no se versionan). Lo que hay antes de «Índice» se conserva. Cada proyecto lleva sus decisiones igual, en su `sf/decisiones/`.

## Índice

- [Vigentes](vigentes.md): las decisiones que se aplican.
- [Deprecadas](deprecadas.md): las superadas, con las que las sustituyen.
