import tkinter as tk
from PIL import Image, ImageTk
from hormiga import Hormiga
from vino import Vino
from veneno import Veneno

class Laberinto:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ANCHO_VENTANA = 550
        self.ALTO_VENTANA = 600
        self.MIN_SIZE = 3
        self.MAX_SIZE = 10
        self.matriz = None  # Matriz que almacenará los objetos
        self.items = {
            'azucar': {'cantidad': 2, 'clase': None},
            'vino': {'cantidad': 2, 'clase': Vino},
            'veneno': {'cantidad': 2, 'clase': Veneno},
            'piedra': {'cantidad': 3, 'clase': None},
            'hormiga': {'cantidad': 1, 'clase': Hormiga},
            'final': {'cantidad': 1, 'clase': None},
            'vacio': {'cantidad': None, 'clase': None}  # La cantidad será calculada según el tamaño
        }
        self.configurar_ventana_principal()
        self.cargar_imagenes()
        self.mostrar_pantalla_inicio()

    def cargar_imagenes(self):
        self.imagenes = {}
        rutas = {
            'azucar': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/azucar.png",
            'vino': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/vino .png",
            'veneno': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/veneno.png",
            'piedra': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/piedra.png",
            'hormiga': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/hormiga.png",
            'final': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/Final.png",
            'vacio': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/casilla sin nada.png"
        }
        for nombre, ruta in rutas.items():
            self.imagenes[nombre] = ImageTk.PhotoImage(Image.open(ruta).resize((80, 80)))

    def crear_laberinto(self, size):
        if not self.MIN_SIZE <= size <= self.MAX_SIZE:
            raise ValueError(f"El tamaño debe estar entre {self.MIN_SIZE} y {self.MAX_SIZE}")
        
        # Inicializar matriz vacía
        self.matriz = [[None for _ in range(size)] for _ in range(size)]
        self.size = size
        
        # Calcular casillas vacías disponibles
        total_casillas = size * size
        casillas_ocupadas = sum(item['cantidad'] for item in self.items.values() if item['cantidad'])
        self.items['vacio']['cantidad'] = total_casillas - casillas_ocupadas
        
        # Crear interfaz para colocar ítems
        self.crear_matriz_visual(size)

    def crear_matriz_visual(self, size):
        for widget in self.ventana.winfo_children():
            widget.destroy()

        # Crear panel de ítems disponibles
        for i, (item_nombre, item_data) in enumerate(self.items.items()):
            if item_data['cantidad']:  # Solo mostrar ítems con cantidad > 0
                frame = tk.Frame(self.ventana)
                frame.grid(row=i, column=0, padx=5, pady=5)
                
                boton = tk.Button(frame, 
                                image=self.imagenes[item_nombre],
                                command=lambda n=item_nombre: self.seleccionar_item(n))
                boton.pack(side=tk.LEFT)
                
                contador = tk.Label(frame, text=str(item_data['cantidad']))
                contador.pack(side=tk.LEFT)

        # Crear matriz de botones
        self.botones_matriz = []
        for i in range(size):
            fila_botones = []
            for j in range(size):
                boton = tk.Button(self.ventana,
                                image=self.imagenes['vacio'],
                                width=80, height=80,
                                command=lambda r=i, c=j: self.colocar_item(r, c))
                boton.grid(row=i, column=j+1, padx=2, pady=2)
                fila_botones.append(boton)
            self.botones_matriz.append(fila_botones)

    def seleccionar_item(self, item_nombre):
        if self.items[item_nombre]['cantidad'] > 0:
            self.item_seleccionado = item_nombre

    def colocar_item(self, fila, columna):
        if hasattr(self, 'item_seleccionado') and self.matriz[fila][columna] is None:
            item_data = self.items[self.item_seleccionado]
            
            # Crear instancia del objeto si tiene una clase asociada
            if item_data['clase']:
                if self.item_seleccionado == 'hormiga':
                    self.matriz[fila][columna] = item_data['clase']((fila, columna))
                elif self.item_seleccionado == 'vino':
                    self.matriz[fila][columna] = item_data['clase'](nivel_alcohol=0)
                else:
                    self.matriz[fila][columna] = item_data['clase']()
            else:
                self.matriz[fila][columna] = self.item_seleccionado

            # Actualizar visual
            self.botones_matriz[fila][columna].config(image=self.imagenes[self.item_seleccionado])
            
            # Actualizar contador
            item_data['cantidad'] -= 1
            self.actualizar_contadores()

    def actualizar_estado(self, posicion_hormiga):
        """Actualiza el estado del laberinto según el movimiento de la hormiga"""
        fila, columna = posicion_hormiga
        
        # Actualizar visualización
        for i in range(self.size):
            for j in range(self.size):
                item = self.matriz[i][j]
                if item:
                    # Determinar qué imagen mostrar basado en el tipo de objeto
                    imagen = None
                    if isinstance(item, Hormiga):
                        imagen = 'hormiga'
                    elif isinstance(item, Vino):
                        imagen = 'vino'
                    elif isinstance(item, Veneno):
                        imagen = 'veneno'
                    elif isinstance(item, str):
                        imagen = item
                    
                    if imagen:
                        self.botones_matriz[i][j].config(image=self.imagenes[imagen])
                else:
                    self.botones_matriz[i][j].config(image=self.imagenes['vacio'])

    def configurar_ventana_principal(self):
        self.ventana.geometry(f"{self.ANCHO_VENTANA}x{self.ALTO_VENTANA}")
        self.ventana.title("Simulación Hormiga")
        for i in range(3):
            self.ventana.grid_rowconfigure(i, weight=0)
            self.ventana.grid_columnconfigure(i, weight=0)

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
            ventana_tamaño.grid_rowconfigure(i, weight=0)
            ventana_tamaño.grid_columnconfigure(i, weight=0)

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

    def volver_a_principal(self, ventana):
        ventana.destroy()
        self.ventana.deiconify()
        self.mostrar_pantalla_inicio()

    def elegir_tamaño(self, size, ventana):
        ventana.destroy()
        self.ventana.deiconify()
        self.crear_laberinto(size)

    def estadisticas(self):
        self.ventana.withdraw()
        ventana_estadisticas = tk.Toplevel()
        ventana_estadisticas.geometry(f"{self.ANCHO_VENTANA}x{self.ALTO_VENTANA}")
        ventana_estadisticas.title("Estadísticas")

        label = tk.Label(ventana_estadisticas, text="Estadísticas", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        boton_volver = tk.Button(ventana_estadisticas, text="Volver", font=("Arial", 16), command=lambda: self.volver_a_principal(ventana_estadisticas), bg="red", fg="white", width=10, height=3)
        boton_volver.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

if __name__ == "__main__":
    ventana = tk.Tk()
    app = Laberinto(ventana)
    app.mostrar_pantalla_inicio()
    ventana.mainloop()