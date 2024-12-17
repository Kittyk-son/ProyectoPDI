"""
Versión: 0.2.3 - Entrega de práctica 3. Añadido la multiumbralización. En sus dos formas, simétrica y asimétrica. Así como se generalizó la función elegir_rango_entero.
Licencia: MIT

Copyright (c) 2024 Bustillos Cruz, López Pérez Fernanda Leonor, Mazariegos Aguilar Julio Darikson, Rodríguez Ramírez Fernanda, Torres Barajas Oscar Uriel.

Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados (el "Software"), para utilizar el Software sin restricción, incluyendo sin limitación los derechos a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar, y/o vender copias del Software, y a permitir a las personas a las que se les proporcione el Software a hacer lo mismo, sujeto a las siguientes condiciones:
El aviso de copyright anterior y este aviso de permiso se incluirán en todas las copias o partes sustanciales del Software.
EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A LAS GARANTÍAS DE COMERCIABILIDAD, IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES O TITULARES DEL COPYRIGHT SERÁN RESPONSABLES DE NINGUNA RECLAMACIÓN, DAÑOS U OTRAS RESPONSABILIDADES, YA SEA EN UNA ACCIÓN DE CONTRATO, AGRAVIO O CUALQUIER OTRA FORMA, QUE SURJA DE O EN CONEXIÓN CON EL SOFTWARE O EL USO U OTRO TIPO DE ACCIONES EN EL SOFTWARE.

Fecha: viernes 29 de Noviembre de 2024
"""


import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import funciones as fnc
import math
from scipy import stats
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from scipy import ndimage

def mostrar_imagen(nombre_salida, img, ruta):
    """
    Muestra una imagen y permite guardarla o cerrar la ventana.
    
    Args:
        nombre_salida (str): Nombre de la ventana
        img: Imagen en formato numpy array (formato OpenCV)
        ruta_destino: Path o string con la ruta base donde guardar
    
    Returns:
        bool: True si la imagen fue guardada, False en caso contrario
    """
    try:
        # Verificar que la imagen no esté vacía
        if img is None or img.size == 0:
            print("Error: Imagen vacía o inválida")
            return False
            
        # Mostrar la imagen
        fnc.reescalar_y_mostrar(img, nombre_salida)
        print("Presiona 's' para guardar la imagen o cualquier otra tecla para salir")
        
        # Esperar por una tecla
        k = cv.waitKey(0) & 0xFF
        
        # Guardar imagen si se presiona 's'
        if k == ord('s'):
            try:
                ruta_destino = ruta / nombre_salida
                
                # Asegurarnos que la ruta tenga extensión válida
                if not str(ruta_destino).lower().endswith(('.png', '.jpg', '.jpeg')):
                    ruta_destino = ruta_destino.with_suffix('.jpg')
                
                # Asegurarnos que el directorio existe
                ruta_destino.parent.mkdir(parents=True, exist_ok=True)
                
                # Guardar la imagen
                guardado = fnc.guardar_imagen(img, str(ruta_destino))
                
                if guardado:
                    print(f"Imagen guardada en: {ruta_destino}")
                else:
                    print("No se pudo guardar la imagen")
                    
            except Exception as e:
                fnc.escribe_el_error(e)
                guardado = False
        else:
            guardado = False
        
        # Cerrar ventanas y limpiar buffer
        cv.destroyAllWindows()
        while cv.waitKey(1) & 0xFF != 255:
            pass
            
        return guardado
        
    except Exception as e:
        fnc.escribe_el_error(e)
        return False

def conversion_a_YUV(img):
    """
    Convierte una imagen a YUV para poder manejar la luminancia por separado.

    Args: 
        img: imagen en BGR y formato numpy array (OpenCV)

    Returns:
        imagen: imagen convertida a YUV
        canal_trabajo: luminancia
        conversion: verificación, si se realizó la conversión
        altura: altura de la imagen
        ancho: ancho de la imagen
    """
    conversion = False
    # Copiar la imagen para no modificar la original
    imagen = np.copy(img)
    
    # Manejar diferentes dimensiones de imagen
    if len(imagen.shape) == 2:
        # Imagen en escala de grises
        pass
    elif len(imagen.shape) == 3:
        # Imagen a color o grises (en tres canales) - convertir a YUV
        imagen = cv.cvtColor(imagen, cv.COLOR_BGR2YUV)
        conversion = True
    else:
        raise ValueError("Las dimensiones de la imagen no son válidas")
    
    # Obtener las dimensiones de trabajo
    if conversion:
        altura, ancho = imagen[:,:,0].shape
        canal_trabajo = imagen[:,:,0]
    else:
        altura, ancho = imagen.shape
        canal_trabajo = imagen

    return imagen, canal_trabajo, conversion, altura, ancho    

def mostrar_canal_color(canal, color, nombre_ventana, ruta_destino):
    """
    Muestra un canal de color en su color correspondiente.
    
    Args:
        canal: Canal individual de la imagen (array 2D)
        color: 'r', 'g', o 'b' para indicar qué canal es
        nombre_ventana: Nombre de la ventana
        ruta_destino: Ruta donde guardar la imagen
    """
    # Crear una imagen en negro (todos los canales en 0)
    zeros = np.zeros_like(canal)
    
    # Crear imagen a color poniendo el canal en su posición correcta
    if color.lower() == 'r':
        img_color = cv.merge([zeros, zeros, canal])  # BGR format
    elif color.lower() == 'g':
        img_color = cv.merge([zeros, canal, zeros])
    elif color.lower() == 'b':
        img_color = cv.merge([canal, zeros, zeros])
    
    # Mostrar la imagen
    mostrar_imagen(nombre_ventana, img_color, ruta_destino)

# Obtener la matriz de la imágen
def leer_matriz(ruta_imagen, nombre_imagen):
    # Intentamos cargar la imagen desde el directorio actual
    img = cv.imread(ruta_imagen / nombre_imagen)
    
    if img is None:
        print(f"No se encontró la imagen en: {ruta_imagen}")
        # Si no se encuentra en el directorio actual, usamos findFile como respaldo
        ruta_opencv = cv.samples.findFile(nombre_imagen)
        print(f"Buscando en rutas de OpenCV: {ruta_opencv}")
        img = cv.imread(ruta_opencv)
    
    if img is None:
        sys.exit("No se pudo leer la imagen en ninguna ubicación.")
    
    return img

