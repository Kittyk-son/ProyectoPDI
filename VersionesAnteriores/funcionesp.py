import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import funciones2 as fnc
import math

def es_gris(img):
    """
    Determina si una imagen está en escala de grises.
    
    Args:
        img: Imagen en formato numpy array (formato OpenCV)
    
    Returns:
        bool: True si la imagen está en escala de grises, False si es a color o hay error
    """
    try:
        # Verificar que la imagen no esté vacía
        if img is None or img.size == 0:
            print("Error: Imagen vacía o inválida")
            return False
            
        # Obtener la forma (shape) de la imagen
        if len(img.shape) == 2:
            # Si la imagen tiene solo 2 dimensiones, es definitivamente gris
            return True
        elif len(img.shape) == 3:
            # Si tiene 3 dimensiones, verificamos los canales
            if img.shape[2] == 1:
                # Si solo tiene 1 canal, es gris
                return True
            elif img.shape[2] == 3:
                # Si tiene 3 canales, verificamos si todos los canales son iguales
                # Separamos los canales
                b, g, r = cv.split(img)
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
    
def reescalar_y_mostrar(img, nombre_ventana, tamano_minimo=500):
    """
    Reescala una imagen si es menor al tamaño mínimo y la muestra.
    
    Args:
        img: Imagen en formato numpy array (OpenCV)
        nombre_ventana: Nombre para la ventana de visualización
        tamano_minimo: Tamaño mínimo deseado en píxeles
    
    Returns:
        numpy.ndarray: Imagen reescalada o la original si no necesita reescalado
    """
    altura, anchura = img.shape[:2]
    
    # Verificar si necesita reescalado
    if altura < tamano_minimo or anchura < tamano_minimo:
        # Calcular ratio manteniendo proporción
        ratio = tamano_minimo / min(altura, anchura)
        nueva_altura = int(altura * ratio)
        nueva_anchura = int(anchura * ratio)
        
        # Reescalar
        img = cv.resize(img, (nueva_anchura, nueva_altura), 
                        interpolation=cv.INTER_AREA)
    
    # Mostrar imagen
    cv.imshow(nombre_ventana, img)
    
    return img