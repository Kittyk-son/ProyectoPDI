import tkinter as tk
from tkinter import Menu, messagebox
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
import math

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes")
        
        # Crear el menú principal
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Submenú de brillo
        self.brightness_menu = Menu(self.menu_bar, tearoff=0)
        self.brightness_menu.add_command(label="Contracción", command=self.contraccion)
        self.brightness_menu.add_command(label="Desplazamiento", command=self.desplazamiento)
        self.brightness_menu.add_command(label="Ecualización", command=self.ecualizar_imagen)
        self.brightness_menu.add_command(label="Ecualización Exponencial", command=self.ecualizacion_exp)

        self.menu_bar.add_cascade(label="Ajustes de Brillo", menu=self.brightness_menu)

        # Crear áreas de visualización para las imágenes
        self.image_label = tk.Label(root)
        self.image_label.pack()

        # Inicializar variables de imagen
        self.image = None
        self.image_np = None

    # Métodos de ajuste de brillo
    def contraccion(self):
        if self.image_np is not None:
            self.image_np = self.ajustar_histograma_contraccion(self.image_np)
            self.mostrar_imagen_resultado(self.image_np)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def desplazamiento(self):
        if self.image_np is not None:
            self.image_np = self.ajustar_histograma_desplazamiento(self.image_np)
            self.mostrar_imagen_resultado(self.image_np)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def ecualizar_imagen(self):
        if self.image_np is not None:
            self.image_np = self.ajustar_histograma_ecualizacion(self.image_np)
            self.mostrar_imagen_resultado(self.image_np)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def ecualizacion_exp(self):
        if self.image_np is not None:
            self.image_np = self.ajustar_histograma_ecualizacion_exp(self.image_np)
            self.mostrar_imagen_resultado(self.image_np)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    # Métodos de procesamiento de imágenes
    def ajustar_histograma_contraccion(self, img):
        F_MAX, F_MIN = np.max(img), np.min(img)
        MAX, MIN = 255, 0  # Valores de rango deseado
        operacion = (MAX - MIN) / (F_MAX - F_MIN) * (img - F_MIN) + MIN
        return np.clip(operacion, MIN, MAX).astype(np.uint8)

    def ajustar_histograma_desplazamiento(self, img, desplazamiento=50):
        img = cv.add(img, desplazamiento)
        return np.clip(img, 0, 255).astype(np.uint8)

    def ajustar_histograma_ecualizacion(self, img):
        if len(img.shape) == 2:
            return cv.equalizeHist(img)
        elif len(img.shape) == 3:
            img_yuv = cv.cvtColor(img, cv.COLOR_BGR2YUV)
            img_yuv[:, :, 0] = cv.equalizeHist(img_yuv[:, :, 0])
            return cv.cvtColor(img_yuv, cv.COLOR_YUV2BGR)

    def ajustar_histograma_ecualizacion_exp(self, img):
        G_MIN = np.min(img)
        ALFA = np.var(img)
        total_pixeles = img.size
        histograma = cv.calcHist([img], [0], None, [256], [0, 256])
        probabilidades = histograma.ravel() / total_pixeles
        lista_frec_acumulada = np.cumsum(probabilidades)

        epsilon = 1e-10
        mapa = np.zeros(256, dtype=np.float32)
        for i, Pg_g in enumerate(lista_frec_acumulada):
            Pg_g = min(Pg_g, 1 - epsilon)
            mapa[i] = G_MIN - (1 / ALFA) * math.log(1 - Pg_g)

        ecualizacion = mapa[img]
        return np.clip(ecualizacion, 0, 255).astype(np.uint8)

    def mostrar_imagen_resultado(self, img):
        self.result_image = Image.fromarray(img)
        self.result_image_tk = ImageTk.PhotoImage(self.result_image)
        self.image_label.config(image=self.result_image_tk)
        self.image_label.image = self.result_image_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()