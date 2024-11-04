class Vino:
    def __init__(self, nivel_alcohol=50):
        self.nivel_alcohol = nivel_alcohol
        self.nombre = "vino"
        self.imagen = "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/vino .png"

    def consumir(self, hormiga, casilla):
        hormiga.modificar_nivel_alcohol(self.nivel_alcohol)
        casilla.remove(self)

    def mostrar_imagen(self):
        self.imagen.show()