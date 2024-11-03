class Azucar:
    def __init__(self, puntos):
        self.puntos = puntos
        self.nombre = "azucar"
        self.imagen = "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/azucar.png"

    def consumir(self, hormiga, casilla):
        hormiga.puntos += self.puntos
        casilla.remove(self)

    def mostrar_imagen(self):
        self.imagen.show()