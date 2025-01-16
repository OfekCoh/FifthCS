
import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift
import cv2
import matplotlib.pyplot as plt

image_path = 'zebra.jpg'
image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)

# Fourier Spectrum
fourier_transform = fftshift(fft2(image))   # transform it to frequency domain, each element is the amplitude and phase of a particular frequency component, then shift to the center
fourier_image=np.log(1+np.absolute(fourier_transform)) # log to compress the range, absoloute to get represent amplitude of frequency (instead of real and imaginary values)

# Fourier Spectrum Zero Padding
height, width= fourier_transform.shape  
larger_fourier= np.zeros((2 * height, 2 * width), dtype=complex)  
larger_fourier[height//2:(height//2)+height, width//2:(width//2)+width] = fourier_transform  # now theres the fourier values in the center and zeros padding around
larger_fourier_image=np.log(1+np.absolute(larger_fourier)) 

# Two Times Larger Grayscale Image
source=np.abs(ifft2(ifftshift(larger_fourier)))
source= np.clip(source * 4, 0, 255).astype(np.uint8)  # because ifft over normalized it by the bigger N

# Fourier Spectrum Four Copies
four_copies_spectrum= np.zeros((2 * height, 2 * width), dtype=complex)  # canvas 2X
four_copies_spectrum[::2, ::2] = fourier_transform     # add 0 between every element 
four_copies_image=np.log(1+np.absolute(four_copies_spectrum)) 

# four zebras
source2=np.abs(ifft2(ifftshift(four_copies_spectrum)))
source2= np.clip(source2 * 4, 0, 255).astype(np.uint8)

plt.figure(figsize=(10,10))
plt.subplot(321)
plt.title('Original Grayscale Image')
plt.imshow(image, cmap='gray')   

plt.subplot(322)
plt.title('Fourier Spectrum')
plt.imshow(fourier_image, cmap='gray')   

plt.subplot(323)
plt.title('Fourier Spectrum Zero Padding')
plt.imshow(larger_fourier_image , cmap='gray')  

plt.subplot(324)
plt.title('Two Times Larger Grayscale Image')
plt.imshow(source, cmap='gray')   

plt.subplot(325)
plt.title('Fourier Spectrum Four Copies')
plt.imshow(four_copies_image, cmap='gray')

plt.subplot(326)
plt.title('Four Copies Grayscale Image')
plt.imshow(source2, cmap='gray')

plt.savefig('zebra_scaled.jpg')
plt.show()