def elegir_imagen(lista, imagen_direccion):
    """
    Elige la imágen de la lista y la prepara para su procesamiento
    
    Args:
    lista: nombres de las imágenes con las que podemos operar
    
    Returns:
    Imagen en forma de matriz y su nombre
    """
    # Mostramos la lista de opciones y elegimos una
    imagen_nombre = fnc.menu('imágenes', 'Elige la imagen con la que operar', lista, False)
    # Obtiene la matriz usando open cv en la ruta.
    return leer_matriz(imagen_direccion, imagen_nombre), imagen_nombre

"""
    if k == ord("s"):
        # Guardamos la imagen en el directorio actual
        cv.imwrite(nombre_salida, img)
        print(f"Imagen guardada como: {nombre_salida}")
"""  




def valores_deseados():
    MIN = MAX = None
    while MIN == MAX:
        # Ingresamos los nuevos valores deseados
        _, MIN = fnc.input_validado('Ingresa nuevo valor mínimo deseado (0,255): ', 3, (0,255))
        _, MAX = fnc.input_validado('Ingresa nuevo valor máximo deseado (0,255): ', 3, (0,255))
        if MIN == MAX:
            print('Los valores no pueden ser iguales, vuelve a ingresarlos')

    # Si estan intercambiados entonces cambian
    if MIN > MAX:
        print('El valor mínimo es mayor al máximo, intercarbiando...')
        auxiliar = MIN
        MIN = MAX
        MAX = auxiliar
    return MAX, MIN

    
def histograma(img, imagen_nombre):
    # Para hacer el espaciado uniforme en un rango de 0-255, que va de 3 en 3
    bins = np.arange(0, 256, 3)
    # Creamos la figura
    fig, ax = plt.subplots() 
    if fnc.es_gris(img):
        # Histograma para escala de grises con un alineamiento
        ax.hist(img.ravel(), bins=bins, color='gray')
        ax.set_title('Histograma de la imagen en grises')
    else:
        # Histograma de los canales de color
        # Extraer los canales de color 
        canales = cv.split(img) # canales = [b, g, r]
        color = ('b', 'g', 'r') # Para colorearlos
        nombres = ('azul', 'verde', 'rojo')
        for i, col in enumerate(color):
            # Agregamos al histograma los datos: ravel para volverlo lista de datos, alpha para trasparencia
            ax.hist(canales[i].ravel(), bins=bins, color=col, alpha=0.5, label=f'Canal {nombres[i]}')
        ax.set_title('Histograma de la imagen en color')
    ax.set_xlabel('Valor de intensidad del pixel')
    ax.set_ylabel('Frecuencia')
    fig.canvas.manager.set_window_title(f'{imagen_nombre}')
    plt.show()

def sumar_restar(img):
    escalar = fnc.input_validado('Ingresa el valor (positivo/negativo): ', 1)
    if escalar > 0:
        # Suma un escalar
        sumado_restado = cv.add(img, escalar)
    elif escalar < 0:
        # Resta un escalar
        sumado_restado = cv.subtract(img, escalar)
    else:
        sumado_restado = img
    return sumado_restado, escalar


def multi_escalar(img):
    _, flotante = fnc.input_validado('Ingresa el valor (0.0, 255.0): ', 6, (0, 255))
    multiplicado = cv.multiply(img, flotante)
    return multiplicado, flotante


def operaciones_escalares(imagen_nombre, img, imagenes_ruta):
    opciones = ('Sumar/restar un escalar'
                ,'Multiplicar por un escalar')

    while True:
        eleccion = fnc.menu('Operaciones artméticas', 'Elije el tipo de operación', opciones)
        match(eleccion):
            case 'Salir':
                break
            case 'Sumar/restar un escalar':
                try:
                    sumado_restado, escalar = sumar_restar(img)
                    mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-Sum_Rst_{escalar}', sumado_restado, imagenes_ruta)
                except Exception as e:
                    fnc.escribe_el_error(e)
            case 'Multiplicar por un escalar':
                try:
                    multiplicado, flotante = multi_escalar(img)
                    mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-Multiplicado_Escalar_{flotante}', multiplicado, imagenes_ruta)
                except Exception as e:
                    fnc.escribe_el_error(e)       

def elegir_dos_imagenes(lista_imagenes, imagenes_ruta):
    print('Elige las imágenes con las que operar')
    img_1, nombre_1 = elegir_imagen(lista_imagenes, imagenes_ruta)
    img_2, nombre_2 = elegir_imagen(lista_imagenes, imagenes_ruta)
    print(f'Se operará {nombre_1} con {nombre_2}')
    return img_1, nombre_1, img_2, nombre_2

def igualar_dimesiones(img_1, img_2):
        if img_1.shape != img_2.shape:
                dimensiones = img_1.shape
                filas = dimensiones[0]
                columnas = dimensiones[1]
                img_2 = cv.resize(img_2, (columnas, filas))
        return img_2


