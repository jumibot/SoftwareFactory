"""Fija y afina el estilo de los documentos de un proyecto (docs/identidad/estilo.json) con muestras del generador.

    python estilo.py parametros                       el catálogo del generador: grupos, parámetros, posibles y defecto
    python estilo.py ver                              el estilo del proyecto y lo que está en prueba
    python estilo.py partir <tema|juego.json>         pone en prueba un estilo completo, resuelto desde un tema o un juego
    python estilo.py cambiar grupo.clave=valor …      cambia valores del estilo en prueba (sin prueba, parte del actual)
    python estilo.py muestras <doc>.md [nombres …]    genera el documento con «prueba», «actual», temas o juegos
    python estilo.py aceptar --motivo "…" [--cambio "…"]   lleva la prueba a estilo.json: respaldo, versión +1, historial
    python estilo.py descartar                        borra la prueba y sus muestras sin tocar estilo.json
    python estilo.py catalogo [--salida carpeta]      el catálogo de temas: cada tema en miniatura, en claro y en oscuro

Opción común: --raiz <carpeta del proyecto> (por defecto, la actual). Escribe solo en la carpeta de identidad del
proyecto (docs/identidad/, o doc/identidad/ si ya existe) y junto al documento de las muestras. No maqueta: las
muestras las hace el generador de crear_documentos (decisión 305).

- estilo.json guarda todos los valores resueltos; el tema o el juego de partida queda solo como «origen» (317).
- Lo que se prueba va en estilo.prueba.json, junto a estilo.json, y no lo cambia hasta aceptarlo.
- Cada aceptación respalda la versión anterior en _respaldo/estilo_v<N>.json, sube la versión y anota el historial (322).
"""

from __future__ import annotations

import argparse, datetime, json, shutil, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
COMUN = AQUI.parent.parent / "crear_documentos" / "scripts"
if not (COMUN / "estilo_proyecto.py").is_file():
    sys.exit(f"Falta la skill crear_documentos junto a esta: no encuentro {COMUN / 'estilo_proyecto.py'}")
sys.path.insert(0, str(COMUN))
import estilo_proyecto as ep  # noqa: E402
from tema_identidad import ROLES_VALIDOS, TEMAS, cabecera_clara, derivar_oscuro, primario_linea, sobre, legible_sobre_su_fondo, mezclar, normalizar_tema  # noqa: E402

GENERADOR = COMUN / "documento_a_html.py"
PRUEBA = "estilo.prueba.json"
LISTA_MUESTRAS = "estilo.prueba.muestras"  # las muestras generadas, una ruta por línea, para borrarlas al acabar

# Opciones de aspecto de un tema del catálogo («estilo» del tema) → parámetros del estilo (informe 387, «Lo que hoy fija
# cada uno por su cuenta»). Sin estilo.json no se aplican (331); al partir de un tema, vuelven como valores resueltos.
CABECERA_TEMA = {"blanca": {"forma": "clara"}, "primario": {"forma": "oscura", "fondo": "primario"},
                 "oscuro": {"forma": "oscura", "fondo": "oscuro"}}


# --- Dónde están los archivos -------------------------------------------------------------------------------------------

def carpeta_identidad(raiz: Path) -> Path:
    """docs/identidad/ del proyecto (o doc/identidad/ si es la que existe)."""
    for sub in ("docs/identidad", "doc/identidad"):
        if (raiz / sub).is_dir():
            return raiz / sub
    return raiz / "docs" / "identidad"


def leer(ruta: Path) -> dict | None:
    return ep.cargar(ruta) if ruta.is_file() else None


