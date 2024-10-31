import numpy as np
import time
import os

def generar_matriz(n):
    """Genera una matriz n*n con números aleatorios de 6 dígitos."""
    return np.random.randint(100000, 999999, size=(n, n)).tolist()

def guardar_matriz_en_txt(matriz, filepath):
    """Guarda la matriz en un archivo .txt en la ruta especificada."""
    try:
        # Asegura que el directorio existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w') as f:
            for fila in matriz:
                f.write(' '.join(map(str, fila)) + '\n')
    except Exception as e:
        print(f"Error al guardar la matriz en {filepath}: {e}")

def cargar_matriz_desde_txt(filepath):
    """Carga una matriz desde un archivo .txt en la ruta especificada."""
    try:
        with open(filepath, 'r') as f:
            return [list(map(int, line.strip().split())) for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: El archivo {filepath} no fue encontrado.")
        return []
    except Exception as e:
        print(f"Error al cargar la matriz desde {filepath}: {e}")
        return []

def medir_tiempo(funcion, *args):
    """Mide el tiempo de ejecución de una función en segundos y lo formatea a 6 decimales, usando notación científica solo cuando es menor a 1e-5."""
    inicio = time.perf_counter()
    resultado = funcion(*args)
    fin = time.perf_counter()
    tiempo = fin - inicio

    # Formato condicional
    if tiempo < 1e-5:
        tiempo_formateado = f"{tiempo:.6e}"  # Notación científica para tiempos muy pequeños
    else:
        tiempo_formateado = f"{tiempo:.6f}"  # Notación decimal con 6 decimales

    return tiempo_formateado, resultado

