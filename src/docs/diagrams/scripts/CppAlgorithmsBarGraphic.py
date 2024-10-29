import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos
data = pd.read_csv("Especificar Ruta Absoluta")

# Agrupar los tiempos de ejecución por algoritmo
avg_times = data.groupby("Algoritmo")["Tiempo(s)"].mean()

# Crear el diagrama de barras
plt.figure(figsize=(10, 6))
avg_times.plot(kind="bar", color="skyblue")
plt.title("Tiempo de ejecución promedio por algoritmo")
plt.xlabel("Algoritmo")
plt.ylabel("Tiempo (s)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Guardar el gráfico
plt.savefig("Especificar Ruta Absoluta")
plt.show()
