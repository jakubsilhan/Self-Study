import os
from typing import Tuple
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

REFERENCE_PATH = os.path.join("data", "reference")
SOURCE_PATH = os.path.join("data","source")

def process():
    images = list()
    # Process images
    for image in os.listdir(SOURCE_PATH):
        image = cv.imread(os.path.join(SOURCE_PATH, image))
        images.append(find_closest(image))
    
    # Display results
    plt.figure()
    index = 1
    for source, reference in images:
        plt.subplot(2,3,index)
        plt.imshow(cv.cvtColor(source, cv.COLOR_BGR2RGB))
        index+=3
        plt.subplot(2,3,index)
        plt.imshow(cv.cvtColor(reference, cv.COLOR_BGR2RGB))
        index-=2
    plt.show()


def find_closest(image):
    # Source preparation
    image_gr = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    source_hist = cv.calcHist(image_gr.astype('uint8'), [0], None, [256], [0,256])

    # Initialize
    references = os.listdir(REFERENCE_PATH)
    distances = list()

    # Cycle through references
    for reference in references:
        # Prepare reference
        ref_im = cv.imread(os.path.join(REFERENCE_PATH, reference))
        ref_gr = cv.cvtColor(ref_im, cv.COLOR_BGR2GRAY)
        ref_hist = cv.calcHist(ref_gr.astype('uint8'), [0], None, [256], [0,256])

        # Calculate distance
        distances.append(np.abs(cv.compareHist(ref_hist, source_hist, cv.HISTCMP_CORREL)))
    
    # Select closest images
    closest_ref = references[np.argmax(distances)]
    closest_im = cv.imread(os.path.join(REFERENCE_PATH, closest_ref))

    # Return source and closest
    return image, closest_im

if __name__ == "__main__":
    process()