def operaciones_imagenes(imagen_nombre, img, imagenes_ruta):
    img_1 = img
    nombre_1 = imagen_nombre
    print()
    print('¡Elije la segunda imágen con la que operar!')
    img_2, nombre_2 = elegir_imagen(lista_imagenes, imagenes_ruta)

    opciones = ('Suma de imágenes'
                ,'Diferencia de imágenes'
                ,'Multiplicación de imágenes'
                ,'Elegir dos imágenes nuevas'
                ,'Elegir la primera imagen'
                ,'Elegir la segunda imagen')

    while True:
        # Asegurarse de que las imágenes tengan el mismo tamaño
        # Asegurar mismo tamaño
        img_2 = igualar_dimesiones(img_1, img_2)

        eleccion = fnc.menu('Operaciones con imágenes', 'Elije el tipo de operación', opciones)
        match(eleccion):  
            case 'Salir':
                break
            case 'Suma de imágenes':
                try:
                    suma = cv.add(img_1, img_2)
                    mostrar_imagen(f'{fnc.quitar_ext(nombre_1)}+{fnc.quitar_ext(nombre_2)}', suma, imagenes_ruta)

                except Exception as e:
                    fnc.escribe_el_error(e)
            case 'Diferencia de imágenes':
                try:
                    resta = cv.subtract(img_1, img_2)
                    mostrar_imagen(f'{fnc.quitar_ext(nombre_1)}-{fnc.quitar_ext(nombre_2)}', resta, imagenes_ruta)

                except Exception as e:
                    fnc.escribe_el_error(e)
            case 'Multiplicación de imágenes':
                try:
                    # Los valores de píxeles están en el rango 0-255
                    # Al multiplicar dos imágenes, los valores resultantes estarían en el rango 0-65025 (255*255)
                    # Dividir por 255 devuelve los valores al rango 0-255 que es el estándar para imágenes
                    multiplicacion = cv.multiply(img_1, img_2, scale=1.0/255.0)
                    mostrar_imagen(f'{fnc.quitar_ext(nombre_1)}*{fnc.quitar_ext(nombre_2)}', multiplicacion, imagenes_ruta)

                except Exception as e:
                    fnc.escribe_el_error(e)

            case 'Elegir dos imágenes nuevas':
                try:
                    img_1, nombre_1, img_2, nombre_2 = elegir_dos_imagenes(lista_imagenes, imagenes_ruta)
                except Exception as e:
                    fnc.escribe_el_error(e)
            case 'Elegir la primera imagen':
                try:
                    print()
                    print('¡Elije la primera imágen con la que operar!')
                    img_1, nombre_1 = elegir_imagen(lista_imagenes, imagenes_ruta)
                except Exception as e:
                    fnc.escribe_el_error(e)
            case 'Elegir la segunda imagen':
                try:
                    print()
                    print('¡Elije la segunda imágen con la que operar!')
                    img_2, nombre_2 = elegir_imagen(lista_imagenes, imagenes_ruta)
                except Exception as e:
                    fnc.escribe_el_error(e)


def operaciones_aritmeticas(imagen_nombre, img, imagenes_ruta):
    opciones = ('Escalares'
                ,'Con imágenes')

    
    eleccion = fnc.menu('Operaciones artméticas', 'Elije el tipo de operación', opciones, False)
    
    match (eleccion):
        case 'Escalares':
            try:
                operaciones_escalares(imagen_nombre, img, imagenes_ruta)
            except Exception as e:
                fnc.escribe_el_error(e)
        case 'Con imágenes':
            try:
                operaciones_imagenes(imagen_nombre, img, imagenes_ruta)
            except Exception as e:
                fnc.escribe_el_error(e)


def operaciones_logicas(imagen_nombre, img, imagenes_ruta):

    img_1 = img
    nombre_1 = imagen_nombre
    img_2 = None
    nombre_2 = None

    opciones = ('NOT'
                ,'AND'
                ,'OR'
                ,'XOR'
                ,'Elegir dos imágenes nuevas'
                ,'Elegir la primera imagen'
                ,'Elegir la segunda imagen')

    while True:
        
        eleccion = fnc.menu('Operaciones con imágenes', 'Elije el tipo de operación', opciones)

        print('Antes de hacer el in')
        if img_2 is None and eleccion in ('AND', 'OR', 'XOR'):
            print()
            print('¡Elije la segunda imágen con la que operar!')
            img_2, nombre_2 = elegir_imagen(lista_imagenes, imagenes_ruta)
        print('Después de hacer el in')

        print('Antes de igualar')
        # Asegurarse de que las imágenes tengan el mismo tamaño
        # Asegurar mismo tamaño
        try:
            if img_2 is not None:
                img_2 = igualar_dimesiones(img_1, img_2)
        except Exception as e:
            fnc.escribe_el_error(e)


        match(eleccion):  
            case 'Salir':
                break
            case 'NOT':
                try:
                    _not = cv.bitwise_not(img_1)
                    mostrar_imagen(f'{fnc.quitar_ext(nombre_1)}_NOT', _not, imagenes_ruta)

                except Exception as e:
                    fnc.escribe_el_error(e)
            case 'AND':
                try:
                    print('Entrando en AND')
                    _and = cv.bitwise_and(img_1, img_2)
                    print('Después de hacer el AND')
                    mostrar_imagen(f'{fnc.quitar_ext(nombre_1)}_AND_{fnc.quitar_ext(nombre_2)}', _and, imagenes_ruta)

                except Exception as e:
                    fnc.escribe_el_error(e)
            case 'OR':
                try:
                    _or = cv.bitwise_or(img_1, img_2)
                    mostrar_imagen(f'{fnc.quitar_ext(nombre_1)}_OR_{fnc.quitar_ext(nombre_2)}', _or, imagenes_ruta)

                except Exception as e:
                    fnc.escribe_el_error(e)
            case 'XOR':
                try:
                    
                    _xor = cv.bitwise_xor(img_1, img_2)
                    mostrar_imagen(f'{fnc.quitar_ext(nombre_1)}_XOR_{fnc.quitar_ext(nombre_2)}', _xor, imagenes_ruta)

                except Exception as e:
                    fnc.escribe_el_error(e)

            case 'Elegir dos imágenes nuevas':
                try:
                    img_1, nombre_1, img_2, nombre_2 = elegir_dos_imagenes(lista_imagenes, imagenes_ruta)
                except Exception as e:
                    fnc.escribe_el_error(e)

            case 'Elegir la primera imagen':
                try:
                    print()
                    print('¡Elije la primera imágen con la que operar!')
                    img_1, nombre_1 = elegir_imagen(lista_imagenes, imagenes_ruta)
                except Exception as e:
                    fnc.escribe_el_error(e)

            case 'Elegir la segunda imagen':
                try:
                    print()
                    print('¡Elije la segunda imágen con la que operar!')
                    img_2, nombre_2 = elegir_imagen(lista_imagenes, imagenes_ruta)
                except Exception as e:
                    fnc.escribe_el_error(e)

# Se generaliza elegir un rango
def elegir_rango_entero(Nombre_variable, lim_inf, lim_sup):
    elegir = False
    while not elegir:
        # Si es correcto elegir sería TRUE y, por tanto, lo negamos para ya no tener que elegir.
        elegir, variable = fnc.input_validado(f'{Nombre_variable}: ', 3, (lim_inf, lim_sup))
    return variable


