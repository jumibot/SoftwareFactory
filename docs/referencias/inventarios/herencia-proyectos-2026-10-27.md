# Lo aprendido en proyectos anteriores que no llegó a la SF

Inventario del 2026-10-27, hecho por un agente de Claude en solo lectura. Base de la propuesta «Incorporar lo aprendido en proyectos anteriores» ([propuestas](../../propuestas.md)). No es una lista de decisiones: cada entrada se revisa con el propietario.

**Proyectos revisados:**
- OncoCore: `CLAUDE.md`, `.claude/`, `skills/`, `_docs/`, `tools/` y la memoria de Claude del proyecto, en `~/.claude/projects/D--Projectes-OncoCore/memory/` (en adelante, «Mem. OncoCore»).
- OncoCore_app, PoseTracker, SmartColdBox y JKanban.
- SocratIX, LecturaFàcil y MedRol, que solo tienen memoria y `docs/`.

No existe `~/.claude/CLAUDE.md`.

**Clave:** G, general; D, propio del dominio. Estado en la SF: ausente, parcial o presente.

## A. Forma de trabajar con el propietario y con Claude

1. **Una corrección es el ejemplo de una regla.** Se aplica donde se pidió, se barre todo el artefacto en el mismo turno y al final se informa de la regla y del barrido. Mem. OncoCore `feedback_correction_as_class_example.md`. G. Parcial: solo en `documento_vision`.
2. **Exponer el riesgo antes de cada cambio:** qué se toca, si es reversible y a qué afecta. Si el riesgo es alto, esperar confirmación. Mem. OncoCore `feedback_evaluate_risk_before_changes.md`; `OncoCore/CLAUDE.md`. G. Ausente.
3. **Orden de ataque con varios cambios:** primero lo de bajo riesgo y lo determinista; lo de alto riesgo, al final. Mem. OncoCore `feedback_change_sequencing.md`. G. Ausente.
4. **Valoración honesta y crítica** de las propuestas del propietario y de las propias. Lo ya invertido no obliga a seguir. Mem. OncoCore `feedback_honest_critical_assessment.md`. G. Ausente.
5. **Afirmaciones sobre el código verificadas** contra el código o una ejecución del día. Lo no comprobado se dice. Mem. OncoCore `feedback_claims_verified_against_code.md`; SocratIX `oncocore_rigor.md`. G. Parcial.
6. **Comunicación:**
   - nombrar los códigos por lo que son, sin coordenadas históricas;
   - al depurar, primero «lugar + fallo»;
   - una hipótesis antes que una pregunta abierta.

   Fuente: `OncoCore/CLAUDE.md`, anti-patrones; Mem. OncoCore `feedback_contextualizar_codigos_y_fases.md`. G. Parcial.
7. **Comparaciones, estados y opciones, en tabla:** celdas cortas, una variable por columna. Mem. OncoCore `feedback_grid_responses.md`; memoria de JKanban `user_preferences.md`. G. Ausente.
8. **Perfil y ritmo del propietario:**
   - en castellano y con mensajes cortos;
   - «dale» significa «procede»;
   - aplicar salvo que haya ambigüedad real;
   - si detiene una herramienta, esa línea queda en pausa.

   Fuentes: memorias de SmartColdBox (`estilo-de-trabajo.md`), OncoCore (`user_jumi_profile.md`) y SocratIX. G. Ausente.
9. **Aconsejar una sesión nueva** al cerrar un bloque. Mem. OncoCore `feedback_aconsejar_sesion_nueva.md`. G. Ausente.
10. **Hábitos:**
    - plan antes de un cambio de más de dos archivos;
    - una «fase 0» reversible antes de un cambio mayor;
    - un cambio estructural por turno;
    - lista de tareas a partir de tres pasos;
    - subagentes para investigar;
    - capturar las decisiones antes de compactar.

    Fuente: `OncoCore/CLAUDE.md`. G. Ausente.
11. **Arquitecto, no programador a toda costa:** el sistema antes que el síntoma, una sola fuente de verdad, la chapuza se declara. `OncoCore/CLAUDE.md`. G. Ausente.
12. **Generalizar antes que parchear:** la lógica no ramifica por un caso concreto. `OncoCore/CLAUDE.md`. G. Ausente.

## B. Documentación, decisiones y memoria

