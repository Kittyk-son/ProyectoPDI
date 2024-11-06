import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import math
import funciones as fun

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes")
        self.root.geometry("1024x768")
        self.root.state('zoomed')

        # Colores personalizados
        self.bg_color = "#4d4d4d"
        self.button_color = "#33c1bd"
        self.sidebar_bg_color = "#2e8378"
        self.button_hover_color = "#28a7a1"
        self.menu_bg_color = "#57b67b"

        self.root.config(bg=self.bg_color)

        # Barra de menú
        self.menu_bar = tk.Menu(self.root, bg=self.menu_bg_color, fg="white")
        self.root.config(menu=self.menu_bar)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.menu_bg_color, fg="white")
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Salir", command=self.root.quit)

        # Barra lateral izquierda
        self.sidebar = tk.Frame(self.root, width=200, bg=self.bg_color)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
        self.buttons = [
            ("Operaciones Aritméticas", self.operaciones_aritmeticas),
            ("Operaciones Lógicas", self.operaciones_logicas),
            ("Aplicar Umbralizado", self.aplicar_umbral),
            ("Convertir a Niveles de Gris", self.convertir_gris),
            ("Histograma", self.histograma),
            ("Componentes RGB", self.componentes_rgb),
            ("Ajustes de Brillo", self.operaciones_de_ajuste_de_brillo)
        ]

        for (text, command) in self.buttons:
            button = tk.Button(self.sidebar, text=text, command=command, width=20, height=3,
                               bg=self.button_color, fg="white", font=("Arial", 12, "bold"),
                               activebackground=self.button_hover_color)
            button.pack(pady=10)

        # Área de visualización de imágenes
        self.display_area = tk.Frame(self.root, bg="white")
        self.display_area.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.left_area = tk.Frame(self.display_area, bg="white")
        self.left_area.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Botón y área de imagen para cargar Imagen 1
        self.image_button_top = tk.Button(self.left_area, text="Cargar Imagen 1", command=self.load_image_top,
                                          bg=self.button_color, fg="white", font=("Arial", 10, "bold"))
        self.image_button_top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.image_frame_top = tk.Label(self.left_area, bg="white", text="Imagen 1")
        self.image_frame_top.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Botón y área de imagen para cargar Imagen 2
        self.image_button_bottom = tk.Button(self.left_area, text="Cargar Imagen 2", command=self.load_image_bottom,
                                             bg=self.button_color, fg="white", font=("Arial", 10, "bold"))
        self.image_button_bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        self.image_frame_bottom = tk.Label(self.left_area, bg="white", text="Imagen 2")
        self.image_frame_bottom.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Área para mostrar resultado
        self.right_area = tk.Frame(self.display_area, bg="white")
        self.right_area.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.result_label = tk.Label(self.right_area, bg="white", text="Resultado")
        self.result_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.save_button = tk.Button(self.right_area, text="Guardar Imagen", command=self.save_image_result,
                                     bg=self.button_color, fg="white", font=("Arial", 12, "bold"))
        self.save_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        self.save_button.config(state=tk.DISABLED)

        # Variables de imágenes
        self.image_top = None
        self.image_bottom = None
        self.result_image = None

    def load_image_top(self):
        # Abrir un cuadro de diálogo para seleccionar la imagen
        file_path = filedialog.askopenfilename(title="Cargar Imagen 1", filetypes=[("Imágenes", "*.jpg;*.png;*.bmp")])
        if file_path:
            # Cargar la imagen usando PIL
            img_pil = Image.open(file_path)
            
            # Convertir la imagen PIL a un arreglo NumPy para trabajar con OpenCV
            img_np = np.array(img_pil)
            
            # Reescalar la imagen a un tamaño fijo (300x300) usando OpenCV
            img_resized_np = cv.resize(img_np, (300, 300), interpolation=cv.INTER_LINEAR)
            
            # Convertir el arreglo NumPy reescalado nuevamente a formato PIL
            img_resized_pil = Image.fromarray(img_resized_np)

            # Almacenar la imagen redimensionada tanto en formato PIL como en formato NumPy
            self.image_top_pil = img_resized_pil
            self.image_top_np = img_resized_np
            
            # Convertir la imagen redimensionada a PhotoImage para mostrarla en Tkinter
            self.image_top = ImageTk.PhotoImage(img_resized_pil)
            
            # Mostrar la imagen en el widget correspondiente (por ejemplo, una etiqueta)
            self.image_frame_top.config(image=self.image_top)
            self.image_frame_top.image = self.image_top  # Evita que la referencia se pierda

    def load_image_bottom(self):
        # Abrir un cuadro de diálogo para seleccionar la imagen
        file_path = filedialog.askopenfilename(title="Cargar Imagen 2", filetypes=[("Imágenes", "*.jpg;*.png;*.bmp")])
        if file_path:
            # Cargar la imagen usando PIL
            img_pil = Image.open(file_path)
            
            # Convertir la imagen PIL a un arreglo NumPy para usar OpenCV
            img_np = np.array(img_pil)
            
            # Reescalar la imagen a un tamaño fijo (300x300) usando OpenCV
            img_resized_np = cv.resize(img_np, (300, 300), interpolation=cv.INTER_LINEAR)
            
            # Convertir el arreglo NumPy redimensionado de nuevo a formato PIL
            img_resized_pil = Image.fromarray(img_resized_np)

            # Almacenar la imagen redimensionada en formato PIL y NumPy
            self.image_bottom_pil = img_resized_pil
            self.image_bottom_np = img_resized_np
            
            # Convertir la imagen redimensionada a PhotoImage para mostrarla en Tkinter
            self.image_bottom = ImageTk.PhotoImage(img_resized_pil)
            
            # Mostrar la imagen en el widget correspondiente (inferior)
            self.image_frame_bottom.config(image=self.image_bottom)
            self.image_frame_bottom.image = self.image_bottom  # Mantener la referencia

    def save_image_result(self):
        if self.result_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("BMP Files", "*.bmp")])
            if file_path:
                self.result_image.save(file_path)
                messagebox.showinfo("Guardar Imagen", f"Imagen guardada en {file_path}.")

    def mostrar_imagen_resultado(self, imagen):

        # Convertir la imagen redimensionada a un formato compatible con Tkinter
        result_img_display = ImageTk.PhotoImage(imagen)

        # Mostrar la imagen en el área de resultados (label o canvas en la parte derecha)
        self.result_label.config(image=result_img_display)
        self.result_label.image = result_img_display  # Guardar referencia para evitar que se recolecte por el garbage collector

        # Habilitar el botón de guardar si no estaba habilitado
        self.save_button.config(state=tk.NORMAL)
    
    def operaciones_aritmeticas(self):
        try:
            self.ventana_aritmetica = tk.Toplevel(self.root)
            self.ventana_aritmetica.title("Operaciones Aritméticas")
            options = [("Suma Escalar", self.suma_escalar),
                       ("Resta Escalar", self.resta_escalar),
                       ("Multiplicación Escalar", self.multiplicacion_escalar),
                       ("Suma", self.suma),
                       ("Resta", self.resta),
                       ("Multiplicación", self.multiplicacion)]
            for (text, command) in options:
                button = tk.Button(self.ventana_aritmetica, text=text, command=command)
                button.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def suma_escalar(self):
        if self.image_top is not None:
            # Solicitar el valor escalar para la suma
            valor_escalar = simpledialog.askinteger("Suma Escalar", "Introduce el valor escalar para sumar (0 a 255):")
            if valor_escalar is not None:
                # Crear un arreglo con el valor escalar
                escalar_array = np.full(self.image_top_np.shape, valor_escalar, dtype=np.uint8)
                
                # Usar cv2.add para la suma escalar con recorte automático
                suma_resultado = cv.add(self.image_top_np, escalar_array)
                
                # Convertir el resultado de vuelta a imagen PIL y mostrarlo
                self.result_image = Image.fromarray(suma_resultado)
                self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

