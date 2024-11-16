import pandas as pd
import matplotlib.pyplot as plt
import os

# Definir la ruta base donde está el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas para carpeta de datos y carpeta de salida
data_folder = os.path.join(BASE_DIR, '../../../data/results/times/')
output_folder = os.path.join(BASE_DIR, '../images/')

# Crear el directorio de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Lista de tamaños de matrices para iterar
matrix_sizes = [2 ** i for i in range(1, 9)]  # Esto genera [2, 4, 8, ..., 256]

# Diccionario para almacenar los datos de tiempos por tamaño de matriz
comparison_data = {}

# Iterar sobre cada tamaño de matriz y cargar los archivos correspondientes
for size in matrix_sizes:
    python_file = os.path.join(data_folder, f'resultadosPython_n{size}.csv')
    cpp_file = os.path.join(data_folder, f'resultadosC++_n{size}.csv')

    # Verificar si ambos archivos existen para el tamaño actual
    if os.path.exists(python_file) and os.path.exists(cpp_file):
        # Cargar datos y calcular el promedio de tiempos para cada algoritmo
        data_python = pd.read_csv(python_file)
        data_cpp = pd.read_csv(cpp_file)

        # Agrupar por algoritmo y calcular promedio para cada lenguaje
        avg_times_python = data_python.groupby("Algoritmo")["Tiempo(s)"].mean()
        avg_times_cpp = data_cpp.groupby("Algoritmo")["Tiempo(s)"].mean()

        # Agregar los datos al diccionario con el tamaño como clave
        comparison_data[f"n{size}"] = {
            "Python": avg_times_python,
            "C++": avg_times_cpp
        }

# Crear un gráfico para cada tamaño de matriz
for size, times in comparison_data.items():
    # Combinar los tiempos en un solo DataFrame para facilidad de graficación
    df = pd.DataFrame({"Python": times["Python"], "C++": times["C++"]})

    # Crear la figura y el gráfico de barras agrupadas
    plt.figure(figsize=(9, 7.2))  # Aumentar la altura de la figura
    ax = df.plot(kind="bar", color=["skyblue", "salmon"], width=0.8, ax=plt.gca())

    # Personalizar el gráfico
    plt.title(f"Comparación de tiempos de ejecución entre Python y C++ para tamaño de matriz {size}", pad=20)  # Añadir margen al título
    plt.xlabel("Algoritmo")
    plt.ylabel("Tiempo de ejecución promedio (s)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Lenguaje")
    plt.tight_layout()

    # Añadir los tiempos de ejecución como texto al lado de las barras, con un desplazamiento adicional en y
    for i, (alg, row) in enumerate(df.iterrows()):
        # Posiciones de las barras (Python y C++)
        x_python = i - 0.15
        x_cpp = i + 0.15

        # Ajustar el desplazamiento vertical
        y_offset = 0.01 * max(row["Python"], row["C++"])  # Ajuste dinámico según el valor de la barra

        # Formato de notación científica para valores muy pequeños
        time_python = f'{row["Python"]:.2e}' if row["Python"] < 0.01 else f'{row["Python"]:.2f}'
        time_cpp = f'{row["C++"]:.2e}' if row["C++"] < 0.01 else f'{row["C++"]:.2f}'

        # Añadir el texto con los tiempos sobre cada barra
        ax.text(x_python, row["Python"] + y_offset, time_python, ha='center', va='bottom', fontsize=6, color="blue", rotation=90)
        ax.text(x_cpp, row["C++"] + y_offset, time_cpp, ha='center', va='bottom', fontsize=6, color="red", rotation=90)

    # Guardar el gráfico en un archivo
    output_path = os.path.join(output_folder, f'comparacion_tiempos_{size}.png')
    plt.savefig(output_path)
    plt.close()

print("Gráficos de comparación generados y guardados en la carpeta de imágenes.")