13. **Qué va a la memoria, al `CLAUDE.md` o a una skill**, con un test para promover algo al `CLAUDE.md`, que hace el propietario. `OncoCore/CLAUDE.md`. G. Ausente.
14. **Plantilla de `CLAUDE.md` de proyecto:**
    - índice de los principios que no se negocian;
    - una «verificación rápida» por regla;
    - una tabla «cuándo leer» cada documento técnico;
    - qué skills se precargan.

    Fuentes: `OncoCore/CLAUDE.md` y la doctrina de `PoseTracker/CLAUDE.md`. El `CLAUDE.md` de SmartColdBox dice que la SF aún no tiene plantilla. G. Parcial.
15. **Documentos de diseño solo con el estado vigente.** El histórico va a las decisiones. Mem. OncoCore `feedback_docs_current_state_only.md`. G. Parcial.
16. **Los entregables van a `docs/`**, nunca solo al scratchpad. Mem. OncoCore `feedback_docs_deliverables_in_docs.md`. G. Ausente.
17. **Documento «dónde estamos» por subproyecto:** cerrado, en curso, siguiente paso, esperando decisión y bloqueos. Lleva identificadores estables y se actualiza en el mismo turno. Mem. OncoCore `feedback_subproject_recap_document.md`; `OncoCore/_docs/subproyectos/`. G. Parcial: `sf.json` y el kanban.
18. **Índice de `docs/` generado desde el árbol real**, con «cuándo leer». `OncoCore/scripts/indice_docs_html.py`. G. Ausente.
19. **Catálogo auditable antes de una modificación masiva.** `OncoCore/CLAUDE.md`. G. Ausente.
20. **Detalles de los diagramas que faltan en la guía SVG:**
    - `<title>` y `<desc>` con `aria-labelledby`;
    - semántica de color: azul determinista, ámbar parada humana, verde ratificado y rojo no pasa;
    - SVG en `img/` como alternativa al inline.

    Fuente: Mem. OncoCore `feedback_ascii_schemas_as_svg.md`. G. Presente en lo esencial; parcial en estos detalles.

## C. HTML, informes y documentos de lectura

21. **Principios de las apps HTML de lectura:**
    - autocontenidas, sin manual y sin elementos sin función;
    - una convención por gesto;
    - el contenido no salta.

    Antes de construir, una ficha de diez preguntas. Fuente: `OncoCore/skills/diseno_documentos/SKILL.md`. G. Parcial: el kit está portado; los principios y la ficha, no.
22. **Verificar HTML sin ventana:**
    - las trampas de Chrome headless;
    - probar que se ve, no que existe;
    - medir la cobertura de cada herramienta.

    Fuente: `diseno_documentos`, §3. G. Parcial: solo `infografia_tecnica`.
23. **Un documento ya repartido se actualiza; no se regenera.** El generador se niega sin `--forzar`. Fuente: `diseno_documentos`, §2b y §4. G. Parcial.
24. **Fuentes externas desde un catálogo determinista**, con instantánea fechada; traducciones validadas de forma determinista. Fuente: `diseno_documentos`, §2b. G. Ausente.
25. **Los cambios de formato de un HTML generado van al generador**, no a mano. Memoria de LecturaFàcil. G. Parcial.
26. **Informes HTML desde `.md`:**
    - plegables;
    - la trazabilidad, cerrada por defecto;
    - CSS versionado.

    Fuentes: `OncoCore/tools/operational/md_to_html/`, `skills/gestion_css/`. G. Parcial.

## D. Skills, versionado y herramientas de Claude Code

27. **Versión por skill:**
    - versión semántica;
    - copia `SKILL_vX.Y.Z.md`;
    - subida automática con un hook;
    - despliegue explícito y visible.

    Fuentes: `OncoCore/skills/gestion_skills/SKILL.md`, `OncoCore/.claude/settings.json`. G. Parcial: hay `ORIGIN.md` y la versión del plugin; el `CHANGELOG` es una propuesta.
