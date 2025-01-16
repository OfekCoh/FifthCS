import numpy as np
import matplotlib.pyplot as plt

canvas= np.zeros((50,50)) 
canvas[::2, ::2]=255

plt.title('check Image')
plt.imshow(canvas, cmap='gray')
plt.show()
