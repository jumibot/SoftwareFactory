# Decisiones de la Software Factory

Decisiones tomadas por el propietario sobre la SF, con su porqué. Las reglas vigentes que salen de ellas están en la [metodología](../../plugins/sf/skills/metodologia/references/desarrollo-de-proyectos.md) y en la [especificación](../specs/funcional/software-factory.md). Las ideas aún sin decidir están en [propuestas](../propuestas.md). Cómo se registra una decisión, dónde se aplica y cómo llega a los proyectos se explica en [Mejora continua a la Software Factory](../mejora-continua-a-la-software-factory.md).

**Cómo se registra una decisión.** Un archivo por decisión en esta carpeta, `NNN-AAAA-MM-DD-titulo.md`: el número de orden total (el siguiente al más alto), la fecha del origen y el título sin tildes ni signos. Empieza por `# Título` y lleva:

- **Origen:** proyecto, fecha y palabras del propietario cuando las hay.
- **Contexto:** el problema.
- **Opciones:** las que se valoraron, si las hubo.
- **Decisión:** lo decidido y por qué.
- **Consecuencias:** lo que cambia y lo que queda pendiente.
- **Aplicada en:** los documentos, skills o piezas que la recogen.

Si una decisión cambia otra anterior, la nueva lo dice («Sustituye a…») y la antigua se marca como sustituida, sin borrarla, con una línea bajo el título: «**Sustituida** el AAAA-MM-DD por «…»» (o **Sustituida en parte**). Cada proyecto lleva sus decisiones igual, en su `docs/decisiones/` (metodología, 6).

Una decisión se registra con `cola.py decision "Título" --archivo RUTA [--push]`, que da el número y el nombre, rehace este índice y hace el commit en `develop` sin cambiar la rama activa. Este índice no se escribe a mano: `python -I -X utf8 plugins/sf/tools/indice_decisiones.py docs/decisiones` lo regenera también al juntar ramas. Lo que hay antes de «Índice» se conserva.

## Índice

