import cv2
import numpy as np

# Utwórz testowy obraz 800x600 biały z czarnymi liniami
img = np.ones((600, 800, 3), dtype=np.uint8) * 255

# Narysuj przykładowe czarne linie (jak w CAD)
cv2.line(img, (100, 100), (700, 100), (0, 0, 0), 1)
cv2.line(img, (100, 100), (100, 500), (0, 0, 0), 1)
cv2.line(img, (700, 100), (700, 500), (0, 0, 0), 1)
cv2.line(img, (100, 500), (700, 500), (0, 0, 0), 1)
cv2.line(img, (100, 100), (700, 500), (0, 0, 0), 1)
cv2.line(img, (700, 100), (100, 500), (0, 0, 0), 1)

# Okrąg
cv2.circle(img, (400, 300), 100, (0, 0, 0), 1)

# Zapisz
cv2.imwrite('test_image.png', img)
print("Utworzono test_image.png")

