import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import subprocess
import sys

# Ruta de la carpeta de imágenes y a InterfazPrincipal.py
images_path = "docs/diagrams/images"
gui_script_path = "InterfazPrincipal.py"  # Ruta a InterfazPrincipal.py
times_path = "data/results/times"
compare_script_path = "docs/diagrams/scripts/ComparingEqualsGraphics.py"

def get_available_sizes():
    available_sizes = []
    for size in ["n2", "n4", "n8", "n16", "n32", "n64", "n128", "n256"]:
        image_path = os.path.join(images_path, f"comparacion_tiempos_{size}.png")
        if os.path.exists(image_path):
            available_sizes.append(size)
    return available_sizes

def open_image(selected_size):
    image_path = os.path.join(images_path, f"comparacion_tiempos_{selected_size}.png")
    if not os.path.exists(image_path):
        messagebox.showerror("Error", f"No se encontró la imagen para {selected_size}")
        return

    image_window = tk.Toplevel()
    image_window.title(f"Comparación de tiempos {selected_size}")

    img = Image.open(image_path)
    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(image_window, image=img_tk)
    label.image = img_tk
    label.pack()

def check_and_enable_compare():
    if len(os.listdir(times_path)) == 16:
        compare_button.config(state="normal")
    else:
        compare_button.config(state="disabled")
    root.after(5000, check_and_enable_compare)

def back_to_gui():
    root.destroy()  # Cierra la ventana actual
    subprocess.run([sys.executable, gui_script_path])  # Ejecuta InterfazPrincipal.py

def run_compare_script():
    try:
        result = subprocess.run([sys.executable, compare_script_path], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
            messagebox.showerror("Error en el script", result.stderr)
        else:
            messagebox.showinfo("Éxito", "El script se ejecutó correctamente.")
            update_image_selector()  # Actualiza el selector de imágenes después de ejecutar el script
    except Exception as e:
        messagebox.showerror("Error ejecutando el script", str(e))

def show_image_selector():
    global size_menu, open_button, size_var, no_images_label

    available_sizes = get_available_sizes()

    # Remover widgets previos si existen
    if 'no_images_label' in globals() and no_images_label:
        no_images_label.pack_forget()
    if 'size_menu' in globals() and size_menu:
        size_menu.pack_forget()
    if 'open_button' in globals() and open_button:
        open_button.pack_forget()

    if not available_sizes:
        no_images_label = tk.Label(root, text="No hay imágenes disponibles")
        no_images_label.pack(pady=10)
    else:
        size_var = tk.StringVar(value=available_sizes[0])
        size_menu = tk.OptionMenu(root, size_var, *available_sizes)
        size_menu.pack(pady=10)

        open_button = tk.Button(root, text="Abrir Imagen", command=lambda: open_image(size_var.get()))
        open_button.pack(pady=10)

def update_image_selector():
    show_image_selector()  # Actualiza el selector después de generar nuevas imágenes

# Configurar la interfaz gráfica principal
root = tk.Tk()
root.title("Selector de Imágenes de Comparación de Tiempos")
root.geometry("300x200")

compare_button = tk.Button(root, text="Generar Gráficas", command=run_compare_script, state="disabled")
compare_button.pack(pady=10)

show_image_selector()

# Botón para volver a InterfazPrincipal.py
back_button = tk.Button(root, text="Volver", command=back_to_gui)
back_button.pack(side="bottom", pady=10)  # Colocar el botón "Volver" en la parte inferior

check_and_enable_compare()

if __name__ == "__main__":
    root.mainloop()
