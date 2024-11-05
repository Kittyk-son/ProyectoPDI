import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

def suma_escalar(self):
    """Crear la ventana para pedir un número al usuario"""
    self.ventana_aritmetica.destroy()

    # Crear nueva ventana para solicitar el número
    self.ventana_num = tk.Toplevel(self.root)
    self.ventana_num.title("Suma Escalar")

    # Etiqueta
    self.label = tk.Label(self.ventana_num, text="Introduce un número:")
    self.label.pack(pady=10)

    # Entrada de número
    self.entry = tk.Entry(self.ventana_num)
    self.entry.pack(pady=10)

    # Botón para aceptar el número
    self.button = tk.Button(self.ventana_num, text="Aceptar", command=self.obtener_numero)
    self.button.pack(pady=10)

def obtener_numero(self):
    """Obtener el número ingresado y aplicar la suma escalar a la imagen cargada"""
    entrada = self.entry.get()
    
    try:
        # Convertir la entrada a número flotante
        numero = float(entrada)

        # Si es un número válido, destruir la ventana de entrada
        self.ventana_num.destroy()

        # Verificar que haya una imagen cargada en la parte superior izquierda (Imagen 1)
        if self.image_top is not None:
            # Convertir la imagen de PIL a formato OpenCV
            image_cv2 = np.array(self.image_top)

            # Verificar si tiene 4 canales (RGBA) y convertirla a RGB si es necesario
            if image_cv2.shape[2] == 4:
                image_cv2 = cv2.cvtColor(image_cv2, cv2.COLOR_RGBA2RGB)

            # Realizar la operación de suma escalar usando OpenCV
            image_result = cv2.add(image_cv2, np.full(image_cv2.shape, numero, dtype=np.uint8))

            # Redimensionar la imagen resultante a 400x400 píxeles
            image_result_resized = cv2.resize(image_result, (400, 400), interpolation=cv2.INTER_LINEAR)

            # Convertir la imagen resultante a formato PIL
            self.result_image = Image.fromarray(image_result_resized)

            # Mostrar la imagen resultante en el área de resultado (derecha)
            self.mostrar_imagen_resultado(self.result_image)

        else:
            # Si no hay una imagen cargada, mostrar mensaje de advertencia
            messagebox.showwarning("Advertencia", "Debes cargar una imagen primero.")

    except ValueError:
        # Si no es un número válido, mostrar mensaje de error
        messagebox.showerror("Error", "Por favor, introduce un número válido.")


def mostrar_imagen_resultado(self, imagen):
    """Función para mostrar la imagen en el área derecha de la interfaz (en self.result_label)"""
    # Redimensionar la imagen a 400x400 píxeles
    imagen_redimensionada = imagen.resize((400, 400), Image.ANTIALIAS)

    # Convertir la imagen redimensionada a un formato compatible con Tkinter
    result_img_display = ImageTk.PhotoImage(imagen_redimensionada)

    # Mostrar la imagen en el área de resultados (label o canvas en la parte derecha)
    self.result_label.config(image=result_img_display)
    self.result_label.image = result_img_display  # Guardar referencia para evitar que se recolecte por el garbage collector

    # Habilitar el botón de guardar si no estaba habilitado
    self.save_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()