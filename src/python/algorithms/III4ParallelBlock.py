import numpy as np
from multiprocessing import Pool, Array

def calcular_bloque(matriz1, matriz2, ii, jj, n, block_size):
    """
    Calcula un bloque de la matriz resultado usando NumPy.
    """
    # Extraer los bloques relevantes de las matrices
    bloque_matriz1 = matriz1[ii:ii + block_size]
    bloque_matriz2 = matriz2[:, jj:jj + block_size]
    # Multiplicar los bloques y devolverlos como una lista
    bloque_resultado = np.dot(bloque_matriz1, bloque_matriz2)
    return ii, jj, bloque_resultado

def multiplicar_iii4_parallel_block(matriz1, matriz2, n, block_size=2):
    """
    Multiplica matrices usando bloques en paralelo, optimizado con NumPy.
    """
    # Convertir las matrices a NumPy
    matriz1 = np.array(matriz1)
    matriz2 = np.array(matriz2)
    resultado = np.zeros((n, n))

    # Crear el grupo de procesos
    with Pool() as pool:
        tareas = []

        # Programar tareas para cada bloque
        for ii in range(0, n, block_size):
            for jj in range(0, n, block_size):
                tareas.append(pool.apply_async(calcular_bloque, args=(matriz1, matriz2, ii, jj, n, block_size)))

        # Recoger los resultados de cada tarea
        for tarea in tareas:
            ii, jj, bloque_resultado = tarea.get()
            resultado[ii:ii + block_size, jj:jj + block_size] += bloque_resultado

    return resultado.tolist()
