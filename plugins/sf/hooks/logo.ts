import { COLOR_SF, RGB } from './constantes'

// ── El logo «/SF» (tarea 339, decisión 255) ──
// Una barra delante de SF, para que recuerde la orden /sf que abre el panel: estrecha y empinada (≈79°), pixelada
// como las letras, y en un morado más claro que ellas para que se lea como tecla y no como ruta. En un terminal sin
// color real la barra queda del color de las letras: se sigue leyendo «/SF», y está bien así.

// Las letras, en el morado de la SF (COLOR_SF, #827dbd); la barra, en el morado claro.
export const COLOR_LETRAS = RGB[COLOR_SF]
export const COLOR_BARRA = '#b3aee6'

// «SF» en letra de bloques, cinco filas de 13 columnas.
export const LETRAS = [
  '▄█████ ██████',
  '██     ██    ',
  '▀████▄ █████ ',
  '    ██ ██    ',
  '█████▀ ██    ',
]
// La barra, cinco filas de 4 columnas y una de hueco, el mismo que hay entre S y F.
export const BARRA = [
  '  ██ ',
  ' ▄█▀ ',
  ' ██  ',
  '▄█▀  ',
  '██   ',
]
export const ANCHO_LETRAS = LETRAS[0]!.length
export const ANCHO_LOGO = BARRA[0]!.length + ANCHO_LETRAS

// Las filas del logo de texto para w columnas: con la barra si cabe (18); si no, solo las letras (13), antes que
// quitarlo; por debajo, ninguna. Barra y letras van aparte para pintarlas cada una con su color.
export type FilaLogo = { barra: string; letras: string }
export function logoTexto(w: number): FilaLogo[] {
  if (w >= ANCHO_LOGO) return LETRAS.map((letras, i) => ({ barra: BARRA[i]!, letras }))
  if (w >= ANCHO_LETRAS) return LETRAS.map(letras => ({ barra: '', letras }))
  return []
}

// El logo como SVG, para las superficies gráficas (la app de escritorio, VS Code, el móvil): allí los bloques ▄█▀ van
// en una fuente que no los dibuja a una celda y el logo se descuadra (tarea 323). Cada carácter, una celda de 1×2:
// █ entera, ▄ la mitad de abajo, ▀ la de arriba. Sin barra, solo las letras.
function rects(filas: string[], x0: number): string {
  const r: string[] = []
  filas.forEach((fila, y) =>
    [...fila].forEach((c, x) => {
      const [dy, alto] = c === '█' ? [0, 2] : c === '▄' ? [1, 1] : c === '▀' ? [0, 1] : [0, 0]
      if (alto > 0) r.push(`<rect x="${x + x0}" y="${y * 2 + dy}" width="1.04" height="${alto + 0.04}"/>`)
    }),
  )
  return r.join('')
}
export function logoSvg(celda = 9, conBarra = true): string {
  const x0 = conBarra ? BARRA[0]!.length : 0
  const w = x0 + ANCHO_LETRAS
  const h = LETRAS.length * 2
  const barra = conBarra ? `<g fill="${COLOR_BARRA}">${rects(BARRA, 0)}</g>` : ''
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w * celda}" height="${h * celda}" shape-rendering="crispEdges">${barra}<g fill="${COLOR_LETRAS}">${rects(LETRAS, x0)}</g></svg>`
}
