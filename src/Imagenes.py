import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import subprocess
import sys

# Ruta de la carpeta de imágenes y scripts
images_path = "docs/diagrams/images"
gui_script_path = "InterfazPrincipal.py"
times_path = "data/results/times"
compare_script_path = "docs/diagrams/scripts/ComparingEqualsGraphics.py"

# Colores personalizados
BG_COLOR = "#2C3E50"  # Fondo
FG_COLOR = "#ECF0F1"  # Texto
BUTTON_COLOR = "#1ABC9C"  # Botones
BUTTON_HOVER_COLOR = "#16A085"  # Botón al pasar el mouse

def get_available_sizes():
    """Obtiene los tamaños disponibles con imágenes generadas."""
    available_sizes = []
    for size in ["n2", "n4", "n8", "n16", "n32", "n64", "n128", "n256"]:
        image_path = os.path.join(images_path, f"comparacion_tiempos_{size}.png")
        if os.path.exists(image_path):
            available_sizes.append(size)
    return available_sizes

def open_image(selected_size):
    """Abre una imagen en una ventana nueva."""
    image_path = os.path.join(images_path, f"comparacion_tiempos_{selected_size}.png")
    if not os.path.exists(image_path):
        messagebox.showerror("Error", f"No se encontró la imagen para {selected_size}")
        return

    image_window = tk.Toplevel()
    image_window.title(f"Comparación de tiempos {selected_size}")
    image_window.configure(bg=BG_COLOR)

    img = Image.open(image_path)
    img_tk = ImageTk.PhotoImage(img)

    label = tk.Label(image_window, image=img_tk, bg=BG_COLOR)
    label.image = img_tk
    label.pack(pady=20)

def check_and_enable_compare():
    """Habilita o deshabilita el botón para generar gráficas."""
    if len(os.listdir(times_path)) == 16:
        compare_button.config(state="normal")
    else:
        compare_button.config(state="disabled")
    root.after(5000, check_and_enable_compare)

def back_to_gui():
    """Vuelve a la interfaz principal."""
    root.destroy()
    subprocess.run([sys.executable, gui_script_path])

def run_compare_script():
    """Ejecuta el script para generar gráficas."""
    try:
        result = subprocess.run([sys.executable, compare_script_path], capture_output=True, text=True)
        if result.stderr:
            messagebox.showerror("Error en el script", result.stderr)
        else:
            messagebox.showinfo("Éxito", "El script se ejecutó correctamente.")
            update_image_selector()
    except Exception as e:
        messagebox.showerror("Error ejecutando el script", str(e))

def show_image_selector():
    """Muestra el selector de tamaños de imágenes disponibles."""
    global size_menu, open_button, size_var, no_images_label

    available_sizes = get_available_sizes()

    # Limpiar widgets previos
    if 'no_images_label' in globals() and no_images_label:
        no_images_label.pack_forget()
    if 'size_menu' in globals() and size_menu:
        size_menu.pack_forget()
    if 'open_button' in globals() and open_button:
        open_button.pack_forget()

    if not available_sizes:
        no_images_label = tk.Label(root, text="No hay imágenes disponibles", bg=BG_COLOR, fg=FG_COLOR)
        no_images_label.pack(pady=10)
    else:
        size_var = tk.StringVar(value=available_sizes[0])
        size_menu = tk.OptionMenu(root, size_var, *available_sizes)
        size_menu.config(bg=BUTTON_COLOR, fg=FG_COLOR, font=("Helvetica", 12))
        size_menu.pack(pady=10)

        open_button = tk.Button(
            root,
            text="Abrir Imagen",
            bg=BUTTON_COLOR,
            fg=FG_COLOR,
            font=("Helvetica", 12),
            command=lambda: open_image(size_var.get())
        )
        open_button.pack(pady=10)

def update_image_selector():
    """Actualiza el selector de imágenes después de generar nuevas gráficas."""
    show_image_selector()

# Configuración de la interfaz gráfica principal
root = tk.Tk()
root.title("Selector de Imágenes de Comparación de Tiempos")
root.geometry("400x300")
root.configure(bg=BG_COLOR)

# Título
title_label = tk.Label(
    root,
    text="Comparación de Tiempos",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Helvetica", 16, "bold")
)
title_label.pack(pady=20)

# Botón para generar gráficas
compare_button = tk.Button(
    root,
    text="Generar Gráficas",
    bg=BUTTON_COLOR,
    fg=FG_COLOR,
    font=("Helvetica", 12),
    command=run_compare_script,
    state="disabled"
)
compare_button.pack(pady=10)

# Mostrar selector de imágenes
show_image_selector()

# Botón para volver a la interfaz principal
back_button = tk.Button(
    root,
    text="Volver",
    bg=BUTTON_COLOR,
    fg=FG_COLOR,
    font=("Helvetica", 12),
    command=back_to_gui
)
back_button.pack(side="bottom", pady=10)

# Comprobar continuamente si habilitar el botón de comparar
check_and_enable_compare()

# Iniciar la interfaz gráfica
if __name__ == "__main__":
    root.mainloop()
