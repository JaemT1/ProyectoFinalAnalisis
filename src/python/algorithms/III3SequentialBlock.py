def multiplicar_iii3_sequential_block(matriz1, matriz2, n, block_size=2):
    resultado = [[0] * n for _ in range(n)]
    for ii in range(0, n, block_size):
        for jj in range(0, n, block_size):
            for kk in range(0, n, block_size):
                for i in range(ii, min(ii + block_size, n)):
                    for j in range(jj, min(jj + block_size, n)):
                        suma = 0
                        for k in range(kk, min(kk + block_size, n)):
                            suma += matriz1[i][k] * matriz2[k][j]
                        resultado[i][j] += suma
    return resultado
