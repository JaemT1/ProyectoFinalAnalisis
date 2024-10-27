def multiplicar_winograd_original(matriz1, matriz2, n):
    resultado = [[0] * n for _ in range(n)]
    row_factor = [0] * n
    col_factor = [0] * n

    for i in range(n):
        row_factor[i] = sum(matriz1[i][2 * j] * matriz1[i][2 * j + 1] for j in range(n // 2))

    for i in range(n):
        col_factor[i] = sum(matriz2[2 * j][i] * matriz2[2 * j + 1][i] for j in range(n // 2))

    for i in range(n):
        for j in range(n):
            resultado[i][j] = -row_factor[i] - col_factor[j]
            for k in range(n // 2):
                resultado[i][j] += (matriz1[i][2 * k + 1] + matriz2[2 * k][j]) * (matriz1[i][2 * k] + matriz2[2 * k + 1][j])

    if n % 2 == 1:
        for i in range(n):
            for j in range(n):
                resultado[i][j] += matriz1[i][n - 1] * matriz2[n - 1][j]

    return resultado
