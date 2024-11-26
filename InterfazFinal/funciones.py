import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import math

def input_validado(texto, opcion, limites=None):
    # Inicializamos tkinter y ocultamos la ventana principal
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter

    while True:
        match(opcion):
            case 1:  # Validar número entero
                try:
                    variable = simpledialog.askinteger("Entrada", texto)
                    if variable is not None:  # Si el usuario no cancela
                        return variable
                    else:
                        print(">>> Entrada cancelada")
                        break
                except ValueError:
                    print(">>> ¿Es número entero?")

            case 2:  # Validar número float
                try:
                    variable = simpledialog.askfloat("Entrada", texto)
                    if variable is not None:
                        return variable
                    else:
                        print(">>> Entrada cancelada")
                        break
                except ValueError:
                    print(">>> ¿Es número decimal?")

            case 3:  # Validar número entero dentro de un rango
                variable = input_validado(texto, 1)
                if variable is None:  # Cancelación
                    print(">>> Entrada cancelada")
                    break
                elif limites[0] <= variable <= limites[1]:
                    return True, variable
                else:
                    print(">>> No está dentro del rango")

            case 4:  # Validar texto no vacío
                t = simpledialog.askstring("Entrada", texto)
                if t is None:
                    print(">>> Entrada cancelada")
                    break
                elif bool(t.strip()):
                    return t
                else:
                    print(">>> No puede ser vacío")

            case 5:  # Validar nombres, con primeras letras y caracteres específicos
                nombre = input_validado(texto, 4)
                if nombre is None:
                    print(">>> Entrada cancelada")
                    break
                elif not nombre[0].isalpha():
                    print(">>> El primer caracter debe ser letra")
                elif all(c.isalnum() or c == ' ' for c in nombre):
                    return nombre
                else:
                    print(">>> ¿Es alfanumérico o contiene espacios?")

            case 6:  # Validar número decimal dentro de un rango
                variable = input_validado(texto, 2)
                if variable is None:
                    print(">>> Entrada cancelada")
                    break
                elif limites[0] <= variable <= limites[1]:
                    return True, variable
                else:
                    print(">>> No está dentro del rango")

    # Cerramos la instancia de tkinter al finalizar
    root.destroy()

def sumar_restar(img):
    escalar = input_validado("Suma/Resta Escalar", "Introduce el valor escalar (0 a 255):", 1)
    if escalar > 0:
        # Suma un escalar
        sumado_restado = cv.add(img, escalar)
    elif escalar < 0:
        # Resta un escalar
        sumado_restado = cv.subtract(img, escalar)
    else:
        sumado_restado = img
    return sumado_restado, escalar

