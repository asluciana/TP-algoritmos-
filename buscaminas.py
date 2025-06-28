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

def calcular_numeros(tablero: list[list[int]]) -> None :
    filas = len(tablero)
    columnas = len(tablero[0])

    tablero_og = []
    for fila in tablero:
        fila_nueva = []
        for numero in fila:
            fila_nueva.append(numero)
        tablero_og.append(fila_nueva)
        
    for i in range(filas):
        for j in range(columnas):
            if tablero_og[i][j] != -1:
                contador = 0
                #subir bajar posiciones
                for sb in [-1, 0, 1]:
                    #izquierda derecha posiciones
                    for id in [-1, 0, 1]:
                        if not (sb == 0 and id == 0): #combinaciones de posicion:
                            psb= i + sb   
                            pid = j + id
                            if 0 <= psb < filas and 0 <= pid < columnas:
                                if tablero_og[psb][pid] == -1:
                                    contador += 1
                tablero[i][j] = contador

        
#ejecicio 3_____________________________________________________

def crear_juego(filas:int, columnas:int, minas:int) -> EstadoJuego:

    tablero = colocar_minas(filas, columnas, minas)
    calcular_numeros(tablero)

    tablero_visible = []
    for i in range(filas):
        fila_visible = []
        for j in range(columnas):
            fila_visible.append(VACIO)
        tablero_visible.append(fila_visible)
    
    estado = {
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

    copia_estado = []
    for fila in estado["tablero_visible"]:
        fila_copia = []
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