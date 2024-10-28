def multiplicar_winograd_escalado(matriz1, matriz2, n):
    # Inicializa la matriz resultado y los factores de fila y columna
    resultado = [[0] * n for _ in range(n)]
    row_factor = [0] * n
    col_factor = [0] * n

    # Calcular los factores de las filas de matriz1
    for i in range(n):
        for j in range(n // 2):
            row_factor[i] += matriz1[i][2 * j] * matriz1[i][2 * j + 1]

    # Calcular los factores de las columnas de matriz2
    for j in range(n):
        for i in range(n // 2):
            col_factor[j] += matriz2[2 * i][j] * matriz2[2 * i + 1][j]

    # Calcular la matriz resultado usando los factores escalados
    for i in range(n):
        for j in range(n):
            # Iniciar el valor de resultado con los factores de fila y columna
            resultado[i][j] = -row_factor[i] - col_factor[j]
            for k in range(n // 2):
                resultado[i][j] += (matriz1[i][2 * k] + matriz2[2 * k + 1][j]) * \
                                   (matriz1[i][2 * k + 1] + matriz2[2 * k][j])

    # Si n es impar, sumar el último producto correspondiente
    if n % 2 == 1:
        for i in range(n):
            for j in range(n):
                resultado[i][j] += matriz1[i][n - 1] * matriz2[n - 1][j]

    return resultado