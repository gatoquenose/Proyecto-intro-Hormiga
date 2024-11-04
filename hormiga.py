import random
import numpy as np
from azucar import Azucar
from vino import Vino
from veneno import Veneno

class AlgoritmoGenetico:
    def __init__(self, tam_poblacion=50, tam_secuencia=20):
        self.tam_poblacion = tam_poblacion
        self.tam_secuencia = tam_secuencia
        self.acciones = ["arriba", "abajo", "izquierda", "derecha", "comer"]
        self.poblacion = self.inicializar_poblacion()
        self.mejor_ruta = None
        self.mejor_puntuacion = float('-inf')
        self.intentos = 0
        self.max_intentos = 100  # Máximo número de intentos para encontrar una mejor ruta

    def inicializar_poblacion(self):
        # Crear población inicial aleatoria
        return [[random.choice(self.acciones) for _ in range(self.tam_secuencia)] 
                for _ in range(self.tam_poblacion)]

    def evaluar_ruta(self, secuencia, hormiga, laberinto):
        # Copia los estados iniciales
        pos_inicial = hormiga.posicion.copy()
        salud_inicial = hormiga.salud
        alcohol_inicial = hormiga.nivel_alcohol
        puntos_inicial = hormiga.puntos
        
        # Simular la ruta
        pos_actual = pos_inicial.copy()
        pasos = 0
        llego_final = False
        
        for accion in secuencia:
            pasos += 1
            
            if accion == "comer":
                # Simular comer
                objeto = laberinto.obtener_objeto(pos_actual[0], pos_actual[1])
                if objeto:
                    hormiga.interactuar_con_objeto(laberinto)
            else:
                # Simular movimiento
                nueva_pos = self.calcular_nueva_posicion(pos_actual, accion)
                if self.es_movimiento_valido(nueva_pos, laberinto):
                    pos_actual = nueva_pos
                    
                    # Verificar si llegó al final
                    objeto = laberinto.obtener_objeto(pos_actual[0], pos_actual[1])
                    if objeto == 'final':
                        llego_final = True
                        break

        # Calcular puntuación considerando múltiples factores
        puntuacion = 0
        if llego_final:
            puntuacion += 1000  # Bonus por llegar al final
            puntuacion += hormiga.puntos * 10  # Puntos recolectados
            puntuacion -= hormiga.nivel_alcohol * 5  # Penalización por alcohol
            puntuacion -= pasos * 2  # Penalización por número de pasos
        
        # Restaurar estados iniciales
        hormiga.posicion = pos_inicial
        hormiga.salud = salud_inicial
        hormiga.nivel_alcohol = alcohol_inicial
        hormiga.puntos = puntos_inicial
        
        return puntuacion, llego_final, pasos

    def encontrar_mejor_ruta(self, hormiga, laberinto):
        while self.intentos < self.max_intentos:
            self.intentos += 1
            
            # Evolucionar población
            for _ in range(10):  # Número de generaciones por intento
                self.evolucionar(hormiga, laberinto)
            
            # Evaluar mejor secuencia actual
            mejor_secuencia = self.mejor_secuencia
            puntuacion, llego_final, pasos = self.evaluar_ruta(mejor_secuencia, hormiga, laberinto)
            
            if puntuacion > self.mejor_puntuacion:
                self.mejor_puntuacion = puntuacion
                self.mejor_ruta = mejor_secuencia
                print(f"Nueva mejor ruta encontrada:")
                print(f"Puntuación: {puntuacion}")
                print(f"Pasos: {pasos}")
                print(f"Llegó al final: {llego_final}")
                
            if llego_final and hormiga.nivel_alcohol == 0:
                break
        
        return self.mejor_ruta

    def calcular_nueva_posicion(self, pos_actual, accion):
        fila, columna = pos_actual
        if accion == "arriba":
            return (fila - 1, columna)
        elif accion == "abajo":
            return (fila + 1, columna)
        elif accion == "izquierda":
            return (fila, columna - 1)
        elif accion == "derecha":
            return (fila, columna + 1)
        return pos_actual

    def es_movimiento_valido(self, pos, laberinto):
        fila, columna = pos
        if 0 <= fila < laberinto.size and 0 <= columna < laberinto.size:
            objeto = laberinto.obtener_objeto(fila, columna)
            return objeto != 'piedra'
        return False

    def seleccion(self, fitness_scores):
        # Selección por torneo
        seleccionados = []
        for _ in range(self.tam_poblacion):
            participantes = random.sample(range(self.tam_poblacion), 3)
            ganador = max(participantes, key=lambda x: fitness_scores[x])
            seleccionados.append(self.poblacion[ganador])
        return seleccionados

    def cruzamiento(self, padre1, padre2):
        # Cruzamiento en un punto
        punto = random.randint(0, self.tam_secuencia - 1)
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2

    def mutacion(self, secuencia, prob_mutacion=0.1):
        # Mutación por cambio aleatorio
        for i in range(len(secuencia)):
            if random.random() < prob_mutacion:
                secuencia[i] = random.choice(self.acciones)
        return secuencia

    def evolucionar(self, hormiga, laberinto, generaciones=50):
        for gen in range(generaciones):
            # Calcular fitness para toda la población
            fitness_scores = [self.calcular_fitness(seq, hormiga, laberinto) 
                            for seq in self.poblacion]
            
            # Actualizar mejor secuencia
            mejor_idx = np.argmax(fitness_scores)
            if fitness_scores[mejor_idx] > self.mejor_fitness:
                self.mejor_fitness = fitness_scores[mejor_idx]
                self.mejor_secuencia = self.poblacion[mejor_idx]

            # Selección
            seleccionados = self.seleccion(fitness_scores)
            
            # Nueva población
            nueva_poblacion = []
            while len(nueva_poblacion) < self.tam_poblacion:
                padre1, padre2 = random.sample(seleccionados, 2)
                hijo1, hijo2 = self.cruzamiento(padre1, padre2)
                nueva_poblacion.extend([
                    self.mutacion(hijo1),
                    self.mutacion(hijo2)
                ])
            
            self.poblacion = nueva_poblacion[:self.tam_poblacion]

