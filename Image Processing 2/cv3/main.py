import os
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
from scipy.fft import dctn

def display_spectrum(path):
    # Read image
    image = cv.imread(path)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image_gr = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    # Fourier Transform
    fft = np.fft.fft2(image_gr)
    # Log-Magnitude spectrum
    fft_m = np.log(np.abs(fft))
    # Centering the spectrum
    shifted = np.fft.fftshift(fft_m)

    # Display
    plt.subplot(1,2,1)
    plt.imshow(image)
    plt.title('Original image')

    plt.subplot(1,2,2)
    plt.imshow(shifted, cmap='jet')
    plt.title("Spectrum")
    plt.colorbar()

    plt.show()

def comparisons(image_folder):
    folder = image_folder
    image_files = os.listdir(folder)

    data = [preprocess(os.path.join(folder, image)) for image in image_files]

    hist_gr = plt.figure("Grayscale histograms")
    hist_hue = plt.figure("Hue histograms")
    dct_vec = plt.figure("DCT Vectors")

    dimension = len(data)

    for image_index, _ in enumerate(data):
        # Grayscale
        image_distances = [np.linalg.norm(data[image_index]["hist_gr"] - data[x]["hist_gr"]) for x,_ in enumerate(data)]
        np_image_distances = np.array(image_distances)
        indices = np.argsort(np_image_distances)

        for index in range(len(indices)):
            plt.figure(hist_gr)
            plt.subplot(dimension, dimension, (image_index*dimension)+index+1) # image*dimension=row, index+1 = column
            plt.imshow(data[indices[index]]["image"])
            plt.axis("off")

        # Hue
        image_distances = [np.linalg.norm(data[image_index]["hist_hue"]-data[x]["hist_hue"]) for x,_ in enumerate(data)]
        np_image_distances = np.array(image_distances)
        indices = np.argsort(np_image_distances)

        for index in range(len(indices)):
            plt.figure(hist_hue)
            plt.subplot(dimension, dimension, (image_index*dimension)+index+1) # image*dimension=row, index+1 = column
            plt.imshow(data[indices[index]]["image"])
            plt.axis("off")

        # DCT
        image_distances = [np.linalg.norm(data[image_index]["dct_vector"]-data[x]["dct_vector"]) for x,_ in enumerate(data)]
        np_image_distances = np.array(image_distances)
        indices = np.argsort(np_image_distances)

        for index in range(len(indices)):
            plt.figure(dct_vec)
            plt.subplot(dimension, dimension, (image_index*dimension)+index+1) # image*dimension=row, index+1 = column
            plt.imshow(data[indices[index]]["image"])
            plt.axis("off")

    hist_hue.show()
    hist_gr.show()
    dct_vec.show()


    input("Press enter to exit")



def preprocess(filepath: str) -> dict:
    """
    Loads image and its transforms
    """
    image = cv.imread(filepath)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image_gr = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    image_hsv = cv.cvtColor(image, cv.COLOR_RGB2HSV)

    # Grayscale histogram
    histogram_gr = cv.calcHist([image_gr], [0], None, [256], [0,256])
    # histogram_gr = cv.normalize(histogram_gr, histogram_gr).flatten()
    # Hue histograme
    histogram_hue = cv.calcHist([image_hsv], [0], None, [256], [0,256])
    # histogram_hue = cv.normalize(histogram_hue, histogram_hue).flatten()
    # DCT
    dctM = dctn(image_gr)
    R = 5
    dctRvec = dctM[0:R, 0:R].flatten()

    return {
        "image": image,
        "hist_gr": histogram_gr,
        "hist_hue": histogram_hue,
        "dct_vector": dctRvec

    }


if __name__ == "__main__":
    # Spectrum
    spectrum_path = os.path.join("images", "pvi_cv03_im09.jpg")
    display_spectrum(spectrum_path)

    comparisons("images")