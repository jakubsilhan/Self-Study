import os
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

def detect_edges(folder: str):
    """
    Uses canny edge detector to detect edges in image
    """
    images = os.listdir(folder)

    plt.figure("Edge detection")
    plt.subplots_adjust(wspace=0.5)
    plot_index = 1

    for image in images:
        # Reads image and detects edges
        image_path = os.path.join(folder, image)
        image_gr = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
        image_edge = cv.Canny(image_gr, 100, 256)

        # Converts to a binary mask (0 or 1)
        binary_gr = cv.threshold(image_gr, 180, 255, cv.THRESH_BINARY)[1] > 0
        binary_edge = cv.threshold(image_edge, 180, 255, cv.THRESH_BINARY)[1] > 0

        # Plot image mask
        plt.subplot(2, len(images), plot_index)
        plt.imshow(binary_gr, cmap='jet')
        plt.title(np.sum(binary_gr))
        plt.colorbar()

        # Plot edge mask
        plt.subplot(2, len(images), plot_index+len(images))
        plt.imshow(binary_edge, cmap='jet')
        plt.title(np.sum(binary_edge))
        plt.colorbar()

        plot_index +=1

    plt.show()


if __name__ == "__main__":
    data_folder = os.path.join("data2")
    detect_edges(data_folder)