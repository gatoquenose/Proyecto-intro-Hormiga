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
            'azucar': {'clase': Azucar, 'cantidad': 2, 'params': {'puntos': 200}},
            'vino': {'clase': Vino, 'cantidad': 2, 'params': {'nivel_alcohol': 50}},
            'veneno': {'clase': Veneno, 'cantidad': 2, 'params': {}},
            'hormiga': {'clase': Hormiga, 'cantidad': 1, 'params': {'posicion': (0,0)}},
            'piedra': {'clase': None, 'cantidad': 3, 'params': {}},
            'final': {'clase': None, 'cantidad': 1, 'params': {}},
            'vacio': {'clase': None, 'cantidad': None, 'params': {}}
        }
        self.estado_inicial = None  # Para guardar el estado inicial del laberinto
        self.posiciones_iniciales = {}  # Para guardar las posiciones iniciales de los objetos
        self.simulacion_iniciada = False  # Nueva variable

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
                
                if os.path.exists(ruta):
                    imagen = Image.open(ruta)
                    imagen = imagen.resize((80, 80))
                    self.imagenes[nombre] = ImageTk.PhotoImage(imagen)
                    
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
                imagen_blanca = Image.new('RGB', (80, 80), 'white')
                self.imagenes[nombre] = ImageTk.PhotoImage(imagen_blanca)

    def crear_matriz(self, size):
        # Reiniciar la bandera de simulación iniciada
        self.simulacion_iniciada = False
        
        # Reiniciar los valores de los objetos disponibles
        self.objetos_disponibles = {
            'azucar': {'clase': Azucar, 'cantidad': 2, 'params': {'puntos': 200}},
            'vino': {'clase': Vino, 'cantidad': 2, 'params': {'nivel_alcohol': 50}},
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
        if self.simulacion_iniciada:  # Si la simulación está iniciada, no permitir cambios
            return
        
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
        
        # Marcar que la simulación ha iniciado
        self.simulacion_iniciada = True
        
        # Encontrar la posición inicial de la hormiga
        self.posicion_inicial = None
        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.matriz_objetos[i][j], Hormiga):
                    self.posicion_inicial = (i, j)
                    self.hormiga = self.matriz_objetos[i][j]
                    self.hormiga.posicion = (i, j)  # Asegurarnos que la hormiga conoce su posición
                    break
            if self.posicion_inicial:
                break

        # Inicializar variables de simulación
        self.posicion_actual = self.posicion_inicial
        self.mejor_puntuacion = float('-inf')
        self.mejor_ruta = None
        self.intento_actual = 0
        self.max_intentos = 100
        
        # Guardar estado inicial
        self.guardar_estado_inicial()
        
        # Crear controles de simulación
        self.crear_controles_simulacion()
        
        # Iniciar primer intento
        self.iniciar_nuevo_intento()

    def crear_controles_simulacion(self):
        frame_controles = tk.Frame(self.ventana)
        frame_controles.grid(row=self.size+2, column=0, columnspan=self.size+1, pady=10)

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
        
        self.label_puntuacion = tk.Label(frame_controles, text="Puntuación: 0")
        self.label_puntuacion.pack(side=tk.LEFT, padx=5)
        
        self.label_alcohol = tk.Label(frame_controles, text="Nivel de alcohol: 0")
        self.label_alcohol.pack(side=tk.LEFT, padx=5)

    def iniciar_nuevo_intento(self):
        # Restaurar el laberinto al estado inicial
        self.restaurar_posiciones()
        
        # Asegurarse de que la posición actual sea la inicial
        self.posicion_actual = self.posicion_inicial
        self.hormiga.posicion = self.posicion_inicial
        
        self.intento_actual += 1
        self.label_intento.config(text=f"Intento: {self.intento_actual}")
        
        # Generar nueva secuencia de movimientos
        self.secuencia_actual = self.generar_secuencia_movimientos()
        self.indice_secuencia = 0
        
        # Reiniciar estados de la hormiga
        self.hormiga.salud = 100
        self.hormiga.nivel_alcohol = 0
        self.hormiga.puntos = 0
        
        # Actualizar puntuación y nivel de alcohol
        self.label_puntuacion.config(text=f"Puntuación: {self.hormiga.puntos}")
        self.label_alcohol.config(text=f"Nivel de alcohol: {self.hormiga.nivel_alcohol}")
        
        self.simulacion_activa = True
        self.pausado = False
        
        # Actualizar visualización inicial
        self.actualizar_estado_hormiga()
        
        # Iniciar la ejecución de turnos
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
            if self.intento_actual < self.max_intentos:
                self.ventana.after(1000, self.iniciar_nuevo_intento)
            else:
                self.finalizar_simulacion()
            return

        # Ejecutar siguiente movimiento
        accion = self.secuencia_actual[self.indice_secuencia]
        self.indice_secuencia += 1

        if accion == "comer":
            resultado = self.hormiga.interactuar_con_objeto(self)
            # Actualizar etiquetas después de cada interacción
            self.label_puntuacion.config(text=f"Puntuación: {self.hormiga.puntos}")
            self.label_alcohol.config(text=f"Nivel de alcohol: {self.hormiga.nivel_alcohol}")
            
            if resultado == "veneno":
                self.restaurar_posiciones()
                self.reiniciar_estados_hormiga()
                self.ventana.after(1000, self.iniciar_nuevo_intento)
                return
        else:
            nueva_posicion = self.hormiga.calcular_nueva_posicion(accion)
            if self.hormiga.es_movimiento_valido(nueva_posicion, self):
                self.mover_hormiga(nueva_posicion)
                self.actualizar_estado_hormiga()

        # Verificar si llegó al final
        fila, columna = self.posicion_actual
        if self.matriz_objetos[fila][columna] == 'final':
            self.registrar_exito()
            return

        # Programar siguiente movimiento
        self.ventana.after(500, self.ejecutar_turno)

    def calcular_puntuacion(self):
        # Ajustar los pesos según la importancia de cada factor
        peso_movimientos = 2
        peso_puntos = 1
        peso_alcohol = 1.5
        
        # Calcular puntuación (los negativos son para minimizar movimientos y alcohol)
        puntuacion = (
            -peso_movimientos * self.indice_secuencia +  # Menos movimientos es mejor
            peso_puntos * self.hormiga.puntos +          # Más puntos es mejor
            -peso_alcohol * self.hormiga.nivel_alcohol    # Menos alcohol es mejor
        )
        
        return puntuacion

    def registrar_exito(self):
        puntuacion = self.calcular_puntuacion()
        if puntuacion > self.mejor_puntuacion:
            self.mejor_puntuacion = puntuacion
            self.mejor_ruta = self.secuencia_actual[:self.indice_secuencia]
            self.label_mejor.config(text=f"Mejor puntuación: {puntuacion}")
        
        # Restaurar posiciones y estados
        self.restaurar_posiciones()
        self.reiniciar_estados_hormiga()
        
        # Continuar con el siguiente intento con delay
        if self.intento_actual < self.max_intentos:
            self.ventana.after(1000, self.iniciar_nuevo_intento)  # 1 segundo entre intentos exitosos
        else:
            self.finalizar_simulacion()

    def reiniciar_estados_hormiga(self):
        # Reiniciar estados de la hormiga
        self.hormiga.salud = 100
        self.hormiga.nivel_alcohol = 0
        self.hormiga.puntos = 0
        
        # Solo actualizar las etiquetas si existen
        if hasattr(self, 'label_salud'):
            self.label_salud.config(text=f"Salud: {self.hormiga.salud}")
        if hasattr(self, 'label_alcohol'):
            self.label_alcohol.config(text=f"Alcohol: {self.hormiga.nivel_alcohol}")
        if hasattr(self, 'label_puntos'):
            self.label_puntos.config(text=f"Puntos: {self.hormiga.puntos}")

    def finalizar_simulacion(self):
        self.simulacion_activa = False
        if self.mejor_ruta:
            mensaje = (
                f"Simulación completada\n"
                f"Mejor puntuación: {self.mejor_puntuacion}\n"
                f"Encontrada en el intento: {self.intento_actual}\n"
                f"Cantidad de movimientos: {len(self.mejor_ruta)}\n"
                f"Puntos finales: {self.hormiga.puntos}\n"
                f"Nivel de alcohol final: {self.hormiga.nivel_alcohol}"
            )
            messagebox.showinfo("Simulación completada", mensaje)
            
            # Mostrar la mejor ruta encontrada
            self.mostrar_mejor_ruta()
        else:
            messagebox.showinfo("Simulación completada",
                              "No se encontró una ruta exitosa")

    def actualizar_estado_hormiga(self):
        # Actualizar etiquetas con los valores actuales
        self.label_puntuacion.config(text=f"Puntuación: {self.hormiga.puntos}")
        self.label_alcohol.config(text=f"Nivel de alcohol: {self.hormiga.nivel_alcohol}")

    def generar_secuencia_movimientos(self):
        # Lista de posibles acciones
        acciones = ["arriba", "abajo", "izquierda", "derecha", "comer"]
        
        # Generar una secuencia más corta para favorecer rutas eficientes
        tam_secuencia = self.size * self.size  # Ajustar según necesidad
        
        secuencia = []
        for _ in range(tam_secuencia):
            # Dar más peso a los movimientos que a comer
            if random.random() < 0.8:  # 80% de probabilidad de movimiento
                accion = random.choice(["arriba", "abajo", "izquierda", "derecha"])
            else:
                accion = "comer"
            secuencia.append(accion)
        
        return secuencia

    def mover_hormiga(self, nueva_posicion):
        # Validar que el movimiento sea a una posición adyacente
        fila_actual, col_actual = self.posicion_actual
        fila_nueva, col_nueva = nueva_posicion
        
        if abs(fila_nueva - fila_actual) > 1 or abs(col_nueva - col_actual) > 1:
            return  # No permitir saltos
        
        # Limpiar posición anterior
        boton_actual = self.ventana.grid_slaves(row=fila_actual, column=col_actual+1)[0]
        boton_actual.config(image=self.imagenes['vacio'])
        boton_actual.image = self.imagenes['vacio']
        
        # Actualizar posición
        self.posicion_actual = nueva_posicion
        self.hormiga.posicion = nueva_posicion
        
        # Actualizar visual en nueva posición
        boton_nuevo = self.ventana.grid_slaves(row=fila_nueva, column=col_nueva+1)[0]
        boton_nuevo.config(image=self.imagenes['hormiga'])
        boton_nuevo.image = self.imagenes['hormiga']
        
        # Actualizar matriz
        self.matriz_objetos[fila_actual][col_actual] = None
        self.matriz_objetos[fila_nueva][col_nueva] = self.hormiga

    def guardar_estado_inicial(self):
        # Guardar una copia del estado inicial de la matriz
        self.estado_inicial = []
        self.posiciones_iniciales = {}  # Reiniciar el diccionario
        
        for i in range(self.size):
            fila = []
            for j in range(self.size):
                objeto = self.matriz_objetos[i][j]
                tipo_objeto = 'vacio'
                
                if isinstance(objeto, Hormiga):
                    tipo_objeto = 'hormiga'
                elif isinstance(objeto, Azucar):
                    tipo_objeto = 'azucar'
                elif isinstance(objeto, Vino):
                    tipo_objeto = 'vino'
                elif isinstance(objeto, Veneno):
                    tipo_objeto = 'veneno'
                elif objeto == 'final':
                    tipo_objeto = 'final'
                elif objeto == 'piedra':
                    tipo_objeto = 'piedra'
                
                fila.append({
                    'tipo': tipo_objeto,
                    'objeto': objeto
                })
                
                # Guardar posiciones de objetos importantes
                if tipo_objeto != 'vacio':
                    self.posiciones_iniciales[(i, j)] = {
                        'tipo': tipo_objeto,
                        'objeto': objeto
                    }
            
            self.estado_inicial.append(fila)

    def restaurar_posiciones(self):
        # Primero limpiamos todas las casillas
        for i in range(self.size):
            for j in range(self.size):
                boton = self.ventana.grid_slaves(row=i, column=j+1)[0]
                boton.config(image=self.imagenes['vacio'])
                boton.image = self.imagenes['vacio']
                self.matriz_objetos[i][j] = None
                boton.info['tipo'] = 'vacio'
                boton.info['objeto'] = None

        # Luego restauramos los objetos a sus posiciones iniciales
        for (i, j), datos in self.posiciones_iniciales.items():
            boton = self.ventana.grid_slaves(row=i, column=j+1)[0]
            tipo = datos['tipo']
            objeto = datos['objeto']
            
            # Usar el tipo para obtener la imagen correcta
            boton.config(image=self.imagenes[tipo])
            boton.image = self.imagenes[tipo]
            self.matriz_objetos[i][j] = objeto
            boton.info['tipo'] = tipo
            boton.info['objeto'] = objeto

    def mostrar_mejor_ruta(self):
        # Restaurar el laberinto al estado inicial
        self.restaurar_posiciones()
        self.reiniciar_estados_hormiga()
        
        # Reproducir la mejor ruta encontrada con más delay
        for i, accion in enumerate(self.mejor_ruta):
            self.ventana.after(1000 * i, lambda a=accion: self.ejecutar_accion(a))  # 1 segundo entre movimientos

    def ejecutar_accion(self, accion):
        if accion == "comer":
            self.hormiga.interactuar_con_objeto(self)
        else:
            nueva_posicion = self.hormiga.calcular_nueva_posicion(accion)
            if self.hormiga.es_movimiento_valido(nueva_posicion, self):
                self.mover_hormiga(nueva_posicion)
        
        self.actualizar_estado_hormiga()

if __name__ == "__main__":
    ventana = tk.Tk()
    app = Laberinto(ventana)
    app.mostrar_pantalla_inicio()
    ventana.mainloop()