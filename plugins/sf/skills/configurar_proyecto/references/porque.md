# Por qué de cada regla

El porqué de cada regla de la skill, en el orden de sus secciones. Cada entrada cita la decisión de la SF que la fijó, con su título y su número entre paréntesis.

## Dónde está la configuración

- **Campos sueltos en `.sf/proyecto.json`** («Todo proyecto.json es configuración: plana, y bloques solo para lo afín», 227): todo lo que guarda el archivo es configuración, también el nombre y el color, así que no hace falta un bloque `config` aparte. Solo se agrupan los elementos afines cuando son muchos, como `automatizaciones`; un par de campos relacionados no justifica un bloque.
- **Se cambia pidiéndoselo a Claude, con su skill y `/sf_config`** («La configuración se cambia pidiéndoselo a Claude, con menús», 228): la configuración se elige al incorporar, pero puede cambiar después (activar la metodología, elegir un kanban, cambiar el remoto). Se descartó una orden suelta de `cola.py` y editar el archivo a mano; primero iba a ser un caso de la incorporación y el propietario prefirió una skill y una orden propias.

## Una operación, sin tarea

- **Sin cola, sin rama y sin panel** («Incorporar un proyecto es una operación sin tarea, guiada por menús», 209): incorporar se hacía como una tarea más, con rama y squash, y poner al día ya había dejado de serlo. Configurar es lo mismo: Claude dice qué va a cambiar, pide el OK y lo aplica en `develop` con su commit; lo que salga mal se deshace con git.

## Un proyecto por sesión

- **La SF se configura igual** («La SF se lleva como los demás proyectos: .sf/proyecto.json, documentos en sf/ y sin excepciones», 299): así la SF se prueba exactamente como la reciben los demás proyectos, y no hay reglas que digan una cosa en los proyectos y otra en la SF.

## Lo fijo no se configura

- **Siempre `develop`** («El manejo del repositorio no se negocia: siempre develop», 205): la SF trabaja con su modelo de ramas (`develop`, una rama por tarea que entra por squash al cerrarla, y publicar es pasar `develop` a `main` con su tag). El manejo del repositorio forma parte del mecanismo que la SF fija.
- **Un remoto en GitHub** («Sin remoto en GitHub no hay SF: se valida al incorporar y, si falta, se crea», 230): un remoto en otro servicio (GitLab u otro) no cuenta. Es una limitación inicial a propósito: «más adelante nos replanteamos abrir el abanico. Por ahora KISS» (propietario).
- **Los commits los hace Claude** («Los commits los lleva siempre Claude», 225): forman parte del manejo del repositorio. Si los hiciera el desarrollador a mano se perderían los subagentes, el squash y revertir; lo que sí se adapta es su idioma y su formato.
- **La versión con su tag** («La versión forma parte del manejo del repositorio», 226): publicar es siempre pasar `develop` a `main` (o a la rama que haga de `main`) con el tag `vX.Y.Z`, igual en todos los proyectos. Lo único que se elige son los archivos donde se sube el número.

## Herramienta

- **La orden de Python, la que da el mod** («La orden de Python sale del intérprete que se detecta, no de `python` fijo», 236): en macOS y Linux `python` suele no existir (allí es `python3`). Con el intérprete que detecta el mod, la SF funciona igual en Windows, macOS y Linux sin preparar nada.

## Procedimiento

- **El color de las sesiones sale del estilo** («El color de sesión se deriva del color primario del estilo del proyecto», 310): una sola fuente para el color del proyecto, así que se cambia con el estilo, no aquí. **Puede coincidir con el de la SF** («El color de sesión de la SF no se reserva: un proyecto puede salir del mismo color», 311): que hoy haya menos temas que colores es circunstancial, y en el futuro puede haber varios temas del mismo color.
- **Kanban opcional, por defecto ninguno** («El kanban se elige, y por defecto ninguno», 224): JKanban no está conectado y un usuario nuevo no lo tiene; el proyecto funciona solo con su cola. Por eso no se afirma que el proyecto exista en el kanban hasta crearlo.
- **La firma de los commits, configurable; sin configurar, sin línea** («La firma del commit de cierre es configurable; sin configurar, sin línea», 238): la línea fija «Co-Authored-By: Claude Opus…» no servía a todos. Se recomienda la de Claude con el modelo de la sesión, porque los commits los hace Claude.
- **El número de la tarea, según el formato de los commits** («El número de la tarea en el commit, según el formato del proyecto», 207): el número sirve a las personas, para ver en `git log` a qué tarea es cada commit. Un «(N)» al final del título rompe formatos estrictos como conventional commits; allí va al pie, `SF-Tarea: N`.
- **El prefijo del squash, del tipo de la tarea** («El título del commit en formato conventional sale del tipo de tarea», 233): la C del panel cierra sin pedir nada, así que el título tiene que salir solo: implementar da `feat`, corregir `fix`, documentar y especificar `docs`; sin tipo, `chore`.
- **Rama de publicación solo en el remoto: se crea la local sin preguntar** («Si main solo está en el remoto, se crea la local sin preguntar», 234): la SF necesita en local `develop` y la rama que hace de `main`; si ya existe en el remoto, basta con seguirla, y se dice en el resumen. Vale igual para `develop`.
- **`master` puede hacer de `main`** («Si el proyecto tiene master, se pregunta si hace de main», 213): la SF no renombra ramas del proyecto, y crear `main` al lado de `master` dejaba dos ramas principales. Si se elige una que no existe, se ofrece crearla desde la actual.
- **Automatizaciones con interruptor; solo se escriben las apagadas** («Las automatizaciones del plugin, configurables y avisando antes que bloquear», 171): pasar reglas a código las hace cumplirse siempre, pero vuelve el plugin rígido para quien trabaje de otra forma. Cada una tiene su interruptor con un valor por defecto prudente (encendida).
- **Lo que falla de la SF no se anota en el proyecto** («Un proyecto solo anota propuestas suyas», 210): las propuestas de cada proyecto se llenaban de cosas de la SF que repetían lo que el propietario ya llevaba a ella y que nadie del proyecto iba a hacer. Llevarlo a la SF es cosa del propietario, en una sesión de la SF.
