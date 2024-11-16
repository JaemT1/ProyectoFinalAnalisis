import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import io
from python.main import main  # Asegúrate de que el path es correcto

# Rutas a los archivos
executable_path_C = "cpp/PRoyectoFinal.exe"

# Lista para almacenar los mensajes de estado
status_messages = []

# Redirigir stdout para capturar mensajes en tiempo real
class StdoutRedirector(io.StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def write(self, message):
        if message != '\n':  # Evitar agregar nuevas líneas vacías
            self.text_widget.insert(tk.END, message)
            self.text_widget.yview(tk.END)  # Desplazar la vista al final
            self.text_widget.update_idletasks()  # Forzar actualización de la interfaz

def run_executable():
    try:
        result = subprocess.run([executable_path_C], capture_output=True, text=True)
        print(result.stdout)
        status_text.insert(tk.END, result.stdout)
        if result.stderr:
            print(result.stderr)
            return result.stderr
    except Exception as e:
        return f"Error ejecutando el archivo: {e}"
    return None

def run_processes(execute_button, status_label, status_text):
    # Deshabilitar el botón de ejecución
    execute_button.config(state="disabled")
    status_label.config(text="Calculando...", fg="blue")
    status_text.update()

    # Ejecutar el archivo C
    error_message = run_executable()

    # Ejecutar el proceso Python
    main_error = None
    try:
        main()
    except Exception as e:
        main_error = f"Error ejecutando el proceso de Python: {e}"

    # Volver a habilitar el botón y actualizar el estado
    execute_button.config(state="normal")
    status_label.config(text="Ejecución finalizada", fg="green")

    # Agregar los mensajes de error (si los hay) al text area
    all_errors = "\n".join(filter(None, [error_message, main_error]))
    if all_errors:
        messagebox.showerror("Errores durante la ejecución", all_errors)
    else:
        messagebox.showinfo("Finalizado", "La ejecución ha terminado.")

def update_status_text(status_text):
    # Cambiar el estado temporalmente a NORMAL para poder insertar texto
    status_text.config(state=tk.NORMAL)

    # Insertar los nuevos mensajes sin borrar los anteriores
    for message in status_messages:
        status_text.insert(tk.END, message + "\n")  # Insertar cada mensaje en el Text widget

    # Desplazar el contenido para mostrar siempre el último mensaje
    status_text.see(tk.END)  # Desplazar el scroll hacia el final

    # Volver a poner el estado del widget en DISABLED (solo lectura)
    status_text.config(state=tk.DISABLED)

# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Ejecutar Procesos")
root.geometry("500x400")

# Botón para ejecutar los procesos
execute_button = tk.Button(root, text="Ejecutar", command=lambda: run_processes(execute_button, status_label, status_text))
execute_button.pack(pady=10)

# Etiqueta para mostrar el estado
status_label = tk.Label(root, text="")
status_label.pack(pady=10)

# Crear Text widget para mostrar los mensajes de estado
status_text = tk.Text(root, height=10, width=50, wrap=tk.WORD, state="normal")
status_text.pack(pady=10)

# Redirigir stdout a un Text widget
redirector = StdoutRedirector(status_text)
sys.stdout = redirector

# Iniciar la interfaz gráfica
if __name__ == "__main__":
    root.mainloop()
