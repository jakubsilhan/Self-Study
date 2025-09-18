import cv2
import numpy as np
import matplotlib.pyplot as plt

'''
Spectrum shows frequency of brightness changes of specific speed (big change/small change)
 - low pass removes high frequencies (removes edges) and blurs the image
 - high pass removes low frequencies (removes plain parts) and emphasizes outlines 
'''


# Read and normalize image
image = cv2.imread("./data/cv04c_robotC.bmp", cv2.IMREAD_GRAYSCALE) / 255

# FFT transform and shift to center
robot = np.fft.fftshift(np.fft.fft2(image))

# Load filter masks and normalize them
filters = ["./data/cv04c_filtDP.bmp", "./data/cv04c_filtDP1.bmp", "./data/cv04c_filtHP.bmp", "./data/cv04c_filtHP1.bmp"]
matrices = [cv2.imread(x, cv2.IMREAD_GRAYSCALE) / 255 for x in filters]

# Apply filters
spectrums = [robot * x for x in matrices]

# Inverse FFT into images(reverse shift, inverse fft, discard phase)
images = [np.abs(np.fft.ifft2(np.fft.ifftshift(x))) for x in spectrums]

# Display
rows = len(filters)
cols = 4
for k in range(rows):
    plt.subplot(rows, cols, (rows * k) + 1)
    plt.imshow(image, cmap="gray")

    plt.subplot(rows, cols, (rows * k) + 2)
    plt.imshow(matrices[k], cmap='gray')

    plt.subplot(rows, cols, (rows * k) + 3)
    plt.imshow(images[k], cmap='gray')

    plt.subplot(rows, cols, (rows * k) + 4)
    plt.imshow(np.log(np.abs(spectrums[k])), cmap='jet')

plt.show()