def binarizacion(imagen_nombre, img, imagenes_ruta):
    # Convertir imagen a escala de grises
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    umbral = elegir_rango_entero('Umbral', 0, 255)
    # Hacer la umbralización con el umbral dado
    _, threshold_img = cv.threshold(gray_img, umbral, 255, cv.THRESH_BINARY)
    mostrar_imagen(fnc.quitar_ext(imagen_nombre)+ f'_Binarizacion{umbral}', threshold_img, imagenes_ruta )

    while True:
        # Elección nos devuelve True si decimos que si, y False si no.
        if fnc.eleccion('¿Quieres intentar con otro umbral?'):
            umbral = elegir_rango_entero('Umbral', 0, 255)
            # Hacer la umbralización con el umbral dado
            _, threshold_img = cv.threshold(gray_img, umbral, 255, cv.THRESH_BINARY)
            mostrar_imagen(fnc.quitar_ext(imagen_nombre)+ f'_Binarizacion{umbral}', threshold_img, imagenes_ruta )
        else:
            break


def intervalo_valores(umbrales):
    """
    Calcula el intervalo unitario y los valores correspondientes para dividir una imagen en categorías basadas en umbrales.
    
    Parámetros:
        umbrales (int): Número de umbrales para dividir la imagen.
    
    Retorna:
        intervalo (int): Tamaño de cada intervalo.
        valores (list): Lista de valores asignados a cada intervalo.
    """
    
    # Se crean las categorías, es decir, en cuántos intervalos se dividirá nuestra imagen
    categorias = umbrales + 1
    # Calculamos el intervalo unitario automáticamente
    intervalo = 255 // categorias  # Uso de división entera para evitar decimales
    
    # Obtenemos el factor que se usará para obtener los valores correspondientes a cada intervalo
    factor = 255 // umbrales
    # Ahora creamos la lista para los valores que tendrán cada una de nuestras divisiones
    valores = [i * factor for i in range(categorias)]

    # Nos aseguramos que el último rango tenga el valor máximo
    if valores[umbrales] != 255:
        valores[umbrales] = 255

    print(f"Valores: {valores}")
    
    return intervalo, valores

def simetrico(img, umbrales):
    """
    Aplica una segmentación simétrica a una imagen basada en umbrales especificados.
    
    Parámetros:
        img (numpy.ndarray): Imagen en formato BGR.
        umbrales (int): Número de umbrales para dividir la imagen.
    
    Retorna:
        numpy.ndarray: Imagen resultante después de la segmentación.
    """
    # Convertimos la imagen al formato YUV y obtenemos información crucial
    imagen, canal_trabajo, conversion, _, _ = conversion_a_YUV(img)
    
    intervalo, valores = intervalo_valores(umbrales)
    # Ahora creamos el mapa para cambiar los valores de nuestra imagen
    mapa = np.zeros(256, dtype=np.uint8)  # Usamos enteros
    inicio = 0
    # Para cada valor que le corresponde a un intervalo
    for i, valor in enumerate(valores):
        # Automáticamente cada umbral es el intervalo 
        umbral = intervalo * (i + 1)
        # Si el valor es mayor al umbral es que nos hemos quedado cortos
        if valor > umbral or umbral > 255: # Aseguramos que el último sea 255
            umbral = 255
        # Asignamos directamente el valor escalar a todo el rango
        print(f'Asignando el valor {valor} al umbral {umbral}')
        mapa[inicio:umbral + 1] = valor
        inicio = umbral + 1

    # Mapeamos la imagen, cada píxel que llevará a su valor nuevo.
    resultado = mapa[canal_trabajo]
    
    if conversion:
        imagen[:, :, 0] = resultado
        resultado = cv.cvtColor(imagen, cv.COLOR_YUV2BGR)
    
    return resultado

def asimetrico(img, umbrales):
    """
    Aplica una segmentación asimétrica a una imagen basada en umbrales elegidos por el usuario.
    
    Parámetros:
        img (numpy.ndarray): Imagen en formato BGR.
        umbrales (int): Número máximo de umbrales a elegir.
    
    Retorna:
        numpy.ndarray: Imagen resultante después de la segmentación.
    """
    # Convertimos la imagen al formato YUV y obtenemos información crucial
    imagen, canal_trabajo, conversion, _, _ = conversion_a_YUV(img)
    intervalos = []

    print('\nElije el valor de los umbrales.')
    # Vamos agregando cada umbral como un intervalo
    for i in range(umbrales):
        umbral = elegir_rango_entero(f'Umbral [{i + 1}]', 1, 254)
        # Para no repetirlos
        if umbral not in intervalos:
            intervalos.append(umbral)
    
    # Puede que nos los hayan dado desordenados
    intervalos.sort()
    print(f"Los intervalos son {intervalos}")
    # Los umbrales son todos los que están en intervalos, no necesariamente el mismo número de los elegidos al inicio
    umbrales = len(intervalos)
    _, valores = intervalo_valores(umbrales)
    
    # Ahora creamos el mapa para cambiar los valores de nuestra imagen
    mapa = np.zeros(256, dtype=np.uint8)  # Usamos enteros
    inicio = 0 
    # Recorremos cada umbral y asignamos los valores correspondientes
    for i, umbral in enumerate(intervalos):
        umbral = min(umbral, 255)  # Aseguramos que no exceda 255
        mapa[inicio:umbral + 1] = valores[i]
        inicio = umbral + 1
    # Asignamos el último rango (n+1 valor)
    mapa[inicio:] = valores[-1]

    # Mapeamos la imagen, cada píxel que llevará a su valor nuevo.
    resultado = mapa[canal_trabajo]
    
    if conversion:
        imagen[:, :, 0] = resultado
        resultado = cv.cvtColor(imagen, cv.COLOR_YUV2BGR)
    
    return resultado, str(intervalos)





