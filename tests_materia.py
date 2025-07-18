import unittest, tempfile
from buscaminas import (crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,
                               reiniciar_juego, colocar_minas, calcular_numeros, verificar_victoria, guardar_estado,  BOMBA, BANDERA, VACIO, EstadoJuego)


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

class marcar_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)


class descubrir_celdaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 2, 2)
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO, VACIO],
            [VACIO, "3", "1"],
            [VACIO, "2", "0"]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [2, -1, 1],
            [-1, 3, 1],
            [-1, 2, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertFalse(estado['juego_terminado'])

    def test_descubrir_mina_termina_juego(self):
        estado = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[-1, 1],
                        [1, 1]],
            'tablero_visible': [[VACIO, VACIO],
                                [VACIO, VACIO]],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 0)
        self.assertTrue(estado['juego_terminado'])
        self.assertEqual(estado['tablero_visible'][0][0], BOMBA)

    def test_descubrir_celda_bloqueada_por_bandera(self):
        estado = crear_juego(2, 2, 0)
        estado['tablero'] = [[0, 0],
                             [0, 0]]
        estado['tablero_visible'] = [[BANDERA, VACIO],
                                     [VACIO, VACIO]]
        descubrir_celda(estado, 0, 0)
        # La celda con bandera no debe cambiar
        self.assertEqual(estado['tablero_visible'][0][0], BANDERA)


class verificar_victoriaTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        # Testeamos que el juego no esté terminado y que no haya ganado
        self.assertTrue(verificar_victoria(estado))
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            ["1", "1"]
        ])
        self.assertFalse(estado['juego_terminado'])

    def test_celda_oculta_sin_descubrir_no_gano(self):
        estado = crear_juego(2, 2, 1)
        estado['tablero'] = [[-1, 1],
                             [1, 1]]
        estado['tablero_visible'] = [[VACIO, VACIO],
                                     [VACIO, VACIO]]
        self.assertFalse(verificar_victoria(estado))

    def test_juego_terminado_pero_faltan_celdas(self):
        estado = crear_juego(2, 2, 1)
        estado['tablero'] = [[-1, 1],
                             [1, 1]]
        estado['tablero_visible'] = [[VACIO, "1"],
                                     [VACIO, "1"]]
        estado['juego_terminado'] = True
        self.assertFalse(verificar_victoria(estado))
        


class obtener_estado_tableroTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
         # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])


class reiniciar_juegoTest(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [ 1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        reiniciar_juego(estado)
        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [
            [-1, 1],
            [ 1, 1]
        ])

    def test_reinicia_juego_con_misma_dim(self):
        estado = crear_juego(3, 3, 2)
        viejo_tablero = [fila.copy() for fila in estado['tablero']]
        reiniciar_juego(estado)
        self.assertEqual(len(estado['tablero']), 3)
        self.assertEqual(len(estado['tablero_visible'][0]), 3)
        self.assertNotEqual(estado['tablero'], viejo_tablero)
        self.assertFalse(estado['juego_terminado'])



if __name__ == '__main__':
    unittest.main(verbosity=2)


        




