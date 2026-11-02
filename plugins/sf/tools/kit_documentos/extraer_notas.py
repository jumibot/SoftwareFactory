"""Lista las notas y los párrafos editados de un documento guardado con «Guardar» (biblioteca tools/kit_documentos/).

    python extraer_notas.py <documento.html> [--json]

Las notas van dentro del HTML, en el bloque <script type="application/json" id="notas-documento">. Los párrafos
editados llevan data-modificado y data-anteriores (el primero, el original); los añadidos desde una nota, la clase
parrafo-anadido. La salida, en Markdown, pone primero la nota general y agrupa las demás por sección, con el texto anotado y el comentario, y después
los párrafos cambiados (antes y ahora) y los añadidos, para usarlos como revisión del .md fuente.
Lo comparten documento_vision y documento_fundacional."""
import argparse, html, json, re, sys
from pathlib import Path


def leer_notas(ruta: Path) -> dict:
    texto = ruta.read_text(encoding="utf-8")
    m = re.search(r'<script[^>]*id="notas-documento"[^>]*>(.*?)</script>', texto, re.S)
    datos = json.loads(m.group(1)) if m else {}
    datos["parrafos"] = parrafos(texto)
    if not m and not datos["parrafos"]:
        sys.exit(f"{ruta} no tiene notas ni párrafos editados.")
    return datos


def plano(h: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", h)).split())


def parrafos(texto: str) -> list[dict]:
    """Párrafos modificados (con su original) y añadidos desde una nota."""
    out = []
    # Los atributos pueden llevar «>» entre comillas (data-anteriores guarda HTML).
    for m in re.finditer(r'<p\b((?:[^>"]|"[^"]*")*)>(.*?)</p>', texto, re.S):
        atr, cuerpo = m.group(1), m.group(2)
        mod = re.search(r'data-modificado="([^"]*)"', atr)
        if mod:
            ant = re.search(r'data-anteriores="([^"]*)"', atr)
            antes = json.loads(html.unescape(ant.group(1))) if ant else []
            out.append({"tipo": "modificado", "fechas": mod.group(1).split(), "original": plano(antes[0]) if antes else "", "ahora": plano(cuerpo)})
        elif "parrafo-anadido" in atr:
            f = re.search(r'data-anadido="([^"]*)"', atr)
            out.append({"tipo": "añadido", "fechas": [f.group(1)] if f else [], "ahora": plano(cuerpo)})
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("html", type=Path)
    ap.add_argument("--json", action="store_true", help="salida en JSON tal cual")
    args = ap.parse_args()
    datos = leer_notas(args.html)
    if args.json:
        print(json.dumps(datos, ensure_ascii=False, indent=2))
        return
    notas = datos.get("notas", [])
    cambiados = datos.get("parrafos", [])
    print(f"# Notas de {html.unescape(datos.get('documento', args.html.name))}\n")
    print(f"Versión v{datos.get('version', '?')} · guardado {datos.get('guardado', '?')} · herramientas v{datos.get('herramientas', '?')} · {len(notas)} notas\n")
    secciones = {}
    for n in sorted(notas, key=lambda x: not x.get("global")):  # la nota general, primero
        clave = "Todo el documento" if n.get("global") else n.get("titulo") or n.get("seccion") or "Inicio"
        secciones.setdefault(clave, []).append(n)
    for titulo, lista in secciones.items():
        print(f"## {titulo}\n")
        for n in sorted(lista, key=lambda x: x.get("creada", "")):
            quien = " · ".join(x for x in (n.get("autor", ""), n.get("modificada", "")[:16].replace("T", " ")) if x)
            if n.get("cita"):
                print(f"- **Sobre:** «{' '.join(n['cita'].split())}»")
                print(f"  **Nota:** {n.get('texto', '').strip() or '(sin comentario: solo marcado)'}")
            elif n.get("global"):
                print(f"- **Nota general:** {n.get('texto', '').strip()}")
            else:
                print(f"- **Nota de sección:** {n.get('texto', '').strip()}")
            if quien:
                print(f"  _{quien}_")
        print()
    for tipo, titulo in (("modificado", "Párrafos modificados"), ("añadido", "Párrafos añadidos")):
        lista = [x for x in cambiados if x["tipo"] == tipo]
        if not lista:
            continue
        print(f"## {titulo}\n")
        for x in lista:
            cuando = ", ".join(f[:16].replace("T", " ") for f in x["fechas"])
            if tipo == "modificado":
                print(f"- **Antes:** {x['original']}\n  **Ahora:** {x['ahora']}\n  _{cuando}_")
            else:
                print(f"- {x['ahora']}\n  _{cuando}_")
        print()


if __name__ == "__main__":
    main()