def multiumbralizado(imagen_nombre, img, imagenes_ruta):
    print('\nIngresa el número de umbrales.')
    umbrales = elegir_rango_entero('Umbrales', 1, 254)

    opciones = ('Simétrico (automático)'
                ,'Asimétrico (manual)'
                ,'Cambiar número de umbrales')

    while True:
        eleccion = fnc.menu('Umbralizado', 'Elije el tipo de operación', opciones)

        match(eleccion):  
                case 'Salir':
                    break
                case 'Simétrico (automático)':
                    try:
                        umbralado = simetrico(img, umbrales)
                        mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-MLT_UMBDO_SIM_U{umbrales}', umbralado, imagenes_ruta)
                    except Exception as e:
                        fnc.escribe_el_error(e)
                case 'Asimétrico (manual)':
                    try:
                        umbralado, u_finales = asimetrico(img, umbrales)
                        mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-MLT_UMBDO_ASIM_U{u_finales}', umbralado, imagenes_ruta)
                    except Exception as e:
                        fnc.escribe_el_error(e)

                case 'Cambiar número de umbrales':
                    try:
                        print('Ingresa el número de umbrales')
                        umbrales = elegir_rango_entero('Umbrales', 1, 254)
                    except Exception as e:
                        fnc.escribe_el_error(e)


def umbralizado(imagen_nombre, img, imagenes_ruta):
    opciones = ('Binarizacion'
                ,'Multiumbralizado')

    while True:
        eleccion = fnc.menu('Umbralizado', 'Elije el tipo de operación', opciones)

        match(eleccion):  
                case 'Salir':
                    break
                case 'Binarizacion':
                    try:
                        binarizacion(imagen_nombre, img, imagenes_ruta)
                    except Exception as e:
                        fnc.escribe_el_error(e)
                case 'Multiumbralizado':
                    try:
                        multiumbralizado(imagen_nombre, img, imagenes_ruta)
                    except Exception as e:
                        fnc.escribe_el_error(e)






def desplazamiento(img):
    """
    Desplaza el histograma de una imagen, ya sea en escala de grises o color.
    
    Args:
        img: Imagen en formato numpy array (OpenCV)
    
    Returns:
        Imagen con el histograma expandido
    """
    
    desp = fnc.input_validado('¿Cuánto quieres desplazar? ', 1)
    if desp > 0:
        # Suma un escalar
        desplazado = cv.add(img, desp)
    elif desp < 0:
        # Resta un escalar
        desplazado = cv.subtract(img, desp)
    else:
        desplazado = img
    return desplazado , desp

def expansion(img):
    """
    Expande el histograma de una imagen, ya sea en escala de grises o color.
    
    Args:
        img: Imagen en formato numpy array (OpenCV)
    
    Returns:
        Imagen con el histograma expandido
    """
    # Verificar si la imagen es en escala de grises
    if len(img.shape) == 2:
        # Imagen ya está en escala de grises
        imagen = img
    # Para operar usamos YUV porque es más eficiente y evita el problema de realizar las operaciones en tres canales
    # Si es imagen a color, usamos el espacio YUV 
    elif len(img.shape) == 3:
        # Convertir de BGR a YUV
        img_yuv = cv.cvtColor(img, cv.COLOR_BGR2YUV)
        
        # Ecualizaremos el canal Y (luminancia)
        imagen = img_yuv[:,:,0]

    # Obtenemos los valores que necesitamos para la operación
    F_MAX = np.max(imagen)
    F_MIN = np.min(imagen)
    # Verificamos que no exista división por cero
    if F_MAX == F_MIN:
        print("La imágen es de un sólo matiz (color), no es posible hacer la expansión")
        return img
    
    # Ingresamos el nuevo rango deseado
    MAX, MIN = valores_deseados()

    
    # Operación vectorizada de numpy, dado que open cv la usa al obtener la imagen la podemos ocupar
    # Esto se realiza píxel por píxel
    operacion = (imagen - F_MIN) / (F_MAX - F_MIN) * (MAX - MIN) + MIN

    # El resultado de esta operación es float, así que la redondeamos
    # Primero con clip limitamos el rango y con astype redondeamos los float
    img_yuv[:,:,0] = np.clip(operacion, MIN, MAX).astype(np.uint8)

    # Convertimos de vuelta a BGR
    return cv.cvtColor(img_yuv, cv.COLOR_YUV2BGR)



def contraccion(img):
    """
    Contrae el histograma de una imagen, ya sea en escala de grises o color.
    
    Args:
        img: Imagen en formato numpy array (OpenCV)
    
    Returns:
        Imagen con el histograma expandido
    """
    # Verificar si la imagen es en escala de grises
    if len(img.shape) == 2:
        # Imagen ya está en escala de grises
        imagen = img
    # Para operar usamos YUV porque es más eficiente y evita el problema de realizar las operaciones en tres canales
    # Si es imagen a color, usamos el espacio YUV 
    elif len(img.shape) == 3:
        # Convertir de BGR a YUV
        img_yuv = cv.cvtColor(img, cv.COLOR_BGR2YUV)
        
        # Ecualizaremos el canal Y (luminancia)
        imagen = img_yuv[:,:,0]

    # Obtenemos los valores que necesitamos para la operación
    F_MAX = np.max(imagen)
    F_MIN = np.min(imagen)
    # Verificamos que no exista división por cero
    if F_MAX == F_MIN:
        print("La imágen es de un sólo matiz (color), no es posible hacer la contracción")
        return img
    
    # Ingresamos el nuevo rango deseado
    MAX, MIN = valores_deseados()

    # Operación vectorizada de numpy, dado que open cv la usa al obtener la imagen la podemos ocupar
    # Esto se realiza píxel por píxel
    operacion = (MAX - MIN) / (F_MAX - F_MIN) * (imagen - F_MIN) + MIN

    # El resultado de esta operación es float, así que la redondeamos
    # Primero con clip limitamos el rango y con astype redondeamos los float
    img_yuv[:,:,0] = np.clip(operacion, MIN, MAX).astype(np.uint8)

    # Convertimos de vuelta a BGR
    return cv.cvtColor(img_yuv, cv.COLOR_YUV2BGR)