| Nº | Fecha | Decisión |
| --- | --- | --- |
| 296 | 2026-11-05 | [Sin la SF activa no hay panel: se avisa al apagarla porque ya hay latido en el proyecto](296-2026-11-05-sin-la-sf-activa-no-hay-panel-se-avisa-al-apagarla-porque-ya-hay-latido-en-el-proyecto.md) |
| 295 | 2026-11-05 | [La sesión apagada avisa y propone /sf_forzar_activa cuando la activa deja de latir, y avisa de que se trabaja sin la SF](295-2026-11-05-la-sesion-apagada-avisa-y-propone-sf-forzar-activa-cuando-la-activa-deja-de-latir-y-avisa-de-que-se-trabaja-sin-la-sf.md) |
| 294 | 2026-11-05 | [Manda el proyecto salvo en cómo se lleva el repositorio: ramas, commits, push, cola y publicación](294-2026-11-05-manda-el-proyecto-salvo-en-como-se-lleva-el-repositorio-ramas-commits-push-cola-y-publicacion.md) |
| 293 | 2026-11-05 | [Un documento de arranque de Claude en la SF, al día con lo que hace falta para seguir desarrollándola](293-2026-11-05-un-documento-de-arranque-de-claude-en-la-sf-al-dia-con-lo-que-hace-falta-para-seguir-desarrollandola.md) |
| 292 | 2026-11-05 | [En la SF, la memoria de Claude no lleva nada útil para los usuarios del plugin, y cambiarla pide autorización del propietario](292-2026-11-05-en-la-sf-la-memoria-de-claude-no-lleva-nada-que-viaje-en-el-plugin-y-cambiarla-pide-autorizacion-del-propietario.md) |
| 291 | 2026-11-05 | [El CLAUDE.md de la SF no lleva nada útil para los usuarios del plugin, y cambiarlo pide autorización del propietario](291-2026-11-05-el-claude-md-de-la-sf-no-lleva-nada-que-viaje-en-el-plugin-y-cambiarlo-pide-autorizacion-del-propietario.md) |
| 290 | 2026-11-05 | [Botones del panel en la app de escritorio con el fondo de su color](290-2026-11-05-botones-del-panel-en-la-app-de-escritorio-con-el-fondo-de-su-color.md) |
| 289 | 2026-11-05 | [Emojis de estado fijos en las respuestas del principal, coherentes con el panel](289-2026-11-05-emojis-de-estado-fijos-en-las-respuestas-del-principal-coherentes-con-el-panel.md) |
| 288 | 2026-11-05 | [Las comprobaciones y pruebas hechas se anotan como pasos de su tarea](288-2026-11-05-las-comprobaciones-y-pruebas-hechas-se-anotan-como-pasos-de-su-tarea.md) |
| 287 | 2026-11-05 | [El principal dice en qué tarea está concentrado el propietario, con «FOCUS: <título corto> (T NN)»](287-2026-11-05-el-principal-dice-en-que-tarea-esta-concentrado-el-propietario-con-focus-titulo-corto-t-nn.md) |
| 286 | 2026-11-04 | [La SF recarga sola los plugins en la incorporación; ACTUALIZAR recarga si basta y Abandonar lo borra todo](286-2026-11-04-la-sf-recarga-sola-los-plugins-en-la-incorporacion-actualizar-recarga-si-basta-y-abandonar-lo-borra-todo.md) |
| 285 | 2026-11-04 | [La SF gestiona el repositorio a su manera: la incorporación no lo deja a elección](285-2026-11-04-la-sf-gestiona-el-repositorio-a-su-manera-la-incorporacion-no-lo-deja-a-eleccion.md) |
| 284 | 2026-11-04 | [Sin subagente de la cola: órdenes compuestas, la cola en el contexto y contestar primero](284-2026-11-04-sin-subagente-de-la-cola-ordenes-compuestas-la-cola-en-el-contexto-y-contestar-primero.md) |
| 283 | 2026-11-04 | [Poner en curso y recoger una tarea con una sola orden](283-2026-11-04-poner-en-curso-y-recoger-una-tarea-con-una-sola-orden.md) |
| 282 | 2026-11-04 | [Agentes del plugin por familia de tarea, solo si la especialización aporta](282-2026-11-04-agentes-del-plugin-uno-por-familia-de-tarea.md) |
| 281 | 2026-11-04 | [Preguntas legibles: pregunta corta, el detalle antes en el chat en palabras llanas y opciones que dicen qué hacen](281-2026-11-04-preguntas-legibles-pregunta-corta-el-detalle-antes-en-el-chat-en-palabras-llanas-y-opciones-que-dicen-que-hacen.md) |
| 280 | 2026-11-04 | [Migración al repositorio público: develop público, ramas de tarea locales y _respaldo/ públicos](280-2026-11-04-migracion-al-repositorio-publico-develop-publico-ramas-de-tarea-locales-y-respaldo-publicos.md) |
| 279 | 2026-11-04 | [Las skills internas de la SF no salen en el menú al escribir /sf](279-2026-11-04-las-skills-internas-de-la-sf-no-salen-en-el-menu-al-escribir-sf.md) |
| 278 | 2026-11-04 | [Una deliberativa solo escribe su documento, sin rama; lo demás va a tareas propias con rama](278-2026-11-04-una-deliberativa-solo-escribe-su-documento-sin-rama-lo-demas-va-a-tareas-propias-con-rama.md) |
| 277 | 2026-11-04 | [La revisión del sprint se guarda como texto breve en el sprint, y la cabecera del sprint en el panel es desplegable](277-2026-11-04-la-revision-del-sprint-se-guarda-como-texto-breve-en-el-sprint-y-la-cabecera-del-sprint-en-el-panel-es-desplegable.md) |
| 276 | 2026-11-04 | [Con kanban, el sprint vive en el kanban como una tarjeta con su lista de tareas](276-2026-11-04-con-kanban-el-sprint-vive-en-el-kanban-como-una-tarjeta-con-su-lista-de-tareas.md) |
| 275 | 2026-11-04 | [Los sprints también en proyectos sin metodología, con interruptor](275-2026-11-04-los-sprints-tambien-en-proyectos-sin-metodologia-con-interruptor.md) |
| 274 | 2026-11-04 | [Los candidatos del sprint los propone Claude y el developer puede aportar otros](274-2026-11-04-los-candidatos-del-sprint-los-propone-claude-y-el-developer-puede-aportar-otros.md) |
| 273 | 2026-11-04 | [En un sprint, los paréntesis fuera de tema solo sirven para anotar tareas o ideas nuevas](273-2026-11-04-en-un-sprint-los-parentesis-fuera-de-tema-solo-sirven-para-anotar-tareas-o-ideas-nuevas.md) |
| 272 | 2026-11-04 | [La daily se hace aunque no haya sprint y sirve para fijarlo](272-2026-11-04-la-daily-se-hace-aunque-no-haya-sprint-y-sirve-para-fijarlo.md) |
| 271 | 2026-11-04 | [Sin sprint definido, la SF propone crear uno](271-2026-11-04-sin-sprint-definido-la-sf-propone-crear-uno.md) |
| 270 | 2026-11-04 | [El documento de una deliberación solo recoge decisiones de su tema](270-2026-11-04-el-documento-de-una-deliberacion-solo-recoge-decisiones-de-su-tema.md) |
| 269 | 2026-11-04 | [Sprints: TURBO solo dentro del sprint, daily breve en el chat y solo /sf_daily](269-2026-11-04-sprints-turbo-solo-dentro-del-sprint-daily-breve-en-el-chat-y-solo-sf-daily.md) |
| 268 | 2026-11-04 | [El informe de una deliberativa basta para retomarla y ponerla en práctica](268-2026-11-04-el-informe-de-una-deliberativa-basta-para-retomarla-y-ponerla-en-practica.md) |
| 267 | 2026-11-04 | [Una deliberativa no se cierra sin su documento validado](267-2026-11-04-una-deliberativa-no-se-cierra-sin-su-documento-validado.md) |
| 266 | 2026-11-04 | [Sprints: en la cola y solo el actual a la vista, panel, observación y tareas fuera del objetivo](266-2026-11-04-sprints-en-la-cola-y-solo-el-actual-a-la-vista-panel-observacion-y-tareas-fuera-del-objetivo.md) |
| 265 | 2026-11-04 | [Ciclo del sprint: cierre, daily, entrada de tareas y cambio de objetivo](265-2026-11-04-ciclo-del-sprint-cierre-daily-entrada-de-tareas-y-cambio-de-objetivo.md) |
| 264 | 2026-11-04 | [La daily se pide con /sf_daily y es una conversación](264-2026-11-04-la-daily-se-pide-con-sf-daily-y-es-una-conversacion.md) |
| 263 | 2026-11-04 | [Una deliberación abre su tarea en curso al empezar y se cierra con su documento validado](263-2026-11-04-una-deliberacion-abre-su-tarea-en-curso-al-empezar-y-se-cierra-creando-las-tareas-que-salen.md) |
| 262 | 2026-11-04 | [La daily se puede pedir en cualquier momento](262-2026-11-04-la-daily-se-puede-pedir-en-cualquier-momento.md) |
| 261 | 2026-11-04 | [El resumen al abrir Claude Code es la daily del sprint](261-2026-11-04-el-resumen-al-abrir-claude-code-es-la-daily-del-sprint.md) |
| 260 | 2026-11-04 | [Un devslice puede tener muchos sprints](260-2026-11-04-un-devslice-puede-tener-muchos-sprints.md) |
| 259 | 2026-11-04 | [Revisión antes de publicar: bloquear en público, preguntar en privado, y revisar también al subir develop](259-2026-11-04-revision-antes-de-publicar-bloquear-en-publico-preguntar-en-privado-y-revisar-tambien-al-subir-develop.md) |
| 258 | 2026-11-04 | [Esc pone en pausa la incorporación, con Continuar y Abandonar en el panel](258-2026-11-04-esc-pone-en-pausa-la-incorporacion-con-continuar-y-abandonar-en-el-panel.md) |
| 257 | 2026-11-04 | [La orden fija del plugin se llama /sf:panel](257-2026-11-04-la-orden-fija-del-plugin-se-llama-sf-panel.md) |
| 256 | 2026-11-04 | [Las tareas de investigar no tienen rama](256-2026-11-04-las-tareas-de-investigar-no-tienen-rama.md) |
| 255 | 2026-11-04 | [Logo «/SF»: barra estrecha y empinada en morado claro](255-2026-11-04-logo-sf-barra-estrecha-y-empinada-en-morado-claro.md) |
| 254 | 2026-11-04 | [En la app, /sf disponible antes del primer mensaje y solo órdenes al escribir /sf](254-2026-11-04-en-la-app-sf-disponible-antes-del-primer-mensaje-y-solo-ordenes-al-escribir-sf.md) |
| 253 | 2026-11-04 | [Botones del panel en la app de escritorio, con contorno de color](253-2026-11-04-botones-del-panel-en-la-app-de-escritorio-con-contorno-de-color.md) (sustituida) |
| 252 | 2026-11-03 | [La SF se trabaja en el repositorio público, con revisión antes de publicar](252-2026-11-03-la-sf-se-trabaja-en-el-repositorio-publico-con-revision-antes-de-publicar.md) |
| 251 | 2026-11-03 | [El título de una tarea dice el resultado buscado, sin ambigüedad](251-2026-11-03-el-titulo-de-una-tarea-dice-el-resultado-buscado-sin-ambiguedad.md) |
| 250 | 2026-11-03 | [No interrumpir mientras se prueba o se está en otra tarea](250-2026-11-03-no-interrumpir-mientras-se-prueba-o-se-esta-en-otra-tarea.md) |
| 249 | 2026-11-03 | [El logo de bienvenida va del color de la sesión](249-2026-11-03-el-logo-de-bienvenida-va-del-color-de-la-sesion.md) |
| 248 | 2026-11-03 | [La pastilla de incorporar es un botón](248-2026-11-03-la-pastilla-de-incorporar-es-un-boton.md) |
| 247 | 2026-11-03 | [Lo útil para terceros viaja en el plugin, no en la memoria ni en CLAUDE.md](247-2026-11-03-lo-util-para-terceros-viaja-en-el-plugin.md) |
| 246 | 2026-11-02 | [Si se dice que no a incorporar, se puede no volver a preguntar](246-2026-11-02-si-se-dice-que-no-a-incorporar-se-puede-no-volver-a-preguntar.md) |
| 245 | 2026-11-02 | [Bienvenida del panel publicada y pantalla completa al incorporar](245-2026-11-02-bienvenida-del-panel-publicada-y-pantalla-completa-al-incorporar.md) |
| 244 | 2026-11-02 | [La instalación la comprueba y la diagnostica Claude](244-2026-11-02-la-instalacion-la-comprueba-y-la-diagnostica-claude.md) |
| 243 | 2026-11-02 | [En una carpeta sin SF, Claude ofrece incorporarla](243-2026-11-02-en-una-carpeta-sin-sf-claude-ofrece-incorporarla.md) |
| 242 | 2026-11-02 | [Tras incorporar, el mod entrega las reglas sin reiniciar](242-2026-11-02-tras-incorporar-el-mod-entrega-las-reglas-sin-reiniciar.md) |
| 241 | 2026-11-02 | [La SF se publica en un repositorio nuevo sin historia, con licencia MIT](241-2026-11-02-la-sf-se-publica-en-un-repositorio-nuevo-sin-historia.md) |
| 240 | 2026-11-02 | [Las tareas de código no llevan pasos de documentación](240-2026-11-02-las-tareas-de-codigo-no-llevan-pasos-de-documentacion.md) |
| 239 | 2026-11-02 | [Así se prepara la prueba del colega](239-2026-11-02-asi-se-prepara-la-prueba-del-colega.md) |
| 238 | 2026-11-02 | [La firma del commit de cierre es configurable; sin configurar, sin línea](238-2026-11-02-la-firma-del-commit-de-cierre-es-configurable.md) |
| 237 | 2026-11-02 | [Los textos fijos de la SF siguen en español](237-2026-11-02-los-textos-fijos-de-la-sf-siguen-en-espanol.md) |
| 236 | 2026-11-02 | [La orden de Python sale del intérprete que se detecta, no de `python` fijo](236-2026-11-02-la-orden-de-python-sale-del-interprete-detectado.md) |
| 235 | 2026-11-02 | [La SF guía el desarrollo: observa y sugiere cómo avanzar](235-2026-11-02-la-sf-guia-observa-y-sugiere-como-avanzar.md) |
| 234 | 2026-11-02 | [Si main solo está en el remoto, se crea la local sin preguntar](234-2026-11-02-main-solo-en-el-remoto-se-crea-local-sin-preguntar.md) |
| 233 | 2026-11-02 | [El título del commit en formato conventional sale del tipo de tarea](233-2026-11-02-el-titulo-conventional-sale-del-tipo-de-tarea.md) |
| 232 | 2026-11-02 | [Una skill general de diseño de documentos, y skills de contenido encima](232-2026-11-02-una-skill-general-de-diseno-de-documentos.md) |
| 231 | 2026-11-02 | [Una skill propia para los informes de las deliberativas, ligera sobre el diseño común](231-2026-11-02-skill-propia-para-los-informes-de-las-deliberativas.md) |
| 230 | 2026-11-02 | [Sin remoto en GitHub no hay SF: se valida al incorporar y, si falta, se crea](230-2026-11-02-sin-remoto-en-github-no-hay-sf.md) |
| 229 | 2026-11-02 | [Sin mapa de documentos: o se sigue la estructura de la SF, o no se mapea](229-2026-11-02-sin-mapa-de-documentos.md) |
| 228 | 2026-11-02 | [La configuración se cambia pidiéndoselo a Claude, con menús](228-2026-11-02-la-configuracion-se-cambia-pidiendoselo-a-claude-con-menus.md) |
| 227 | 2026-11-02 | [Todo proyecto.json es configuración: plana, y bloques solo para lo afín](227-2026-11-02-todo-proyecto-json-es-configuracion-plana-y-bloques-solo-para-lo-afin.md) |
| 226 | 2026-11-02 | [La versión forma parte del manejo del repositorio](226-2026-11-02-la-version-forma-parte-del-manejo-del-repositorio.md) |
| 225 | 2026-11-02 | [Los commits los lleva siempre Claude](225-2026-11-02-los-commits-los-lleva-siempre-claude.md) |
| 224 | 2026-11-02 | [El kanban se elige, y por defecto ninguno](224-2026-11-02-el-kanban-se-elige-y-por-defecto-ninguno.md) |
| 223 | 2026-11-02 | [Siete tipos de tarea en tres familias, para agentes especializados](223-2026-11-02-siete-tipos-de-tarea-en-tres-familias-para-agentes-especializados.md) |
| 222 | 2026-11-02 | [Las deliberativas se cierran con «Finalizar deliberación»](222-2026-11-02-las-deliberativas-se-cierran-con-finalizar-deliberacion.md) |
| 221 | 2026-11-02 | [En una deliberativa, lo que es de otra tarea se propone separar](221-2026-11-02-en-una-deliberativa-lo-que-es-de-otra-tarea-se-propone-separar.md) |
| 220 | 2026-11-02 | [Cada cambio de un .md regenera su HTML](220-2026-11-02-cada-cambio-de-un-md-regenera-su-html.md) |
| 219 | 2026-11-02 | [El tipo de tarea decide cómo se maneja el repositorio](219-2026-11-02-el-tipo-de-tarea-decide-como-se-maneja-el-repositorio.md) |
| 218 | 2026-11-02 | [Una tarea deliberativa da un informe y las tareas que salgan](218-2026-11-02-una-tarea-deliberativa-da-un-informe-y-las-tareas-que-salgan.md) |
| 217 | 2026-11-02 | [Antes de sustituir un documento, se respalda en _respaldo/](217-2026-11-02-antes-de-sustituir-un-documento-se-respalda-en-respaldo.md) |
| 216 | 2026-11-02 | [Los documentos nuevos van a develop en cada vuelta y se ofrecen en el navegador](216-2026-11-02-los-documentos-nuevos-van-a-develop-en-cada-vuelta-y-se-ofrecen-en-el-navegador.md) |
| 215 | 2026-11-02 | [«En observación», sin alias ni rastros](215-2026-11-02-en-observacion-sin-alias-ni-rastros.md) |
| 214 | 2026-11-02 | [Sin develop no hay SF, y las decisiones mezcladas se sacan con enlace](214-2026-11-02-sin-develop-no-hay-sf-y-las-decisiones-mezcladas-se-sacan-con-enlace.md) |
| 213 | 2026-11-02 | [Si el proyecto tiene master, se pregunta si hace de main](213-2026-11-02-si-el-proyecto-tiene-master-se-pregunta-si-hace-de-main.md) |
| 212 | 2026-11-02 | [Testing pasa a llamarse «En observación»](212-2026-11-02-testing-pasa-a-llamarse-en-observacion.md) |
| 211 | 2026-11-02 | [Lo que falta por concretar va como pasos de la tarea](211-2026-11-02-lo-que-falta-por-concretar-va-como-pasos-de-la-tarea.md) |
| 210 | 2026-11-02 | [Un proyecto solo anota propuestas suyas](210-2026-11-02-un-proyecto-solo-anota-propuestas-suyas.md) |
| 209 | 2026-11-02 | [Incorporar un proyecto es una operación sin tarea, guiada por menús](209-2026-11-02-incorporar-un-proyecto-es-una-operacion-sin-tarea-guiada-por-menus.md) |
| 208 | 2026-11-02 | [Las decisiones son material de la SF: siempre en sf/decisiones/](208-2026-11-02-las-decisiones-son-material-de-la-sf-siempre-en-sf-decisiones.md) |
| 207 | 2026-11-02 | [El número de la tarea en el commit, según el formato del proyecto](207-2026-11-02-el-numero-de-la-tarea-en-el-commit-segun-el-formato-del-proyecto.md) |
| 206 | 2026-11-02 | [Claude escribe en el idioma del proyecto y del desarrollador](206-2026-11-02-claude-escribe-en-el-idioma-del-proyecto-y-del-desarrollador.md) |
| 205 | 2026-11-02 | [El manejo del repositorio no se negocia: siempre develop](205-2026-11-02-el-manejo-del-repositorio-no-se-negocia-siempre-develop.md) |
| 204 | 2026-11-02 | [Los estados de las tareas se nombran con el lenguaje de la SF](204-2026-11-02-los-estados-de-las-tareas-se-nombran-con-el-lenguaje-de-la-sf.md) |
| 203 | 2026-11-02 | [Los documentos de la SF van en la carpeta sf/](203-2026-11-02-los-documentos-de-la-sf-van-en-la-carpeta-sf.md) |
| 202 | 2026-11-02 | [La SF fija el mecanismo y se adapta a las convenciones del proyecto](202-2026-11-02-la-sf-fija-el-mecanismo-y-se-adapta-a-las-convenciones-del-proyecto.md) |
| 201 | 2026-11-02 | [Incorporar un proyecto no mueve ni renombra nada](201-2026-11-02-incorporar-un-proyecto-no-mueve-ni-renombra-nada.md) |
| 200 | 2026-11-01 | [Cerrar se niega si el subagente tiene trabajo sin traer](200-2026-11-01-cerrar-se-niega-si-el-subagente-tiene-trabajo-sin-traer.md) |
| 199 | 2026-11-01 | [Poner un proyecto al día con la SF, sin tarea](199-2026-11-01-poner-un-proyecto-al-dia-con-la-sf-sin-tarea.md) |
| 198 | 2026-11-01 | [Los comandos de la SF empiezan por sf_](198-2026-11-01-los-comandos-de-la-sf-empiezan-por-sf.md) |
| 197 | 2026-11-01 | [Las propuestas, en el bloque TAREAS; sin bloque PROYECTO](197-2026-11-01-las-propuestas-en-el-bloque-tareas-sin-bloque-proyecto.md) |
| 196 | 2026-11-01 | [La incorporación crea docs/propuestas.md; el índice de decisiones sale del panel](196-2026-11-01-la-incorporacion-crea-docs-propuestas-md.md) |
| 195 | 2026-11-01 | [Fuera la sección Documentos del panel](195-2026-11-01-fuera-la-seccion-documentos-del-panel.md) |
| 194 | 2026-11-01 | [Sin registro ni mejoras de la SF desde otros proyectos](194-2026-11-01-sin-registro-ni-mejoras-de-la-sf-desde-otros-proyectos.md) |
| 193 | 2026-11-01 | [Una sola sesión con la SF por proyecto](193-2026-11-01-una-sola-sesion-con-la-sf-por-proyecto.md) |
| 192 | 2026-11-01 | [La mejora desde otro proyecto se escribe con Edit o Write](192-2026-11-01-la-mejora-desde-otro-proyecto-se-escribe-con-edit-o-write.md) (sustituida) |
| 191 | 2026-11-01 | [Activar rama integra develop, avisa a Claude si choca y adelanta la rama del subagente](191-2026-11-01-activar-rama-integra-develop-y-avisa-a-claude-si-choca.md) |
| 190 | 2026-11-01 | [La orden fija de cola.py pasa por el lanzador real, también con CLAUDE_CONFIG_DIR](190-2026-11-01-la-orden-fija-de-cola-py-pasa-por-el-lanzador-real.md) |
| 189 | 2026-11-01 | [Descartar borra también la rama del subagente](189-2026-11-01-descartar-borra-tambien-la-rama-del-subagente.md) |
| 188 | 2026-11-01 | [Cerrar y pasar a Testing desde el panel también las tareas en curso sin rama](188-2026-11-01-cerrar-desde-el-panel-tambien-sin-rama.md) |
| 187 | 2026-11-01 | [El panel entrega las reglas y la orquestación en los proyectos](187-2026-11-01-el-panel-entrega-las-reglas-y-la-orquestacion-en-los-proyectos.md) |
| 186 | 2026-11-01 | [Las tareas para Claude, con título legible y descripción para el propietario](186-2026-11-01-las-tareas-para-claude-con-titulo-legible-y-descripcion-para-el-propietario.md) |
| 185 | 2026-11-01 | [Claude lanza cola.py con un comando fijo, la misma copia que el panel](185-2026-11-01-claude-lanza-cola-py-con-un-comando-fijo.md) |
| 184 | 2026-11-01 | [Ayudas de prueba: tras activar la rama y no obligatorias para cerrar](184-2026-11-01-ayudas-de-prueba-tras-activar-la-rama-y-no-obligatorias.md) |
| 183 | 2026-11-01 | [El generador de documentos no elige por el autor](183-2026-11-01-el-generador-de-documentos-no-elige-por-el-autor.md) |
| 182 | 2026-11-01 | [Etiquetas «A Testing» en las tareas en curso y «Cerrar» en las de Testing](182-2026-11-01-etiquetas-a-testing-en-curso-y-cerrar-en-testing.md) |
| 181 | 2026-11-01 | [El principal planifica los pasos sin pedir aprobación](181-2026-11-01-el-principal-planifica-los-pasos-sin-pedir-aprobacion.md) |
| 180 | 2026-11-01 | [Los pasos de una tarea se deciden en modo plan](180-2026-11-01-los-pasos-de-una-tarea-se-deciden-en-modo-plan.md) |
| 179 | 2026-11-01 | [En Testing, la prueba y el OK de Claude, cada uno en su línea](179-2026-11-01-en-testing-la-prueba-y-el-ok-de-claude-cada-uno-en-su-linea.md) |
| 178 | 2026-11-01 | [Una tarea que espera y no puede volver a la cola lleva un paso «Esperar a …»](178-2026-11-01-una-tarea-que-espera-y-no-puede-volver-a-la-cola-lleva-un-paso-de-espera.md) |
| 177 | 2026-11-01 | [ACTUALIZAR y REFRESCAR: dos botones para dos casos](177-2026-11-01-actualizar-y-refrescar-dos-botones-para-dos-casos.md) |
| 176 | 2026-11-01 | [Todas las skills externas actuales, como dependencias](176-2026-11-01-todas-las-skills-externas-actuales-como-dependencias.md) |
| 175 | 2026-11-01 | [Skills externas: tal cual, como dependencias; adaptadas, como propias](175-2026-11-01-skills-externas-tal-cual-como-dependencias-adaptadas-como-propias.md) |
| 174 | 2026-11-01 | [Los pasos de cierre, desde que la tarea entra en curso](174-2026-11-01-los-pasos-de-cierre-desde-que-la-tarea-entra-en-curso.md) |
| 173 | 2026-11-01 | [Toda tarea se despliega y lleva su etiqueta «?»](173-2026-11-01-toda-tarea-se-despliega-y-lleva-su-etiqueta-de-explicar.md) |
| 172 | 2026-11-01 | [El paso de prueba es «Activar rama para poder probar»](172-2026-11-01-el-paso-de-prueba-es-activar-rama-para-poder-probar.md) |
| 171 | 2026-11-01 | [Las automatizaciones del plugin, configurables y avisando antes que bloquear](171-2026-11-01-las-automatizaciones-del-plugin-configurables-y-avisando-antes-que-bloquear.md) |
| 170 | 2026-11-01 | [Una tarea en curso con rama no vuelve a la cola](170-2026-11-01-una-tarea-en-curso-con-rama-no-vuelve-a-la-cola.md) |
| 169 | 2026-11-01 | [cola.py recoge el subagente al dejar la tarea sin él](169-2026-11-01-cola-py-recoge-el-subagente-al-dejar-la-tarea-sin-el.md) |
| 168 | 2026-11-01 | [Las órdenes de cada tarea, en un menú de etiquetas](168-2026-11-01-las-ordenes-de-cada-tarea-en-un-menu-de-etiquetas.md) |
| 167 | 2026-11-01 | [Lo que pinta la SF y lo global no son del proyecto](167-2026-11-01-lo-que-pinta-la-sf-y-lo-global-no-son-del-proyecto.md) |
| 166 | 2026-11-01 | [La línea gris del proyecto sale del panel](166-2026-11-01-la-linea-gris-del-proyecto-sale-del-panel.md) |
| 165 | 2026-11-01 | [Un /clear empieza una sesión nueva en el panel](165-2026-11-01-un-clear-empieza-una-sesion-nueva-en-el-panel.md) |
| 164 | 2026-11-01 | [Los avisos del panel, en la cabecera con fondo blanco](164-2026-11-01-los-avisos-del-panel-en-la-cabecera-con-fondo-blanco.md) |
| 163 | 2026-11-01 | [El índice de decisiones en html se genera al abrirlo](163-2026-11-01-el-indice-de-decisiones-en-html-se-genera-al-abrirlo.md) |
| 162 | 2026-11-01 | [La marca del subagente, verde trabajando y roja en espera](162-2026-11-01-la-rueda-del-subagente-verde-trabajando-y-roja-en-espera.md) |
| 161 | 2026-10-31 | [Un solo aviso de proyecto atrasado en el panel](161-2026-10-31-un-solo-aviso-de-proyecto-atrasado-en-el-panel.md) |
| 160 | 2026-10-31 | [TURBO pone en curso las tareas que no necesitan al propietario](160-2026-10-31-turbo-pone-en-curso-las-tareas-que-no-necesitan-al-propietario.md) |
| 159 | 2026-10-31 | [Números de tarea en tres columnas, apartados con 0 y rojo solo para las reabiertas](159-2026-10-31-numeros-de-tarea-en-tres-columnas-apartados-con-0-y-rojo-solo-para-reabiertas.md) |
| 158 | 2026-10-31 | [No dejar anotado lo que no aporta](158-2026-10-31-no-dejar-anotado-lo-que-no-aporta.md) |
| 157 | 2026-10-31 | [Cerrar antes que abrir](157-2026-10-31-cerrar-antes-que-abrir.md) |
| 156 | 2026-10-31 | [Las normas llegan por el plugin, en sus skills](156-2026-10-31-las-normas-llegan-por-el-plugin-en-sus-skills.md) |
| 155 | 2026-10-31 | [Las decisiones, a develop en cuanto se toman](155-2026-10-31-las-decisiones-a-develop-en-cuanto-se-toman.md) |
| 154 | 2026-10-31 | [Cerrar directamente lo que no tiene prueba](154-2026-10-31-cerrar-directamente-lo-que-no-tiene-prueba.md) |
| 153 | 2026-10-31 | [TURBO solo lanza las tareas en curso](153-2026-10-31-turbo-solo-lanza-las-tareas-en-curso.md) |
| 152 | 2026-10-31 | [Documentos compartidos, también por subagente](152-2026-10-31-documentos-compartidos-tambien-por-subagente.md) |
| 151 | 2026-10-31 | [Todo el trabajo de la tarea, a su subagente](151-2026-10-31-todo-el-trabajo-de-la-tarea-a-su-subagente.md) |
| 150 | 2026-10-31 | [Sin referencias por número que no se vean en pantalla](150-2026-10-31-sin-referencias-por-numero-que-no-se-vean-en-pantalla.md) |
| 149 | 2026-10-31 | [Orquestación con un subagente vivo por tarea](149-2026-10-31-orquestacion-con-un-subagente-vivo-por-tarea.md) |
| 148 | 2026-10-31 | [Las reglas del método se actualizan en una sola tarea](148-2026-10-31-las-reglas-del-metodo-se-actualizan-en-una-sola-tarea.md) |
| 147 | 2026-10-31 | [Documentación, una vez por tarea](147-2026-10-31-documentacion-una-vez-por-tarea.md) |
| 146 | 2026-10-30 | [Las mejoras de la SF pasan a tarea solo desde la SF](146-2026-10-30-las-mejoras-de-la-sf-pasan-a-tarea-solo-desde-la-sf.md) |
| 145 | 2026-10-31 | [Cada tarea tiene un tipo](145-2026-10-31-cada-tarea-tiene-un-tipo.md) |
| 144 | 2026-10-31 | [Cada tarea, en una sola sección del panel](144-2026-10-31-cada-tarea-en-una-sola-seccion-del-panel.md) |
| 143 | 2026-10-31 | [El objetivo del panel es el control y el foco](143-2026-10-31-el-objetivo-del-panel-es-el-control-y-el-foco.md) |
| 142 | 2026-10-31 | [Una tarea por documento que actualizar](142-2026-10-31-una-tarea-por-documento-que-actualizar.md) |
| 141 | 2026-10-30 | [Tras una fusión, redescribir la tarea resultante](141-2026-10-30-tras-una-fusion-redescribir-la-tarea-resultante.md) |
| 140 | 2026-10-30 | [El registro de decisiones es obligatorio](140-2026-10-30-el-registro-de-decisiones-es-obligatorio.md) |
| 139 | 2026-10-30 | [Menú al anotar: paso, en curso o en cola](139-2026-10-30-menu-al-anotar-paso-en-curso-o-en-cola.md) |
| 138 | 2026-10-30 | [Configuración inicial: tareas y repo siempre, el resto opcional](138-2026-10-30-configuracion-inicial-tareas-y-repo-siempre-el-resto-opcional.md) |
| 137 | 2026-10-30 | [La etiqueta de la cabecera dice SF y la versión del plugin](137-2026-10-30-la-etiqueta-de-la-cabecera-dice-sf-y-la-version-del-plugin.md) |
| 136 | 2026-10-30 | [El panel ejecuta una copia de cola.py hecha al cargar](136-2026-10-30-el-panel-ejecuta-una-copia-de-cola-py-hecha-al-cargar.md) |
| 135 | 2026-10-30 | [Borrar las ramas del subagente al volver](135-2026-10-30-borrar-las-ramas-del-subagente-al-volver.md) |
| 134 | 2026-10-30 | [Revertir elimina la tarea o la deja pendiente](134-2026-10-30-revertir-elimina-la-tarea-o-la-deja-pendiente.md) |
| 133 | 2026-10-30 | [Las tareas sin historial, con H y fuera de Cerradas](133-2026-10-30-las-tareas-sin-historial-con-h-y-fuera-de-cerradas.md) |
| 132 | 2026-10-30 | [Las descartadas se limpian al abrir una sesión nueva](132-2026-10-30-las-descartadas-se-limpian-al-abrir-una-sesion-nueva.md) |
| 131 | 2026-10-30 | [/paso, antes de los pasos de cierre](131-2026-10-30-paso-antes-de-los-pasos-de-cierre.md) |
| 130 | 2026-10-30 | [Prever choques al poner una tarea en curso](130-2026-10-30-prever-choques-al-poner-una-tarea-en-curso.md) |
| 129 | 2026-10-30 | [Lo último tocado, arriba; la tarea principal, la última tocada](129-2026-10-30-lo-ultimo-tocado-arriba-y-la-principal-la-ultima-tocada.md) |
| 128 | 2026-10-30 | [El «?» de los pasos, en verde](128-2026-10-30-el-interrogante-de-los-pasos-en-verde.md) |
| 127 | 2026-10-30 | [redescribir no guarda la descripción anterior](127-2026-10-30-redescribir-no-guarda-la-descripcion-anterior.md) |
| 126 | 2026-10-30 | [/redescribir: Claude vuelve a redactar una descripción](126-2026-10-30-redescribir-claude-vuelve-a-redactar-una-descripcion.md) |
| 125 | 2026-10-30 | [Al fusionar, cada descripción en su párrafo](125-2026-10-30-al-fusionar-cada-descripcion-en-su-parrafo.md) |
| 124 | 2026-10-29 | [Botón ACTUALIZAR: el plugin sf, solo cuando hay versión publicada nueva](124-2026-10-29-boton-actualizar-el-plugin-sf-solo-cuando-hay-version-publicada-nueva.md) |
| 123 | 2026-10-29 | [Botón RELEASE: versión elegida al pulsar, fast-forward y aviso de lo sin probar](123-2026-10-29-boton-release-version-elegida-al-pulsar-fast-forward-y-aviso-de-lo-sin-probar.md) |
| 122 | 2026-10-29 | [La P de probar pasa a T, de Test Mode](122-2026-10-29-la-p-de-probar-pasa-a-t-test-mode.md) |
| 121 | 2026-10-29 | [Cerrar exige siempre el paso de cerrar; quitar el de probar es cerrar sin probar](121-2026-10-29-cerrar-exige-siempre-el-paso-de-cerrar-quitar-el-de-probar-es-cerrar-sin-probar.md) |
| 120 | 2026-10-29 | [Cabecera en dos filas y botón TURBO](120-2026-10-29-cabecera-en-dos-filas-y-boton-turbo.md) |
| 119 | 2026-10-29 | [La ⚙ sale solo con un subagente trabajando](119-2026-10-29-la-rueda-dentada-sale-solo-con-un-subagente-trabajando.md) |
| 118 | 2026-10-29 | [Arriba, todas las tareas en curso enteras](118-2026-10-29-arriba-todas-las-tareas-en-curso-enteras.md) |
| 117 | 2026-10-29 | [Pasos de cierre fijos y E con confirmación para quitar pasos](117-2026-10-29-pasos-de-cierre-fijos-y-e-con-confirmacion-para-quitar-pasos.md) (sustituida en parte) |
| 116 | 2026-10-29 | [El paso de documentar es crear la tarea de documentos](116-2026-10-29-el-paso-de-documentar-es-crear-la-tarea-de-documentos.md) |
| 115 | 2026-10-29 | [Flujo de tareas: respuestas a la revisión de la tabla de estados](115-2026-10-29-flujo-de-tareas-respuestas-a-la-revision-de-la-tabla-de-estados.md) |
| 114 | 2026-10-29 | [La sección 2 de la metodología resume el flujo de tareas y remite a sf:flujo_tareas](114-2026-10-29-la-seccion-2-de-la-metodologia-resume-el-flujo-de-tareas-y-remite-a-sf-flujo-tareas.md) |
| 113 | 2026-10-29 | [Flujo de tareas: un CLI común, historial por tarea y copias de la cola](113-2026-10-29-flujo-de-tareas-un-cli-comun-historial-por-tarea-y-copias-de-la-cola.md) |
| 112 | 2026-10-29 | [Los documentos compartidos se actualizan en una tarea aparte](112-2026-10-29-los-documentos-compartidos-se-actualizan-en-una-tarea-aparte.md) |
| 111 | 2026-10-29 | [Un cierre que falla pasa a Claude](111-2026-10-29-un-cierre-que-falla-pasa-a-claude.md) |
| 110 | 2026-10-29 | [El mod impide que un subagente escriba la cola](110-2026-10-29-el-mod-impide-que-un-subagente-escriba-la-cola.md) |
| 109 | 2026-10-29 | [Un worktree es el proyecto de su repositorio](109-2026-10-29-un-worktree-es-el-proyecto-de-su-repositorio.md) |
| 108 | 2026-10-29 | [Una decisión por archivo, en `docs/decisiones/`](108-2026-10-29-una-decision-por-archivo-en-docs-decisiones.md) |
| 107 | 2026-10-29 | [Botón R para revertir una tarea](107-2026-10-29-boton-r-para-revertir-una-tarea.md) |
| 106 | 2026-10-29 | [Cabecera del panel fija al hacer scroll](106-2026-10-29-cabecera-del-panel-fija-al-hacer-scroll.md) |
| 105 | 2026-10-29 | [Lanzar sin esperar lo que no necesita al propietario](105-2026-10-29-lanzar-sin-esperar-lo-que-no-necesita-al-propietario.md) |
| 104 | 2026-10-29 | [Una entrada del registro dice la lección](104-2026-10-29-una-entrada-del-registro-dice-la-leccion.md) |
| 103 | 2026-10-29 | [La P no recarga el plugin](103-2026-10-29-la-p-no-recarga-el-plugin.md) |
| 102 | 2026-10-29 | [Libre, el orquestador desbloquea las tareas en curso](102-2026-10-29-libre-el-orquestador-desbloquea-las-tareas-en-curso.md) |
| 101 | 2026-10-29 | [Botón C para cerrar una tarea](101-2026-10-29-boton-c-para-cerrar-una-tarea.md) |
| 100 | 2026-10-29 | [El orquestador sugiere fusiones y splits](100-2026-10-29-el-orquestador-sugiere-fusiones-y-splits.md) |
| 99 | 2026-10-29 | [/fusionar junta tareas en una](099-2026-10-29-fusionar-junta-tareas-en-una.md) |
| 98 | 2026-10-29 | [Las descripciones, sin origen](098-2026-10-29-las-descripciones-sin-origen.md) |
| 97 | 2026-10-29 | [/split separa pasos en una tarea nueva](097-2026-10-29-split-separa-pasos-en-una-tarea-nueva.md) (sustituida en parte) |
| 96 | 2026-10-29 | [Los bugs son tareas nuevas](096-2026-10-29-los-bugs-son-tareas-nuevas.md) |
| 95 | 2026-10-29 | [La tarea que se prueba es la de la rama activa](095-2026-10-29-la-tarea-que-se-prueba-es-la-de-la-rama-activa.md) |
| 94 | 2026-10-29 | [Mejorar la skill que se usa es un paso](094-2026-10-29-mejorar-la-skill-que-se-usa-es-un-paso.md) |
| 93 | 2026-10-29 | [Los documentos, sin paja](093-2026-10-29-los-documentos-sin-paja.md) |
| 92 | 2026-10-29 | [Comandos antes que inferencia](092-2026-10-29-comandos-antes-que-inferencia.md) |
| 91 | 2026-10-29 | [Botón P para probar una tarea en su rama](091-2026-10-29-boton-p-para-probar-una-tarea-en-su-rama.md) |
| 90 | 2026-10-29 | [Pasos de cierre: probar y cerrar la tarea](090-2026-10-29-pasos-de-cierre-probar-y-cerrar-la-tarea.md) |
| 89 | 2026-10-29 | [Letras E, D y R en los botones de las tareas](089-2026-10-29-letras-e-d-y-r-en-los-botones-de-las-tareas.md) |
| 88 | 2026-10-29 | [Botón D para descartar una tarea](088-2026-10-29-boton-d-para-descartar-una-tarea.md) |
| 87 | 2026-10-29 | [El botón de Cerradas se llama «limpiar»](087-2026-10-29-el-boton-de-cerradas-se-llama-limpiar.md) |
| 86 | 2026-10-29 | [El subagente se lanza sin preguntar](086-2026-10-29-el-subagente-se-lanza-sin-preguntar.md) |
| 85 | 2026-10-29 | [La cabecera, en etiquetas: rama y duración de la sesión](085-2026-10-29-la-cabecera-en-etiquetas-rama-y-duracion-de-la-sesion.md) |
| 84 | 2026-10-29 | [El código de la tarea en curso, en amarillo también en las secciones](084-2026-10-29-el-codigo-de-la-tarea-en-curso-en-amarillo-tambien-en-las-secciones.md) |
| 83 | 2026-10-29 | [El principal orquesta; los subagentes ejecutan](083-2026-10-29-el-principal-orquesta-los-subagentes-ejecutan.md) |
| 82 | 2026-10-29 | [Una rama de feature por tarea](082-2026-10-29-una-rama-de-feature-por-tarea.md) |
| 81 | 2026-10-29 | [Pasos hechos, en participio](081-2026-10-29-pasos-hechos-en-participio.md) |
| 80 | 2026-10-29 | [Definir y decidir también son pasos](080-2026-10-29-definir-y-decidir-tambien-son-pasos.md) |
| 79 | 2026-10-29 | [Eliminar una tarea](079-2026-10-29-eliminar-una-tarea.md) |
| 78 | 2026-10-29 | [Descartar y revertir una tarea](078-2026-10-29-descartar-y-revertir-una-tarea.md) |
| 77 | 2026-10-28 | [Errores detectados, a Pendientes](077-2026-10-28-errores-detectados-a-pendientes.md) |
| 76 | 2026-10-28 | [«Cómo funciona el panel», aparte](076-2026-10-28-como-funciona-el-panel-aparte.md) |
| 75 | 2026-10-28 | [«Mejoras», sin más](075-2026-10-28-mejoras-sin-mas.md) |
| 74 | 2026-10-28 | [Probar antes de cerrar](074-2026-10-28-probar-antes-de-cerrar.md) |
| 73 | 2026-10-28 | [Medir el uso del panel: cualitativo](073-2026-10-28-medir-el-uso-del-panel-cualitativo.md) |
| 72 | 2026-10-28 | [/paso pone a Claude con el paso](072-2026-10-28-paso-pone-a-claude-con-el-paso.md) |
| 71 | 2026-10-28 | [El panel, sin horas y con el amarillo solo arriba](071-2026-10-28-el-panel-sin-horas-y-con-el-amarillo-solo-arriba.md) |
| 70 | 2026-10-28 | [El panel avisa si el proyecto va por detrás de la SF](070-2026-10-28-el-panel-avisa-si-el-proyecto-va-por-detras-de-la-sf.md) |
| 69 | 2026-10-28 | [Una tarea reabierta lleva H](069-2026-10-28-una-tarea-reabierta-lleva-h.md) |
| 68 | 2026-10-28 | [El mod, repartido en módulos](068-2026-10-28-el-mod-repartido-en-modulos.md) |
| 67 | 2026-10-28 | [Pasos de una tarea](067-2026-10-28-pasos-de-una-tarea.md) |
| 66 | 2026-10-28 | [Código de tarea más ligero: 74C](066-2026-10-28-codigo-de-tarea-mas-ligero-74c.md) |
| 65 | 2026-10-28 | [«Mejoras SF a valorar»](065-2026-10-28-mejoras-sf-a-valorar.md) |
| 64 | 2026-10-28 | [Cerradas: todo cambio en el cierre de una tarea](064-2026-10-28-cerradas-todo-cambio-en-el-cierre-de-una-tarea.md) |
| 63 | 2026-10-28 | [Cierre de tareas: propuestas sin Testing y Cerradas a 0](063-2026-10-28-cierre-de-tareas-propuestas-sin-testing-y-cerradas-a-0.md) |
| 62 | 2026-10-28 | [Modo prueba en el panel](062-2026-10-28-modo-prueba-en-el-panel.md) |
| 61 | 2026-10-28 | [Un bug en una tarea cerrada la reabre con su número](061-2026-10-28-un-bug-en-una-tarea-cerrada-la-reabre-con-su-numero.md) |
| 60 | 2026-10-28 | [La tarea que se está probando, en curso](060-2026-10-28-la-tarea-que-se-esta-probando-en-curso.md) |
| 59 | 2026-10-28 | [La tarea en curso, con su código en todos los sitios](059-2026-10-28-la-tarea-en-curso-con-su-codigo-en-todos-los-sitios.md) |
| 58 | 2026-10-28 | [Código de tarea: número y estado, «57-A»](058-2026-10-28-codigo-de-tarea-numero-y-estado-57-a.md) |
| 57 | 2026-10-28 | [Cerradas: botón para quitar las probadas](057-2026-10-28-cerradas-boton-para-quitar-las-probadas.md) |
| 56 | 2026-10-28 | [Panel: código en color y subrayado en lugar de led y ▸/▾](056-2026-10-28-panel-codigo-en-color-y-subrayado-en-lugar-de-led-y.md) |
| 55 | 2026-10-28 | [Nombre de la sesión: el del proyecto, solo al entrar](055-2026-10-28-nombre-de-la-sesion-el-del-proyecto-solo-al-entrar.md) |
| 54 | 2026-10-28 | [La letra es el estado: A, H, T y C; Sin probar pasa a Testing](054-2026-10-28-la-letra-es-el-estado-a-h-t-y-c-sin-probar-pasa-a-testing.md) |
| 53 | 2026-10-28 | [Bloque TAREAS con A y H](053-2026-10-28-bloque-tareas-con-a-y-h.md) |
| 52 | 2026-10-28 | [Las en curso, también en Pendientes](052-2026-10-28-las-en-curso-tambien-en-pendientes.md) |
| 51 | 2026-10-28 | [La pregunta de «¿está probada?»: una por petición, con tres respuestas](051-2026-10-28-la-pregunta-de-esta-probada-una-por-peticion-con-tres-respuestas.md) |
| 50 | 2026-10-28 | [Sin probar hasta el OK del propietario; preguntar antes de cambiar de tarea](050-2026-10-28-sin-probar-hasta-el-ok-del-propietario-preguntar-antes-de-cambiar-de-tarea.md) |
| 49 | 2026-10-28 | [Propuestas con número fijo: P01, P02…](049-2026-10-28-propuestas-con-numero-fijo-p01-p02.md) |
| 48 | 2026-10-28 | [Preguntar antes de cerrar una petición; lo nuevo, a la cola](048-2026-10-28-preguntar-antes-de-cerrar-una-peticion-lo-nuevo-a-la-cola.md) |
| 47 | 2026-10-28 | [Propuestas por decidir, desplegables con su resumen](047-2026-10-28-propuestas-por-decidir-desplegables-con-su-resumen.md) |
| 46 | 2026-10-28 | [Incorporar: menú con el caso detectado](046-2026-10-28-incorporar-menu-con-el-caso-detectado.md) |
| 45 | 2026-10-28 | [Skill para incorporar un proyecto; el `CLAUDE.md` del proyecto no se reescribe](045-2026-10-28-skill-para-incorporar-un-proyecto-el-claude-md-del-proyecto-no-se-reescribe.md) |
| 44 | 2026-10-27 | [Hecho en esta sesión: peticiones cerradas](044-2026-10-27-hecho-en-esta-sesion-peticiones-cerradas.md) |
| 43 | 2026-10-27 | [Marcador: solo los prompts; Cerradas cuenta todo lo cerrado](043-2026-10-27-marcador-solo-los-prompts-cerradas-cuenta-todo-lo-cerrado.md) |
| 42 | 2026-10-27 | [Lo probado sale de Sin probar](042-2026-10-27-lo-probado-sale-de-sin-probar.md) |
| 41 | 2026-10-27 | [El panel, en dos bloques; con JKanban, Planificado](041-2026-10-27-el-panel-en-dos-bloques-con-jkanban-planificado.md) |
| 40 | 2026-10-27 | [Textos compactos: nada que no aporte](040-2026-10-27-textos-compactos-nada-que-no-aporte.md) |
| 39 | 2026-10-27 | [La tarea en curso, en amarillo](039-2026-10-27-la-tarea-en-curso-en-amarillo.md) |
| 38 | 2026-10-27 | [Fuera el marcador de la última fila](038-2026-10-27-fuera-el-marcador-de-la-ultima-fila.md) |
| 37 | 2026-10-27 | [Sin línea de estado](037-2026-10-27-sin-linea-de-estado.md) |
| 36 | 2026-10-27 | [Claude Code Commander](036-2026-10-27-claude-code-commander.md) |
| 35 | 2026-10-27 | [Marcador del día: terminadas, dejadas y propuestas](035-2026-10-27-marcador-del-dia-terminadas-dejadas-y-propuestas.md) |
| 34 | 2026-10-27 | [Identidad de la sesión: color y nombre del proyecto](034-2026-10-27-identidad-de-la-sesion-color-y-nombre-del-proyecto.md) |
| 33 | 2026-10-27 | [El mod se presenta como una ventana pequeña](033-2026-10-27-el-mod-se-presenta-como-una-ventana-pequena.md) |
| 32 | 2026-10-27 | [El mod, centro de control de la SF: realimentación](032-2026-10-27-el-mod-centro-de-control-de-la-sf-realimentacion.md) |
| 31 | 2026-10-27 | [Cola de peticiones y un commit por petición](031-2026-10-27-cola-de-peticiones-y-un-commit-por-peticion.md) |
| 30 | 2026-10-27 | [Un proyecto por sesión](030-2026-10-27-un-proyecto-por-sesion.md) |
| 29 | 2026-10-27 | [Guías de instalación y de actualización en cada proyecto; documentos opcionales junto a la visión](029-2026-10-27-guias-de-instalacion-y-de-actualizacion-en-cada-proyecto-documentos-opcionales-junto-a-la-vision.md) |
| 28 | 2026-10-27 | [Forma de los documentos: texto literal, tarjetas, color con significado y código coloreado](028-2026-10-27-forma-de-los-documentos-texto-literal-tarjetas-color-con-significado-y-codigo-coloreado.md) |
| 27 | 2026-10-27 | [La carpeta `.sf/` identifica el proyecto y guarda su estado](027-2026-10-27-la-carpeta-sf-identifica-el-proyecto-y-guarda-su-estado.md) |
| 26 | 2026-10-27 | [Diagramas en SVG, nunca en ASCII](026-2026-10-27-diagramas-en-svg-nunca-en-ascii.md) |
| 25 | 2026-10-27 | [Un mapa de la SF: «Cómo funciona»](025-2026-10-27-un-mapa-de-la-sf-como-funciona.md) |
| 24 | 2026-10-27 | [La metodología viaja en el plugin `sf`](024-2026-10-27-la-metodologia-viaja-en-el-plugin-sf.md) |
| 23 | 2026-10-27 | [Propuestas, decisiones, plantillas y ejemplos, cada uno en su sitio](023-2026-10-27-propuestas-decisiones-plantillas-y-ejemplos-cada-uno-en-su-sitio.md) (sustituida en parte) |
| 22 | 2026-10-27 | [Llevar cada decisión a los documentos en cuanto se toma](022-2026-10-27-llevar-cada-decision-a-los-documentos-en-cuanto-se-toma.md) |
| 21 | 2026-10-27 | [Un solo plugin, `sf`, con las skills y activado para el usuario](021-2026-10-27-un-solo-plugin-sf-con-las-skills-y-activado-para-el-usuario.md) |
| 20 | 2026-10-27 | [La SF es fuente, no instalación operativa](020-2026-10-27-la-sf-es-fuente-no-instalacion-operativa.md) |
| 19 | 2026-10-27 | [Estado del proyecto en `docs/sf.json` y mod de estado](019-2026-10-27-estado-del-proyecto-en-docs-sf-json-y-mod-de-estado.md) (sustituida en parte) |
| 18 | 2026-10-27 | [Los proyectos anteriores a la SF se incorporan sin rehacerlos](018-2026-10-27-los-proyectos-anteriores-a-la-sf-se-incorporan-sin-rehacerlos.md) |
| 17 | 2026-10-26 | [Kit de documentos HTML en la SF](017-2026-10-26-kit-de-documentos-html-en-la-sf.md) |
| 16 | 2026-10-26 | [Documento fundacional en todos los proyectos](016-2026-10-26-documento-fundacional-en-todos-los-proyectos.md) |
| 15 | 2026-10-26 | [Documentos fundacionales juntos en `docs/specs/vision/`](015-2026-10-26-documentos-fundacionales-juntos-en-docs-specs-vision.md) |
| 14 | 2026-10-26 | [SmartColdBox, proyecto de referencia de software, hardware y gemelo digital](014-2026-10-26-smartcoldbox-proyecto-de-referencia-de-software-hardware-y-gemelo-digital.md) |
| 13 | 2026-10-26 | [La SF es para una persona con muchos proyectos](013-2026-10-26-la-sf-es-para-una-persona-con-muchos-proyectos.md) |
| 12 | 2026-10-26 | [Varias visiones de la SF, una por perspectiva](012-2026-10-26-varias-visiones-de-la-sf-una-por-perspectiva.md) |
| 11 | 2026-10-26 | [Claude Code, centro del trabajo de desarrollo](011-2026-10-26-claude-code-centro-del-trabajo-de-desarrollo.md) |
| 10 | 2026-10-26 | [JKanban, con un MCP a medida e instalado dentro de la SF](010-2026-10-26-jkanban-con-un-mcp-a-medida-e-instalado-dentro-de-la-sf.md) |
| 9 | 2026-10-25 | [Método propio, técnicas reutilizadas](009-2026-10-25-metodo-propio-tecnicas-reutilizadas.md) |
| 8 | 2026-10-25 | [Perfil técnico «Escritorio Python con MVP y agente Claude Code»](008-2026-10-25-perfil-tecnico-escritorio-python-con-mvp-y-agente-claude-code.md) |
| 7 | 2026-10-25 | [Fuente de las skills en la SF y lo propio de cada proyecto en `docs/identidad/`](007-2026-10-25-fuente-de-las-skills-en-la-sf-y-lo-propio-de-cada-proyecto-en-docs-identidad.md) (sustituida en parte) |
| 6 | 2026-10-25 | [Tamaño y orden de las devslices](006-2026-10-25-tamano-y-orden-de-las-devslices.md) |
| 5 | 2026-10-25 | [Skill de infografía técnica generalizada](005-2026-10-25-skill-de-infografia-tecnica-generalizada.md) |
| 4 | 2026-10-25 | [Skill de visión independiente de OncoCore y del dominio](004-2026-10-25-skill-de-vision-independiente-de-oncocore-y-del-dominio.md) |
| 3 | 2026-10-25 | [Temas visuales de la skill de visión](003-2026-10-25-temas-visuales-de-la-skill-de-vision.md) |
| 2 | 2026-10-25 | [Adoptar `oklch-skill` para las paletas](002-2026-10-25-adoptar-oklch-skill-para-las-paletas.md) |
| 1 | 2026-10-25 | [Funcionalidades y devslices son cosas distintas](001-2026-10-25-funcionalidades-y-devslices-son-cosas-distintas.md) |
