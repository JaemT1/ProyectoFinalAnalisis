import numpy as np
from concurrent.futures import ThreadPoolExecutor

def multiplicar_iv5_enhanced_parallel_block(matriz1, matriz2, n, block_size=2):
    # Convertir las matrices a NumPy arrays para operaciones rápidas, asegurando tipo entero
    matriz1 = np.array(matriz1, dtype=int)  # Asegurarse de que la matriz sea de tipo entero
    matriz2 = np.array(matriz2, dtype=int)  # Asegurarse de que la matriz sea de tipo entero
    resultado = np.zeros((n, n), dtype=int)  # Asegurarse de que el resultado sea de tipo entero

    def calcular_bloque(ii, jj):
        """
        Calcula un bloque del resultado usando NumPy para aprovechar la vectorización.
        """
        bloque_matriz1 = matriz1[ii:ii + block_size, :]
        bloque_matriz2 = matriz2[:, jj:jj + block_size]
        resultado_bloque = np.dot(bloque_matriz1, bloque_matriz2)
        resultado[ii:ii + block_size, jj:jj + block_size] += resultado_bloque

    # Ejecutar cálculos en paralelo
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(calcular_bloque, ii, jj)
            for ii in range(0, n, block_size)
            for jj in range(0, n, block_size)
        ]
        # Esperar a que todos los futuros se completen
        for future in futures:
            future.result()

    # Convertir el resultado a lista de enteros si es necesario
    return resultado.tolist()