def escribir(ruta: Path, estilo: dict) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(estilo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --- Resolver un tema o un juego a un estilo completo (decisión 317) ----------------------------------------------------

def _identidad_del_proyecto(ident: Path) -> dict:
    ruta = ident / "identidad.json"
    if not ruta.is_file():
        return {}
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {k: datos[k] for k in ("producto", "logo") if isinstance(datos.get(k), str) and datos[k].strip()}


def resolver_tema(nombre: str, ident: Path) -> dict:
    """Un estilo con todos los valores resueltos desde un tema del catálogo: los colores que el tema no da, derivados como
    hace el generador; sus opciones de aspecto, pasadas a parámetros; lo demás, con su valor por defecto. La lectura
    (destino y herramientas) no se resuelve: el generador no elige por el autor (183)."""
    ruta = TEMAS / f"{nombre}.json"
    if not ruta.is_file():
        sys.exit(f"Tema no encontrado: {nombre}. Temas: {', '.join(sorted(p.stem for p in TEMAS.glob('*.json')))}; "
                 "o la ruta a un juego (un estilo.json completo).")
    tema = normalizar_tema(json.loads(ruta.read_text(encoding="utf-8")), ruta.name)
    colores = dict(tema["colores"])
    if tema["colores-oscuro"]:
        colores["colores-oscuro"] = dict(tema["colores-oscuro"])
    if tema["serie"]:
        colores["serie"] = list(tema["serie"])
    colores["significado"] = dict(ep.SIGNIFICADO)
    letra = {k: tema["tipografias"][k] for k in ("texto", "titulos", "escena", "url")}
    letra.update(tamano=17, escala="editorial")
    opciones = tema.get("estilo", {})
    portada = {"forma": "clara", "fondo": "oscuro", "linea": "si", **CABECERA_TEMA.get(opciones.get("cabecera"), {})}
    secciones = {"cabecera": "numero-etiqueta", "etiqueta": opciones.get("etiqueta", "tinte"),
                 "opacidad": opciones.get("opacidad", 1), "marcador": opciones.get("marcador", "flecha"),
                 "plegado": "primera"}
    pagina = {"ancho": 1240, "codigo": "bloque", "pie": "claro", "filetes": "si"}
    if "esquinas" in opciones:
        pagina["esquinas"] = opciones["esquinas"]
    estilo = {"version": 1, "origen": nombre, "historial": [], "identidad": _identidad_del_proyecto(ident),
              "colores": colores, "letra": letra, "portada": portada, "secciones": secciones, "pagina": pagina,
              "recuadros": {"filete": "si"}, "lectura": {"menu": "botones"}, "diagramas": {"tema": "documento"},
              "aparte": {"escenario": "derivado", "hud": "primario"}}
    if not estilo["identidad"]:
        del estilo["identidad"]
    return ep.validar(estilo, f"tema {nombre}")


def _estilo_del_origen(estilo: dict, ident: Path) -> dict | None:
    """El estilo resuelto desde el tema de partida de «estilo» (su «origen»), o None si el origen no es un tema."""
    origen = estilo.get("origen")
    if not isinstance(origen, str) or not (TEMAS / f"{origen}.json").is_file():
        return None
    return resolver_tema(origen, ident)


JUEGOS = AQUI.parent / "assets" / "juegos"


def juegos() -> dict:
    """Las muestras del plugin (decisión 335, 6): una por tema del catálogo, cada una con una forma propia (portada,
    cabecera de sección, marcador, esquinas, letra), para que se distingan a primera vista y no solo por el color."""
    todos = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in JUEGOS.glob("*.json")}
    return dict(sorted(todos.items(), key=lambda par: par[1]["muestra"]))  # de la A a la F


def resolver_juego(nombre: str, ident: Path) -> dict:
    """Un juego del plugin por su nombre: su tema resuelto y sus cambios encima; el tema queda como «origen» (317)."""
    juego = juegos()[nombre]
    return aplicar_cambios(resolver_tema(juego["origen"], ident), juego["cambios"])


def resolver(origen: str, ident: Path) -> dict:
    """Un tema del catálogo por su nombre, un juego del plugin por el suyo (sereno, tecnico…) o un juego propio: la
    ruta a un estilo.json completo (su «origen» se conserva)."""
    if origen in juegos():
        return resolver_juego(origen, ident)
    ruta = Path(origen)
    if ruta.suffix == ".json":
        if not ruta.is_file():
            sys.exit(f"No encuentro el juego de estilo: {ruta}")
        juego = ep.cargar(ruta)
        juego = {**juego, "version": 1, "historial": []}
        juego.setdefault("origen", ruta.stem)
        return juego
    return resolver_tema(origen, ident)


def contraste(estilo: dict, nombre: str) -> list[str]:
    """Los textos por debajo de 4,5:1 (3:1 el grande) con los que el generador se detendría (320)."""
    tema = ep.tema_del_estilo(estilo, Path(nombre))
    errores, _ = ep.comprobar_contraste(tema, estilo)
    return errores


# --- Cambios -------------------------------------------------------------------------------------------------------------

def _valor(texto: str):
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return texto


def familia_primario(colores: dict, antes: dict, pedidos: set[str]) -> None:
    """Recalcula la familia de un primario nuevo, en claro y en oscuro, con la mezcla de tema_identidad.py (decisión 338):
    vivo, texto, fondo, tenue y, si el acento era el primario, el acento con su fondo y su borde; en oscuro, los mismos
    con el primario aclarado lo justo para leerse sobre la página oscura y el texto sobre él (347, 348). Lo que se pide
    en el mismo cambio («pedidos», rutas grupo.clave) no se toca."""
    p = colores["primario"]
    blanco = "#ffffff"
    pagina = colores.get("pagina", mezclar(p, blanco, .97))
    superficie = colores.get("superficie", blanco)
    nuevos = {"primario-vivo": mezclar(p, blanco, .25), "fondo": mezclar(p, blanco, .95),
              "tenue": mezclar(p, blanco, .55)}
    # Legible también sobre su fondo de aviso, si hace de acento (la página blanca con un 6 % del color).
    nuevos["primario-texto"] = legible_sobre_su_fondo(
        p, [pagina, superficie, nuevos["fondo"], colores.get("fondo-medio", mezclar(p, blanco, .84))], blanco, .06, "#000000")
    nuevos.update(cabecera_clara(p, colores.get("texto", "#2b2b2f")))  # la cabecera destacada (351)
    nuevos["primario-linea"] = primario_linea(p, [pagina, superficie, nuevos["fondo"]], "#000000")  # 335, 8
    acento_es_primario = antes.get("acento") in (antes.get("primario"), antes.get("primario-texto"))
    if acento_es_primario:
        nuevos["acento"] = nuevos["primario-texto"]
        nuevos["acento-fondo"] = mezclar(nuevos["acento"], blanco, .94)
        nuevos["acento-borde"] = mezclar(nuevos["acento"], blanco, .72)
    for rol, valor in nuevos.items():
        if f"colores.{rol}" not in pedidos:
            colores[rol] = valor
    # En oscuro: la familia del primario se quita (salvo lo pedido) y se vuelve a derivar de la clara.
    oscuro = dict(colores.get("colores-oscuro") or {})
    antes_oscuro = antes.get("colores-oscuro") or {}
    familia = ["primario", "primario-vivo", "primario-texto", "sobre-primario", "fondo", "tenue", "cabecera",
               "sobre-cabecera", "primario-linea"]
    if acento_es_primario and antes_oscuro.get("acento") in (antes_oscuro.get("primario"), None):
        familia += ["acento", "acento-fondo", "acento-borde"]
    for rol in familia:
        if f"colores.colores-oscuro.{rol}" not in pedidos:
            oscuro.pop(rol, None)
    claro = normalizar_tema({"colores": {k: v for k, v in colores.items() if k in ROLES_VALIDOS}}, "el estilo")["colores"]
    colores["colores-oscuro"] = derivar_oscuro(claro, oscuro)


