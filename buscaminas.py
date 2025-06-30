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

def filas_columnas_vecinas(tablero: list[list[int]]) -> None:
    """Calculamos la cantidad de minas en las celdas vecinas de cada celda en el tablero"""
    filas:int = len(tablero)
    columnas:int = len(tablero[0])

    for i in range(filas):
        for j in range(columnas):
            if tablero[i][j] != -1:
                contador:int = 0
                #subir bajar posiciones
                for sb in [-1, 0, 1]:
                    #izquierda derecha posiciones
                    for id in [-1, 0, 1]:
                        if not (sb == 0 and id == 0): #combinaciones de posicion:
                            psb:int = i + sb   
                            pid:int = j + id
                            if 0 <= psb < filas and 0 <= pid < columnas:
                                if tablero[psb][pid] == -1:
                                    contador += 1
                tablero[i][j] = contador

def calcular_numeros(tablero: list[list[int]]) -> None :
    filas:int = len(tablero)
    columnas:int = len(tablero[0])

    tablero_original: list[list[int]] = []
    for fila in tablero:
        fila_nueva:list[int] = []
        for numero in fila:
            fila_nueva.append(numero)
        tablero_original.append(fila_nueva)
        
    filas_columnas_vecinas(tablero_original)
    

        
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
            celda = estado['tablero_visible'][fila][columna]
            
            if celda == VACIO:
                estado['tablero_visible'][fila][columna] = BANDERA
            elif celda == BANDERA:
                estado['tablero_visible'][fila][columna] = VACIO


def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    return


def verificar_victoria(estado: EstadoJuego) -> bool:
    return True


def reiniciar_juego(estado: EstadoJuego) -> None:
    return


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    return


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    return False