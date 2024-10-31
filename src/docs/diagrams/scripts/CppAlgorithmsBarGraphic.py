import pandas as pd
import matplotlib.pyplot as plt
import os

# Definir la ruta base donde está el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta para la carpeta de datos
data_folder = os.path.join(BASE_DIR, '../../../data/results/times/')
output_folder = os.path.join(BASE_DIR, '../images/')

# Obtener todos los archivos CSV en la carpeta de datos
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

# Crear el directorio de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Iterar sobre cada archivo CSV
for csv_file in csv_files:
    data_path = os.path.join(data_folder, csv_file)

    # Cargar los datos
    data = pd.read_csv(data_path)

    # Agrupar los tiempos de ejecución por algoritmo
    avg_times = data.groupby("Algoritmo")["Tiempo(s)"].mean()

    # Crear una figura para graficar
    plt.figure(figsize=(10, 6))

    # Graficar los tiempos promedios
    avg_times.plot(kind="bar", color="skyblue")

    # Personalizar el gráfico
    plt.title(f"Tiempo de ejecución promedio por algoritmo - {csv_file[:-4]}")
    plt.xlabel("Algoritmo")
    plt.ylabel("Tiempo (s)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Guardar el gráfico en un archivo
    output_path = os.path.join(output_folder, f'resultados_{csv_file[:-4]}.png')
    plt.savefig(output_path)
    plt.close()  # Cerrar la figura actual para liberar memoria

print("Gráficos generados y guardados en la carpeta de imágenes.")