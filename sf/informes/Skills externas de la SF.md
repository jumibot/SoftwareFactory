# Skills externas de la SF

Inventario de la tarea 255 (2026-11-01), sobre el plugin `sf` 1.2.9 de `develop`. Distingue lo **comprobado** (en el repositorio, en `git log` o en los archivos) de lo que es **hipótesis**.

Después del inventario, el propietario tomó la decisión 175: una skill externa que la SF usa tal cual es una dependencia, que se resuelve al instalar el plugin. Solo viaja en el plugin una versión nuestra, personalizada, con su origen y sus cambios anotados. Cómo aplicarla está en «Cómo declarar dependencias» y en «Propuesta por skill», al final.

## En resumen

- **Viajan en el plugin 16 skills de terceros, copiadas enteras:** las cinco `gsap-*` (GreenSock), las diez `threejs-*` (CloudAI-X) y `oklch-skill` (Jakub Krehel). Las tres son MIT y llevan su `LICENSE` y su `ORIGIN.md`. Entraron el 2026-10-25, por la decisión 007 («todas las skills, también las externas, tienen su fuente en la SF»), y viajan en el plugin desde el 2026-10-27 (0.3.0). No tienen ningún cambio.
- **Dos skills propias dependen de skills de terceros que el plugin no lleva:** `documento_vision` pide el validador de paletas de `dataviz` y `diseno_interfaz` cita `frontend-design` y `webapp-testing` como candidatas sin validar.
- **Otras fuentes se estudiaron y se reescribieron, sin copiarlas** (BMAD, Spec Kit, MADR, Superpowers, las guías de Vercel y Taste Skill). Quedan anotadas en el `ORIGIN.md` de cada skill propia. No son dependencias.
- **El plugin no declara dependencias de otros plugins** (`plugin.json` y `marketplace.json`).
- **Solo `oklch-skill` está adoptada** tras usarla (decisión 002). De las `gsap-*` y las `threejs-*` no hay ninguna prueba de uso registrada.

## Copiadas en el plugin

