import random
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

def existe_archivo(ruta_directorio: str, nombre_archivo:str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))

def colocar_minas(filas:int, columnas: int, minas:int) -> list[list[int]]:
    matriz:list[list[int]] = []
    for i in range(filas):
        fila: list[int] = []
        for j in range(columnas):
            fila.append(0)
        matriz.append(fila)

    posiciones: list[tuple[int, int]] = []
    for i in range(filas):
        for j in range(columnas):
            posiciones.append((i, j))

    posiciones_minas = random.sample(posiciones, minas)

    for i, j in posiciones_minas:
        matriz[i][j] = -1

    return matriz

#ejercicio 2 ---------------------------------------------------

def filas_columnas_vecinas(tablero: list[list[int]]) -> list[list[int]]:
    """Calculamos la cantidad de minas en las celdas vecinas de cada celda en el tablero"""
    filas:int = len(tablero)
    columnas:int = len(tablero[0])
    
    res : list[list[int]] = []
    
    for i in range(filas):
        fila_res: list[int] = []
        for j in range(columnas):
            if tablero[i][j] != -1:
                # Celda con mina
                fila_res.append(-1)
            else:
                contador: int = 0
                vecinos = vecinos_validos(filas, columnas, i, j)
                for vecino in vecinos:
                    vi = vecino[0]
                    vj = vecino[j]
                    if tablero[vi][vj] == -1:
                        contador += 1
                fila_res.append(contador)
        res.append(fila_res)
    return res
                        
def vecinos_validos (filas: int, columnas: int, i: int, j: int) -> list[tuple[int,int]]:
    """ 
    Devuelve la lista de vecinos adyacentes a la posicion (i,j) 
    considerando las 8 posiciones posibles.
    """
    res : list[tuple[int,int]] = []
    # Recorremos Subiendo y Bajando
    for sb in [-1,0,1]:
        # Recorrido Izquierda y Derecha
        for id in [-1,0,1]:
            psb = i + sb
            pid = j + id
            if 0 <= psb < filas and o <= pid < columnas:
                if not(psb == i and pid == j):
                    res.append((psb,pid))
    return res

def calcular_numeros(tablero: list[list[int]]) -> None :
    # Hacemos una copia del tablero original para no modificarlo
    nuevo_tablero: list[list[int]] = filas_columnas_vecinas(tablero)
    
    filas: int = len(tablero)
    columnas: int = len(tablero[0])
    
    for i in range(filas):
        for j in range(columnas):
            tablero[i][j] = nuevo_tablero[i][j]
    

        
#ejecicio 3_____________________________________________________

def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:

    tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
    calcular_numeros(tablero)

    tablero_visible: list[list[str]]= []
    for i in range(filas):
        fila_visible: list[str] = []
        for j in range(columnas):
            fila_visible.append(VACIO)
        tablero_visible.append(fila_visible)
    
    estado: EstadoJuego = {
        "filas": filas,
        "columnas": columnas,
        "minas": minas,
        "tablero": tablero,
        "juego_terminado": False,
        "tablero_visible": tablero_visible
    }

    return estado

#ejercicio 4-----------------------------------------

def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:

    copia_estado: EstadoJuego = []
    for fila in estado["tablero_visible"]:
        fila_copia: list[str] = []
        for cell in fila:
            fila_copia.append(cell)
        copia_estado.append(fila_copia)
    return copia_estado

#ejercicio5-------------------------------------------

def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
   
    if 0 <= fila < estado['filas'] and 0 <= columna < estado['columnas']:
        if not estado['juego_terminado']:
            celda: str = estado['tablero_visible'][fila][columna]
            if celda == VACIO:
                estado['tablero_visible'][fila][columna] = BANDERA
            elif celda == BANDERA:
                estado['tablero_visible'][fila][columna] = VACIO

