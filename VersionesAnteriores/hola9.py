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
            self.image_bottom_pil = img
            self.image_bottom = ImageTk.PhotoImage(img)

            # Convertir a formato NumPy (uint8) para operaciones con OpenCV
            self.image_bottom_np = np.array(img, dtype=np.uint8)

            # Mostrar la imagen en el segundo espacio (inferior)
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
        self.button = tk.Button(self.ventana_num, text="Aplicar", command=self.aplicar_suma_escalar)
        self.button.pack(pady=10)

    def aplicar_suma_escalar(self):
        try:
            escalar = float(self.entry.get())
            resultado_top = self.image_top_np.astype(np.float32) + escalar
            resultado_bottom = self.image_bottom_np.astype(np.float32) + escalar
            
            resultado_top = np.clip(resultado_top, 0, 255).astype(np.uint8)
            resultado_bottom = np.clip(resultado_bottom, 0, 255).astype(np.uint8)

            self.result_image = Image.fromarray(resultado_top)
            self.mostrar_imagen_resultado(self.result_image)
            self.result_image_bottom = Image.fromarray(resultado_bottom)
            self.mostrar_imagen_resultado(self.result_image_bottom)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido.")

    def resta_escalar(self):
        self.ventana_aritmetica.destroy()
        self.ventana_num = tk.Toplevel(self.root)
        self.ventana_num.title("Resta Escalar")
        self.label = tk.Label(self.ventana_num, text="Introduce un número:")
        self.label.pack(pady=10)
        self.entry = tk.Entry(self.ventana_num)
        self.entry.pack(pady=10)
        self.button = tk.Button(self.ventana_num, text="Aplicar", command=self.aplicar_resta_escalar)
        self.button.pack(pady=10)

    def aplicar_resta_escalar(self):
        try:
            escalar = float(self.entry.get())
            resultado_top = self.image_top_np.astype(np.float32) - escalar
            resultado_bottom = self.image_bottom_np.astype(np.float32) - escalar
            
            resultado_top = np.clip(resultado_top, 0, 255).astype(np.uint8)
            resultado_bottom = np.clip(resultado_bottom, 0, 255).astype(np.uint8)

            self.result_image = Image.fromarray(resultado_top)
            self.mostrar_imagen_resultado(self.result_image)
            self.result_image_bottom = Image.fromarray(resultado_bottom)
            self.mostrar_imagen_resultado(self.result_image_bottom)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido.")

    def multiplicacion_escalar(self):
        self.ventana_aritmetica.destroy()
        self.ventana_num = tk.Toplevel(self.root)
        self.ventana_num.title("Multiplicación Escalar")
        self.label = tk.Label(self.ventana_num, text="Introduce un número:")
        self.label.pack(pady=10)
        self.entry = tk.Entry(self.ventana_num)
        self.entry.pack(pady=10)
        self.button = tk.Button(self.ventana_num, text="Aplicar", command=self.aplicar_multiplicacion_escalar)
        self.button.pack(pady=10)

    def aplicar_multiplicacion_escalar(self):
        try:
            escalar = float(self.entry.get())
            resultado_top = self.image_top_np.astype(np.float32) * escalar
            resultado_bottom = self.image_bottom_np.astype(np.float32) * escalar
            
            resultado_top = np.clip(resultado_top, 0, 255).astype(np.uint8)
            resultado_bottom = np.clip(resultado_bottom, 0, 255).astype(np.uint8)

            self.result_image = Image.fromarray(resultado_top)
            self.mostrar_imagen_resultado(self.result_image)
            self.result_image_bottom = Image.fromarray(resultado_bottom)
            self.mostrar_imagen_resultado(self.result_image_bottom)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido.")

    def redimensionar_imagenes(self):
        if self.image_top_np.shape != self.image_bottom_np.shape:
            # Redimensionar la imagen inferior para que coincida con la superior
            self.image_bottom_np = cv.resize(self.image_bottom_np, (self.image_top_np.shape[1], self.image_top_np.shape[0]))

    def son_imagenes_compatibles(self):
        if self.image_top_np.shape != self.image_bottom_np.shape:
            messagebox.showerror("Error", "Las imágenes deben tener el mismo tamaño y número de canales.")
            return False
        return True

    def suma(self):
        if self.image_top_np is not None and self.image_bottom_np is not None:
            self.redimensionar_imagenes()  # Asegúrate de que las imágenes son del mismo tamaño
            if not self.son_imagenes_compatibles():
                return
            resultado = cv.add(self.image_top_np, self.image_bottom_np)
            self.result_image = Image.fromarray(resultado)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showerror("Error", "Por favor carga ambas imágenes para realizar la suma.")

    def resta(self):
        if self.image_top_np is not None and self.image_bottom_np is not None:
            self.redimensionar_imagenes()  # Asegúrate de que las imágenes son del mismo tamaño
            if not self.son_imagenes_compatibles():
                return
            resultado = cv.subtract(self.image_top_np, self.image_bottom_np)
            self.result_image = Image.fromarray(resultado)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showerror("Error", "Por favor carga ambas imágenes para realizar la resta.")

    def multiplicacion(self):
        if self.image_top_np is not None and self.image_bottom_np is not None:
            self.redimensionar_imagenes()  # Asegúrate de que las imágenes son del mismo tamaño
            if not self.son_imagenes_compatibles():
                return
            resultado = cv.multiply(self.image_top_np, self.image_bottom_np)
            self.result_image = Image.fromarray(resultado)
            self.mostrar_imagen_resultado(self.result_image)
        else:
            messagebox.showerror("Error", "Por favor carga ambas imágenes para realizar la multiplicación.")

    def operaciones_logicas(self):
        messagebox.showinfo("Operaciones Lógicas", "Funcionalidad no implementada aún.")

    def aplicar_umbral(self):
        messagebox.showinfo("Umbralizado", "Funcionalidad no implementada aún.")

    def convertir_gris(self):
        messagebox.showinfo("Convertir a Niveles de Gris", "Funcionalidad no implementada aún.")

    def histograma(self):
        messagebox.showinfo("Histograma", "Funcionalidad no implementada aún.")

    def componentes_rgb(self):
        messagebox.showinfo("Componentes RGB", "Funcionalidad no implementada aún.")

    def ajustes_brillo(self):
        messagebox.showinfo("Ajustes de Brillo", "Funcionalidad no implementada aún.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()