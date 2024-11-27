
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
	while image[y_pos, x_pos] == 0:
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

images, names = read_dir('data')
numbers, _ = read_dir('numbers')

max_student_num=[]  # get the top bar value for each image

for img in range (7):  # find max_student_num: the highest bar number, get from compare hist
	for i in range (9, -1 , -1):
		if compare_hist(images[img], numbers[i]):
			# print("image", img, "gets result",i)
			max_student_num.append(i)
			break  # Exit the loop if the histograms match

quantized_images= quantization(images,3)  # change to 3 colors images
black_white_images = []

for img in quantized_images:  # turn quantized_images to black and white
	binary_img = np.full_like(img, 255,dtype='uint8')  # start with an image all white 
	binary_img[img<220] = 0  # for all pixels under 220 in image turn them black in binary image
	black_white_images.append(binary_img)  # add to black_white_images

# max_student_num: the highest bar number, get from compare hist
# max_bin_height: the height of that bar (from the line above)
# bin_height: current bar height

max_bin_height=[]   

for img in black_white_images: # find max_bin_height for each image
	temp_heights=[] # save all heights of an image
	for i in range (10):
		temp_heights.append(get_bar_height(img, i))
	max_bin_height.append(np.max(temp_heights))


for id in range(7):  # loop through the images and calc how many students are in each bar
	heights=[]  # store the results for each image
	for i in range (10): # loop all bars
		bin_height= (get_bar_height(black_white_images[id], i))
		students_per_bin = round(max_student_num[id] * bin_height / max_bin_height[id])  
		heights.append(students_per_bin)
	print(f'Histogram {names[id]} gave {heights}')







# for x in range(7):   # check black and white images
# 	plt.imshow(black_white_images[x], cmap='gray')
# 	plt.show()
# 	cv2.imshow('names[0]', black_white_images[x]) 
# 	cv2.waitKey(0)
# cv2.destroyAllWindows()

# for x in quantized_images:   #check quantized_images pixels
# 	plt.imshow(x, cmap='gray')
# 	plt.show()

# for x in black_white_images:   #check quantized_images pixels
# 	plt.imshow(x, cmap='gray')
# 	plt.show()

# cv2.imshow('names[0]', images[0]) 
# cv2.waitKey(0)
# cv2.destroyAllWindows() 