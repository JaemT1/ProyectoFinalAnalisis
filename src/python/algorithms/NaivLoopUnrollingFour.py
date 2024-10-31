def multiplicar_naiv_loop_unrolling_four(matriz1, matriz2, n):
    # Inicializar la matriz resultado con ceros
    resultado = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            suma = 0

            # Procesar bloques de 4 elementos
            for k in range(0, n // 4 * 4, 4):
                suma += (matriz1[i][k] * matriz2[k][j] +
                         matriz1[i][k + 1] * matriz2[k + 1][j] +
                         matriz1[i][k + 2] * matriz2[k + 2][j] +
                         matriz1[i][k + 3] * matriz2[k + 3][j])

            # Manejar los elementos restantes
            for k in range(n // 4 * 4, n):
                suma += matriz1[i][k] * matriz2[k][j]

            resultado[i][j] = suma

    return resultado