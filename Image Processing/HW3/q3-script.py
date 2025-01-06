import cv2
import numpy as np
import matplotlib.pyplot as plt

def clean_Gaussian_noise_bilateral(im, radius, stdSpatial, stdIntensity):
	# Your code goes here
    
    # As explained, using float64 for more accurate results
    im = im.astype(np.float64)
    
    # Size of the image
    height, width = im.shape
    
    # Create the spatial Gaussian mask (gs) - precomputed as it's the same for every pixel.
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
  

def first_task_3(im):
    # Making the image gray
    gray_broken = cv2.imread(im, cv2.IMREAD_GRAYSCALE)
    # Median filter
    median_filtered = cv2.medianBlur(gray_broken, 3)
    # Bilateral filter
    clear_image_d = clean_Gaussian_noise_bilateral(median_filtered, 7, 10, 25) 

    cv2.imwrite(r'I dont tell you\ImageProcessing2024_2025_HW3\q3\part-a-clean.jpg', clear_image_d)
    return clear_image_d


original_image_path_d = r'I dont tell you\ImageProcessing2024_2025_HW3\q3\broken.jpg'
imageD = cv2.imread(original_image_path_d, cv2.IMREAD_GRAYSCALE)
result = first_task_3(original_image_path_d)
plt.imshow(result, cmap='gray')
plt.show()


# Part B
path_to_images = r'I dont tell you\noised_images.npy'
img_array = np.load(path_to_images)

denoised_image = np.median(img_array, axis=0)
plt.imshow(denoised_image, cmap='gray')
plt.title("Denoised Image")
plt.axis('off')
cv2.imwrite(r'I dont tell you\ImageProcessing2024_2025_HW3\q3\part-b-clean.jpg', denoised_image)
plt.show()
