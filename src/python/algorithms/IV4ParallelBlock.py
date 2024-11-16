import numpy as np
from multiprocessing import Pool

def calcular_bloque(matriz1, matriz2, ii, jj, kk, block_size, n):
    """
    Calcula un bloque parcial de la matriz resultado usando NumPy.
    """
    # Extraer submatrices relevantes
    bloque_matriz1 = matriz1[ii:ii + block_size, kk:kk + block_size]
    bloque_matriz2 = matriz2[kk:kk + block_size, jj:jj + block_size]

    # Multiplicar bloques y devolver la submatriz resultado
    return ii, jj, np.dot(bloque_matriz1, bloque_matriz2)

def multiplicar_iv4_parallel_block(matriz1, matriz2, n, block_size=2):
    """
    Multiplica matrices en paralelo usando bloques con NumPy.
    """
    # Convertir matrices a NumPy para optimizar operaciones
    matriz1 = np.array(matriz1, dtype=int)
    matriz2 = np.array(matriz2, dtype=int)
    resultado = np.zeros((n, n), dtype=int)

    # Crear grupo de procesos
    with Pool() as pool:
        tareas = []

        # Programar tareas para cada combinación de bloques
        for ii in range(0, n, block_size):
            for jj in range(0, n, block_size):
                for kk in range(0, n, block_size):
                    tareas.append(pool.apply_async(
                        calcular_bloque,
                        args=(matriz1, matriz2, ii, jj, kk, block_size, n)
                    ))

        # Recoger los resultados y combinarlos
        for tarea in tareas:
            ii, jj, bloque_resultado = tarea.get()
            resultado[ii:ii + block_size, jj:jj + block_size] += bloque_resultado

    return resultado.tolist()