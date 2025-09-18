import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read image as grayscale
image = cv2.imread("./data/cv04c_robotC.bmp", cv2.IMREAD_GRAYSCALE) # 2D array

# Apply Fourier transform
fft2 = np.fft.fft2(image) # magnitude=intensity of frequency, phase=orientation/position

# Magnitude spectrum (shows frequency strength)
spectrum = np.abs(fft2)

# Shift spectrum to the center
shifted_spectrum = np.fft.fftshift(spectrum)

# Visualize amplitude spectrum
plt.subplot(1, 2, 1)
plt.imshow(np.log(spectrum), cmap='jet')
plt.title('Amplitude spectrum')
plt.colorbar()

plt.subplot(1, 2, 2)
plt.imshow(np.log(shifted_spectrum), cmap='jet')
plt.title('Shifted amplitude spectrum')
plt.colorbar()

plt.show()