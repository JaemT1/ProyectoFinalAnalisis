import concurrent.futures

def multiplicar_iv5_enhanced_parallel_block(matriz1, matriz2, n, block_size=2):
    resultado = [[0] * n for _ in range(n)]

    def calcular_bloque(ii, jj):
        for i in range(ii, min(ii + block_size, n)):
            for j in range(jj, min(jj + block_size, n)):
                suma = 0
                for k in range(n):
                    suma += matriz1[i][k] * matriz2[k][j]
                resultado[i][j] += suma

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for ii in range(0, n, block_size):
            for jj in range(0, n, block_size):
                futures.append(executor.submit(calcular_bloque, ii, jj))
        concurrent.futures.wait(futures)

    return resultado
