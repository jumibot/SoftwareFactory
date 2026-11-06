# Guía para trabajar en la Software Factory

Este proyecto construye y evoluciona la propia SF para Claude Code. Las aplicaciones consumidoras tendrán sus propias instrucciones; este archivo no es todavía su plantilla.

## Lectura de entrada

Leer solo [Arranque de Claude en la SF](docs/arranque-claude.md): qué es este repositorio, las piezas del plugin, dónde vive cada cosa y cuándo abrir cada documento grande.

## Reglas de trabajo

- La SF se lleva exactamente igual que los demás proyectos (decisiones 297, 298 y 299).
- Este archivo no lleva nada que sea útil para los usuarios del plugin: eso va al plugin. Aquí, solo lo propio de trabajar en el repositorio de la SF, con enlaces a lo demás. Añadirlo o cambiarlo pide la autorización del propietario: la tarea que lo necesite propone el texto y espera su OK (decisión 291).
- La memoria de Claude de la SF no guarda nada que sea útil para los usuarios del plugin: eso va al plugin. Añadir, cambiar o borrar una memoria pide la autorización del propietario: Claude propone el texto y espera su OK (decisión 292).
- Mejora continua: en la SF, las mejoras son tareas y propuestas suyas, bajo la tarea permanente **Mejorar la Software Factory** del proyecto **SoftwareFactory** del kanban, cuando esté conectado. Las instrucciones directas del propietario autorizan el cambio solicitado dentro de su alcance; lo demás, como dice la metodología («Automejora durante el uso de la SF»).
- Si cambia una pieza de la SF o la forma de publicarla, actualizar [Cómo funciona la Software Factory](docs/como-funciona-la-software-factory.md); si es del panel, también [Cómo funciona el panel](docs/como-funciona-el-panel.md). Si cambia lo que hace falta para seguir desarrollando la SF (piezas, dónde vive cada cosa, cómo se trabaja aquí), se pone al día [el arranque](docs/arranque-claude.md); como este archivo, añadir o cambiar algo en él pide la autorización del propietario: se propone el texto y se espera su OK (decisión 293). Estos documentos, la metodología, la plantilla y este archivo se actualizan en su tarea «Actualizar <documento>» (los tres últimos, en una sola), de una en una y cada una con su subagente, como dice `sf:orquestacion` («Documentos compartidos»).
- Mantener coherentes la metodología y la especificación: si cambia el método, actualizar su referencia y las partes de la SF afectadas.
- Las decisiones van a [docs/decisiones/](docs/decisiones/README.md) y lo no decidido a [propuestas](docs/propuestas.md), no a `sf/`; las plantillas, al plugin (`plugins/sf/templates/`).
- Este repositorio es la fuente de la SF, no una instalación operativa: ningún proyecto usa su copia de trabajo, sino lo publicado e instalado (especificación, «El proyecto central de la SF»).
- Skills externas: las que la SF usa tal cual son dependencias del plugin, fijadas a su commit; una adaptada viaja en el plugin como propia, con su origen y lo que cambia («Skills externas: tal cual, como dependencias; adaptadas, como propias» y «Todas las skills externas actuales, como dependencias»). Las de la propuesta «Skills externas candidatas» (P18) no tienen validación práctica: no instalarlas ni adoptar una metodología completa como consecuencia de leer su listado.
- En los documentos de la SF, el propietario se nombra «propietario de la Software Factory»; las marcas «(norma del propietario, fecha)» no cambian.

El siguiente entregable se concreta con las instrucciones del propietario y el contexto disponible. Leer estos archivos no autoriza implementar todas las propuestas ni programar actividad en segundo plano.