# Resta escalar con cv2.subtract
    def resta_escalar(self):
        if self.image_top is not None:
            # Solicitar el valor escalar para la resta
            valor_escalar = simpledialog.askinteger("Resta Escalar", "Introduce el valor escalar para restar (0 a 255):")
            if valor_escalar is not None:
                # Crear un arreglo con el valor escalar
                escalar_array = np.full(self.image_top_np.shape, valor_escalar, dtype=np.uint8)
                
                # Usar cv2.subtract para la resta escalar con recorte automático
                resta_resultado = cv.subtract(self.image_top_np, escalar_array)
                
                # Convertir el resultado de vuelta a imagen PIL y mostrarlo
                self.result_image = Image.fromarray(resta_resultado)
                self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def multiplicacion_escalar(self):
        if self.image_top is not None:
            # Solicitar el valor escalar para la resta
            valor_escalar = simpledialog.askinteger("Multiplicacion Escalar", "Introduce el valor continuo para multiplicar (0 a 255):")
            if valor_escalar is not None:
                # Crear un arreglo con el valor escalar
                escalar_array = np.full(self.image_top_np.shape, valor_escalar, dtype=np.uint8)
                
                # Usar cv2.subtract para la resta escalar con recorte automático
                multi_resultado = cv.multiply(self.image_top_np, escalar_array)
                
                # Convertir el resultado de vuelta a imagen PIL y mostrarlo
                self.result_image = Image.fromarray(multi_resultado)
                self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def suma(self):
        if self.image_top is not None and self.image_bottom is not None:
            # Redimensionar la imagen inferior a las dimensiones de la superior
            height_top, width_top = self.image_top_np.shape[:2]
            self.image_bottom_np = self.redimensionar_imagen(self.image_bottom_np, width_top, height_top)
            # Suma de imágenes
            suma_img = cv.add(self.image_top_np,self.image_bottom_np)
            self.result_image = Image.fromarray(suma_img)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar ambas imágenes primero.")

    # 5. Resta entre dos imágenes
    def resta(self):
        if self.image_top is not None and self.image_bottom is not None:
            # Redimensionar la imagen inferior a las dimensiones de la superior
            height_top, width_top = self.image_top_np.shape[:2]
            self.image_bottom_np = self.redimensionar_imagen(self.image_bottom_np, width_top, height_top)
            # Resta de imágenes
            resta_img = cv.subtract(self.image_top_np,self.image_bottom_np)
            self.result_image = Image.fromarray(resta_img)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar ambas imágenes primero.")

    # 6. Multiplicación entre dos imágenes
    def multiplicacion(self):
        if self.image_top is not None and self.image_bottom is not None:
            # Redimensionar la imagen inferior a las dimensiones de la superior
            height_top, width_top = self.image_top_np.shape[:2]
            self.image_bottom_np = self.redimensionar_imagen(self.image_bottom_np, width_top, height_top)
            # Multiplicación de imágenes
            multiplicacion_img = cv.multiply(self.image_top_np,self.image_bottom_np)
            self.result_image = Image.fromarray(multiplicacion_img)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar ambas imágenes primero.")
    
    def operaciones_logicas(self):
        try:
            self.ventana_logica = tk.Toplevel(self.root)
            self.ventana_logica.title("Operaciones Lógicas")
            options = [("AND", self.and_logico),
                       ("OR", self.or_logico),
                       ("XOR", self.xor_logico),
                       ("NOT", self.not_logico)]
            for (text, command) in options:
                button = tk.Button(self.ventana_logica, text=text, command=command)
                button.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def and_logico(self):
        if self.image_top is not None and self.image_bottom is not None:
            # Redimensionar ambas imágenes a las dimensiones de la imagen superior
            height_top, width_top = self.image_top_np.shape[:2]
            self.image_bottom_np = self.redimensionar_imagen(self.image_bottom_np, width_top, height_top)
            and_img = cv.bitwise_and(self.image_top_np,self.image_bottom_np)
            self.result_image = Image.fromarray(and_img)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar ambas imágenes primero.")

    def or_logico(self):
        if self.image_top is not None and self.image_bottom is not None:
            # Redimensionar ambas imágenes a las dimensiones de la imagen superior
            height_top, width_top = self.image_top_np.shape[:2]
            self.image_bottom_np = self.redimensionar_imagen(self.image_bottom_np, width_top, height_top)
            or_img = cv.bitwise_or(self.image_top_np,self.image_bottom_np)
            self.result_image = Image.fromarray(or_img)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar ambas imágenes primero.")

    def xor_logico(self):
        if self.image_top is not None and self.image_bottom is not None:
            # Redimensionar ambas imágenes a las dimensiones de la imagen superior
            height_top, width_top = self.image_top_np.shape[:2]
            self.image_bottom_np = self.redimensionar_imagen(self.image_bottom_np, width_top, height_top)
            xor_img = cv.bitwise_xor(self.image_top_np,self.image_bottom_np)
            self.result_image = Image.fromarray(xor_img)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar ambas imágenes primero.")

    def not_logico(self):
        if self.image_top is not None and self.image_bottom is not None:
            # Redimensionar ambas imágenes a las dimensiones de la imagen superior
            height_top, width_top = self.image_top_np.shape[:2]
            self.image_bottom_np = self.redimensionar_imagen(self.image_bottom_np, width_top, height_top)
            not_img = cv.bitwise_not(self.image_top_np,self.image_bottom_np)
            self.result_image = Image.fromarray(not_img)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar ambas imágenes primero.")

    def aplicar_umbral(self):
        if self.image_top is not None:
            # Pedir al usuario el valor del umbral
            umbral = simpledialog.askinteger("Umbral", "Introduce el valor de umbral (0 a 255):", minvalue=0, maxvalue=255)
            
            if umbral is not None:  # Asegurarse de que el usuario no canceló el diálogo
                # Convertir a escala de grises
                gray_image = cv.cvtColor(self.image_top_np, cv.COLOR_RGB2GRAY)
                
                # Aplicar umbral con el valor proporcionado por el usuario
                _, binary_image = cv.threshold(gray_image, umbral, 255, cv.THRESH_BINARY)
                
                # Convertir el resultado a una imagen PIL y mostrarlo
                self.result_image = Image.fromarray(binary_image)
                self.mostrar_imagen_resultado(self.result_image)
            else:
                messagebox.showinfo("Umbral no aplicado", "No se aplicó umbral ya que se canceló la operación.")
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def operaciones_de_ajuste_de_brillo(self):
        try:
            self.ventana_brillo = tk.Toplevel(self.root)
            self.ventana_brillo.title("Ajustes de Brillo y Contraste")
            options = [("Desplazamiento", self.desplazamiento),
                    ("Expansión", self.expansion),
                    ("Contracción", self.contraccion),
                    ("Ecualización", self.ecualizacion),
                    ("Ecualización Exponencial", self.ecualizacion_exp)]
            for (text, command) in options:
                button = tk.Button(self.ventana_brillo, text=text, command=command)
                button.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Ajustes de brillo aplicados directamente a self.image_top_np
    def contraccion(self):
        if self.image_top_np is not None:
            self.image_top_np = self.ajustar_histograma_contraccion(self.image_top_np)
            self.mostrar_imagen_resultado(Image.fromarray(self.image_top_np))
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def desplazamiento(self):
        if self.image_top_np is not None:
            self.image_top_np = self.ajustar_histograma_desplazamiento(self.image_top_np)
            self.mostrar_imagen_resultado(Image.fromarray(self.image_top_np))
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def expansion(self):
        if self.image_top_np is not None:
            self.image_top_np = self.ajustar_histograma_expansion(self.image_top_np)
            self.mostrar_imagen_resultado(Image.fromarray(self.image_top_np))
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def ecualizacion(self):
        if self.image_top_np is not None:
            self.image_top_np = self.ajustar_histograma_ecualizacion(self.image_top_np)
            self.mostrar_imagen_resultado(Image.fromarray(self.image_top_np))
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def ecualizacion_exp(self):
        if self.image_top_np is not None:
            self.image_top_np = self.ajustar_histograma_ecualizacion_exp(self.image_top_np)
            self.mostrar_imagen_resultado(Image.fromarray(self.image_top_np))
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    # Métodos de procesamiento de imágenes
    def ajustar_histograma_contraccion(self, img):
        F_MAX, F_MIN = np.max(img), np.min(img)
        MAX, MIN = 255, 0
        if F_MAX == F_MIN:
            # Si F_MAX es igual a F_MIN, la imagen es uniforme y no requiere ajuste
            return img
        operacion = (MAX - MIN) / (F_MAX - F_MIN) * (img - F_MIN) + MIN
        return np.clip(operacion, MIN, MAX).astype(np.uint8)

    def ajustar_histograma_expansion(self, img):
        F_MAX, F_MIN = np.max(img), np.min(img)
        MAX, MIN = 255, 0
        if F_MAX == F_MIN:
            # Si F_MAX es igual a F_MIN, la imagen es uniforme y no requiere ajuste
            return img
        operacion = (img - F_MIN) / (F_MAX - F_MIN) * (MAX - MIN) + MIN
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

    def igualar_dimesiones(img_1, img_2):
        if img_1.shape != img_2.shape:
                dimensiones = img_1.shape
                filas = dimensiones[0]
                columnas = dimensiones[1]
                img_2 = cv.resize(img_2, (columnas, filas))
        return img_2

    def redimensionar_imagen(self, imagen, nuevo_ancho, nuevo_alto):
        return cv.resize(imagen, (nuevo_ancho, nuevo_alto), interpolation=cv.INTER_AREA)

    def convertir_gris(self):
        if self.image_top is not None:
            gray_image = cv.cvtColor(self.image_top_np, cv.COLOR_RGB2GRAY)
            self.result_image = Image.fromarray(gray_image)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def histograma(self):
        if self.image_top is not None:
            plt.hist(self.image_top_np.ravel(), bins=256, color='gray', alpha=0.7)
            plt.title('Histograma de la Imagen')
            plt.xlabel('Intensidad')
            plt.ylabel('Número de píxeles')
            plt.grid()
            plt.show()
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def componentes_rgb(self):
        if self.image_top is not None:
            r, g, b = cv.split(self.image_top_np)
            # Mostrar componentes
            plt.figure(figsize=(12, 4))
            plt.subplot(1, 3, 1)
            plt.imshow(r, cmap='Reds')
            plt.title('Componente Rojo')
            plt.axis('off')

            plt.subplot(1, 3, 2)
            plt.imshow(g, cmap='Greens')
            plt.title('Componente Verde')
            plt.axis('off')

            plt.subplot(1, 3, 3)
            plt.imshow(b, cmap='Blues')
            plt.title('Componente Azul')
            plt.axis('off')

            plt.show()
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()