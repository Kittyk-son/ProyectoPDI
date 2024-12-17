import cv2 as cv
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import traceback
import numpy as np
import cv2 as cv

def imprimir_matriz(matriz, nombre="Matriz", max_elementos=150, espaciado=3):
    """
    Imprime una matriz de manera elegante y controlada.
    
    Args:
    matriz: La matriz a imprimir (numpy array)
    max_elementos: Número máximo de elementos totales para usar formato bonito
    nombre: Nombre identificativo para la matriz
    espaciado: Número de espacios para la indentación
    
    Returns:
    None
    """
    # Obtenemos las dimensiones y el total de elementos
    dimensiones = matriz.shape
    total_elementos = np.prod(dimensiones)
    
    # Creamos el espaciado para la indentación
    indent = " " * espaciado
    
    # Imprimimos la información básica
    print(f"\n{nombre}:")
    print(f"{indent}Dimensiones: {dimensiones}")
    print(f"{indent}Tipo de datos: {matriz.dtype}")
    print(f"{indent}Total elementos: {total_elementos}")
    
    # Decidimos el método de impresión basado en el tamaño
    if total_elementos <= max_elementos:
        # Impresión bonita para matrices pequeñas
        print(f"{indent}Contenido:")
        
        # Manejamos diferentes dimensiones
        if len(dimensiones) == 1:  # Vector 1D
            print(indent, end="")
            for i in range(dimensiones[0]):
                print(f"{matriz[i]:3}", end=" ")
            print()  # Nueva línea al final
            
        elif len(dimensiones) == 2:  # Matriz 2D
            for i in range(dimensiones[0]):
                print(indent, end="")
                for j in range(dimensiones[1]):
                    print(f"{matriz[i, j]:3}", end=" ")
                print()
                
        elif len(dimensiones) == 3:  # Matriz 3D (como imágenes a color)
            canales = ('azul', 'green', 'red')
            for k in range(dimensiones[2]):
                print(f"{indent}Canal {canales[k]}:")
                for i in range(dimensiones[0]):
                    print(indent, end="")
                    for j in range(dimensiones[1]):
                        print(f"{matriz[i, j, k]:3}", end=" ")
                    print()
                if k < dimensiones[2] - 1:  # Si no es el último canal
                    print()
    else:
        # Para matrices grandes, usamos el print normal de numpy
        print(f"{indent}Contenido (formato resumido debido al tamaño):")
        print(matriz)

def eleccion(Pregunta):
    while True:
        choice = input(f"\n{Pregunta} (s/n)\nR: ")
        if (choice.upper() == 'S' or choice.upper() == 'N'):
            if choice.upper() == 'S':
                return True
            elif choice.upper() == 'N':
                return False
        print('>>>Opción inválida, intenta otra vez.')


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

def quitar_ext(nombre_extension):
    """
    Quita la última extensión de archivo

    Args: 
        nombre_extension (String): Cadena de texo a la que quitar la extensión
        
    Returns:
        String: Cadena sin el punto y texto después

    Examples:
        >>>quitar_ext('Hola.png')
        Hola
        >>>quitar_ext('Hola.tar.zip')
        Hola.tar
    """
    if '.' not in nombre_extension:
        print('El nombre no tiene extensión que quitar')
    else:
        for i, letra in enumerate(nombre_extension[::-1]): # Recorremos en nombre de atrás para adelante
            # i sigue yendo de 0 a n así que lo normalizamos
            j = -1 + (-1*i)
            if letra == '.':
                # Devolvemos la imágen sin la extensión
                return nombre_extension[:j]
    return nombre_extension


