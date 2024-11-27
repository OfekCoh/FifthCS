# Student_Name1, Student_ID1
# Student_Name2, Student_ID2

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

import warnings
warnings.filterwarnings("ignore")

# Input: numpy array of images and number of gray levels to quantize the images down to
# Output: numpy array of images, each with only n_colors gray levels
def quantization(imgs_arr, n_colors=4):
	img_size = imgs_arr[0].shape
	res = []
	
	for img in imgs_arr:
		X = img.reshape(img_size[0] * img_size[1], 1)
		km = KMeans(n_clusters=n_colors)
		km.fit(X)
		
		img_compressed = km.cluster_centers_[km.labels_]
		img_compressed = np.clip(img_compressed.astype('uint8'), 0, 255)

		res.append(img_compressed.reshape(img_size[0], img_size[1]))
	
	return np.array(res)

# Input: A path to a folder and formats of images to read
# Output: numpy array of grayscale versions of images read from input folder, and also a list of their names
def read_dir(folder, formats=(".jpg", ".png")):
	image_arrays = []
	lst = [file for file in os.listdir(folder) if file.endswith(formats)]
	for filename in lst:
		file_path = os.path.join(folder, filename)
		image = cv2.imread(file_path)
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		image_arrays.append(gray_image)
	return np.array(image_arrays), lst

# Input: image object (as numpy array) and the index of the wanted bin (between 0 to 9)
# Output: the height of the idx bin in pixels
def get_bar_height(image, idx):
	# Assuming the image is of the same pixel proportions as images supplied in this exercise, the following values will work
	x_pos = 70 + 40 * idx
	y_pos = 274
	while image[y_pos, x_pos] == 1:
		y_pos-=1
	return 274 - y_pos

# The function should return whether a region was found with EMD < 260	
def compare_hist(src_image, target):
	windows= np.lib.stride_tricks.sliding_window_view(src_image, (target.shape[0], target.shape[1])) #create the windows- (hh,ww,height,width), each window[hh,ww] represents a corresponding window with size (height,width)
	target_hist = cv2.calcHist([target], [0], None, [256], [0, 256]).flatten()  # get target histogram
	target_sum = np.cumsum(target_hist) 	

	for x in range(30, 50):
		for y in range(100, 145):
			window_hist= cv2.calcHist([windows[y,x]], [0], None, [256], [0, 256]).flatten() #calculate the window’s histogram (256 length array).
			window_sum=np.cumsum(window_hist)  # cumulative histogram
			
			emd = np.sum(np.abs(window_sum - target_sum)) # calc the total cumulative histogram difference
			if emd < 260:
				return True  # found a matching window
				
	return False # no match was found
	

images, names = read_dir(r'C:\Users\ofekc\Desktop\CS_Haifa\FifthCS\Image Processing\HW1\data')
numbers, _ = read_dir(r'C:\Users\ofekc\Desktop\CS_Haifa\FifthCS\Image Processing\HW1\numbers')

# cv2.imshow('names[0]', images[0]) 
# cv2.waitKey(0)
# cv2.destroyAllWindows() 
# # read digits
# cv2.imshow('_[0]', numbers[0]) 
# cv2.waitKey(0)
# cv2.destroyAllWindows() 
# exit()

# #check comapre_hist function
# j=4
# cv2.imshow('name', images[j]) 
# cv2.waitKey(0)
# for i in range (10):
# 	print(i, ": ", compare_hist(images[j], numbers[i]))

# for j in range (7):
# 	for i in range (9, -1 , -1):
# 		if compare_hist(images[j], numbers[i]):
# 			print("iamge", j, "gets result",i)
# 			break  # Exit the loop if the histograms match

 
quantized_images= quantization(images,3)
black_white_images = []
for i in range (7):
	plt.imshow(quantized_images[i], cmap='gray')  # Use 'gray' for grayscale images
	plt.axis('off')  # Optional: Hide axis ticks
	plt.title('Image Display')  # Optional: Add a title
	plt.show()
# for img in quantized_images:
#     _, binary_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     black_white_images.append(binary_img)

# for i in range (7):
# 	cv2.imshow(f'Black & White Image {i}', black_white_images[i]) 
# 	cv2.waitKey(0)

# The following print line is what you should use when printing out the final result - the text version of each histogram, basically.

# print(f'Histogram {names[id]} gave {heights}')
