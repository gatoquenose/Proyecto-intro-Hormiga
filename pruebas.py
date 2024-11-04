import tkinter as tk
from PIL import Image, ImageTk

# Crear la ventana principal
root = tk.Tk()
root.title("Visualizador de Imágenes")

# Lista de URLs de las imágenes
image_urls = [
    "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/veneno.png",
    "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/vino .png",
    "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/casilla sin nada.png"
]

# Función para cargar y mostrar una imagen
def mostrar_imagen(url):
    # Cargar la imagen desde la URL
    image = Image.open(url)
    image = ImageTk.PhotoImage(image)
    
    # Crear un widget Label para mostrar la imagen
    label = tk.Label(root, image=image)
    label.image = image  # Mantener una referencia a la imagen
    label.pack()

# Mostrar todas las imágenes
for url in image_urls:
    mostrar_imagen(url)

# Ejecutar el bucle principal de Tkinter
root.mainloop()