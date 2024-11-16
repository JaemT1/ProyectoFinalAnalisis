import numpy as np

def multiplicar_winograd_escalado(matriz1, matriz2, n):
    # Convertir las matrices a arrays de numpy para aprovechar operaciones vectorizadas
    matriz1 = np.array(matriz1, dtype=int)  # Asegurarse de que matriz1 sea de tipo entero
    matriz2 = np.array(matriz2, dtype=int)  # Asegurarse de que matriz2 sea de tipo entero

    # Inicializar las matrices de resultados y los factores
    resultado = np.zeros((n, n), dtype=int)  # Asegurarse de que el resultado sea de tipo entero
    row_factor = np.zeros(n, dtype=int)      # Usar enteros para los factores de fila
    col_factor = np.zeros(n, dtype=int)      # Usar enteros para los factores de columna

    # Precomputar los factores de las filas de matriz1
    for i in range(n):
        row_factor[i] = np.sum(matriz1[i, ::2] * matriz1[i, 1::2])

    # Precomputar los factores de las columnas de matriz2
    for j in range(n):
        col_factor[j] = np.sum(matriz2[::2, j] * matriz2[1::2, j])

    # Calcular el producto utilizando los factores escalados
    for i in range(n):
        for j in range(n):
            suma = -row_factor[i] - col_factor[j]
            # Calcular la contribución de los productos restantes
            suma += np.sum((matriz1[i, ::2] + matriz2[1::2, j]) * (matriz1[i, 1::2] + matriz2[::2, j]))
            resultado[i, j] = suma

    # Si n es impar, agregar el último elemento
    if n % 2 == 1:
        resultado += matriz1[:, n-1, np.newaxis] * matriz2[n-1, :]

    # Convertir el resultado a una lista de listas de enteros
    return resultado.tolist()
