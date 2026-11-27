import type { ClientModule, RenderNode } from 'claude-code'

// Lo pulsable del panel en la app de escritorio que el botón nativo no sabe pintar (tarea 432): la línea entera de una
// tarea, las órdenes de la tarea y la marca del subagente. Es un módulo de superficie (Client): lo dibuja la app con su
// texto de color y su fondo, sin botón nativo, y un clic izquierdo en cualquier punto de su región avisa al panel
// (surface.post), que responde en su hook de ui.message con lo mismo que el botón del terminal. Solo en la app de
// escritorio, la única superficie gráfica con Client; VS Code y el móvil siguen con botones nativos.

// Un Text del panel como datos (las props de un Client lo son): sus estilos y sus hijos, texto u otros Text.
export type TextoDatos = string | { estilo: Record<string, string | number | boolean>; hijos: TextoDatos[] }

// Las tres formas: la etiqueta de una orden (texto de color sobre una etiqueta redondeada de altura mínima con el fondo
// dado), un texto suelto (la marca del subagente) y la línea de una tarea (cabeza, título y «▸» o «▾», que se pulsa
// entera).
export type PropsPulsable =
  | { forma: 'etiqueta'; texto: TextoDatos; fondo: string }
  | { forma: 'texto'; texto: TextoDatos }
  | { forma: 'linea'; cabeza: TextoDatos | null; ancho: number; delante: number; cuerpo: TextoDatos; abierta: boolean; flecha: string }

const Pulsable: ClientModule = (datos, surface) => {
  const { Box, Text } = surface.elements
  const p = datos as unknown as PropsPulsable
  // Un clic: el botón izquierdo que sube dentro de la región. El panel decide qué hace por la clave del Client.
  surface.onPointer(ev => {
    if (ev.type === 'up' && ev.button === 'left') surface.post({ pulsa: true })
  })
  const texto = (t: TextoDatos): RenderNode => (typeof t === 'string' ? t : <Text {...t.estilo}>{t.hijos.map(texto)}</Text>)
  if (p.forma === 'etiqueta')
    // El contorno, del color del fondo, es lo que redondea la etiqueta: en la app se dibuja con la medida de la
    // superficie, una línea fina, no una celda; sin relleno arriba ni abajo, la etiqueta queda del alto del texto.
    return (
      <Box flexShrink={0} backgroundColor={p.fondo} borderStyle="round" borderColor={p.fondo} paddingX="xs" paddingY={0}>
        <Text>{texto(p.texto)}</Text>
      </Box>
    )
  if (p.forma === 'texto') return <Text>{texto(p.texto)}</Text>
  return (
    // Arriba y no centrado: si el título se parte en varias líneas, el número queda con la primera, como en el terminal;
    // el hueco delante alinea los números a la derecha.
    <Box flexDirection="row" alignItems="flex-start" minWidth={0} width="100%">
      {p.cabeza !== null && (
        <Box minWidth={p.ancho} flexShrink={0} paddingLeft={p.delante}>
          {typeof p.cabeza === 'string' ? <Text>{p.cabeza}</Text> : texto(p.cabeza)}
        </Box>
      )}
      <Box flexShrink={1} flexGrow={1} minWidth={0} overflow="hidden">
        <Text wrap={p.abierta ? 'wrap' : 'truncate-end'}>{texto(p.cuerpo)}</Text>
      </Box>
      <Box flexShrink={0} marginLeft={1}>
        <Text>{p.flecha}</Text>
      </Box>
    </Box>
  )
}
export default Pulsable
