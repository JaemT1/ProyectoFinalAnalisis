def multiplicar_naiv_loop_unrolling_two(matriz1, matriz2, n):
    # Inicializamos el resultado con ceros
    resultado = [[0] * n for _ in range(n)]

    # Hacemos la multiplicación usando unrolling y optimizando el acceso a memoria
    for i in range(n):
        for j in range(n):
            suma = 0  # Variable temporal para la suma del producto
            # Bucle unrolling para procesar 2 elementos a la vez
            k = 0
            while k < n - 1:  # Procesamos pares de columnas
                m1_ik = matriz1[i][k]     # Acceso a la matriz1
                m1_i_k1 = matriz1[i][k+1] # Acceso a la matriz1
                m2_k_j = matriz2[k][j]    # Acceso a la matriz2
                m2_k1_j = matriz2[k+1][j] # Acceso a la matriz2

                suma += m1_ik * m2_k_j
                suma += m1_i_k1 * m2_k1_j
                k += 2

            # Si n es impar, tratamos el último elemento
            if k < n:  # Solo queda un elemento por procesar
                suma += matriz1[i][k] * matriz2[k][j]

            resultado[i][j] = suma

    return resultado
