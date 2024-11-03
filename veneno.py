class Veneno:
    def __init__(self):
        self.nombre = "veneno"
        self.imagen = "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/veneno.png"

    def consumir(self, hormiga, casilla):
        hormiga.salud = 0
        casilla.remove(self)

    def mostrar_imagen(self):
        self.imagen.show()