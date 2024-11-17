import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

# Rutas a los archivos
IMAGENES_SCRIPT_PATH = "Imagenes.py"  # Ruta a imagenes.py
EJECUCION_SCRIPT_PATH = "ejecucion.py"  # Ruta a ejecucion.py

def open_imagenes():
    """Abrir el script de imágenes."""
    try:
        root.destroy()  # Cierra la ventana actual
        subprocess.run([sys.executable, IMAGENES_SCRIPT_PATH])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el script de imágenes: {e}")

def open_ejecucion():
    """Abrir el script de ejecución."""
    try:
        root.destroy()
        subprocess.run([sys.executable, EJECUCION_SCRIPT_PATH])
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el script de ejecución: {e}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Gestión de Algoritmos")
root.geometry("400x300")
root.resizable(False, False)

# Colores personalizados
BACKGROUND_COLOR = "#2C3E50"  # Fondo de la ventana
BUTTON_COLOR = "#1ABC9C"  # Color de los botones
BUTTON_HOVER_COLOR = "#16A085"  # Color de los botones al pasar el mouse
LABEL_COLOR = "#ECF0F1"  # Color del texto
BUTTON_TEXT_COLOR = "#FFFFFF"  # Color del texto de los botones

# Aplicar fondo a la ventana principal
root.configure(bg=BACKGROUND_COLOR)

# Función para manejar el hover en los botones
def on_enter(button):
    button.configure(bg=BUTTON_HOVER_COLOR)

def on_leave(button):
    button.configure(bg=BUTTON_COLOR)

# Etiqueta de bienvenida
welcome_label = tk.Label(
    root,
    text="Seleccione una acción:",
    bg=BACKGROUND_COLOR,
    fg=LABEL_COLOR,
    font=("Helvetica", 14)
)
welcome_label.pack(pady=20)

# Botón para ejecutar los procesos
execute_button = tk.Button(
    root,
    text="Ejecutar Algoritmos",
    bg=BUTTON_COLOR,
    fg=BUTTON_TEXT_COLOR,
    font=("Helvetica", 12),
    command=open_ejecucion,
    activebackground=BUTTON_HOVER_COLOR,
    activeforeground=BUTTON_TEXT_COLOR
)
execute_button.pack(pady=10, ipadx=10, ipady=5)

# Hover para botón de ejecutar proceso
execute_button.bind("<Enter>", lambda e: on_enter(execute_button))
execute_button.bind("<Leave>", lambda e: on_leave(execute_button))

# Botón para abrir el selector de gráficos
compare_button = tk.Button(
    root,
    text="Ver Gráficas",
    bg=BUTTON_COLOR,
    fg=BUTTON_TEXT_COLOR,
    font=("Helvetica", 12),
    command=open_imagenes,
    activebackground=BUTTON_HOVER_COLOR,
    activeforeground=BUTTON_TEXT_COLOR
)
compare_button.pack(pady=10, ipadx=10, ipady=5)

# Hover para botón de gráficas
compare_button.bind("<Enter>", lambda e: on_enter(compare_button))
compare_button.bind("<Leave>", lambda e: on_leave(compare_button))

# Etiqueta de estado (inicialmente vacía)
status_label = tk.Label(
    root,
    text="",
    bg=BACKGROUND_COLOR,
    fg=LABEL_COLOR,
    font=("Helvetica", 12)
)
status_label.pack(pady=20)

if __name__ == "__main__":
    root.mainloop()
