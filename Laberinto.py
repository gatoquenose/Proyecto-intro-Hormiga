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
        self.configurar_ventana_principal()
        self.mostrar_pantalla_inicio()
        self.imagenes = []
        self.contadores_izquierda = {}
        self.botones_izquierda = {}
        self.posicion_hormiga = (0, 0)
        self.hormiga = Hormiga(self.posicion_hormiga)
        self.vino = Vino(nivel_alcohol = 0)
        self.veneno = Veneno()

    def configurar_ventana_principal(self):
        self.ventana.geometry(f"{self.ANCHO_VENTANA}x{self.ALTO_VENTANA}")
        self.ventana.title("Simulación Hormiga")
        for i in range(3):
            self.ventana.grid_rowconfigure(i, weight=0)
            self.ventana.grid_columnconfigure(i, weight=0)

    def items(self):
        items = {
            "azucar": "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/azucar.png",
            "final": "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/Final.png",
            "hormiga": "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/hormiga.png",
            "piedra": "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/piedra.png",
            "veneno": "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/veneno.png",
            "vino": "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/vino .png",
            "casilla": "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/casilla sin nada.png"
        }
        
        def crear_item(tipo , imagenes):
            return Item(tipo, imagenes[tipo])

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
        self.crear_matriz(size)

    def crear_matriz(self, size):
        for widget in self.ventana.winfo_children():
            widget.destroy()

        self.botones = []
        self.contadores_izquierda = {0: 2, 1: 1, 2: 1, 3: 3, 4: 2, 5: 2, 6: 36}
        self.botones_izquierda = {}

        rutas_imagenes = [
            "azucar",
            "final",
            "hormiga",
            "piedra",
            "veneno",
            "vino",
            "casilla"
        ]

        self.imagenes = [ImageTk.PhotoImage(Image.open(ruta).resize((80, 80))) for ruta in rutas_imagenes]
    
        for i in range(7):
            boton = tk.Button(self.ventana, image=self.imagenes[i], bg="gray", fg="white", width=80, height=80)
            boton.configure(command=lambda i=i: self.boton_click_izquierda(i))
            boton.grid(row=i, column=0, sticky="nsew")
            self.botones.append(boton)

        boton_inicio = tk.Button(self.ventana, text="Inicio", font=("Arial", 12), bg="green", fg="white", width=10, height=2)
        boton_inicio.grid(row=6, column=1, sticky="nsew")

        boton_volver = tk.Button(self.ventana, text="Volver", font=("Arial", 12), bg="red", fg="white", command=self.mostrar_pantalla_inicio, width=10, height=2)
        boton_volver.grid(row=7, column=0, columnspan=size+1, sticky="nsew")

        for i in range(size):
            for j in range(size):
                boton = tk.Button(self.ventana, bg="white", fg="black", width=5, height=2)
                boton.grid(row=i, column=j+1, sticky="nsew")
                self.botones.append(boton)

    def boton_click_izquierda(self, i):
        if self.contadores_izquierda[i] > 0:
            self.contadores_izquierda[i] -= 1
            imagen = self.imagenes[i]
            for boton in self.botones:
                if boton.cget("image") == "": 
                    boton.config(image=imagen, compound="center", width=80, height=80)
                    if i == 2:  # Si es la imagen de la hormiga, guardar su posición
                        self.posicion_hormiga = (self.botones_matriz.index(boton) // self.elegir_tamaño, self.botones_matriz.index(boton) % self.elegir_tamaño)
                        self.hormiga = Hormiga(self.posicion_hormiga)
                    break
        contador = self.contadores_izquierda[i]
        boton = self.botones_izquierda[i]
        boton.config(image=imagen, compound="center", width=80, height=80)
                    
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