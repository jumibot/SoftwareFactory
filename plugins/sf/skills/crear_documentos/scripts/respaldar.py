"""Respalda un documento antes de sustituirlo por una versión nueva («Antes de sustituir un documento, se respalda en
_respaldo/», decisión 217).

    python respaldar.py <documento>.md <motivo>

Copia el .md, y su .html si lo tiene, a la subcarpeta _respaldo/ de la misma carpeta, como
<nombre>_antes-<motivo>.<ext>. El motivo son una o dos palabras de lo que cambia la versión nueva («rediseno»,
«sin-mapa»). Volver atrás es copiar de vuelta la versión respaldada, sin tocar git.

Si ya hay un respaldo con ese nombre, se detiene sin tocar nada: qué hacer con dos vueltas del mismo motivo está por
decidir (pregunta 10 del informe «Tipos de tarea», en la tarea 297); mientras tanto, se elige otro motivo.
"""
import re
import shutil
import sys
import unicodedata
from pathlib import Path


def motivo_limpio(texto: str) -> str:
    t = unicodedata.normalize("NFD", texto.strip().lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^\w-]+", "-", t).strip("-")
    if not t:
        sys.exit("El motivo no puede quedar vacío: una o dos palabras de lo que cambia la versión nueva.")
    return t


def respaldar(md: Path, motivo: str) -> list[Path]:
    if not md.is_file():
        sys.exit(f"No encuentro el documento: {md}")
    carpeta = md.parent / "_respaldo"
    origenes = [x for x in (md, md.with_suffix(".html")) if x.is_file()]
    destinos = [carpeta / f"{x.stem}_antes-{motivo_limpio(motivo)}{x.suffix}" for x in origenes]
    ya = [d for d in destinos if d.exists()]
    if ya:
        sys.exit("Ya hay un respaldo con ese nombre: " + ", ".join(str(d) for d in ya) + ". Elige otro motivo.")
    carpeta.mkdir(exist_ok=True)
    for o, d in zip(origenes, destinos):
        shutil.copy2(o, d)
    return destinos


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip().splitlines()[2].strip())
    for d in respaldar(Path(sys.argv[1]), sys.argv[2]):
        print(d)


if __name__ == "__main__":
    main()
