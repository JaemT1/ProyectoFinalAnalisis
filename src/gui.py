import tkinter as tk
from tkinter import messagebox
import subprocess
from python.main import main  # Asegúrate de que el path es correcto

# Ruta al archivo ejecutable generado
executable_path_C = "PRoyectoFinal.exe"

def run_executable():
    try:
        # Ejecutar el archivo y capturar su salida y errores sin abrir ventanas
        result = subprocess.run([executable_path_C], capture_output=True, text=True)

        # Mostrar salida en consola y almacenar posibles errores
        print(result.stdout)
        if result.stderr:
            print(result.stderr)  # Mostrar errores en consola
            return result.stderr  # Devolver errores si existen
    except Exception as e:
        return f"Error ejecutando el archivo: {e}"
    return None

def run_processes():
    # Deshabilitar el botón y mostrar el mensaje "Calculando..."
    execute_button.config(state="disabled")
    status_label.config(text="Calculando...", fg="blue")
    root.update()  # Actualizar la GUI para mostrar el mensaje inmediatamente

    # Ejecutar el archivo C y capturar posibles errores
    error_message = run_executable()

    # Ejecutar main() y capturar posibles errores
    main_error = None
    try:
        main()
    except Exception as e:
        main_error = f"Error ejecutando el proceso de Python: {e}"

    # Restaurar el estado de la GUI cuando finalice la ejecución
    execute_button.config(state="normal")
    status_label.config(text="Ejecución finalizada", fg="green")

    # Mostrar mensaje de error único si hubo alguno
    all_errors = "\n".join(filter(None, [error_message, main_error]))  # Unir todos los errores
    if all_errors:
        messagebox.showerror("Errores durante la ejecución", all_errors)
    else:
        messagebox.showinfo("Finalizado", "La ejecución ha terminado.")

# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Ejecutar Procesos")
root.geometry("300x200")

# Botón para ejecutar los procesos
execute_button = tk.Button(root, text="Ejecutar", command=run_processes)
execute_button.pack(pady=20)

# Etiqueta de estado que mostrará "Calculando..." mientras se ejecutan los procesos
status_label = tk.Label(root, text="")
status_label.pack(pady=10)

if __name__ == "__main__":
    # Iniciar el loop de la interfaz
    root.mainloop()
