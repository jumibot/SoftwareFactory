"""Pruebas de la skill diagramas: el cálculo de contraste del comprobador y, con un navegador, que el ejemplo pasa
y que una página mala da cada error.

python -I -X utf8 -m unittest discover -s plugins/sf/tests -p "test_diagramas.py"
"""
import importlib.util
import re
import shutil
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / 'skills' / 'diagramas'
spec = importlib.util.spec_from_file_location('comprobar_diagramas', SKILL / 'scripts' / 'comprobar_diagramas.py')
cd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cd)


def hay_navegador() -> bool:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            cd.navegador(pw).close()
        return True
    except BaseException:  # noqa: BLE001 — sin Playwright o sin navegador, se saltan
        return False


class Contraste(unittest.TestCase):
    def test_blanco_y_negro(self):
        self.assertAlmostEqual(cd.contraste((0, 0, 0), (255, 255, 255)), 21, places=2)

    def test_gris_del_tema(self):
        # --texto-suave #555 sobre blanco: 7,46:1
        self.assertAlmostEqual(cd.contraste((0x55,) * 3, (255, 255, 255)), 7.46, places=2)

    def test_composicion_y_pila(self):
        self.assertEqual(cd.componer((0, 0, 0, 0.5), (255, 255, 255)), (127.5, 127.5, 127.5))
        fondo = cd.fondo_de([(0xe0, 0xf4, 0xf3, 1)], (255, 255, 255, 1))
        self.assertEqual(fondo, (0xe0, 0xf4, 0xf3))

    def test_texto_grande(self):
        self.assertTrue(cd.texto_grande(24, 400))
        self.assertTrue(cd.texto_grande(19, 700))
        self.assertFalse(cd.texto_grande(19, 600))


TEMAS = SKILL.parent / 'crear_documentos'
FUNDACIONAL = SKILL.parent / 'documento_fundacional' / 'scripts' / 'fundacional_to_html.py'
DOCUMENTO = SKILL.parent / 'crear_documentos' / 'scripts' / 'documento_a_html.py'


class TemaTinta(unittest.TestCase):
    """El tema tinta, la paleta de diagram-design, en claro y en oscuro (tema de referencia de los diagramas)."""

    def setUp(self):
        import sys
        sys.path.insert(0, str(TEMAS / 'scripts'))
        import tema_identidad
        self.ti = tema_identidad
        self.tema = tema_identidad.cargar_tema('tinta')

    def test_carga_con_sus_dos_versiones(self):
        c, o = self.tema['colores'], self.tema['colores-oscuro']
        self.assertEqual((c['primario'], c['texto'], c['pagina']), ('#b8431c', '#25283a', '#fbfbfa'))
        self.assertEqual((o['primario'], o['texto'], o['pagina']), ('#f08a59', '#f2f2f0', '#1b1d2c'))
        self.assertEqual(set(c), {r for r, _, _ in self.ti.ROLES} | set(self.ti.ROLES_PROPIOS))
        self.assertEqual(set(o), set(c))  # la oscura, completa: lo que el tema no da, derivado (decisión 348)
        self.assertEqual(o['tinta-oscura'], '#f2f2f0')  # la tinta fuerte, clara en oscuro (349)
        self.assertGreaterEqual(cd.contraste((255, 255, 255), tuple(int(o['oscuro'][i:i + 2], 16) for i in (1, 3, 5))), 4.5)
        css = self.ti.variables_css(self.tema)
        self.assertIn('--primario: #b8431c;', css)
        self.assertIn(':root[data-theme="dark"] { --primario: #f08a59;', css)

    def test_contraste_de_los_textos(self):
        h = lambda x: tuple(int(x[i:i + 2], 16) for i in (1, 3, 5))
        for colores in (self.tema['colores'], self.tema['colores-oscuro']):
            for fondo in ('pagina', 'fondo-suave'):
                for texto in ('texto', 'texto-suave', 'texto-tenue', 'primario', 'acento', 'tinta-oscura'):
                    k = cd.contraste(h(colores[texto]), h(colores[fondo]))
                    self.assertGreaterEqual(k, 4.5, f'{texto} sobre {fondo}: {k:.2f}')

    def test_un_rol_oscuro_raro_se_rechaza(self):
        import json
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / 'raro.json'
            ruta.write_text(json.dumps({'colores': {'primario': '#b8431c'}, 'colores-oscuro': {'inventado': '#000000'}}), encoding='utf-8')
            with self.assertRaises(SystemExit):
                self.ti.cargar_tema(str(ruta))

    def test_el_generador_lo_acepta(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as d:
            md = Path(d) / 'doc.md'
            md.write_text('---\ndestino: proyecto\nherramientas: ninguna\n---\n# Prueba\n\n## Uno | Primera {#uno}\n\nTexto.\n',
                          encoding='utf-8')
            r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(FUNDACIONAL), str(md), '--tema', 'tinta',
                                '--identidad', 'ninguna', '--logo', 'ninguno'], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            html = md.with_suffix('.html').read_text(encoding='utf-8')
        self.assertIn('--primario: #b8431c;', html)
        self.assertIn('Instrument+Serif', html)


spec_g = importlib.util.spec_from_file_location('generar_diagrama', SKILL / 'scripts' / 'generar_diagrama.py')
gd = importlib.util.module_from_spec(spec_g)
spec_g.loader.exec_module(gd)
EJEMPLOS = sorted((SKILL / 'assets' / 'ejemplos').glob('*.diagrama'))


# «Cómo se testea hoy» (tarea 474), con lo fijado antes de dibujar: objetivo, concepto y puntos clave (decisiones 385 y 387)
HOY = chr(10).join([
    'tipo: proceso', 'titulo: Cómo se testea hoy',
    'objetivo: Que el propietario vea por qué hoy se gastan tantos tokens al probar.',
    'concepto: Al acabar una vuelta, el subagente lanza a mano una orden por comprobación y, según el resultado, la repite, espera o lee su salida entera.',
    'puntos-clave:',
    '  Cada comprobación es una orden a mano. | vuelta > pruebas',
    '  Un fallo o un cambio vuelve a lanzar lo ya pasado. | pruebas > repetir > pruebas',
    '  Las lentas obligan a esperar. | pruebas > espera',
    'modulos-clave: vuelta, pruebas, repetir, espera, leer',
    'interconexiones-clave:', '  pruebas > repetir > pruebas',
    'nodos:', '  vuelta: Acabar la vuelta', '  pruebas: Lanzar a mano', '  repetir: ¿Falló o cambió? | dec',
    '  espera: Esperar a las lentas', '  leer: Leer la salida',
    'flechas:', '  inicio > vuelta', '  vuelta > pruebas: 6 DE MEDIA', '  pruebas > repetir: RESULTADO',
    '  repetir > pruebas: REPITE | rojo, vuelta', '  pruebas > espera: LENTA', '  pruebas > leer: SALIDA ENTERA'])


class Concepto(unittest.TestCase):
    """Lo fijado antes de dibujar, por escrito en los datos, y lo que el generador comprueba con ello (decisiones 385 y 387)."""

    def errores(self, texto, exigir=True, base=Path('.')):
        return gd.concepto(gd.modelo(gd.leer(texto)), base, exigir)

    def test_sin_objetivo_concepto_ni_puntos_clave_no_genera_si_se_exige(self):
        sin = chr(10).join(x for x in HOY.split(chr(10)) if not x.startswith(('objetivo', 'concepto', 'puntos-clave', '  Cada', '  Un fallo', '  Las lentas')))
        errores, avisos = self.errores(sin)
        self.assertEqual(len(errores), 1)
        self.assertIn('«objetivo:», «concepto:», «puntos-clave:»', errores[0])
        self.assertEqual(self.errores(sin, exigir=False)[0], [])            # sin exigir, un aviso
        self.assertEqual(self.errores(HOY)[0], [])
        with tempfile.TemporaryDirectory() as d:
            datos = Path(d) / 't.diagrama'
            datos.write_text(sin, encoding='utf-8')
            self.assertEqual(gd.main([str(datos), '--exigir', '--sin-comprobar']), 2)
            self.assertFalse((Path(d) / 't.html').exists())

    def test_el_dibujo_que_contradice_lo_fijado_es_un_error(self):
        # carpetas inventadas, el bucle perdido y un punto clave sin dónde: lo que pasó al rehacer «Cómo se testea hoy»
        mal = (HOY.replace('  repetir > pruebas: REPITE | rojo, vuelta' + chr(10), '')
                  .replace('  Las lentas obligan a esperar. | pruebas > espera', '  Las lentas obligan a esperar.')
                  .replace('nodos:', 'zonas:' + chr(10) + '  elegir: ELEGIR A MANO | vuelta, pruebas, repetir' + chr(10) + 'nodos:'))
        errores = ' / '.join(self.errores(mal)[0])
        self.assertIn('la carpeta «elegir» no es un módulo clave', errores)
        self.assertIn('el bucle «pruebas → repetir → pruebas» no aparece: falta «repetir > pruebas»', errores)
        self.assertIn('el punto clave «Un fallo o un cambio vuelve a lanzar lo ya pasado.» no aparece', errores)
        self.assertIn('el punto clave «Las lentas obligan a esperar.» no dice dónde se ve', errores)

    def test_rehacerlo_conserva_el_concepto_del_de_antes(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / 'antes.diagrama').write_text(HOY, encoding='utf-8')
            igual = HOY + chr(10) + 'opciones: cajas=plegadas'
            self.assertEqual(self.errores(igual.replace('tipo: proceso', 'tipo: proceso' + chr(10) + 'antes: antes.diagrama'), base=Path(d))[0], [])
            # por ids: un rótulo mejor no cambia el concepto; una decisión que pasa a acción, una caja menos o una
            # etiqueta cambiada, sí (el piloto de la 474)
            con_antes = lambda t: t.replace('tipo: proceso', 'tipo: proceso' + chr(10) + 'antes: antes.diagrama')
            self.assertEqual(self.errores(con_antes(HOY.replace('Esperar a las lentas', 'Vigilar los tests lentos')), base=Path(d))[0], [])
            otro = con_antes(HOY.replace('¿Falló o cambió? | dec', 'Relanzar lo que ya pasó').replace('vuelta > pruebas: 6 DE MEDIA', 'vuelta > pruebas: A MANO')
                             .replace('  leer: Leer la salida' + chr(10), '').replace('  pruebas > leer: SALIDA ENTERA', '').replace(', leer', ''))
            errores = ' / '.join(self.errores(otro, base=Path(d))[0])
            self.assertIn('faltan pasos del concepto: «Leer la salida»', errores)
            self.assertIn('faltan decisiones del concepto: «Relanzar lo que ya pasó»', errores)
            self.assertIn('decía «6 DE MEDIA» y ahora «A MANO»', errores)
            self.assertEqual(gd.comparar_grafos(gd.modelo(gd.leer(HOY)), gd.modelo(gd.leer(HOY.replace('  repetir > pruebas: REPITE | rojo, vuelta' + chr(10), '')))),
                             ['faltan flechas del concepto: «¿Falló o cambió? → Lanzar a mano»',
                              'faltan bucles del concepto: «Lanzar a mano → ¿Falló o cambió?»'])