| Skill | Origen | Licencia | Para qué y quién la usa | Probada en la práctica | Riesgos |
| --- | --- | --- | --- | --- | --- |
| `oklch-skill` | [jakubkrehel/oklch-skill](https://github.com/jakubkrehel/oklch-skill), commit `0e81f04` (2026-10-02). Comprobado. | MIT, Jakub Krehel | Crear la `serie` de colores de los temas de `documento_vision` (`SKILL.md`, línea 268; tema `colorido`) | **Sí.** Se rehízo el tema `colorido` con ella y la serie pasó el validador de `dataviz`. La adoptó el propietario (decisión 002). | Bajo. Pesa unos 16 KB, que solo se cargan al invocarla. |
| `gsap-core`, `gsap-timeline`, `gsap-plugins`, `gsap-utils`, `gsap-performance` | GreenSock, «skills oficiales de GSAP», según su `LICENSE`. **No consta el repositorio ni la versión:** se copiaron de la antigua instalación global en `~/.claude/skills/`, retirada después. Pendiente de que lo confirme el propietario. | MIT, GreenSock. Cubre el texto de la skill, no la librería GSAP. | Skills de apoyo de `infografia_tecnica`, que las carga a discreción y manda sobre ellas (tabla «Cuándo aporta cada una») | **No consta.** Hipótesis: la tabla se escribió con experiencia de SmartColdBox, pero sus dos infografías no usan GSAP (0 apariciones) y la plantilla de la skill tampoco. | Origen sin rastrear, así que no se pueden actualizar con garantías. Seis remisiones a skills que no se copiaron (`gsap-scrolltrigger`, `gsap-react`). Unos 63 KB. La licencia de la librería GSAP no es MIT (hipótesis, por comprobar antes de usarla en un producto). |
| `threejs-fundamentals`, `-geometry`, `-materials`, `-lighting`, `-textures`, `-animation`, `-interaction`, `-shaders`, `-postprocessing`, `-performance` | CloudAI-X, según su `LICENSE`. **No consta el repositorio ni la versión.** Están escritas para three.js r186 (2026-09-08), así que se copiaron entre esa fecha y el 2026-10-25. | MIT, CloudAI-X | Skills de apoyo de `infografia_tecnica`, que fija three.js 0.186.1 «porque es la versión de las skills» | **No consta su uso como skills.** Las infografías de SmartColdBox usan three.js e `InstancedMesh`, pero no `OutlinePass` ni los demás recursos que recomienda la tabla. Hipótesis: lo aprendido vino del proyecto, no de cargar las skills. | Atan la infografía a r186, que envejecerá. Gran parte del texto trata de WebGPU y TSL, que la propia `infografia_tecnica` descarta. Son las más pesadas: unos 261 KB. |

**Peso fijo en el contexto (comprobado).** Las 16 descripciones suman unos 5 KB (unos 1.300 tokens). Ese texto entra en la lista de skills de **toda sesión de todo proyecto que tenga el plugin**, aunque no haga infografías ni paletas. El cuerpo de cada skill solo se carga al invocarla.

## Dependencias que el plugin no lleva

| Skill | Origen | Quién la usa y cómo | Viaja | Riesgo |
| --- | --- | --- | --- | --- |
| `dataviz` (`validate_palette.js`) | Skill de Anthropic que trae el entorno de Claude. Hipótesis: no está en `~/.claude/skills` ni en los plugins instalados. | `documento_vision` la exige para validar el orden de una serie («hasta que no dé fallos») | No | Si un entorno no la trae, el paso no se puede cumplir. No está anotada como dependencia, aunque la especificación (sección 2) pide anotar las dependencias que no vienen incluidas. |
| `frontend-design`, `webapp-testing` | Anthropic (`frontend-design` está instalado como plugin oficial en esta máquina) | `diseno_interfaz` las menciona como candidatas para el aspecto y las pruebas web, «ninguna validada» | No | Bajo: solo se mencionan, no hay que cargarlas. Siguen sin evaluar en la propuesta P18. |

## Estudiadas y reescritas, no instaladas

Se anotan en el `ORIGIN.md` de cada skill propia. No se ejecutan ni se cargan, así que no hay que mantenerlas:

- **`definicion_tecnica`:** BMAD `bmad-architecture` (commit `61e01f8`), Spec Kit (`67e0f72`) y MADR 4.0.0.
- **`diseno_interfaz`:** BMAD `bmad-ux`, Spec Kit, Scott Hurff y Superpowers `brainstorming`.
- **`documento_fundacional` y `kit_documentos`:** las Web Interface Guidelines de Vercel (solo se leyeron las reglas) y `leonxlnx/taste-skill`, cuyos `lint.mjs` e `inspect.mjs` se ejecutaron sobre una copia.

Ninguna de estas dos skills propias está validada en un piloto (decisión 009 y P18).

## Lo que dicen las normas, y dónde no casan

- **La especificación (sección 2) es un acuerdo:** las externas seleccionadas se copian enteras al repositorio y viajan con el plugin. Cada una lleva su procedencia: autor, repositorio, versión o commit, licencia, cambios y dependencias. Las `gsap-*` y las `threejs-*` **no cumplen** lo del repositorio ni lo del commit.
- **La propuesta P07, pendiente de aprobación,** dice lo contrario: estudiar las externas y reescribirlas, sin instalarlas. Su punto 6 pide revisar una a una `oklch-skill`, las `gsap-*` y las `threejs-*`.
- **`CLAUDE.md`** dice: «Las skills externas son candidatas sin validación práctica». Se refiere a las de la P18, pero 16 externas ya viajan en el plugin, y 15 de ellas sin una validación registrada.

## Cómo declarar dependencias (Claude Code 2.1.316)

La documentación oficial está en code.claude.com/docs/en: `plugins-reference`, `plugins/dependencies`, `plugins/marketplace-reference` y `plugins/install`. Cada punto dice cómo se sabe: **[D]**, documentado; **[V]**, comprobado con `claude plugin validate` sobre un manifiesto de prueba, sin instalar nada; **[H]**, hipótesis.

- **Campo `dependencies`** en `plugin.json` o en la entrada del `marketplace.json` **[D] [V]**:
  - Cada elemento es `"nombre"`, `"nombre@marketplace"` o `{name, marketplace, version}`. Un nombre suelto se busca en el marketplace propio.
  - `version` es un rango semver que se resuelve contra los tags `<plugin>--v<versión>` de la dependencia: su mantenedor tiene que publicar tags.
  - El validador reconoce el campo: a un nombre mal escrito le pregunta «did you mean "dependencies"?».
- **Se instalan solas** **[D]**:
  - Al instalar el plugin, Claude Code instala y activa sus dependencias en el mismo ámbito.
  - Al desinstalarlo, quedan hasta `claude plugin prune`, una orden que sí aparece en la ayuda del CLI.
- **Solo un plugin puede ser una dependencia** **[D]**. Una skill suelta no.
- **Una dependencia de otro marketplace** **[D]**:
  - Por defecto no se instala.
  - Hay que permitirla en el `marketplace.json` de la SF, con `allowCrossMarketplaceDependenciesOn: ["<marketplace>"]` **[V]**.
  - Si se declara en la entrada del marketplace y no está permitida, se rechaza la instalación. Si se declara en `plugin.json`, el plugin se instala sin la dependencia y después no carga.
  - **[H]** Hipótesis: el marketplace ajeno tiene que estar añadido en la máquina antes.
- **Una entrada del marketplace de la SF puede apuntar a un repositorio ajeno, fijado a un commit** **[D] [V]**:
  - `source` admite `github` (`repo`, `ref`, `sha`), `url` y `git-subdir` (`url`, `path`, `sha`).
  - Si el repositorio ajeno no tiene `plugin.json`, la entrada hace de manifiesto, y puede llevar `strict: false` y `skills` para elegir qué skills se cargan.
  - Con un `plugin.json` en el repositorio y `skills` en la entrada, el plugin no carga: «conflicting manifests».
  - Así se depende de él como de un plugin del mismo marketplace: sin lista de permitidos y con la versión fijada por `sha`.
- **No sirve para esto:**
  - Rutas fuera de la carpeta del plugin: no cargan **[D]**.
  - `enabledPlugins` en los ajustes del proyecto: no descarga un plugin externo en otra máquina **[D]**.

**No se ha probado ninguna instalación real**, porque estaba prohibido instalar en `~/.claude`. Hay que probarla antes de publicar. Otra consecuencia **[H]**: cada dependencia es un plugin con su propio espacio de nombres. Por ejemplo, `oklch:oklch-skill` en lugar de `sf:oklch-skill`, así que habría que cambiar las remisiones de `documento_vision` y de `infografia_tecnica`.

## El origen, ya rastreado (comprobado con `gh api`, 2026-11-01)

| Skill | Repositorio | ¿Es plugin o marketplace? | ¿Nuestra copia es igual? | Qué más trae el repositorio |
| --- | --- | --- | --- | --- |
| `gsap-*` | [greensock/gsap-skills](https://github.com/greensock/gsap-skills), MIT. El último cambio en `skills/` es el commit `a9d6270` (2026-04-21). | **Sí.** Marketplace `gsap-skills` con el plugin `gsap-skills` 1.0.0, con su `plugin.json`. No tiene tags. | **Sí.** Los cinco `SKILL.md` son idénticos al `main` actual. | Tres skills más: `gsap-scrolltrigger`, `gsap-react` y `gsap-frameworks`. |
| `threejs-*` | [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills), MIT, commit `0e18186` (2026-10-19) | **No.** No tiene `.claude-plugin`. | **Sí.** Los diez son idénticos. | Tres más: `threejs-asset-pipeline`, `threejs-loaders` y `threejs-react-three-fiber`. |
| `oklch-skill` | [jakubkrehel/oklch-skill](https://github.com/jakubkrehel/oklch-skill), MIT, commit `0e81f04` (2026-10-02) | **No.** | **Sí.** El `SKILL.md` y sus cuatro referencias son idénticos. | Nada más. |
| `dataviz` | Anthropic. **[H]** Viene con Claude Code: no está entre las skills sincronizadas de la cuenta (`~/.claude/skills/synced`) ni en el marketplace oficial. | No. | No hay copia. | No aplica. |

**Las 16 se usan tal cual.** Ninguna está personalizada, así que la decisión 175 no deja ninguna en el plugin como versión nuestra.

## Propuesta por skill (sin aplicar)

| Skill | Propuesta | A favor | En contra |
| --- | --- | --- | --- |
| `oklch-skill` | **Dependencia.** Una entrada `oklch` en el marketplace de la SF, con `source` `github`, `sha` `0e81f04` y `strict: false`, y `"dependencies": ["oklch"]` en `sf`. | Es la única adoptada y usada. Queda fijada al commit y no necesita lista de permitidos. Se actualiza cambiando el `sha`. | Cambia su espacio de nombres. Hay que probar que una entrada sin `plugin.json` carga la carpeta `skills/` **[H]**. |
| `threejs-*` | **A)** Dependencia: una entrada `threejs` con `source` `github`, `sha` `0e18186`, `strict: false` y `skills` limitado a las diez de ahora. **B)** Quitarlas: `infografia_tecnica` conserva su tabla y dice que se instalen aparte si hacen falta. | A: se mantiene el apoyo, con la versión fijada y sin las tres sobrantes. B: un proyecto sin infografías no carga sus descripciones (unos 3 KB por sesión, y las diez juntas pesan 261 KB). | A: no consta que se hayan usado, y pesan en todos los proyectos. B: se pierde la carga automática, y la infografía fija three.js r186 por ellas. |
| `gsap-*` | **A)** Dependencia cruzada con `gsap-skills@gsap-skills`, permitida en `allowCrossMarketplaceDependenciesOn`. **B)** Volver a listar su repositorio en el marketplace de la SF, con `source` `github` y `sha`. **C)** Quitarlas. | A: el canal oficial, que se actualiza solo. B: la versión queda fijada. C: no se usan (ni las infografías de SmartColdBox ni la plantilla usan GSAP), se ahorra peso y se evita la duda sobre la licencia de la librería. | A: sin tags no hay rango semver, así que entra lo último sin revisarlo, más tres skills que no se usan. B: su `plugin.json` impide elegir skills: entran las ocho. C: si algún día hace falta GSAP, cada proyecto la instala aparte. |
| `dataviz` | **No puede ser una dependencia**, porque no es un plugin. **A)** Anotarla como requisito del entorno en `documento_vision`, con un paso de reserva si no está. **B)** Un validador de paletas propio en `documento_vision/scripts/`, escrito por la SF: sería una versión nuestra. | A: barata. B: el paso siempre se puede cumplir y no depende de lo que traiga la sesión. | A: el paso queda a merced del entorno. B: hay que escribirlo y mantenerlo. La licencia de `dataviz` no consta, así que solo se podrían tomar ideas. |

