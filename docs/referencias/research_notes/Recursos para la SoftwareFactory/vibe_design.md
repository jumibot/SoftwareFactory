# Vibe design y prototipado de interfaces con IA: herramientas, prácticas y paso a implementación (a 2026-10-26)

Notas de investigación. Fecha de consulta de todas las fuentes: 2026-10-26. Cuando la página no muestra fecha se indica «sin fecha». Se distingue lo **verificado** (documentación oficial) de lo **secundario/opinión** (blogs, foros, proveedores sobre competidores).

## 1. Claude Design: qué es oficialmente, funciones y límites

### Takeaway
Claude Design es un producto de Anthropic Labs (lanzado el 17-04-2026 como research preview) que ya no vive solo en claude.ai/design: ahora funciona dentro de cualquier conversación, en la pestaña Artifacts y en Claude Code (`/design`, `/design-sync`). El sitio independiente cierra el 14-12-2026. Ofrece lienzo con artboards, sistemas de diseño importados de código, ajustes en vivo, comentarios, exportaciones y handoff a Claude Code. El formato interno del bundle de handoff no está documentado.

### Cited Findings
**Verificado (Anthropic):**
- Lanzamiento el 17-04-2026, Anthropic Labs, research preview, con Claude Opus 4.7: «lets you collaborate with Claude to create polished visual work» (diseños, prototipos, slides, one-pagers). En el onboarding Claude construye un design system a partir del código y los archivos de diseño; se pueden tener varios. Exportación: URL interna, carpeta, Canva, PDF, PPTX, HTML independiente. «Handoff bundle that you can pass to Claude Code with a single instruction». Ajustes en vivo (knobs/sliders creados por Claude para espaciado, color, layout), comentarios en línea, edición directa de texto. Entradas: prompt, DOCX/PPTX/XLSX, codebase — [Anthropic, «Introducing Claude Design by Anthropic Labs», 17-04-2026](https://www.anthropic.com/news/claude-design-anthropic-labs)
- Estado actual (artículo de ayuda «Updated this week», sin fecha exacta): disponible en Free, Pro, Max, Team y Enterprise; Enterprise activado por defecto el 15-10-2026 (Organization settings > Artifacts). **claude.ai/design cierra el 14-12-2026**; los proyectos migran a Claude y los design systems deben migrarse antes. Funciona en conversaciones, en la pestaña Artifacts y en Claude Code (`/design`, `/design-sync`); en iOS/Android se puede crear y editar — [Claude Help Center, «Get started with Claude Design»](https://support.claude.com/en/articles/14604416-get-started-with-claude-design)
- Mismo artículo: design systems importables desde repo de GitHub, archivos de diseño, subidas o codebase local vía `/design-sync`; «Claude checks its output against the system before showing it». Refinado por chat (incluidas revisiones de accesibilidad), comentarios en línea y edición directa en el lienzo (arrastrar, redimensionar, alinear). **Sin historial de versiones integrado** (se pide a Claude que guarde el estado). Exportación: .zip, PDF, PPTX, Google Slides, HTML independiente; integraciones con Adobe, Base44, Canva, Gamma, HubSpot, Hyperframes, Lovable, Miro, Netlify, Replit, v0, Vercel, Wix; **Handoff to Claude Code** a un agente local o a Claude Code Web. Uso compartido con el mismo cupo que Claude y Claude Code — [Claude Help Center](https://support.claude.com/en/articles/14604416-get-started-with-claude-design)
- Limitaciones conocidas documentadas: comentarios que desaparecen, lag con codebases muy grandes («link them from Claude Code instead»), edición simultánea multiusuario básica y poco fiable, «Design system import quality depends on the source» — [Claude Help Center](https://support.claude.com/en/articles/14604416-get-started-with-claude-design)
- Página de producto: import desde GitHub, archivos de diseño o codebase local; exporta PPTX, PDF, HTML; handoff a Claude Code o `/design-sync` y `/design`; apps conectadas Adobe, Canva, Gamma, Lovable, Miro, Replit, Vercel, Wix; enlace privado por defecto; migración de design systems con banner y opción «Let Claude clean it up» (guía, tokens, componentes) — [claude.com/product/design](https://claude.com/product/design) (sin fecha)
- Comandos de Claude Code (doc oficial): `/design [brief]` es una skill incluida que dibuja maquetas, flujos, landings o pósters como artboards en un lienzo, publicado como artifact de Claude Design; se edita en navegador de escritorio con guardado automático; cada artboard exporta a PNG o PDF; requiere Claude Code ≥ v2.1.265 y artifacts disponibles; no disponible en Bedrock, Google Cloud, Foundry ni Claude Platform on AWS — [Claude Code Docs, Commands](https://code.claude.com/docs/en/commands) (sin fecha)
- `/design-sync [hint]`: «Convert your repo's React design system and upload it to Claude Design, so designs it produces use your real components»; la primera sincronización verifica cada componente y puede tardar horas en un repo grande; sube al sitio independiente claude.ai/design que cierra el 14-12-2026. `/design-login` autoriza el acceso; `/design consent` / `/design revoke` conceden o retiran acceso — [Claude Code Docs, Commands](https://code.claude.com/docs/en/commands)
- Tutorial oficial de prototipos/UX: pedir explícitamente pantallas clicables; alternativas en artboards separados; recorridos paso a paso; pedir estados vacío, error y carga y casos de pocos/muchos datos; duplicar antes de cambios grandes. Para usar componentes propios: design system (recomendado) o trabajar desde Claude Code en el repo. Handoff: si se diseñó en Claude Code, seguir en la misma sesión y pedir que lo construya; si no, dar acceso de edición y pegar el enlace en Claude Code; **nombrar bien artboards y componentes porque Claude Code lee esos nombres**; anotar decisiones y razones en notas del artboard. Avisos: Claude puede carecer de datos reales (precios) y suponerlos; sin los componentes reales «dibuja su propia versión» parecida; un design system sincronizado desde código es una copia de la última sincronización y puede quedar desactualizado — [Claude Academy, «Using Claude Design for prototypes and UX»](https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux) (sin fecha)
- Guía de administración: Labs release sin audit logs ni usage tracking — [Claude Help Center, admin guide](https://support.claude.com/en/articles/14604406-claude-design-admin-guide-for-team-and-enterprise-plans) (vía resultado de búsqueda, no leída completa)

**Secundario/opinión:**
- Anthropic no ha publicado el formato interno del bundle de handoff; el autor no sabe si son metadatos, archivos o prompts. Riesgos: el lienzo puede omitir estados vacíos/errores y hacer que las omisiones parezcan intencionadas; mapeos de componentes plausibles pero erróneos; tokens obsoletos; el bundle «lands in a vacuum» sin skills ni CLAUDE.md en el repo; cita una prueba de PCWorld que consumió gran parte del cupo semanal Pro en ~30 min — [Ready Solutions AI, «Claude Design: The Handoff Is the Feature», 24-04-2026, act. 31-05-2026](https://readysolutions.ai/blog/2026-04-24-claude-design-handoff-not-canvas/)
- `/design-sync` bidireccional anunciado el 17-06-2026 según @ClaudeDevs (secundario); solo React (paquete con dist/ o Storybook), no Vue/Angular/Svelte (afirmación de sitio de tips, sin confirmar) — [Pasquale Pillitteri](https://pasqualepillitteri.it/en/news/5308/claude-code-claude-design-two-way-sync-design-sync); [wmedia.es](https://wmedia.es/en/tips/claude-code-design-sync-your-components); [Serverworks blog (JA)](https://blog.serverworks.co.jp/claude-design-sync)
- Issue: `/design-sync` no reconocido en Claude Code 2.1.195 — [GitHub anthropics/claude-code #71738](https://github.com/anthropics/claude-code/issues/71738)

### Inferences
- «DesignSync» existe y está documentado como `/design-sync`, pero solo para design systems **React**; no aplica directamente a Tkinter ni a móvil nativo. Para esos productos, el canal útil es `/design` en Claude Code y el handoff, no la sincronización de componentes.
- Como no hay historial de versiones integrado, versionar en el repo los HTML exportados por pantalla y su manifiesto (lo que el propietario ya hace con `.dc.html` + `canvas.json`) cubre un hueco real del producto. El formato `.dc.html` no aparece en la documentación consultada: probablemente sea un formato de exportación del propio proyecto o no documentado.
- El aviso «do not ship that pipeline» del handoff que recibió el propietario encaja con el posicionamiento oficial (prototipo, no producción), pero no encontré ese texto en documentación pública.
- El cierre del 14-12-2026 afecta a cualquier flujo de la SF que dependa de `/design-sync` o `/design-login` contra claude.ai/design.

### Gaps
- Contenido exacto del bundle de handoff (README, stack recomendado, panel de tweaks): no documentado públicamente.
- No leí el artículo de migración (support.claude.com/en/articles/17440474); no sé si `/design-sync` tendrá destino tras el cierre.
- Página de artifacts de Claude Code (`artifacts.md#draft-a-design-canvas`) no consultada.

## 2. Otras herramientas de vibe design y sus opciones de exportación/handoff

### Takeaway
Todas generan prototipos rápidos; difieren en el puente al código: Figma (MCP oficial con lectura y escritura del lienzo, Code Connect), Stitch (MCP, DESIGN.md, exportación HTML/React), v0 (React/shadcn), Lovable (sincronización con GitHub), Magic Patterns (tokens y componentes propios). La mayoría de comparativas son de proveedores o blogs; no hay pruebas independientes de calidad de exportación.

### Cited Findings
**Verificado (oficial):**
- Figma MCP server: lleva contexto de diseño (variables, componentes, layout) al IDE para generar código a partir de frames, y escribe contenido nativo en Figma Design, FigJam y Slides; soporta Code Connect, recursos de FigJam y Make, Figma Specs. Remoto recomendado (`https://mcp.figma.com/mcp`); el de escritorio requiere Dev o Full seat en plan de pago. Escribir en el lienzo: servidor remoto y Full seat, gratis en beta, luego por uso. Claude Code soporta remoto, escritorio, escritura y plugin/skills — [Figma Developer Docs, Figma MCP server](https://developers.figma.com/docs/figma-mcp-server/) (sin fecha)
- Qt publicó dos skills agénticas para Figma: una extrae tokens a singletons QML y otra genera controles Qt con esos tokens, vía Figma MCP, para Qt 6 Quick — [Qt blog, «Introducing the agentic Figma design extraction skills»](https://www.qt.io/blog/introducing-the-agentic-figma-design-extraction-skills) (fecha no comprobada)

**Secundario/opinión:**
- Instalación de Figma en Claude Code: `claude plugin install figma@claude-plugins-official` (MCP + skills) — [Builder.io, Figma MCP server](https://www.builder.io/blog/figma-mcp-server) (vía búsqueda; sin verificar en doc de Figma)
- Figma Make: la sincronización con GitHub es de una sola dirección (petición de bidireccional en nov-2025) y hubo imágenes rotas tras exportar a GitHub (informes nov-2025 a feb-2026) — [Figma Forum, sync from GitHub](https://forum.figma.com/suggest-a-feature-11/sync-from-github-the-figma-make-47169); [Figma Forum, images broken](https://forum.figma.com/report-a-problem-6/after-exporting-the-project-from-figma-make-to-github-the-images-are-broken-46916)
- Figma Make: código no pensado para usarse tal cual por un equipo; aloja en figma.site. Lovable: exportación a GitHub y vuelta. v0: React con shadcn/ui, inserción en codebase existente. Magic Patterns: tokens y librería propios, exporta React/HTML/Tailwind e importa de Figma o Storybook (fuente: el propio Magic Patterns) — [Banani, alternativas a Figma Make, 2026](https://banani.co/blog/best-figma-make-ai-alternatives); [Magic Patterns blog](https://www.magicpatterns.com/blog/best-ai-design-tools); [salesdorado.com](https://salesdorado.com/en/?p=71166)
- Google Stitch: revisión grande el 19-03-2026 (lienzo infinito, agente de diseño, integración con Claude Code por MCP); DESIGN.md (18-03-2026) como archivo portable de reglas de diseño para agentes; exporta HTML/CSS/React, pegar en Figma, Firebase Studio; endpoint MCP `stitch.googleapis.com/mcp` con autenticación Google que Claude Code no soporta de forma nativa (requiere envoltorio de terceros); existe `stitch-skills` oficial — [Pasquale Pillitteri, Stitch MCP](https://pasqualepillitteri.it/en/news/647/google-stitch-mcp-export-claude-code-design-to-code); [glama.ai](https://glama.ai/mcp/servers/mo4l17vefb); [MindStudio](https://www.mindstudio.ai/blog/google-stitch-mcp-coding-agents/); codelab oficial: [Google Codelabs, Design-to-Code with Antigravity and Stitch MCP](https://codelabs.developers.google.com/design-to-code-with-antigravity-stitch)
- Calidad de «Paste to Figma» de Stitch: componentes desordenados que requieren limpieza — [digitiz.fr](https://digitiz.fr/google-stitch/) (opinión)
- Tkinter Designer convierte frames de Figma en código Tkinter vía la API de Figma (requiere nombrar capas de cierta forma) — [Tkinter Designer (índice)](https://docsearch.algolia.com/mcp/docs/repo/parthjadhav/tkinter-designer)

### Inferences
- Para la SF, solo Claude Design (vía `/design` y handoff) y Figma MCP tienen integración documentada oficialmente con Claude Code; Stitch es viable pero con autenticación de terceros.
- Ninguna herramienta documenta exportación directa a toolkits de escritorio Python; el camino más fiable es tokens + capturas/HTML como referencia y reescritura.

### Gaps
- No consulté documentación oficial de v0, Lovable, Bolt, Uizard ni Galileo (Galileo fue adquirido por Google y es la base de Stitch, según memoria, no verificado en esta investigación). Sin datos propios de Bolt ni Uizard.
- No hay comparativas independientes de calidad de código exportado.

## 3. Prácticas: prototipo primero vs especificación primero, datos reales, sincronía con contratos, tokens, accesibilidad, traducción a escritorio

### Takeaway
Las fuentes serias recomiendan decidir antes qué se quiere aprender, especificar estados y casos límite antes de generar, usar datos reales saneados o sintéticos, prototipar con los componentes que se van a enviar y tratar el prototipo como instrumento de decisión, no como código. La traducción web→escritorio pasa por tokens, no por el código.

### Cited Findings
- NN/g: definir el objetivo de investigación; tomar decisiones de diseño primero (layout, jerarquía, interacciones, estados vacío/error); usar datos reales saneados o sintéticos, nunca PII, y revisar cómo usa los datos el proveedor; prompt detallado en Markdown con datos adjuntos; iterar y hacer piloto — [Megan Chan, NN/g, «Test Earlier with AI», 11-09-2026](https://nngroup.com/articles/test-earlier-with-ai)
- Intercom: «make the prototype experience as realistic as possible by choosing a simple visual design but employing actual data» — [Intercom on Product](https://www.intercom.com/blog/videos/intercom-on-product-designing-product-with-ai) (sin fecha comprobada)
- Anthropic: pedir estados vacío/error/carga y volúmenes extremos de datos; nombrar artboards; anotar decisiones; re-sincronizar el design system tras publicar la librería — [Claude Academy](https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux)
- Anthropic: Claude Design admite pedir revisiones de accesibilidad por chat y comprueba la salida contra el design system — [Claude Help Center](https://support.claude.com/en/articles/14604416-get-started-with-claude-design)
- UXPin: la deriva de diseño la causan los pasos de traducción (maqueta estática → reconstrucción), variantes sin control y overrides de tokens; recomienda prototipar con los mismos componentes que se envían — [UXPin](https://www.uxpin.com/studio/?p=58097) (proveedor)
- Framna: usar vibe coding cuando hay incertidumbre de viabilidad o interacción; sesiones de 1-2 h; reiniciar si varios prompts no aclaran; separar prototipos de aprendizaje de sistemas de producción; reconstruir deliberadamente — [Peter Gerdes, Framna, «Not every prototype deserves to survive»](https://framna.com/insights/not-every-prototype-deserves-to-survive) (sin fecha)
- Tokens multiplataforma: Figma to Qt convierte variables en un módulo QML `DesignTokens` — [Qt Docs, Convert variables into design tokens](https://doc-snapshots.qt.io/figmatoqt/figmatoqt-how-to-variables.html)

### Inferences
- La práctica del propietario (datos de pantalla generados por scripts desde el contrato real) coincide con la recomendación de datos reales/sintéticos de NN/g e Intercom y además evita deriva de contrato; no encontré fuentes que describan esa automatización concreta.
- Para Tkinter, lo transferible del prototipo web son tokens (color, tipografía, espaciado), jerarquía, estados y textos; conviene extraerlos a un archivo neutro de tokens y no reutilizar HTML/CSS.

### Gaps
- No encontré fuentes sobre traducción de prototipos HTML a Tkinter con IA ni sobre comprobaciones de accesibilidad automatizadas en estas herramientas más allá de la mención de Anthropic.
- Ninguna fuente compara empíricamente prototipo-primero frente a especificación-primero.

## 4. Riesgos: prototipos que parecen terminados, código de prototipo que llega a producción, deriva de diseño

### Takeaway
El riesgo más citado es la «trampa de fidelidad»: el prototipo pulido se toma por producto o por decisión. Le siguen la reutilización del código generado sin reingeniería (seguridad, arquitectura por acumulación) y la deriva entre maqueta y código cuando se reconstruye a mano.

### Cited Findings
- NN/g: «fidelity trap»: un prototipo pulido lleva a suponer que está listo; la salida puede parecer completa con patrones o jerarquías erróneos; la IA rellena huecos sin juicio; revisión experta antes de avanzar — [NN/g, 11-09-2026](https://nngroup.com/articles/test-earlier-with-ai)
- Framna: el prototipo puede parecer terminado sin arquitectura, seguridad ni mantenibilidad; «Vibe Wall»: cuando hay que depurar el código generado, ya se está haciendo ingeniería — [Framna](https://framna.com/insights/not-every-prototype-deserves-to-survive)
- Ready Solutions: el artefacto puede hacer que las omisiones (estados vacíos, errores) parezcan intencionadas — [Ready Solutions AI, 24-04-2026](https://readysolutions.ai/blog/2026-04-24-claude-design-handoff-not-canvas/)
- Anthropic: sin componentes reales, Claude dibuja una versión que solo se parece al producto; el design system sincronizado puede quedar desactualizado — [Claude Academy](https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux)
- Seguridad (dato de segunda mano): benchmark de dic-2025 con un 61 % de soluciones correctas pero solo un 10,5 % seguras; escaneo de Escape.tech (oct-2025) con más de 2.000 vulnerabilidades en apps vibe-coded; caso RLS de Lovable — [GoodBarber blog](https://www.goodbarber.com/blog/vibe-coding-is-magic-in-the-demo-is-your-app-really-production-ready-a1558/) (proveedor; cifras no verificadas en fuente primaria)
- Opinión de diseñadores: el vibe coding erosiona la autoridad del diseño y hace que los prototipos se traten como decisiones — [UX Collective, «Vibe coding is accelerating the erosion of design authority»](https://uxdesign.cc/vibe-coding-is-accelerating-the-erosion-of-design-authority-4dc21b233606); saltarse la revisión de diseño da resultados genéricos — [UX Planet, «Vibe coding makes you a bad designer»](https://uxplanet.org/vibe-coding-makes-you-a-bad-designer-a2e557635652) (solo para miembros, leído vía resumen)
- Sistemas de diseño como freno a la deriva — [Supernova blog](https://www.supernova.io/blog/from-prototype-to-product-how-design-systems-prevent-the-vibe-coding-pitfalls) (proveedor)

### Inferences
- La SF debería marcar visualmente los prototipos como tales y separar «decisión aprendida» de «artefacto», y exigir reconstrucción en el stack real, lo que coincide con el «do not ship that pipeline» del handoff del propietario.

### Gaps
- Testimonios directos de primera mano escasos; la mayoría son ensayos o blogs de proveedores.

## 5. Skills y MCP que conectan herramientas de diseño con Claude Code

### Takeaway
Hay cuatro vías con respaldo oficial o cuasioficial: las skills incluidas `/design` y `/design-sync` (Anthropic), el Figma MCP con plugin/skills (Figma), la skill `frontend-design` (Anthropic, repo anthropics/skills) y el MCP de Stitch (Google, con autenticación de terceros en Claude Code). Hay también skills de proveedores de toolkits (Qt).

### Cited Findings
- `/design`, `/design-sync`, `/design-login`, `/design consent` — [Claude Code Docs, Commands](https://code.claude.com/docs/en/commands)
- Mención de una «Claude Design MCP integration» en el testimonio de Replit, sin detalles; un artículo de ayuda anterior mencionaba conectar el MCP de Claude Design desde la terminal (vía resultado de búsqueda, no presente en la versión actual leída) — [claude.com/product/design](https://claude.com/product/design); [Claude Help Center](https://support.claude.com/en/articles/14604416-get-started-with-claude-design)
- Figma MCP (remoto/escritorio, escritura en lienzo, Code Connect, soporte de plugin/skills en Claude Code) — [Figma Developer Docs](https://developers.figma.com/docs/figma-mcp-server/)
- `frontend-design`: skill oficial en `anthropics/skills/skills/frontend-design` (Apache 2.0) que fija una dirección visual deliberada antes de escribir UI; instalable con `npx skills add https://github.com/anthropics/skills --skill frontend-design` o como plugin `frontend-design@claude-code-plugins` — [GitHub anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design) (no leí el SKILL.md; datos vía [claudelog](https://claudelog.com/faqs/what-is-frontend-design-skill-in-claude-code/)). Nota: en este entorno ya aparece instalada como `frontend-design:frontend-design`.
- Qt: skills agénticas de extracción de diseño desde Figma — [Qt blog](https://www.qt.io/blog/introducing-the-agentic-figma-design-extraction-skills)
- Stitch MCP y `stitch-skills` — [glama.ai](https://glama.ai/mcp/servers/mo4l17vefb); [Google Codelabs](https://codelabs.developers.google.com/design-to-code-with-antigravity-stitch)

### Inferences
- Para la SF, la integración nativa (`/design` + handoff) no necesita MCP externos; Figma MCP solo compensa si el propietario usa Figma. Según las reglas del proyecto, todas las skills externas siguen siendo candidatas sin validar.

### Gaps
- No verifiqué si existe un MCP oficial y documentado de Claude Design aparte de los comandos de Claude Code.
- No leí el SKILL.md de `frontend-design` ni la documentación de las skills de Figma.
