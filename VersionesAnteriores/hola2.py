import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes")
        self.root.geometry("1024x768")  # Inicializar con una ventana grande
        self.root.state('zoomed')  # Maximizar la ventana

        # Crear barra de menú superior
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Menú "Archivo"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Cargar Imagen", command=self.load_image)
        self.file_menu.add_command(label="Guardar Imagen", command=self.save_image)
        self.file_menu.add_command(label="Guardar Imagen como", command=self.save_image_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=self.root.quit)

        # Crear barra lateral izquierda con los botones
        self.sidebar = tk.Frame(self.root, width=200, bg='#f0f0f0')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Crear botones en la barra lateral
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
            button = tk.Button(self.sidebar, text=text, command=command, width=25, height=2)
            button.pack(pady=5)

    # Funciones para las operaciones del menú
    def load_image(self):
        file_path = filedialog.askopenfilename(title="Cargar Imagen", filetypes=[("Imagenes", "*.jpg;*.png;*.bmp")])
        if file_path:
            messagebox.showinfo("Cargar Imagen", f"Imagen cargada: {file_path}")

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
        options = [("AND", self.operacion_and), 
                   ("OR", self.operacion_or), 
                   ("XOR", self.operacion_xor)]
        for (text, command) in options:
            button = tk.Button(self.ventana_logica, text=text, command=command)
            button.pack(pady=5)
    
    def operacion_and(self):
        self.ventana_logica.destroy()
        messagebox.showinfo("Operación Lógica", "Operación AND realizada.")

    def operacion_or(self):
        self.ventana_logica.destroy()
        messagebox.showinfo("Operación Lógica", "Operación OR realizada.")

    def operacion_xor(self):
        self.ventana_logica.destroy()
        messagebox.showinfo("Operación Lógica", "Operación XOR realizada.")
    
    def aplicar_umbral(self):
        threshold = simpledialog.askfloat("Umbral", "Ingrese un valor para el umbral:")
        if threshold is not None:
            messagebox.showinfo("Umbral", f"Umbral aplicado con valor {threshold}.")

    def convertir_gris(self):
        messagebox.showinfo("Convertir a Niveles de Gris", "Conversión realizada.")

    def histograma(self):
        messagebox.showinfo("Histograma", "Histograma generado.")

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
