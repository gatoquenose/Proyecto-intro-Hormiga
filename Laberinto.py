import tkinter as tk
from PIL import Image, ImageTk
from hormiga import Hormiga
from vino import Vino
from veneno import Veneno
from item import Item
from azucar import Azucar
import os
import tkinter.messagebox as messagebox
import random

class Laberinto:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ANCHO_VENTANA = 600
        self.ALTO_VENTANA = 600
        self.matriz_objetos = None  # Matriz para almacenar los objetos
        self.size = None
        self.configurar_ventana_principal()
        self.imagenes = {}
        self.cargar_imagenes()
        self.objetos_disponibles = {
            'azucar': {'clase': Azucar, 'cantidad': 2, 'params': {'puntos': 10}},
            'vino': {'clase': Vino, 'cantidad': 2, 'params': {'nivel_alcohol': 5}},
            'veneno': {'clase': Veneno, 'cantidad': 2, 'params': {}},
            'hormiga': {'clase': Hormiga, 'cantidad': 1, 'params': {'posicion': (0,0)}},
            'piedra': {'clase': None, 'cantidad': 3, 'params': {}},
            'final': {'clase': None, 'cantidad': 1, 'params': {}},
            'vacio': {'clase': None, 'cantidad': None, 'params': {}}
        }

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
            "hormiga": "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/imagen hormiga.png",
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

    def cargar_imagenes(self):
        # Definir nombres y rutas de las imágenes con rutas absolutas y nombres corregidos
        nombres_imagenes = {
            'azucar': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/azucar.png",
            'final': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/Final.png",
            'hormiga': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/imagen hormiga.png",
            'piedra': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/piedra.png",
            'veneno': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/veneno.png",
            'vino': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/vino .png",
            'vacio': "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/casilla sin nada.png"
        }
        
        # Verificar si los archivos existen antes de cargarlos
        for nombre, ruta in nombres_imagenes.items():
            try:
                # Imprimir la ruta para debugging
                print(f"Intentando cargar: {ruta}")
                
                # Verificar si el archivo existe
                if os.path.exists(ruta):
                    imagen = Image.open(ruta)
                    imagen = imagen.resize((80, 80))
                    self.imagenes[nombre] = ImageTk.PhotoImage(imagen)
                    print(f"Imagen {nombre} cargada exitosamente")
                else:
                    print(f"El archivo no existe: {ruta}")
                    # Buscar el archivo en el directorio
                    directorio = "C:/Users/vdeag/OneDrive/Desktop/Repositorio intro/"
                    archivos = os.listdir(directorio)
                    print(f"Archivos disponibles en el directorio:")
                    for archivo in archivos:
                        if archivo.lower().endswith('.png'):
                            print(f"- {archivo}")
                    
                    # Crear imagen en blanco como fallback
                    imagen_blanca = Image.new('RGB', (80, 80), 'white')
                    self.imagenes[nombre] = ImageTk.PhotoImage(imagen_blanca)
                    
            except Exception as e:
                print(f"Error cargando {nombre}: {str(e)}")
                imagen_blanca = Image.new('RGB', (80, 80), 'white')
                self.imagenes[nombre] = ImageTk.PhotoImage(imagen_blanca)

    def crear_matriz(self, size):
        # Reiniciar los valores de los objetos disponibles
        self.objetos_disponibles = {
            'azucar': {'clase': Azucar, 'cantidad': 2, 'params': {'puntos': 10}},
            'vino': {'clase': Vino, 'cantidad': 2, 'params': {'nivel_alcohol': 5}},
            'veneno': {'clase': Veneno, 'cantidad': 2, 'params': {}},
            'hormiga': {'clase': Hormiga, 'cantidad': 1, 'params': {'posicion': (0,0)}},
            'piedra': {'clase': None, 'cantidad': 3, 'params': {}},
            'final': {'clase': None, 'cantidad': 1, 'params': {}},
            'vacio': {'clase': None, 'cantidad': None, 'params': {}}
        }
        
        # Reiniciar el tamaño y la matriz
        self.size = size
        self.matriz_objetos = [[None for _ in range(size)] for _ in range(size)]
        
        # Limpiar la ventana
        for widget in self.ventana.winfo_children():
            widget.destroy()

        # Frame para los controles
        frame_controles = tk.Frame(self.ventana)
        frame_controles.grid(row=size+1, column=0, columnspan=size+1, pady=10)

        # Botón de inicio
        boton_inicio = tk.Button(
            frame_controles,
            text="INICIO",
            font=("Arial", 12),
            bg="green",
            fg="white",
            command=self.iniciar_simulacion
        )
        boton_inicio.pack(side=tk.LEFT, padx=5)

        # Botón de volver
        boton_volver = tk.Button(
            frame_controles,
            text="Volver",
            font=("Arial", 12),
            bg="red",
            fg="white",
            command=self.mostrar_pantalla_inicio
        )
        boton_volver.pack(side=tk.LEFT, padx=5)

        # Crear botones de la izquierda
        for i, (nombre, datos) in enumerate(self.objetos_disponibles.items()):
            if datos['cantidad'] is not None:
                boton = tk.Button(
                    self.ventana,
                    image=self.imagenes[nombre],
                    width=80, height=80,
                    command=lambda n=nombre: self.seleccionar_objeto(n)
                )
                boton.image = self.imagenes[nombre]
                boton.grid(row=i, column=0)
                
                # Agregar contador
                label = tk.Label(self.ventana, text=str(datos['cantidad']))
                label.grid(row=i, column=0, sticky='e')

        # Crear matriz de botones
        for i in range(size):
            for j in range(size):
                boton = tk.Button(
                    self.ventana,
                    image=self.imagenes['vacio'],
                    width=80, height=80,
                    command=lambda r=i, c=j: self.colocar_objeto(r, c)
                )
                boton.image = self.imagenes['vacio']
                boton.grid(row=i, column=j+1)
                boton.info = {'tipo': 'vacio', 'objeto': None}

    def seleccionar_objeto(self, nombre):
        if self.objetos_disponibles[nombre]['cantidad'] > 0:
            self.objeto_seleccionado = nombre

    def colocar_objeto(self, fila, columna):
        if hasattr(self, 'objeto_seleccionado'):
            datos = self.objetos_disponibles[self.objeto_seleccionado]
            if datos['cantidad'] > 0:
                # Crear instancia del objeto
                if datos['clase'] is not None:
                    objeto = datos['clase'](**datos['params'])
                else:
                    objeto = self.objeto_seleccionado

                # Actualizar matriz y botón
                self.matriz_objetos[fila][columna] = objeto
                boton = self.ventana.grid_slaves(row=fila, column=columna+1)[0]
                boton.config(image=self.imagenes[self.objeto_seleccionado])
                boton.image = self.imagenes[self.objeto_seleccionado]
                boton.info = {'tipo': self.objeto_seleccionado, 'objeto': objeto}

                # Actualizar contador
                datos['cantidad'] -= 1
                self.actualizar_contadores()

    def actualizar_contadores(self):
        for i, (nombre, datos) in enumerate(self.objetos_disponibles.items()):
            if datos['cantidad'] is not None:
                label = self.ventana.grid_slaves(row=i, column=0)[0]
                if isinstance(label, tk.Label):
                    label.config(text=str(datos['cantidad']))

    def obtener_objeto(self, fila, columna):
        return self.matriz_objetos[fila][columna]

    def estadisticas(self):
        self.ventana.withdraw()
        ventana_estadisticas = tk.Toplevel()
        ventana_estadisticas.geometry(f"{self.ANCHO_VENTANA}x{self.ALTO_VENTANA}")
        ventana_estadisticas.title("Estadísticas")

        label = tk.Label(ventana_estadisticas, text="Estadísticas", font=("Arial", 24))
        label.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        boton_volver = tk.Button(ventana_estadisticas, text="Volver", font=("Arial", 16), command=lambda: self.volver_a_principal(ventana_estadisticas), bg="red", fg="white", width=10, height=3)
        boton_volver.grid(row=4, column=2, padx=10, pady=10, sticky="nsew")

    def validar_laberinto(self):
        elementos_requeridos = {
            'hormiga': 1,
            'final': 1
        }
        
        elementos_encontrados = {
            'hormiga': 0,
            'final': 0
        }
        
        # Contar elementos en la matriz
        for i in range(self.size):
            for j in range(self.size):
                objeto = self.matriz_objetos[i][j]
                if isinstance(objeto, Hormiga):
                    elementos_encontrados['hormiga'] += 1
                elif isinstance(objeto, str) and objeto == 'final':
                    elementos_encontrados['final'] += 1
        
        # Verificar que se cumplan los requisitos
        mensajes_error = []
        for elemento, cantidad_requerida in elementos_requeridos.items():
            if elementos_encontrados[elemento] < cantidad_requerida:
                mensajes_error.append(f"Falta colocar {elemento}")
            elif elementos_encontrados[elemento] > cantidad_requerida:
                mensajes_error.append(f"Solo debe haber un {elemento}")
        
        if mensajes_error:
            messagebox.showerror("Error", "\n".join(mensajes_error))
            return False
        
        return True

    def iniciar_simulacion(self):
        if not self.validar_laberinto():
            return
        
        # Encontrar la posición inicial de la hormiga
        posicion_hormiga = None
        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.matriz_objetos[i][j], Hormiga):
                    posicion_hormiga = (i, j)
                    break
            if posicion_hormiga:
                break

        if not posicion_hormiga:
            messagebox.showerror("Error", "No se encontró la hormiga en el laberinto")
            return

        # Inicializar variables de simulación
        self.hormiga = self.matriz_objetos[posicion_hormiga[0]][posicion_hormiga[1]]
        self.posicion_inicial = posicion_hormiga
        self.mejor_puntuacion = float('-inf')
        self.mejor_ruta = None
        self.intento_actual = 0
        self.max_intentos = 100
        
        # Agregar botones de control
        self.crear_controles_simulacion()
        
        # Iniciar primer intento
        self.iniciar_nuevo_intento()

    def crear_controles_simulacion(self):
        frame_controles = tk.Frame(self.ventana)
        frame_controles.grid(row=self.size+2, column=0, columnspan=self.size+1, pady=10)

        self.boton_siguiente = tk.Button(
            frame_controles,
            text="Siguiente Intento",
            command=self.iniciar_nuevo_intento
        )
        self.boton_siguiente.pack(side=tk.LEFT, padx=5)

        self.boton_pausar = tk.Button(
            frame_controles,
            text="Pausar",
            command=self.pausar_simulacion
        )
        self.boton_pausar.pack(side=tk.LEFT, padx=5)

        self.boton_continuar = tk.Button(
            frame_controles,
            text="Continuar",
            command=self.continuar_simulacion
        )
        self.boton_continuar.pack(side=tk.LEFT, padx=5)
        self.boton_continuar.config(state=tk.DISABLED)

        # Etiquetas de información
        self.label_intento = tk.Label(frame_controles, text="Intento: 0")
        self.label_intento.pack(side=tk.LEFT, padx=5)
        
        self.label_mejor = tk.Label(frame_controles, text="Mejor puntuación: 0")
        self.label_mejor.pack(side=tk.LEFT, padx=5)

    def iniciar_nuevo_intento(self):
        # Reiniciar el laberinto
        self.reiniciar_laberinto()
        
        self.intento_actual += 1
        self.label_intento.config(text=f"Intento: {self.intento_actual}")
        
        # Generar nueva secuencia de movimientos
        self.secuencia_actual = self.generar_secuencia_movimientos()
        self.indice_secuencia = 0
        
        self.simulacion_activa = True
        self.pausado = False
        self.boton_pausar.config(state=tk.NORMAL)
        self.boton_continuar.config(state=tk.DISABLED)
        
        self.ejecutar_turno()

    def reiniciar_laberinto(self):
        # Limpiar posición anterior de la hormiga
        if hasattr(self, 'posicion_actual'):
            fila, columna = self.posicion_actual
            boton = self.ventana.grid_slaves(row=fila, column=columna+1)[0]
            boton.config(image=self.imagenes['vacio'])
            boton.image = self.imagenes['vacio']
        
        # Restaurar hormiga a posición inicial
        self.posicion_actual = self.posicion_inicial
        fila, columna = self.posicion_inicial
        boton = self.ventana.grid_slaves(row=fila, column=columna+1)[0]
        boton.config(image=self.imagenes['hormiga'])
        boton.image = self.imagenes['hormiga']
        
        # Reiniciar estados de la hormiga
        self.hormiga.salud = 100
        self.hormiga.nivel_alcohol = 0
        self.hormiga.puntos = 0
        
        self.actualizar_estado_hormiga()

    def pausar_simulacion(self):
        self.pausado = True
        self.boton_pausar.config(state=tk.DISABLED)
        self.boton_continuar.config(state=tk.NORMAL)

    def continuar_simulacion(self):
        self.pausado = False
        self.boton_pausar.config(state=tk.NORMAL)
        self.boton_continuar.config(state=tk.DISABLED)
        self.ejecutar_turno()

    def ejecutar_turno(self):
        if not self.simulacion_activa or self.pausado:
            return

        if self.indice_secuencia >= len(self.secuencia_actual):
            # Fin de la secuencia actual
            puntuacion_actual = self.calcular_puntuacion()
            if puntuacion_actual > self.mejor_puntuacion:
                self.mejor_puntuacion = puntuacion_actual
                self.mejor_ruta = self.secuencia_actual
                self.label_mejor.config(text=f"Mejor puntuación: {puntuacion_actual}")
            
            if self.intento_actual >= self.max_intentos:
                self.finalizar_simulacion()
            return

        # Ejecutar siguiente movimiento
        accion = self.secuencia_actual[self.indice_secuencia]
        self.indice_secuencia += 1

        if accion == "comer":
            self.hormiga.interactuar_con_objeto(self)
            self.actualizar_estado_hormiga()  # Actualizar después de comer
        else:
            nueva_posicion = self.hormiga.calcular_nueva_posicion(accion)
            if self.hormiga.es_movimiento_valido(nueva_posicion, self):
                self.mover_hormiga(nueva_posicion)
                self.actualizar_estado_hormiga()  # Actualizar después de moverse

        # Verificar si llegó al final
        fila, columna = self.posicion_actual
        if self.matriz_objetos[fila][columna] == 'final':
            self.registrar_exito()
            return

        # Programar siguiente movimiento
        self.ventana.after(500, self.ejecutar_turno)

    def calcular_puntuacion(self):
        return (self.hormiga.puntos * 10) - (self.hormiga.nivel_alcohol * 5) - (self.indice_secuencia * 2)

    def registrar_exito(self):
        puntuacion = self.calcular_puntuacion()
        if puntuacion > self.mejor_puntuacion:
            self.mejor_puntuacion = puntuacion
            self.mejor_ruta = self.secuencia_actual[:self.indice_secuencia]
            self.label_mejor.config(text=f"Mejor puntuación: {puntuacion}")
        
        messagebox.showinfo("¡Éxito!", 
                          f"¡La hormiga llegó al final!\n"
                          f"Puntos: {self.hormiga.puntos}\n"
                          f"Nivel de alcohol: {self.hormiga.nivel_alcohol}\n"
                          f"Pasos: {self.indice_secuencia}")

    def finalizar_simulacion(self):
        self.simulacion_activa = False
        if self.mejor_ruta:
            messagebox.showinfo("Simulación completada",
                              f"Mejor puntuación: {self.mejor_puntuacion}\n"
                              f"Encontrada en el intento: {self.intento_actual}")
        else:
            messagebox.showinfo("Simulación completada",
                              "No se encontró una ruta exitosa")

    def actualizar_estado_hormiga(self):
        # Crear o actualizar frame de estado si no existe
        if not hasattr(self, 'frame_estado'):
            self.frame_estado = tk.Frame(self.ventana)
            self.frame_estado.grid(row=self.size+3, column=0, columnspan=self.size+1, pady=5)
            
            # Crear etiquetas para mostrar el estado
            self.label_salud = tk.Label(self.frame_estado, text="Salud: 100")
            self.label_salud.pack(side=tk.LEFT, padx=5)
            
            self.label_alcohol = tk.Label(self.frame_estado, text="Alcohol: 0")
            self.label_alcohol.pack(side=tk.LEFT, padx=5)
            
            self.label_puntos = tk.Label(self.frame_estado, text="Puntos: 0")
            self.label_puntos.pack(side=tk.LEFT, padx=5)
        
        # Actualizar valores
        self.label_salud.config(text=f"Salud: {self.hormiga.salud}")
        self.label_alcohol.config(text=f"Alcohol: {self.hormiga.nivel_alcohol}")
        self.label_puntos.config(text=f"Puntos: {self.hormiga.puntos}")

    def generar_secuencia_movimientos(self):
        # Lista de posibles acciones
        acciones = ["arriba", "abajo", "izquierda", "derecha", "comer"]
        
        # Generar una secuencia aleatoria de movimientos
        # El tamaño de la secuencia puede ser ajustado según necesites
        tam_secuencia = self.size * self.size * 2  # Por ejemplo, 2 veces el área del laberinto
        
        secuencia = []
        for _ in range(tam_secuencia):
            # Agregar una acción aleatoria a la secuencia
            accion = random.choice(acciones)
            secuencia.append(accion)
        
        return secuencia

    def mover_hormiga(self, nueva_posicion):
        # Limpiar posición anterior
        fila_actual, columna_actual = self.posicion_actual
        boton_actual = self.ventana.grid_slaves(row=fila_actual, column=columna_actual+1)[0]
        boton_actual.config(image=self.imagenes['vacio'])
        boton_actual.image = self.imagenes['vacio']
        
        # Actualizar posición
        self.posicion_actual = nueva_posicion
        fila_nueva, columna_nueva = nueva_posicion
        
        # Actualizar visual en nueva posición
        boton_nuevo = self.ventana.grid_slaves(row=fila_nueva, column=columna_nueva+1)[0]
        boton_nuevo.config(image=self.imagenes['hormiga'])
        boton_nuevo.image = self.imagenes['hormiga']
        
        # Actualizar posición de la hormiga en la matriz
        self.matriz_objetos[fila_actual][columna_actual] = None
        self.matriz_objetos[fila_nueva][columna_nueva] = self.hormiga
        
        # Actualizar la posición de la hormiga
        self.hormiga.posicion = nueva_posicion

if __name__ == "__main__":
    ventana = tk.Tk()
    app = Laberinto(ventana)
    app.mostrar_pantalla_inicio()
    ventana.mainloop()