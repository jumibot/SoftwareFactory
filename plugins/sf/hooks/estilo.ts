

// Amarillo claro de la tarea en curso: el de la paleta (#ca8a04) se ve mostaza en el panel oscuro.
export const COLOR_TAREA = '#facc15'
// Fondo de las etiquetas neutras de la cabecera: el marcador y la rama que no es de una tarea.
export const FONDO_ETIQUETA = '#3f3f46'
// Fondo de las etiquetas del menú de órdenes de una tarea. A prueba, negro (petición del propietario, 2026-11-01); el
// anterior era un amarillo oscuro y apagado, '#4a4226': para volver, basta con ponerlo aquí.
export const FONDO_ORDEN = '#000000'

// La letra del código de tarea, más apagada que el número, en su mismo tono (dimColor se quedaba corto).
// Los números de tarea ocupan tres columnas, alineados a la derecha: «  4», « 41», «236» (petición del propietario,
// 2026-10-31; antes, dos). El hueco delante va fuera del botón del número, para que nada lo recorte.
export const ANCHO_NUMERO = 3
export const hueco = (id: number | string) => Math.max(0, ANCHO_NUMERO - String(id).length)

// Un color por letra, igual en las cuentas y en los códigos: verde solo para las C; las demás, sin color. La tarea
// en curso, en amarillo (decisión del propietario, 2026-10-28). El rojo, solo para las reabiertas, como fondo del
// número; las H de sesiones anteriores, sin rojo (petición del propietario, 2026-10-31).
export const colorLetra = (l: string) => (l === 'C' ? 'success' : undefined)
export const colorLetraApagada = (l: string) => (l === 'C' ? LETRA.cerrada : LETRA.neutra)

// La marca del subagente de una tarea, verde si trabaja y roja si espera (decisión 162). Windows Terminal dibuja la
// ⚙ (U+2699) como emoji, gris, sin el color del texto: va ● (U+25CF), que está en las fuentes de terminal y toma
// el color. La alternativa es '⚙︎', la ⚙ con el selector de texto, que no todos los terminales respetan. Ocupa
// una columna, como Activar rama, la C y la D; con los espacios, tres.
export const MARCA_SUBAGENTE = '●'
// Las órdenes de una tarea que destruyen (Eliminar, Descartar, Revertir), en rojo; las demás, con la letra normal
// (decisión 168, precisada por el propietario el 2026-11-01). El rojo claro de ACTUALIZAR, legible sobre el gris.
export const COLOR_ORDEN_DESTRUCTIVA = '#f87171'
// El de TURBO, en la cabecera: cian, lejos del naranja de PRUEBA y en letra, no en fondo como el nombre.
export const COLOR_TURBO = '#22d3ee'
// El de RELEASE, a su lado: violeta, distinto del cian de TURBO, del naranja de PRUEBA y del amarillo de la tarea.
export const COLOR_RELEASE = '#c084fc'
// El de ACTUALIZAR, junto a RELEASE: rojo, para no confundirlos (decisión del propietario, 2026-10-29).
export const COLOR_ACTUALIZAR = '#f87171'
// Los avisos, bajo las dos filas de la cabecera: fondo blanco y letra oscura (petición del propietario, 2026-11-01).
export const FONDO_AVISO = '#ffffff'
// Con varios avisos, uno por turno, el fondo alterna entre blanco y este gris claro, para que se note el cambio
// (decisión 164).
export const FONDO_AVISO_ALTERNO = '#d4d4d4'
export const COLOR_AVISO = '#1a1a1a'
// Los avisos emergentes (toasts) y sus errores, distintos de un vistazo (petición del propietario, tarea 257). El
// toast del motor solo admite texto, sin fondo ni color: la marca del principio hace de fondo, un cuadrado de color
// (emoji, que los terminales pintan en color). Azul, los avisos; rojo, los errores, como las órdenes que destruyen.
export const MARCA_AVISO_EMERGENTE = '🟦'
export const MARCA_ERROR_EMERGENTE = '🟥'

