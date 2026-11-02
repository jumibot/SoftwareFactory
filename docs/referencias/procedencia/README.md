# Procedencia de las piezas del plugin

De dónde viene cada skill y cada herramienta del plugin `sf`, qué se tomó de otros, qué se cambió y por qué, con las decisiones del propietario que la fueron formando. Es historia de la SF: vive en el repositorio y no viaja en el plugin.

Hasta la tarea 317 (2026-11-02) cada pieza llevaba esta historia en un `ORIGIN.md` dentro del plugin. Se trasladó aquí para que el plugin publicado no lleve la historia del propietario ni los nombres de sus proyectos; los archivos conservan su historial en git (`git log --follow`).

Lo que exige la licencia de lo que es de terceros (atribución y texto de la licencia) sigue en el plugin, en [`plugins/sf/LICENCIAS-DE-TERCEROS.md`](../../../plugins/sf/LICENCIAS-DE-TERCEROS.md).

## Skills

| Skill | Procedencia |
| --- | --- |
| `configurar_proyecto` | [skills/configurar_proyecto.md](skills/configurar_proyecto.md) |
| `crear_documentos` | [skills/crear_documentos.md](skills/crear_documentos.md) |
| `definicion_tecnica` | [skills/definicion_tecnica.md](skills/definicion_tecnica.md): técnicas de BMAD Method, Spec Kit y MADR |
| `diseno_interfaz` | [skills/diseno_interfaz.md](skills/diseno_interfaz.md): técnicas de BMAD Method, Spec Kit, Superpowers y Scott Hurff |
| `documento_fundacional` | [skills/documento_fundacional.md](skills/documento_fundacional.md) |
| `documento_vision` | [skills/documento_vision.md](skills/documento_vision.md) |
| `incorporar_proyecto_a_sf` | [skills/incorporar_proyecto_a_sf.md](skills/incorporar_proyecto_a_sf.md) |
| `infografia_tecnica` | [skills/infografia_tecnica.md](skills/infografia_tecnica.md) |
| `informe_deliberativa` | [skills/informe_deliberativa.md](skills/informe_deliberativa.md) |
| `metodologia` | [skills/metodologia.md](skills/metodologia.md) |

Las skills sin archivo aquí (`flujo_tareas`, `orquestacion`) son propias de la SF y se escribieron en ella; su porqué está en las [decisiones](../../decisiones/README.md).

## Herramientas

| Herramienta | Procedencia |
| --- | --- |
| `tools/kit_documentos/` | [kit_documentos.md](kit_documentos.md) |

## Al añadir o cambiar una pieza

- La historia (qué se tomó, de qué versión, qué se cambió y por qué) se escribe aquí, en el archivo de la pieza.
- Si se toma algo de terceros, su atribución y su licencia van también a `plugins/sf/LICENCIAS-DE-TERCEROS.md`, que es lo que viaja con el plugin.
