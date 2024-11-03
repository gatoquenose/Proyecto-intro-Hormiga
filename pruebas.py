import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

class Laberinto:
    def __init__(self, filas, columnas):
        if not (3 <= filas <= 10 and 3 <= columnas <= 10):
            raise ValueError("El tamaño de la matriz debe estar entre 3x3 y 10x10")
        self.matriz = [[' ' for _ in range(columnas)] for _ in range(filas)]
        self.items = ['azucar', 'vino', 'veneno', 'roca']
        self.ant_image_path = r'C:\Users\vdeag\OneDrive\Desktop\Repositorio intro\imagen hormiga.png'
    
    def crear_laberinto(self):
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[i])):
                if random.random() < 0.2:  # 20% chance to place an item
                    self.matriz[i][j] = random.choice(self.items)
    
    def actualizar_estado(self, x, y, nuevo_estado):
        if 0 <= x < len(self.matriz) and 0 <= y < len(self.matriz[0]):
            self.matriz[x][y] = nuevo_estado
        else:
            raise IndexError("Coordenadas fuera del rango del laberinto")

class LaberintoGUI:
    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.root = tk.Tk()
        self.root.title("Laberinto")
        
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()
        
        self.mostrar_matriz()
        self.mostrar_imagen_hormiga()
        
        self.root.mainloop()
    
    def mostrar_matriz(self):
        for i in range(len(self.laberinto.matriz)):
            for j in range(len(self.laberinto.matriz[i])):
                x0, y0 = j * 50, i * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
                self.canvas.create_text((x0 + 25, y0 + 25), text=self.laberinto.matriz[i][j])
    
    def mostrar_imagen_hormiga(self):
        try:
            img = Image.open(self.laberinto.ant_image_path)
            img = img.resize((50, 50))
            self.ant_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(25, 25, image=self.ant_image, anchor=tk.NW)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la imagen: {e}")

# Ejemplo de uso
laberinto = Laberinto(5, 5)
laberinto.crear_laberinto()
laberinto.actualizar_estado(2, 2, 'hormiga')

LaberintoGUI(laberinto)