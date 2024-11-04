import matplotlib.pyplot as plt
import numpy as np

def inicializar_grafico():
    plt.ion()  # Habilita modo interactivo
    # Crear dos subplots: uno para puntajes y otro para tiempos
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Configura primer subplot (puntajes)
    ax1.set_xlabel('Generaciones')
    ax1.set_ylabel('Puntaje')
    ax1.set_title('Evolución del Puntaje')
    ax1.grid(True)
    
    # Configura segundo subplot (tiempos)
    ax2.set_xlabel('Generaciones')
    ax2.set_ylabel('Tiempo (s)')
    ax2.set_title('Tiempo por Generación')
    ax2.grid(True)
    
    return ax1, ax2

def actualizar_grafico(ax1, ax2, mejores_puntajes, puntajes_promedio, tiempos):
    ax1.clear()
    ax2.clear()
    
    # Grafica puntajes
    generaciones = range(1, len(mejores_puntajes) + 1)
    ax1.plot(generaciones, mejores_puntajes, 'b-', label='Mejor Puntaje')
    ax1.plot(generaciones, puntajes_promedio, 'g--', label='Puntaje Promedio')
    ax1.legend()
    ax1.grid(True)
    
    # Grafica tiempos
    ax2.bar(generaciones, tiempos, alpha=0.6)
    ax2.grid(True)
    
    # Muestra las estadísticas
    stats_text = f'Mejor Puntaje: {max(mejores_puntajes)}\n'
    stats_text += f'Tiempo Promedio: {np.mean(tiempos):.2f}s'
    plt.figtext(0.02, 0.02, stats_text, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.draw()
    plt.pause(0.01)

def finalizar_grafico():
    plt.ioff()
    plt.savefig('estadisticas_hormiga.png')  # Guarda el gráfico
    plt.show()