28. **Un hook recién registrado no se carga en la sesión que lo crea.** `OncoCore/CLAUDE.md`. G. Ausente.
29. **Skills que solo se ejecutan cuando se piden** (`disable-model-invocation: true`). Mem. OncoCore `feedback_explicit_only_assets.md`. G. Ausente.
30. **Enumerar ejemplos en un `SKILL.md` solo si el conjunto es cerrado**; si no, describir el criterio. Fuente: `gestion_skills`. G. Ausente.
31. **Toda skill aprende de las correcciones:** al final, «Añadido a la skill: …» o «Nada nuevo». G. Parcial: solo `documento_vision`.
32. **Nombres:**
    - por función, no por posición;
    - el script se llama como su comando;
    - `snake_case`;
    - código en inglés y prosa en castellano.

    Fuentes: `OncoCore/CLAUDE.md`, `gestion_skills`. G. Ausente. **Choca con lo actual**: la SF usa guiones y PoseTracker, código en español. Hay que decidirlo.
33. **Línea de estado con contexto y tokens.** `OncoCore/tools/dev/statusline/statusline.py`. G. Parcial: el mod muestra la fase.

## E. Arquitectura, pruebas y agentes

34. **Determinismo antes que inferencia:** lo reproducible es una tool con JSON de entrada y de salida, y el LLM queda para lo ambiguo. Primero emitir bien el dato; el linter, solo como red. `OncoCore/CLAUDE.md`; Mem. OncoCore `feedback_base_phase_over_validation_phase.md`. G. Parcial: metodología 7.4 y 7.7.
35. **Contrato canónico para el JSON que cruza una frontera:** un productor, consumidores declarados y versión. `OncoCore/CLAUDE.md`. G. Parcial.
36. **Responsabilidad única garantizada con una prueba de guarda**, más pruebas de arquitectura y de portabilidad. Fuentes: `JKanban/tests/test_persistence_portability.py`, Mem. OncoCore. G. Ausente.
37. **Matices de MVP:**
    - `main()` como raíz de composición;
    - dependencias por constructor;
    - sin ABC hasta la segunda implementación;
    - constantes de tema en un módulo.

    Fuentes: `OncoCore/CLAUDE.md`, `PoseTracker/CLAUDE.md`. G. Parcial: metodología 7.1.
38. **Puerta humana en apps con agente:** la IA propone, una persona ratifica y el código determinista consume. El juicio de dominio codificado exige que el propietario lo reconfirme. Mem. OncoCore `project_human_gate_progression.md`. G como patrón. Ausente.
39. **Pruebas:**
    - con una base de datos real en un archivo temporal;
    - las pruebas no ejecutan SQL;
    - pruebas de humo con datos sintéticos;
    - medir antes de optimizar;
    - baterías contra el agente real, espaciadas.

    Fuentes: `JKanban/docs/testing.md`, `PoseTracker/CLAUDE.md`, Mem. OncoCore. G. Parcial.
40. **Configuración en `.ini`, secretos en `.env`.** Sin rutas absolutas de desarrollo en lo desplegado. Mem. OncoCore `feedback_config_ini.md`. G. Parcial.

## F. Git, seguridad y entorno

41. **Ramas y versiones:** `develop`, `feature/*`, `release/*` y `main` con etiquetas; `CHANGELOG` en formato Keep a Changelog; **los PR los fusiona el propietario**. Fuentes: `JKanban/CLAUDE.md`, memoria de JKanban. G. Ausente.
42. **Seguridad:**
    - escapar el contenido del usuario en `innerHTML`;
    - nada confidencial en repositorios públicos;
    - `noopener noreferrer` en los enlaces externos.

    Fuente: `JKanban/CLAUDE.md`. G. Ausente.
43. **Windows y PowerShell:** `git commit -F` con UTF-8 sin BOM; los archivos CRLF, con Edit; entornos virtuales separados para el MCP. Memoria de JKanban. G. Ausente.

## Incoherencias encontradas

- `SmartColdBox/CLAUDE.md` enlaza `SoftwareFactory/docs/metodologia/…` y `docs/mejora-continua.md`, que ya no existen, y no tiene `docs/sf.json`.
- Dos memorias antiguas de OncoCore describen una política de despliegue anterior.

## Propio de un dominio: no va a la SF

- **OncoCore:**
  - la fidelidad del vault y de la KB;
  - las reglas clínicas, los litmus y la redacción del informe molecular;
  - las skills, tools y comandos clínicos;
  - los enlaces y la terminología clínica de `diseno_documentos`;
  - la interfaz de OncoCore_app, como mucho como inspiración.
- **PoseTracker:** fuentes Hershey, MediaPipe y filtros.
- **JKanban:** los detalles de SQL portable y los fixtures.
- **SmartColdBox, MedRol y SocratAI:** sus reglas propias.
