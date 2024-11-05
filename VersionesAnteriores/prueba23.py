import tkinter as tk
from tkinter import messagebox

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Suma Escalar")
        
        # Etiqueta de instrucción
        self.label = tk.Label(root, text="Introduce un número:")
        self.label.pack(pady=10)

        # Entrada de número
        self.entry = tk.Entry(root)
        self.entry.pack(pady=10)

        # Botón para enviar
        self.button = tk.Button(root, text="Aceptar", command=self.obtener_numero)
        self.button.pack(pady=10)

    def obtener_numero(self):
        # Obtiene el valor de la entrada
        entrada = self.entry.get()
        
        try:
            # Intenta convertir la entrada a un número
            numero = float(entrada)
            # Si es válido, aquí puedes usarlo para la operación que necesites
            print(f"Número ingresado: {numero}")
            messagebox.showinfo("Resultado", f"El número es {numero}")

        except ValueError:
            # Si no es un número válido, muestra un mensaje de error
            messagebox.showerror("Error", "Por favor, introduce un número válido.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
