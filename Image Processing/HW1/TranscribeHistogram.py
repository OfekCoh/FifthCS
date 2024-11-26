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

# We get a small target and a big image, slide a target's size window on the image to search for a target match.
# The function should return whether a region was found with EMD < 260	
def compare_hist(src_image, target):
	windows= np.lib.stride_tricks.sliding_window_view(src_image, (target.shape[0], target.shape[1])) #create the windows- (hh,ww,height,width), each window[hh,ww] represents a corresponding window with size (height,width)
	
	for x in range(30, 50):
		for y in range(100, 145):
			#  לחשב את ה-cumulative histogram בעזרת np.cumsum(), ואז לחשב את ה-EMD לפי הנוסחה הפשוטה של סכום הערכים המוחלטים של הפרשי ההיסטוגרמות המצטברות
			
			cv2.calcHist([windows[y,x]], [0], None, [256], [0, 256]).flatten() #calculate the window’s histogram (256 length array).

	#Since we will need only the topmost number (e.g 6 in a.jpg), you can search just the region around it without needing to look
	#further down the image. With this function you can find if a digit is present in the image.


	return True 
	return False
	


# Sections a, b

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

for i in range (9, -1 , -1):
	if compare_hist(images[0], numbers[i]):
		break  # Exit the loop if the histograms match


# The following print line is what you should use when printing out the final result - the text version of each histogram, basically.

# print(f'Histogram {names[id]} gave {heights}')
