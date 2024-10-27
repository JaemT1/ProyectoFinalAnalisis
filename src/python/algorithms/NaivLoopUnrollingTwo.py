def multiplicar_naiv_loop_unrolling_two(matriz1, matriz2, n):
    resultado = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            k = 0
            while k < n - 1:
                resultado[i][j] += matriz1[i][k] * matriz2[k][j]
                resultado[i][j] += matriz1[i][k + 1] * matriz2[k + 1][j]
                k += 2
            if k < n:  # Para el caso en que n es impar
                resultado[i][j] += matriz1[i][k] * matriz2[k][j]
    return resultado
