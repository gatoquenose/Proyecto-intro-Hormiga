import random
from item import Hormiga
from Laberinto import Laberinto
class AlgoritmoGenetico:
    def __init__(self, laberinto, pop_size=10, generations=100, sequence_length=20, mutation_rate=0.1):
        self.laberinto = laberinto
        self.pop_size = pop_size
        self.generations = generations
        self.sequence_length = sequence_length
        self.mutation_rate = mutation_rate
        self.poblacion = self.generar_poblacion()

    # Generar una población inicial de secuencias de movimientos
    def generar_poblacion(self):
        return [
            [random.choice(Hormiga.ACCIONES) for _ in range(self.sequence_length)]
            for _ in range(self.pop_size)
        ]

    # Calcular la función de evaluación (fitness)
    def fitness(self, individuo):
        hormiga = Hormiga(posicion_inicial=(0, 0))
        score = 0
        for accion in individuo:
            hormiga.mover(accion, self.laberinto)
            hormiga.ajustar_nivel_alcohol()  # Ajustamos el nivel de alcohol en cada paso
            if self.laberinto.es_objetivo(hormiga.posicion):
                score += 10  # Puntos extra por llegar a la meta
                break
        # Considerar el puntaje, la distancia al objetivo y el nivel de alcohol
        distancia = self.laberinto.distancia_objetivo(hormiga.posicion)
        fitness_value = score - distancia - abs(hormiga.nivel_alcohol)
        return fitness_value

    # Selección de los mejores padres
    def seleccionar_padres(self, fitness_scores):
        return random.choices(self.poblacion, weights=fitness_scores, k=self.pop_size // 2)

    # Cruzamiento entre dos individuos
    def cruzar(self, padre1, padre2):
        punto_cruce = random.randint(0, len(padre1) - 1)
        hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
        hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
        return hijo1, hijo2

    # Mutación de un individuo
    def mutar(self, individuo):
        return [
            random.choice(Hormiga.ACCIONES) if random.random() < self.mutation_rate else gene
            for gene in individuo
        ]

    # Método para ejecutar el algoritmo genético
    def ejecutar(self):
        for generacion in range(self.generations):
            fitness_scores = [self.fitness(ind) for ind in self.poblacion]

            # Selección de los padres
            padres = self.seleccionar_padres(fitness_scores)
            
            # Crear nueva población con cruzamiento y mutación
            nueva_poblacion = []
            for i in range(0, len(padres), 2):
                hijo1, hijo2 = self.cruzar(padres[i], padres[(i + 1) % len(padres)])
                nueva_poblacion.extend([self.mutar(hijo1), self.mutar(hijo2)])

            self.poblacion = nueva_poblacion

            # Verificar si se encontró la solución óptima
            if max(fitness_scores) >= 10:
                print(f'Solución encontrada en la generación {generacion}')
                break

        # Retornar el mejor individuo encontrado
        mejor_individuo = self.poblacion[fitness_scores.index(max(fitness_scores))]
        return mejor_individuo