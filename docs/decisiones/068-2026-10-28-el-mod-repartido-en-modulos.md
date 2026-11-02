# El mod, repartido en módulos

- **Origen:** SoftwareFactory, 2026-10-28, valoración de la sesión: `register.tsx` rondaba las 1.500 líneas y cada cambio visual tocaba muchos sitios. El propietario aprobó el reparto («sí, adelante»).
- **Decisión:** el mod se reparte en `register.tsx` (eventos), `panel.tsx`, `lectura.ts`, `cola.ts`, `control.ts`, `identidad.ts`, `prueba.ts`, `estilo.ts` y `constantes.ts`, moviendo el código sin reescribirlo. Dos reglas del motor: cada archivo declara los valores de estado (`atom`) que usa, y una función que recibe `$` desde otro archivo es una declaración `function`. `panel.tsx` sigue grande (unas 740 líneas); partirlo más espera a la 76, la prueba del panel en casos pequeños.
- **Aplicada en:** mod de estado; `docs/como-funciona-la-software-factory.md`; plugin `sf` 0.32.1.
