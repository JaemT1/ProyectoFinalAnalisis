import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
from python.main import main  # Asegúrate de que el path es correcto

# Rutas a los archivos
imagenes_script_path = "Imagenes.py"  # Ruta a imagenes.py
ejecucion_script_path = "ejecucion.py"  # Ruta a imagenes.py

def open_imagenes():
    root.destroy()  # Cierra la ventana actual
    subprocess.run([sys.executable, imagenes_script_path])  # Ejecuta imagenes.py

def open_ejecucion():
    root.destroy()
    subprocess.run([sys.executable, ejecucion_script_path])

# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Ejecutar Procesos")
root.geometry("300x200")

# Botón para ejecutar los procesos
execute_button = tk.Button(root, text="Ejecutar", command=open_ejecucion, state="normal")
execute_button.pack(pady=10)

# Botón para abrir el selector de gráficos
compare_button = tk.Button(root, text="Graficas", command=open_imagenes, state="normal")
compare_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

if __name__ == "__main__":
    root.mainloop()
