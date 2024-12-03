import cv2
import numpy as np
from matplotlib import pyplot as plt

# Cargar la imagen
image_path = "OSCURA.jpg"  # Cambia a la ruta de tu imagen
image = cv2.imread(image_path)

# Ajustar brillo y contraste
alpha = 2.0  # Contraste
beta = 50    # Brillo
bright_contrast = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

# Convertir a escala de grises
gray = cv2.cvtColor(bright_contrast, cv2.COLOR_BGR2GRAY)

# Aplicar filtro para reducir ruido
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Binarización (umbral adaptativo)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY_INV, 11, 2)

# Operaciones morfológicas para reforzar las letras
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Encontrar contornos
contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Crear una copia de la imagen original para colorear
colored_image = bright_contrast.copy()

# Dibujar contornos con un color (rojo en este ejemplo)
for contour in contours:
    # Generar un color aleatorio para cada letra
    color = tuple(np.random.randint(0, 255, 3).tolist())
    cv2.drawContours(colored_image, [contour], -1, color, thickness=cv2.FILLED)

# Mostrar la imagen con las letras coloreadas
cv2.imshow("Letras Coloreadas", colored_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Guardar la imagen coloreada si es necesario
output_path = "letras_coloreadas.jpg"
cv2.imwrite(output_path, colored_image)