class Rotulos(unittest.TestCase):
    """Quién hace qué con las palabras del glosario (decisiones 422 y 423), con los esquemas de la prueba piloto (474)."""

    def avisos(self, nombre):
        ruta = Path(__file__).parent / 'diagramas' / f'{nombre}.diagrama'
        m = gd.modelo(gd.leer(ruta.read_text(encoding='utf-8')))
        return gd.concepto(m, ruta.parent)[1]

    def test_un_modo_en_vez_de_verbo_y_objeto(self):
        avisos = ' / '.join(gd.rotulos(gd.modelo(gd.leer(HOY.replace('Lanzar a mano', 'Elegir a ojo')))))
        self.assertIn('«Elegir a ojo» dice cómo («a ojo»)', avisos)
        self.assertNotIn('«Acabar la vuelta»', avisos)

    def test_lo_que_dudaron_las_lecturas_en_frio(self):
        hoy = ' / '.join(self.avisos('piloto-hoy'))
        self.assertIn('no dice cuándo acaba', hoy)                                  # el bucle sin salida
        self.assertIn('«Vigilar en segundo plano» no vuelve al camino', hoy)        # la rama sin final
        # el glosario inspira, no obliga (decisión 426): ni palabras de fuera ni términos sin usar
        self.assertNotIn('no están en el glosario', hoy)
        m = gd.modelo(gd.leer((Path(__file__).parent / 'diagramas' / 'piloto-propuesta.diagrama').read_text(encoding='utf-8')))
        uno = gd.modelo(gd.leer(chr(10).join(['tipo: proceso', 'glosario:', '  orden | lo que se lanza', 'nodos:', '  a: Lanzar la orden',
                                              '  b: Leer la salida', 'flechas:', '  inicio > a', '  a > b'])))
        uno['id'] = 'uno'
        self.assertNotIn('data-glosario', gd.figura(uno)[0])
        self.assertIn('Glosario:', gd.lectura(m))                                 # la lectura en frío lo tiene delante
        sin = ' / '.join(self.avisos('piloto-sin-propuesta'))
        self.assertIn('la etiqueta «CADA TEST DICE QUÉ CUBRE» explica', sin)
        self.assertIn('no habla de «detectar», su id', sin)
        self.assertIn('la discontinua tiene dos sentidos', sin)

    def test_el_actor_donde_cambia_y_el_glosario_compartido(self):
        texto = (Path(__file__).parent / 'diagramas' / 'piloto-propuesta.diagrama').read_text(encoding='utf-8')
        m = gd.modelo(gd.leer(texto))
        self.assertEqual(m['actores'], ['subagente', 'comprobar.py'])
        self.assertFalse(any('¿quién?' in a or 'en el título de casi todos' in a for a in gd.rotulos(m)))
        todos = gd.modelo(gd.leer(texto.replace('Ronda 1: seleccionar tests', 'comprobar.py selecciona tests')
                                  .replace('Saltar lo que ya pasó', 'comprobar.py salta lo que ya pasó')
                                  .replace('Ronda 2: ejecutar a la vez', 'comprobar.py ejecuta')
                                  .replace('Devolver el resumen', 'comprobar.py devuelve el resumen')))
        self.assertTrue(any('en el título de casi todos' in a for a in gd.rotulos(todos)))
        with tempfile.TemporaryDirectory() as d:
            for x in ('piloto-hoy', 'piloto-propuesta'):
                t = (Path(__file__).parent / 'diagramas' / f'{x}.diagrama').read_text(encoding='utf-8')
                (Path(d) / f'{x}.diagrama').write_text(t.replace('  captura | Imagen', '  imagen | Imagen') if x == 'piloto-hoy' else t, encoding='utf-8')
            avisos = gd.concepto(gd.modelo(gd.leer((Path(d) / 'piloto-hoy.diagrama').read_text(encoding='utf-8'))), Path(d))[1]
            self.assertTrue(any('el glosario no es el mismo que el de piloto-propuesta.diagrama' in a for a in avisos), avisos)

    def test_la_idea_no_todo_el_detalle(self):
        # el piloto de un esquema de la tarea 475: diez cajas con los códigos de la respuesta; el del informe, cinco
        avisos = ' / '.join(self.avisos('piloto-475'))
        self.assertIn('10 cajas: ¿la versión más simple que transmite el objetivo?', avisos)
        self.assertIn('«401 CADUCADO» lleva un código o una cifra («401»)', avisos)
        self.assertIn('«REINTENTA 10 S» lleva un código o una cifra', avisos)
        self.assertNotIn('cajas: ¿la versión más simple', ' / '.join(self.avisos('piloto-hoy')))

    def test_sin_punto_de_inicio(self):
        # en el piloto, una propuesta dibujada desde cero perdió «inicio > detectar» sin que nada lo dijera
        texto = (Path(__file__).parent / 'diagramas' / 'piloto-propuesta.diagrama').read_text(encoding='utf-8')
        self.assertFalse(any('sin punto de inicio' in a for a in gd.rotulos(gd.modelo(gd.leer(texto)))))
        sin = gd.modelo(gd.leer(texto.replace('  inicio > detectar' + chr(10), '')))
        self.assertTrue(any('sin punto de inicio' in a for a in gd.rotulos(sin)))

    def test_la_estructura_sale_del_concepto(self):
        # el piloto desde cero: «¿Falló o cambió?» pasó a acción y el bucle salía de ella; «Vigilar lo lento», al final
        sin = ' / '.join(self.avisos('piloto-sin-hoy'))
        self.assertIn('vuelve desde una acción', sin)
        hoy = ' / '.join(self.avisos('piloto-hoy'))
        self.assertIn('«Relanzar lo que ya pasó» es una condición', hoy)
        texto = (Path(__file__).parent / 'diagramas' / 'piloto-hoy.diagrama').read_text(encoding='utf-8')
        m = gd.modelo(gd.leer(texto.replace('compara-con:', 'decisiones: repetir' + chr(10) + 'compara-con:')))
        self.assertIn('«Relanzar lo que ya pasó» es una decisión del concepto', ' / '.join(gd.concepto(m, Path(__file__).parent / 'diagramas')[0]))
        m['id'] = 'p'
        with self.assertRaisesRegex(gd.Error, 'acorta los rótulos para que quepa al lado'):
            gd.dibujar(m, 'v')
        self.assertFalse(any('vuelve desde una acción' in a or 'es una condición' in a for a in self.avisos('hoy')))

    def test_lo_que_sale_del_camino_va_al_lado(self):
        # el piloto de la 475: «Copiar y pegar en el chat» (la rama del token caducado) y «Abrir desde el disco» no
        # cabían al lado y los dos dibujantes los bajaron al eje con «una-columna»
        texto = (Path(__file__).parent / 'diagramas' / 'piloto-475.diagrama').read_text(encoding='utf-8')
        m = gd.modelo(gd.leer(texto))
        self.assertEqual(gd.ramas_finales(m), ['copiar', 'disco'])
        m['id'], m['exigir'] = 'p', True          # con --exigir, el dibujante; sin él, un aviso
        with self.assertRaisesRegex(gd.Error, 'sale del camino y acaba fuera de él: al lado, no en el eje'):
            gd.dibujar(m, 'v')
        m = gd.modelo(gd.leer(texto.replace('opciones: completo, una-columna', 'opciones: completo')))
        m['id'] = 'p'
        with self.assertRaisesRegex(gd.Error, '«Copiar y pegar en el chat, Abrir desde el disco» sale del camino: acorta los rótulos'):
            gd.dibujar(m, 'v')
        # el final del camino al que también se llega de una decisión no es una rama: «Devolver el resumen»
        m = gd.modelo(gd.leer((Path(__file__).parent / 'diagramas' / 'piloto-propuesta.diagrama').read_text(encoding='utf-8')))
        self.assertNotIn('resumen', gd.ramas_finales(m))

    def test_un_bucle_clave_por_un_camino_del_dibujo(self):
        # en el piloto, «num > enviar > num» no se podía declarar: de enviar a num hay un camino, no una flecha
        texto = (Path(__file__).parent / 'diagramas' / 'piloto-475.diagrama').read_text(encoding='utf-8')
        m = gd.modelo(gd.leer(texto.replace('  num > enviar' + chr(10) + '  tok > copiar', '  num > enviar > num' + chr(10) + '  tok > copiar', 1)))
        self.assertEqual(gd.concepto(m, Path('.'))[0], [])
        m = gd.modelo(gd.leer(texto.replace('  num > enviar' + chr(10) + '  tok > copiar', '  num > chat > num' + chr(10) + '  tok > copiar', 1)))
        self.assertTrue(any('el bucle «num → chat → num» no aparece: falta «chat > num»' in e for e in gd.concepto(m, Path('.'))[0]))

    def test_la_lectura_en_frio_solo_lo_que_se_ve(self):
        texto = gd.lectura(gd.modelo(gd.leer((Path(__file__).parent / 'diagramas' / 'piloto-hoy.diagrama').read_text(encoding='utf-8'))))
        self.assertTrue(texto.startswith('Glosario:'))
        self.assertIn('- Decidir qué tests lanzar (el subagente, sin mirar lo cambiado ni caché)', texto)
        self.assertIn('- Leer la salida entera → Relanzar lo que ya pasó: FALLA O CAMBIA', texto)
        self.assertNotIn('Que se vea', texto)                           # ni el objetivo
        self.assertNotIn('137.000 tokens en la SF', texto.split('Cajas:')[1])   # ni las fichas


