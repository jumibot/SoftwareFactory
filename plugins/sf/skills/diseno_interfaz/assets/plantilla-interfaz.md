# Interfaz de {Proyecto}

<!-- Plantilla de la skill diseno_interfaz de la SF. Quitar los comentarios y las secciones que no hagan falta; no dejar encabezados vacíos. -->

Estado: borrador · Actualizado: {fecha} · Fuentes: especificación funcional ({ruta}), visión ({ruta}).

Esta especificación es el contrato de la interfaz. Los bocetos de `bocetos/` la ilustran; si chocan, manda este documento.

## Forma y fundamento

<!-- Escritorio, web, móvil o varias. Sistema de componentes heredado, si lo hay. Sin tecnologías ni librerías. -->

## Recorridos clave

### {Nombre del recorrido, igual que en la especificación funcional}

Protagonista: {nombre y situación concreta}.

1. {paso}
2. {paso}
3. **Momento clave:** {lo que el usuario obtiene}

Camino de fallo: {qué pasa si algo sale mal y cómo se recupera}.

## Pantallas

| Pantalla | Se llega desde | Para qué |
| --- | --- | --- |
| {nombre} | {origen} | {propósito} |

Reglas de navegación: {por ejemplo, un solo nivel de diálogos modales}.

## Estados de cada pantalla

<!-- Estados base: ideal, vacío, cargando, parcial, error, sin permiso. Añadir los propios del producto. «No aplica» con motivo. -->

### {Pantalla}

| Estado | Qué ve y qué puede hacer el usuario |
| --- | --- |
| Ideal | |
| Vacío | |
| Cargando | |
| Parcial | |
| Error | |
| Sin permiso | |

## Componentes

| Componente | Dónde | Reglas de comportamiento |
| --- | --- | --- |
| {nombre} | {pantallas} | {qué hace al pulsar, editar, fallar} |

## Interacción

- Teclado y atajos: {…}
- Foco y orden de tabulación: {…}
- Ratón o toque: {…}
- Prohibido: {…}

## Textos y tono

| Sí | No |
| --- | --- |
| «{frase real}» | «{frase a evitar}» |

## Accesibilidad mínima

- {nivel exigido y cómo se cumple en el comportamiento}

## Bocetos

- [`bocetos/{pantalla}.html`](bocetos/{pantalla}.html): {qué ilustra; secciones que lo gobiernan}. Traducción a la plataforma: {ventanas, paneles, diálogos… o rutas y componentes}.

## Criterios de aceptación

### {Nombre descriptivo del criterio}

- **Dado** {estado inicial}, **cuando** {acción}, **entonces** {resultado esperado}.

## Supuestos y preguntas abiertas

- [SUPUESTO] {…} → Pregunta: {…}
