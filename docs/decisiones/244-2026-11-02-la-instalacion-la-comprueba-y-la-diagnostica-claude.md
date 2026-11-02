# La instalación la comprueba y la diagnostica Claude

- **Origen:** SoftwareFactory, 2026-11-02. En «Primeros cinco minutos de un usuario nuevo con la SF» (289) se preguntó qué hacer con una instalación a medias (dependencias instaladas y `sf` no). El propietario eligió comprobarlo, «pero lo compruebas todo tú y lo diagnosticas tú desde la línea de prompts».
- **Contexto:** sin `sf` cargado no hay nada de la SF que avise. Se proponía que la portada pidiera al usuario `claude plugin list`, o hacer opcionales las dependencias.
- **Decisión:** la comprobación de la instalación la hace Claude, no el usuario. La portada dice que, tras instalar, se le pida a Claude que compruebe la instalación de la SF; Claude revisa catálogo, `sf` y dependencias, diagnostica lo que falte y lo arregla con el OK. Se quita además el recuadro antiguo de actualizar desde la 1.2.10 del README del plugin.
- **Consecuencias:** las dependencias siguen siendo obligatorias. El usuario no tiene que leer la salida de `claude plugin list`.
- **Aplicada en:** la 289.
