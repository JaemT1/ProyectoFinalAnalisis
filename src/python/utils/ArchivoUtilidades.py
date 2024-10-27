import numpy as np
import time

def generar_matriz(n):
    """Genera una matriz n*n con números aleatorios de 6 dígitos."""
    return np.random.randint(100000, 999999, size=(n, n)).tolist()

def guardar_matriz_en_txt(matriz, filename):
    """Guarda la matriz en un archivo .txt."""
    with open(filename, 'w') as f:
        for fila in matriz:
            f.write(' '.join(map(str, fila)) + '\n')

def cargar_matriz_desde_txt(filename):
    """Carga una matriz desde un archivo .txt."""
    with open(filename, 'r') as f:
        return [list(map(int, line.strip().split())) for line in f.readlines()]

def medir_tiempo(funcion, *args):
    """Mide el tiempo de ejecución de una función."""
    inicio = time.time()
    resultado = funcion(*args)
    fin = time.time()
    return fin - inicio, resultado
