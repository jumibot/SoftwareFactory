"""Conversor de cabecera: pone al día la cabecera de un .md al migrarlo al generador único.

    python convertir_cabecera.py <documento>.md [--comprobar]

- Los comentarios de opciones del principio de la visión («<!-- destino: … -->», «<!-- herramientas: … -->») pasan a
  la cabecera «---».
- Quita de la cabecera las claves que fijan el aspecto (portada, tema, logo): el aspecto es del estilo del proyecto
  (decisión 318). Las de la lectura (destino, herramientas, menu) se quedan: cada documento fija cómo se lee.

El contenido no se toca. Escribe el .md en su sitio y dice qué ha cambiado; antes, como en cualquier vuelta, se respalda
(scripts/respaldar.py). Con --comprobar solo dice qué cambiaría, sin escribir, y sale con 1 si hay algo que cambiar.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ASPECTO = ("portada", "tema", "logo")
COMENTARIO = re.compile(r"<!--\s*(destino|herramientas)\s*:\s*(.*?)\s*-->[ \t]*\n?")


def convertir(texto: str) -> tuple[str, list[str]]:
    cambios = []
    m = re.match(r"---\s*\n(.*?)\n---\s*\n", texto, re.S)
    lineas, cuerpo = (m.group(1).splitlines(), texto[m.end():]) if m else ([], texto)
    # Comentarios de opciones antes del título «# …».
    titulo = re.search(r"^#\s", cuerpo, re.M)
    previo = cuerpo[:titulo.start()] if titulo else cuerpo
    claves = {ln.split(":", 1)[0].strip().lower() for ln in lineas if ":" in ln}
    for c in COMENTARIO.finditer(previo):
        clave, valor = c.group(1), c.group(2)
        if clave in claves:
            cambios.append(f"quitado el comentario «{clave}»: ya está en la cabecera")
        else:
            lineas.append(f"{clave}: {valor}")
            claves.add(clave)
            cambios.append(f"«{clave}: {valor}» pasa del comentario a la cabecera")
    if titulo:
        cuerpo = COMENTARIO.sub("", previo).lstrip("\n") + cuerpo[titulo.start():]
    # Claves del aspecto.
    quedan = []
    for ln in lineas:
        clave = ln.split(":", 1)[0].strip().lower() if ":" in ln else ""
        if clave in ASPECTO:
            cambios.append(f"quitada «{ln.strip()}»: el aspecto lo fija el estilo del proyecto")
        else:
            quedan.append(ln)
    if not cambios:
        return texto, []
    cabecera = "---\n" + "\n".join(quedan) + "\n---\n" if quedan else ""
    return cabecera + cuerpo, cambios


def main():
    ap = argparse.ArgumentParser(description="Pone al día la cabecera de un .md al migrarlo al generador único")
    ap.add_argument("md")
    ap.add_argument("--comprobar", action="store_true", help="solo dice qué cambiaría, sin escribir")
    args = ap.parse_args()
    ruta = Path(args.md)
    if not ruta.is_file():
        sys.exit(f"No encuentro {ruta}")
    texto = ruta.read_text(encoding="utf-8")
    nuevo, cambios = convertir(texto)
    if not cambios:
        print(f"{ruta}: la cabecera ya está al día.")
        return 0
    print(f"{ruta}:\n  " + "\n  ".join(cambios))
    if args.comprobar:
        return 1
    ruta.write_bytes(nuevo.encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