def aplicar_cambios(estilo: dict, cambios: list[str]) -> dict:
    """«grupo.clave=valor» (el valor, JSON si lo es: 0.4, 16, ["a.svg"]; si no, texto); «grupo.clave=» lo quita y vuelve
    a su valor por defecto. Un primario nuevo recalcula su familia, salvo lo pedido en el mismo cambio (338). Se valida
    con el catálogo del generador."""
    nuevo = json.loads(json.dumps(estilo))
    pedidos = {c.split("=", 1)[0] for c in cambios if "=" in c}
    primario_nuevo = any(c.startswith("colores.primario=") and c != "colores.primario=" for c in cambios)
    antes = json.loads(json.dumps(estilo.get("colores", {})))
    for cambio in cambios:
        if cambio.startswith("nombre="):  # el nombre del estilo («Áureo»); «nombre=» lo quita
            valor = cambio.split("=", 1)[1].strip()
            if valor:
                nuevo["nombre"] = valor
            else:
                nuevo.pop("nombre", None)
            continue
        if "=" not in cambio or "." not in cambio.split("=", 1)[0]:
            sys.exit(f"«{cambio}»: se escribe grupo.clave=valor (por ejemplo, secciones.etiqueta=solida).")
        ruta, valor = cambio.split("=", 1)
        grupo, clave = ruta.split(".", 1)
        if grupo not in ep.CATALOGO:
            sys.exit(f"«{grupo}» no es un grupo del estilo. Grupos: {', '.join(ep.CATALOGO)}.")
        destino = nuevo.setdefault(grupo, {})
        if "." in clave:  # colores.colores-oscuro.primario, colores.significado.aviso
            sub, clave = clave.split(".", 1)
            destino = destino.setdefault(sub, {})
        if valor == "":
            destino.pop(clave, None)
        else:
            destino[clave] = _valor(valor)
    if primario_nuevo:
        nuevo["colores"]["primario"] = str(nuevo["colores"]["primario"]).lower()
        ep.validar(json.loads(json.dumps(nuevo)), "el estilo en prueba")  # un primario no válido se dice antes de mezclar
        familia_primario(nuevo["colores"], antes, pedidos)
    return ep.validar(nuevo, "el estilo en prueba")


def diferencias(antes: dict, despues: dict) -> list[str]:
    """«grupo.clave: valor» de lo que cambia (y el nombre del estilo), sin versión, origen ni historial."""
    def plano(e: dict) -> dict:
        out = {"nombre": e["nombre"]} if e.get("nombre") else {}
        for grupo in ep.CATALOGO:
            for clave, v in (e.get(grupo) or {}).items():
                if isinstance(v, dict):
                    for k2, v2 in v.items():
                        out[f"{grupo}.{clave}.{k2}"] = v2
                else:
                    out[f"{grupo}.{clave}"] = v
        return out
    a, d = plano(antes), plano(despues)
    lineas = []
    for k in sorted(set(a) | set(d)):
        if a.get(k) != d.get(k):
            lineas.append(f"{k}: {json.dumps(d[k], ensure_ascii=False) if k in d else '(por defecto)'}")
    return lineas


# --- Órdenes -------------------------------------------------------------------------------------------------------------

def orden_parametros(_args) -> None:
    catalogo = dict(ep.CATALOGO, diagramas=ep._diagramas())
    for grupo, params in catalogo.items():
        print(f"{grupo}")
        for clave, validar in params.items():
            posibles = getattr(validar, "posibles", "ver crear_documentos, «Estilo del proyecto»") if validar else \
                "objeto o lista (ver crear_documentos, «Estilo del proyecto»)"
            defecto = ep.POR_DEFECTO.get(grupo, {}).get(clave)
            print(f"  {clave}: {posibles}" + (f" · por defecto: {defecto}" if defecto is not None else ""))


def _lineas(titulo: str, cambios: list[str]) -> None:
    print(f"  {titulo}:" + ("" if cambios else " nada"))
    for linea in cambios:
        print(f"    {linea}")


