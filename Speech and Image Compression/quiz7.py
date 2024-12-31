import cv2
import numpy as np
from scipy.fftpack import dct

# Load the image (grayscale)
image_path = "peppers.png"  # Replace with your image path
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Find the average pixel value
average_pixel = np.mean(image)
print(f"Average pixel value: {average_pixel}")

# Perform the Discrete Cosine Transform (DCT)
# Ensure the image is converted to float32 for DCT
image_float = np.float32(image)
dct_transformed = dct(dct(image_float.T, norm='ortho').T, norm='ortho')

# Extract the DC component (top-left corner)
dc_component = dct_transformed[0, 0]
print(f"DC Component: {dc_component}")
