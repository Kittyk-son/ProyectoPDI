import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import math
import funciones as fun
from scipy import stats
import os

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
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.buttons = [
            ("Operaciones Aritméticas", self.operaciones_aritmeticas),
            ("Operaciones Lógicas", self.operaciones_logicas),
            ("Aplicar Umbralizado", self.aplicar_umbral),
            ("Convertir a Niveles de Gris", self.convertir_gris),
            ("Histograma", self.histograma),
            ("Componentes RGB", self.componentes_rgb),
            ("Ajustes de Brillo", self.operaciones_de_ajuste_de_brillo),
            ("Filtros Paso Bajas",self.operaciones_con_filtro_paso_bajas),
            ("Filtros Paso Altas",self.operaciones_con_filtro)
        ]

        for (text, command) in self.buttons:
            button = tk.Button(self.sidebar, text=text, command=command, width=20, height=2,
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
            while valor_escalar>255 or valor_escalar<0:
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
            self.image_bottom_np=self.igualar_dimesiones(self.image_top_np,self.image_bottom_np)
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
            self.image_bottom_np = self.igualar_dimesiones(self.image_top_np,self.image_bottom_np)
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
        if self.image_top is not None:
            not_img = cv.bitwise_not(self.image_top_np)
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

    def igualar_dimesiones(self,img_1, img_2):
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
    def es_gris(self):
        """
        Determina si una imagen está en escala de grises.
        
        Args:
            img: Imagen en formato numpy array (formato OpenCV)
        
        Returns:
            bool: True si la imagen está en escala de grises, False si es a color o hay error
        """
        try:
            # Verificar que la imagen no esté vacía
            if self.image_top_np is None or self.image_top_np.size == 0:
                print("Error: Imagen vacía o inválida")
                return False
                
            # Obtener la forma (shape) de la imagen
            if len(self.image_top_np.shape) == 2:
                # Si la imagen tiene solo 2 dimensiones, es definitivamente gris
                return True
            elif len(self.image_top_np.shape) == 3:
                # Si tiene 3 dimensiones, verificamos los canales
                if self.image_top_np.shape[2] == 1:
                    # Si solo tiene 1 canal, es gris
                    return True
                elif self.image_top_np.shape[2] == 3:
                    # Si tiene 3 canales, verificamos si todos los canales son iguales
                    # Separamos los canales
                    b, g, r = cv.split(self.image_top_np)
                    # Comparamos si todos los canales son iguales
                    if (b == g).all() and (b == r).all():
                        return True
                    return False
                else:
                    print("Error: Formato de imagen no soportado")
                    return False
            else:
                print("Error: Dimensiones de imagen no válidas")
                return False
                
        except Exception as e:
            print(f"Error al analizar la imagen: {str(e)}")
            return False


    def histograma(self):
        if self.image_top is not None:
            # Para hacer el espaciado uniforme en un rango de 0-255, que va de 3 en 3
            bins = np.arange(0, 256, 3)
            # Creamos la figura
            fig, ax = plt.subplots() 
            if self.es_gris():
                # Histograma para escala de grises con un alineamiento
                ax.hist(self.image_top_np.ravel(), bins=bins, color='gray')
                ax.set_title('Histograma de la imagen en grises')
            else:
                # Histograma de los canales de color
                # Extraer los canales de color 
                canales = cv.split(self.image_top_np) # canales = [b, g, r]
                color = ('b', 'g', 'r') # Para colorearlos
                nombres = ('azul', 'verde', 'rojo')
                for i, col in enumerate(color):
                    # Agregamos al histograma los datos: ravel para volverlo lista de datos, alpha para trasparencia
                    ax.hist(canales[i].ravel(), bins=bins, color=col, alpha=0.5, label=f'Canal {nombres[i]}')
                ax.set_title('Histograma de la imagen en color')
            ax.set_xlabel('Valor de intensidad del pixel')
            ax.set_ylabel('Frecuencia')
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

    def operaciones_con_filtro_paso_bajas(self):
        try:
            self.ventana_filtro = tk.Toplevel(self.root)
            self.ventana_filtro.title("Operaciones con Filtro")
            options = [("Aplicar Ruido Sal y Pimienta", self.ruido_sal_y_pimienta),
                    ("Aplicar Ruido Gaussiano", self.ruido_gaussiano),
                    ("Aplicar Filtro Moda", self.filtro_moda)]
            for (text, command) in options:
                button = tk.Button(self.ventana_filtro, text=text, command=command)
                button.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ruido_sal_y_pimienta(self):
        try:
            self.ventana_sal = tk.Toplevel(self.root)
            self.ventana_sal.title("Operaciones con Filtro")
            options = [("Aplicar Sal", self.sal),
                    ("Aplicar Pimienta", self.pimienta),
                    ("Aplicar Sal y Pimienta", self.sal_y_pimienta)]
            for (text, command) in options:
                button = tk.Button(self.ventana_sal, text=text, command=command)
                button.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def sal(self):
        if self.image_top is not None:
            cantidad = 0.05
            conversion = False
            # Copiar la imagen para no modificar la original
            imagen = np.copy(self.image_top_np)
                
            # Manejar diferentes dimensiones de imagen
            if len(imagen.shape) == 2:
                # Imagen en escala de grises
                pass
            elif len(imagen.shape) == 3:
                    # Imagen a color o grises (en tres canales) - convertir a YUV
                imagen = cv.cvtColor(imagen, cv.COLOR_BGR2YUV)
                conversion = True
            else:
                raise ValueError("Las dimensiones de la imagen no son válidas")
                
            # Obtener las dimensiones de trabajo
            if conversion:
                    altura, ancho = imagen[:,:,0].shape
                    canal_trabajo = imagen[:,:,0]
            else:
                altura, ancho = imagen.shape
                canal_trabajo = imagen
                # Crear máscara de ruido
                # Se hacen valores aleatorios entre 0, 1 y 2, para una máscara del tamaño de la imágen
            mascara = np.random.choice([0, 1, 2], size=(altura, ancho), 
                    p=[1 - cantidad, cantidad/2, cantidad/2])
            # P guarda las probabilidades en que aparecen = [ 1 - cantidad (si cantidad es 5% sería 100% - 5% = 95% de probabilida de que aparezca 0), ... ]
            # Aplicar ruido sal (255) y pimienta (0)
            # Los 0 no aplican, son las que quedan igual
            canal_trabajo[mascara == 1] = 255
            if conversion:
                imagen[:,:,0] = canal_trabajo
                imagen = cv.cvtColor(imagen, cv.COLOR_YUV2BGR)
            # Convertir el resultado de vuelta a imagen PIL y mostrarlo
            self.result_image = Image.fromarray(imagen)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def pimienta(self):
        if self.image_top is not None:
            cantidad = 0.05
            conversion = False
            # Copiar la imagen para no modificar la original
            imagen = np.copy(self.image_top_np)
                
            # Manejar diferentes dimensiones de imagen
            if len(imagen.shape) == 2:
                # Imagen en escala de grises
                pass
            elif len(imagen.shape) == 3:
                    # Imagen a color o grises (en tres canales) - convertir a YUV
                imagen = cv.cvtColor(imagen, cv.COLOR_BGR2YUV)
                conversion = True
            else:
                raise ValueError("Las dimensiones de la imagen no son válidas")
                
            # Obtener las dimensiones de trabajo
            if conversion:
                    altura, ancho = imagen[:,:,0].shape
                    canal_trabajo = imagen[:,:,0]
            else:
                altura, ancho = imagen.shape
                canal_trabajo = imagen
                # Crear máscara de ruido
                # Se hacen valores aleatorios entre 0, 1 y 2, para una máscara del tamaño de la imágen
            mascara = np.random.choice([0, 1, 2], size=(altura, ancho), 
                    p=[1 - cantidad, cantidad/2, cantidad/2])
            # P guarda las probabilidades en que aparecen = [ 1 - cantidad (si cantidad es 5% sería 100% - 5% = 95% de probabilida de que aparezca 0), ... ]
            # Aplicar ruido sal (255) y pimienta (0)
            # Los 0 no aplican, son las que quedan igual
            canal_trabajo[mascara == 2] = 0
            if conversion:
                imagen[:,:,0] = canal_trabajo
                imagen = cv.cvtColor(imagen, cv.COLOR_YUV2BGR)
            # Convertir el resultado de vuelta a imagen PIL y mostrarlo
            self.result_image = Image.fromarray(imagen)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def sal_y_pimienta(self):
        if self.image_top is not None:
            cantidad = 0.05
            conversion = False
            # Copiar la imagen para no modificar la original
            imagen = np.copy(self.image_top_np)
                
            # Manejar diferentes dimensiones de imagen
            if len(imagen.shape) == 2:
                # Imagen en escala de grises
                pass
            elif len(imagen.shape) == 3:
                    # Imagen a color o grises (en tres canales) - convertir a YUV
                imagen = cv.cvtColor(imagen, cv.COLOR_BGR2YUV)
                conversion = True
            else:
                raise ValueError("Las dimensiones de la imagen no son válidas")
                
            # Obtener las dimensiones de trabajo
            if conversion:
                    altura, ancho = imagen[:,:,0].shape
                    canal_trabajo = imagen[:,:,0]
            else:
                altura, ancho = imagen.shape
                canal_trabajo = imagen
                # Crear máscara de ruido
                # Se hacen valores aleatorios entre 0, 1 y 2, para una máscara del tamaño de la imágen
            mascara = np.random.choice([0, 1, 2], size=(altura, ancho), 
                    p=[1 - cantidad, cantidad/2, cantidad/2])
            # P guarda las probabilidades en que aparecen = [ 1 - cantidad (si cantidad es 5% sería 100% - 5% = 95% de probabilida de que aparezca 0), ... ]
            # Aplicar ruido sal (255) y pimienta (0)
            # Los 0 no aplican, son las que quedan igual
            canal_trabajo[mascara == 1] = 255
            canal_trabajo[mascara == 2] = 0
            if conversion:
                imagen[:,:,0] = canal_trabajo
                imagen = cv.cvtColor(imagen, cv.COLOR_YUV2BGR)
            # Convertir el resultado de vuelta a imagen PIL y mostrarlo
            self.result_image = Image.fromarray(imagen)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def ruido_gaussiano(self):
        """
        Agrega ruido gaussiano a una imagen
        
        Args:
            img: Imagen en formato numpy array (OpenCV)
            media: el valor promedio de la distribución (default 0)
            sigma: Proporción de píxeles que serán afectados (default 10%)
        
        Returns:
            Imagen con ruido sal y pimienta
        """
        if self.image_top is not None:
            conversion = False
            media=0
            sigma=simpledialog.askinteger("Establecer Sigma", "Introduce el valor continuo para multiplicar (0 a 100):")
            # Copiar la imagen para no modificar la original
            imagen = np.copy(self.image_top_np)
            
            # Manejar diferentes dimensiones de imagen
            if len(imagen.shape) == 2:
                # Imagen en escala de grises
                pass
            elif len(imagen.shape) == 3:
                # Imagen a color o grises (en tres canales) - convertir a YUV
                imagen = cv.cvtColor(imagen, cv.COLOR_BGR2YUV)
                conversion = True
            else:
                raise ValueError("Las dimensiones de la imagen no son válidas")
            
            # Obtener las dimensiones de trabajo
            if conversion:
                canal_trabajo = imagen[:,:,0]
            else:
                canal_trabajo = imagen
            
            # Aplicamos el ruido gaussiano
            gauss = np.zeros_like(canal_trabajo, dtype=np.uint8)
            cv.randn(gauss, media, sigma)
            canal_trabajo = cv.add(canal_trabajo, gauss)
            
            # Si estamos trabajando en YUV, actualizar el canal Y y convertir de vuelta a BGR
            if conversion:
                imagen[:,:,0] = canal_trabajo
                imagen = cv.cvtColor(imagen, cv.COLOR_YUV2BGR)
            # Convertir el resultado de vuelta a imagen PIL y mostrarlo
            self.result_image = Image.fromarray(imagen)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def filtro_moda(self):
        """
        Aplica el filtro moda a una imagen
        
        Args:
            img: Imagen en formato numpy array (OpenCV)
            Kerne_size: tamaño de un lado del cuadro del cual obtendremos la información para el filtro (default 3)
        
        Returns:
            Imagen con ruido sal y pimienta
        """
        if self.image_top is not None:
            kernel_size=simpledialog.askinteger("Establecer Kernel", "Introduce el valor continuo para multiplicar (0 a 4):")
            conversion = False
            # Copiar la imagen para no modificar la original
            imagen = np.copy(self.image_top_np)
            
            # Manejar diferentes dimensiones de imagen
            if len(imagen.shape) == 2:
                # Imagen en escala de grises
                pass
            elif len(imagen.shape) == 3:
                # Imagen a color o grises (en tres canales) - convertir a YUV
                imagen = cv.cvtColor(imagen, cv.COLOR_BGR2YUV)
                conversion = True
            else:
                raise ValueError("Las dimensiones de la imagen no son válidas")
            
            # Obtener las dimensiones de trabajo
            if conversion:
                altura, ancho = imagen[:,:,0].shape
                canal_trabajo = imagen[:,:,0]
            else:
                altura, ancho = imagen.shape
                canal_trabajo = imagen

            # Creamos una copia para trabajar y evitar que los resultados anteriores afecten al siguiente
            resultado = np.copy(canal_trabajo) 
            
            # Cuantos pixeles necesitamos en cada lado
            pad = kernel_size // 2
            # Se agrega un borde extra para poder trabajar las orillas, en este caso refleja los pixeles.
            imagen_padded = np.pad(canal_trabajo, pad, mode = 'reflect')
            ''' Por ejemplo:
                De esto:
                1 2 3
                4 5 6
                7 8 9

                A esto:
                5 4 5 6 5
                2 1 2 3 2
                5 4 5 6 5
                8 7 8 9 8
                5 4 5 6 5
            '''
            resultado = np.zeros((altura, ancho), dtype=imagen_padded.dtype)
            
            # Muy lento
            # Crear vistas de todas las ventanas de una vez, para crear vistas eficientes de las ventanas
            windows = np.lib.stride_tricks.sliding_window_view(
                imagen_padded, 
                (kernel_size, kernel_size)
            )
            
            # Calcular la moda para cada ventana
            for i in range(altura):
                #print(f'Fila = {i} de {altura}')
                for j in range(ancho):
                    # Obtienes la moda, utiliza keepdims para añadir compatibilidado con versiones recientes de scipy
                    resultado[i,j] = stats.mode(windows[i,j].flatten(), keepdims=True)[0][0] # Sólo queremos el primer valor


            
            # Si estamos trabajando en YUV, actualizar el canal Y y convertir de vuelta a BGR
            if conversion:
                imagen[:,:,0] = resultado
                imagen = cv.cvtColor(imagen, cv.COLOR_YUV2BGR)
                self.result_image = Image.fromarray(imagen)
                self.mostrar_imagen_resultado(self.result_image)
            
            self.result_image = Image.fromarray(resultado)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showwarning("Advertencia", "Cargar una imagen primero.")

    def operaciones_con_filtro(self):
        try:
            self.ventana_filtro = tk.Toplevel(self.root)
            self.ventana_filtro.title("Operaciones con Filtro")
            options = [("Aplicar Ruido Sal y Pimienta", self.ruido_sal_y_pimienta),
                    ("Aplicar Ruido Gaussiano", self.ruido_gaussiano),
                    ("Aplicar Filtro Moda", self.filtro_moda)]
            for (text, command) in options:
                button = tk.Button(self.ventana_filtro, text=text, command=command)
                button.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", str(e))

        

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()