def e_exponencial(img):
    """
    Ecualiza el histograma de una imagen, ya sea en escala de grises o color.
    
    Args:
        img: Imagen en formato numpy array (OpenCV)
    
    Returns:
        Imagen ecualizada por el método exponencial
    """
    conversion = False
    # Si la imagen está en dos dimensiones entonces aplicamos directamente el filtro.
    if len(img.shape) == 2:
        imagen = np.copy(img)
        
    # Si es de tres dimensiones, usamos el espacio YUV 
    # Para operar usamos YUV porque es más eficiente y evita el problema de realizar las operaciones en tres canales
    elif len(img.shape) == 3:
        # Convertir de BGR a YUV
        img_yuv = cv.cvtColor(img, cv.COLOR_BGR2YUV)
        # Ecualizaremos el canal Y (luminancia)
        imagen = img_yuv[:,:,0]
        # Para verificar
        conversion = True
    else:
        raise ValueError("Las dimensiones de la imagen no son válidos")

    # Obtenemos los valores que necesitamos para la operación
    G_MIN = np.min(imagen)
    ALFA = np.var(imagen) # ALFA es la varianza
    # Calculamos P(g), un arreglo con las frecuencias acumuladas
    total_pixeles = imagen.size # Primero debemos saber los píxeles totales
    # Con el histograma tendremos las frecuencias con las que cada pixel aparece.
    histograma = cv.calcHist([imagen], [0], None, [256], [0, 256])
    # Para calcular las probabilidades, el histograma lo convertiremos en un arreglo de una dimensión con ravel.
    # Las probabilidades son calculadas (con operaciones vectorizadas de numpy) de la forma P(x)=casos_favorables/casos_posibles
    probabilidades = histograma.ravel() / total_pixeles
    # Para obtener la frecuencia acumulada, cumsum es suma acumulada, es decir para cada i suma desde la posición 0 hasta i 
    lista_frec_acumulada = np.cumsum(probabilidades)

    # Creamos el mapa de transformación
    mapa = np.zeros(256, dtype=np.float32) # Usamos float32 para los cálculos
    
    # Evitamos el logaritmo de cero agregando un pequeño epsilon
    epsilon = 1e-10 # Esto es 0.0000000001
    for i, Pg_g in enumerate(lista_frec_acumulada):
        # Limitamos Pg_g a un valor máximo menor que 1
        Pg_g = min(Pg_g, 1 - epsilon)
        mapa[i] = G_MIN - (1/ALFA) * math.log(1 - Pg_g) # 1 - 1 = 0 podría llevar al logaritmo a la indeterminación
    # Mapeamos la imagen, cada píxel será como el índice que llevará a su valor nuevo.
    ecualizacion = mapa[imagen]

    # El resultado de esta operación es float, así que la redondeamos
    # Primero con clip limitamos el rango y con astype redondeamos los float
    resultado = np.clip(ecualizacion, 0, 255).astype(np.uint8)

    # Si hicimos la conversión la volvemos a cambiar.
    if conversion:
        img_yuv[:,:,0] = resultado
        # Convertimos de vuelta a BGR
        return cv.cvtColor(img_yuv, cv.COLOR_YUV2BGR)
    else:
        return resultado


def ecualizar_imagen(img):
    """
    Ecualiza el histograma de una imagen, ya sea en escala de grises o color.
    
    Args:
        img: Imagen en formato numpy array (OpenCV)
    
    Returns:
        Imagen ecualizada
    """
    try:
        # Verificar si la imagen es en escala de grises
        if len(img.shape) == 2:
            # Imagen ya está en escala de grises
            return cv.equalizeHist(img)
        # Para operar usamos YUV porque es más eficiente y evita el problema de realizar las operaciones en tres canales
        # Si es imagen a color, ecualizar en espacio YUV
        elif len(img.shape) == 3:
            # Convertir de BGR a YUV
            img_yuv = cv.cvtColor(img, cv.COLOR_BGR2YUV)
            
            # Ecualizar el canal Y (luminancia)
            img_yuv[:,:,0] = cv.equalizeHist(img_yuv[:,:,0])
            
            # Convertir de vuelta a BGR
            return cv.cvtColor(img_yuv, cv.COLOR_YUV2BGR)
            
    except Exception as e:
        print(f"Error al ecualizar la imagen: {str(e)}")
        return img  # Retornar imagen original si hay error


def ajuste_brillo(imagen_nombre, img):
    opciones = ('Desplazamiento'
                ,'Expansión del histograma'
                ,'Contracción del histograma'
                ,'Ecualización'
                ,'Ecualización exponencial')
    # Elegimos el tipo de ajuste
    eleccion = fnc.menu('Ajuste de brillo', 'Elije el tipo de ajuste', opciones, False)
    match eleccion:
        case 'Desplazamiento':
            try:
                desplazado, desp = desplazamiento(img)
                mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-Desplazamiento{desp}', desplazado, imagenes_ruta)
            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Expansión del histograma':
            try:
                expandido = expansion(img)
                mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-Expansion', expandido, imagenes_ruta)
            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Contracción del histograma':
            try:
                contraido = contraccion(img)
                mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-Contraccion', contraido, imagenes_ruta)
            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Ecualización':
            try:
                ecualizada = ecualizar_imagen(img)

                mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-Ecualizada', ecualizada, imagenes_ruta)

            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Ecualización exponencial':
            try:
                exponencial = e_exponencial(img)
                mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-Exponencial', exponencial, imagenes_ruta)
            except Exception as e:
                fnc.escribe_el_error(e)

#------------------------------------------------------------------------------------------------------------
# Funciones de ruido
#------------------------------------------------------------------------------------------------------------


def agregar_ruido_sal_pimienta(img, cantidad=0.05):
    """
    Agrega ruido sal y pimienta a una imagen
    
    Args:
        img: Imagen en formato numpy array (OpenCV)
        cantidad: Proporción de píxeles que serán afectados (default 0.05 = 5%)
    
    Returns:
        Imagen con ruido sal y pimienta
    """
    # Convertimos la imagen al formato YUV y obtenemos información crucial
    imagen, canal_trabajo, conversion, altura, ancho = conversion_a_YUV(img)

    # Crear máscara de ruido
    # Se hacen valores aleatorios entre 0, 1 y 2, para una máscara del tamaño de la imágen
    mascara = np.random.choice([0, 1, 2], size=(altura, ancho), 
            p=[1 - cantidad, cantidad/2, cantidad/2])
    # P guarda las probabilidades en que aparecen = [ 1 - cantidad (si cantidad es 5% sería 100% - 5% = 95% de probabilida de que aparezca 0), ... ]

    # Aplicar ruido sal (255) y pimienta (0)
    # Los 0 no aplican, son las que quedan igual
    if fnc.eleccion('¿Quieres aplicar los dos tipos de ruido?'):
        canal_trabajo[mascara == 1] = 255  # Sal
        canal_trabajo[mascara == 2] = 0    # Pimienta
        extension = 'SP'
    elif fnc.eleccion('¿Quieres aplicar el ruido sal?'):
        canal_trabajo[mascara == 1] = 255  # Sal
        extension = 'Sal'
    else:
        print('Aplicando ruido pimienta')
        canal_trabajo[mascara == 2] = 0    # Pimienta
        extension = 'Pmnta'
    
    # Si estamos trabajando en YUV, actualizar el canal Y y convertir de vuelta a BGR
    if conversion:
        imagen[:,:,0] = canal_trabajo
        imagen = cv.cvtColor(imagen, cv.COLOR_YUV2BGR)
    
    return imagen, int(cantidad*100), extension


