# Un solo plugin, `sf`, con las skills y activado para el usuario

- **Origen:** SoftwareFactory, 2026-10-27. El propietario preguntó cómo usar en cada proyecto lo que se crea en la SF. Después: «mete el mod en el plugin de sf. Crea un plugin para sf, de momento solo con el mod»; «mete también las skills en el plugin sf y desinstalas del global. Creo que puedes activar el plugin globalmente y no solo por project».
- **Contexto:** las skills se copiaban a mano a `~/.claude/skills/` y el kit a `~/.claude/tools/`, sin versión. La copia global no podía llevar mods, comandos, hooks ni MCP. La instalación global se decidió el 2026-10-25 sin conocer los plugins.
- **Opciones:** copia global (la de entonces); un plugin por pieza; un solo plugin; activación por proyecto o para el usuario.
- **Decisión:** un solo plugin, `sf`, en `plugins/sf/`, listado en el catálogo `softwarefactory` del repositorio. Lleva todas las skills (propias y externas), el kit de documentos y el mod de estado, y llevará los comandos, hooks y el MCP de JKanban. Se instala con ámbito de usuario desde GitHub. Las copias globales se retiran.
- **Consecuencias:** las skills se invocan con el prefijo `sf:`; publicar es subir la versión, hacer push y `claude plugin update`. No hay versiones distintas por proyecto. **Sustituye** a la parte de instalación global de «Fuente de las skills en la SF…» (2026-10-25).
- **Aplicada en:** especificación, 1 y 2 («Plugin y mods de la SF»); metodología, 2; `plugins/sf/README.md`; plugin `sf` 0.2.0 y 0.3.0.
