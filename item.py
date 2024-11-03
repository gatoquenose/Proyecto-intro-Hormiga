from PIL import Image, ImageTk
from vino import Vino
from veneno import Veneno
from azucar import Azucar
from hormiga import Hormiga

class Item:
    def __init__(self, tipo, ruta_imagen):
        self.tipo = tipo
        self.imagen = ImageTk.PhotoImage(Image.open(ruta_imagen).resize((80, 80)))
        self.veneno = Veneno()
        self.vino = Vino()


# Diccionario para almacenar las rutas de las imágenes
rutas_imagenes = {
    'azucar': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/azucar.png",
    'vino': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/vino .png",
    'veneno': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/veneno.png",
    'roca': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/piedra.png",
    'hormiga': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/imagen hormiga.png",
    'casilla': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/casilla sin nada.png"
}

# Función para crear un objeto Item con su imagen
def crear_item(tipo , imagenes):
    return Item(tipo, imagenes[tipo])