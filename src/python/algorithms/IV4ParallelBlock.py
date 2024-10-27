import multiprocessing

def multiplicar_iv4_parallel_block(matriz1, matriz2, n, block_size=64):
    resultado = [[0] * n for _ in range(n)]

    def calcular_bloque(ii, jj):
        for i in range(ii, min(ii + block_size, n)):
            for j in range(jj, min(jj + block_size, n)):
                suma = 0
                for k in range(n):
                    suma += matriz1[i][k] * matriz2[k][j]
                resultado[i][j] += suma

    with multiprocessing.Pool() as pool:
        for ii in range(0, n, block_size):
            for jj in range(0, n, block_size):
                pool.apply_async(calcular_bloque, args=(ii, jj))
        pool.close()
        pool.join()

    return resultado
