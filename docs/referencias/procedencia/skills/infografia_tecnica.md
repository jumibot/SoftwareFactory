# Origen de la skill `infografia_tecnica`

- **Fuente:** skill global del propietario, `~/.claude/skills/infografia_tecnica/` (copiada el 2026-10-25; primer commit de la carpeta, sin cambios).
- **Motivo:** instrucción del propietario del 2026-10-25: las skills que nacen en un proyecto y pasan a uso general tienen su fuente en la SF (desde el 2026-10-27 viajan dentro del plugin `sf` y ya no se instalan en la global); la skill no lleva contenido de ningún proyecto.
- **Copia de seguridad de la global anterior:** `skills/_respaldo/infografia_tecnica_global_2026-10-25/`, sin la referencia de 750 KB, que ya está en su proyecto.

## Cambios respecto a la fuente

| Archivo | Cambio |
|---|---|
| `SKILL.md` | Mismas reglas, sin la Smart Cold Box: ejemplos neutros (ventilador, placa, batería, rejillas) en lugar de Peltier, viales, nevera, farmacia, NFC o el calendario del caso. Nueva sección «Lo propio de cada proyecto» (`docs/identidad/reglas-infografia.md`). Resueltas tres contradicciones a favor de la práctica más reciente: el detalle de la pieza va en un HUD central, no desplegado en la etiqueta ni en una columna lateral. «La skill aprende»: lo particular va a las reglas del proyecto y lo general se propone como mejora de la SF. Verificación con el modo de prueba de la plantilla y Playwright; `meta viewport` obligatoria. |
| `assets/referencia-smart-cold-box.html` | Retirado. Es idéntico (md5) a `SmartColdBox/docs/specs/vision/infografias/infografia-smart-cold-box.html` (antes en `docs/fundacion/`), que se queda en su proyecto. |
| `assets/plantilla-infografia.html` | Nuevo. Plantilla genérica con un «equipo de ejemplo» neutro y los mecanismos estándar de la skill, escrita desde cero (no es un recorte de la referencia), con la disposición de la referencia: título y capas en columna arriba a la izquierda, batería y medidor semicircular arriba a la derecha, modos y despiece abajo a la izquierda, interruptores redondos en columna abajo a la derecha. |
| `scripts/empaquetar_autonomo.py` | Sin cambios. |
| `SKILL.md` (2026-10-26) | La infografía va por defecto en `docs/specs/vision/infografias/`, con los documentos fundacionales, por decisión del propietario. |
| `scripts/comprobar_sin_red.py` | Nuevo (2026-10-26). Sale de `SmartColdBox/off2.py`, un script de una sesión anterior que comprobaba la versión autónoma sin red; ahora con argumentos, mensajes en español y código de salida. Probado con `smart-cold-box-3d.html` en Edge y WebKit: lienzo, three.js 186 y sin errores. |

Lo específico de la Smart Cold Box que salió de `SKILL.md` está en `SmartColdBox/docs/identidad/reglas-infografia.md`.

## Comprobación (2026-10-25)

- Plantilla con Playwright: Chrome instalado (SwiftShader) a 1500 × 900 y 1100 × 800, WebKit a 1300 × 800 e iPhone simulado (390 × 844). Casos: reposo, en marcha con despiece al 60 y al 100 %, corte con y sin pieza seleccionada, inglés. Sin errores de página ni scroll; capturas revisadas. Unas 60 llamadas de dibujo por fotograma con contorno (130 con el HUD central abierto).
- Versión autónoma de la plantilla (`empaquetar_autonomo.py`, 2,3 MB) con la red bloqueada en WebKit y Chrome: arranca; solo falla la fuente de Google, que cae a la del sistema.
- La infografía de la Smart Cold Box en su proyecto arranca en Chrome sin errores.
- No probado en un iPhone real ni la secuencia completa de interacciones con clics.

## Dependencias: skills de apoyo (2026-11-01)

Por las decisiones 175 y 176, las 15 skills de apoyo dejan de viajar copiadas en el plugin y pasan a ser dependencias de `sf`, que se instalan con él. Se invocan con el prefijo de su plugin.

| Dependencia | Procedencia | Cómo llega |
| --- | --- | --- |
| `threejs-skills`: `threejs-fundamentals`, `-geometry`, `-materials`, `-lighting`, `-textures`, `-animation`, `-interaction`, `-shaders`, `-postprocessing` y `-performance` | [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills), MIT, commit `0e181866f095b5f06d005133876e926515390d95` (2026-10-19), sin cambios. Escritas para three.js r186. | Una entrada del marketplace de la SF (`git-subdir` de su carpeta `skills/`, fijada a ese commit), que carga solo estas diez: el repositorio trae también `threejs-asset-pipeline`, `threejs-loaders` y `threejs-react-three-fiber`. |
| `gsap-skills`: `gsap-core`, `-timeline`, `-plugins`, `-utils` y `-performance` | Skills oficiales de GreenSock, [greensock/gsap-skills](https://github.com/greensock/gsap-skills), MIT, commit `aed9cfd3277740755f6bfc1155c7aa645403b760` (2026-04-21, su `main` el 2026-11-01), sin cambios. Las copias anteriores eran idénticas. | Una entrada del marketplace de la SF (`git-subdir` de su carpeta `skills/`, fijada a ese commit), que carga solo estas cinco: el repositorio trae también `gsap-scrolltrigger`, `gsap-react` y `gsap-frameworks`. No se usa su propio marketplace porque, sin añadirlo antes, `sf` no cargaría (decisión 176). |

No consta que estas skills se hayan usado en la práctica: las infografías de SmartColdBox no usan GSAP.

## Preguntar destino y controles; lectura por capas (2026-11-01)

Tarea 204 («Las skills de documentos HTML preguntan qué herramientas incluir»): antes de construir, se pregunta el destino de la infografía y qué controles lleva, con la recomendación primero, y la elección va a las reglas del proyecto. Se añade la lectura por capas: al abrir, lo esencial; el detalle, tras su etiqueta o su control.
