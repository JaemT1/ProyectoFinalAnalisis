import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import io
import threading
from python.main import main  # Asegúrate de que el path es correcto

# Rutas a los archivos
EXECUTABLE_PATH_C = "cpp/PRoyectoFinal.exe"
GUI_SCRIPT_PATH = "InterfazPrincipal.py"

# Redirigir stdout para capturar mensajes en tiempo real
class StdoutRedirector(io.StringIO):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def write(self, message):
        if message.strip():  # Evitar líneas vacías
            self.text_widget.insert(tk.END, message + "\n")
            self.text_widget.yview(tk.END)  # Desplazar la vista al final
            self.text_widget.update_idletasks()

def run_executable():
    """Ejecuta el archivo ejecutable C++."""
    try:
        result = subprocess.run([EXECUTABLE_PATH_C], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
            return result.stderr
    except Exception as e:
        return (f"Error ejecutando los algoritmos de C++: {e}")
    return None

def run_processes(execute_button, status_label, status_text, back_button):
    """Ejecuta los procesos en un hilo separado."""
    execute_button.config(state="disabled")
    back_button.config(state="disabled")
    status_label.config(text="Calculando...", fg="#3498DB")
    status_text.update()

    def run():
        # Ejecutar el archivo C
        error_message = run_executable()

        # Ejecutar el proceso Python
        main_error = None
        try:
            main()
        except Exception as e:
            main_error = f"Error ejecutando el proceso de Python: {e}"

        # Habilitar botones nuevamente
        execute_button.config(state="normal")
        back_button.config(state="normal")
        status_label.config(text="Ejecución finalizada", fg="#2ECC71")

        # Mostrar errores, si los hay
        all_errors = "\n".join(filter(None, [error_message, main_error]))
        if all_errors:
            messagebox.showerror("Errores durante la ejecución", all_errors)
        else:
            messagebox.showinfo("Finalizado", "La ejecución ha terminado.")

    threading.Thread(target=run).start()

def back_to_gui():
    """Vuelve a la interfaz principal."""
    root.destroy()
    subprocess.run([sys.executable, GUI_SCRIPT_PATH])

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Gestión de Algoritmos")
root.geometry("600x500")
root.configure(bg="#2C3E50")  # Fondo oscuro

# Colores personalizados
BG_COLOR = "#2C3E50"  # Fondo principal
FG_COLOR = "#ECF0F1"  # Texto principal
BUTTON_COLOR = "#1ABC9C"  # Botones
BUTTON_HOVER_COLOR = "#16A085"  # Botón al pasar mouse
TEXT_BG_COLOR = "#34495E"  # Fondo del widget de texto
TEXT_FG_COLOR = "#ECF0F1"  # Texto del widget de texto

# Estilo de etiquetas
# Estilo de etiquetas
def create_label(parent, text, font=("Helvetica", 12), **kwargs):
    return tk.Label(parent, text=text, bg=BG_COLOR, fg=FG_COLOR, font=font, **kwargs)


# Hover en botones
def on_enter(button):
    button.configure(bg=BUTTON_HOVER_COLOR)

def on_leave(button):
    button.configure(bg=BUTTON_COLOR)

# Etiqueta de título
title_label = create_label(root, "Gestión de Algoritmos", font=("Helvetica", 16, "bold"))
title_label.pack(pady=20)

# Botón para ejecutar los procesos
execute_button = tk.Button(
    root,
    text="Ejecutar Algoritmos",
    bg=BUTTON_COLOR,
    fg=FG_COLOR,
    font=("Helvetica", 12),
    command=lambda: run_processes(execute_button, status_label, status_text, back_button),
    activebackground=BUTTON_HOVER_COLOR,
    activeforeground=FG_COLOR
)
execute_button.pack(pady=10, ipadx=10, ipady=5)
execute_button.bind("<Enter>", lambda e: on_enter(execute_button))
execute_button.bind("<Leave>", lambda e: on_leave(execute_button))

# Etiqueta para mostrar el estado
status_label = create_label(root, "")
status_label.pack(pady=10)

# Widget de texto para mostrar los mensajes
status_text = tk.Text(
    root,
    height=12,
    width=70,
    wrap=tk.WORD,
    bg=TEXT_BG_COLOR,
    fg=TEXT_FG_COLOR,
    font=("Courier", 10),
    state="normal"
)
status_text.pack(pady=10, padx=20)

# Botón para volver a la interfaz principal
back_button = tk.Button(
    root,
    text="Volver",
    bg=BUTTON_COLOR,
    fg=FG_COLOR,
    font=("Helvetica", 12),
    command=back_to_gui,
    activebackground=BUTTON_HOVER_COLOR,
    activeforeground=FG_COLOR
)
back_button.pack(side="bottom", pady=20, ipadx=10, ipady=5)
back_button.bind("<Enter>", lambda e: on_enter(back_button))
back_button.bind("<Leave>", lambda e: on_leave(back_button))

# Redirigir stdout a un Text widget
redirector = StdoutRedirector(status_text)
sys.stdout = redirector

# Iniciar la interfaz gráfica
if __name__ == "__main__":
    root.mainloop()