# Función para validar las entradas.
def input_validado(texto, opcion, limites = None):
    while True:
        match(opcion):
            case 1:
                try:
                    # Validar números
                    variable = int(input(texto)) 
                    return variable
                except ValueError:
                    print(">>>¿Es número?>>>")
            case 2:
                try: # Validar float 
                    variable = float(input(texto)) 
                    return variable
                except ValueError:
                    print(">>>¿Es número?>>>")
            case 3: # Validar rangos int
                variable = input_validado(texto + f'({limites[0]}-{limites[1]}): ', 1)
                if(limites[0] <= variable <= limites[1]):
                    return True, variable
                else:
                    print(f">>>No esta dentro del rango ({limites[0]}, {limites[1]})")
                    return False, variable
            case 4: # Validar texto: no vacío
                #Quitamos saltos de línea y espacios con strip y luego lo convertimos a bool para saber si está vacío o no. Si no está vacío devuelve True.
                t = input(texto)
                if(bool(t.strip())):
                    return t
                else:
                    print(">>>No puede ser vacío")
            case 5: # Validar nombres
                Nombre = input_validado(texto,4) 
                if not(Nombre[0].isalpha()):
                    print(">>>El primer caracter debe ser letra")
                elif all(c.isalnum() or ' ' for c in Nombre):
                    # print(">>>Entrada correcta...")
                    return Nombre
                else:
                    print(">>>¿Es alfanumérico?")

            case 6: # Validar rangos float
                variable = input_validado(texto + f'({limites[0]}-{limites[1]}): ', 2)
                if(limites[0] <= variable <= limites[1]):
                    return True, variable
                else:
                    print(f">>>No esta dentro del rango ({limites[0]}, {limites[1]})")
                    return False, variable

# Función para crear un menú, con una opción para salir por defecto
def menu(texto_titulo, texto_eleccion, lista_opciones, salida = True):
    valido = False
    # Mientra no elijas un imput válido
    while not valido:
        i = 1
        # Imprime el título
        print(f"\n----------< {texto_titulo.upper()} >----------")
        # Imprime las opciones
        for opcion in lista_opciones:
            print(f'{i}. {opcion}')
            i+=1
        if salida:
            print('0. Salir')
            # Valida la elección de la elección
            rango = (0, i-1)
        else:
            rango = (1, i-1)
        valido, eleccion = input_validado(f"{texto_eleccion}:\nR: ", 3, rango)
    # Devuelve lo que eligió 
    return lista_opciones[eleccion-1] if eleccion!=0 else 'Salir'

def imagenes_Dir():
    current_directory = Path.cwd()
    folder_name = 'img'
    target_folder = current_directory / folder_name
    if not target_folder.exists():
        target_folder.mkdir()
        print(f"La carpeta ha sido creada: {target_folder}")
        
    return target_folder


def listar_archivos(ruta):
    """
    Lista todos los archivos en una carpeta (no incluye subcarpetas).
    
    Args:
        ruta (str): Ruta a la carpeta que se quiere examinar
        
    Returns:
        list: Lista de nombres de archivos con sus extensiones
    """
    # Convertimos la ruta a objeto Path
    carpeta = Path(ruta)
    
    # Verificamos que la carpeta existe
    if not carpeta.exists():
        raise ValueError(f"La ruta {ruta} no existe")
    
    # Verificamos que es una carpeta
    if not carpeta.is_dir():
        raise ValueError(f"{ruta} no es una carpeta")
        
    # Listamos solo archivos (no carpetas)
    archivos = [archivo.name for archivo in carpeta.iterdir() if archivo.is_file()]
    
    return archivos


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

def guardar_imagen(img, ruta_destino):
    """
    Guarda una imagen en la ruta especificada.
    
    Args:
        img: Imagen en formato numpy array (OpenCV)
        ruta_destino: Path o string con la ruta donde guardar
    
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    try:
        ruta_destino = Path(ruta_destino)
        
        # Asegurarse que la extensión sea válida
        if not str(ruta_destino).lower().endswith(('.png', '.jpg', '.jpeg')):
            ruta_destino = ruta_destino.with_suffix('.png')
        
        # Crear directorio si no existe
        ruta_destino.parent.mkdir(parents=True, exist_ok=True)
        
        # Guardar imagen
        success = cv.imwrite(str(ruta_destino), img)
        
        if success:
            print(f"Imagen guardada exitosamente en: {ruta_destino}")
        else:
            print(f"Error al guardar la imagen en: {ruta_destino}")
        
        return success
        
    except Exception as e:
        print(f"Error al guardar la imagen: {str(e)}")
        return False


def escribe_el_error(e):
    # Obtiene información detallada de la excepción
    tb = traceback.format_exc() # Información completa del error
    print("Se ha producido un error:")
    print(tb) # Muestra la traza completa del error

    # Extrae la última línea de la traza para identificar la línea exacta
    linea_error = traceback.extract_tb(e.__traceback__)[-1]
    print(f"El error ocurrió en la línea {linea_error.lineno}")