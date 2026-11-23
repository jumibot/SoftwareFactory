"""Escribe el estilo del proyecto en una infografía técnica (decisiones 315 y 323).

Uso:
    python -I -X utf8 <skills>/infografia_tecnica/scripts/estilo_infografia.py <infografia>.html
        [--estilo <ruta>|ninguno] [--tema <nombre>|<ruta .json>] [--identidad <carpeta>|ninguna] [--comprobar]

Lee docs/identidad/estilo.json, que se busca subiendo carpetas desde la infografía como hace el generador de documentos,
y reescribe el bloque «estilo» de la hoja (entre «/* estilo:inicio» y «/* estilo:fin */») y la hoja de letra
(<link id="estilo-letra">): página, letra, escenario y HUD. Lo demás de la infografía no se toca, y repetirlo con el mismo
estilo da el mismo archivo.

- Página: «pagina», «texto» y «texto-suave» del estilo, y los de «colores-oscuro» en modo oscuro.
- Letra: «letra.texto» y «letra.titulos»; la de código («letra.codigo»), o la monoespaciada del sistema, en el HUD.
- Escenario («aparte.escenario»): «derivado», oscuro y sacado del «oscuro» del estilo (por defecto), o «claro».
- HUD («aparte.hud»): «primario» (su tono vivo, por defecto), «acento» o un #rrggbb. Con «primario» o «acento», se aclara
  (o se oscurece, con el escenario claro) hasta 7:1 sobre el escenario, para que brille; un #rrggbb por debajo de 4,5:1
  detiene.
- Esquinas del marco: «pagina.esquinas», si está.

Sin estilo.json, los valores por defecto de un tema, como el generador (decisión 323): --tema, el de identidad.json, el
más cercano al color de sesión del proyecto o «morado», con un aviso.

Los colores con significado del modelo (materiales, flujos, avisos, la pantalla del propio producto) no son del estilo y
no se tocan.
"""

from __future__ import annotations

import argparse, json, re, sys
from pathlib import Path

COMUN = Path(__file__).resolve().parent.parent.parent / "crear_documentos" / "scripts"
if not (COMUN / "estilo_proyecto.py").is_file():
    sys.exit(f"Falta la skill crear_documentos junto a esta: no encuentro {COMUN / 'estilo_proyecto.py'}")
sys.path.insert(0, str(COMUN))
import estilo_proyecto  # noqa: E402
from tema_identidad import _rgb, buscar_identidad, contraste, mezclar, sobre  # noqa: E402

INICIO = "/* estilo:inicio"
FIN = "/* estilo:fin */"
MONO_SISTEMA = 'ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace'
MINIMO = 4.5  # el HUD es texto pequeño (rótulos, el modo, el número de cada etiqueta)
VIVO = 7  # el HUD que se deriva del primario o del acento brilla como un holograma: 7:1 sobre el escenario


def rgb(color: str) -> str:
    return ",".join(str(x) for x in _rgb(color))


def peor_contraste(color: str, fondos: tuple[str, ...]) -> float:
    return min(contraste(color, f) for f in fondos)


def ajustar(color: str, fondos: tuple[str, ...], hacia: str, minimo: float) -> str:
    """El color, mezclado con «hacia» en pasos de 5 % hasta leerse a «minimo»:1 sobre todos los fondos."""
    for paso in range(21):
        c = mezclar(color, hacia, paso / 20)
        if peor_contraste(c, fondos) >= minimo:
            return c
    return hacia


def escenario(c: dict, claro: bool) -> dict:
    """Los colores del escenario: el centro (stage-a), el borde (stage-b) y el cristal de los paneles."""
    if claro:
        return {"a": mezclar(c["pagina"], "#ffffff", .6), "b": c["fondo-medio"], "vidrio": "#ffffff"}
    # Derivado del oscuro: más oscuro todavía, hasta que el blanco se lea de sobra en el centro.
    prop = .45
    while contraste("#ffffff", mezclar(c["oscuro"], "#000000", prop)) < 12 and prop < .95:
        prop += .05
    return {"a": mezclar(c["oscuro"], "#000000", prop), "b": mezclar(c["oscuro"], "#000000", min(prop + .4, .92)),
            "vidrio": mezclar(c["oscuro"], "#000000", min(prop + .25, .9))}


