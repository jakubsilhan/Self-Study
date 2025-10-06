import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def noise_removal(path: str):
    """
    Tests different image smoothing methods
    """
    orig_gr = cv.imread(path, cv.IMREAD_GRAYSCALE)
    orig_hist = calculate_hist(orig_gr)
    orig_spect = calculate_spectrum(orig_gr)

    # Averaging - average smoothing
    avg_gr = cv.blur(orig_gr, (3,3))
    avg_hist = calculate_hist(avg_gr)
    avg_spect = calculate_spectrum(avg_gr)

    display_smoothing("Image Smoothing - Average", orig_gr, avg_gr, orig_hist, avg_hist, orig_spect, avg_spect)

    # Median - median smoothing
    blur_gr = cv.medianBlur(orig_gr, 5)
    blur_hist = calculate_hist(blur_gr)
    blur_spect = calculate_spectrum(blur_gr)

    display_smoothing("Image Smoothing - Median", orig_gr, blur_gr, orig_hist, blur_hist, orig_spect, blur_spect)

    # Custom median
    cust_gr = calculate_median(orig_gr, 5)
    cust_hist = calculate_hist(cust_gr)
    cust_spect = calculate_spectrum(cust_gr)

    display_smoothing("Image Smoothing - Median Custom", blur_gr, cust_gr, blur_hist, cust_hist, blur_spect, cust_spect)


def display_smoothing(name: str, image, image_sm, hist, hist_sm, spect, spect_sm):
    """
    Displays smoothing results
    """
    figure = plt.figure(name, figsize=(8,8))
    figure.tight_layout()
    plt.subplot(2,3,1)
    plt.imshow(image, cmap='gray')
    plt.title("Original image")

    plt.subplot(2,3,2)
    plt.plot(hist)
    plt.title("Histogram")

    plt.subplot(2,3,3)
    plt.imshow(spect, cmap='jet')
    plt.title("Spectrum")
    plt.colorbar()

    plt.subplot(2,3,4)
    plt.imshow(image_sm, cmap='gray')
    plt.title("New image")

    plt.subplot(2,3,5)
    plt.plot(hist_sm)
    plt.title("Histogram")

    plt.subplot(2,3,6)
    plt.imshow(spect_sm, cmap='jet')
    plt.title("Spectrum")
    plt.colorbar()

    plt.show()


def calculate_median(image_gr, kernel_size):
    """
    Looks at a n*n region around the pixel and replaces the pixels value with the region median
    """
    edge = kernel_size//2

    smoothed = np.copy(image_gr)

    for y in range(edge,image_gr.shape[0]-(edge+1)):
        for x in range(edge, image_gr.shape[1]-(edge+1)):
            neighborhood = image_gr[y:y+kernel_size, x:x+kernel_size] # extract region

            smoothed[y,x] = np.median(neighborhood)

    return smoothed

def calculate_hist(image_gr: np.ndarray):
    """
    Calculates greyscale histogram
    """
    histogram = cv.calcHist([image_gr], [0], None, [256], [0,256])
    return histogram


def calculate_spectrum(image_gr: np.ndarray) -> np.ndarray:
    """
    Calculates greyscale spectrum
    """
    # Fourier Transform
    fft = np.fft.fft2(image_gr)
    # Log-Magnitude spectrum
    fft_m = np.log(np.abs(fft))
    # Centering the spectrum
    shifted = np.fft.fftshift(fft_m)

    return shifted

if __name__ == "__main__":
    image_path = os.path.join("data1", "pvi_cv04.png")
    noise_removal(image_path)