Recomendación: `oklch-skill` como dependencia. Las `gsap-*`, quitarlas (C). Las `threejs-*` y `dataviz`, que decida el propietario. Si las `threejs-*` se quedan, como dependencia (A). Para `dataviz`, empezar por A. Antes de publicar, probar la instalación con un marketplace de prueba en un ámbito desechable.

## Qué hay que cambiar después

- **Plugin:**
  - `marketplace.json`: entradas nuevas y, si hace falta, `allowCrossMarketplaceDependenciesOn`.
  - `plugin.json` de `sf`: `dependencies`.
  - Fuera de `plugins/sf/skills/`: las carpetas de las 16 skills externas.
  - Una `version` nueva al publicar.
- **Skills propias:**
  - `infografia_tecnica` (`SKILL.md`, sección «Skills de apoyo», y `ORIGIN.md`): nombres con el nuevo espacio de nombres, o sin las de GSAP.
  - `documento_vision` (`SKILL.md`, línea 268, y `ORIGIN.md`): `oklch` como dependencia y `dataviz` como requisito o con su sustituto.
  - Los `ORIGIN.md` de las externas desaparecen con ellas. Su procedencia (repositorio, commit, licencia y para qué se usa) pasa a la entrada del marketplace y a un registro de dependencias. Dónde va ese registro está por decidir: en el `ORIGIN.md` de la skill que la usa, o en una tabla del README.