def _contar_prueba(prueba: dict, actual: dict | None, ident: Path, antes: dict | None = None) -> None:
    """Lo que cambia la prueba: el último cambio (si se da «antes»), todo lo cambiado frente a su tema de partida y, si
    el proyecto ya tiene estilo, frente a él; y lo que no pasa el contraste."""
    origen = _estilo_del_origen(prueba, ident)
    todo = diferencias(origen, prueba) if origen is not None else None
    este = diferencias(antes, prueba) if antes is not None else None
    if este is not None and este != todo:
        _lineas("Este cambio", este)
    if todo is not None:
        _lineas(f"Frente a {prueba['origen']}, todo lo cambiado", todo)
    if actual:
        _lineas(f"Frente al estilo del proyecto (v{actual.get('version')})", diferencias(actual, prueba))
    for error in contraste(prueba, PRUEBA):
        print(f"  No pasa el contraste: {error}")


def orden_ver(args) -> None:
    ident = carpeta_identidad(args.raiz)
    actual, prueba = leer(ident / "estilo.json"), leer(ident / PRUEBA)
    if actual:
        print(f"Estilo del proyecto: {ident / 'estilo.json'}"
              + (f", «{actual['nombre']}»" if actual.get("nombre") else "") + f", versión {actual['version']}, origen "
              f"{actual.get('origen', '—')}")
        for h in actual.get("historial", []):
            print(f"  v{h.get('version')} · {h.get('fecha')} · {_cambio_y_motivo(h.get('cambio'), h.get('motivo'))}")
    else:
        print("El proyecto no tiene estilo (docs/identidad/estilo.json): el generador usa los valores por defecto de un "
              "tema (decisión 323).")
    if prueba:
        print(f"En prueba: {ident / PRUEBA}, origen {prueba.get('origen', '—')}")
        _contar_prueba(prueba, actual, ident)
    else:
        print("Nada en prueba.")


def orden_partir(args) -> None:
    ident = carpeta_identidad(args.raiz)
    estilo = resolver(args.origen, ident)
    if args.cambios:
        estilo = aplicar_cambios(estilo, args.cambios)
    escribir(ident / PRUEBA, estilo)
    print(f"En prueba: {ident / PRUEBA} (origen {estilo['origen']}); estilo.json no cambia hasta aceptarlo.")
    if args.cambios:
        _contar_prueba(estilo, leer(ident / "estilo.json"), ident)
    else:
        for error in contraste(estilo, PRUEBA):
            print(f"  No pasa el contraste: {error}")


def orden_cambiar(args) -> None:
    ident = carpeta_identidad(args.raiz)
    base = leer(ident / PRUEBA) or leer(ident / "estilo.json")
    if base is None:
        sys.exit("No hay estilo ni prueba: primero «partir <tema>».")
    estilo = aplicar_cambios(base, args.cambios)
    escribir(ident / PRUEBA, estilo)
    print(f"En prueba: {ident / PRUEBA}")
    _contar_prueba(estilo, leer(ident / "estilo.json"), ident, antes=base)


def _nombre_archivo(nombre: str) -> str:
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in Path(nombre).stem)


def _dentro(ruta: Path, raiz: Path) -> bool:
    try:
        ruta.resolve().relative_to(raiz.resolve())
        return True
    except ValueError:
        return False


def _leer_lista(ident: Path, raiz: Path) -> list[Path]:
    """Las muestras hechas, como rutas absolutas dentro del proyecto. La lista las guarda relativas a su raíz; una ruta
    que quede fuera (una lista copiada de otro proyecto, una antigua con rutas absolutas) no se toma."""
    lista = ident / LISTA_MUESTRAS
    if not lista.is_file():
        return []
    rutas = []
    for linea in lista.read_text(encoding="utf-8").splitlines():
        if linea.strip():
            ruta = (raiz / linea.strip()).resolve()
            if _dentro(ruta, raiz) and ruta.suffix == ".html" and ruta not in rutas:
                rutas.append(ruta)
    return rutas


def _escribir_lista(ident: Path, raiz: Path, rutas: list[Path]) -> None:
    lista = ident / LISTA_MUESTRAS
    if not rutas:
        lista.unlink(missing_ok=True)
        return
    ident.mkdir(parents=True, exist_ok=True)
    lista.write_text("".join(r.relative_to(raiz.resolve()).as_posix() + "\n" for r in rutas), encoding="utf-8")


