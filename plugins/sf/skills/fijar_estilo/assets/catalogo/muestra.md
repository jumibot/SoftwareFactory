---
antetitulo: Proyecto de ejemplo · Muestra del tema
lema: Así se ven los documentos // con este tema.
subtitulo: Portada, secciones, recuadros, tabla, botones y un diagrama, tal como los genera crear_documentos.
version: Versión 1.0
estado: Muestra
destino: proyecto
herramientas: recomendadas
---
# Muestra del tema

## Recuadros | Recuadros y tabla {#recuadros}

La entradilla abre cada sección, un poco más grande que el texto, y deja ver la letra de los títulos y del texto.

> **Decisión propuesta**
> Un recuadro con etiqueta, para lo que no debe pasar desapercibido.

| Pieza | Estado | Responsable |
| --- | --- | --- |
| Portada | Lista | Diseño |
| Secciones | En curso | Redacción |

> [!aviso]
> Un aviso, en el color de acento.

Y después, la decisión, sobre el color oscuro del tema:

> [!decision]
> **Decisión**
> El recuadro de decisión va sobre el color oscuro del tema.

## Diagrama | Un proceso {#diagrama}

Un diagrama de la skill diagramas, con los colores y la letra del tema.

![](muestra.diagrama)

## Tarjetas | Tarjetas con color {#tarjetas}

Tres tarjetas con color e icono y sus campos.

::: tarjetas 3

### Código {color=turquesa icono=codigo}

Estado
:   Listo

### Documento {color=naranja icono=documento}

Estado
:   En curso

### Rama {color=verde icono=rama}

Estado
:   Pendiente

:::

## Más recursos | Pregunta, código y cifra {#mas}

Una pregunta decidida, un bloque de código y una cifra destacada.

::: preguntas 1

### ¿Qué portada? {recomendada=A estado=decidida elegida=B}

Opción A
:   Clara, con el logo.

Opción B
:   Destacada, con el color del proyecto.

Recomendación
:   La A, más sobria.

Decisión
:   La B.

:::

```json
{"colores": {"primario": "#1d6fb6"}, "portada": {"forma": "oscura"}}
```

**4,5:1** contraste mínimo del texto
{: .metrica}
