"""El diagrama como recurso del catálogo (decisión 314): el .md nombra su .diagrama y el generador lo dibuja.

Una línea sola, fuera del código, con la forma de una imagen cuyo archivo acaba en .diagrama:

    ![](diagramas/flujo.diagrama)

se sustituye, en cada generación, por la <figure> que dibuja el motor de la skill de diagramas
(`diagramas/scripts/generar_diagrama.py --fragmento --tema ""`): sin tema propio, la figura toma el estilo del
documento (decisión 307). La ruta es relativa a la carpeta del .md. El texto entre corchetes no se usa: el título,
la descripción y el pie salen de los datos del diagrama. El id de la figura es el nombre del archivo.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MOTOR = Path(__file__).resolve().parents[2] / "diagramas" / "scripts" / "generar_diagrama.py"
REFERENCIA = re.compile(r"^ {0,3}!\[[^\]\n]*\]\(\s*(?:<([^>\n]+\.diagrama)>|([^)\s]+\.diagrama))\s*\)\s*$")
VALLA = re.compile(r"^\s*(```|~~~)")


class ErrorDiagrama(Exception):
    pass


def referencias(md: str) -> list[tuple[int, str]]:
    """(número de línea, ruta) de cada referencia a un .diagrama, fuera de los bloques de código."""
    out, en_codigo = [], None
    for n, linea in enumerate(md.split("\n"), 1):
        v = VALLA.match(linea)
        if v:
            en_codigo = None if en_codigo == v.group(1) else (en_codigo or v.group(1))
            continue
        if en_codigo:
            continue
        m = REFERENCIA.match(linea)
        if m:
            out.append((n, m.group(1) or m.group(2)))
    return out


def dibujar(ruta: Path) -> str:
    """La <figure> del .diagrama, del motor de la skill de diagramas, sin tema (la del documento)."""
    if not ruta.is_file():
        raise ErrorDiagrama(f"no existe {ruta}")
    with tempfile.TemporaryDirectory() as d:
        salida = Path(d) / "figura.html"
        r = subprocess.run([sys.executable, "-I", "-X", "utf8", str(MOTOR), str(ruta), "--fragmento", "--tema", "",
                            "-o", str(salida)], capture_output=True, text=True, encoding="utf-8")
        avisos = [x for x in r.stderr.splitlines() if x.strip()]
        if r.returncode != 0 or not salida.is_file():
            raise ErrorDiagrama(f"{ruta.name}: " + ("; ".join(avisos) or f"el motor salió con {r.returncode}"))
        for a in avisos:  # p. ej. «sin horizontal»: el diagrama sale, solo en vertical
            print(f"Aviso ({ruta.name}): {a.lstrip('· ')}", file=sys.stderr)
        return salida.read_text(encoding="utf-8").strip()


def expandir(md: str, carpeta: Path, desplazamiento: int = 0) -> str:
    """El .md con cada referencia a un .diagrama sustituida por su figura. Se detiene si falta uno o el motor falla.
    desplazamiento: líneas de la cabecera de datos, para que los errores digan la línea del archivo."""
    refs = dict(referencias(md))
    if not refs:
        return md
    lineas = md.split("\n")
    errores = []
    for n, rel in refs.items():
        try:
            lineas[n - 1] = dibujar((carpeta / rel).resolve())
        except ErrorDiagrama as e:
            errores.append(f"línea {n + desplazamiento}: {e}")
    if errores:
        raise ErrorDiagrama("No se pudo dibujar un diagrama del documento:\n  " + "\n  ".join(errores))
    return "\n".join(lineas)
