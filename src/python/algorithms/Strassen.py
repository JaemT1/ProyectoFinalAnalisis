from typing import List

# Definimos el tipo para las matrices
Matrix = List[List[int]]

# Función para sumar dos matrices
def add(A: Matrix, B: Matrix) -> Matrix:
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

# Función para restar dos matrices
def subtract(A: Matrix, B: Matrix) -> Matrix:
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C

# Algoritmo de Strassen
def strassen(A: Matrix, B: Matrix) -> Matrix:
    n = len(A)
    if n == 1:
        # Caso base: multiplicación de un solo elemento
        return [[A[0][0] * B[0][0]]]

    # Tamaño de las submatrices
    newSize = n // 2

    # Inicializar submatrices
    A11, A12, A21, A22 = [[0] * newSize for _ in range(newSize)], [[0] * newSize for _ in range(newSize)], [[0] * newSize for _ in range(newSize)], [[0] * newSize for _ in range(newSize)]
    B11, B12, B21, B22 = [[0] * newSize for _ in range(newSize)], [[0] * newSize for _ in range(newSize)], [[0] * newSize for _ in range(newSize)], [[0] * newSize for _ in range(newSize)]

    # Dividir matrices A y B en submatrices
    for i in range(newSize):
        for j in range(newSize):
            A11[i][j] = A[i][j]
            A12[i][j] = A[i][j + newSize]
            A21[i][j] = A[i + newSize][j]
            A22[i][j] = A[i + newSize][j + newSize]

            B11[i][j] = B[i][j]
            B12[i][j] = B[i][j + newSize]
            B21[i][j] = B[i + newSize][j]
            B22[i][j] = B[i + newSize][j + newSize]

    # Calcular los productos intermedios de Strassen
    M1 = strassen(add(A11, A22), add(B11, B22))
    M2 = strassen(add(A21, A22), B11)
    M3 = strassen(A11, subtract(B12, B22))
    M4 = strassen(A22, subtract(B21, B11))
    M5 = strassen(add(A11, A12), B22)
    M6 = strassen(subtract(A21, A11), add(B11, B12))
    M7 = strassen(subtract(A12, A22), add(B21, B22))

    # Combinar los productos intermedios para obtener las submatrices de C
    C11 = add(subtract(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(subtract(add(M1, M3), M2), M6)

    # Combinar submatrices en la matriz resultado
    C = [[0] * n for _ in range(n)]
    for i in range(newSize):
        for j in range(newSize):
            C[i][j] = C11[i][j]
            C[i][j + newSize] = C12[i][j]
            C[i + newSize][j] = C21[i][j]
            C[i + newSize][j + newSize] = C22[i][j]

    return C