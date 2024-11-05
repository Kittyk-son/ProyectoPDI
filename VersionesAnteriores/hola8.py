import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv

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
        self.file_menu.add_command(label="Cargar Imagen", command=self.load_image)
        self.file_menu.add_separator()
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
            ("Ajustes de Brillo", self.ajustes_brillo)
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

    def load_image(self):
        messagebox.showinfo("Cargar Imagen", "Usa los botones 'Cargar Imagen 1' o 'Cargar Imagen 2'.")

    def load_image_top(self):
        file_path = filedialog.askopenfilename(title="Cargar Imagen 1", filetypes=[("Imágenes", "*.jpg;*.png;*.bmp")])
        if file_path:
            # Cargar la imagen en PIL
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # Redimensionar la imagen para la interfaz

            # Almacenar tanto la imagen PIL como el arreglo NumPy
            self.image_top_pil = img
            self.image_top = ImageTk.PhotoImage(img)

            # Convertir a formato NumPy (uint8) para operaciones con OpenCV
            self.image_top_np = np.array(img, dtype=np.uint8)
            
            # Mostrar la imagen en el primer espacio (superior)
            self.image_frame_top.config(image=self.image_top)
            self.image_frame_top.image = self.image_top  # Guardar referencia de la imagen


    def load_image_bottom(self):
        file_path = filedialog.askopenfilename(title="Cargar Imagen 2", filetypes=[("Imagenes", "*.jpg;*.png;*.bmp")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            self.image_bottom = ImageTk.PhotoImage(img)
            self.image_frame_bottom.config(image=self.image_bottom)
            self.image_frame_bottom.image = self.image_bottom

    def save_image_result(self):
        if self.result_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("BMP Files", "*.bmp")])
            if file_path:
                self.result_image.save(file_path)
                messagebox.showinfo("Guardar Imagen", f"Imagen guardada en {file_path}.")

    def mostrar_imagen_resultado(self, imagen):
        # Redimensionar la imagen a 400x400 píxeles
        imagen_redimensionada = imagen.resize((400, 400), Image.LANCZOS)

        # Convertir la imagen redimensionada a un formato compatible con Tkinter
        result_img_display = ImageTk.PhotoImage(imagen_redimensionada)

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
            print("Error al crear ventana de operaciones aritméticas:", e)


    def suma_escalar(self):
        self.ventana_aritmetica.destroy()
        self.ventana_num = tk.Toplevel(self.root)
        self.ventana_num.title("Suma Escalar")
        self.label = tk.Label(self.ventana_num, text="Introduce un número:")
        self.label.pack(pady=10)
        self.entry = tk.Entry(self.ventana_num)
        self.entry.pack(pady=10)
        self.button = tk.Button(self.ventana_num, text="Aceptar", command=self.obtener_numero)
        self.button.pack(pady=10)

    def obtener_numero(self):
        entrada = self.entry.get()
        try:
            numero = float(entrada)
            self.ventana_num.destroy()
            if self.image_top_np is not None:
                # Convertimos la imagen NumPy al formato que necesita OpenCV
                image_cv2 = self.image_top_np
                
                # Verificar si la imagen es en escala de grises o tiene tres canales
                if len(image_cv2.shape) == 2:
                    # Suma escalar en escala de grises
                    image_result = cv.add(image_cv2, np.full(image_cv2.shape, numero, dtype=np.uint8))
                elif len(image_cv2.shape) == 3 and image_cv2.shape[2] == 4:
                    # Convertimos de RGBA a RGB
                    image_cv2 = cv.cvtColor(image_cv2, cv.COLOR_RGBA2RGB)
                    image_result = cv.add(image_cv2, np.full(image_cv2.shape, numero, dtype=np.uint8))
                else:
                    # Suma escalar en imagen RGB
                    image_result = cv.add(image_cv2, np.full(image_cv2.shape, numero, dtype=np.uint8))
                
                # Redimensionamos la imagen resultado para mostrarla
                image_result_resized = cv.resize(image_result, (400, 400), interpolation=cv.INTER_LINEAR)
                self.result_image = Image.fromarray(image_result_resized)
                self.mostrar_imagen_resultado(self.result_image)
            else:
                messagebox.showwarning("Advertencia", "Debes cargar una imagen primero.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce un número válido.")

    def resta_escalar(self):
        self.ventana_aritmetica.destroy()
        self.get_number_input("Resta Escalar")

    def multiplicacion_escalar(self):
        self.ventana_aritmetica.destroy()
        self.get_number_input("Multiplicación Escalar")

    def suma(self):
        self.ventana_aritmetica.destroy()
        messagebox.showinfo("Operación", "Suma realizada.")

    def resta(self):
        self.ventana_aritmetica.destroy()
        messagebox.showinfo("Operación", "Resta realizada.")

    def multiplicacion(self):
        self.ventana_aritmetica.destroy()
        messagebox.showinfo("Operación", "Multiplicación realizada.")

    def get_number_input(self, operation):
        num = simpledialog.askfloat(operation, f"Ingrese un número para {operation.lower()}:")
        if num is not None:
            messagebox.showinfo(operation, f"{operation} realizada con el valor {num}.")

    def operaciones_logicas(self):
        self.ventana_logica = tk.Toplevel(self.root)
        self.ventana_logica.title("Operaciones Lógicas")
        options = [("AND", self.and_operation),
                   ("OR", self.or_operation),
                   ("XOR", self.xor_operation)]
        for (text, command) in options:
            button = tk.Button(self.ventana_logica, text=text, command=command)
            button.pack(pady=5)

    def and_operation(self):
        self.ventana_logica.destroy()
        messagebox.showinfo("Operación Lógica", "Operación AND realizada.")

    def or_operation(self):
        self.ventana_logica.destroy()
        messagebox.showinfo("Operación Lógica", "Operación OR realizada.")

    def xor_operation(self):
        self.ventana_logica.destroy()
        messagebox.showinfo("Operación Lógica", "Operación XOR realizada.")

    def aplicar_umbral(self):
        umbral = simpledialog.askfloat("Umbral", "Ingrese el valor de umbral:")
        if umbral is not None:
            messagebox.showinfo("Umbral", f"Umbral aplicado con el valor {umbral}.")

    def convertir_gris(self):
        messagebox.showinfo("Convertir a Niveles de Gris", "Imagen convertida a niveles de gris.")

    def histograma(self):
        messagebox.showinfo("Histograma", "Histograma mostrado.")

    def componentes_rgb(self):
        messagebox.showinfo("Componentes RGB", "Componentes RGB mostrados.")

    def ajustes_brillo(self):
        self.ventana_brillo = tk.Toplevel(self.root)
        self.ventana_brillo.title("Ajustes de Brillo")
        options = [("Desplazamiento", self.desplazamiento),
                   ("Expansión del Histograma", self.expansion_histograma),
                   ("Contracción del Histograma", self.contraccion_histograma),
                   ("Ecualización", self.ecualizacion),
                   ("Ecualización Exponencial", self.ecualizacion_exponencial)]
        for (text, command) in options:
            button = tk.Button(self.ventana_brillo, text=text, command=command)
            button.pack(pady=5)

    def desplazamiento(self):
        self.ventana_brillo.destroy()
        messagebox.showinfo("Ajustes de Brillo", "Desplazamiento realizado.")

    def expansion_histograma(self):
        self.ventana_brillo.destroy()
        messagebox.showinfo("Ajustes de Brillo", "Expansión del histograma realizada.")

    def contraccion_histograma(self):
        self.ventana_brillo.destroy()
        messagebox.showinfo("Ajustes de Brillo", "Contracción del histograma realizada.")

    def ecualizacion(self):
        self.ventana_brillo.destroy()
        messagebox.showinfo("Ajustes de Brillo", "Ecualización realizada.")

    def ecualizacion_exponencial(self):
        self.ventana_brillo.destroy()
        messagebox.showinfo("Ajustes de Brillo", "Ecualización exponencial realizada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()