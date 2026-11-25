"""Pone en la web comercial (site/) los colores, la letra y los logos del estilo de la SF (docs/identidad/estilo.json).

La web comparte con los documentos los colores y la letra del estilo y conserva su propia forma de página (decisión
312): no se genera con el generador de documentos. Este script escribe en site/index.html el bloque «estilo» (entre
«/* estilo:inicio» y «/* estilo:fin */»), con cada rol de color del estilo como variable CSS (--primario, --texto…), en
claro y en oscuro, la paleta oscura también fija como --en-oscuro-<rol> (para los terminales simulados), los colores con
significado (--correcto…) y la letra (--letra-texto, --letra-titulos, --letra-codigo); cambia la hoja de letra por la
del estilo y el color del navegador (theme-color) por su oscuro, y copia sus logos a site/img/. La página traduce esos
roles a sus propias variables (--paper, --accent…), que no cambian.

Uso: python -I -X utf8 scripts/estilo_web.py [--comprobar]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "plugins" / "sf" / "skills" / "crear_documentos" / "scripts"))
import estilo_proyecto  # noqa: E402
from tema_identidad import oscuro_de  # noqa: E402

ESTILO = RAIZ / "docs" / "identidad" / "estilo.json"
PAGINA = RAIZ / "site" / "index.html"
IMG = RAIZ / "site" / "img"
INICIO = "/* estilo:inicio"
FIN = "/* estilo:fin */"
LETRA = re.compile(r'<link id="estilo-letra"[^>]*>')
COLOR_NAVEGADOR = re.compile(r'<meta name="theme-color" content="[^"]*">')


def _decl(variables: dict, sangria: str) -> str:
    return "\n".join(f"{sangria}--{k}: {v};" for k, v in variables.items())


def bloque(estilo: dict, ruta: Path) -> str:
    tema = estilo_proyecto.tema_del_estilo(estilo, ruta)
    claro, oscuro = tema["colores"], tema["colores-oscuro"]
    significado = estilo_proyecto.significado(estilo)
    letra = estilo.get("letra", {})
    tipos = tema["tipografias"]
    fijo = {
        **claro,
        **significado,
        **{f"en-oscuro-{k}": v for k, v in oscuro.items()},
        **{f"en-oscuro-{k}": oscuro_de(v, oscuro) for k, v in significado.items()},
        "letra-texto": tipos["texto"],
        "letra-titulos": tipos["titulos"],
        "letra-codigo": letra.get("codigo", "ui-monospace, Consolas, monospace"),
    }
    nocturno = {**oscuro, **{k: oscuro_de(v, oscuro) for k, v in significado.items()}}
    nombre = f"«{estilo['nombre']}» " if estilo.get("nombre") else ""
    return (f"{INICIO} · lo escribe scripts/estilo_web.py con el estilo de la SF {nombre}v{estilo['version']} "
            f"(docs/identidad/estilo.json); no se edita a mano */\n"
            f"  :root {{\n{_decl(fijo, '    ')}\n  }}\n"
            f"  @media (prefers-color-scheme: dark) {{\n    :root {{\n{_decl(nocturno, '      ')}\n    }}\n  }}\n"
            f"  {FIN}")


def aplicar(html: str, estilo: dict, ruta: Path) -> str:
    i, j = html.find(INICIO), html.find(FIN)
    if i < 0 or j < i:
        sys.exit(f"{PAGINA} no tiene el bloque «estilo» («{INICIO}» … «{FIN}»).")
    html = html[:i] + bloque(estilo, ruta) + html[j + len(FIN):]
    if not LETRA.search(html):
        sys.exit(f'{PAGINA} no tiene la hoja de letra (<link id="estilo-letra" …>).')
    url = estilo.get("letra", {}).get("url", "")
    html = LETRA.sub(lambda _: f'<link id="estilo-letra" href="{url}" rel="stylesheet">', html, count=1)
    if not COLOR_NAVEGADOR.search(html):
        sys.exit(f"{PAGINA} no tiene <meta name=\"theme-color\" …>.")
    return COLOR_NAVEGADOR.sub(lambda _: f'<meta name="theme-color" content="{estilo["colores"]["oscuro"]}">', html,
                               count=1)


def logos(estilo: dict) -> dict[Path, str]:
    """Los logos del estilo, con el nombre que tienen en site/img/: logo.svg (claro) y logo-oscuro.svg."""
    ident = estilo.get("identidad", {})
    claro = ident.get("logo")
    claro = claro[0] if isinstance(claro, list) else claro
    pares = {"logo.svg": claro, "logo-oscuro.svg": ident.get("logo-oscuro")}
    falta = [k for k, v in pares.items() if not v]
    if falta:
        sys.exit(f"El estilo de la SF no tiene {' ni '.join(falta)} en «identidad».")
    return {IMG / destino: (ESTILO.parent / origen).read_text(encoding="utf-8") for destino, origen in pares.items()}


def main():
    ap = argparse.ArgumentParser(description="Estilo de la SF → web comercial (site/)")
    ap.add_argument("--comprobar", action="store_true", help="solo dice si la web tiene el estilo al día, sin escribir")
    args = ap.parse_args()
    estilo = estilo_proyecto.cargar(ESTILO)
    antes = PAGINA.read_text(encoding="utf-8")
    cambios = {PAGINA: aplicar(antes, estilo, ESTILO), **logos(estilo)}
    viejos = [p for p, texto in cambios.items() if not p.is_file() or p.read_text(encoding="utf-8") != texto]
    if args.comprobar:
        if viejos:
            sys.exit("La web no tiene el estilo de la SF al día en: "
                     + ", ".join(p.relative_to(RAIZ).as_posix() for p in viejos)
                     + ". Se pone con python -I -X utf8 scripts/estilo_web.py")
        print(f"Web al día con el estilo de la SF v{estilo['version']}.")
        return
    for p in viejos:
        p.write_text(cambios[p], encoding="utf-8", newline="\n")
    print(f"Estilo de la SF v{estilo['version']} en la web: "
          + (", ".join(p.relative_to(RAIZ).as_posix() for p in viejos) if viejos else "sin cambios"))


if __name__ == "__main__":
    main()
