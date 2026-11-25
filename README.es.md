<p align="center">
  <picture><source media="(prefers-color-scheme: dark)" srcset="site/img/logo-oscuro.svg"><img src="site/img/logo.svg" width="96" alt="SoftwareFactory"></picture>
</p>

<h1 align="center">Un nuevo mod para Claude Code</h1>

<p align="center">
  <b>Ve rápido con Claude Code, sin perder el control. En la terminal y en la app de escritorio.</b><br>
  Un mod se instala en Claude Code y cambia cómo trabaja, sin cambiar de herramienta. <b>SoftwareFactory</b> le añade un panel en vivo,<br>
  una cola de tareas y una forma de trabajar, para quien construye solo o con poca gente: cada petición es una tarea<br>
  con su subagente y su rama, todas avanzan en paralelo y nada se publica sin revisar los datos privados.
</p>

<p align="center">
  <a href="README.md">🇬🇧 Read in English</a> · 🇪🇸 Castellano
</p>

<p align="center">
  <a href="https://github.com/jumibot/SoftwareFactory/releases"><img alt="Última versión" src="https://img.shields.io/github/v/tag/jumibot/SoftwareFactory?label=versi%C3%B3n&color=f5c400"></a>
  <a href="LICENSE"><img alt="Licencia MIT" src="https://img.shields.io/badge/licencia-MIT-f5c400"></a>
  <img alt="Windows, macOS, Linux" src="https://img.shields.io/badge/Windows%20%C2%B7%20macOS%20%C2%B7%20Linux-555">
</p>

<p align="center">
  <a href="#instalar"><b>Instálalo con 2 órdenes</b></a> &nbsp;|&nbsp; <a href="https://jumibot.github.io/SoftwareFactory/"><b>Haz el recorrido en la web</b></a>
</p>

<p align="center">
  <img src="site/img/panel-es.svg" width="560" alt="El panel de SoftwareFactory en Claude Code: siete tareas en curso, cada una con su subagente, una lista para probar, 38 pendientes con el botón Poner en curso, 3 en observación, 124 cerradas y 12 propuestas">
</p>

## Instalar

Una sola vez por equipo:

```bash
claude plugin marketplace add jumibot/SoftwareFactory
claude plugin install sf@softwarefactory --scope user
```

Después, abre Claude Code y pídele *«Comprueba la instalación de la SF»*: Claude revisa el plugin y los requisitos y arregla lo que falte, con tu OK. Abre tu proyecto, pon la pantalla completa con `/tui fullscreen` o abre la app de escritorio, y pulsa el botón de la bienvenida.

**Necesitas** Claude Code, git, la CLI de GitHub con la sesión iniciada (`gh auth login`) y Python 3.9 o posterior. Instalar `sf` trae solas sus tres dependencias.

## No esperes. Orquesta.

Cada tarea tiene su propio subagente, trabajando en segundo plano en su propia rama. Mientras trabajan, tú sigues hablando con Claude: pides más cosas o pruebas otra tarea. Nunca esperas a que termine una para empezar la siguiente.

- Varios subagentes en paralelo, uno por tarea.
- Cada uno en su rama: no se pisan.
- El panel enseña cada paso según ocurre.

## Claude sabe en qué estás. Y no te interrumpe.

> 🅵🅾🅲🆄🆂 `Arreglar los acentos del CSV (T❹ ❼ )`
>
> Arreglado: la exportación va ahora en UTF-8 con BOM y Excel abre la ñ y la é. Lista para probar en su rama.
>
> (`ᴏꜰꜰ-ᴛᴏᴘɪᴄ` T❹ ❽ : modo oscuro listo para probar ▶️)

Cada respuesta empieza por la tarea en la que estás. Lo de otras tareas espera al final de una respuesta, en una línea breve. Una idea que surge a mitad va a la cola, no a la conversación.

> **No producir más. Pedirte menos atención.** Ese es el objetivo de SoftwareFactory: una persona lleva muchos proyectos a la vez, desarrolla, investiga, enseña y aprende, y la fábrica lleva la cuenta para que la cabeza quede libre.

## Publica sin miedo

Antes de subir nada a un repositorio público, SoftwareFactory revisa lo que sale: secretos y claves, correos, rutas de tu máquina, tu usuario y el nombre del equipo, archivos locales. **Si encuentra algo, para: no se sube nada.** Cuando está limpio, RELEASE pasa `develop` a `main`, pone el tag de la versión y lo sube, con un botón.