// Texto de las tareas en las secciones, un punto menos brillante que el normal (decisión del propietario, 2026-10-28).
export const TEXTO_TAREA = '#717171'
// Texto de los pasos pendientes y en curso: algo más claro que el de las tareas, sin llegar al blanco, para que se
// distinga bien del gris oscuro de los hechos, LETRA.neutra (petición del propietario, 2026-11-01, tarea 256).
export const TEXTO_PASO = '#a3a3a3'

export const LETRA = { tarea: '#a88a14', cerrada: '#3a9355', reabierta: '#ab4040', neutra: '#4f4f4f' } as const

// Las etiquetas de la cabecera, todas del mismo ancho salvo la de la rama (tarea 260): el de ACTUALIZAR con su
// relleno de siempre, « ACTUALIZAR », 12 columnas (petición del propietario, 2026-11-01: «todos del tamaño de
// actualizar»). El texto va centrado con espacios dentro del propio texto, sobre su fondo: no depende de que el
// terminal respete minWidth ni justifyContent, que en el panel real no ensanchaban la etiqueta. «N prompts» se queda
// en 12 hasta 9999 comiéndose su relleno (11 o 12 letras); lo más largo (las confirmaciones) crece lo que necesita.
// En un panel estrecho, el común se reduce a lo que cabe en cada fila, comiéndose el relleno, sin bajar del texto más
// largo (con ACTUALIZAR, 10); si ni así cabe, cada una vuelve a su ancho propio (null), como antes, y la línea no se
// parte. Visto en el terminal real (claude en una pseudoterminal): con un panel de unas 60 columnas, ACTUALIZAR y
// PRUEBA, exigir el relleno dejaba cada etiqueta con su ancho, que es lo que vio el propietario.
export const ANCHO_ETIQUETA = ' ACTUALIZAR '.length
// `filas`: por fila, las columnas que necesita como mínimo cada etiqueta de ancho común (su texto) y las que reserva
// para lo demás; entre dos etiquetas, una columna de separación.
export const anchoComun = (disponible: number, filas: { necesita: number[]; reserva: number }[]): number | null => {
  const mayor = Math.max(0, ...filas.flatMap(f => f.necesita))
  const ocupa = (w: number, f: { necesita: number[]; reserva: number }) =>
    f.necesita.reduce((a, n) => a + Math.max(w, n), 0) + Math.max(0, f.necesita.length - 1) + f.reserva
  for (let w = ANCHO_ETIQUETA; w >= Math.min(ANCHO_ETIQUETA, mayor); w--) {
    if (filas.every(f => f.necesita.length === 0 || ocupa(w, f) <= disponible)) return w
  }
  return null
}
// Los espacios a cada lado para centrar n columnas en w: el que sobra, a la derecha.
export const huecos = (n: number, w: number): [number, number] => {
  const libre = Math.max(0, w - n)
  return [Math.floor(libre / 2), libre - Math.floor(libre / 2)]
}
export const centrar = (t: string, w: number) => {
  const [i, d] = huecos(t.length, w)
  return ' '.repeat(i) + t + ' '.repeat(d)
}

// Los puntos de una prueba o de lo que comprobó Claude, para listarlos (tarea 237): los textos separan los puntos con
// «;» y a veces empiezan por un contexto con «:» («Tras publicar: a; b»). El contexto, si lo hay, aparte: solo si es
// corto (hasta 40 caracteres) y va antes del primer «;». Sin «;», un solo punto; sin contexto, null.
export const puntosDe = (texto: string): { contexto: string | null; puntos: string[] } => {
  let resto = texto.trim()
  let contexto: string | null = null
  const dosPuntos = resto.indexOf(':')
  const puntoYComa = resto.indexOf(';')
  if (dosPuntos > 0 && dosPuntos <= 40 && (puntoYComa < 0 || dosPuntos < puntoYComa) && resto.slice(dosPuntos + 1).trim() !== '') {
    contexto = resto.slice(0, dosPuntos).trim()
    resto = resto.slice(dosPuntos + 1).trim()
  }
  const puntos = resto
    .split(';')
    .map(x => x.trim())
    .filter(x => x !== '')
    .map(x => x.charAt(0).toUpperCase() + x.slice(1))
  return { contexto, puntos: puntos.length > 0 ? puntos : [resto] }
}
