import tkinter as tk
from tkinter import messagebox

# Función que calcula el doble del valor ingresado y cierra la ventana
def calcular_y_cerrar():
    try:
        valor = float(entrada.get())  # Obtiene el valor ingresado
        doble = valor * 2
        messagebox.showinfo("Resultado", f"El doble es: {doble}")  # Muestra el resultado en una ventana emergente
        ventana.destroy()  # Cierra la ventana automáticamente después de mostrar el resultado
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa un número válido.")  # Muestra un error si no es un número

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de Dobles")

# Etiqueta para el título
titulo = tk.Label(ventana, text="Ingresa un valor para calcular su doble:")
titulo.pack(pady=10)

# Campo de entrada
entrada = tk.Entry(ventana)
entrada.pack(pady=10)

# Botón para calcular y cerrar la ventana
boton = tk.Button(ventana, text="Calcular y Cerrar", command=calcular_y_cerrar)
boton.pack(pady=10)

# Iniciar la interfaz gráfica
ventana.mainloop()
