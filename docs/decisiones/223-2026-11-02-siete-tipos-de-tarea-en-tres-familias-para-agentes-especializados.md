# Siete tipos de tarea en tres familias, para agentes especializados

- **Origen:** SoftwareFactory, 2026-11-02. En «Tareas deliberativas: registrar decisiones y dilemas abiertos» (274) se propuso agrupar los siete tipos de tarea en familias; tras la decisión 218 (las deliberativas se tratan como documentales), el informe proponía bajar a dos familias. El propietario: «dejamos los siete tipos en tres familias. La idea es crear agentes especializados en el plugin».
- **Contexto:** los siete tipos (implementar, corregir, investigar, deliberar, diseñar, especificar, documentar) se cerraban todos como si fueran de código. Las decisiones 216 a 222 separan el manejo del repositorio de las tareas de código y de las de documentos. Con dos familias, deliberar y documentar quedaban juntas porque se manejan igual en el repositorio.
- **Decisión:** los siete tipos se agrupan en tres familias:
  - **Código:** implementar y corregir.
  - **Deliberativas:** investigar, deliberar y diseñar.
  - **Documentales:** especificar y documentar.
  Deliberativas y documentales comparten el manejo del repositorio (218, 219), pero son familias distintas porque su trabajo es distinto: las deliberativas dialogan, deciden y separan temas; las documentales escriben un documento acordado. La razón de mantener tres es que cada familia tenga en el plugin su propio agente especializado.
- **Consecuencias:** el plugin tendrá un agente (subagente) por familia, con su encargo, sus herramientas y sus skills; el principal lanza el de la familia de la tarea. `cola.py` y el panel distinguen la familia por el tipo. Cómo son esos agentes queda para su propia tarea.
- **Aplicada en:** pendiente; en la 274 (la agrupación) y en una tarea por crear para los agentes especializados.
