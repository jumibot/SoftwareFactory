import { COLOR_SF, RGB } from './constantes'
import { centrar } from './estilo'
import { ANCHO_LETRAS, COLOR_BARRA, logoTexto } from './logo'

// ── La bienvenida, en un proyecto sin SF (tarea 289) ──
// La primera vez que alguien abre el panel en una carpeta sin .sf/proyecto.json, lo único que necesita saber es qué
// pulsar o escribir para empezar: la marca, qué es la SF en una frase y la orden, sin JSON, rutas, skills ni contadores. Todo
// va centrado a mano, con espacios, porque el panel no centra solo; las líneas son de texto puro, para que se lea
// igual en un terminal sin color.

// El color de la marca en la bienvenida: el de la SF, el morado de su sesión (COLOR_SF, #827dbd), fijo (decisión 249).
// La letra negra encima: contraste 5,6:1 (con blanca, 3,8:1).
export const COLOR_MARCA = RGB[COLOR_SF]
export const LETRA_MARCA = '#000000'
// El morado claro de la barra del logo, para lo secundario junto a la marca (el Abandonar de la incorporación en pausa,
// tarea 333): sobre el gris del bloque (#3a3a3a), contraste 5,5:1.
export const COLOR_MARCA_CLARO = COLOR_BARRA

export const NOMBRE_ANCHO = 'S O F T W A R E   F A C T O R Y'
export const NOMBRE = 'SOFTWARE FACTORY'
export const LEMA = 'Tu fábrica de software sobre Claude Code: de la idea al código, tarea a tarea.'
export const PARA_EMPEZAR = 'Para empezar, pulsa o escríbelo en el chat:'
export const ORDEN_EMPEZAR = 'incorpora este proyecto a la SF'
export const DESPUES = 'Claude te hará unas pocas preguntas y no cambia nada sin tu OK.'

// Un texto partido por palabras en líneas de w columnas como mucho; una palabra más larga, recortada.
export function partir(texto: string, w: number): string[] {
  const lineas: string[] = []
  for (const palabra of texto.split(' ')) {
    const ultima = lineas.at(-1)
    if (ultima !== undefined && (ultima + ' ' + palabra).length <= w) lineas[lineas.length - 1] = `${ultima} ${palabra}`
    else lineas.push(palabra.length > w ? palabra.slice(0, Math.max(1, w)) : palabra)
  }
  return lineas
}

// Como partir, pero con las líneas lo más iguales posible: las mismas que partir, en el menor ancho que no añade
// ninguna. Así no queda una palabra sola en la última («chat:», «SF»).
export function equilibrar(texto: string, w: number): string[] {
  const n = partir(texto, w).length
  let mejor = w
  const minimo = Math.min(w, Math.max(...texto.split(' ').map(p => p.length)))
  for (let x = w - 1; x >= minimo && partir(texto, x).length === n; x--) mejor = x
  return partir(texto, mejor)
}

// Lo que pinta la bienvenida en w columnas: cada línea ya centrada y su estilo. Las del logo llevan además, aparte, la
// sangría, la barra y las letras, para pintar cada una con su color (tarea 339); sin sitio para la barra, solo las letras. La orden, en una pastilla del color de la SF con
// un espacio a cada lado; si no cabe, partida en varias del mismo ancho. Sin `invitacion` (con una incorporación en
// marcha, que tiene sus botones), solo la marca y el lema: ni «Para empezar…», ni la orden, ni lo que viene después
// (tarea 333, a petición del propietario).
export type LineaBienvenida = {
  texto: string
  estilo: 'logo' | 'nombre' | 'lema' | 'normal' | 'orden' | 'tenue' | 'hueco'
  logo?: { sangria: number; barra: string; letras: string }
}
export function bienvenida(w: number, invitacion = true): LineaBienvenida[] {
  const ancho = Math.max(12, w)
  const c = (t: string) => centrar(t, ancho).trimEnd()
  const l: LineaBienvenida[] = [{ texto: '', estilo: 'hueco' }]
  if (ancho >= ANCHO_LETRAS) {
    for (const { barra, letras } of logoTexto(ancho)) {
      const texto = c(barra + letras)
      const sangria = texto.length - texto.trimStart().length - (barra + letras).length + (barra + letras).trimStart().length
      l.push({ texto, estilo: 'logo', logo: { sangria, barra, letras: letras.trimEnd() } })
    }
    l.push({ texto: '', estilo: 'hueco' })
  }
  for (const x of ancho >= NOMBRE_ANCHO.length ? [NOMBRE_ANCHO] : equilibrar(NOMBRE, ancho)) l.push({ texto: c(x), estilo: 'nombre' })
  l.push({ texto: '', estilo: 'hueco' })
  for (const x of equilibrar(LEMA, Math.min(ancho, 44))) l.push({ texto: c(x), estilo: 'lema' })
  l.push({ texto: '', estilo: 'hueco' })
  if (!invitacion) return l
  l.push({ texto: '', estilo: 'hueco' })
  for (const x of equilibrar(PARA_EMPEZAR, ancho)) l.push({ texto: c(x), estilo: 'normal' })
  l.push({ texto: '', estilo: 'hueco' })
  const trozos = equilibrar(ORDEN_EMPEZAR, ancho - 2)
  const largo = Math.max(...trozos.map(t => t.length))
  for (const x of trozos) {
    const pastilla = ` ${x.padEnd(largo)} `
    l.push({ texto: pastilla, estilo: 'orden' })
  }
  l.push({ texto: '', estilo: 'hueco' })
  for (const x of equilibrar(DESPUES, Math.min(ancho, 44))) l.push({ texto: c(x), estilo: 'tenue' })
  return l
}

// Los espacios delante de la pastilla de la orden, para centrarla en w columnas (va aparte porque lleva fondo).
export const sangriaOrden = (pastilla: string, w: number) => Math.max(0, Math.floor((Math.max(12, w) - pastilla.length) / 2))