def orden_muestras(args) -> None:
    """El mismo documento con cada estilo: «prueba», «actual» (estilo.json), un tema del catálogo o un juego. Cada muestra
    sale junto al documento como <doc>.muestra-<nombre>.html, para que sus imágenes y diagramas se vean. El documento
    tiene que estar dentro del proyecto: las muestras se borran al aceptar o descartar, y fuera de él no se borra nada.
    Si una muestra no se puede rehacer, la anterior con su nombre se borra: ya no dice lo que hay en prueba."""
    ident = carpeta_identidad(args.raiz)
    doc = Path(args.documento).resolve()
    if not doc.is_file():
        sys.exit(f"No encuentro el documento de muestra: {doc}")
    if not _dentro(doc, args.raiz):
        sys.exit(f"El documento de muestra está fuera del proyecto ({doc}): cópialo dentro, con lo que enlaza, y saca las "
                 "muestras de esa copia.")
    nombres = args.nombres or ["prueba"]
    hechas = _leer_lista(ident, args.raiz)
    temporales = []
    try:
        for nombre in nombres:
            if nombre == "prueba":
                ruta_estilo = ident / PRUEBA
            elif nombre == "actual":
                ruta_estilo = ident / "estilo.json"
            else:  # un tema o un juego: resuelto en un archivo aparte, junto a estilo.json (rutas del logo)
                ruta_estilo = ident / f"estilo.muestra-{_nombre_archivo(nombre)}.json"
                escribir(ruta_estilo, resolver(nombre, ident))
                temporales.append(ruta_estilo)
            if not ruta_estilo.is_file():
                sys.exit(f"No hay «{nombre}»: {ruta_estilo}")
            copia = doc.with_name(f"{doc.stem}.muestra-{_nombre_archivo(nombre)}.md")
            shutil.copy2(doc, copia)
            temporales.append(copia)
            orden = [sys.executable, "-I", "-X", "utf8", str(GENERADOR), str(copia), "--estilo", str(ruta_estilo),
                     "--identidad", str(ident) if (ident / "identidad.json").is_file() else "ninguna"]
            if args.perfil:
                orden += ["--perfil", args.perfil]
            r = subprocess.run(orden, capture_output=True, text=True, encoding="utf-8")
            html = copia.with_suffix(".html").resolve()
            if r.returncode != 0:
                print(f"{nombre}: el generador se detiene:\n{(r.stderr or r.stdout).strip()}")
                if html in hechas:
                    html.unlink(missing_ok=True)
                    hechas.remove(html)
                    print(f"  Borrada la muestra anterior de «{nombre}», que ya no dice lo que hay en prueba: {html}")
                elif html.is_file():
                    print(f"  Ojo: {html} no es de esta prueba y no dice lo que hay en ella.")
                continue
            if html not in hechas:
                hechas.append(html)
            print(f"{nombre}: {html}")
    finally:
        for t in temporales:
            t.unlink(missing_ok=True)
        _escribir_lista(ident, args.raiz, hechas)


# --- Catálogo de temas ---------------------------------------------------------------------------------------------------

CATALOGO_ASSETS = AQUI.parent / "assets" / "catalogo"
# El aspecto del propio catálogo es el estilo del proyecto (decisión 353); sin estilo.json, el tema por defecto.
TEMA_POR_DEFECTO = "morado"
# Las vistas de cada muestra: la portada con los botones del menú, los recuadros con la tabla, el diagrama.
VISTAS = (("", "Portada y botones"), ("#recuadros", "Recuadros y tabla"), ("#diagrama", "Diagrama"))
# Con «?modo=oscuro», la muestra abre en el modo oscuro de «Lectura» (347), después de que lectura.js aplique el suyo.
MODO_DE_LA_URL = ("<script>(function(){if(new URLSearchParams(location.search).get('modo')!=='oscuro')return;"
                  "var r=document.documentElement;function o(){r.dataset.modo='oscuro';r.dataset.theme='dark';}"
                  "o();addEventListener('DOMContentLoaded',o);addEventListener('load',o);})();</script>")
CSS_CATALOGO = ("<style>.miniaturas{display:grid;gap:.6rem}.miniatura{display:block;position:relative;width:100%;"
                "max-width:340px;aspect-ratio:960/600;overflow:hidden;border:1px solid var(--borde);"
                "border-radius:var(--esquinas,6px);text-decoration:none}.miniatura iframe{position:absolute;top:0;"
                "left:0;width:960px;height:600px;border:0;transform:scale(.3542);transform-origin:0 0;"
                "pointer-events:none}.miniatura-pie{display:block;font-size:.8rem;color:var(--texto-suave);"
                "margin-top:.2rem}</style>")


def _generar(md: Path, ruta_estilo: Path, ident: Path, *extra: str) -> subprocess.CompletedProcess:
    orden = [sys.executable, "-I", "-X", "utf8", str(GENERADOR), str(md), "--estilo", str(ruta_estilo),
             "--identidad", str(ident) if (ident / "identidad.json").is_file() else "ninguna", *extra]
    return subprocess.run(orden, capture_output=True, text=True, encoding="utf-8")


def _miniaturas(archivo: str) -> str:
    """Las tres vistas de una muestra, cada una en claro y en oscuro: el documento real en un marco reducido."""
    tarjetas = ["::: tarjetas 3", ""]
    for ancla, titulo in VISTAS:
        celdas = []
        for modo, rotulo in (("", "Claro"), ("?modo=oscuro", "Oscuro")):
            src = f"{archivo}{modo}{ancla}"
            celdas.append(f'<div><a class="miniatura" href="{src}" target="_blank" rel="noopener" '
                          f'title="{titulo}, {rotulo.lower()}: abrir la muestra"><iframe src="{src}" loading="lazy" '
                          f'tabindex="-1" scrolling="no" title="{titulo} en {rotulo.lower()}"></iframe></a>'
                          f'<span class="miniatura-pie">{rotulo}</span></div>')
        tarjetas += [f"### {titulo}", "", f'<div class="miniaturas">{"".join(celdas)}</div>', ""]
    return "\n".join(tarjetas + [":::", ""])


