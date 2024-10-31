def multiplicar_naiv(matriz1, matriz2, n):
    resultado = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                resultado[i][j] += matriz1[i][k] * matriz2[k][j]
    return resultado
