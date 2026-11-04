---
name: comprobar_instalacion
description: Comprueba la instalación de la Software Factory (SF) en este equipo y la arregla con el OK del usuario — el catálogo softwarefactory (jumibot/SoftwareFactory), el plugin sf@softwarefactory y sus tres dependencias (gsap-skills, threejs-skills, oklch-skill), que estén instalados, activos y en la versión publicada, y los requisitos (git con nombre y correo, gh con la sesión iniciada, Python 3.9 o posterior). Claude lanza las órdenes, lee su salida, dice en pocas líneas qué está bien y qué falta, y propone el arreglo con un menú. Úsala cuando pidan comprobar, revisar, diagnosticar o reparar la instalación de la SF o del plugin sf, cuando el panel de la SF no salga, cuando /plugin dé sf como «failed to load», o tras instalar la SF por primera vez.
---

# Comprobar la instalación de la SF

La instalación la comprueba Claude, no el usuario («La instalación la comprueba y la diagnostica Claude», 244). El usuario solo la pide, por ejemplo «comprueba la instalación de la SF», y da el OK a lo que se arregla. No tiene que leer la salida de ninguna orden.

**Una operación, sin tarea.** No se anota en la cola ni crea rama: se hace desde la línea de prompts, con mensajes cortos y un menú (la herramienta de preguntas con opciones) para el OK.

**Lo global, con su OK.** Instalar, activar o actualizar plugins y cambiar la configuración global de git afectan a todos los proyectos del equipo. Se proponen y se hacen solo con el OK del usuario, una vez dicho qué cambia.

**Si esta skill no está.** Si `sf` no carga, sus skills no existen y Claude no tiene esta guía. La portada de la SF pide entonces la comprobación con una frase que basta sin ella: catálogo, `sf@softwarefactory` y dependencias, con `claude plugin list`, y el arreglo con OK. Se sigue la misma lógica de abajo.

## Qué se mira

Se lanzan las órdenes sin preguntar, porque solo leen:

1. **El catálogo:** `claude plugin marketplace list`. Debe estar `softwarefactory`, con origen `jumibot/SoftwareFactory`.
2. **Los plugins:** `claude plugin list`. Deben estar `sf@softwarefactory`, `gsap-skills@softwarefactory`, `threejs-skills@softwarefactory` y `oklch-skill@softwarefactory`, los cuatro activos («enabled»). Si `sf` sale como «failed to load», el motivo suele nombrar la primera dependencia que falta.
3. **La versión:** `python -I -X utf8 <plugin>/tools/plugin_sf.py ver` compara la versión de `sf` que corre, la instalada y la publicada (el último tag `vX.Y.Z` del catálogo) y da el estado: `al_dia`, `actualizar`, `refrescar` (instalada más nueva que la que corre), `sin_instalar` o `desconocido` (sin red). La misma comprobación hace `sf:incorporar_proyecto_a_sf` antes de nada. Si `sf` no carga, no hay `<plugin>`: se compara la versión de `sf` que da `claude plugin list` con el último tag de `git ls-remote --tags https://github.com/jumibot/SoftwareFactory.git`.
4. **Los requisitos:** `git config user.name` y `git config user.email` con valor; `gh auth status` con la sesión iniciada; y `python3 --version`, `python --version` o `py --version` con 3.9 o posterior (basta uno).

## Qué se dice

En pocas líneas: qué está bien y qué falta, sin copiar la salida de las órdenes. Si todo está bien, se dice en una línea y se sigue con el paso siguiente: abrir Claude Code en la carpeta del proyecto y pedir «incorpora este proyecto a la SF».

## Cómo se arregla

Cada arreglo, con su orden, en un menú: «Arreglarlo» o «Dejarlo así». Con el OK, se lanza, y se vuelve a mirar lo que tocaba.

| Qué falta | Arreglo |
| --- | --- |
| El catálogo | `claude plugin marketplace add jumibot/SoftwareFactory` |
| `sf` | `claude plugin install sf@softwarefactory --scope user`, que trae solas sus dependencias. No se instalan las dependencias a mano antes. |
| Una dependencia, con `sf` ya instalado | `claude plugin install <dependencia>@softwarefactory --scope user`, una orden por dependencia: `claude plugin install` instala solo el primer plugin que se le da. |
| Un plugin desactivado | `claude plugin enable <plugin>@softwarefactory` |
| `sf` en una versión vieja | `plugin_sf.py actualizar`: refresca el catálogo, actualiza `sf` en cada scope atrasado e instala las dependencias nuevas que falten. Sin `sf` cargado, `claude plugin marketplace update softwarefactory` y después `claude plugin update sf@softwarefactory`. |
| «Filename too long» al clonar, en Windows | `git config --global core.longpaths true`, y se repite la orden que falló. |
| «Permission denied (publickey)» al clonar | Una dependencia se clona por SSH: la SF publicada las trae por HTTPS, así que se actualiza el catálogo y se repite. |
| git sin nombre o correo | Se piden al usuario y se ponen con `git config --global user.name` y `user.email`. |
| `gh` sin instalar o sin sesión | Se dice cómo instalarlo (https://cli.github.com/) y que haga `gh auth login`. Lo hace el usuario: pide su cuenta. |
| Python que falta o es viejo | En macOS, `xcode-select --install` o `brew install python`; en Windows, desde python.org. Lo instala el usuario. |

## Al terminar

Si se ha instalado, activado o actualizado algo, los cambios entran al reiniciar: se pide en una línea, con la orden en la suya, «Sal con `/exit` y vuelve a abrir Claude Code». Si solo ha cambiado la versión de `sf`, basta `/reload-plugins`. Al volver, el panel de la SF da la bienvenida en una carpeta sin SF.

Si algo de la SF falla, sobra o falta durante la comprobación, se dice en una línea que es de la SF. Llevarlo a ella es cosa del propietario de la SF.
