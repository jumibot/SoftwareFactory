# Definición técnica de {Proyecto}

<!-- Plantilla de la skill definicion_tecnica de la SF. Quitar los comentarios y las secciones que no hagan falta; no dejar encabezados vacíos. -->

Estado: borrador · Actualizado: {fecha} · Fuentes: especificación funcional ({ruta}), interfaz ({ruta}), perfil de partida ({sección de la metodología}).

## Contexto técnico

- **Lenguaje y versión:** {… o NECESITA ACLARACIÓN}
- **Dependencias principales:** {…}
- **Persistencia:** {motor, o «no aplica»}
- **Pruebas:** {herramientas}
- **Plataforma:** {sistemas y versiones}
- **Tipo de proyecto:** {escritorio, web, API, biblioteca…}
- **Rendimiento:** {objetivos del dominio, o «sin requisitos especiales»}
- **Restricciones:** {sin conexión, memoria, privacidad…}
- **Escala:** {usuarios, datos, volumen}
- **Integraciones:** {servicios externos}
- **Instalación y distribución:** {el paso único; local u *on premise*, nube…}
- **Capacidades opcionales:** {agente de IA, brain de desarrollo, KB operativa, API; solo las que el proyecto necesita}

## Perfil y excepciones

Perfil de partida: {nombre y sección de la metodología}.

| Excepción | Por qué hace falta | Alternativa más simple descartada porque |
| --- | --- | --- |
| {…} | {…} | {…} |

## Paradigma

{Nombre del paradigma} — {capa} → `{carpeta}`; {capa} → `{carpeta}`.

## Decisiones de arquitectura

<!-- Diagrama de dependencias: SVG inline, nunca ASCII ni mermaid (metodología, 6). Una capa por fila, de arriba abajo, con flecha hacia la capa de la que depende; recomendaciones de la guía metodologia/references/diagramas-svg.md del plugin sf. -->
<figure class="vertical">
<svg viewBox="0 0 560 {alto}" width="100%" role="img" aria-label="Dependencias entre capas de {proyecto}" style="font-family:var(--fuente-texto);display:block">
<!-- {una fila por capa: nombre en negrita y carpeta debajo, en gris; flecha hacia la capa de la que depende} -->
</svg>
<figcaption>{Qué hay que ver en el diagrama}</figcaption>
</figure>

### {Nombre descriptivo de la decisión}

- **A qué obliga:** {partes o funcionalidades afectadas}
- **Qué evita:** {la divergencia}
- **Regla:** {lo que debe cumplirse}
- **Porqué:** [`sf/decisiones/`, «{decisión}»]({ruta del archivo de la decisión})

## Convenciones

| Aspecto | Convención |
| --- | --- |
| Nombres (entidades, archivos, interfaces) | |
| Datos y formatos (identificadores, fechas, errores) | |
| Estado y transversales (errores, registro, configuración, permisos) | |

## Stack

Versiones verificadas el {fecha}.

| Nombre | Versión | Fuente |
| --- | --- | --- |
| {…} | {…} | {URL} |

## Estructura semilla

```text
{proyecto}/
  {carpeta}/   # {qué vive aquí}
```

## Persistencia

{Entidades principales y relaciones; motor; migraciones en `{ruta}`.}

## Capacidades opcionales

<!-- Solo las que el proyecto use. Agente de IA: contrato, credencial, agente simulado (metodología 7.4 y 7.7). Brain y KB: metodología 7.6. -->

## Instalación y operación

{Paso único de instalación, entornos, despliegue, copias de seguridad.}

## Mapa funcionalidad → componente

| Funcionalidad | Vive en | La gobierna |
| --- | --- | --- |
| {nombre de la especificación funcional} | {componente} | {decisión, convención o paradigma} |

## Aplazado

- {decisión}: {por qué puede esperar y cuándo se decide}.

## Preguntas abiertas

- {…}