def agregar_ruido_gaussiano(img, media = 0, sigma = 10):
    """
    Agrega ruido gaussiano a una imagen
    
    Args:
        img: Imagen en formato numpy array (OpenCV)
        media: el valor promedio de la distribución (default 0)
        sigma: Proporción de píxeles que serán afectados (default 10%)
    
    Returns:
        Imagen con ruido sal y/o pimienta
    """

    # Convertimos la imagen al formato YUV y obtenemos información crucial
    imagen, canal_trabajo, conversion, _, _ = conversion_a_YUV(img)
    
    # Aplicamos el ruido gaussiano
    gauss = np.zeros_like(canal_trabajo, dtype=np.uint8)
    cv.randn(gauss, media, sigma)
    canal_trabajo = cv.add(canal_trabajo, gauss)
    
    # Si estamos trabajando en YUV, actualizar el canal Y y convertir de vuelta a BGR
    if conversion:
        imagen[:,:,0] = canal_trabajo
        imagen = cv.cvtColor(imagen, cv.COLOR_YUV2BGR)
    
    return imagen, sigma



def filtro_moda(img, kernel_size = 3):
    """
    Aplica el filtro moda a una imagen
    
    Args:
        img: Imagen en formato numpy array (OpenCV)
        Kerne_size: tamaño de un lado del cuadro del cual obtendremos la información para el filtro (default 3)
    
    Returns:
        Imagen con ruido sal y pimienta
    """

    # Convertimos la imagen al formato YUV y obtenemos información crucial
    imagen, canal_trabajo, conversion, altura, ancho = conversion_a_YUV(img)

    # Creamos una copia para trabajar y evitar que los resultados anteriores afecten al siguiente
    resultado = np.copy(canal_trabajo) 
    
    # Cuantos pixeles necesitamos en cada lado
    pad = kernel_size // 2
    # Se agrega un borde extra para poder trabajar las orillas, en este caso refleja los pixeles.
    imagen_padded = np.pad(canal_trabajo, pad, mode = 'reflect')
    ''' Por ejemplo:
        De esto:
        1 2 3
        4 5 6
        7 8 9

        A esto:
        5 4 5 6 5
        2 1 2 3 2
        5 4 5 6 5
        8 7 8 9 8
        5 4 5 6 5
    '''
    resultado = np.zeros((altura, ancho), dtype=imagen_padded.dtype)
    
    # Muy lento
    # Crear vistas de todas las ventanas de una vez, para crear vistas eficientes de las ventanas
    windows = np.lib.stride_tricks.sliding_window_view(
        imagen_padded, 
        (kernel_size, kernel_size)
    )
    
    # Calcular la moda para cada ventana
    for i in range(altura):
        print(f'Fila = {i} de {altura}')
        for j in range(ancho):
            # Obtienes la moda, utiliza keepdims para añadir compatibilidado con versiones recientes de scipy
            resultado[i,j] = stats.mode(windows[i,j].flatten(), keepdims=True)[0][0] # Sólo queremos el primer valor


    
    # Si estamos trabajando en YUV, actualizar el canal Y y convertir de vuelta a BGR
    if conversion:
        imagen[:,:,0] = resultado
        imagen = cv.cvtColor(imagen, cv.COLOR_YUV2BGR)
        return imagen
    
    return resultado


def ruidos(img, imagenes_ruta):
    opciones = ('Añadir ruido sal y pimienta'
                ,'Añadir ruido gaussiano'
                ,'Filtro moda'
                )

    while True:              
        # Elegimos el tipo de ajuste
        eleccion = fnc.menu('Ruidos', 'Elije lo que deseas hacer', opciones)
        match eleccion:
            case 'Salir':
                break
            case 'Añadir ruido sal y pimienta':
                try:
                    if fnc.eleccion('¿Quieres elegir el porcenaje de ruido?'):
                        valido = False
                        while not valido:
                            valido, porcentaje = fnc.input_validado('Porcentaje', 6, (0, 1))
                        con_SP, percent, ext = agregar_ruido_sal_pimienta(img, porcentaje)
                    else:
                        con_SP, percent, ext  = agregar_ruido_sal_pimienta(img)
                    mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-R_{ext}_{percent}', con_SP, imagenes_ruta)
                except Exception as e:
                    fnc.escribe_el_error(e)
            case 'Añadir ruido gaussiano':
                try:
                    if fnc.eleccion('¿Quieres elegir la cantidad de ruido?'):
                        valido = False
                        while not valido:
                            valido, sigma = fnc.input_validado('Ruido (desviación estándar)', 3, (0, 255))
                        con_gauss, varianza = agregar_ruido_gaussiano(img, sigma = sigma)
                    else:
                        con_gauss, varianza  = agregar_ruido_gaussiano(img)
                        
                    mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-R_Gauss_{varianza}', con_gauss, imagenes_ruta)
                except Exception as e:
                    fnc.escribe_el_error(e)
            case 'Filtro moda':
                try:
                    if fnc.eleccion('¿Quieres elegir el tamaño del kernel?'):
                        valido = False
                        while not valido:
                            valido, kernel = fnc.input_validado('Tamaño en celdas del kernel', 3, (0, max(img.shape)))
                            # Validar que kernel_size sea impar
                            if kernel % 2 == 0:
                                print('El kernel debe ser impar')
                                valido = False
                        f_moda = filtro_moda(img,  kernel)
                    else:
                        f_moda = filtro_moda(img)
                        
                    mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-F_Moda', f_moda, imagenes_ruta)
                except Exception as e:
                    fnc.escribe_el_error(e)

