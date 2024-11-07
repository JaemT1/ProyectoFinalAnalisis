import pandas as pd
import matplotlib.pyplot as plt
import os

# Definir la ruta base donde está el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas para la carpeta de datos y la carpeta de salida
data_folder = os.path.join(BASE_DIR, '../../../data/results/times/')
output_folder = os.path.join(BASE_DIR, '../images/')

# Crear el directorio de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Lista de tamaños para iterar
matrix_sizes = [2 ** i for i in range(1, 9)]  # Esto genera [2, 4, 8, ..., 256]

# Diccionario para almacenar los datos de tiempos por lenguaje y tamaño
data_all = {"Python": {}, "C++": {}}

# Iterar sobre cada tamaño de matriz y cargar los archivos correspondientes
for size in matrix_sizes:
    python_file = os.path.join(data_folder, f'resultadosPython_n{size}.csv')
    cpp_file = os.path.join(data_folder, f'resultadosC++_n{size}.csv')

    # Cargar datos de ambos archivos
    if os.path.exists(python_file):
        data_python = pd.read_csv(python_file)
        data_all["Python"][f"n{size}"] = data_python.groupby("Algoritmo")["Tiempo(s)"].mean()

    if os.path.exists(cpp_file):
        data_cpp = pd.read_csv(cpp_file)
        data_all["C++"][f"n{size}"] = data_cpp.groupby("Algoritmo")["Tiempo(s)"].mean()

# Convertir los datos en un DataFrame para facilidad de graficación
df_python = pd.DataFrame(data_all["Python"])
df_cpp = pd.DataFrame(data_all["C++"])

# Crear la figura y las subgráficas para comparar cada algoritmo
plt.figure(figsize=(12, 8))

# Iterar sobre cada algoritmo y graficar los tiempos para Python y C++
for i, algoritmo in enumerate(df_python.index):
    plt.plot(df_python.columns, df_python.loc[algoritmo], label=f"{algoritmo} (Python)", marker='o', linestyle='--')
    plt.plot(df_cpp.columns, df_cpp.loc[algoritmo], label=f"{algoritmo} (C++)", marker='o', linestyle='-')

# Personalizar el gráfico
plt.title("Comparación de tiempos de ejecución entre Python y C++ por tamaño de matriz")
plt.xlabel("Tamaño de matriz (n)")
plt.ylabel("Tiempo de ejecución promedio (s)")
plt.legend(title="Algoritmo y Lenguaje", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()

# Guardar el gráfico en un archivo
output_path = os.path.join(output_folder, 'comparacion_tiempos_python_cpp_multiples_tamanos.png')
plt.savefig(output_path)
plt.close()

print("Gráfico de comparación generado y guardado en la carpeta de imágenes.")
