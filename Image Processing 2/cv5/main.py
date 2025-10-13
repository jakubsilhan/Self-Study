import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label


def process_image(path):
    """Processes image for object labeling"""
    # Load image and convert to gray and hue
    image_bgr = cv.imread(path)
    image_rgb = cv.cvtColor(image_bgr, cv.COLOR_BGR2RGB)
    image_gr = cv.cvtColor(image_bgr, cv.COLOR_BGR2GRAY)
    image_hue = cv.cvtColor(image_bgr, cv.COLOR_BGR2HSV)[:,:,0]

    # Prepare hue mask
    hue_mask = mask_calculation(image_gr, image_hue)

    # Label objects
    classification(image_rgb, hue_mask, 3)

def mask_calculation(image_gr, image_hue):
    """Calculate grayscale and hue masks"""
    # Calculate hists
    hist_gr = cv.calcHist([image_gr], [0], None, [256], [0,256])
    hist_hue = cv.calcHist([image_hue], [0], None, [256], [0,256])

    # Treshold into binary images
    _, binary_gr = cv.threshold(image_gr, 150, 1, cv.THRESH_BINARY)
    _, binary_hue = cv.threshold(image_hue, 80, 1, cv.THRESH_BINARY_INV)

    # Display
    figure = plt.figure("Simple thresholding", figsize=(10,10))
    figure.tight_layout()

    plt.subplot(3,3,1)
    plt.imshow(image_gr, cmap='gray')
    plt.title("Gray Image")
    plt.colorbar()

    plt.subplot(3,3,2)
    plt.plot(hist_gr)
    plt.title("Gray Image Histogram")

    plt.subplot(3,3,3)
    plt.imshow(binary_gr, cmap="jet")
    plt.title("Binary Image from Gray")
    plt.colorbar()

    plt.subplot(3,3,4)
    plt.imshow(image_hue, cmap="jet")
    plt.title("Hue Image")
    plt.colorbar()

    plt.subplot(3,3,5)
    plt.plot(hist_hue)
    plt.title("Hue Image Histogram")

    plt.subplot(3,3,6)
    plt.imshow(binary_hue, cmap="jet")
    plt.title("Binary Image from Hue")
    plt.colorbar()

    plt.show()

    return binary_hue

def classification(image, hue_mask, kernel_size=5):
    """Complete classification task"""
    # Morphology
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (kernel_size, kernel_size))
    opened = cv.morphologyEx(hue_mask, cv.MORPH_OPEN, kernel)
    display_morphology(hue_mask, opened)

    # Region Coloring
    BWLabel, ncc = label(opened)
    display_coloring(opened, BWLabel)

    # Regions
    regions = find_regions(BWLabel, ncc)
    display_counts(image, regions)

    # Labeling
    display_labels(image, regions)

def display_morphology(initial, post_morphology):
    """Display morphology operation result"""
    figure = plt.figure("Morphology")

    plt.subplot(1,2,1)
    plt.imshow(initial, cmap="jet")
    plt.title("Binary Image from Hue")
    plt.colorbar()

    plt.subplot(1,2,2)
    plt.imshow(post_morphology, cmap="jet")
    plt.title("Binary Image from Hue - Opening")
    plt.colorbar()

    plt.show()

def display_coloring(initial, colored):
    """Display region coloring result"""
    figure = plt.figure("Morphology")

    plt.subplot(1,2,1)
    plt.imshow(initial, cmap="jet")
    plt.title("Binary Image from Hue - Opening")
    plt.colorbar()

    plt.subplot(1,2,2)
    plt.imshow(colored, cmap="jet")
    plt.title("Binary Image from Hue - Label")
    plt.colorbar()

    plt.show()

def find_regions(labeled: np.ndarray, label_count):
    """Find region centroids and areas"""
    regions = []
    # Create a region dict for each label
    for label in range(1,label_count+1):
        
        # Binary mask for label
        mask = (labeled == label).astype(np.uint8)

        # Calculate label area
        area = np.sum(mask)
        
        # Get all nonzero indices for each dimension
        ys, xs = np.nonzero(mask)

        # Calculate centroid coordinates
        x = np.mean(xs)
        y = np.mean(ys)

        # Save into a dict
        region = {
            "area": area,
            "centroid": (y,x)
        }
        regions.append(region)
    
    return regions

def display_counts(image, regions):
    """Displays pixel count for each object"""
    image = image.copy()
    font = cv.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = (0, 0, 255)
    thickness = 1
    for region in regions:
        y, x = region["centroid"]
        size = region["area"]

        cv.putText(image, str(size), (int(x),int(y)), font, fontScale, color, thickness, cv.LINE_AA)

    plt.figure("Regions")
    plt.imshow(image)
    plt.show()
        
def display_labels(image, regions):
    """Dusokays label for each object"""
    image = image.copy()
    font = cv.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    color = (0, 0, 255)
    thickness = 1
    for region in regions:
        y, x = region["centroid"]
        size = region["area"]

        cv.putText(image, classify_region(size), (int(x),int(y)), font, fontScale, color, thickness, cv.LINE_AA)

    plt.figure("Classification")
    plt.imshow(image)
    plt.show()

def classify_region(size):
    """Assign label according to area"""
    if size < 4000:
        return "1 Kc"
    elif size < 4500:
        return "2 Kc"
    elif size < 5100:
        return "5 Kc"
    else :
        return "10 Kc"

if __name__ == "__main__":

    image_path = os.path.join("data", "pvi_cv05_mince_noise.png")
    process_image(image_path)