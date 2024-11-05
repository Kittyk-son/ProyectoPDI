import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes")
        self.root.geometry("1024x768")
        self.root.state('zoomed')  # Maximizar la ventana

        # Colores personalizados
        self.bg_color = "#4d4d4d"  # Fondo oscuro
        self.button_color = "#33c1bd"  # Color botones
        self.sidebar_bg_color = "#2e8378"  # Color barra lateral
        self.button_hover_color = "#28a7a1"  # Color hover botones
        self.menu_bg_color = "#57b67b"  # Color menú Archivo

        # Fondo de la ventana principal
        self.root.config(bg=self.bg_color)

        # Crear barra de menú superior
        self.menu_bar = tk.Menu(self.root, bg=self.menu_bg_color, fg="white")
        self.root.config(menu=self.menu_bar)

        # Menú "Archivo"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, bg=self.menu_bg_color, fg="white")
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Cargar Imagen", command=self.load_image)
        self.file_menu.add_command(label="Guardar Imagen", command=self.save_image)
        self.file_menu.add_command(label="Guardar Imagen como", command=self.save_image_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=self.root.quit)

        # Crear barra lateral izquierda con los botones
        self.sidebar = tk.Frame(self.root, width=200, bg=self.bg_color)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        # Botones en la barra lateral
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

        # Crear el área de visualización de imágenes
        self.display_area = tk.Frame(self.root, bg="white")
        self.display_area.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Área izquierda dividida en dos partes para mostrar imágenes
        self.left_area = tk.Frame(self.display_area, bg="white")
        self.left_area.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Botón para cargar la primera imagen (parte superior)
        self.image_button_top = tk.Button(self.left_area, text="Cargar Imagen 1", command=self.load_image_top,
                                          bg=self.button_color, fg="white", font=("Arial", 10, "bold"))
        self.image_button_top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Área para mostrar la primera imagen (parte superior)
        self.image_frame_top = tk.Label(self.left_area, bg="white", text="Imagen 1")
        self.image_frame_top.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Botón para cargar la segunda imagen (parte inferior)
        self.image_button_bottom = tk.Button(self.left_area, text="Cargar Imagen 2", command=self.load_image_bottom,
                                             bg=self.button_color, fg="white", font=("Arial", 10, "bold"))
        self.image_button_bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Área para mostrar la segunda imagen (parte inferior)
        self.image_frame_bottom = tk.Label(self.left_area, bg="white", text="Imagen 2")
        self.image_frame_bottom.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Área derecha para mostrar el resultado de la operación
        self.right_area = tk.Label(self.display_area, bg="white", text="Resultado")
        self.right_area.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Variables para almacenar las imágenes cargadas
        self.image_top = None
        self.image_bottom = None

    # Funciones para las operaciones del menú
    def load_image(self):
        messagebox.showinfo("Cargar Imagen", "Usa los botones 'Cargar Imagen 1' o 'Cargar Imagen 2'.")

    def load_image_top(self):
        # Cargar una imagen en el área superior
        file_path = filedialog.askopenfilename(title="Cargar Imagen 1", filetypes=[("Imagenes", "*.jpg;*.png;*.bmp")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # Redimensionar imagen para que encaje en la interfaz
            self.image_top = ImageTk.PhotoImage(img)

            # Mostrar imagen en el primer espacio (superior)
            self.image_frame_top.config(image=self.image_top)
            self.image_frame_top.image = self.image_top  # Guardar referencia de la imagen

    def load_image_bottom(self):
        # Cargar una imagen en el área inferior
        file_path = filedialog.askopenfilename(title="Cargar Imagen 2", filetypes=[("Imagenes", "*.jpg;*.png;*.bmp")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((400, 400))  # Redimensionar imagen para que encaje en la interfaz
            self.image_bottom = ImageTk.PhotoImage(img)

            # Mostrar imagen en el segundo espacio (inferior)
            self.image_frame_bottom.config(image=self.image_bottom)
            self.image_frame_bottom.image = self.image_bottom  # Guardar referencia de la imagen

    def save_image(self):
        messagebox.showinfo("Guardar Imagen", "Imagen guardada correctamente.")

    def save_image_as(self):
        file_path = filedialog.asksaveasfilename(title="Guardar Imagen como", filetypes=[("Imagenes", "*.jpg;*.png;*.bmp")])
        if file_path:
            messagebox.showinfo("Guardar Imagen como", f"Imagen guardada en: {file_path}")

    # Botones del menú lateral
    def operaciones_aritmeticas(self):
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
    
    def suma_escalar(self):
        self.ventana_aritmetica.destroy()
        self.get_number_input("Suma Escalar")

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

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()