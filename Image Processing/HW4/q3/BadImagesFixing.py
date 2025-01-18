import numpy as np
from numpy.fft import fft2, ifft2, fftshift, ifftshift
import cv2
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from scipy.ndimage import median_filter

def perspective_transform(image, points):
    pts1 = np.float32(points)
    
    height, width = image.shape[:2]
    
    # Define destination points
    pts2 = np.float32([
        [0, 0],           # top-left
        [width, 0],       # top-right
        [0, height],      # bottom-left
        [width, height]   # bottom-right
    ])
    
    # Calculate perspective transform matrix
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    
    # Apply perspective transformation
    transformed_image = cv2.warpPerspective(image, matrix, (width, height))
    
    return transformed_image

def clean_baby(im):
    # Median blur
    im = cv2.medianBlur(im, 3)
    height, width = im.shape
    
    # Top-left image
    img1 = im[20:130, 5:110]
    img1 = cv2.resize(img1, (width, height), interpolation=cv2.INTER_LINEAR)
    
    # Top-right image
    points2 = [
        (181, 3),    # top-left
        (250, 70),   # top-right
        (120, 50),   # bottom-left
        (175, 120)   # bottom-right
    ]
    img2 = perspective_transform(im, points2)
    
    # Bottom-left image
    points3 = [
        (77, 162),   # top-left
        (146, 116),  # top-right
        (132, 244),  # bottom-left
        (245, 160)   # bottom-right
    ]
    img3 = perspective_transform(im, points3)
    

    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)
    img3 = img3.astype(np.float32)
    
    # Calculate pixel-wise average
    result = (img1 + img2 + img3) / 3.0
    
    result = np.clip(result, 0, 255).astype(np.uint8)
    
    return result 
    
    
def clean_windmill(im):
    fourier_transform = fftshift(fft2(im))    

    # magnitude_spectrum = np.log(1+np.absolute(fourier_transform))  # 13.61 is the peak
    # plt.imshow(magnitude_spectrum, cmap='gray')
    # plt.colorbar()
    # plt.show()

    # by observing the plot above we found those 2 peaks that we need to remove
    x1,y1= 100,124
    x2,y2=156,132
    fourier_transform[y1, x1] = 0
    fourier_transform[y2, x2] = 0

    # also clean the symmetric points (as Fourier transform is symmetric)
    y1_sym, x1_sym = im.shape[0] - y1, im.shape[1] - x1  
    y2_sym, x2_sym = im.shape[0] - y2, im.shape[1] - x2  
    fourier_transform[y1_sym, x1_sym] = 0
    fourier_transform[y2_sym, x2_sym] = 0

    # inverse fourier transform
    clean_image=np.abs(ifft2(ifftshift(fourier_transform)))

    return clean_image
    
          
def clean_watermelon(im):
    # Create a sharpening kernel
    kernel = np.array([[-1,-1,-1],
                      [-1, 9,-1],
                      [-1,-1,-1]])
    
    # Apply the sharpening kernel
    sharpened = cv2.filter2D(im, -1, kernel)
    
    return sharpened


def clean_umbrella(im):  
    x0,y0= 79, 4    # by checking the image =>  (x,y)=(82,63)  ==>   (x-x0,y-y0)=(161,67)  ==>  x0=-79  y0=-4

    # calc delta
    delta= np.zeros_like(im)
    delta[0][0]=1
    F_delta=fftshift(fft2(delta)) 

    # calc delta shifted based on found x0 y0
    delta_shifted = np.roll(delta, shift=(y0, x0), axis=(0, 1))
    F_delta_shifted=fftshift(fft2(delta_shifted)) 


    # F(shifted image) -- F(A) purpose from toturial
    F_im=fftshift(fft2(im))

    # now we will apply this logic:  F_im = 0.5 *  F_original * (F_delta + F_delta_shifted)) 

    
    # F_im =  0.5* F_original * F_delta_combined
    F_delta_combined = 0.5 * (F_delta + F_delta_shifted) 

    
    F_original=F_im
    # F_original= F_im / F_delta_combined
    for i in range(F_im.shape[0]):  
        for j in range(F_im.shape[1]):  
            if F_delta_combined[i, j] <0.00000000001 :  # just because very small values sent the valuse very high
                F_original[i, j] = 0
            else:
                F_original[i, j] = F_im[i, j] / F_delta_combined[i, j]
    
    # inverse to image 
    original_image=np.abs(ifft2(ifftshift(F_original)))
    
    return original_image
    
    
def clean_USAflag(im):
    stars = im[0:92, 0:142].copy()  # x=145 y=92   len=12/13  width=

    clean = median_filter(im, size=(1, 10))  # horizontal
    clean[96][188]=204  # fixing this one black pixel that wont go away

    clean = cv2.GaussianBlur(clean, (99, 1), 0) # horizontal

    for i in range(stars.shape[0]):  # restore stars
        for j in range(stars.shape[1]):
            clean[i][j]=stars[i][j]

    return clean



def clean_house(im):
    im = im.astype(np.float32) / 255.0
    
    # Simple kernel and padding
    k = np.zeros((10, 10))
    k[5, :] = 0.1
    
    # Fix padding to match image size exactly
    pad_h = ((im.shape[0] - k.shape[0]) // 2, (im.shape[0] - k.shape[0] + 1) // 2)
    pad_w = ((im.shape[1] - k.shape[1]) // 2, (im.shape[1] - k.shape[1] + 1) // 2)
    k_pad = np.pad(k, (pad_h, pad_w))
    
    # Quick de-convolution
    imf = fft2(im)
    kf = fft2(fftshift(k_pad))
    deblurred = np.real(ifft2(imf * np.conj(kf) / (np.abs(kf)**2 + 0.0001)))
    
    deblurred = np.clip(deblurred * 255, 0, 255).astype(np.uint8)
    
    # Correct the shift
    shift_amount = 6 
    deblurred = np.roll(deblurred, -shift_amount, axis=1)
    
    return deblurred

def clean_bears(im):
    im_float = im.astype(np.float32)
    
    # Simple contrast stretching with normalization
    im_norm = (im_float - im_float.min()) / (im_float.max() - im_float.min())

    return (im_norm * 255).astype(np.uint8)
    
