import random
from typing import Any, TextIO
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
            if tablero[i][j] == -1:
                # Celda con mina
                fila_res.append(-1)
            else:
                contador: int = 0
                vecinos = vecinos_validos(filas, columnas, i, j)
                for vecino in vecinos:
                    vi = vecino[0]
                    vj = vecino[1]
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
            if 0 <= psb < filas and 0 <= pid < columnas:
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

    copia_estado: list[list[str]] = []
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
                if estado['tablero'][i][j] == -1:
                     estado['tablero_visible'][i][j] = BOMBA  # BOMBA para las minas
                else:
                    estado['tablero_visible'][i][j] = str(estado['tablero'][i][j])  # Para otra celdas(numero)
                
            
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
                    vj = vecino[1]
                    
                    # No fue descubierta, no tiene bandera y tampoco esta pendiente de ver, se agrega a pendientes
                    if vecino not in descubiertos and vecino not in pendientes and tablero_visible[vi][vj] != BANDERA:
                        pendientes.append(vecino)
    return descubiertos

def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    """Verifica que todas las celdas que no son minas fueron descubiertas

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
                if tablero_visible[i][j] == VACIO:
                    return False
    return True
            
            


def verificar_victoria(estado: EstadoJuego) -> bool:
    """Devuelve true si todas las celdas seguras son descubiertas 

    Args:
        estado (EstadoJuego): diccionario de los diferentes valores asociadoas al estado de juego

    Returns:
        bool: valor de verdad
    """
    return todas_celdas_seguras_descubiertas(estado['tablero'], estado['tablero_visible'])


def reiniciar_juego(estado: EstadoJuego) -> None:
    """Reinicia el juego manteniendo las dimensiones del tablero y
    cantidad de minas.
    Cambia el estado del juego.

    Args:
        estado (EstadoJuego): diccionario de los diferentes valores asociados al estado del juego
    """
    filas: int = estado['filas']
    columnas: int = estado['columnas']
    minas: int = estado['minas']    
    
    # Copia del tablero con nueva disposicion de minas en el tablero
    tablero_nuevo = colocar_minas(filas, columnas, minas)
    calcular_numeros(tablero_nuevo)
    
    # Creacion del tablero visible con celdas de valor VACIO
    tablero_visible_nuevo: list[list[str]] = []
    for i in range(filas):
        fila_visible: list[str] = []
        for j in range(columnas):
            fila_visible.append(VACIO)
        tablero_visible_nuevo.append(fila_visible)
        
    # Actualizacion de estados
    estado['tablero']= tablero_nuevo
    estado['tablero_visible'] = tablero_visible_nuevo
    estado['juego_terminado'] = False
    


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    """Guarda el estado del juego en dos archivos de texto, uno para tablero y otro para tablero visible

    Args:
        estado (EstadoJuego): diccionario de valores asociados al estado del juego
        ruta_directorio (str): ruta del archivo
    """
    tablero_visible: list[list[str]] = estado['tablero_visible']
    tablero: list[list[int]] = estado['tablero']
    # Genero mis text files de tableros
    ruta_tablero:str = os.path.join(ruta_directorio, "tablero.txt")
    ruta_tablero_visible:str = os.path.join(ruta_directorio, "tablero_visible.txt")
    
    guardar_tablero(tablero, ruta_tablero)
    guardar_tablero_visible(tablero_visible, ruta_tablero_visible)
    return

def guardar_tablero(tablero: list[list[int]], ruta_archivo: str) -> None:
    """Guarda el tablero en un archivo de texto, separado por comas y sin espacios

    Args:
        tablero (list[list[int]]): tablero
        ruta_archivo (str): ruta del archivo
    """
    archivo: TextIO = open(ruta_archivo, "w")
    for fila in tablero:
        linea: str = ""
        filas: int = len(fila)
        for i in range(filas): 
            linea += str(fila[i])
            if i < filas - 1:
                linea += ","
        archivo.write(linea + "\n")
    archivo.close()

def guardar_tablero_visible(tablero_visible: list[list[str]], ruta_archivo: str):
    """Guarda el tablero visible en un archivo 
    reemplazando los simbolos por otros caracteres

    Args:
        tablero_visible (list[list[str]]): tablero visible
        ruta_archivo (str): ruta del archivo
    """
    archivo: TextIO = open(ruta_archivo, "w")
    for fila in tablero_visible:
        linea:str = ""
        filas: int = len(fila)
        for i in range(filas):
            celda: str = fila[i]
            if celda == BANDERA:
                linea += "*"
            elif celda == VACIO:
                linea += "?"
            else:
                linea += celda
            if i < filas -1 :
                linea += ","
        archivo.write(linea + "\n")
    archivo.close()

def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    
    ruta_tablero: str = os.path.join(ruta_directorio, "tablero.txt")
    ruta_tablero_visible: str = os.path.join(ruta_directorio, "tablero_visible.txt")
    
    if not (existe_archivo(ruta_directorio, "tablero.txt") and existe(ruta_directorio, "tablero_visible.txt")):
        return False
    
    lineas_tablero: list[str] = leer_lineas(ruta_tablero)
    lineas_tablero_visible: list[str] = leer_lineas(ruta_tablero_visible)
    
    if not (validar_formato_lineas(lineas_tablero) and validar_formato_lineas(lineas_tablero_visible) and len(lineas_tablero) == len(lineas_tablero_visible)):
        return False
    
    tablero: list[list[int]] = convertir_a_tablero(lineas_tablero)
    tablero_visible: list[list[str]] = convertir_a_tablero_visible(lineas_tablero_visible)
    
    filas:int = len(tablero)
    columnas: int = len(tablero[0])
    celdas_seguras_ocultas: int = 0
    minas: int = 0
    
    for i in range(filas):
        for j in range(columnas):
            valor: int = tablero[i][j]
            valor_visible: str = tablero_visible[i][j]
            
            if valor == -1:
                minas += 1
            if valor > 0 and valor_visible == VACIO:
                celdas_seguras_ocultas += 1
 
    # Actualizar 
    estado['tablero'] = tablero  
    estado['tablero_visible'] = tablero_visible   
    estado['minas'] = minas  
    estado['celdas_seguras_ocultas'] = celdas_seguras_ocultas  
    estado['filas'] = filas  
    estado['columnas'] = columnas  
    return True  
    
def leer_lineas(ruta_archivo: str) -> list[str]:
    """Lee las lineas no vacias de un archivo de texto y devuelve 
    una lista de strings sin espacios ni saltos de lineas

    Args:
        ruta_archivo (str): ruta dela rchivo

    Returns:
        list[str]: lista de lineas del archivo modificada
    """
    archivo: TextIO = open(ruta_archivo, "r")
    lineas: list[str] = []
    for linea in archivo:
        linea_strip: str = linea.strip()
        if linea.strip() != "":
            lineas.append(linea_strip)
    archivo.close()
    return lineas
def validar_formato_lineas(lineas: list[str])-> bool:
    """Verifica que se cumpla la cantidad de comas por lineas

    Args:
        lineas (list[str]): _description_

    Returns:
        bool: _description_
    """
    if len(lineas) == 0:
        return False
    cantidad_de_comas: int = 0
    for caracter in lineas[0]:
        if caracter == ',':
            cantidad_de_comas += 1
    for linea in lineas:
        comas_lineas: int = 0
        for caracter in linea:
            if caracter == ',':
                comas_lineas += 1
        if comas_lineas != cantidad_de_comas:
            return False
    return True

def convertir_a_tablero(lineas: list[str]) -> list[list[int]]:
    """Convierte de listas de lineas de texto a tablero

    Args:
        lineas (list[str]): _description_

    Returns:
        list[list[int]]: _description_
    """
    tablero: list[list[int]] = []
    for linea in lineas:
        fila_str: list[str] = linea.split(',')
        fila_int: list[int] = []
        for valor in fila_str:
            fila_int.append(int(valor))
        tablero.append(fila_int)
    return tablero

def convertir_a_tablero_visible(lineas: list[str]) -> list[list[str]]:
    """Convierte de una lista de lineas del archivo de texto de tablero visible al tablero visible

    Args:
        lineas (list[str]): _description_

    Returns:
        list[list[str]]: _description_
    """
    tablero_visible: list[list[str]] = []
    for linea in lineas:
        fila_str: list[str] = linea.split(",")
        fila: list[str] = []
        for simbolo in fila_str:
            if simbolo == "*":
                fila.append(BANDERA)
            elif simbolo == "?":
                fila.append(VACIO)
            else:
                fila.append(simbolo)
        tablero_visible.append(fila)
    return tablero_visible