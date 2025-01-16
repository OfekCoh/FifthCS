import numpy as np
import matplotlib.pyplot as plt

canvas= np.zeros((1600,2400)) 
canvas[25][25]=255

plt.title('Original Grayscale Image')
plt.imshow(canvas, cmap='gray')
plt.show()
