import numpy as np

def multiplicar_winograd_original(matriz1, matriz2, n):
    # Convertir las matrices a arrays de numpy para aprovechar operaciones vectorizadas
    matriz1 = np.array(matriz1)
    matriz2 = np.array(matriz2)

    # Inicializar las matrices de resultado y los factores
    resultado = np.zeros((n, n))
    row_factor = np.zeros(n)
    col_factor = np.zeros(n)

    # Calcular los factores de fila (row_factor)
    for i in range(n):
        row_factor[i] = np.sum(matriz1[i, ::2] * matriz1[i, 1::2])

    # Calcular los factores de columna (col_factor)
    for j in range(n):
        col_factor[j] = np.sum(matriz2[::2, j] * matriz2[1::2, j])

    # Calcular el producto utilizando Winograd
    for i in range(n):
        for j in range(n):
            suma = -row_factor[i] - col_factor[j]
            # Calcular la contribución de los productos restantes
            suma += np.sum((matriz1[i, ::2] + matriz2[1::2, j]) * (matriz1[i, 1::2] + matriz2[::2, j]))
            resultado[i, j] = suma

    # Si n es impar, agregar el último producto
    if n % 2 == 1:
        resultado += matriz1[:, n-1, np.newaxis] * matriz2[n-1, :]

    return resultado.tolist()
