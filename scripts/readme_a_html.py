"""Genera README.html para leer el README en local con el estilo de la SF.

Los enlaces a un .md que tiene .html al lado pasan a apuntar al .html.
Uso: python -I -X utf8 scripts/readme_a_html.py
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

RAIZ = Path(__file__).resolve().parent.parent
GENERADOR = RAIZ / "plugins/sf/skills/documento_vision/scripts/doc_to_html.py"
TITULO = "Índice de la SoftwareFactory"  # el generador lo toma del nombre del archivo


def a_html(m):
    texto, destino = m.group(1), m.group(2)
    if destino.endswith(".md") and not destino.startswith(("http", "#")):
        html = destino[:-3] + ".html"
        if (RAIZ / unquote(html)).exists():
            destino = html
    return f"[{texto}]({destino})"


def adaptar(md):
    md = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", a_html, md)
    # En esta versión los enlaces ya abren los html: sobran los «html, en local» y el aviso.
    md = re.sub(r" \(\[html, en local\]\([^)]+\)\)", "", md)
    md = md.replace("..\n", ".\n")
    md = re.sub(r"\nLos enlaces abren el `\.md`[^\n]*\n", "\n", md)
    md = re.sub(r"\nLos enlaces abren los `\.md`[^\n]*\n", "\n", md)
    md = re.sub(r"\nPara leer este índice en local[^\n]*\n", "\n", md)
    # El generador no admite listas anidadas: las notas pasan a una línea con separadores.
    md = re.sub(r"- Notas:\n((?:  - [^\n]+\n)+)",
                lambda m: "- Notas: " + " · ".join(l[4:] for l in m.group(1).splitlines()) + "\n", md)
    # Ni bloques de código sangrados dentro de una lista: se sacan al nivel superior.
    md = re.sub(r"\n  ```(\w*)\n((?:  [^\n]*\n)+?)  ```\n",
                lambda m: "\n```" + m.group(1) + "\n"
                + "".join(l[2:] + "\n" for l in m.group(2).splitlines()) + "```\n", md)
    md = re.sub(r"\n  (El script encuentra[^\n]*)", r"\n\1", md)
    # Lista justo después de un párrafo: el generador necesita una línea en blanco.
    md = re.sub(r"(\S[^\n]*)\n(- )", r"\1\n\n\2", md)
    return md


def main():
    md = adaptar((RAIZ / "README.md").read_text(encoding="utf-8"))
    # Carpeta temporal dentro del repo, para que el generador encuentre la identidad.
    tmp = RAIZ / "_tmp_readme"
    tmp.mkdir(exist_ok=True)
    tmp_md = tmp / f"{TITULO}.md"
    try:
        tmp_md.write_text(md, encoding="utf-8")
        subprocess.run([sys.executable, "-I", "-X", "utf8", str(GENERADOR), str(tmp_md),
                        "--tipo", "Índice", "--destino", "proyecto", "--herramientas", "recomendadas"], check=True)
        html = tmp_md.with_suffix(".html").read_text(encoding="utf-8")
        # En un índice todas las secciones empiezan abiertas.
        html = re.sub(r'(<details id="[^"]*" class="bloque[^"]*")(?! open)>', r"\1 open>", html)
        (RAIZ / "README.html").write_text(html, encoding="utf-8")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("README.html generado")


if __name__ == "__main__":
    main()
