# sf — plugin de la Software Factory

Plugin de Claude Code de la SF. Reúne todo lo que la SF da a los proyectos: la metodología (skill `sf:metodologia`), las skills, las plantillas de estructuras, el kit de documentos HTML y el mod de estado. El mapa completo está en [Cómo funciona la SF](https://github.com/jumibot/SoftwareFactory/blob/main/docs/como-funciona-la-software-factory.md).

## Mod de estado

Dice si el proyecto abierto está bajo la Software Factory y en qué punto del método está.

- **Panel lateral (`/sf`):** se abre solo en pantalla completa; sin panel, una **caja sobre el prompt** de reserva, cuya primera línea es `SF · <proyecto> · <n>/7 <fase> · devslice <nombre>`, `SF · repositorio de la SF` o `Sin SF`. El mod no usa la línea de estado. Sin pantalla completa los clics no llegan: el panel y la caja lo avisan en texto y, con el primer mensaje del propietario, Claude ofrece activarla (en `.claude/settings.local.json` del proyecto, solo con su OK).
- **`/sf`:** panel con las fases del método (✓ hechas, ▶ actual, · pendientes), la devslice en curso, los documentos que existen en `docs/` y los pendientes.
- **Reglas y orquestación:** en los proyectos con `.sf/proyecto.json`, no en la SF, el mod entrega como contexto, al empezar la sesión, tras `/clear` y tras compactar, las reglas comunes de `templates/claude-sf.md`, las del método de `templates/claude-sf-metodologia.md` si el proyecto sigue la metodología, una línea con sus convenciones (idioma, commits, remoto y rama de publicación) y la skill `sf:orquestacion` entera, del plugin instalado (decisión 187). Si el `CLAUDE.md` aún importa `.sf/claude-sf.md`, entrega solo la orquestación y el panel avisa de que el proyecto va atrasado. La orquestación se apaga con `"automatizaciones": {"orquestacion": false}` en `.sf/proyecto.json`.

Lee la carpeta `.sf/` del proyecto al abrir la sesión y al acabar cada turno (metodología, 6).

`.sf/proyecto.json`, versionado, dice que el proyecto está bajo la SF y guarda su configuración, en campos sueltos; lo que falta vale lo de por defecto (`metodologia` true, sin `kanban`, `idioma` es, `commits` libre, `remoto` origin, `rama_main` main, sin `manifiesto` y sin `coautor`: los commits de la SF van sin línea de coautoría, decisión 238). El detalle, en el informe «Configuración inicial»:

```json
{
  "sf": "1.5.0",
  "proyecto": "Recetario",
  "descripcion": "Guarda recetas y genera la lista de la compra de la semana",
  "color": "pink",
  "metodologia": true,
  "kanban": { "proveedor": "jkanban", "proyecto": "Recetario" },
  "idioma": "ca",
  "commits": "libre",
  "remoto": "origin",
  "rama_main": "master",
  "manifiesto": ["frontend/package.json", "backend/pyproject.toml"],
  "coautor": "Co-Authored-By: Claude <noreply@anthropic.com>"
}
```

La configuración se cambia con `/sf_config` (o pidiéndoselo a Claude): la skill `sf:configurar_proyecto` la enseña, pregunta qué cambiar con menús, pide el OK y lo aplica en `develop` con su commit, sin tarea. `tools/configuracion.py` (`ver` y `detectar`, solo lee) la comprueba y detecta las convenciones, para esa skill y para la incorporación.

Sin metodología, el panel no da fase ni lee `.sf/estado.json`. Un valor que no se entiende, o un remoto que no existe o no apunta a GitHub, sale en los avisos del panel.

`.sf/estado.json`, fuera de git, guarda el estado en el método (solo con metodología):

```json
{
  "fase": "especificacion",
  "detalle": "interfaz: pantalla de revisión",
  "devslice": null,
  "hechas": ["vision"],
  "actualizado": "2026-10-27",
  "pendientes": ["aclarar qué manifiesto manda"]
}
```

Fases (metodología, 3.1–3.7): `vision`, `especificacion`, `tecnica`, `planificacion`, `preparacion`, `desarrollo`, `cierre`. Sin `hechas`, se dan por hechas las fases anteriores a la actual. Si el proyecto solo tiene el antiguo `docs/sf.json`, el mod lo lee y avisa de que hay que moverlo a `.sf/`.

## Instalación

### Requisitos

- **Claude Code**, con la sesión iniciada.
- **git** y una **cuenta de GitHub**, con [`gh`](https://cli.github.com/) instalado y la sesión iniciada (`gh auth login`): cada proyecto bajo la SF tiene su repositorio en GitHub, y la incorporación lo crea con `gh` si falta (decisión 230).
- **Python 3.9 o posterior**, como `python`, `python3` o `py`: el mod usa el primero que encuentra (decisión 236). El de macOS sirve sin instalar nada. Los documentos HTML necesitan además el paquete `markdown`, y `Pillow` si llevan logo (`python3 -m pip install markdown Pillow`).
- **Sistema:** Windows, macOS o Linux.
- **El panel** (`/sf`) se abre con Claude Code a pantalla completa; sin ella, la SF funciona igual y el estado sale en una caja sobre el prompt.

### Instalar

La SF es la fuente: aquí se crea y se modifica, pero los proyectos no la usan directamente. Instalan la versión publicada en GitHub, de la que Claude Code guarda su propia copia en `~/.claude/plugins/cache/`. Nunca se instala desde la carpeta local del repositorio.

Una sola vez por equipo, para el usuario (así queda activo en todos los proyectos):

```
claude plugin marketplace add jumibot/SoftwareFactory
claude plugin install sf@softwarefactory --scope user
```

Al instalar `sf` se instalan también sus dependencias: `gsap-skills`, `threejs-skills` y `oklch-skill`. Son entradas del catálogo de la SF fijadas a un commit de sus repositorios (decisiones 175 y 176), así que no hace falta añadir ningún otro catálogo.

Después, en Claude Code, pide «comprueba la instalación de la SF»: la skill `sf:comprobar_instalacion` revisa el catálogo, `sf`, sus dependencias y los requisitos, y arregla lo que falte con tu OK (decisión 244).

## Publicar un cambio

Para quien mantiene la SF.

1. Cambiar el mod aquí y probarlo en una sesión aparte: `claude --plugin-dir <repositorio de la SF>/plugins/sf`.
2. Subir `version` en `.claude-plugin/plugin.json`; la copia instalada se guarda por versión.
3. Commit y push.
4. Actualizar la copia instalada con el botón ACTUALIZAR del panel. El botón refresca el catálogo, ejecuta `claude plugin update` e instala las dependencias de la versión nueva que falten antes de recargar o pedir reiniciar (decisión 176). Si alguna no se instala, avisa con una orden por dependencia, una por línea, y no recarga. Se puede apagar en `.sf/proyecto.json` con `"automatizaciones": {"dependencias_al_actualizar": false}`: entonces no instala nada y da las órdenes de las que falten.

### Actualizar a mano

`claude plugin update` no instala las dependencias nuevas, y sin una de ellas `sf` no carga, ni su panel. A mano, una orden por plugin:

```
claude plugin marketplace update softwarefactory
claude plugin update sf@softwarefactory --scope user
claude plugin install gsap-skills@softwarefactory --scope user
claude plugin install threejs-skills@softwarefactory --scope user
claude plugin install oklch-skill@softwarefactory --scope user
```

Instalar una dependencia que ya está no cambia nada. Si una versión añade otra, se añade aquí al publicarla.
