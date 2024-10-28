import numpy as np
import os
import pandas as pd

from algorithms.NaviOnArray import multiplicar_naiv
from algorithms.NaivLoopUnrollingTwo import multiplicar_naiv_loop_unrolling_two
from algorithms.NaivLoopUnrollingFour import multiplicar_naiv_loop_unrolling_four
from algorithms.WinogradOriginal import multiplicar_winograd_original
from algorithms.WinogradScaled import multiplicar_winograd_escalado
from algorithms.SequentialBlock import multiplicar_sequential_block
from algorithms.ParallelBlock import multiplicar_parallel_block
from algorithms.IV3SequentialBlock import multiplicar_iv3_sequential_block
from algorithms.IV4ParallelBlock import multiplicar_iv4_parallel_block
from algorithms.IV5EnhancedParallelBlock import multiplicar_iv5_enhanced_parallel_block
from utils.ArchivoUtilidades import generar_matriz, guardar_matriz_en_txt, cargar_matriz_desde_txt, medir_tiempo

def main():
    n = 2  # Tamaño de la matriz, puedes cambiarlo
    matriz1 = generar_matriz(n)
    matriz2 = generar_matriz(n)

    # Guardar las matrices en un archivo .txt
    guardar_matriz_en_txt(matriz1, 'matriz1.txt')
    guardar_matriz_en_txt(matriz2, 'matriz2.txt')

    # Cargar las matrices desde el archivo .txt
    matriz1_cargada = cargar_matriz_desde_txt('matriz1.txt')
    matriz2_cargada = cargar_matriz_desde_txt('matriz2.txt')

    resultados = []

    # Medir tiempo para cada algoritmo
    resultados.append({
        'Tamano': n,
        'NaivOnArray': medir_tiempo(multiplicar_naiv, matriz1_cargada, matriz2_cargada, n),
        'NaivLoopUnrollingTwo': medir_tiempo(multiplicar_naiv_loop_unrolling_two, matriz1_cargada, matriz2_cargada, n),
        # 'NaivLoopUnrollingFour': medir_tiempo(multiplicar_naiv_loop_unrolling_four, matriz1_cargada, matriz2_cargada, n),
        'WinogradOriginal': medir_tiempo(multiplicar_winograd_original, matriz1_cargada, matriz2_cargada, n),
        'WinogradScaled': medir_tiempo(multiplicar_winograd_escalado, matriz1_cargada, matriz2_cargada, n),
        'III.3 Sequential Block': medir_tiempo(multiplicar_sequential_block, matriz1_cargada, matriz2_cargada, n),
        'III.4 Parallel Block': medir_tiempo(multiplicar_parallel_block, matriz1_cargada, matriz2_cargada, n, 64),
        'IV.3 Sequential block': medir_tiempo(multiplicar_iv3_sequential_block, matriz1_cargada, matriz2_cargada, n),
        'IV.4 Parallel Block': medir_tiempo(multiplicar_iv4_parallel_block, matriz1_cargada, matriz2_cargada, n, 64),
        'IV.5 Enhanced Parallel Block': medir_tiempo(multiplicar_iv5_enhanced_parallel_block, matriz1_cargada, matriz2_cargada, n)
    })

    # Guardar resultados en CSV
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv('resultados.csv', index=False)
    print("Resultados guardados en resultados.csv")

if __name__ == "__main__":
    main()
