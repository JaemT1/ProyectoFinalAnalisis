import multiprocessing

def calcular_bloque(matriz1, matriz2, n, ii, jj, block_size):
    bloque_resultado = []
    for i in range(ii, min(ii + block_size, n)):
        for j in range(jj, min(jj + block_size, n)):
            suma = 0
            for k in range(n):
                suma += matriz1[i][k] * matriz2[k][j]
            bloque_resultado.append((i, j, suma))  # Almacenar el resultado del bloque
    return bloque_resultado

def multiplicar_iii4_parallel_block(matriz1, matriz2, n, block_size=2):
    resultado = multiprocessing.Array('d', n * n)  # Crear un array unidimensional compartido

    # Crear un grupo de procesos para los bloques
    with multiprocessing.Pool() as pool:
        tareas = []
        for ii in range(0, n, block_size):
            for jj in range(0, n, block_size):
                # Programar cada bloque como una tarea asincrónica
                tareas.append(pool.apply_async(calcular_bloque, args=(matriz1, matriz2, n, ii, jj, block_size)))

        # Recoger los resultados de todas las tareas
        for tarea in tareas:
            for i, j, suma in tarea.get():
                resultado[i * n + j] += suma  # Actualizar el resultado en el índice correspondiente

    # Convertir el array unidimensional en una matriz 2D para el resultado final
    resultado_final = [[resultado[i * n + j] for j in range(n)] for i in range(n)]
    return resultado_final