class Hormiga:
    ACCIONES = ["arriba", "abajo", "izquierda", "derecha", "comer"]
    
    def __init__(self, posicion, salud=100, nivel_alcohol=0, puntos=0):
        self.posicion = posicion
        self.salud = salud
        self.nivel_alcohol = nivel_alcohol
        self.puntos = puntos
        self.nombre = "hormiga"
        self.imagen = "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/imagen hormiga.png"
        self.algoritmo_genetico = AlgoritmoGenetico()
        self.secuencia_actual = []
        self.indice_secuencia = 0

    def decidir_movimiento(self, laberinto):
        if self.salud <= 0:
            return None

        # Si no hay secuencia actual o se acabó, evolucionar nueva secuencia
        if not self.secuencia_actual or self.indice_secuencia >= len(self.secuencia_actual):
            self.algoritmo_genetico.evolucionar(self, laberinto)
            self.secuencia_actual = self.algoritmo_genetico.mejor_secuencia
            self.indice_secuencia = 0

        # Obtener siguiente movimiento de la secuencia
        movimiento = self.secuencia_actual[self.indice_secuencia]
        self.indice_secuencia += 1

        # Validar el movimiento
        if movimiento != "comer":
            nueva_pos = self.calcular_nueva_posicion(movimiento)
            if not self.es_movimiento_valido(nueva_pos, laberinto):
                return random.choice(["arriba", "abajo", "izquierda", "derecha"])

        return movimiento

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
        objeto = laberinto.obtener_objeto(fila, columna)
        
        if isinstance(objeto, Veneno):
            self.salud = 0
            laberinto.matriz_objetos[fila][columna] = None
            return "veneno"
        elif isinstance(objeto, Azucar):
            self.puntos += 200
            laberinto.matriz_objetos[fila][columna] = None
            # Actualizar etiquetas
            laberinto.label_puntuacion.config(text=f"Puntuación: {self.puntos}")
            return "azucar"
        elif isinstance(objeto, Vino):
            self.nivel_alcohol += 50
            laberinto.matriz_objetos[fila][columna] = None
            # Actualizar etiquetas
            laberinto.label_alcohol.config(text=f"Nivel de alcohol: {self.nivel_alcohol}")
            return "vino"
        return None

    def modificar_salud(self, cantidad):
        self.salud = max(0, min(100, self.salud + cantidad))

    def modificar_nivel_alcohol(self, cantidad):
        self.nivel_alcohol = max(0, min(50, self.nivel_alcohol + cantidad))

    def generar_secuencia_movimientos(self):
        acciones = ["arriba", "abajo", "izquierda", "derecha", "comer"]
        return [random.choice(acciones) for _ in range(50)]  # Secuencia de 50 movimientos
