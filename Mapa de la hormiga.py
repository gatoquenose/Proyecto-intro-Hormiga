import tkinter as tk
from PIL import Image, ImageTk

class Mapa_e_inicio:
    def __init__(self, root):
        self.root = root
        self.ANCHO_VENTANA = 400
        self.ALTO_VENTANA = 400
        self.configurar_ventana_principal()
        self.mostrar_pantalla_inicio()
        self.cargar_imagenes()

    def configurar_ventana_principal(self):
        self.root.geometry(f"{self.ANCHO_VENTANA}x{self.ALTO_VENTANA}")
        self.root.title("Simulación Hormiga")
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def mostrar_pantalla_inicio(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        label = tk.Label(self.root, text="Simulación Hormiga", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        button_width = 10
        button_height = 3

        boton_tamanio = tk.Button(self.root, text="INICIO", font=("Arial", 16), command=self.abrir_tamanio, bg="blue", fg="white", width=button_width, height=button_height)
        boton_tamanio.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        boton_estadisticas = tk.Button(self.root, text="Estadísticas", font=("Arial", 16), command=self.estadisticas, bg="blue", fg="white", width=button_width, height=button_height)
        boton_estadisticas.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    def abrir_tamanio(self):
        self.root.withdraw()  # Oculta la ventana principal
        ventana_tamanio = tk.Toplevel()
        ventana_tamanio.geometry(f"{self.ANCHO_VENTANA}x{self.ALTO_VENTANA}")
        ventana_tamanio.title("Elegir Tamaño")

        for i in range(5):
            ventana_tamanio.grid_rowconfigure(i, weight=1)
            ventana_tamanio.grid_columnconfigure(i, weight=1)

        label = tk.Label(ventana_tamanio, text="Elegir Tamaño", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        button_width = 10
        button_height = 3

        boton_4x4 = tk.Button(ventana_tamanio, text="4x4", font=("Arial", 16), command=lambda: self.elegir_tamanio(4, ventana_tamanio), bg="blue", fg="white", width=button_width, height=button_height)
        boton_4x4.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        boton_5x5 = tk.Button(ventana_tamanio, text="5x5", font=("Arial", 16), command=lambda: self.elegir_tamanio(5, ventana_tamanio), bg="blue", fg="white", width=button_width, height=button_height)
        boton_5x5.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

        boton_6x6 = tk.Button(ventana_tamanio, text="6x6", font=("Arial", 16), command=lambda: self.elegir_tamanio(6, ventana_tamanio), bg="blue", fg="white", width=button_width, height=button_height)
        boton_6x6.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")

        boton_volver = tk.Button(ventana_tamanio, text="Volver", font=("Arial", 16), command=lambda: self.volver_a_principal(ventana_tamanio), bg="red", fg="white", width=button_width, height=button_height)
        boton_volver.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

    def volver_a_principal(self, ventana):
        ventana.destroy()  # Cierra la ventana secundaria
        self.root.deiconify()  # Vuelve a mostrar la ventana principal
        self.mostrar_pantalla_inicio()  # Llama a la pantalla de inicio

    def elegir_tamanio(self, size, ventana):
        ventana.destroy()
        self.root.deiconify()
        self.crear_matriz(size)

    def crear_matriz(self, size):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Crear botones laterales con imágenes
        self.imagenes = []
        for i in range(6):
            imagen = Image.open(f"imagen_{i+1}.png")  # Asegúrate de que estos archivos existan
            imagen = imagen.resize((40, 40), Image.LANCZOS)  # Ajusta el tamaño según sea necesario
            self.imagenes.append(ImageTk.PhotoImage(imagen))

        for i in range(6):
            boton = tk.Button(self.root, image=self.imagenes[i], compound=tk.LEFT, text=f"Btn {i+1}", font=("Arial", 12), bg="gray", fg="white")
            boton.grid(row=i, column=0, sticky="nsew")

        boton_volver = tk.Button(self.root, text="Volver", font=("Arial", 12), bg="red", fg="white", command=self.mostrar_pantalla_inicio)
        boton_volver.grid(row=6, column=0, sticky="nsew")

        self.root.grid_rowconfigure(6, weight=0)  # Configura la fila 6 para que tenga un peso menor
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)  # Configura las filas de los botones de la izquierda para que tengan un peso mayor

        for i in range(size):
            for j in range(size):
                boton = tk.Button(self.root, text=f"{i},{j}", font=("Arial", 12), bg="white", fg="black")
                boton.grid(row=i, column=j+1, padx=2, pady=2, sticky="nsew")

        # Configure grid weights
        for i in range(max(size, 7)):  # 7 because we have 6 buttons + 1 "Volver" button
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(size + 1):  # +1 for the left column
            self.root.grid_columnconfigure(i, weight=1)

    def estadisticas(self):
        self.root.withdraw()  # Oculta la ventana principal
        ventana_estadisticas = tk.Toplevel()
        ventana_estadisticas.geometry(f"{self.ANCHO_VENTANA}x{self.ALTO_VENTANA}")
        ventana_estadisticas.title("Estadísticas")

        for i in range(5):
            ventana_estadisticas.grid_rowconfigure(i, weight=1)
            ventana_estadisticas.grid_columnconfigure(i, weight=1)

        label = tk.Label(ventana_estadisticas, text="Estadísticas", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        boton_volver = tk.Button(ventana_estadisticas, text="Volver", font=("Arial", 16), command=lambda: self.volver_a_principal(ventana_estadisticas), bg="red", fg="white", width=10, height=3)
        boton_volver.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

root = tk.Tk()
app = Mapa_e_inicio(root)
root.mainloop()
