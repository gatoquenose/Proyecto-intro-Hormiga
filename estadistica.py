import matplotlib.pyplot as plt

# Inicializa el gráfico
def inicializar_grafico():
    plt.ion()  # Habilitar modo interactivo
    plt.figure()
    plt.xlabel('Generaciones')
    plt.ylabel('Puntaje')
    plt.title('Evolución del Puntaje a lo Largo de las Generaciones')

# Actualiza el gráfico con los nuevos puntajes
def actualizar_grafico(puntajes):
    plt.plot(puntajes)
    plt.draw()
    plt.pause(0.01)  # Pausa para actualizar el gráfico

# Finaliza el gráfico
def finalizar_grafico():
    plt.ioff()  # Deshabilitar modo interactivo
    plt.show()  # Mostrar el gráfico final