#ejercicio 6-------------------------------------------
def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """
    Descubre la celda en el estado dado. Si es mina, el juego termina y se muestran todas las minas del tablero.
    Caso contrario, se descubren las celdas aledanas segune el camino descubierto.
    Actualiza 'tablero_visible' y cambia el estado del juego si se topa con una mina.

    Args:
        estado (EstadoJuego): _description_
        fila (int): _description_
        columna (int): _description_
    """
    if estado['juego_terminado'] == False:
        if estado['tablero'][fila][columna] == -1:
            estado['juego_terminado'] = True
            filas: int = estado['filas']
            columnas: int = estado['columnas']
            for i in range(filas):
                for j in range(columnas):
                    if estado['tablero'][i][j] == -1:
                        estado['tablero_visible'][i][j] = BOMBA
    
    caminos: list[list[tuple[int, int]]] = caminos_descubiertos(estado['tablero'], estado['tablero_visible'], fila, columna)
    
    for camino in caminos:
        for posicion in camino:
            i = posicion[0]
            j = posicion[1]
            if estado['tablero_visible'][i][j] != BANDERA:
                estado['tablero_visible'][i][j] = str(estado['tablero'][i][j])
            
    if todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible']):
        estado['juego_terminado'] = True

def caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], f:int, c:int) -> list[list[tuple[int, int]]]:
    """Todos los caminos posibles a partir de la posicion (f,c)
    Si la celda es de valor > 0, es ella misma el unico recorrido.
    Si es 0, devuelve el listado de posiciones conectadas con mismo valor 0, o sea, celdas seguras.

    Args:
        tablero (list[list[int]]): tablero
        tablero_visible (list[list[str]]): tablero visible
        f (int): indice fila
        c (int): indice columna

    Returns:
        list[list[tuple[int, int]]]: listado de recorridos posibles de (f,c)
    """
    
    punto_de_partida: tuple[int, int] = (f, c)
    fila_de_partida: int = punto_de_partida[0]
    col_de_partida: int = punto_de_partida[1]
    
    if tablero[fila_de_partida][col_de_partida] > 0:
        return [[punto_de_partida]]
    
    else:
        recorrido: list[tuple[int,int]] = recorrido_descubierto(tablero, tablero_visible, f, c)
        if len(recorrido) > 0:
            return [recorrido]
        else:
            return []
        
def recorrido_descubierto (tablero: list[list[int]], tablero_visible: list[list[str]], f:int, c:int) -> list[tuple[int,int]]:
    """Devuelve la lista de posiciones ya descubiertas
    partiendo de la posicion (f,c)


    Args:
        tablero (list[list[int]]):tablero
        tablero_visible (list[list[str]]): tablero visible
        f (int): indice fila por donde empiezo el recorrido
        c (int): indice columna por donde empiezo el recorrido

    Returns:
        list[tuple[int,int]]: lista de posiciones descubiertas
    """
    
    filas: int = len(tablero)
    columnas: int = len(tablero[0])
    
    descubiertos: list[tuple[int,int]] = []
    pendientes: list[tuple[int,int]] = [(f,c)]
    
    while len(pendientes) > 0:
        actual = pendientes.pop(0)
        i = actual[0]
        j = actual[1]
        
        # Si no fue descubierta y no tiene BANDERA, agregamos a descubiertas
        if actual not in descubiertos and tablero_visible[i][j] != BANDERA:
            descubiertos.append(actual)
            
            # En el caso que la celda sea 0, exploramos los vecinos adyacentes a ella
            # para ver si hay mas celdas "seguras"

            if tablero[i][j] == 0:
                vecinos = vecinos_validos(filas, columnas, i, j)
                for vecino in vecinos:
                    vi = vecino[0]
                    vj = vecino[j]
                    
                    # No fue descubierta, no tiene bandera y tampoco esta pendiente de ver, se agrega a pendientes
                    if vecino not in descubiertos and vecino not in pendientes and tablero_visible[vi][vj] != BANDERA:
                        pendientes.append(vecino)
    return descubiertos

def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    """Funcion auxiliar que verifica que todas las celdas que no son minas fueron descubiertas

    Args:
        tablero (list[list[int]]): tablero
        tablero_visible (list[list[str]]): tablero visible

    Returns:
        bool: valor de verdad
    """
    
    filas: int = len(tablero)
    columnas: int = len(tablero[0])
    
    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] != -1:
                if tablero_visible == VACIO:
                    return False
    return True
            
            


def verificar_victoria(estado: EstadoJuego) -> bool:
    return True


def reiniciar_juego(estado: EstadoJuego) -> None:
    return


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    return


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    return False