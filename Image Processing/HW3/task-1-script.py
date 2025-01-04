

import cv2
import numpy as np

def img1_calculate (img, img_from_task):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Vertical gaussian blur
    kernel_size = (3001,1)

    changedImg = cv2.GaussianBlur(gray, kernel_size, 0)

    # Calculate MSE
    mse = np.mean((changedImg - img_from_task) ** 2)
    print(f"MSE between processed and task image: {mse} used kernel size: {kernel_size}")

    cv2.imshow('Original', img)
    cv2.imshow('Task image', img_from_task)
    cv2.imshow('the changed original ', changedImg)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

def img2_calculate (img, img_from_task):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Vertical gaussian blur
    kernel_size = (25,25)

    changedImg = cv2.GaussianBlur(gray, kernel_size, 0)

    # Calculate MSE
    mse = np.mean((changedImg - img_from_task) ** 2)
    print(f"MSE between processed and task image: {mse} used kernel size: {kernel_size}")

    cv2.imshow('Original', img)
    cv2.imshow('Task image', img_from_task)
    cv2.imshow('the changed original ', changedImg)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

def img3_calculate(img, img_from_task):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel_size = (13)
    # Apply median blur
    changedImg = cv2.medianBlur(gray, kernel_size)

    # Calculate MSE
    mse = np.mean((changedImg - img_from_task) ** 2)
    print(f"MSE between processed and task image: {mse}")

    cv2.imshow('Original', img)
    cv2.imshow('Task image', img_from_task)
    cv2.imshow('median blur Result', changedImg)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

def img4_calculate(img, img_from_task):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    kernel_size = (1,27)
    # Apply gaussian blur
    changedImg = cv2.GaussianBlur(gray, kernel_size,0)

    # Calculate MSE
    mse = np.mean((changedImg - img_from_task) ** 2)
    print(f"MSE between processed and task image: {mse} used kernel size: {kernel_size}")


    cv2.imshow('Original', img)
    cv2.imshow('Task image', img_from_task)
    cv2.imshow('gaussian blur Result', changedImg)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
    
def img6_calculate(img, img_from_task):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    kernel1 = np.array([
        [0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0]
    ])

    
    result1 = cv2.filter2D(gray, -1, kernel1)
    
    # Calculate MSE
    mse = np.mean((result1 - img_from_task) ** 2)
    print(f"MSE between processed and task image: {mse}")
    
    # Display results
    cv2.imshow('Original', img)
    cv2.imshow('Task image', img_from_task)
    cv2.imshow('Kernel 1 Result', result1)
    cv2.waitKey(0)

    
    cv2.destroyAllWindows()
    
def img7_calculate(img, img_from_task):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Flip top and bottom halves in one operation using array indexing
    changedImg = np.vstack((gray[gray.shape[0]//2:], gray[:gray.shape[0]//2]))
    
    # Calculate MSE
    mse = np.mean((changedImg - img_from_task) ** 2)
    print(f"MSE between processed and task image: {mse}")
    
    # Display images
    cv2.imshow('Original', img)
    cv2.imshow('Task image', img_from_task)
    cv2.imshow('Swapped halves', changedImg)
    cv2.waitKey(0)
        
    cv2.destroyAllWindows()
    
def img8_calculate(img, img_from_task):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    mse = np.mean((gray - img_from_task) ** 2)
    print(f"MSE between processed and task image: {mse}")
    
    # Display images
    cv2.imshow('Original', img)
    cv2.imshow('Task image', img_from_task)
    cv2.imshow('Gray', gray)
    cv2.waitKey(0)
        
    cv2.destroyAllWindows()

def img9_calculate(img, img_from_task):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    kernel = np.array([[-0.2,-0.2,-0.2],
                      [-0.2, 2.6,-0.2],
                      [-0.2,-0.2,-0.2]])

    
    # Apply the sharpening filter
    changedImg = cv2.filter2D(gray, -1, kernel)
    
    # Calculate MSE
    mse = np.mean((changedImg - img_from_task) ** 2)
    print(f"MSE between processed and task image: {mse}")

    cv2.imshow('Original', img)
    cv2.imshow('Task image', img_from_task)
    cv2.imshow('Edge Enhanced Result', changedImg)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

img = cv2.imread(r'I dont tell you\ImageProcessing2024_2025_HW3\q1\1.jpg')

img_from_task1 = cv2.imread(r'I dont tell you\ImageProcessing2024_2025_HW3\q1\image_1.jpg', 0)

img1_calculate(img, img_from_task1)

img_from_task2 = cv2.imread(r'I dont tell you\ImageProcessing2024_2025_HW3\q1\image_2.jpg', 0)

img2_calculate(img, img_from_task2)

img_from_task3 = cv2.imread(r'I dont tell you\ImageProcessing2024_2025_HW3\q1\image_3.jpg', 0)

img3_calculate(img, img_from_task3)

img_from_task4 = cv2.imread(r'I dont tell you\ImageProcessing2024_2025_HW3\q1\image_4.jpg', 0)

img4_calculate(img, img_from_task4)

img_from_task6 = cv2.imread(r'I dont tell you\ImageProcessing2024_2025_HW3\q1\image_6.jpg', 0)

img6_calculate(img, img_from_task6)

img_from_task7 = cv2.imread(r'I dont tell you\ImageProcessing2024_2025_HW3\q1\image_7.jpg', 0)

img7_calculate(img, img_from_task7)

img_from_task8 = cv2.imread(r'I dont tell you\ImageProcessing2024_2025_HW3\q1\image_8.jpg', 0)

img8_calculate(img, img_from_task8)

img_from_task9 = cv2.imread(r'I dont tell you\ImageProcessing2024_2025_HW3\q1\image_9.jpg', 0)

img9_calculate(img, img_from_task9)