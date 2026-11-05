"""Pone al día las herramientas de un documento ya repartido (o de una copia anotada) sin tocar su contenido.

    python actualizar_copia.py <documento.html> [...] [--comprobar] [--herramientas "buscador notas …"]

Cada bloque de código del kit lleva data-kit con su ruta desde la carpeta que contiene skills/ y tools/ (en el
repositorio de la SF y en ~/.claude): se sustituye por la versión actual de ese archivo. Los bloques que no llevan la
marca son contenido (el tema, las notas, el CSS del proyecto) y no se tocan. Las copias anteriores a las marcas se
reconocen por la primera línea de cada archivo del kit. Los scripts del kit que falten (por ejemplo, lectura.js en una
copia de herramientas 1.1) se añaden tras herramientas.js.

Los marcadores de color de las plantillas ({{primario}}, {{oscuro}}…, en las URI de datos SVG) se rellenan con el tema
del propio documento, el de sus variables :root (--primario: #…), como hacen los generadores; si falta alguno, no se toca.

Antes de escribir, comprueba que el documento sin el código del kit queda igual, y guarda el original en copias/.
--herramientas cambia las herramientas que lleva el documento (<html data-herramientas>).
Procedencia: docs/referencias/procedencia/kit_documentos.md del repositorio de la SF."""
import argparse, datetime, re, shutil, sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
BASE = KIT.parent.parent
CONOCIDOS = ["tools/kit_documentos/herramientas.css", "tools/kit_documentos/herramientas.js", "tools/kit_documentos/lectura.js",
             "tools/kit_documentos/edicion.js", "skills/documento_vision/assets/estilo_base.css",
             "skills/crear_documentos/assets/estilo_documento.css", "skills/crear_documentos/assets/plegado.js",
             "skills/crear_documentos/assets/fichas.js", "tools/kit_documentos/diagramas.js",
             "skills/diagramas/assets/diagramas.css", "skills/diagramas/assets/diagramas.js"]
SCRIPTS_KIT = ["tools/kit_documentos/herramientas.js", "tools/kit_documentos/lectura.js", "tools/kit_documentos/edicion.js"]
# Archivos que cambiaron de sitio: la copia se pone al día con el archivo de su sitio nuevo.
ANTIGUOS = {"skills/documento_vision/assets/herramientas.css": "tools/kit_documentos/herramientas.css",
            "skills/documento_vision/assets/herramientas.js": "tools/kit_documentos/herramientas.js",
            # 301: lo común de los documentos pasa a la skill crear_documentos.
            "skills/documento_fundacional/assets/estilo_fundacional.css": "skills/crear_documentos/assets/estilo_documento.css",
            "skills/documento_fundacional/assets/plegado.js": "skills/crear_documentos/assets/plegado.js",
            "skills/documento_fundacional/assets/fichas.js": "skills/crear_documentos/assets/fichas.js"}
ETIQUETA = re.compile(r"<(style|script)\b([^>]*)>(.*?)</\1\s*>", re.S)


def actual(ruta: str) -> str:
    return (BASE / ruta).read_text(encoding="utf-8").rstrip()


def primera_linea(ruta: str) -> str:
    return actual(ruta).splitlines()[0].strip()[:60]


def sin_kit(html: str) -> str:
    return re.sub(r'\s*<(style|script)\b[^>]*\bdata-kit="[^"]+"[^>]*>.*?</\1\s*>', "", html, flags=re.S)


def marcar(html: str) -> tuple[str, list[str]]:
    """Copias sin marcas: cada bloque cuyo cuerpo empieza como un archivo del kit recibe su data-kit."""
    firmas = {primera_linea(r): r for r in CONOCIDOS if (BASE / r).is_file()}
    marcados = []
    def uno(m):
        if "data-kit=" in m.group(2):
            return m.group(0)
        cuerpo = m.group(3).strip()
        for firma, ruta in firmas.items():
            if cuerpo.startswith(firma):
                marcados.append(ruta)
                return f'<{m.group(1)} data-kit="{ruta}"{m.group(2)}>{m.group(3)}</{m.group(1)}>'
        # El estilo del fundacional iba en el mismo bloque que las variables del tema: se deja como está.
        return m.group(0)
    return ETIQUETA.sub(uno, html), marcados


MARCADOR = re.compile(r"\{\{([a-z][a-z-]*)\}\}")


def colores_tema(html: str) -> dict:
    """Colores del tema del documento: las variables --rol: #hex de sus bloques :root, fuera del código del kit."""
    colores = {}
    for bloque in re.findall(r":root\s*\{([^}]*)\}", sin_kit(html)):
        for rol, valor in re.findall(r"--([a-z][a-z-]*)\s*:\s*(#[0-9a-fA-F]{3,8})\s*;", bloque):
            colores.setdefault(rol, valor)
    return colores