def valores(tema: dict, estilo: dict | None) -> tuple[dict, list[str], list[str]]:
    """(variables CSS, avisos, errores) con los colores y la letra del tema y los parámetros «aparte» del estilo."""
    c, t = tema["colores"], tema["tipografias"]
    claro = estilo_proyecto.param(estilo, "aparte", "escenario", "derivado") == "claro"
    hud_param = estilo_proyecto.param(estilo, "aparte", "hud", "primario")
    esc = escenario(c, claro)
    fondos = (esc["a"], esc["b"])
    avisos, errores = [], []
    base = {"primario": c["primario-vivo"], "acento": c["acento"]}.get(hud_param, hud_param)
    if hud_param in ("primario", "acento"):
        hud = ajustar(base, fondos, "#000000" if claro else "#ffffff", VIVO if not claro else MINIMO)
    else:
        hud = base.lower()
        if peor_contraste(hud, fondos) < MINIMO:
            errores.append(f"aparte.hud {hud} da {peor_contraste(hud, fondos):.2f}:1 sobre el escenario "
                           f"{esc['a']}–{esc['b']} (mínimo {MINIMO:g}:1)")
    if claro:
        fuerte, tinta, halo, apagado = c["texto"], c["texto"], "#ffffff", c["borde"]
        aviso = mezclar(estilo_proyecto.significado(estilo)["aviso"], "#000000", .2)
    else:
        fuerte, tinta, halo, apagado = "#ffffff", mezclar(hud, "#ffffff", .75), "#000000", mezclar(esc["vidrio"], "#ffffff", .12)
        aviso = mezclar(estilo_proyecto.significado(estilo)["aviso"], "#ffffff", .7)
    for nombre, color in (("texto del HUD", tinta), ("títulos del HUD", fuerte), ("avisos del HUD", aviso)):
        r = peor_contraste(color, fondos)
        if r < MINIMO:
            avisos.append(f"{nombre}: {color} da {r:.2f}:1 sobre el escenario (mínimo {MINIMO:g}:1)")
    # Los rótulos secundarios (batería, consumo, modos sin elegir) van en el HUD traslúcido: tan opaco como haga falta
    # para leerse a 4,5:1, desde el 42 % de la plantilla.
    alfa = .42
    while alfa < 1 and min(contraste(mezclar(f, hud, alfa), f) for f in fondos) < MINIMO:
        alfa = round(alfa + .02, 2)
    oscuro = tema.get("colores-oscuro", {})
    fondo_oscuro = oscuro.get("pagina", mezclar(c["oscuro"], "#000000", .82))
    v = {
        "--bg": c["pagina"], "--ink": c["texto"], "--muted": c["texto-suave"],
        "--stage-a": esc["a"], "--stage-b": esc["b"],
        "--hud": hud, "--hud-rgb": rgb(hud), "--hud-ink": tinta, "--hud-fuerte": fuerte,
        "--sobre-hud": sobre(hud, tinta=esc["b"] if not claro else c["texto"]),
        # Rótulos secundarios y cristal de los paneles: más opacos con el escenario claro, para que se lean.
        "--hud-dim": f"rgba({rgb(hud)},{alfa})",
        "--hud-glass": f"rgba({rgb(esc['vidrio'])},{.8 if claro else .62})",
        "--vidrio-rgb": rgb(esc["vidrio"]), "--halo-rgb": rgb(halo), "--apagado": apagado, "--aviso-hud": aviso,
        "--body": t["texto"], "--titulos": t["titulos"],
        "--mono": estilo_proyecto.param(estilo, "letra", "codigo", MONO_SISTEMA),
    }
    if estilo_proyecto.param(estilo, "pagina", "esquinas") is not None:
        v["--r-marco"] = f"{float(estilo['pagina']['esquinas']):g}px"
    else:
        v["--r-marco"] = "18px"
    v["_oscuro"] = {"--bg": fondo_oscuro, "--ink": oscuro.get("texto", "#e6edf5"),
                    "--muted": oscuro.get("texto-suave", "#9aa6b6")}
    return v, avisos, errores