| Sale | No sale |
|---|---|
| ✓ tu código, tus documentos, el registro de cambios | ✕ tokens y claves (`ghp_…`, claves privadas, contraseñas en el código) |
| ✓ el tag de la versión (`v1.3.0`) en `main` | ✕ correos, tu usuario y el nombre del equipo, rutas de tu carpeta personal |
| ✓ lo que ya era público, sin volver a preguntar | ✕ `.env`, la cola local y los ajustes locales de Claude Code |

Solo cuenta lo nuevo: lo que ya era público no se vuelve a señalar, y lo que aceptas no se pregunta dos veces.

## Tu proyecto, contado como una historia

El documento de visión no enumera funciones: cuenta una historia, con un protagonista con nombre, un problema de verdad, escenas y capítulos, y cada función vista en acción en el momento en que le cambia algo a alguien. Se lee como un libro, en un lector que pasa página. Alrededor, el resto del documento lleva portada, secciones plegables, tarjetas y diagramas interactivos con los colores de tu proyecto, y se imprime en A4.

## El mismo Claude. Un día muy distinto.

| Claude Code a pelo | Con SoftwareFactory |
|---|---|
| Pides cinco cosas. Tres se pierden en el scroll. | Cada petición entra en una cola en cuanto la dices. |
| Todos los cambios se amontonan en la rama en la que estés. | Cada tarea trabaja en su rama, con su agente, todas a la vez. |
| La lista de pendientes vive en tu cabeza. | Un panel enseña lo que está en marcha, lo que espera y lo hecho. |
| Subes y cruzas los dedos para que no se cuele nada privado. | Cada publicación se revisa en busca de secretos y datos personales. |
| Cada proyecto, a preparar todo otra vez. | Cualquier proyecto queda listo tras unas pocas preguntas. |

## Qué ganas

**Ninguna idea se pierde.** Dilo en el chat, con tus palabras. Antes de empezar nada, ya está en la cola como tarea con sus pasos. TURBO pasa a Claude todas las tareas que no te necesitan.

**Tú decides. Claude trabaja.** Cada tarea tiene su propio agente y su propia rama. Nada toca tu código estable hasta que lo pruebas y das el OK. Una pendiente se pone en marcha con un clic (**Poner en curso**, en el panel); cuando está lista, otro clic la cierra en un único commit limpio.

**Todo de un vistazo, uses Claude Code donde lo uses.** El mismo panel en vivo junto al chat, en la terminal y en la app de escritorio; sin pantalla completa, una caja pequeña sobre el prompt guarda lo esencial. Cierra, descarta o revierte una tarea con un clic. Las mismas marcas en el chat y en el panel: 🟢 trabajando, 🔴 terminado y esperando, ▶️ lista para probar, 👀 en observación, 🔒 cerrada.

**Tus proyectos de siempre, sin rehacerlos.** Trae un proyecto que ya tengas, o empieza en una carpeta vacía. Unas pocas preguntas con menús y queda listo, sin mover ni renombrar tu código. ¿Sin repositorio en GitHub? La incorporación lo crea con tu OK. Tras recargar los plugins, sigue sola.

**Nada se da por hecho.** Cada cierre dice qué cambió, qué se comprobó y qué queda. Un subagente que se topa con un bloqueo lo dice; nunca lo sortea.

**Método, si lo quieres.** Con la metodología, Claude guía el proyecto de la visión y la especificación al código, en devslices pequeñas, guarda cada decisión por escrito con su porqué y escribe documentos que de verdad se leen, con diagramas interactivos.

| Ninguna idea se pierde | Publica sin miedo |
|:---:|:---:|
| <img src="site/img/request-es.svg" width="380" alt="Pides en el chat, Claude lo convierte en las tareas 47 y 48, y un subagente hace los pasos"> | <img src="site/img/publish-es.svg" width="380" alt="RELEASE revisa nueve commits nuevos, encuentra una ruta personal y bloquea la publicación hasta arreglarla"> |

<p align="center">
  <a href="https://jumibot.github.io/SoftwareFactory/"><b>Mira todas las funciones en la web</b></a>
</p>

## Más

- [Página web](https://jumibot.github.io/SoftwareFactory/): el recorrido completo, en inglés y en castellano.
- [El plugin](plugins/sf/README.md): qué contiene y cómo se publica.
- [Guía de desarrollo](DESARROLLO.md): para quien trabaja en la propia SoftwareFactory.
- [Licencias de terceros](plugins/sf/LICENCIAS-DE-TERCEROS.md).

SoftwareFactory es software libre con [licencia MIT](LICENSE).
