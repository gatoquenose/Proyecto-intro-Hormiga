import tkinter as tk
from PIL import Image, ImageTk
import random
from item import Item, crear_item

class Laberinto:
    def __init__(self, ventana, size):
        self.ventana = ventana
        self.size = size
        self.matriz = [[None for _ in range(size)] for _ in range(size)]
        self.items = ['azucar', 'vino', 'veneno', 'roca']
        self.posiciones_botones = {}  # Diccionario para guardar las posiciones de los botones
        self.posicion_hormiga = None  # Guardar la posición actual de la hormiga

    def cargar_imagenes(self):
        rutas_imagenes = {
            'azucar': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/azucar.png",
            'vino': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/vino .png",
            'veneno': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/veneno.png",
            'roca': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/piedra.png",
            'hormiga': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/imagen hormiga.png",
            'casilla': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/casilla sin nada.png"
        }
        for item, ruta in rutas_imagenes.items():
            self.imagenes[item] = ImageTk.PhotoImage(Image.open(ruta).resize((80, 80)))

    def crear_laberinto(self):
        for i in range(self.size):
            for j in range(self.size):
                if random.random() < 0.2:  # 20% de probabilidad de colocar un ítem
                    tipo_item = random.choice(self.items)
                    self.matriz[i][j] = crear_item(tipo_item)
                else:
                    self.matriz[i][j] = crear_item('casilla')

    def actualizar_estado(self, fila, columna):
        item = self.laberinto.matriz[fila][columna].tipo
        if item == 'azucar':
            print("La hormiga ha encontrado azúcar.")
        elif item == 'vino':
            print("La hormiga ha encontrado vino.")
        elif item == 'veneno':
            print("La hormiga ha encontrado veneno.")
        elif item == 'roca':
            print("La hormiga ha encontrado una roca.")
        # Vaciar la casilla después de que la hormiga pase por ella
        self.laberinto.matriz[fila][columna] = crear_item('casilla', self.laberinto.imagenes)
        self.posiciones_botones[(fila, columna)].config(image=self.laberinto.imagenes['casilla'])

