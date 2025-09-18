import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
Edge detection highlights rapid color/brightness changes in image
"""

# Loading an image
image = cv2.imread("./data/cv06_robotC.bmp", cv2.IMREAD_GRAYSCALE)
image = image.astype(np.float32)

# Display preparation
rows = 4
cols = 2

# Laplace edge detection - checks second derivative in intensity
laplace_kernel = np.array([
    [0, 1, 0],
    [1, -4, 1],
    [0, 1, 0]
])
laplacian = cv2.filter2D(image, -1, laplace_kernel)

# Sobel edge detection - checks first derivative (smaller weights)
sobel_kernel = np.array([
    [1, 2, 1],
    [0, 0, 0],
    [-1, -2, -1]
])

sobel_images = [cv2.filter2D(image, -1, np.rot90(sobel_kernel, x)) for x in range(8)]
sobel = np.max(sobel_images, axis=0)

# Kirsch edge detection - checks first derivative (bigger weights)
kirsch_kernel = np.array([
    [3, 3, 3],
    [3, 0, 3],
    [-5, -5, -5]
])

kirsch_images = [cv2.filter2D(image, -1, np.rot90(kirsch_kernel, x)) for x in range(8)]

kirsch = np.max(kirsch_images, axis=0)

# Display
plt.subplot(rows, cols, 1)
plt.imshow(image, cmap="gray")
plt.title("Original")

plt.subplot(rows,cols,2)
plt.imshow(np.log(np.abs(np.fft.fftshift(np.fft.fft2(image)))), cmap="jet")
plt.title("Spectrum")

plt.subplot(rows, cols, 3)
plt.imshow(laplacian, cmap="jet")
plt.title("Result - Laplacian")

plt.subplot(rows, cols, 4)
plt.imshow(np.log(np.abs(np.fft.fftshift(np.fft.fft2(laplacian)))), cmap="jet")
plt.title("Spectrum - Laplacian")

plt.subplot(rows, cols, 5)
plt.imshow(sobel, cmap="jet")
plt.title("Result - Sobel")

plt.subplot(rows, cols, 6)
plt.imshow(np.log(np.abs(np.fft.fftshift(np.fft.fft2(sobel)))), cmap="jet")
plt.title("Spectrum - Sobel")

plt.subplot(rows, cols, 7)
plt.imshow(kirsch, cmap="jet")
plt.title("Result - Kirsch")

plt.subplot(rows, cols, 8)
plt.imshow(np.log(np.abs(np.fft.fftshift(np.fft.fft2(kirsch)))), cmap="jet")
plt.title("Spectrum - Kirsch")

plt.show()
