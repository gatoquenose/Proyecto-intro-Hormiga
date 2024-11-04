import random
from azucar import Azucar
from vino import Vino
from veneno import Veneno

class Hormiga:
    ACCIONES = ["arriba", "abajo", "izquierda", "derecha", "comer"]
    
    def __init__(self, posicion, salud=100, nivel_alcohol=0, puntos=0):
        self.posicion = posicion
        self.salud = salud
        self.nivel_alcohol = nivel_alcohol
        self.puntos = puntos
        self.nombre = "hormiga"
        self.imagen = "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/imagen hormiga.png"

    def decidir_movimiento(self, laberinto):
        # Verificar si la hormiga está viva
        if self.salud <= 0:
            return None

        # Encontrar el final
        posicion_final = None
        for i in range(laberinto.size):
            for j in range(laberinto.size):
                if laberinto.matriz_objetos[i][j] == 'final':
                    posicion_final = (i, j)
                    break
            if posicion_final:
                break

        # Verificar objeto en posición actual
        fila_actual, columna_actual = self.posicion
        objeto_actual = laberinto.matriz_objetos[fila_actual][columna_actual]
        if isinstance(objeto_actual, (Azucar, Vino)) and not isinstance(objeto_actual, Veneno):
            return "comer"

        # Evaluar solo movimientos válidos
        movimientos_validos = []
        for direccion in ["arriba", "abajo", "izquierda", "derecha"]:
            nueva_posicion = self.calcular_nueva_posicion(direccion)
            if self.es_movimiento_valido(nueva_posicion, laberinto):
                movimientos_validos.append((direccion, nueva_posicion))

        if not movimientos_validos:
            return None

        # Elegir mejor movimiento entre los válidos
        mejor_movimiento = None
        mejor_valor = float('-inf')

        for direccion, nueva_posicion in movimientos_validos:
            valor = 0
            # Valorar distancia al final
            if posicion_final:
                distancia_actual = abs(fila_actual - posicion_final[0]) + abs(columna_actual - posicion_final[1])
                distancia_nueva = abs(nueva_posicion[0] - posicion_final[0]) + abs(nueva_posicion[1] - posicion_final[1])
                if distancia_nueva < distancia_actual:
                    valor += 50

            # Valorar objetos
            objeto = laberinto.matriz_objetos[nueva_posicion[0]][nueva_posicion[1]]
            if objeto == 'final':
                valor += 1000
            elif isinstance(objeto, Azucar):
                valor += 30
            elif isinstance(objeto, Vino) and self.nivel_alcohol < 30:
                valor += 20
            elif isinstance(objeto, Veneno):
                valor -= 100

            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = direccion

        # Si no hay mejor movimiento, elegir uno aleatorio entre los válidos
        if not mejor_movimiento and movimientos_validos:
            mejor_movimiento = random.choice([m[0] for m in movimientos_validos])

        return mejor_movimiento

    def calcular_nueva_posicion(self, direccion):
        fila, columna = self.posicion
        nueva_fila, nueva_columna = fila, columna
        
        if direccion == "arriba":
            nueva_fila = fila - 1
        elif direccion == "abajo":
            nueva_fila = fila + 1
        elif direccion == "izquierda":
            nueva_columna = columna - 1
        elif direccion == "derecha":
            nueva_columna = columna + 1
        
        return (nueva_fila, nueva_columna)

    def es_movimiento_valido(self, posicion, laberinto):
        fila, columna = posicion
        
        # Verificar límites de la matriz
        if not (0 <= fila < laberinto.size and 0 <= columna < laberinto.size):
            return False
        
        # Verificar si hay obstáculos
        objeto = laberinto.matriz_objetos[fila][columna]
        return objeto != 'piedra'

    def interactuar_con_objeto(self, laberinto):
        fila, columna = self.posicion
        objeto = laberinto.matriz_objetos[fila][columna]
        
        if isinstance(objeto, Azucar):
            self.puntos += 10
            laberinto.matriz_objetos[fila][columna] = None
        elif isinstance(objeto, Vino):
            if self.nivel_alcohol < 30:
                self.modificar_nivel_alcohol(5)
                self.puntos += 5
                laberinto.matriz_objetos[fila][columna] = None
        elif isinstance(objeto, Veneno):
            self.modificar_salud(-20)
            self.puntos -= 5
            laberinto.matriz_objetos[fila][columna] = None

    def modificar_salud(self, cantidad):
        self.salud = max(0, min(100, self.salud + cantidad))

    def modificar_nivel_alcohol(self, cantidad):
        self.nivel_alcohol = max(0, min(50, self.nivel_alcohol + cantidad))
