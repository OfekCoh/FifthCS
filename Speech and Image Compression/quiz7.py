import cv2
import numpy as np
from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt

# Load the image (grayscale)
image_path = "peppers.png"  # Replace with your image path
gray_image  = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
image_float = np.float32(gray_image )  # Convert to float for computation

dct_transformed = dct(dct(image_float.T, norm='ortho').T, norm='ortho')  # 2D DCT
reconstructed_image = idct(idct(dct_transformed.T, norm='ortho').T, norm='ortho')  # 2D inverse DCT

# Convert the reconstructed image to integers
reconstructed_image = np.clip(reconstructed_image, 0, 255).astype(np.uint8)

# Step 3: Calculate the difference and MSE
difference = np.abs(gray_image - reconstructed_image)
mse = np.mean((gray_image - reconstructed_image) ** 2)

print(f"Mean Squared Error (MSE): {mse}")

# Step 4: Display the original and reconstructed images side by side
plt.figure(figsize=(10, 5))

# Display original image
plt.subplot(1, 3, 1)
plt.title("Original Image")
plt.imshow(gray_image, cmap='gray')
plt.axis('off')

# Display reconstructed image
plt.subplot(1, 3, 2)
plt.title("Reconstructed Image")
plt.imshow(reconstructed_image, cmap='gray')
plt.axis('off')

# Display difference
plt.subplot(1, 3, 3)
plt.title("Difference")
plt.imshow(difference, cmap='hot')
plt.colorbar()
plt.axis('off')

plt.tight_layout()
plt.show()