class Mapa_e_inicio:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ANCHO_VENTANA = 550
        self.ALTO_VENTANA = 600
        self.configurar_ventana_principal()
        self.mostrar_pantalla_inicio()
        self.imagenes = []
        self.contadores_izquierda = {}
        self.posicion_hormiga = None
        self.laberinto = None

    def configurar_ventana_principal(self):
        self.ventana.geometry(f"{self.ANCHO_VENTANA}x{self.ALTO_VENTANA}")
        self.ventana.title("Simulación Hormiga")
        for i in range(3):
            self.ventana.grid_rowconfigure(i, weight=1)
            self.ventana.grid_columnconfigure(i, weight=1)

    def mostrar_pantalla_inicio(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

        label = tk.Label(self.ventana, text="Simulación Hormiga", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        button_width = 10
        button_height = 3

        boton_tamaño = tk.Button(self.ventana, text="INICIO", font=("Arial", 16), command=self.abrir_tamaño, bg="blue", fg="white", width=button_width, height=button_height)
        boton_tamaño.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        boton_estadisticas = tk.Button(self.ventana, text="Estadísticas", font=("Arial", 16), command=self.estadisticas, bg="blue", fg="white", width=button_width, height=button_height)
        boton_estadisticas.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    def abrir_tamaño(self):
        self.ventana.withdraw()
        ventana_tamaño = tk.Toplevel()
        ventana_tamaño.geometry(f"{self.ANCHO_VENTANA}x{self.ALTO_VENTANA}")
        ventana_tamaño.title("Elegir Tamaño")

        for i in range(5):
            ventana_tamaño.grid_rowconfigure(i, weight=1)
            ventana_tamaño.grid_columnconfigure(i, weight=1)

        label = tk.Label(ventana_tamaño, text="Elegir Tamaño", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        button_width = 10
        button_height = 3

        boton_4x4 = tk.Button(ventana_tamaño, text="4x4", font=("Arial", 16), command=lambda: self.elegir_tamaño(4, ventana_tamaño), bg="blue", fg="white", width=button_width, height=button_height)
        boton_4x4.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        boton_5x5 = tk.Button(ventana_tamaño, text="5x5", font=("Arial", 16), command=lambda: self.elegir_tamaño(5, ventana_tamaño), bg="blue", fg="white", width=button_width, height=button_height)
        boton_5x5.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        boton_6x6 = tk.Button(ventana_tamaño, text="6x6", font=("Arial", 16), command=lambda: self.elegir_tamaño(6, ventana_tamaño), bg="blue", fg="white", width=button_width, height=button_height)
        boton_6x6.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

        boton_volver = tk.Button(ventana_tamaño, text="Volver", font=("Arial", 16), command=lambda: self.volver_a_principal(ventana_tamaño), bg="red", fg="white", width=button_width, height=button_height)
        boton_volver.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

    def estadisticas(self):
        self.ventana.withdraw()
        ventana_estadisticas = tk.Toplevel()
        ventana_estadisticas.geometry(f"{self.ANCHO_VENTANA}x{self.ALTO_VENTANA}")
        ventana_estadisticas.title("Estadísticas")

        label = tk.Label(ventana_estadisticas, text="Estadísticas", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        boton_volver = tk.Button(ventana_estadisticas, text="Volver", font=("Arial", 16), command=lambda: self.volver_a_principal(ventana_estadisticas), bg="red", fg="white", width=10, height=3)
        boton_volver.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

    def volver_a_principal(self, ventana):
        ventana.destroy()
        self.ventana.deiconify()
        self.mostrar_pantalla_inicio()

    def elegir_tamaño(self, size, ventana):
        ventana.destroy()
        self.ventana.deiconify()
        self.crear_matriz(size)

    def crear_matriz(self, size):
        for widget in self.ventana.winfo_children():
            widget.destroy()

        self.botones_izquierda = []
        self.botones_matriz = []
        self.contadores_izquierda = {0: 2, 1: 3, 2: 4, 3: 7, 4: 1, 5: 1, 6: 100}
        
        self.laberinto = Laberinto(self.ventana, size)
        self.laberinto.cargar_imagenes()
        self.laberinto.crear_laberinto()

        for i in range(7):  # Cambiar a 7 para incluir el nuevo botón
            boton = tk.Button(self.ventana, image=self.laberinto.imagenes['casilla'], bg="gray", fg="white", width=80, height=80)
            boton.configure(command=lambda i=i: self.boton_click_izquierda(i))
            boton.grid(row=i, column=0, sticky="nsew")
            self.botones_izquierda.append(boton)

        # Botón adicional "Inicio" al lado del último botón de la izquierda
        boton_inicio = tk.Button(self.ventana, text="Inicio", font=("Arial", 12), bg="green", fg="white", command=self.mover_hormiga_arriba, width=10, height=2)
        boton_inicio.grid(row=6, column=1, sticky="nsew")

        # Botón adicional "Mover Abajo" al lado del botón "Inicio"
        boton_mover_abajo = tk.Button(self.ventana, text="Mover Abajo", font=("Arial", 12), bg="yellow", fg="black", command=self.mover_hormiga_abajo, width=10, height=2)
        boton_mover_abajo.grid(row=7, column=1, sticky="nsew")

        boton_volver = tk.Button(self.ventana, text="Volver", font=("Arial", 12), bg="red", fg="white", command=self.mostrar_pantalla_inicio, width=10, height=2)
        boton_volver.grid(row=8, column=0, columnspan=size+1, sticky="nsew")

        for i in range(size):
            for j in range(size):
                item = self.laberinto.matriz[i][j]
                boton = tk.Button(self.ventana, image=item.imagen, bg="white", fg="black", width=80, height=80)
                boton.grid(row=i, column=j+1, sticky="nsew")
                self.botones_matriz.append(boton)
                self.posiciones_botones[(i, j)] = boton  # Guardar la posición del botón en el diccionario

    def boton_click_izquierda(self, i):
        if self.contadores_izquierda[i] > 0:
            self.contadores_izquierda[i] -= 1
            imagen = self.laberinto.imagenes['hormiga']
            for boton in self.botones_matriz:  # Aplicar la imagen a los botones de la matriz
                if boton.cget("image") == str(self.laberinto.imagenes['casilla']):  # Aplicar la imagen solo si el botón no tiene una imagen
                    boton.config(image=imagen, compound="center", width=80, height=80)
                    self.posicion_hormiga = (self.botones_matriz.index(boton) // self.laberinto.size, self.botones_matriz.index(boton) % self.laberinto.size)
                    break
        contador = self.contadores_izquierda[i]
        boton = self.botones_izquierda[i]
        boton.config(image=self.laberinto.imagenes['casilla'], compound="center", width=80, height=80)

    def actualizar_estado(self, fila, columna):
        # Implementar la lógica para actualizar el estado de las casillas
        item = self.laberinto.matriz[fila][columna].tipo
        if item == 'azucar':
            print("La hormiga ha encontrado azúcar.")
        elif item == 'vino':
            print("La hormiga ha encontrado vino.")
        elif item == 'veneno':
            print("La hormiga ha encontrado veneno.")
        elif item == 'roca':
            print("La hormiga ha encontrado una roca.")
        # Vaciar la casilla después de que la hormiga pase por ella
        self.laberinto.matriz[fila][columna] = Item('casilla', self.laberinto.imagenes['casilla'])
        self.posiciones_botones[(fila, columna)].config(image=self.laberinto.imagenes['casilla'])

if __name__ == "__main__":
    ventana = tk.Tk()
    app = Mapa_e_inicio(ventana)
    app.mostrar_pantalla_inicio()
    ventana.mainloop()