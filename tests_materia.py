import unittest
from buscaminas import (crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,
                               reiniciar_juego, colocar_minas, calcular_numeros, verificar_victoria, guardar_estado, cargar_estado, BOMBA, BANDERA, VACIO, EstadoJuego)


'''
Ayudamemoria: entre los métodos para testear están los siguientes:

    self.assertEqual(a, b) -> testea que a y b tengan el mismo valor
    self.assertTrue(x)     -> testea que x sea True
    self.assertFalse(x)    -> testea que x sea False
    self.assertIn(a, b)    -> testea que a esté en b (siendo b una lista o tupla)
'''
def cant_minas_en_tablero(tablero: list[list[int]]) -> int:
    """Chequea que el número de minas en el tablero sea igual al número de minas esperado"""
    contador_minas:int = 0
    for fila in tablero:
        for celda in fila:
            if celda == -1:
                contador_minas += 1
    return contador_minas

def son_solo_ceros_y_bombas (tablero: list[list[int]]) -> bool:
    for fila in tablero:
        for celda in fila:
            if celda not in [0, -1]:
                return False
    return True

def dimension_correcta(tablero: list[list[int]], filas: int, columnas: int) -> bool:
    """Chequea que el tablero tenga las dimensiones correctas"""
    if len(tablero) != filas:
        return False
    for fila in tablero:
        if len(fila) != columnas:
            return False
    return True



class colocar_minasTest(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1
        
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)

        # Testeamos que las dimensiones del tablero sean correctas
        self.assertTrue(dimension_correcta(tablero, filas, columnas))
    
    def test_muchas_iteraciones(self):
        filas = 4
        columnas = 4
        minas = 5
        for _ in range(20):
            tablero = colocar_minas(filas, columnas, minas)
            self.assertTrue(dimension_correcta(tablero, filas, columnas))
            self.assertEqual(cant_minas_en_tablero(tablero), minas)
            self.assertTrue(son_solo_ceros_y_bombas(tablero))

class calcular_numerosTest(unittest.TestCase):
    def test_ejemplo(self):
        tablero = [[0,-1],
                   [0, 0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1,-1],
                                   [1, 1]])
        
    def test_fila_unica(self):
        tablero = [[0, -1, 0, 0]]
        calcular_numeros(tablero)
        self.assertEqual(tablero, [[1, -1, 1, 0]])

    def test_tablero_grande(self):
        tablero = [[0,  0, -1],
                   [0,  0,  0],
                   [-1, 0,  0]
                   ]
        calcular_numeros(tablero)
        self.assertEqual(tablero, [[0, 1, -1],
                                   [1, 2,  1],
                                   [-1, 1, 0]])

class crear_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)

    def test_tablero_mas_grande(self):
        estado = crear_juego(5, 5, 3)
        self.assertTrue(dimension_correcta(estado['tablero'], 5, 5))
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)

class obtener_estado_tablero_visibleTest(unittest.TestCase):
    def test_ejemplo(self):
        estado = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1, 1],
                        [1, 1]],
            'tablero_visible': [[VACIO, '1'],
                                [VACIO, VACIO]],
            'juego_terminado': False
        }

        visible = obtener_estado_tablero_visible(estado)

        # Testea que la copia sea igual al original
        self.assertEqual(visible, estado['tablero_visible'])

        # Testea que sea una copia (modificar visible no cambia el original)
        visible[0][0] = 'MODIFICADO'
        self.assertNotEqual(visible, estado['tablero_visible'])


        