- **Documentos:**
  - Especificación, sección 2: las externas tal cual son dependencias, no copias. La procedencia pasa a la dependencia. Hay que borrar «incluso sin adaptaciones» y el ejemplo de `gsap-*` y `threejs-*`.
  - `README.md`, líneas 93 a 97.
  - La decisión 007: anotar que la 175 la sustituye en lo de las externas.
  - La P07: superada en lo que choca con la 175. Lo que queda (estudiar en cuarentena y reescribir) se aplica a las versiones nuestras.
  - La P18: las candidatas que se adopten tal cual entrarán como dependencias.
- **Documentos compartidos** (en su tarea «Actualizar…»):
  - «Cómo funciona la Software Factory»: piezas del plugin, dependencias e instalación.
  - `CLAUDE.md`: la regla sobre las skills externas.
  - La metodología, apartado 6, si habla de dónde viven las skills.

## Aplicación (decisión 176, 2026-11-01)

El propietario decidió que las 16 skills pasan a ser dependencias, sin quitar ninguna. Así quedó aplicado:

- **`plugin.json` de `sf`:** `"dependencies": ["threejs-skills@softwarefactory", "oklch-skill@softwarefactory", "gsap-skills@gsap-skills"]`.
- **`marketplace.json`:**
  - `allowCrossMarketplaceDependenciesOn: ["gsap-skills"]`.
  - Entrada `oklch-skill`: `github`, `sha` `0e81f04…`, `strict: false`.
  - Entrada `threejs-skills`: `git-subdir` de `skills/`, `sha` `0e18186…`, `strict: false` y las diez skills en `skills`.
- **Copias retiradas** de `plugins/sf/skills/`.

