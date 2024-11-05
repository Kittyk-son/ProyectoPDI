import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np

class ImagenApp:
    def __init__(self, root):
        self.root = root
        self.ventana_aritmetica = None
        self.ventana_num = None
        self.label = None
        self.entry = None
        self.button = None

        # Carga una imagen inicial usando OpenCV
        self.imagen = cv2.imread("ruta/a/tu/imagen.jpg")
        self.imagen_original = self.imagen.copy()  # Crear una copia para operaciones

    def suma_escalar(self):
        if self.ventana_aritmetica:
            self.ventana_aritmetica.destroy()

        # Crear nueva ventana
        self.ventana_num = tk.Toplevel(self.root)
        self.ventana_num.title("Operaciones Aritméticas")

        # Etiqueta
        self.label = tk.Label(self.ventana_num, text="Introduce un número:")
        self.label.pack(pady=10)

        # Entrada de número
        self.entry = tk.Entry(self.ventana_num)
        self.entry.pack(pady=10)

        # Botón para enviar
        self.button = tk.Button(self.ventana_num, text="Aceptar", command=self.obtener_numero)
        self.button.pack(pady=10)

    def obtener_numero(self):
        entrada = self.entry.get()
        try:
            # Intenta convertir la entrada a un número
            numero = float(entrada)

            # Realizar la operación de suma escalar
            print(f"Número ingresado: {numero}")

            # Sumar el escalar a la imagen
            imagen_modificada = self.sumar_escalar_imagen(numero)

            # Mostrar la imagen modificada
            cv2.imshow("Imagen Modificada", imagen_modificada)
            cv2.waitKey(0)  # Espera hasta que el usuario presione una tecla
            cv2.destroyAllWindows()

            self.ventana_num.destroy()

        except ValueError:
            # Si no es un número válido, muestra un mensaje de error
            messagebox.showerror("Error", "Por favor, introduce un número válido.")

    def sumar_escalar_imagen(self, numero):
        # Convertir el escalar a un valor de tipo float32 si es necesario
        escalar = np.full(self.imagen_original.shape, numero, dtype="float32")

        # Sumar el escalar a cada píxel de la imagen
        imagen_modificada = cv2.add(self.imagen_original, escalar)

        # Asegurarse de que los valores de los píxeles estén en el rango [0, 255]
        imagen_modificada = np.clip(imagen_modificada, 0, 255).astype("uint8")

        return imagen_modificada

# Inicializar la aplicación de Tkinter
root = tk.Tk()
app = ImagenApp(root)
root.mainloop()
