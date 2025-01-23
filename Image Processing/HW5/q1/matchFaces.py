# Student_Name1, Student_ID1
# Student_Name2, Student_ID2

# Please replace the above comments with your names and ID numbers in the same format.

import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifft2, fftshift, ifftshift

import warnings
warnings.filterwarnings("ignore")

def scale_down(image, resize_ratio):
    # Your code goes here
    sigma = max(1.0, 1.0 / resize_ratio)
    
    # Compute an appropriate kernel size (ensure it's odd)
    kernel_size = int(2 * round(3 * sigma) + 1)
    kernel_size = max(3, kernel_size)  # Ensure minimum kernel size of 3x3
    
    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

    # Compute the 2D Fourier Transform
    f_transform = fftshift(fft2(blurred_image))

    # Get the shape of the original image
    rows, cols = blurred_image.shape
    new_rows, new_cols = int(rows * resize_ratio), int(cols * resize_ratio)

    # Define cropping boundaries in frequency domain
    row_center, col_center = rows // 2, cols // 2
    row_start, row_end = row_center - new_rows // 2, row_center + new_rows // 2
    col_start, col_end = col_center - new_cols // 2, col_center + new_cols // 2

    # Crop the frequency domain representation
    cropped_f_transform = f_transform[row_start:row_end, col_start:col_end]

    # Inverse Fourier Transform to obtain the downscaled image
    f_transform_back = ifftshift(cropped_f_transform)
    scaled_image = np.abs(ifft2(f_transform_back))

    # Normalize and convert to uint8
    scaled_image = cv2.normalize(scaled_image, None, 0, 255, cv2.NORM_MINMAX)
    return scaled_image.astype(np.uint8)


def scale_up(image, resize_ratio):
    # Your code goes here
    # Compute the 2D Fourier Transform
    f_transform = fft2(image)
    f_transform_shifted = fftshift(f_transform)

    # Get the shape of the original image
    rows, cols = image.shape
    new_rows, new_cols = int(rows * resize_ratio), int(cols * resize_ratio)

    # Create a new zero-padded frequency domain representation
    padded_f_transform = np.zeros((new_rows, new_cols), dtype=complex)

    # Define the position to insert the original frequency content
    row_center, col_center = rows // 2, cols // 2
    new_row_center, new_col_center = new_rows // 2, new_cols // 2
    
    # Copy the original frequency content to the center of the new padded array
    padded_f_transform[new_row_center - row_center:new_row_center + row_center,
                       new_col_center - col_center:new_col_center + col_center] = f_transform_shifted

    # Inverse Fourier Transform to obtain the upscaled image
    f_transform_shifted_back = ifftshift(padded_f_transform)
    upscaled_image = np.abs(ifft2(f_transform_shifted_back))

    # Normalize and convert to uint8
    upscaled_image = cv2.normalize(upscaled_image, None, 0, 255, cv2.NORM_MINMAX)
    return upscaled_image.astype(np.uint8)


from numpy.lib.stride_tricks import sliding_window_view
def ncc_2d(image, pattern):
    # Your code goes here
    # Create sliding windows of the same shape as the pattern
    windows = sliding_window_view(image, pattern.shape)
    
    # Compute mean and standard deviation of the pattern
    pattern_mean = np.mean(pattern)
    pattern_std = np.std(pattern)
    
    # Handle the case when pattern variance is zero
    if pattern_std == 0:
        return np.zeros_like(image[:image.shape[0] - pattern.shape[0] + 1,
                                  :image.shape[1] - pattern.shape[1] + 1])
    
    # Normalize the pattern
    pattern_norm = (pattern - pattern_mean) / pattern_std
    
    # Compute mean and standard deviation for each window
    window_means = np.mean(windows, axis=(2, 3))
    window_stds = np.std(windows, axis=(2, 3))
    
    # Avoid division by zero by setting zero-variance regions to NCC of 0
    valid_mask = window_stds > 0
    ncc = np.zeros_like(window_means)
    
    # Perform NCC computation only for valid regions
    ncc[valid_mask] = np.sum((windows[valid_mask] - window_means[valid_mask, None, None]) * pattern_norm,
                             axis=(2, 3)) / (window_stds[valid_mask] * pattern_std)
    
    return ncc



def display(image, pattern):
    
    plt.subplot(2, 3, 1)
    plt.title('Image')
    plt.imshow(image, cmap='gray')
        
    plt.subplot(2, 3, 3)
    plt.title('Pattern')
    plt.imshow(pattern, cmap='gray', aspect='equal')
    
    ncc = ncc_2d(image, pattern)
    
    plt.subplot(2, 3, 5)
    plt.title('Normalized Cross-Correlation Heatmap')
    plt.imshow(ncc ** 2, cmap='coolwarm', vmin=0, vmax=1, aspect='auto') 
    
    cbar = plt.colorbar()
    cbar.set_label('NCC Values')
        
    plt.show()

def draw_matches(image, matches, pattern_size):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for point in matches:
        y, x = point
        top_left = (int(x - pattern_size[1]/2), int(y - pattern_size[0]/2))
        bottom_right = (int(x + pattern_size[1]/2), int(y + pattern_size[0]/2))
        cv2.rectangle(image, top_left, bottom_right, (255, 0, 0), 1)
    
    plt.imshow(image, cmap='gray')
    plt.show()
    
    cv2.imwrite(f"{CURR_IMAGE}_result.jpg", image)



CURR_IMAGE = "students"

image = cv2.imread(f'{CURR_IMAGE}.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

pattern = cv2.imread('template.jpg')
pattern = cv2.cvtColor(pattern, cv2.COLOR_BGR2GRAY)

############# DEMO #############
display(image, pattern)





############# Students #############

image_scaled = # Your code goes here. If you choose not to scale the image, just remove it.
pattern_scaled =  # Your code goes here. If you choose not to scale the pattern, just remove it.

display(image_scaled, pattern_scaled)

ncc = # Your code goes here
real_matches = # Your code goes here

######### DONT CHANGE THE NEXT TWO LINES #########
real_matches[:,0] += pattern_scaled.shape[0] // 2			# if pattern was not scaled, replace this with "pattern"
real_matches[:,1] += pattern_scaled.shape[1] // 2			# if pattern was not scaled, replace this with "pattern"

# If you chose to scale the original image, make sure to scale back the matches in the inverse resize ratio.

draw_matches(image, real_matches, pattern_scaled.shape)	# if pattern was not scaled, replace this with "pattern"





############# Crew #############

image_scaled = # Your code goes here. If you choose not to scale the image, just remove it.
pattern_scaled =  # Your code goes here. If you choose not to scale the pattern, just remove it.

display(image_scaled, pattern_scaled)

ncc = # Your code goes here
real_matches = # Your code goes here

######### DONT CHANGE THE NEXT TWO LINES #########
real_matches[:,0] += pattern_scaled.shape[0] // 2			# if pattern was not scaled, replace this with "pattern"
real_matches[:,1] += pattern_scaled.shape[1] // 2			# if pattern was not scaled, replace this with "pattern"

# If you chose to scale the original image, make sure to scale back the matches in the inverse resize ratio.

draw_matches(image, real_matches, pattern_scaled.shape)	# if pattern was not scaled, replace this with "pattern"
