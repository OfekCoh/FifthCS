import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifft2, fftshift, ifftshift

import warnings
warnings.filterwarnings("ignore")

def scale_down(image, resize_ratio):
    # compute new size.
    N,M = image.shape
    half_N = int((N * resize_ratio) // 2)
    half_M = int((M * resize_ratio) // 2)
    center_N, center_M = N // 2, M // 2

    # crop the central portion of the frequency domain
    fourier_transform = fftshift(fft2(image))
    cropped = fourier_transform[center_N - half_N:center_N + half_N, center_M - half_M:center_M + half_M]

    # inverse to image domain
    image_resized=np.abs(ifft2(ifftshift(cropped)))
    image_resized = cv2.normalize(image_resized, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    return image_resized


def scale_up(image, resize_ratio):
    fourier_transform = fftshift(fft2(image))
    
    # get sizes
    height, width= fourier_transform.shape  
    new_height, new_width= int(resize_ratio * height), int(resize_ratio * width)
    start_h = (new_height - height) // 2
    start_w = (new_width - width) // 2

    # pad with zeros 
    larger_fourier= np.zeros((new_height, new_width), dtype=complex)  
    larger_fourier[start_h:start_h + height, start_w:start_w + width] = fourier_transform  # now theres the fourier values in the center and zeros padding around

    # resize_ratio Larger Grayscale Image
    image_resized=np.abs(ifft2(ifftshift(larger_fourier)))
    image_resized = cv2.normalize(image_resized, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    return image_resized


from numpy.lib.stride_tricks import sliding_window_view
def ncc_2d(image, pattern):
    # extract the sliding windows from the image
    windows = sliding_window_view(image, pattern.shape)  # Shape: (H', W', pattern_H, pattern_W)

    # compute the mean and standard deviation of pattern
    pattern_mean = np.mean(pattern)
    pattern_std = np.std(pattern)

    # compute the mean and standard deviation of window
    window_means = np.mean(windows, axis=(-2, -1))
    window_stds = np.std(windows, axis=(-2, -1))

    # compute NCC
    numerator = np.sum((windows - window_means[..., None, None]) * (pattern - pattern_mean), axis=(-2, -1))
    denominator = window_stds * pattern_std * pattern.size

    ncc_values = np.where(denominator != 0, numerator / denominator, 0)
    
    return ncc_values


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
# display(image, pattern)



############# Students #############
im_ratio=1      # scale parameteres for image and patern
pt_ratio=0.5

image_scaled = scale_down(image, im_ratio) 
pattern_scaled =  scale_down(pattern, pt_ratio)

display(image_scaled, pattern_scaled)

threshold=0.46  # for real matches
ncc = ncc_2d(image_scaled, pattern_scaled)
real_matches = np.argwhere(ncc >= threshold)  # returns the indices of matches

# ######### DONT CHANGE THE NEXT TWO LINES #########
real_matches[:,0] += pattern_scaled.shape[0] // 2			# if pattern was not scaled, replace this with "pattern"
real_matches[:,1] += pattern_scaled.shape[1] // 2			# if pattern was not scaled, replace this with "pattern"

draw_matches(image, real_matches, pattern_scaled.shape)	# if pattern was not scaled, replace this with "pattern"



CURR_IMAGE = "thecrew"

image = cv2.imread(f'{CURR_IMAGE}.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ############# Crew #############
im_ratio=2.5     # scale parameteres for image and patern
pt_ratio=0.6

image_scaled = scale_up(image, im_ratio) 
pattern_scaled =  scale_down(pattern, pt_ratio)

display(image_scaled, pattern_scaled)

threshold=0.435  # for real matches
ncc = ncc_2d(image_scaled, pattern_scaled)
real_matches = np.argwhere(ncc >= threshold)  # returns the indices of matches

######### DONT CHANGE THE NEXT TWO LINES #########
real_matches[:,0] += pattern_scaled.shape[0] // 2			# if pattern was not scaled, replace this with "pattern"
real_matches[:,1] += pattern_scaled.shape[1] // 2			# if pattern was not scaled, replace this with "pattern"

# If you chose to scale the original image, make sure to scale back the matches in the inverse resize ratio.
real_matches = (real_matches / im_ratio).astype(int)

draw_matches(image, real_matches, pattern_scaled.shape)	# if pattern was not scaled, replace this with "pattern"


