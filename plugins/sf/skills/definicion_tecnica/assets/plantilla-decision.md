# {La regla, en una frase: lo decidido, no el tema}

<!-- Plantilla de una decisión de la SF, en su formato «regla y porqué». Nació de MADR 4.0.0 (versión mínima) y ya no sigue sus secciones: el título dice la regla, el porqué va aparte y no hay «Estado», «Fecha» ni «Decide» mientras está vigente. Es un archivo de sf/decisiones/, NNN-AAAA-MM-DD-titulo.md (número de orden total, fecha del registro y título sin tildes ni signos); se registra con cola.py decision "Título" --archivo RUTA (tools/ del plugin), que da el nombre, rehace el índice (README.md, vigentes.md y deprecadas.md) y hace el commit en develop sin cambiar la rama activa. Las líneas entre llaves se cambian o se quitan. -->

{Solo si está deprecada, la primera línea bajo el título; mientras está vigente, no lleva estado:}
Estado: deprecada el {AAAA-MM-DD} por «{Título de la que la sustituye}» ({NNN}); lo demás, por «{Título}» ({NNN}).

{Lo decidido, en párrafos cortos o en lista: la regla que se aplica, con los nombres de las piezas.}

{Solo si hubo alternativas reales:}
Opciones: {A}, {B}. Se elige {A} porque {…}; {B} se descarta porque {…}.

{Solo si cambia otra decisión:}
Sustituye a «{Título}» ({NNN}), que queda deprecada.
{o, si de la otra sigue valiendo algo:}
Recoge lo que sigue valiendo de «{Título}» ({NNN}), que queda deprecada.

Porqué: {el problema y la razón, con las palabras del propietario cuando las hay, y de dónde viene (la tarea, el informe)}.

Aplicada en: {piezas, skills y documentos que la recogen}; pendiente: {lo que falta}.
