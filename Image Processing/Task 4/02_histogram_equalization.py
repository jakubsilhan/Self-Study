import cv2
import numpy as np
import matplotlib.pyplot as plt 

'''
Does image equalization on an image (improves contrast)
'''

# Reading image
image = cv2.imread("./data/cv04_rentgen.bmp")
equalized = image.copy()

# Calculating the histogram
flat_img = image[:,:,0].ravel() # Assumed grayscale 1D array
histogram, _ = np.histogram(flat_img, bins=256, range=[0,256])

# Constants
lowest_intensity = 0 # start index for cum sum
min_intensity = 0 # lowest greyscale value
max_intensity = 255 # highest greyscale value
width = image.shape[0]
height = image.shape[1]

# Equalization
for y in range(0, width):
    for x in range(0,height):
        intensity = image[y,x,0]
        cum_intensity = np.sum(histogram[lowest_intensity:intensity+1]) # cum sum from zero to current intensity (to see where it lies in the distribution)
        equalized[y,x] = (max_intensity/(width*height))*cum_intensity # normalization (to spread values accros the distribution of 0-255)

# Image display
display = np.concatenate((image, equalized), axis=1)
cv2.imshow("Equalized image", display)
cv2.waitKey(0)

# Flatten equalized hist
flat_equal=equalized[:,:,0].ravel()
equal_hist, _ = np.histogram(flat_equal, bins=256, range=[0,256])

# Display hists
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.title("Original Histogram")
plt.bar(range(0,256), histogram, color='blue')
plt.subplot(1, 2, 2)
plt.title("Equalized Histogram")
plt.bar(range(0,256), equal_hist, color='green')
plt.tight_layout()
plt.show()