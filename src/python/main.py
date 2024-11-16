from gc import freeze
from multiprocessing.spawn import freeze_support

import numpy as np
import os
import pandas as pd

from src.python.algorithms.NaivOnArray import multiplicar_naiv
from src.python.algorithms.NaivLoopUnrollingTwo import multiplicar_naiv_loop_unrolling_two
from src.python.algorithms.NaivLoopUnrollingFour import multiplicar_naiv_loop_unrolling_four
from src.python.algorithms.WinogradOriginal import multiplicar_winograd_original
from src.python.algorithms.WinogradScaled import multiplicar_winograd_escalado
from src.python.algorithms.III3SequentialBlock import multiplicar_iii3_sequential_block
from src.python.algorithms.III4ParallelBlock import multiplicar_iii4_parallel_block
from src.python.algorithms.IV3SequentialBlock import multiplicar_iv3_sequential_block
from src.python.algorithms.IV4ParallelBlock import multiplicar_iv4_parallel_block
from src.python.algorithms.IV5EnhancedParallelBlock import multiplicar_iv5_enhanced_parallel_block
from src.python.utils.ArchivoUtilidades import generar_matriz, guardar_matriz_en_txt, cargar_matriz_desde_txt, medir_tiempo

# Definir la ruta base del directorio donde está main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    for i in range (1,9):
        # Ruta completa de las matrices utilizando BASE_DIR
        matrizA_path = os.path.join(BASE_DIR, f'../data/test_cases/matrizA{2**i}.txt')
        matrizB_path = os.path.join(BASE_DIR, f'../data/test_cases/matrizB{2**i}.txt')

        # Cargar las matrices desde el archivo .txt
        matriz1_cargada = cargar_matriz_desde_txt(matrizA_path)
        matriz2_cargada = cargar_matriz_desde_txt(matrizB_path)

        resultados = []

        # Determinar el tamaño de la matriz cargada
        n = len(matriz1_cargada)

        # Medir tiempo para cada algoritmo y almacenar resultados en formato deseado
        algoritmos = {
            'Naiv': multiplicar_naiv,
            'LoopUnrollingTwo': multiplicar_naiv_loop_unrolling_two,
            'LoopUnrollingFour': multiplicar_naiv_loop_unrolling_four,
            'WinogradOriginal': multiplicar_winograd_original,
            'WinogradScaled': multiplicar_winograd_escalado,
            'III_3_SequentialBlock': multiplicar_iii3_sequential_block,
            'III_4_ParallelBlock': lambda m1, m2, n: multiplicar_iii4_parallel_block(m1, m2, n, 64),
            'IV_3_SequentialBlock': multiplicar_iv3_sequential_block,
            'IV_4_ParallelBlock': lambda m1, m2, n: multiplicar_iv4_parallel_block(m1, m2, n, 64),
            'IV_5_EnhancedParallelBlock': multiplicar_iv5_enhanced_parallel_block
        }

        for nombre, funcion in algoritmos.items():
            tiempo, _ = medir_tiempo(funcion, matriz1_cargada, matriz2_cargada, n)
            resultados.append({
                'Algoritmo': nombre,
                'Tamaño': n,
                'Tiempo(s)': tiempo
            })

        # Definir la carpeta de resultados y el nombre del archivo en función del tamaño
        results_dir = os.path.join(BASE_DIR, '../data/results/times')
        os.makedirs(results_dir, exist_ok=True)

        # Definir el nombre del archivo según el tamaño de la matriz
        filename = f'resultadosPython_n{n}.csv'
        filepath = os.path.join(results_dir, filename)

        # Guardar resultados en CSV
        df_resultados = pd.DataFrame(resultados)
        df_resultados.to_csv(filepath, index=False)
        print(f"Ejecución de los algoritmos en Python para tamaño {2**i}*{2**i} completada\n")


if __name__ == "__main__":
    main()