def robert(img):
    """
    Aplica el filtro Robert a una imagen, de manera que se marcan los bordes. Muy rápido pero sensible a 

    Args: imagen en color o en gris

    Returns: imagen en escala de grises con los bordes marcados.
    """
    # Convertimos a gris para sólo detectar los bordes
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Convertimos la imagen al formato YUV y obtenemos información crucial
    imagen, canal_trabajo, conversion, _, _ = conversion_a_YUV(gris)
    
    # Declaramos las dos máscaras que pasarán por toda la imágen con una convolución
    roberts_cross_v = np.array( [[1, 0 ],
                                [0,-1 ]] )
    
    roberts_cross_h = np.array( [[ 0, 1 ],
                                [ -1, 0 ]] )
    
    # Para realizar operaciones sobre el canal, lo transformamos a float
    canal_float = canal_trabajo.astype('float64')
    # Normalizamos en un rango de [0,1], si el pixel es negro entonces 255/255 = 1, y así todos los valores menores.
    canal_float/=255.0

    # Realizamos la convolución (es decir aplicar la máscara en cada pixel según sus vecinos)
    vertical = ndimage.convolve( canal_float, roberts_cross_v )
    horizontal = ndimage.convolve( canal_float, roberts_cross_h )
    
    # Ahora obtenermos el módulo del vector gradiente, que nos indica qué tanto cambian los píxeles de alrededor
    edged_img = np.sqrt( np.square(horizontal) + np.square(vertical))

    # Los volvemos a su valor original.
    edged_img*=255
    
    # Primero con clip limitamos el rango y con astype redondeamos los float
    resultado = np.clip(edged_img, 0, 255).astype(np.uint8)

    if conversion:
        imagen[:,:,0] = resultado
        resultado = cv.cvtColor(imagen, cv.COLOR_YUV2BGR)
        return resultado

    return resultado


def bordes(img, imagenes_ruta):
    bordeado = robert(img)
    mostrar_imagen(fnc.quitar_ext(imagen_nombre)+f'-Robert', bordeado, imagenes_ruta)


#=============================================================================================================
#                                          === MAIN ===
#=============================================================================================================

# try:
# Obtenemos la ruta del directorio actual donde se está ejecutando el script
directorio_actual = os.getcwd()
print(f"Directorio de trabajo actual: {directorio_actual}")

# Obtenemos las imágenes 
imagenes_ruta = fnc.imagenes_Dir()

# Ahora recuperamos la lista de las imágenes con las que operar
lista_imagenes = fnc.listar_archivos(imagenes_ruta)

# Para elegir la imágen estándar
img, imagen_nombre = elegir_imagen(lista_imagenes, imagenes_ruta)
print(f'Se operará con: {imagen_nombre}')
# except Exception as e:
#     print(f"Ocurrió un error al: {str(e)}")

# Repite el menú
while True:
    opciones = ('Elegir imágen'
                ,'Mostrar imagen'
                ,'Operaciones ariméticas'
                ,'Operaciones lógicas'
                ,'Umbralizado'
                ,'Conversión a escala de grises'
                ,'Obtención del histograma'
                ,'Extracción de componentes espectrales (RGB)'
                ,'Ajuste de brillo'
                ,'Imprimir matriz'
                ,'Añadir/quitar ruidos'
                ,'Detección de bordes (Robert)'
                )

    # Función menú
    eleccion = fnc.menu('Menú', 'Elección', opciones)
    #Seleccionando
    match(eleccion):
        case 'Salir':
            break

        case 'Elegir imágen':
            try:
                # Ahora recuperamos la lista de las imágenes con las que operar
                lista_imagenes = fnc.listar_archivos(imagenes_ruta)
                img, imagen_nombre = elegir_imagen(lista_imagenes, imagenes_ruta)
                print(f'Se operará con: {imagen_nombre}')
            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Mostrar imagen': #Mostrar imágenes originales
            try:
                mostrar_imagen(imagen_nombre, img, imagenes_ruta)

            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Operaciones ariméticas': # Operaciones ariméticas
            try:
                operaciones_aritmeticas(imagen_nombre, img, imagenes_ruta)  
            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Operaciones lógicas': # Operaciones lógicas
            try:
                operaciones_logicas(imagen_nombre, img, imagenes_ruta) 
            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Umbralizado': # Umbralizado
            try:
                umbralizado(imagen_nombre, img, imagenes_ruta)
            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Conversión a escala de grises': # Conversión a escala de grises
            try:
                # Convertir imagen a escala de grises
                gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                # Mostrar resultados
                mostrar_imagen(fnc.quitar_ext(imagen_nombre)+'_Gris', gray_img, imagenes_ruta)
            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Obtención del histograma': # Obtención del histograma
            try:
                histograma(img, imagen_nombre)
            except Exception as e:
                fnc.escribe_el_error(e)
                
        case 'Extracción de componentes espectrales (RGB)': # Extracción de componentes espectrales (RGB)
            try:
                # Extraer los canales de color
                b, g, r = cv.split(img)

                # Mostrar los canales en su color correspondiente
                mostrar_canal_color(r, 'r', 'Canal Rojo', imagenes_ruta)
                mostrar_canal_color(g, 'g', 'Canal Verde', imagenes_ruta)
                mostrar_canal_color(b, 'b', 'Canal Azul', imagenes_ruta)
            except Exception as e:
                fnc.escribe_el_error(e)
        case 'Ajuste de brillo': # Ajuste de brillo
            try:
                # LLamamos a la función especializada para no saturar de código
                ajuste_brillo(imagen_nombre, img)
            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Imprimir matriz': 
            try:
                fnc.imprimir_matriz(img, imagen_nombre)
            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Añadir/quitar ruidos': 
            try:
                ruidos(img, imagenes_ruta)
            except Exception as e:
                fnc.escribe_el_error(e)

        case 'Detección de bordes (Robert)': 
            try:
                bordes(img, imagenes_ruta)
            except Exception as e:
                fnc.escribe_el_error(e)

            
        case _:
            print('No hubo match')