def orden_catalogo(args) -> None:
    """El catálogo de temas para elegir el de partida: cada tema del catálogo de crear_documentos genera la misma muestra
    (portada, botones, recuadros, tabla, diagrama, tarjetas) con su estilo resuelto, como haría «partir», y el catálogo
    la enseña en miniatura, en claro y en oscuro, con su contraste. Todo lo hace el generador (305): las miniaturas son
    las propias muestras en un marco reducido. Es un activo del proyecto y se versiona (decisión 352): sale dentro de él,
    en <identidad>/catalogo-temas/ (o en --salida, también dentro), y se rehace al cambiar los temas o el generador."""
    ident = carpeta_identidad(args.raiz)
    salida = (args.salida or ident / "catalogo-temas").resolve()
    if not _dentro(salida, args.raiz):
        sys.exit(f"El catálogo es un activo del proyecto y va dentro de él (decisión 352): {salida} está fuera de "
                 f"{args.raiz}. Sin --salida, sale en {ident / 'catalogo-temas'}.")
    salida.mkdir(parents=True, exist_ok=True)
    filas, secciones, problemas, temporales = [], [], [], []
    for diagrama in ("muestra.diagrama", "catalogo.diagrama"):
        shutil.copy2(CATALOGO_ASSETS / diagrama, salida / diagrama)
        temporales.append(salida / diagrama)
    hechas = []
    try:
        for nombre, estilo, titulo, descripcion, partir in _muestras_del_catalogo(ident):
            hechas.append(f"muestra-{nombre}.html")
            ruta_estilo = ident / f"estilo.catalogo-{nombre}.json"  # junto a estilo.json: valen las rutas del logo
            escribir(ruta_estilo, estilo)
            md = salida / f"muestra-{nombre}.md"
            shutil.copy2(CATALOGO_ASSETS / "muestra.md", md)
            temporales += [ruta_estilo, md]
            errores = contraste(estilo, nombre)
            r = _generar(md, ruta_estilo, ident, "--contraste-avisa")
            if r.returncode != 0:
                sys.exit(f"{nombre}: el generador se detiene:\n{(r.stderr or r.stdout).strip()}")
            html = md.with_suffix(".html")
            html.write_text(html.read_text(encoding="utf-8").replace("</body>", MODO_DE_LA_URL + "\n</body>", 1),
                            encoding="utf-8")
            c = estilo["colores"]
            letra = estilo["letra"]["titulos"].split(",")[0].strip("'\" ")
            portada = estilo["portada"]["forma"] + (f" ({estilo['portada']['fondo']})"
                                                    if estilo["portada"]["forma"] == "oscura" else "")
            filas.append(f"| [{titulo}](#tema-{nombre}) | `{estilo['origen']}` | `{c['primario']}` | {letra} | {portada} | "
                         f"{'no pasa' if errores else 'pasa'} |")
            seccion = [f"## Muestra | {titulo} {{#tema-{nombre}}}", "", descripcion, ""]
            if errores:
                problemas.append(f"- **{titulo}**: " + "; ".join(e.rstrip(".") for e in errores) + ".")
                seccion += ["> [!aviso]", f"> **Contraste insuficiente.** Al partir de {titulo}, el generador se "
                            "detiene hasta corregir: " + "; ".join(errores) + ".", ""]
            seccion += [_miniaturas(html.name)]
            seccion += (["> **Para partir de esta muestra**", f"> `estilo.py partir {partir}`, y después se afina con "
                         f"`cambiar`. [Abrir la muestra entera]({html.name}){{: .salto}}", ""] if partir else
                        ["> **Es el estilo actual**", "> Se afina con `estilo.py cambiar` y se acepta con `aceptar`. "
                         f"[Abrir la muestra entera]({html.name}){{: .salto}}", ""])
            secciones += seccion
        temporales += _escribir_catalogo(salida, ident, filas, secciones, problemas)
        for vieja in salida.glob("muestra-*.html"):  # las de un catálogo anterior que ya no salen
            if vieja.name not in hechas:
                vieja.unlink()
    finally:
        for t in temporales:
            t.unlink(missing_ok=True)


def _color_del_proyecto(ident: Path) -> str | None:
    """El color del proyecto sin estilo.json, para la séptima muestra: el del tema de su identidad.json o su color de
    sesión (.sf/proyecto.json)."""
    identidad = ident / "identidad.json"
    if identidad.is_file():
        tema = json.loads(identidad.read_text(encoding="utf-8")).get("tema")
        ruta = ident / tema if tema and tema.endswith(".json") else TEMAS / f"{tema}.json" if tema else None
        if ruta and ruta.is_file():
            return json.loads(ruta.read_text(encoding="utf-8"))["colores"]["primario"]
    color = ep.color_del_proyecto(ident / "x.md")
    color = ep.COLORES_SESION.get(color, color) if color else None
    return color if color and ep._hex(color) else None


def _muestras_del_catalogo(ident: Path):
    """(nombre, estilo, título, descripción, lo que se pasa a «partir»): las seis del plugin, una por tema (335, 6), y
    la séptima: el estilo del proyecto tal cual si ya lo tiene; si no, «tinta» con su color, si lo tiene."""
    for nombre, juego in juegos().items():
        tema = json.loads((TEMAS / f"{juego['origen']}.json").read_text(encoding="utf-8"))
        descripcion = (f"{juego['caracter']}. Parte del tema `{juego['origen']}`: "
                       + tema.get("descripcion", "").split(". ")[0].rstrip(".") + ".")
        yield nombre, resolver_juego(nombre, ident), f"{juego['muestra']} · {juego['nombre']}", descripcion, nombre
    actual = leer(ident / "estilo.json")
    if actual:  # el estilo del proyecto tal cual, con su portada, sus logos y todo lo afinado
        version = actual.get("version", 1)
        titulo = (f"G · {actual['nombre']} (estilo del proyecto, v{version})" if actual.get("nombre")
                  else f"G · Estilo del proyecto (v{version})")
        yield ("proyecto", actual, titulo,
               f"El estilo de este proyecto, `estilo.json` tal cual: parte de `{actual.get('origen', '—')}` y lleva "
               "todo lo afinado. Es el que ya usan sus documentos; se cambia con `cambiar`.", None)
        return
    color = _color_del_proyecto(ident)
    if color:
        base = resolver_tema("tinta", ident)
        cambio = f"colores.primario={color} colores.sobre-primario={sobre(color, base['colores']['texto'])}"
        estilo = aplicar_cambios(base, cambio.split())
        yield ("proyecto", estilo, "G · Color del proyecto",
               f"El tema `tinta` con el color del proyecto, `{color}`, y su familia derivada (338).", f"tinta {cambio}")


