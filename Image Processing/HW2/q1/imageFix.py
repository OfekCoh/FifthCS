import cv2
import matplotlib.pyplot as plt
import numpy as np

def apply_fix(image, id):
	if(id==1):
		# Histogram equalization
		equalized_image = cv2.equalizeHist(image)
		return equalized_image
	
	if(id==2):
		# Gamma Correction
		gamma = 0.55     # >1 darkens, <1 brightens
		normalized_image= image / 255.0      # Normalize the image to the range [0, 1]
		corrected_image = np.power(normalized_image, gamma) * 255    # Apply gamma correction and scale back pixles to *255 
		corrected_image = corrected_image.astype(np.uint8)
		return corrected_image
		
	if(id==3):
		# none
		return image
		 


for i in range(1,4):
	if(i==1):
		path = f'{i}.png'
	else:
		path = f'{i}.jpg'
	
	image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
	fixed_image = apply_fix(image, i)
	plt.imsave(f'{i}_fixed.jpg', fixed_image, cmap='gray', vmin=0, vmax=255)
	
	# cv2.imshow("image", fixed_image)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()




	# # Brightness and contrast stretching.
	# min_in = np.min(image)  # Minimum pixel value in the input image
	# 	max_in = np.max(image)  # Maximum pixel value in the input image

	# 	# Define the output range
	# 	min_out = 0   # New minimum value (e.g., black)
	# 	max_out = 255 # New maximum value (e.g., white)

	# 	# Apply contrast stretching
	# 	stretched_image = ((image - min_in) / (max_in - min_in)) * (max_out - min_out) + min_out
	# 	stretched_image = np.clip(stretched_image, 0, 255)  # Ensure pixel values are within [0, 255]
	# 	stretched_image = stretched_image.astype(np.uint8)

	# 	return stretched_image