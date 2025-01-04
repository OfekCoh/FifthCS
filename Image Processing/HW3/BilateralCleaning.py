# Liran Anteby, 207435009
# Ofek Cohen, 319001533

# Please replace the above comments with your names and ID numbers in the same format.

import cv2
import numpy as np
import matplotlib.pyplot as plt

def clean_Gaussian_noise_bilateral(im, radius, stdSpatial, stdIntensity):
	# Your code goes here
    
    # As explained, using float64 for more accurate results
    im = im.astype(np.float64)
    
    # Size of the image
    height, width = im.shape
    
    # Create the spatial Gaussian mask (gs) - precomputed as it's the same for every pixel
    x, y = np.meshgrid(np.arange(-radius, radius + 1), np.arange(-radius, radius + 1))
    gs = np.exp(-(x**2 + y**2) / (2 * stdSpatial**2))
    
    # Init the output image
    cleanIm = np.zeros_like(im)
    
    # For every pixel
    for i in range(height):
        for j in range(width):
            # Define the window bounds, avoiding out of bounds
            i_min = max(i - radius, 0)
            i_max = min(i + radius + 1, height)
            j_min = max(j - radius, 0)
            j_max = min(j + radius + 1, width)
            
            # Extract the image around current pixel
            window = im[i_min:i_max, j_min:j_max]
            
            # Adjust gs to the current window size
            gs_window = gs[
                radius - (i - i_min): radius + (i_max - i),
                radius - (j - j_min): radius + (j_max - j)
            ]
            
            # Compute intensity Gaussian mask (gi)
            gi = np.exp(-((window - im[i, j])**2) / (2 * stdIntensity**2))
            
            # Combine spatial and intensity weights
            weights = gs_window * gi
            
            # Normalize the weights
            weights /= np.sum(weights)
            
            # Compute the weighted average
            cleanIm[i, j] = np.sum(weights * window)
    
    # Convert back to uint8 for display
    return np.clip(cleanIm, 0, 255).astype(np.uint8)
    

# change this to the name of the image you'll try to clean up
original_image_path_a = 'taj.jpg'
original_image_path_b = 'balls.jpg'
original_image_path_c = 'NoisyGrayImage.png'

imageA = cv2.imread(original_image_path_a, cv2.IMREAD_GRAYSCALE)
imageB = cv2.imread(original_image_path_b, cv2.IMREAD_GRAYSCALE)
imageC = cv2.imread(original_image_path_c, cv2.IMREAD_GRAYSCALE)

# values for taj
clear_image_a = clean_Gaussian_noise_bilateral(imageA, 7, 20, 25) 

# values for balls
clear_image_b = clean_Gaussian_noise_bilateral(imageB, 3, 5, 10) 

# values for noisy gray image
clear_image_c = clean_Gaussian_noise_bilateral(imageC, 7, 20, 50) 

# Create a figure with 3 rows and 2 columns
plt.figure(figsize=(12, 12))  # Makes the figure larger

# First row: Taj Mahal
plt.subplot(321)  # 3 rows, 2 cols, position 1
plt.title('Original Taj')
plt.imshow(imageA, cmap='gray')

plt.subplot(322)  # 3 rows, 2 cols, position 2
plt.title('Filtered Taj')
plt.imshow(clear_image_a, cmap='gray')

# Second row: Balls
plt.subplot(323)  # 3 rows, 2 cols, position 3
plt.title('Original Balls')
plt.imshow(imageB, cmap='gray')

plt.subplot(324)  # 3 rows, 2 cols, position 4
plt.title('Filtered Balls')
plt.imshow(clear_image_b, cmap='gray')

# Third row: Noisy Gray
plt.subplot(325)  # 3 rows, 2 cols, position 5
plt.title('Original Noisy')
plt.imshow(imageC, cmap='gray')

plt.subplot(326)  # 3 rows, 2 cols, position 6
plt.title('Filtered Noisy')
plt.imshow(clear_image_c, cmap='gray')

# Add spacing between subplots
plt.tight_layout()
plt.show()
