
import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_laplacian_pyramid(image, levels):
    pyramid = []
    # convert to float32 for better precision in calculations
    current_image = image.astype(np.float32)
    
    for _ in range(levels):
        # pyrDown: Reduces image size by half and applies Gaussian smoothing
        downSampled = cv2.pyrDown(current_image)
        
        # pyrUp: Doubles image size to match original
        upSampled = cv2.pyrUp(downSampled, dstsize=(current_image.shape[1], current_image.shape[0]))
        
        # Captures the high-frequency details
        laplacian = current_image - upSampled  
        
        # Store the Laplacian level
        pyramid.append(laplacian)
        
        # Update current_image to downSampled version for next iteration
        current_image = downSampled
        
    # This preserves the DC 
    pyramid.append(current_image)
    
    return pyramid

def restore_from_pyramid(pyramidList):
    restored_image = pyramidList[-1]  # Start from the DC component
    
    for laplacian in reversed(pyramidList[:-1]):
        restored_image = cv2.pyrUp(restored_image, dstsize=(laplacian.shape[1], laplacian.shape[0]))
        restored_image += laplacian 
    
    return np.clip(restored_image, 0, 255).astype(np.uint8)  # Convert back to uint8


def validate_operation(img):
	levels = 6
	pyr = get_laplacian_pyramid(img, levels)
	img_restored = restore_from_pyramid(pyr)

	plt.title(f"MSE is {np.mean((img_restored - img) ** 2)}")
	plt.imshow(img_restored, cmap='gray')

	plt.show()
	

def blend_pyramids(levels):
   global pyr_apple, pyr_orange
   blended_pyr = []
   
   # loop foreach level
   for curr_level in range(levels + 1):
       orange_level = pyr_orange[curr_level]
       apple_level = pyr_apple[curr_level]
       
       height, width = orange_level.shape
       # Initialize mask matrix with zeros - will control blending amounts
       mask = np.zeros((height, width), dtype=np.float32)
       
       # Here we limit blend width to prevent issues with small images
       # We limit it to 1/4 of width to ensure safer blending
       blend_width = min(curr_level, width//4)
       
       # Also we added safety bounds checking
       # max(0,...) ensures we don't get negative indices
       left_bound = max(0, int(width//2 - blend_width))
       mask[:, :left_bound] = 1.0 
       
       # Same as above, but for right side
       right_bound = min(width, int(width//2 + blend_width))
       
       # Create gradual blending transition
       for i in range(left_bound, right_bound):
           if curr_level > 0:
			   # For levels > 0, we use more gradual blending
               mask[:, i] = 0.9 - 0.9 * (i - left_bound) / (2 * blend_width)
           else:
               mask[:, i] = 0.5  # For level 0, use simple 50-50 blend in transition
       
       # Cross-dissolve blending:
       blended = orange_level * mask + apple_level * (1 - mask)
       blended_pyr.append(blended)
   
   return blended_pyr
apple = cv2.imread('apple.jpg')
apple = cv2.cvtColor(apple, cv2.COLOR_BGR2GRAY)

orange = cv2.imread('orange.jpg')
orange = cv2.cvtColor(orange, cv2.COLOR_BGR2GRAY)

# validate_operation(apple)
# validate_operation(orange)

pyr_apple = get_laplacian_pyramid(apple,6)
pyr_orange = get_laplacian_pyramid(orange,6)



pyr_result = []

# # Your code goes here
pyr_result = blend_pyramids(6)

final = restore_from_pyramid(pyr_result)
plt.imshow(final, cmap='gray')
plt.show()

cv2.imwrite("result.jpg", final)