def rellenar(cuerpo: str, colores: dict) -> str:
    """Como aplicar_tema de los generadores: {{rol}} → %23hex. Los marcadores sin color (p. ej. {{rol}} en un
    comentario) se dejan."""
    return MARCADOR.sub(lambda m: "%23" + colores[m.group(1)].lstrip("#") if m.group(1) in colores else m.group(0), cuerpo)


def faltan_colores(cuerpo: str, colores: dict) -> list[str]:
    """Marcadores usados en valores (dentro de comillas de un atributo SVG) que el tema no rellena."""
    return sorted({r for r in re.findall(r"'\{\{([a-z][a-z-]*)\}\}'", cuerpo) if r not in colores})


def actualizar(html: str) -> tuple[str, dict]:
    cambios = {}
    colores = colores_tema(html)
    def uno(m):
        k = re.search(r'\bdata-kit="([^"]+)"', m.group(2))
        if not k:
            return m.group(0)
        ruta = ANTIGUOS.get(k.group(1), k.group(1))
        if not (BASE / ruta).is_file():
            cambios[ruta] = "desconocido (se deja)"
            return m.group(0)
        nuevo = actual(ruta)
        if MARCADOR.search(nuevo):
            faltan = faltan_colores(nuevo, colores)
            if faltan:
                sys.exit(f"{ruta}: el documento no tiene los colores de su tema para {', '.join(faltan)}; no se toca nada")
            nuevo = rellenar(nuevo, colores)
        cambios[ruta] = "igual" if m.group(3).strip() == nuevo.strip() else "actualizado"
        if cambios[ruta] == "igual" and ruta == k.group(1):
            return m.group(0)  # sin cambios: ni siquiera de espacios
        return f'<{m.group(1)} data-kit="{ruta}">\n{nuevo}\n</{m.group(1)}>'
    html = ETIQUETA.sub(uno, html)
    # Scripts del kit que falten, tras el anterior que sí esté.
    for i, ruta in enumerate(SCRIPTS_KIT):
        if f'data-kit="{ruta}"' in html:
            continue
        anterior = next((r for r in reversed(SCRIPTS_KIT[:i]) if f'data-kit="{r}"' in html), None)
        if not anterior:
            continue
        m = re.search(rf'<script data-kit="{re.escape(anterior)}">.*?</script>', html, re.S)
        html = html[:m.end()] + f'\n<script data-kit="{ruta}">\n{actual(ruta)}\n</script>' + html[m.end():]
        cambios[ruta] = "nuevo"
    return html, cambios


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("html", type=Path, nargs="+")
    ap.add_argument("--comprobar", action="store_true", help="dice qué cambiaría, sin escribir")
    ap.add_argument("--herramientas", help="herramientas que lleva el documento, separadas por espacios")
    args = ap.parse_args()
    for ruta in args.html:
        original = ruta.read_text(encoding="utf-8")
        html, marcados = marcar(original)
        nuevo, cambios = actualizar(html)
        if args.herramientas is not None:
            nuevo = re.sub(r'(<html\b[^>]*?)\s+data-herramientas="[^"]*"', r"\1", nuevo, count=1)
            nuevo = nuevo.replace("<html", f'<html data-herramientas="{args.herramientas.strip()}"', 1)
        if sin_kit(nuevo).replace(' data-herramientas="', '"').split("<head", 1)[1] != sin_kit(html).replace(' data-herramientas="', '"').split("<head", 1)[1]:
            sys.exit(f"{ruta}: el contenido cambiaría; no se toca nada")
        print(f"{ruta.name}{' · marcado por primera vez: ' + ', '.join(Path(m).name for m in marcados) if marcados else ''}")
        for estado in ("actualizado", "nuevo", "igual", "desconocido (se deja)"):
            n = sorted(Path(k).name for k, v in cambios.items() if v == estado)
            if n:
                print(f"  {estado}: {', '.join(n)}")
        if args.comprobar or nuevo == original:
            print("  " + ("(comprobación: no se escribe)" if args.comprobar else "sin cambios"))
            continue
        copias = ruta.parent / "copias"
        copias.mkdir(exist_ok=True)
        shutil.copy2(ruta, copias / f"{ruta.stem}__{datetime.datetime.now():%Y%m%d_%H%M%S}{ruta.suffix}")
        ruta.write_text(nuevo, encoding="utf-8")
        print("  escrito; el original, en copias/")


if __name__ == "__main__":
    main()