def _escribir_catalogo(salida: Path, ident: Path, filas: list, secciones: list, problemas: list) -> list[Path]:
    """Genera catalogo-temas.html con el estilo del proyecto (353) o, sin él, el tema por defecto, con las secciones
    abiertas (un marco dentro de una sección plegada no se coloca en su vista); devuelve los archivos de paso."""
    hoy = datetime.date.today().strftime("%d/%m/%Y")
    resumen = ["## Resumen | Las muestras de un vistazo {#resumen}", "",
               f"Las {len(filas)} muestras salen con el mismo documento, cada una con su estilo de partida: una por "
               "tema del catálogo, con una forma propia para que se distingan también por la portada y las cabeceras, "
               "y la última, el estilo del proyecto tal cual o, si aún no lo tiene, `tinta` con su color (decisión 335). Es lo que daría `estilo.py partir` con su nombre, "
               "antes de afinarlo. Se elige la que más se acerca y se ajusta después con sus parámetros.", "",
               "| Muestra | Tema | Primario | Letra de los títulos | Portada | Contraste |",
               "| --- | --- | --- | --- | --- | --- |", *filas, "", "![](catalogo.diagrama)", ""]
    revela = ["## Contraste | Lo que revelan las muestras {#contraste}", ""]
    revela += (["Estas muestras no pasan la comprobación de contraste del generador (decisión 320): se ven en el catálogo, "
                "pero al partir de ellas hay que corregir esos colores antes de generar.", "", *problemas, ""]
               if problemas else ["Todas las muestras pasan la comprobación de contraste del generador, en claro y en "
                                  "oscuro (decisión 320).", ""])
    md = "\n".join([
        "---", "antetitulo: Estilo de los documentos del proyecto",
        "lema: Un vistazo a cada tema // antes de partir de él.",
        "subtitulo: Una muestra por tema, y otra con el color del proyecto, en modo claro y en modo oscuro.",
        f"version: Generado el {hoy}", "estado: Catálogo", "destino: proyecto", "herramientas: recomendadas",
        "pie: Las miniaturas son las propias muestras del generador; un clic abre cada una entera.", "---",
        "# Catálogo de temas", "",
        "> **Cómo se usa**",
        "> Se mira cada muestra en claro y en oscuro (el modo oscuro es el de «Lectura»), se abre entero el que encaje y se "
        "parte de él con `estilo.py partir` y su nombre. Nada de esto cambia el estilo del proyecto.", "",
        CSS_CATALOGO, "", *resumen, *secciones, *revela])
    archivo = salida / "catalogo-temas.md"
    archivo.write_text(md, encoding="utf-8")
    actual = leer(ident / "estilo.json")
    estilo = json.loads(json.dumps(actual)) if actual else resolver_tema(TEMA_POR_DEFECTO, ident)
    estilo.setdefault("secciones", {})["plegado"] = "todas"
    ruta_estilo = ident / "estilo.catalogo.json"  # junto a estilo.json, para que valgan las rutas del logo
    escribir(ruta_estilo, estilo)
    r = _generar(archivo, ruta_estilo, ident)
    if r.returncode != 0:
        archivo.unlink(missing_ok=True)
        ruta_estilo.unlink(missing_ok=True)
        sys.exit(f"El catálogo: el generador se detiene:\n{(r.stderr or r.stdout).strip()}")
    print(f"Catálogo de temas: {archivo.with_suffix('.html')}\n  Es un activo del proyecto: se sube a git con sus "
          "muestras (decisión 352).")
    if problemas:
        print("Contraste insuficiente:\n  " + "\n  ".join(problemas))
    return [archivo, ruta_estilo]


def _cambio_de_partida(prueba: dict, ident: Path) -> str:
    """La línea «cambio» de la versión 1: de qué tema parte y, si se tocó, cuántos valores cambian frente a él."""
    origen = prueba.get("origen")
    base = _estilo_del_origen(prueba, ident)
    cambios = diferencias(base, prueba) if base else []
    texto = f"estilo de partida desde {origen}" if origen else "estilo de partida"
    if len(cambios) == 1:
        texto += f", con {cambios[0]}"
    elif cambios:
        texto += f", con {len(cambios)} valores cambiados"
    return texto


def _cambio_y_motivo(cambio, motivo) -> str:
    """«cambio · motivo», sin repetir el motivo si dice lo mismo que el cambio."""
    if not motivo or str(motivo).strip().lower() == str(cambio).strip().lower():
        return str(cambio)
    return f"{cambio} · {motivo}"