**Comprobado, con una configuración desechable** (`CLAUDE_CONFIG_DIR` en el scratchpad, sin tocar `~/.claude`), con `claude plugin validate`, `claude plugin test` (248 pruebas superadas), pytest (91) y una instalación real desde la copia de trabajo:

- **Instalación limpia:** con el catálogo de GreenSock añadido antes, `sf` se instala con sus tres dependencias, todas activas.
- **Sin el catálogo de GreenSock:** `sf` se instala, pero **no carga** («Dependency "gsap-skills@gsap-skills" is not installed»). Al añadir el catálogo, la dependencia se instala sola.
- **Las skills de three.js:** con `source` `github`, la lista `skills` se suma a la carpeta `skills/` y se cargaban las 13. Con `git-subdir`, solo las diez (unos 790 tokens fijos por sesión).
- **Tokens fijos por sesión:** `oklch-skill`, unos 80; `gsap-skills`, unos 700 (8 skills); `sf`, unos 1.550.
- **Actualización:** subir `sf` a una versión que añade una dependencia, con `claude plugin update`, **no** instala la dependencia, y `sf` no carga hasta `claude plugin install <dependencia>`. Se comprobó con un catálogo local, no con el publicado en GitHub.

**Sin comprobar:**

- **El prefijo de las skills de las dependencias en una sesión real.** Hipótesis: `threejs-skills:threejs-lighting`, `gsap-skills:gsap-core`, `oklch-skill:oklch-skill`.
- **Si una sesión nueva resuelve sola las dependencias tras una actualización desde GitHub.**

## GSAP, también desde el marketplace de la SF (medida 1, 2026-11-01)

Desde el marketplace oficial de GreenSock, `sf` no cargaba si antes no se había añadido ese catálogo. Por eso `gsap-skills` pasa a ser, como three.js, una entrada del marketplace de la SF: `git-subdir` de `skills/` en `greensock/gsap-skills`, fijada al commit `aed9cfd` (su `main` el 2026-11-01). Así se eligen solo las cinco skills de ahora, sin tropezar con el `plugin.json` de su raíz. Se quita `allowCrossMarketplaceDependenciesOn`, y las tres dependencias pasan a ser `…@softwarefactory`.

**Comprobado desde cero, con una configuración desechable y sin añadir ningún catálogo ajeno:** `sf`, `gsap-skills` (5 skills, unos 440 tokens fijos por sesión), `threejs-skills` (10 skills, unos 790) y `oklch-skill` (1, unos 80) quedan activos.

## ACTUALIZAR instala las dependencias (medida 2, 2026-11-01)

El botón ACTUALIZAR del panel (`actualizarPlugin` en `plugins/sf/hooks/cola.ts`), tras `claude plugin update` y mientras aún corre la versión vieja:

- Lee las `dependencies` del `plugin.json` de la versión instalada de `sf`: la `installPath` de `installed_plugins.json`, que es la que cargará el reinicio o `/reload-plugins`.
- Instala con `claude plugin install <id> --scope <scope>` las que falten. Una dependencia ya instalada con el scope de usuario vale para todos.
- Solo después pide reiniciar o recarga. Si una falla, avisa con la orden exacta y no recarga.
- Interruptor en `.sf/proyecto.json`: `"automatizaciones": {"dependencias_al_actualizar": false}`, encendido por defecto. Es el primer interruptor de la decisión 171.
- Lee la carpeta de plugins de `CLAUDE_CONFIG_DIR` si está puesta.

**Comprobado:**

- **5 pruebas nuevas del panel:** instala las que faltan; un fallo no pide reiniciar; con la sesión por detrás, instala y después recarga; si falla, no recarga; con el interruptor apagado, no instala. En total, 254 pruebas superadas.
- **En una configuración desechable,** con un catálogo local en git:
  - La versión vieja de `sf` instalada sin dependencias.
  - `claude plugin marketplace update` y `claude plugin update` a una versión con dependencias: `sf` «failed to load».
  - La `installPath` ya apunta a la versión nueva, con sus `dependencies`.
  - Las mismas órdenes de instalación que lanza el botón dejan `sf` y sus tres dependencias activos.

**Sin comprobar:**

- **El clic real en el panel**, que necesita una sesión de Claude Code con el mod cargado. Para probarlo:
  - En una configuración desechable (`CLAUDE_CONFIG_DIR`), instalar la versión publicada actual (1.2.9, sin dependencias) desde GitHub.
  - Publicar la nueva.
  - Abrir `claude` con esa configuración en un proyecto con SF y pulsar ACTUALIZAR dos veces.
  - Comprobar `claude plugin list`.
- **La instalación desde GitHub,** que necesita publicar.

