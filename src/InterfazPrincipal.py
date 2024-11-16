import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
from python.main import main  # Asegúrate de que el path es correcto

# Rutas a los archivos
executable_path_C = "cpp/PRoyectoFinal.exe"
imagenes_script_path = "Imagenes.py"  # Ruta a imagenes.py

def run_executable():
    try:
        result = subprocess.run([executable_path_C], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
            return result.stderr
    except Exception as e:
        return f"Error ejecutando el archivo: {e}"
    return None

def run_processes():
    execute_button.config(state="disabled")
    status_label.config(text="Calculando...", fg="blue")
    root.update()

    error_message = run_executable()
    main_error = None
    try:
        main()
    except Exception as e:
        main_error = f"Error ejecutando el proceso de Python: {e}"

    execute_button.config(state="normal")
    status_label.config(text="Ejecución finalizada", fg="green")

    all_errors = "\n".join(filter(None, [error_message, main_error]))
    if all_errors:
        messagebox.showerror("Errores durante la ejecución", all_errors)
    else:
        messagebox.showinfo("Finalizado", "La ejecución ha terminado.")

def open_imagenes():
    root.destroy()  # Cierra la ventana actual
    subprocess.run([sys.executable, imagenes_script_path])  # Ejecuta imagenes.py

# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Ejecutar Procesos")
root.geometry("300x200")

# Botón para ejecutar los procesos
execute_button = tk.Button(root, text="Ejecutar", command=run_processes)
execute_button.pack(pady=10)

# Botón para abrir el selector de gráficos
compare_button = tk.Button(root, text="Graficas", command=open_imagenes, state="normal")
compare_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

if __name__ == "__main__":
    root.mainloop()
