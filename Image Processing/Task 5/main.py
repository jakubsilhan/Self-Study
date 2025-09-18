import cv2
import numpy as np
import matplotlib.pyplot as plt


"""
Using smoothing to do noise reduction in images
"""

def crop(image, x, y, size):
    """
    Retrieves a square patch of size from image
    """
    top = max(y-size//2,0)
    bottom = min(y+size//2+1,image.shape[0])
    left = max(x-size//2,0)
    right = min(x+size//2+1,image.shape[1])

    return image[top:bottom,left:right]

def average_with_rotating_mask(image):
    """
    Uses the most uniform local region around the pixel and averages within the region to replace said pixel
    """
    size = 3
    copy = np.zeros(image.shape)

    # pixel loop
    for y in range(0, image.shape[0]):
        for x in range(0, image.shape[1]):
            # Mask for offset of each of the eight surrounding pixels
            """
                    M1       M2       M3
                (x-1,y-1) (x-1,y) (x-1,y+1)

                    M4        C       M5
                (x, y-1)  (x, y)  (x, y+1)

                    M6       M7       M8
                (x+1,y-1) (x+1,y) (x+1,y+1)
                * indexes may not be completely correct
            """
            mask_1 = crop(image, x - 1, y - 1, size)
            mask_2 = crop(image, x - 1, y + 0, size)
            mask_3 = crop(image, x - 1, y + 1, size)
            mask_4 = crop(image, x,     y - 1, size)
            mask_5 = crop(image, x,     y + 1, size)
            mask_6 = crop(image, x + 1, y - 1, size)
            mask_7 = crop(image, x + 1, y + 0, size)
            mask_8 = crop(image, x + 1, y + 1, size)

            masks = [mask_1, mask_2, mask_3, mask_4, mask_5, mask_6, mask_7, mask_8]
            
            # Find the smoothest region
            lowest_variance_index = np.argmin([np.var(x) for x in masks])

            # Replace pixel with the average of the smoothest region
            copy[y, x] = np.mean(masks[lowest_variance_index])

    return copy

# Loading image
image = cv2.imread("./data/cv05_robotS.bmp", cv2.IMREAD_GRAYSCALE)

# Kernel size for mean filter
kernel = 1/9 * np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
])

# Simple mean (blurs evenly)
mean = cv2.filter2D(src=image, ddepth=1, kernel=kernel)

# Adaptive smoothing
rotation = average_with_rotating_mask(image)

# Replaces pixel with median of its size*size neighborhood
median = cv2.medianBlur(image, 3)


# Display
rows = 2
cols = 4

plt.subplot(rows, cols, 1)
plt.imshow(image, cmap="gray")
plt.title("Input")

plt.subplot(rows, cols, 2)
plt.imshow(np.log(np.abs(np.fft.fftshift(np.fft.fft2(image)))), cmap='jet')
plt.title("Spectrum")

plt.subplot(rows, cols, 3)
plt.imshow(mean, cmap="gray")
plt.title("Result - Simple mean")

plt.subplot(rows, cols, 4)
plt.imshow(np.log(np.abs(np.fft.fftshift(np.fft.fft2(mean)))), cmap='jet')
plt.title("Spectrum - Simple mean")

plt.subplot(rows, cols, 5)
plt.imshow(rotation, cmap="gray")
plt.title("Result - Rotating mask")

plt.subplot(rows, cols, 6)
plt.imshow(np.log(np.abs(np.fft.fftshift(np.fft.fft2(rotation)))), cmap='jet')
plt.title("Spectrum - Rotating mask")

plt.subplot(rows, cols, 7)
plt.imshow(median, cmap="gray")
plt.title("Result - Median")

plt.subplot(rows, cols, 8)
plt.imshow(np.log(np.abs(np.fft.fftshift(np.fft.fft2(median)))), cmap='jet')
plt.title("Spectrum - Median")


plt.show()