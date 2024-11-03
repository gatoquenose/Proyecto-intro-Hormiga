import random
from Algoritmo import AlgoritmoGenetico

class Hormiga:
    def __init__(self, posicion, salud=100, nivel_alcohol=0, puntos=0):
        self.posicion = posicion
        self.salud = salud
        self.nivel_alcohol = nivel_alcohol
        self.puntos = puntos
        self.secuencias = []
        self.nombre = "hormiga"
        self.imagen = "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/hormiga.png"

    def mover(self, direccion, laberinto):
        fila, columna = laberinto.posicion_hormiga
        if direccion == "arriba":
            nueva_fila, nueva_columna = fila - 1, columna
        elif direccion == "abajo":
            nueva_fila, nueva_columna = fila + 1, columna
        elif direccion == "izquierda":
            nueva_fila, nueva_columna = fila, columna - 1
        elif direccion == "derecha":
            nueva_fila, nueva_columna = fila, columna + 1
        else:
            return

    def comer(self, item):
        if item == "azucar":
            self.puntos += 10
        elif item == "veneno":
            self.modificar_salud(-20)
            self.puntos -= 5
        elif item == "alcohol":
            self.modificar_nivel_alcohol(5)
            self.puntos += 5

    def modificar_salud(self, cantidad):
        self.salud = max(0, min(100, self.salud + cantidad))

    def modificar_nivel_alcohol(self, cantidad):
        self.nivel_alcohol = max(0, min(50, self.nivel_alcohol + cantidad))

    def algoritmo_genetico(self):
        secuencia = AlgoritmoGenetico()
        self.secuencias.append(secuencia)
        self.secuencias = sorted(self.secuencias, key=lambda x: self.puntos, reverse=True)[:3]
        self.guardar_secuencias()

    def guardar_secuencias(self):
        with open("mejores_secuencias.txt", "w") as file:
            for secuencia in self.secuencias:
                file.write(f"{secuencia}\n")

    def obtener_posicion(self):
        return self.posicion

    def mostrar_imagen(self):
        self.imagen.show()