class Generador(unittest.TestCase):
    """El generador: datos breves → figura con su vertical y su horizontal, mismos ids, fichas y tema."""

    def figura(self, texto):
        m = gd.modelo(gd.leer(texto))
        m['id'] = 'p'
        return gd.figura(m)

    def test_hay_un_ejemplo_por_tipo(self):
        self.assertEqual({p.stem for p in EJEMPLOS}, set(gd.TIPOS))

    def test_las_dos_formas_con_los_mismos_ids(self):
        import re
        for ruta in EJEMPLOS:
            with self.subTest(ruta.stem):
                html, dib, errores = self.figura(ruta.read_text(encoding='utf-8'))
                self.assertEqual(set(dib), {'v', 'h'}, errores)
                svgs = re.findall(r'<svg .*?</svg>', html)
                ids = [sorted(set(re.findall(r'data-nodo="([\w-]+)"', x))) for x in svgs]
                self.assertEqual(ids[0], ids[1])
                self.assertIn('data-diagrama', html)
                self.assertIn('data-ficha=', html)
                self.assertIn('<div class="d-fichas" hidden>', html)   # las fichas, solo para el HUD: sin lista debajo
                self.assertNotIn('<details', html)
                for c in gd.VARIANTES['cajas']:
                    for f in gd.VARIANTES['forma']:
                        self.assertIn(f'data-cajas="{c}" data-forma="{f}" class="vertical', html)

    def test_cajas_plegadas_y_croqueta(self):
        import re
        m = gd.modelo(gd.leer((SKILL / 'assets' / 'ejemplos' / 'estados.diagrama').read_text(encoding='utf-8')))
        m['id'] = 'p'
        for o in ('v', 'h'):
            with self.subTest(o):
                normal, plegada = gd.dibujar(m, o), gd.dibujar(m, o, 'plegadas')
                self.assertLess(plegada.H, normal.H)                       # más compacta, no solo sin texto
                self.assertLess(plegada.cajas['curso'].h, normal.cajas['curso'].h)
                self.assertNotIn('class="d-sb"', ''.join(plegada.nodos))
                croqueta = gd.dibujar(m, o, 'desplegadas', 'croqueta')
                c, r = croqueta.cajas['curso'], croqueta.radio['curso']
                self.assertEqual(r, c.h / 2)
                # cada flecha que llega a una caja toca su borde redondeado: el extremo, dentro de la caja y a 2 o menos
                for d in re.findall(r'data-a="(\w+)" d="[^"]*L([\d.]+),([\d.]+)"', ''.join(croqueta.flechas)):
                    b, x, y = croqueta.cajas[d[0]], float(d[1]), float(d[2])
                    rr = croqueta.radio.get(d[0], 0)
                    if rr and b.x <= x <= b.r and (y <= b.cy):
                        # llega por arriba (al borde de arriba) o por la izquierda (al lado redondo)
                        dx = max(b.x + rr - x, x - (b.r - rr), 0)
                        arriba = b.y + rr - (rr * rr - min(dx, rr) ** 2) ** .5
                        dy = max(b.y + rr - y, y - (b.b - rr), 0)
                        izquierda = b.x + rr - (rr * rr - min(dy, rr) ** 2) ** .5
                        self.assertTrue(abs(y - (arriba - 2)) <= .6 or abs(x - (izquierda - 2)) <= .6, msg=d)

    def test_estados_como_la_sintesis(self):
        html = self.figura((SKILL / 'assets' / 'ejemplos' / 'estados.diagrama').read_text(encoding='utf-8'))[0]
        self.assertIn('data-de="curso" data-a="cerr"', html)               # CERRAR desde En curso
        self.assertIn('d-etiqueta d-b-verde', html)                         # botón sin color: verde
        self.assertIn('Desde en observación o cerradas', html)   # la mono la pone en mayúsculas
        self.assertIn('class="d-nota-c"', html)
        self.assertNotIn('d-b-verde">sin trabajo', html)                    # lo que hace Claude no es un botón
        # ajustes por defecto nuevos, y cada caja con detalle, plegable sola
        for k, v in (('cajas', 'desplegadas'), ('forma', 'redondeada'), ('borde', 'fino'), ('fondo', 'papel'),
                     ('recorrido', 'segundo'), ('lienzo', 'papel')):
            self.assertIn(f'data-d-{k}="{v}"', html)
        self.assertNotIn('d-no-tarjeta', html)
        self.assertIn('data-plegar="curso"', html)
        self.assertIn('class="d-sb d-plegado"', html)                       # el detalle de las plegadas, oculto
        self.assertIn('data-d-cajas="acordeon"', self.figura('opciones: cajas=acordeon\n' + (SKILL / 'assets' / 'ejemplos' / 'estados.diagrama').read_text(encoding='utf-8'))[0])

    def test_recorrido_paso_a_paso(self):
        """El replay: cada paso, un nodo o una flecha con su porqué, en .d-pasos; la figura, en el modo recorrer."""
        html = self.figura((SKILL / 'assets' / 'ejemplos' / 'proceso.diagrama').read_text(encoding='utf-8'))[0]
        self.assertIn('data-modo="recorrer"', html)
        self.assertIn('<div class="d-pasos" hidden><div data-paso-nodo="eleg">', html)
        self.assertIn('<div data-paso-de="dec" data-paso-a="no">Si algo falla', html)
        self.assertIn('«Recorrer» lo cuenta paso a paso', html)
        base = 'tipo: proceso\nnodos:\n  a: A\n  b: B\nflechas:\n  a > b\n'
        self.assertNotIn('data-modo', self.figura(base)[0])
        for texto, trozo in ((base + 'recorrido:\n  b > a: no\n', 'la flecha «b > a»'),
                             (base + 'recorrido:\n  c: no\n', '«c: no»')):
            with self.subTest(trozo), self.assertRaises(gd.Error) as e:
                self.figura(texto)
            self.assertIn(trozo, str(e.exception))

    def test_medidas_de_lectura(self):
        """El bucle de afinado: el generador mide cada dibujo; una flecha que sube sin ser vuelta se ve."""
        texto = '\n'.join(['tipo: arquitectura', 'nodos:', '  a: A', '  b: B', '  c: C', '  d: D', 'flechas:',
                           '  a > d: | flujo', '  b > c', '  d > a: VUELVE'])
        m = gd.modelo(gd.leer(texto))
        m['id'] = 'p'
        L = gd.dibujar(m, 'v')
        r = gd.medidas(L, m)
        self.assertEqual(r['flechas'], 3)
        self.assertEqual(r['flujo']['flechas'], 1)
        self.assertIn('d > a', r['suben'])                  # sube sin ser vuelta
        self.assertGreater(r['pantallas'][375], 0)
        self.assertIn('d-flujo', ''.join(L.flechas))
        self.assertIn('Medidas (vertical): 3 flechas', gd.texto_medidas(r, 'vertical'))
        m['flechas'][2]['clases'].add('vuelta')
        self.assertEqual(gd.medidas(L, m)['suben'], [])

    def test_eje_con_entradas_frente_a_su_destino(self):
        """Decisión 326: el camino en una columna y cada nodo «lado» a la altura de su ancla, dentro de su zona; la
        flecha entre los dos, recta; un origen con tres o más al lado, en bus."""
        texto = '\n'.join(['tipo: proceso', 'nodos:', '  ctl: Control | lado', '  a: Mezcla A', '  b: Filtro', '  c: Mezcla C',
                           '  va: Voz A | lado', '  vb: Voz B | lado', '  vc: Voz C | lado', '  acc: Acción | izquierda',
                           'zonas:', '  cad: CADENA | a, b, c', '  voces: VOCES | va, vb, vc',
                           'flechas:', '  a > b: | flujo', '  b > c: | flujo', '  va > a', '  vb > b', '  vc > c',
                           '  ctl > va', '  ctl > vb', '  ctl > vc', '  acc > b'])
        m = gd.modelo(gd.leer(texto))
        m['id'] = 'p'
        for v in ('desplegadas', 'plegadas'):
            L = gd.dibujar(m, 'v', v)
            c = L.cajas
            self.assertEqual(len({c[n].x for n in 'abc'}), 1)                     # el eje, en una columna
            for lat, dest in (('va', 'a'), ('vb', 'b'), ('vc', 'c'), ('acc', 'b')):
                self.assertEqual(c[lat].cy, c[dest].cy, lat)                     # a la altura de su destino
            self.assertLess(c['acc'].r, c['b'].x)
            self.assertGreater(c['va'].x, c['a'].r)
            r = gd.medidas(L, m)
            self.assertEqual((r['cruces'], r['compartido'], r['por_caja']), (0, 0, []))
            self.assertEqual(r['flujo']['codos'], 0)
            caminos = {(f['de'], f['a']): p for f, p in L.caminos}
            for e in (('va', 'a'), ('vb', 'b'), ('vc', 'c'), ('acc', 'b')):
                self.assertEqual(len(caminos[e]), 2, e)                           # rectas
            self.assertEqual(len({caminos[('ctl', n)][1][0] for n in ('vb', 'vc')}), 1)   # un solo tronco (va, justo debajo: recta)
            zonas = re.findall(r'<rect class="d-zona" x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"', ''.join(L.fondo))
            for (x, y, w, h), ids in zip(zonas, ('abc', ('va', 'vb', 'vc'))):
                z = gd.R(*map(float, (x, y, w, h)))
                for n in ids:
                    self.assertTrue(z.x < c[n].x and c[n].r < z.r and z.y < c[n].y and c[n].b < z.b, n)

    def test_sin_horizontal_lo_dice(self):
        """Si la horizontal no cabe, la figura lo apunta (data-sin-h) y trae el aviso para cuando se elija."""
        html, dib, errores = self.figura('\n'.join(['tipo: proceso', 'opciones: orientacion=horizontal', 'nodos:'] + [f'  n{i}: Paso número {i}' for i in range(9)] + ['flechas:'] + [f'  n{i} > n{i + 1}' for i in range(8)]))
        self.assertNotIn('h', dib)
        self.assertTrue(errores)
        self.assertIn('data-sin-h="desplegadas-redondeada desplegadas-croqueta plegadas-redondeada plegadas-croqueta"', html)
        self.assertIn('No cabe en horizontal a este ancho', html)
        self.assertNotIn('solo-estrecho', html)                     # la vertical se ve siempre
        html = self.figura((SKILL / 'assets' / 'ejemplos' / 'estados.diagrama').read_text(encoding='utf-8'))[0]
        self.assertNotIn('data-sin-h', html)

    def test_presupuesto_recomendado_y_completo(self):
        import contextlib
        import io
        base = ['tipo: proceso', 'nodos:'] + [f'  n{i}: N{i}' for i in range(11)]
        for ops, trozo in (([], '¿Dos diagramas'), (['opciones: completo'], 'completo, como piden los datos')):
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                m = gd.modelo(gd.leer(chr(10).join(ops + base)))
            self.assertIn(trozo, err.getvalue())
            self.assertEqual(m['completo'], bool(ops))

    def test_orden_de_la_zona_serpentina_y_plegadas_compactas(self):
        nl = chr(10)
        m = gd.modelo(gd.leer(nl.join(['tipo: arquitectura', 'nodos:', '  a: Uno', '  b: Dos', '  c: Tres', 'zonas:', '  z: Z | c, b, a'])))
        m['id'] = 'p'
        L = gd.dibujar(m, 'v')
        orden = sorted('abc', key=lambda n: (L.cajas[n].y, L.cajas[n].x))
        self.assertEqual(orden, ['c', 'b', 'a'])                       # manda el orden de la zona, no el de los nodos
        cadena = ['tipo: arquitectura', 'nodos:'] + [f'  n{i}: Paso {i}' for i in range(6)] + ['zonas:', '  z: Z | ' + ', '.join(f'n{i}' for i in range(6)),
                                                                                             'flechas:'] + [f'  n{i} > n{i + 1}' for i in range(5)]
        m = gd.modelo(gd.leer(nl.join(cadena)))
        m['id'] = 'p'
        L = gd.dibujar(m, 'v')
        c = L.cajas
        filas = sorted({c[n].y for n in c})
        self.assertGreater(len(filas), 1)
        fila = lambda y: sorted((n for n in c if c[n].y == y), key=lambda n: c[n].x)
        uno, dos = fila(filas[0]), fila(filas[1])
        self.assertEqual(uno, sorted(uno))                              # la primera fila, de izquierda a derecha
        self.assertEqual(dos, sorted(dos, reverse=True))                # la segunda, de vuelta: serpentina
        self.assertEqual(c[uno[-1]].x, c[dos[-1]].x)                     # el paso de fila, recto hacia abajo
        Lp = gd.dibujar(m, 'v', 'plegadas')
        self.assertLessEqual(Lp.cajas['n0'].h, 48)                       # plegada: 40 de alto (47 en la vertical)

    def test_etiquetas_junto_a_su_tramo_y_un_carril_por_flecha(self):
        """En los ejemplos, cada etiqueta junto a su flecha y ningún tramo compartido entre flechas de orígenes y destinos
        distintos, ni cruces."""
        for t in ('estados', 'proceso', 'arquitectura', 'piezas'):
            m = gd.modelo(gd.leer((SKILL / 'assets' / 'ejemplos' / f'{t}.diagrama').read_text(encoding='utf-8')))
            m['id'] = 'p'
            for o in ('v', 'h'):
                L = gd.dibujar(m, o)
                r = gd.medidas(L, m)
                self.assertEqual((r['lejos'], r['compartido'], r['cruces']), ([], 0, 0), (t, o))

    ORDEN = ['tipo: proceso', 'nodos:', '  diff: Qué cambió | git diff contra develop', '  elegir: Elegir | reglas del proyecto',
                 '  huella: Huella | ¿ya pasó así? | dec', '  lanzar: Lanzar a la vez | pruebas en trozos',
                 '  resumen: Resumen | pocas líneas · solo lo que falla', '  registro: Registro | la salida entera | externo',
                 'flechas:', '  inicio > diff', '  diff > elegir: ARCHIVOS', '  elegir > huella: COMPROBACIONES', '  huella > lanzar: CAMBIÓ',
                 '  huella > resumen: IGUAL | verde', '  lanzar > resumen: RESULTADOS', '  lanzar > registro: SALIDAS ENTERAS | discontinua']

    def test_una_rama_lateral_va_al_lado_de_su_paso(self):
        """Una caja que cuelga de un paso del medio no va al fondo: el generador prueba una columna más y se queda con
        la que mejor se lee (el diagrama «Una sola orden por vuelta»)."""
        m = gd.modelo(gd.leer(chr(10).join(self.ORDEN)))
        m['id'] = 'p'
        self.assertEqual(gd.ramas_laterales(m), ['registro'])
        for v in ('desplegadas', 'plegadas'):
            L = gd.dibujar(m, 'v', v)
            c = L.cajas
            self.assertEqual(c['registro'].cy, c['lanzar'].cy)
            self.assertGreater(c['registro'].x, c['lanzar'].r)
            r = gd.medidas(L, m)
            self.assertEqual((r['aisladas'], r['cruces']), ([], 0))
        L = gd.dibujar(m, 'h')
        self.assertGreater(L.cajas['registro'].y, L.cajas['lanzar'].b)      # en la horizontal, debajo de su paso
        m1 = gd.modelo(gd.leer(chr(10).join(['opciones: una-columna'] + self.ORDEN)))
        m1['id'] = 'p'
        L = gd.dibujar(m1, 'v')
        self.assertGreater(L.cajas['registro'].y, L.cajas['resumen'].b)     # una columna, si se pide: al fondo
        self.assertEqual(len(gd.medidas(L, m1)['aisladas']), 1)

    def test_zonas_dentro_de_zonas_flecha_a_una_zona_acciones_y_previsto(self):
        texto = chr(10).join(['tipo: proceso', 'nodos:', '  ctl: Control | lado', '  a: Mezcla A', '  b: Filtro', '  c: Mezcla C', '  d: Salida',
                              '  va: Voz A | lado', '  vb: Voz B | lado | previsto', '  acc: Reiniciar | accion', '  acg: Guardar | accion',
                              'zonas:', '  motor: MOTOR | cad, d', '  cad: CADENA | a, b, c', '  voces: VOCES | va, vb',
                              'flechas:', '  a > b: | flujo', '  b > c: | flujo', '  c > d: | flujo', '  va > a', '  vb > b: | previsto',
                              '  ctl > va', '  acc > cad', '  acg > d'])
        m = gd.modelo(gd.leer(texto))
        m['id'] = 'p'
        self.assertEqual(m['zonas'], [('MOTOR', ['a', 'b', 'c', 'd']), ('VOCES', ['va', 'vb'])])
        self.assertEqual(m['subzonas'], [('CADENA', ['a', 'b', 'c'])])
        L = gd.dibujar(m, 'v')
        c = L.cajas
        svg = L.svg('vertical', 'x')
        self.assertIn('d-carpeta-dentro', svg)                                  # la zona a la que llega, con su carpeta
        self.assertNotIn('d-corchete', svg)
        self.assertLess(c['acc'].r, c['b'].x)                                   # la acción, a la izquierda
        self.assertEqual(c['acc'].cy, (c['a'].y + c['c'].b) / 2)                # a la altura del centro de la zona
        fin = re.search(r'<path class="[^"]*" data-de="acc" data-a="cad" d="[^"]*?([\d.]+),[\d.]+"', svg)
        self.assertAlmostEqual(float(fin.group(1)), c['a'].x - 6, delta=3)    # llega a su borde, no a una caja
        self.assertIn('accion', re.search(r'<g data-nodo="acc" class="([^"]*)"', svg).group(1))
        self.assertIn('previsto', re.search(r'<g data-nodo="vb" class="([^"]*)"', svg).group(1))
        self.assertEqual(svg.count('class="d-zona"'), 2)                         # la de dentro, sin marco
        r = gd.medidas(L, m)
        self.assertEqual((r['cruces'], r['por_caja'], r['codos']), (0, [], 0))
        with self.assertRaisesRegex(gd.Error, 'solo recibe flechas de un nodo de al lado'):
            m2 = gd.modelo(gd.leer(texto.replace('  acg > d', '  va > cad')))
            m2['id'] = 'p'
            gd.dibujar(m2, 'v')
        with self.assertRaisesRegex(gd.Error, 'usa una zona'):            # sin corchetes (decisión 420)
            gd.modelo(gd.leer(texto.replace('zonas:', 'corchetes:' + chr(10) + '  mez: Mezcladores | a, b, c' + chr(10) + 'zonas:')))
        with self.assertRaisesRegex(gd.Error, 'dentro de dos zonas'):
            gd.modelo(gd.leer(texto.replace('  voces: VOCES | va, vb', '  voces: VOCES | va, vb, cad')))

    ANILLO = ['tipo: proceso', 'nodos:', '  acc: Cambiar | accion', '  f: Ficha | lado', '  p: Programador | lado', '  c: Cola | lado',
              '  v: Voz', '  m: Mezcla', '  s: Salida', '  g: Ganancia', '  r: Reloj | lado',
              'zonas:', '  ctl: CONTROL | f, p, c', '  mot: MOTOR | v, m, s', '  esc: ESCUCHA | g, r',
              'flechas:', '  acc > f', '  f > p', '  p > c', '  c > v', '  v > m: | flujo', '  m > s: | flujo', '  s > g: 1 × 128 | flujo',
              '  g > r', '  r > p: PIDE | vuelta']

    def test_bloques_ciclo_o_jerarquia_y_su_forma_fijada(self):
        m = gd.modelo(gd.leer(chr(10).join(self.ANILLO)))
        b = gd.bloques(m)
        self.assertEqual((b['forma'], b['orden']), ('anillo', [0, 1, 2]))      # empieza por el bloque al que vuelve
        jer = [x for x in self.ANILLO if x != '  r > p: PIDE | vuelta'] + ['  c > g']
        b = gd.bloques(gd.modelo(gd.leer(chr(10).join(jer))))
        self.assertEqual((b['forma'], b['orden']), ('columnas', [0, 1, 2]))
        self.assertEqual(b['hermanos'], [])
        her = [x for x in jer if x != '  s > g: 1 × 128 | flujo']
        self.assertEqual(gd.bloques(gd.modelo(gd.leer(chr(10).join(her))))['hermanos'], [[1, 2]])
        fijo = gd.modelo(gd.leer(chr(10).join(['anillo: mot, esc, ctl'] + self.ANILLO)))
        self.assertEqual(gd.bloques(fijo)['orden'], [1, 2, 0])
        self.assertIsNone(gd.bloques(gd.modelo(gd.leer(chr(10).join(['opciones: una-columna'] + self.ANILLO)))))
        with self.assertRaisesRegex(gd.Error, 'no es una zona de primer nivel'):
            gd.modelo(gd.leer(chr(10).join(['columnas: ctl | otra'] + self.ANILLO)))

    def test_anillo_con_su_cadena_recta_y_bloques_cerrados_al_empezar(self):
        m = gd.modelo(gd.leer(chr(10).join(self.ANILLO)))
        m['id'] = 'p'
        L = gd.dibujar(m, 'h')
        self.assertEqual(L.bloques, 'anillo')
        c = L.cajas
        self.assertEqual({c['f'].cy, c['p'].cy, c['c'].cy}, {c['f'].cy})               # la cadena del bloque, en una fila
        self.assertTrue(c['f'].x > c['p'].x > c['c'].x)                                  # de derecha a izquierda
        self.assertLess(c['p'].b, c['v'].y)                                              # arriba; las columnas, debajo
        self.assertLess(c['m'].r, c['g'].x)
        self.assertEqual(gd.medidas(L, m)['requiebros'], [])
        html = gd.figura(m)[0]
        self.assertIn('data-bloques-forma="anillo"', html)
        self.assertIn('<div class="d-vista" data-vista="cerrado">', html)               # cerrados al empezar
        for v in ('b0', 'b1', 'b2', 'todo'):
            self.assertIn(f'<div class="d-vista" data-vista="{v}" hidden>', html)
        self.assertIn('data-nodo="_b1"', html)
        self.assertIn('data-ficha="_b0"', html)
        abiertos = gd.modelo(gd.leer(chr(10).join(['opciones: abiertos'] + self.ANILLO)))
        abiertos['id'] = 'q'
        self.assertNotIn('d-vista', gd.figura(abiertos)[0])

    CADENA = ['tipo: proceso', 'nodos:', '  a1: Pedir', '  a2: Enviar', '  b1: Validar', '  b2: Encolar', '  c1: Procesar', '  c2: Responder',
              'zonas:', '  za: CLIENTE | a1, a2', '  zb: SERVIDOR | b1, b2', '  zc: TRABAJADOR | c1, c2',
              'flechas:', '  inicio > a1', '  a1 > a2', '  a2 > b1: PETICIÓN | flujo', '  b1 > b2', '  b2 > c1: TAREA | flujo', '  c1 > c2']
    PARCIAL = CADENA[:8] + ['  d1: Archivar'] + CADENA[8:11] + ['  zd: ARCHIVO | d1'] + CADENA[11:] + ['  c2 > a1: AVISO | vuelta', '  c2 > d1: COPIA']
    P475 = Path(__file__).parent / 'diagramas' / 'piloto-475-zonas.diagrama'

    def test_bloques_por_partes_ida_y_vuelta_y_ciclos_de_algunos(self):
        # el grafo de bloques por partes (propietario): un par con flechas en los dos sentidos cuenta por su ida y va
        # vecino; un ciclo de solo algunos bloques, en anillo, con lo demás colgando de él
        sin_op = chr(10).join(x for x in self.P475.read_text(encoding='utf-8').splitlines() if not x.startswith('opciones:'))
        casos = {'un par doble': (self.CADENA + ['  c2 > b1: HECHO | vuelta'], 'columnas', [0, 1, 2], None, [(1, 2)]),
                 'todos dobles': (self.CADENA + ['  c2 > b1: HECHO | vuelta', '  b1 > a1: RESPUESTA | vuelta'], 'columnas', [0, 1, 2], None, [(0, 1), (1, 2)]),
                 'ciclo de algunos con una rama': (self.PARCIAL, 'anillo', [0, 1, 3, 2], [0, 1, 3], []),
                 'anillo completo': (self.ANILLO, 'anillo', [0, 1, 2], [0, 1, 2], []),
                 'piloto 475: página ⇄ sf_proxy ⇄ sesión': (sin_op.splitlines(), 'columnas', [0, 1, 2], None, [(0, 1), (1, 2)])}
        for nombre, (lineas, forma, orden, ciclo, dobles) in casos.items():
            with self.subTest(nombre):
                m = gd.modelo(gd.leer(chr(10).join(lineas)))
                m['id'] = 'p'
                b = gd.bloques(m)
                self.assertEqual((b['forma'], b['orden'], b['ciclo'], b['dobles']), (forma, orden, ciclo, dobles))
                L = gd.dibujar(m, 'h')
                self.assertEqual(L.bloques, forma)
                if not nombre.startswith('piloto'):            # en el piloto, la ida y la vuelta se cruzan una vez
                    self.assertEqual(gd.medidas(L, m)['cruces'], 0)
                for p_ in (p_ for _, p_ in L.caminos):         # ninguna flecha cruza una caja
                    for a, c in zip(p_, p_[1:]):
                        tramo = gd.seg_rect(a, c, 1)
                        self.assertFalse([k for k, r in L.cajas.items() if tramo.corta(gd.R(r.x + 3, r.y + 3, r.w - 6, r.h - 6))], (nombre, p_))

    def test_cada_zona_una_sola_carpeta(self):
        # el piloto de la 475 (en vertical y abiertos): la vuelta partía sf_proxy y la página en dos carpetas cada una
        m = gd.modelo(gd.leer(self.P475.read_text(encoding='utf-8')))
        m['id'] = 'p'
        L = gd.dibujar(m, 'v')
        c = L.cajas
        marco = lambda *ns: [r for r in L.zonas_rc if all(r.x <= c[n].x and c[n].r <= r.r and r.y <= c[n].y and c[n].b <= r.b for n in ns)]
        self.assertTrue(marco('ctl', 'rech', 'lin', 'guard'))
        self.assertTrue(marco('env', 'est'))
        self.assertTrue(marco('chat', 'reg'))
        html = gd.figura(m)[0]
        for svg in html.split('<svg')[1:]:
            nombres = re.findall(r'class="[^"]*d-zona-n"[^>]*>([^<]+)<', svg)
            self.assertEqual(len(nombres), len(set(nombres)), nombres)

    def test_requiebros_de_un_flujo_lineal_con_sitio(self):
        R = gd.R
        cajas = {'a': R(20, 20, 100, 40), 'b': R(20, 90, 100, 40), 'c': R(150, 90, 100, 40)}
        zona = [R(8, 8, 400, 140)]
        self.assertEqual(gd.requiebros(cajas, zona, [('a', 'b'), ('b', 'c')]), ['a → b → c'])
        recta = dict(cajas, c=R(20, 160, 100, 40))
        self.assertEqual(gd.requiebros(recta, [R(8, 8, 400, 220)], [('a', 'b'), ('b', 'c')]), [])
        self.assertEqual(gd.requiebros(cajas, [R(8, 8, 250, 140)], [('a', 'b'), ('b', 'c')]), [])   # no cabe recta

    def test_recorrido_por_defecto_lo_nuevo_y_zonas_que_se_pliegan(self):
        texto = chr(10).join(['tipo: proceso', 'nodos:', '  a: Uno', '  b: Dos | nuevo', '  c: Tres', 'zonas:', '  z: ZONA | a, b, c',
                              'flechas:', '  a > b: | flujo', '  b > c: | flujo'])
        m = gd.modelo(gd.leer(texto))
        m['id'] = 'p'
        self.assertEqual([p['nodo'] for p in m['recorrido']], ['a', 'b', 'c'])      # el del concepto que fluye
        html = gd.figura(m)[0]
        self.assertIn('data-modo="recorrer"', html)
        self.assertIn('class="d-nodo nuevo"', html)
        self.assertIn('d-nuevo', html)
        self.assertIn('class="d-zona-g" data-zona="0"', html)
        self.assertIn('class="d-tapa" data-zona="0"', html)

    def test_marcas_sin_dos_puntos_y_separadas_por_espacios_chip_y_codigo(self):
        texto = chr(10).join(['tipo: proceso', 'nodos:', '  a: Uno | chip=MOTOR', '  b: Dos | detalle | externo lado', 'flechas:',
                              '  a > b | flujo discontinua', 'fichas:', '  a: Lo primero.', '    - codigo: tools/cola.py ver'])
        m = gd.modelo(gd.leer(texto))
        m['id'] = 'p'
        self.assertEqual(m['nodos']['b']['clases'], {'externo', 'lado'})
        self.assertEqual(m['nodos']['b']['sub'], 'detalle')
        f = m['flechas'][0]
        self.assertEqual((f['etiqueta'], f['clases'] >= {'flujo', 'discontinua'}), ('', True))
        html = gd.figura(m)[0]
        self.assertIn('data-tipo="MOTOR"', html)
        self.assertIn('<li class="d-li-codigo"><code>tools/cola.py ver</code></li>', html)

    def test_chips_apagados_plegada_de_40_y_encendidos_su_otro_dibujo_de_64(self):
        texto = chr(10).join(['tipo: proceso', 'opciones: cajas=plegadas', 'nodos:', '  a: Mezcla | chip=MEZCLA', '  b: Filtro | chip=FILTRO',
                              'flechas:', '  a > b | flujo'])
        m = gd.modelo(gd.leer(texto))
        m['id'] = 'p'
        html = gd.figura(m)[0]
        self.assertIn('d-no-chips', html)                                       # apagados, como manda el ajuste
        alto = lambda chips: {float(h) for h in re.findall(r'<svg data-chips="' + chips + r'" data-cajas="plegadas"[^>]*class="ancho[^>]*>.*?'
                                                           r'<rect class="d-caja"[^>]*? height="([\d.]+)"', html)}
        self.assertEqual(alto('no'), {40.0})
        self.assertEqual(alto('si'), {64.0})
        m['opciones']['chips'] = True                                           # encendidos: el dibujo principal, el de 64
        self.assertIn('<svg data-chips="si" data-cajas="plegadas"', gd.figura(m)[0])

    def test_cauces_con_su_color_y_su_leyenda(self):
        texto = chr(10).join(['tipo: proceso', 'nodos:', '  ctl: Control | lado', '  a: Uno', '  b: Dos', 'flechas:',
                              '  a > b | flujo cauce=audio', '  ctl > a | discontinua cauce=control'])
        m = gd.modelo(gd.leer(texto))
        m['id'] = 'p'
        self.assertEqual(m['cauces'], [('audio', 'acento'), ('control', 'segundo')])
        self.assertEqual([f['linea'] for f in m['flechas']], ['acento', 'segundo'])
        html = gd.figura(m)[0]
        self.assertIn('<p class="d-cauces" role="note">', html)
        self.assertIn('d-c-segundo', html)

    def test_croqueta_que_no_cabe_usa_la_redondeada(self):
        nl = chr(10)
        texto = nl.join(['tipo: proceso', 'nodos:', '  i: Cambiar fonendo | accion', '  a: Mezclador de captación', '  b: Filtro',
                         '  l: Captación | lado', 'flechas:', '  a > b | flujo', '  i > a', '  l > b', '  b > a | vuelta'])
        m = gd.modelo(gd.leer(texto))
        m['id'] = 'p'
        try:
            gd.dibujar(m, 'v', 'desplegadas', 'croqueta')
            self.skipTest('la croqueta cabe con estos datos')
        except gd.Error:
            pass
        html = gd.figura(m)[0]
        self.assertIn('data-forma-dibujo="redondeada"', html)
        ids = re.findall(r' id="([^"]+)"', html)
        self.assertEqual(len(ids), len(set(ids)))                              # sin ids repetidos

    def test_errores_que_se_explican(self):
        for texto, trozo in (('tipo: tarta', 'tipo «tarta»'),
                             ('tipo: estados\nnodos:\n  a: A\nflechas:\n  a > b: X', '«b» no es ningún nodo'),
                             ('tipo: estados\nnodos:\n  a: A | x | rara', 'no es una clase de nodo'),
                             ('tipo: estados\nnodos:\n  a: ' + 'Nombre larguísimo ' * 4, 'no cabe')):
            with self.subTest(trozo), self.assertRaises(gd.Error) as e:
                self.figura(texto)
            self.assertIn(trozo, str(e.exception))

    def test_opciones_de_la_decision_302(self):
        base = (SKILL / 'assets' / 'ejemplos' / 'estados.diagrama').read_text(encoding='utf-8')
        html = self.figura(base)[0]
        self.assertIn('d-b-rojo', html)
        self.assertIn('d-cl', html)                 # «claude»: atajo de cursiva y vuelta
        self.assertIn('d-discontinua', html)
        self.assertNotIn('d-carril', html)
        html = self.figura('opciones: carriles, sin color, orientacion=vertical\n' + base)[0]
        self.assertIn('d-carril', html)
        self.assertIn('d-no-color', html)            # el color sigue en el marcado: la herramienta lo puede volver a poner
        self.assertIn('data-d-orientacion="vertical"', html)
        self.assertIn('solo-ancho', html)            # las dos formas, para poder cambiar de orientación
        with self.assertRaises(gd.Error):
            self.figura('opciones: titulo=gigante\n' + base)

    def test_fragmento_en_un_documento(self):
        import subprocess
        import sys
        with tempfile.TemporaryDirectory() as d:
            frag = Path(d) / 'f.html'
            self.assertEqual(gd.main([str(EJEMPLOS[0]), '--fragmento', '-o', str(frag)]), 0)
            figura = frag.read_text(encoding='utf-8')
            self.assertIn('data-d-tema="tinta"', figura)
            for herr, con_kit in (('recomendadas', True), ('todas -diagramas', False)):
                md = Path(d) / 'doc.md'
                md.write_text(f'---\ndestino: proyecto\nherramientas: {herr}\n---\n# Prueba\n\n## Uno | Primera {{#uno}}\n\nTexto.\n\n{figura}\n',
                              encoding='utf-8')
                r = subprocess.run([sys.executable, '-X', 'utf8', str(DOCUMENTO), str(md), '--identidad', 'ninguna', '--logo', 'ninguno'],
                                   capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
                html = md.with_suffix('.html').read_text(encoding='utf-8')
                self.assertIn('data-kit="skills/diagramas/assets/diagramas.css"', html)
                self.assertIn('data-kit="skills/diagramas/assets/diagramas.js"', html)
                self.assertIn('.diagrama[data-d-tema="tinta"]', html)
                self.assertIn('id="diagramas-temas"', html)
                self.assertEqual('data-kit="tools/kit_documentos/diagramas.js"' in html, con_kit, herr)
                self.assertIn('class="ancho solo-ancho"', html)   # el fragmento pasa entero
            md.write_text('---\ndestino: proyecto\nherramientas: recomendadas\n---\n# Prueba\n\n## Uno | Primera\n\nTexto.\n', encoding='utf-8')
            subprocess.run([sys.executable, '-X', 'utf8', str(DOCUMENTO), str(md), '--identidad', 'ninguna', '--logo', 'ninguno'],
                           capture_output=True, check=True)
            self.assertNotIn('skills/diagramas/assets/diagramas.css', md.with_suffix('.html').read_text(encoding='utf-8'))

    def test_vertical_de_arquitectura_con_varias_cajas_por_fila(self):
        for nombre in ('arquitectura', 'piezas'):
            with self.subTest(nombre):
                m = gd.modelo(gd.leer((SKILL / 'assets' / 'ejemplos' / f'{nombre}.diagrama').read_text(encoding='utf-8')))
                m['id'] = 'p'
                L = gd.dibujar(m, 'v')
                filas = {}
                for c in L.cajas.values():
                    filas.setdefault(c.y, []).append(c)
                self.assertTrue(any(len(f) > 1 for f in filas.values()))           # dos cajas en alguna fila
                self.assertLess(len(filas), len(L.cajas))
                for f in filas.values():                                          # sin pisarse ni salirse
                    f.sort(key=lambda c: c.x)
                    self.assertTrue(all(a.r + 24 <= b.x for a, b in zip(f, f[1:])))
                    self.assertLessEqual(f[-1].r, 400 - 16)
        # un nombre largo, en dos líneas antes que una caja por fila
        texto = 'tipo: arquitectura\nnodos:\n  a: fundacional · informe | uno\n  b: Corto | dos\nzonas:\n  z: ZONA | a, b\n'
        m = gd.modelo(gd.leer(texto))
        m['id'] = 'p'
        L = gd.dibujar(m, 'v')
        self.assertEqual(L.cajas['a'].y, L.cajas['b'].y)
        self.assertEqual(''.join(L.nodos).count('class="d-nn"'), 3)

    def test_sin_tema_toma_el_del_documento(self):
        with tempfile.TemporaryDirectory() as d:
            frag = Path(d) / 'f.html'
            self.assertEqual(gd.main([str(EJEMPLOS[0]), '--fragmento', '--tema', '', '-o', str(frag)]), 0)
            self.assertNotIn('data-d-tema', frag.read_text(encoding='utf-8'))

    def test_pagina_con_el_tema(self):
        m = gd.modelo(gd.leer(EJEMPLOS[0].read_text(encoding='utf-8')))
        m['id'] = 'p'
        html, _ = gd.pagina(m, 'tinta')
        self.assertIn('--primario:#b8431c;', html)
        self.assertIn(':root[data-theme="dark"]', html)
        self.assertIn('window.sfDiagramas', html)


MALO = """<!doctype html><html><head><meta name="viewport" content="width=device-width"></head>
<body style="margin:0;padding:0 16px"><figure style="margin:0">
<svg viewBox="0 0 400 300" width="100%" role="img" aria-label="malo">
<line x1="0" y1="40" x2="400" y2="40" stroke="#555"/>
<text x="20" y="45" font-size="17">cruzado</text>
<rect x="20" y="80" width="80" height="40" fill="none" stroke="#555"/>
<text x="30" y="105" font-size="17">se sale de la caja</text>
<rect x="60" y="100" width="80" height="40" fill="none" stroke="#555"/>
<text x="200" y="200" font-size="6">menuda</text>
<text x="200" y="240" font-size="17" fill="#bbb">clarito</text>
<text x="205" y="246" font-size="17">pisa</text>
<text x="380" y="280" font-size="17">fuera</text>
<g tabindex="0"><circle cx="300" cy="100" r="5" fill="#555"/></g>
</svg></figure></body></html>"""


@unittest.skipUnless(hay_navegador(), 'sin Playwright o sin navegador')
class EnNavegador(unittest.TestCase):
    def test_el_ejemplo_pasa(self):
        salida = cd.comprobar(SKILL / 'assets' / 'ejemplo-estados.html', [375, 1440], 6.5, ('claro', 'oscuro'))
        for m in salida:
            self.assertIsNone(m['pagina'])
            self.assertEqual(m['interaccion'], [], m['ancho'])
            self.assertEqual(m['js'], [])
            self.assertEqual([e for f in m['figuras'] for e in f['errores']], [], m['ancho'])

    def test_cada_tipo_generado_pasa(self):
        with tempfile.TemporaryDirectory() as d:
            for ruta in EJEMPLOS:
                with self.subTest(ruta.stem):
                    salida = Path(d) / (ruta.stem + '.html')
                    self.assertEqual(gd.main([str(ruta), '-o', str(salida), '--sin-comprobar']), 0)
                    for m in cd.comprobar(salida, [375, 1440], 6.5, ('claro', 'oscuro')):
                        self.assertEqual(m['interaccion'], [], (m['ancho'], m['modo']))
                        self.assertEqual(m['js'], [])
                        self.assertEqual([e for f in m['figuras'] for e in f['errores']], [], (m['ancho'], m['modo']))

    def test_con_el_tema_del_documento(self):
        """Una figura sin tema: «Por defecto» vuelve al del documento, el fondo «Claro» es su papel y los rótulos de
        zona llegan a 4,5:1 aunque el texto tenue del tema no llegue (pool: 2,54:1)."""
        import subprocess
        import sys
        from playwright.sync_api import sync_playwright
        with tempfile.TemporaryDirectory() as d:
            frag = Path(d) / 'f.html'
            self.assertEqual(gd.main([str(SKILL / 'assets' / 'ejemplos' / 'arquitectura.diagrama'), '--fragmento', '--tema', '', '-o', str(frag)]), 0)
            md = Path(d) / 'doc.md'
            md.write_text('---\ndestino: proyecto\nherramientas: todas\n---\n# Prueba\n\n## Uno | Primera {#uno}\n\nTexto.\n\n'
                          + frag.read_text(encoding='utf-8') + '\n', encoding='utf-8')
            r = subprocess.run([sys.executable, '-X', 'utf8', str(DOCUMENTO), str(md), '--identidad', 'ninguna', '--logo', 'ninguno', '--tema', 'pool'],
                               capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
            html = md.with_suffix('.html')
            for m in cd.comprobar(html, [375, 1440], 6.5, ('claro',)):
                self.assertEqual([e for f in m['figuras'] for e in f['errores']], [], m['ancho'])
            with sync_playwright() as pw:
                b = cd.navegador(pw)
                p = b.new_page(viewport={'width': 1440, 'height': 900})
                p.goto(html.resolve().as_uri())
                p.wait_for_timeout(500)
                fondo = "() => [getComputedStyle(document.body).backgroundColor, getComputedStyle(document.querySelector('figure.diagrama')).backgroundColor]"
                pagina, lienzo = p.evaluate(fondo)
                self.assertEqual(lienzo, pagina)
                p.evaluate("document.querySelectorAll('#herr-diagramas .dg-grupo').forEach(d => d.open = true)")
                p.select_option('#herr-diagramas select[data-dg="tema"]', 'tinta')
                self.assertEqual(p.evaluate("document.querySelector('figure.diagrama').dataset.dTema"), 'tinta')
                p.click('#herr-diagramas [data-dg-poner="def"]')
                self.assertIsNone(p.evaluate("document.querySelector('figure.diagrama').dataset.dTema || null"))
                self.assertEqual(p.input_value('#herr-diagramas select[data-dg="tema"]'), 'documento')
                p.click('#herr-diagramas [data-dg-poner="orig"]')
                self.assertEqual(p.evaluate("document.querySelector('figure.diagrama').dataset.dTema"), 'tinta')
                b.close()

    def test_los_diagramas_pasan_con_cada_tema_del_catalogo(self):
        """Los seis diagramas del documento de ejemplo, con cada tema, en claro y en oscuro: contraste incluido
        (con el morado, la cabecera de las notas daba 3,66:1)."""
        import subprocess
        import sys
        temas = sorted(p.stem for p in (SKILL.parent / 'crear_documentos' / 'assets' / 'temas').glob('*.json'))
        self.assertIn('morado', temas)
        with tempfile.TemporaryDirectory() as d:
            shutil.copytree(SKILL / 'assets' / 'ejemplos', Path(d) / 'ejemplos')
            for tema in temas:
                with self.subTest(tema):
                    md = Path(d) / f'doc-{tema}.md'
                    shutil.copy(SKILL / 'assets' / 'ejemplo-documento.md', md)
                    r = subprocess.run([sys.executable, '-X', 'utf8', str(DOCUMENTO), str(md), '--identidad', 'ninguna', '--logo', 'ninguno', '--tema', tema],
                                       capture_output=True, text=True, encoding='utf-8')
                    self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
                    for m in cd.comprobar(md.with_suffix('.html'), [1440], 6.5, ('claro', 'oscuro')):
                        self.assertEqual([e for f in m['figuras'] for e in f['errores']], [], (tema, m['modo']))

    def test_el_documento_de_ejemplo_pasa_y_su_herramienta_cambia_todas(self):
        ruta = SKILL / 'assets' / 'ejemplo-documento.html'
        for m in cd.comprobar(ruta, [375, 1440], 6.5, ('claro', 'oscuro')):   # también el oscuro de «Lectura»
            self.assertEqual(m['interaccion'], [], (m['ancho'], m['modo']))
            self.assertEqual(m['js'], [])
            self.assertEqual(len([f for f in m['figuras'] if f['nombre'] != 'Notas' and not (f['nombre'] or '').startswith('con los chips')]), 6)
            self.assertEqual([e for f in m['figuras'] for e in f['errores']], [], (m['ancho'], m['modo']))
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = cd.navegador(pw)
            p = b.new_page(viewport={'width': 1440, 'height': 900})
            p.goto(ruta.resolve().as_uri())
            p.wait_for_timeout(500)
            self.assertEqual(p.locator('#herr-diagramas').get_attribute('data-modo'), 'columna')
            grupos = p.evaluate("() => [...document.querySelectorAll('#herr-diagramas .dg-grupo > summary')].map(s => s.textContent)")
            self.assertEqual(grupos, ['Aspecto general', 'Cabecera', 'Cajas', 'Flechas y etiquetas', 'Notas', 'Interacción', 'Pie'])
            # empiezan plegados; abiertos, todos los desplegables con el mismo ancho y en la misma columna
            self.assertEqual(p.evaluate("document.querySelectorAll('#herr-diagramas .dg-grupo[open]').length"), 0)
            p.evaluate("document.querySelectorAll('#herr-diagramas .dg-grupo').forEach(d => d.open = true)")
            # solo ajustes genéricos: el color y el estilo de cada flecha, de sus datos
            visibles = "() => [...document.querySelectorAll('#herr-diagramas .dg-grupo[data-grupo=flechas] label')].map(l => l.textContent.trim())"
            self.assertIn('Colores de los datos', p.evaluate(visibles))
            self.assertFalse(any('Claude' in x or 'botón' in x for x in p.evaluate(visibles)))
            cajas = p.evaluate("() => [...document.querySelectorAll('#herr-diagramas .dg-grupo select')].map(s => { const r = s.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.width)]; })")
            self.assertEqual(len(set(map(tuple, cajas))), 1, cajas)
            # Flechas y etiquetas y Notas cambian todas las figuras
            p.select_option('#herr-diagramas select[data-dg="esquinas"]', 'rectas')
            self.assertNotIn('Q', p.evaluate("document.querySelector('#estados path[data-da]').getAttribute('d')"))
            p.select_option('#herr-diagramas select[data-dg="esquinas"]', 'redondeadas')
            p.select_option('#herr-diagramas select[data-dg="lugar-nota"]', 'debajo')
            self.assertTrue(p.evaluate("[...document.querySelectorAll('#estados svg.d-notas-svg')].some(s => s.getBoundingClientRect().width)"))
            p.select_option('#herr-diagramas select[data-dg="lugar-nota"]', 'hueco')
            p.select_option('#herr-diagramas select[data-dg="orientacion"]', 'vertical')
            p.uncheck('#herr-diagramas input[data-dg="color"]')
            estado = p.evaluate("() => [...document.querySelectorAll('figure.diagrama')].map(f => [f.dataset.dOrientacion, f.classList.contains('d-no-color')])")
            self.assertEqual(estado, [['vertical', True]] * 6)
            p.click('#herr-diagramas [data-dg-poner="def"]')
            estado = p.evaluate("() => [...document.querySelectorAll('figure.diagrama')].map(f => [f.dataset.dOrientacion, f.classList.contains('d-no-color'), f.dataset.dTema])")
            self.assertEqual(estado, [['auto', False, None]] * 6)   # sin tema propio: el del documento (307)
            # «Letra más grande» cambia la letra de las seis figuras, también en la horizontal
            escala = "() => [...document.querySelectorAll('figure.diagrama')].map(f => getComputedStyle([...f.querySelectorAll('svg')].find(s => s.getBoundingClientRect().width).querySelector('.d-nn')).transform)"
            self.assertEqual(set(p.evaluate(escala)), {'none'})
            p.check('#herr-diagramas input[data-dg="letra"]')
            self.assertNotIn('none', p.evaluate(escala))
            p.uncheck('#herr-diagramas input[data-dg="letra"]')
            # el circulito pliega su caja sola, sin abrir la ficha, y su flecha sigue tocándola
            caja = "() => { const s = [...document.querySelectorAll('#estados svg')].find(s => s.getBoundingClientRect().width); const r = s.querySelector('[data-nodo=\"obs\"] .d-caja'); const f = s.querySelector('path[data-a=\"obs\"][data-de=\"curso\"]').getAttribute('d').match(/(-?[\\d.]+),(-?[\\d.]+)$/); return [+r.getAttribute('y'), +r.getAttribute('height'), +f[2]]; }"
            y, h, fy = p.evaluate(caja)
            p.locator('#estados svg:visible [data-plegar="obs"]').click()
            y2, h2, fy2 = p.evaluate(caja)
            self.assertLess(h2, h)
            self.assertTrue(y2 - 3 <= fy2 <= y2 + h2, (fy2, y2, h2))   # la flecha (ahora recta, por el lado) sigue en la caja
            self.assertTrue(p.evaluate("document.querySelector('#estados .d-hud').hidden"))
            self.assertEqual(p.locator('#estados svg:visible [data-plegar="obs"]').get_attribute('aria-expanded'), 'false')
            # recorrido en el segundo color del tema (el del documento)
            p.locator('#estados svg:visible [data-nodo="pend"]').hover()
            p.wait_for_timeout(400)   # la transición del resaltado
            segundo = p.evaluate("() => { const e = document.createElement('i'); e.style.color = 'var(--segundo, #2f5597)'; document.querySelector('#estados').append(e); const c = getComputedStyle(e).color; e.remove(); return c; }")
            self.assertEqual(p.evaluate("getComputedStyle([...document.querySelectorAll('#estados path.d-on')].find(e => e.getBoundingClientRect().width)).stroke"), segundo)
            b.close()

    def test_una_flecha_que_no_toca_su_caja(self):
        pagina = ('<!doctype html><html><head><meta name="viewport" content="width=device-width"></head><body style="margin:0">'
                  '<figure style="margin:0"><svg viewBox="0 0 400 200" width="100%" role="img" aria-label="x">'
                  '<path data-de="a" data-a="b" d="M120,40 L250,40" fill="none" stroke="#555" marker-end="url(#m)"/>'
                  '<path data-de="b" data-a="a" d="M300,130 L300,110 L60,110 L60,62" fill="none" stroke="#555"/>'
                  '<g data-nodo="a"><rect class="d-caja" x="20" y="20" width="100" height="40" fill="none" stroke="#555"/></g>'
                  '<g data-nodo="b"><rect class="d-caja" x="252" y="60" width="100" height="40" fill="none" stroke="#555"/></g>'
                  '</svg></figure></body></html>')
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / 'flechas.html'
            ruta.write_text(pagina, encoding='utf-8')
            errores = cd.comprobar(ruta, [1440], 6.5)[0]['figuras'][0]['errores']
        self.assertIn('la flecha a → b no toca su destino', errores)
        self.assertIn('la flecha b → a no toca su origen', errores)

    def test_horizontal_que_no_cabe_se_ve_en_vertical_con_aviso(self):
        from playwright.sync_api import sync_playwright
        with tempfile.TemporaryDirectory() as d:
            datos = Path(d) / 'largo.diagrama'
            datos.write_text('\n'.join(['tipo: proceso', 'opciones: orientacion=horizontal', 'nodos:'] + [f'  n{i}: Paso número {i}' for i in range(9)] + ['flechas:'] + [f'  n{i} > n{i + 1}' for i in range(8)]), encoding='utf-8')
            ruta = Path(d) / 'largo.html'
            self.assertEqual(gd.main([str(datos), '-o', str(ruta), '--sin-comprobar']), 0)
            with sync_playwright() as pw:
                b = cd.navegador(pw)
                p = b.new_page(viewport={'width': 1440, 'height': 900})
                p.goto(ruta.resolve().as_uri())
                self.assertTrue(p.locator('.d-aviso-h').is_visible())
                self.assertEqual(p.evaluate("[...document.querySelectorAll('figure svg')].filter(s => s.getBoundingClientRect().width).length"), 1)
                p.evaluate("document.querySelector('figure').dataset.dOrientacion = 'auto'")
                self.assertFalse(p.locator('.d-aviso-h').is_visible())
                b.close()

    def test_avisa_de_una_caja_lejos_de_su_unica_union(self):
        with tempfile.TemporaryDirectory() as d:
            datos = Path(d) / 'orden.diagrama'
            datos.write_text(chr(10).join(['opciones: una-columna'] + Generador.ORDEN), encoding='utf-8')
            ruta = Path(d) / 'orden.html'
            self.assertEqual(gd.main([str(datos), '-o', str(ruta), '--sin-comprobar']), 0)
            avisos = [a for f in cd.comprobar(ruta, [375], 6.5)[0]['figuras'] for a in f['avisos']]
        self.assertTrue(any('«Registro» queda lejos de «Lanzar a la vez»' in a and '«Resumen»' in a for a in avisos), avisos)

    def test_una_flecha_cortada_y_una_etiqueta_lejos_de_su_flecha(self):
        # el piloto de la 475: carriles fuera del dibujo, trocitos de flecha sueltos, y «401 CADUCADO» lejos de la suya
        with tempfile.TemporaryDirectory() as d:
            datos = Path(d) / 't.diagrama'
            datos.write_text(chr(10).join(['tipo: proceso', 'nodos:', '  a: Lanzar la orden', '  b: Leer la salida', '  c: Guardar el registro',
                                           'flechas:', '  inicio > a', '  a > b: SALIDA', '  b > c']), encoding='utf-8')
            ruta = Path(d) / 't.html'
            self.assertEqual(gd.main([str(datos), '-o', str(ruta)]), 0)          # bien dibujado, sin errores
            html = ruta.read_text(encoding='utf-8')
            html = re.sub(r'(data-de="b" data-a="c" d="M)([\d.]+),([\d.]+) L[\d.]+,[\d.]+"', r'\g<1>\2,\3 L5000,\3"', html)
            html = html.replace('<g class="d-et" data-de="a" data-a="b">', '<g class="d-et" data-de="a" data-a="b" transform="translate(0,60)">')
            ruta.write_text(html, encoding='utf-8')
            errores = [e for m in cd.comprobar(ruta, [1440], 6.5) for f in m['figuras'] for e in f['errores']]
        self.assertTrue(any('la flecha b → c se sale del dibujo' in e for e in errores), errores)
        self.assertTrue(any('la etiqueta «SALIDA» queda a' in e and 'de su flecha (a → b)' in e for e in errores), errores)

    def test_bloques_cerrados_se_abren_en_su_sitio_y_se_imprimen_abiertos(self):
        from playwright.sync_api import sync_playwright
        with tempfile.TemporaryDirectory() as d:
            datos = Path(d) / 'a.diagrama'
            datos.write_text(chr(10).join(Generador.ANILLO), encoding='utf-8')
            ruta = Path(d) / 'a.html'
            self.assertEqual(gd.main([str(datos), '-o', str(ruta)]), 0)          # el comprobador prueba abrir y cerrar
            with sync_playwright() as pw:
                b = cd.navegador(pw)
                for ancho in (375, 1440):
                    p = b.new_page(viewport={'width': ancho, 'height': 900})
                    p.goto(ruta.resolve().as_uri())
                    vis = lambda: p.evaluate("[...document.querySelectorAll('.d-vista')].filter(d => !d.hidden).map(d => d.dataset.vista).join()")
                    self.assertEqual(vis(), 'cerrado')
                    next(x for x in p.locator('[data-nodo="_b1"]').all() if x.is_visible()).click()
                    self.assertEqual(vis(), 'b1')
                    next(x for x in p.locator('.d-vista[data-vista="b1"] .d-zona-g').all() if x.is_visible()).click()
                    self.assertEqual(vis(), 'cerrado')
                    p.emulate_media(media='print')
                    self.assertTrue(p.locator('.d-vista[data-vista="todo"]').is_visible())
                    self.assertFalse(p.locator('.d-vista[data-vista="cerrado"]').is_visible())
                    p.close()
                b.close()

    def test_una_zona_en_dos_carpetas_y_los_puntos_clave_con_bloques_cerrados(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / 'r.html'
            svg = ('<svg viewBox="0 0 400 300" role="img" aria-label="x">'
                   + ''.join(f'<rect class="d-zona" x="8" y="{y}" width="380" height="120" fill="none" stroke="#555"/>'
                             f'<text class="d-zona-n" x="16" y="{y + 20}" font-size="14">PROXY</text>' for y in (8, 160)) + '</svg>')
            ruta.write_text('<!doctype html><html><head><meta name="viewport" content="width=device-width"></head><body>'
                            f'<figure class="diagrama">{svg}</figure></body></html>', encoding='utf-8')
            errores = [e for f in cd.comprobar(ruta, [1440], 6.5)[0]['figuras'] for e in f['errores']]
            self.assertIn('la zona «PROXY» se pinta en 2 carpetas: una sola', errores)
            # el piloto de la 475 sin opciones: bloques cerrados al empezar, y sus puntos clave cuentan por su bloque
            datos = Path(d) / 'p.diagrama'
            datos.write_text(chr(10).join(x for x in Generador.P475.read_text(encoding='utf-8').splitlines()
                                          if not x.startswith('opciones:')), encoding='utf-8')
            salida = Path(d) / 'p.html'
            self.assertEqual(gd.main([str(datos), '-o', str(salida), '--sin-comprobar']), 0)
            for m in cd.comprobar(salida, [375, 1440], 6.5):
                self.assertEqual([e for f in m['figuras'] for e in f['errores']], [], m['ancho'])
                self.assertFalse([a for f in m['figuras'] for a in f['avisos'] if 'solo se ve al abrir' in a], m['ancho'])

    def test_avisa_de_requiebros_y_de_un_ciclo_apilado(self):
        svg = ('<svg viewBox="0 0 400 300" data-bloques="apilado-anillo" role="img" aria-label="x">'
               '<rect class="d-zona" x="8" y="8" width="380" height="200" fill="none" stroke="#555"/>'
               + ''.join(f'<g data-nodo="{n}" class="d-nodo"><rect class="d-caja" x="{x}" y="{y}" width="100" height="40" fill="#fff" stroke="#555"/>'
                         f'<text class="d-nn" x="{x + 10}" y="{y + 25}" font-size="14">{n.upper()}</text></g>'
                         for n, x, y in (('a', 30, 40), ('b', 30, 120), ('c', 200, 120)))
               + '<path class="d-fl" data-de="a" data-a="b" d="M80,80 L80,118" fill="none" stroke="#555"/>'
               + '<path class="d-fl" data-de="b" data-a="c" d="M130,140 L198,140" fill="none" stroke="#555"/></svg>')
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / 'r.html'
            ruta.write_text('<!doctype html><html><head><meta name="viewport" content="width=device-width"></head><body>'
                            f'<figure class="diagrama">{svg}</figure></body></html>', encoding='utf-8')
            avisos = [a for f in cd.comprobar(ruta, [1440], 6.5)[0]['figuras'] for a in f['avisos']]
        self.assertTrue(any('«A → B → C» hace requiebros' in a for a in avisos), avisos)
        self.assertTrue(any('ciclo entre bloques y va apilado' in a for a in avisos), avisos)

    def test_avisa_de_bloques_cerrados_que_cargan_a_un_lado(self):
        def caja(n, x, y):
            return (f'<g data-nodo="{n}" class="d-nodo"><rect class="d-caja" x="{x}" y="{y}" width="100" height="40" fill="#fff" stroke="#555"/>'
                    f'<text class="d-nn" x="{x + 10}" y="{y + 25}" font-size="14">{n.upper()}</text></g>')

        def avisos(d, xb):
            svg = ('<svg viewBox="0 0 600 200" role="img" aria-label="x">'
                   '<path class="d-carpeta d-carpeta-zona" d="M8,8 H592 V80 H8 Z" fill="none" stroke="#555"/>'
                   + caja('a', 20, 24) + caja('b', 250, 24) + caja('c', 480, 24) + caja('_b0', xb[0], 120) + caja('_b1', xb[1], 120)
                   + '</svg>')
            ruta = Path(d) / 'q.html'
            ruta.write_text('<!doctype html><html><head><meta name="viewport" content="width=device-width"></head><body>'
                            f'<figure class="diagrama">{svg}</figure></body></html>', encoding='utf-8')
            return [a for f in cd.comprobar(ruta, [1440], 6.5)[0]['figuras'] for a in f['avisos'] if 'desequilibrio' in a]
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(avisos(d, (20, 140)))                   # apiñados a la izquierda, con sitio a la derecha
            self.assertFalse(avisos(d, (20, 480)))                  # repartidos bajo la fila

    def test_una_vista_descentrada_o_con_hueco_arriba_es_un_error(self):
        def errores(d, x, y):
            svg = (f'<svg viewBox="0 0 600 200" role="img" aria-label="x"><g data-nodo="a" class="d-nodo">'
                   f'<rect class="d-caja" x="{x}" y="{y}" width="200" height="60" fill="#fff" stroke="#555"/>'
                   f'<text class="d-nn" x="{x + 10}" y="{y + 35}" font-size="14">A</text></g></svg>')
            ruta = Path(d) / 'c.html'
            ruta.write_text('<!doctype html><html><head><meta name="viewport" content="width=device-width"></head><body>'
                            f'<figure class="diagrama"><div class="d-vista" data-vista="cerrado">{svg}</div></figure></body></html>', encoding='utf-8')
            return [e for f in cd.comprobar(ruta, [1440], 6.5)[0]['figuras'] for e in f['errores'] if 'descentrado' in e or 'hueco de' in e]
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(len(errores(d, 350, 80)), 2)           # a la derecha y con 80 vacíos arriba
            self.assertEqual(errores(d, 200, 12), [])               # centrada y arriba

    def test_el_comprobador_mira_que_cada_punto_clave_se_vea(self):
        with tempfile.TemporaryDirectory() as d:
            datos = Path(d) / 't.diagrama'
            datos.write_text(HOY, encoding='utf-8')
            self.assertEqual(gd.main([str(datos), '--exigir']), 0)
            html = (Path(d) / 't.html').read_text(encoding='utf-8')
            self.assertIn('data-puntos-clave=', html)
            # sin la flecha de la espera en el dibujo, su punto clave no se ve
            (Path(d) / 'u.html').write_text(re.sub(r'<path class="d-fl[^"]*" data-de="pruebas" data-a="espera"[^>]*>', '', html), encoding='utf-8')
            errores = [e for m in cd.comprobar(Path(d) / 'u.html', [375], 6.5) for f in m['figuras'] for e in f['errores']]
            self.assertIn('el punto clave «Las lentas obligan a esperar.» no se ve: «pruebas > espera» no está en el dibujo', errores)

    def test_una_zona_dentro_de_otra_es_una_carpeta_en_todos_los_tipos(self):
        # opción B del propietario: en arquitectura, piezas y el proceso en columna, la de dentro con su carpeta, y la
        # flecha a ella llega a su borde
        base = chr(10).join(['titulo: La SF en el equipo', 'nodos:', '  main: main | lo publicado', '  act: Instalar | /plugin install | accion',
                             '  sk1: diagramas | skill', '  sk2: documentos | skill', '  mod: Mod | el panel',
                             'zonas:', '  repo: REPOSITORIO | main, act', '  equipo: EQUIPO | skills, mod', '  skills: SKILLS | sk1, sk2',
                             'flechas:', '  main > act: VERSIÓN', '  act > skills: CAMBIA | discontinua linea=morado', '  sk2 > mod: USA'])
        columna = chr(10).join(['tipo: proceso', 'titulo: Publicar', 'nodos:', '  prep: Preparar', '  pr: Pruebas', '  val: Validar', '  pub: Publicar',
                                'zonas:', '  todo: RELEASE | prep, comprobar, pub', '  comprobar: COMPROBAR | pr, val',
                                'flechas:', '  inicio > prep', '  prep > pr | flujo', '  pr > val | flujo', '  val > pub | flujo'])
        with tempfile.TemporaryDirectory() as d:
            for nombre, texto in (('arquitectura', 'tipo: arquitectura' + chr(10) + base), ('piezas', 'tipo: piezas' + chr(10) + base),
                                  ('columna', columna)):
                datos = Path(d) / f'{nombre}.diagrama'
                datos.write_text(texto, encoding='utf-8')
                self.assertEqual(gd.main([str(datos)]), 0, nombre)       # el comprobador, sin errores (375 y 1440, claro y oscuro)
                html = datos.with_suffix('.html').read_text(encoding='utf-8')
                # la fila horizontal del proceso no dibuja zonas: en él, la vertical
                svgs = [x for x in re.findall(r'<svg .*?</svg>', html, re.S) if nombre != 'columna' or 'class="vertical' in x[:300]]
                self.assertTrue(svgs and all('d-carpeta-dentro' in x for x in svgs), nombre)
                if nombre != 'columna':
                    self.assertTrue(all('data-de="act" data-a="skills"' in x for x in svgs), nombre)

    def test_hoy_y_su_propuesta_en_la_misma_orientacion_y_lo_de_al_lado_donde_no_cruce(self):
        # los esquemas de «Cómo se testea hoy» y su propuesta (tarea 474), con compara-con entre ellos: los dos en
        # vertical sin leer el otro (en el piloto se dibujan por separado y hoy salía en horizontal); «Vigilar lo
        # lento», «lado», cruzaba una línea a la derecha a 375 y el generador lo pone a la izquierda
        with tempfile.TemporaryDirectory() as d:
            m = gd.modelo(gd.leer((Path(__file__).parent / 'diagramas' / 'hoy.diagrama').read_text(encoding='utf-8')))
            errores, avisos = gd.concepto(m, Path(d), True)        # sin propuesta.diagrama al lado
            self.assertEqual(m['opciones']['orientacion'], 'vertical')
            for x in ('hoy', 'propuesta'):
                shutil.copy(Path(__file__).parent / 'diagramas' / f'{x}.diagrama', Path(d) / f'{x}.diagrama')
            m = gd.modelo(gd.leer((Path(d) / 'hoy.diagrama').read_text(encoding='utf-8')))
            errores, avisos = gd.concepto(m, Path(d), True)
            self.assertEqual((errores, m['opciones']['orientacion']), ([], 'vertical'))
            self.assertFalse(any('con el que se compara, en' in a for a in avisos), avisos)
            # si uno fija otra, el otro lo dice
            t = (Path(d) / 'propuesta.diagrama').read_text(encoding='utf-8')
            (Path(d) / 'propuesta.diagrama').write_text(t.replace('tipo: proceso', 'tipo: proceso' + chr(10) + 'opciones: orientacion=horizontal', 1), encoding='utf-8')
            m = gd.modelo(gd.leer((Path(d) / 'hoy.diagrama').read_text(encoding='utf-8')))
            self.assertTrue(any('va en vertical y propuesta.diagrama, con el que se compara, en horizontal' in a
                                for a in gd.concepto(m, Path(d), True)[1]))
            (Path(d) / 'propuesta.diagrama').write_text(t, encoding='utf-8')
            for x in ('hoy', 'propuesta'):
                self.assertEqual(gd.main([str(Path(d) / f'{x}.diagrama'), '--exigir']), 0, x)

    def test_una_flecha_de_un_paso_a_un_bloque_cerrado_llega_a_su_pestana(self):
        # el caso de «Cómo se testea hoy»: de «Lanzar a mano» (en una carpeta) a «Esperar» (en otra, cerrada), por arriba
        texto = chr(10).join(['tipo: proceso', 'nodos:', '  vuelta: Acabar la vuelta', '  pruebas: Lanzar a mano', '  repetir: ¿Falló o cambió? | dec',
                              '  espera: Esperar', '  leer: Leer todo', '  captura: Mirar capturas | externo',
                              'zonas:', '  elegir: ELEGIR A MANO | vuelta, pruebas, repetir', '  lanzar: LANZAR Y LEER | espera, leer, captura',
                              'flechas:', '  inicio > vuelta', '  vuelta > pruebas: A MANO | flujo', '  pruebas > repetir: RESULTADO | flujo',
                              '  repetir > pruebas: REPITE | rojo vuelta', '  pruebas > espera: LENTA', '  espera > leer | flujo',
                              '  leer > captura: SI HAY DUDA | discontinua'])
        with tempfile.TemporaryDirectory() as d:
            datos = Path(d) / 't.diagrama'
            datos.write_text(texto, encoding='utf-8')
            self.assertEqual(gd.main([str(datos), '-o', str(Path(d) / 't.html')]), 0)     # el comprobador, sin errores

    def test_solo_lo_nuevo_y_plegar_una_zona(self):
        from playwright.sync_api import sync_playwright
        texto = chr(10).join(['tipo: proceso', 'nodos:', '  a: Uno', '  b: Dos | nuevo', '  c: Tres', 'zonas:', '  z: ZONA | a, b, c',
                              'flechas:', '  a > b', '  b > c'])
        with tempfile.TemporaryDirectory() as d:
            datos = Path(d) / 'n.diagrama'
            datos.write_text(texto, encoding='utf-8')
            ruta = Path(d) / 'n.html'
            self.assertEqual(gd.main([str(datos), '-o', str(ruta)]), 0)          # el comprobador, sin errores
            with sync_playwright() as pw:
                b = cd.navegador(pw)
                p = b.new_page(viewport={'width': 375, 'height': 900})
                p.goto(ruta.resolve().as_uri())
                p.locator('.d-nuevo-b').click()
                self.assertTrue(p.evaluate("document.querySelector('figure').classList.contains('d-solo-nuevo')"))
                g = next(x for x in p.locator('.d-zona-g').all() if x.is_visible())
                self.assertGreaterEqual(g.bounding_box()['height'], 24)
                g.click()
                self.assertEqual(g.get_attribute('aria-expanded'), 'false')
                self.assertTrue(next(x for x in p.locator('.d-tapa').all() if x.is_visible()))
                b.close()

    def test_una_pagina_mala_da_cada_error(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d) / 'malo.html'
            ruta.write_text(MALO, encoding='utf-8')
            m = cd.comprobar(ruta, [375], 6.5)[0]
        errores = ' | '.join(m['figuras'][0]['errores'])
        for trozo in ('role="img" con elementos que se pulsan', 'se pulsa en', 'letra de', '«menuda»',
                      'se sale de su caja', '«fuera» se sale del dibujo', 'se pisan', 'dos cajas se pisan',
                      'una línea cruza «cruzado»', 'contraste'):
            self.assertIn(trozo, errores)


if __name__ == '__main__':
    unittest.main()