def bloque(v: dict, origen: str) -> str:
    claves = [k for k in v if not k.startswith("_")]
    lineas = "\n".join(f"  {k}:{v[k]};" for k in claves)
    oscuro = ";".join(f"{k}:{x}" for k, x in v["_oscuro"].items()) + ";color-scheme:dark"
    return (f"{INICIO} · lo escribe scripts/estilo_infografia.py con {origen}; no se edita a mano */\n"
            f":root{{\n{lineas}\n}}\n"
            f'@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{{oscuro}}}}}\n'
            f':root[data-theme="dark"]{{{oscuro}}}\n{FIN}')


def aplicar(html: str, v: dict, url_letra: str, origen: str) -> str:
    i, j = html.find(INICIO), html.find(FIN)
    if i < 0 or j < i:
        sys.exit("La infografía no tiene el bloque «estilo» («/* estilo:inicio» … «/* estilo:fin */»): "
                 "se parte de assets/plantilla-infografia.html o se copia ese bloque y sus variables.")
    html = html[:i] + bloque(v, origen) + html[j + len(FIN):]
    letra = re.compile(r'<link id="estilo-letra"[^>]*>\n?')
    if not letra.search(html):
        sys.exit('La infografía no tiene la hoja de letra (<link id="estilo-letra" …>) de la plantilla.')
    nueva = f'<link id="estilo-letra" rel="stylesheet" href="{url_letra}">\n' if url_letra else ""
    return letra.sub(lambda _: nueva, html, count=1)


def main():
    ap = argparse.ArgumentParser(description="Estilo del proyecto → infografía técnica (bloque «estilo» de la hoja)")
    ap.add_argument("html")
    ap.add_argument("--estilo", default=None, help="estilo.json del proyecto o 'ninguno'; por defecto, docs/identidad/estilo.json "
                    "subiendo desde la infografía")
    ap.add_argument("--tema", default=None, help="sin estilo del proyecto: tema de crear_documentos o ruta a un .json")
    ap.add_argument("--identidad", default=None, help="carpeta con identidad.json o 'ninguna'")
    ap.add_argument("--comprobar", action="store_true", help="solo dice si la infografía tiene el estilo al día, sin escribir")
    args = ap.parse_args()
    ruta = Path(args.html)
    if not ruta.is_file():
        sys.exit(f"No encuentro la infografía: {ruta}")
    ruta_estilo = estilo_proyecto.buscar_estilo(ruta, args.identidad, args.estilo)
    estilo = estilo_proyecto.cargar(ruta_estilo) if ruta_estilo else None
    if estilo:
        tema, aviso = estilo_proyecto.tema_del_estilo(estilo, ruta_estilo), ""
        origen = f"el estilo del proyecto v{estilo['version']}"
    else:
        ruta_id = buscar_identidad(ruta, args.identidad)
        identidad = json.loads(ruta_id.read_text(encoding="utf-8")) if ruta_id else {}
        tema, aviso = estilo_proyecto.tema_sin_estilo(ruta, identidad, ruta_id, args.tema)
        origen = f"el tema por defecto «{tema.get('nombre', '')}», sin estilo del proyecto"
    v, avisos, errores = valores(tema, estilo)
    if errores and estilo:
        sys.exit(f"Contraste insuficiente del HUD en el estilo del proyecto ({ruta_estilo}):\n  " + "\n  ".join(errores))
    if aviso:
        print(aviso, file=sys.stderr)
    for a in avisos + (errores if not estilo else []):
        print("Aviso: " + a, file=sys.stderr)
    antes = ruta.read_text(encoding="utf-8")
    despues = aplicar(antes, v, tema["tipografias"]["url"], origen)
    if args.comprobar:
        if antes != despues:
            sys.exit(f"{ruta}: el estilo no está al día; se escribe sin --comprobar.")
        print(f"{ruta}: estilo al día ({origen}).")
        return
    if antes != despues:
        ruta.write_text(despues, encoding="utf-8")
    print(f"{ruta} · {origen} · escenario {estilo_proyecto.param(estilo, 'aparte', 'escenario', 'derivado')}"
          f" · HUD {v['--hud']}" + ("" if antes != despues else " · sin cambios"))


if __name__ == "__main__":
    main()
