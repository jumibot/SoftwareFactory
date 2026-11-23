# Al cambiar el color principal del estilo se recalculan solos sus derivados

En la skill que fija los parámetros del estilo, cambiar colores.primario recalcula su familia, en claro y en oscuro: primario-vivo, primario-texto, fondo, tenue, acento y sus fondos y bordes, y el primario oscuro. Se mantiene lo que se pida en el mismo cambio. Se usa la misma mezcla con blanco y negro que ya usan los temas de la identidad.

Por qué: en la prueba de la tarea «Construir la skill que fija los parámetros del estilo» (392), poner el primario en amarillo dejó el resto en el terracota del tema de partida, y el documento salió medio amarillo y medio terracota. Se descartaron un atajo colores.marca aparte y cambiar los derivados a mano.