def _borrar_prueba(ident: Path, raiz: Path) -> list[str]:
    """Borra la prueba y sus muestras; solo dentro del proyecto."""
    borrados = []
    for ruta in _leer_lista(ident, raiz):
        if ruta.is_file():
            ruta.unlink()
            borrados.append(str(ruta))
    (ident / LISTA_MUESTRAS).unlink(missing_ok=True)
    if (ident / PRUEBA).is_file():
        (ident / PRUEBA).unlink()
        borrados.append(str(ident / PRUEBA))
    return borrados


def orden_aceptar(args) -> None:
    ident = carpeta_identidad(args.raiz)
    prueba = leer(ident / PRUEBA)
    if prueba is None:
        sys.exit("No hay nada en prueba: «partir» o «cambiar» primero.")
    errores = contraste(prueba, PRUEBA)
    if errores:
        sys.exit("No se acepta: el generador se detendría con estos textos (decisión 320):\n  " + "\n  ".join(errores))
    ruta = ident / "estilo.json"
    actual = leer(ruta)
    cambios = diferencias(actual or {}, prueba)
    if actual and not cambios:
        sys.exit("La prueba es igual que el estilo del proyecto: no hay nada que aceptar.")
    hoy = args.fecha or datetime.date.today().isoformat()
    if actual:
        respaldo = ident / "_respaldo" / f"estilo_v{actual['version']}.json"
        if respaldo.exists():
            sys.exit(f"Ya hay un respaldo de la versión {actual['version']}: {respaldo}. No se toca nada.")
        respaldo.parent.mkdir(exist_ok=True)
        shutil.copy2(ruta, respaldo)
        version, historial = actual["version"] + 1, list(actual.get("historial", []))
        cambio = args.cambio or "; ".join(cambios)
        origen = actual.get("origen", prueba.get("origen"))
    else:
        respaldo, version, historial = None, 1, []
        cambio = args.cambio or _cambio_de_partida(prueba, ident)
        origen = prueba.get("origen")
    historial.append({"version": version, "fecha": hoy, "cambio": cambio, "motivo": args.motivo})
    nuevo = {"version": version, "origen": origen, "historial": historial,
             **{k: v for k, v in prueba.items() if k not in ("version", "origen", "historial")}}
    if nuevo["origen"] is None:
        del nuevo["origen"]
    ep.validar(nuevo, ruta)
    escribir(ruta, nuevo)
    _borrar_prueba(ident, args.raiz)
    print(f"Estilo v{version}: {ruta}" + (f" (la v{version - 1}, en {respaldo})" if respaldo else ""))
    print(f"  {_cambio_y_motivo(cambio, args.motivo)}")


def orden_descartar(args) -> None:
    borrados = _borrar_prueba(carpeta_identidad(args.raiz), args.raiz)
    print("Borrado: " + ", ".join(borrados) if borrados else "Nada en prueba.")


def main() -> None:
    ap = argparse.ArgumentParser(description="Fija y afina el estilo de los documentos del proyecto con muestras.")
    ap.add_argument("--raiz", type=Path, default=Path.cwd(), help="carpeta del proyecto (por defecto, la actual)")
    sub = ap.add_subparsers(dest="orden", required=True)
    sub.add_parser("parametros", help="catálogo de parámetros del generador").set_defaults(f=orden_parametros)
    sub.add_parser("ver", help="estilo del proyecto y lo que está en prueba").set_defaults(f=orden_ver)
    p = sub.add_parser("partir", help="pone en prueba un estilo completo desde un tema o un juego")
    p.add_argument("origen", help="tema del catálogo de crear_documentos o ruta a un juego (.json)")
    p.add_argument("cambios", nargs="*", help="grupo.clave=valor sobre el tema")
    p.set_defaults(f=orden_partir)
    p = sub.add_parser("cambiar", help="cambia valores del estilo en prueba")
    p.add_argument("cambios", nargs="+", help="grupo.clave=valor; «grupo.clave=» lo quita")
    p.set_defaults(f=orden_cambiar)
    p = sub.add_parser("muestras", help="genera el documento con cada estilo")
    p.add_argument("documento", help=".md del documento de muestra")
    p.add_argument("nombres", nargs="*", help="prueba (por defecto), actual, un tema o un juego (.json)")
    p.add_argument("--perfil", default=None, help="perfil.json del tipo de documento")
    p.set_defaults(f=orden_muestras)
    p = sub.add_parser("aceptar", help="lleva la prueba a estilo.json")
    p.add_argument("--motivo", required=True, help="por qué, en pocas palabras (va al historial)")
    p.add_argument("--cambio", default=None, help="qué cambia; por defecto, la lista de parámetros cambiados")
    p.add_argument("--fecha", default=None, help=argparse.SUPPRESS)
    p.set_defaults(f=orden_aceptar)
    sub.add_parser("descartar", help="borra la prueba y sus muestras").set_defaults(f=orden_descartar)
    p = sub.add_parser("catalogo", help="catálogo de temas en miniatura, en claro y en oscuro, para elegir el de partida")
    p.add_argument("--salida", type=Path, default=None, help="carpeta dentro del proyecto; por defecto, <identidad>/catalogo-temas/")
    p.set_defaults(f=orden_catalogo)
    args = ap.parse_args()
    args.raiz = args.raiz.resolve()
    args.f(args)


if __name__ == "__main__":
    main()
