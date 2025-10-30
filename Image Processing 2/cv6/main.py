import os, math
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label
from scipy.signal import find_peaks

def process_image(path):
    # Load image
    image_bgr = cv.imread(path)
    image_rgb = cv.cvtColor(image_bgr, cv.COLOR_BGR2RGB)
    image_hue = cv.cvtColor(image_bgr, cv.COLOR_BGR2HSV)[:, :, 0]

    # Segmentation
    hist_hue = cv.calcHist([image_hue], [0], None, [180], [0,180])
    _, binary_hue = cv.threshold(image_hue, 45, 255, cv.THRESH_BINARY_INV)
    display_segmentation(image_rgb, image_hue, hist_hue, binary_hue)

    # Watershed
    watershed_mask = watershed(image_bgr, binary_hue)

    # Region coloring - to remove small cutoffs
    BWLabel, ncc = label(watershed_mask>127)

    min_size = 1000
    cleaned_mask = np.zeros_like(BWLabel, dtype=np.uint8)
    for i in range(1, ncc+1):
        region = (BWLabel == i)
        if np.sum(region) >= min_size:
            cleaned_mask[region] = 255
        
    display_coloring(watershed_mask, BWLabel, cleaned_mask)

    # Granulometric
    kernel_size = 0
    granulometric = np.zeros_like(cleaned_mask, dtype=np.uint8)
    while(True):
        kernel = np.ones((kernel_size,kernel_size), np.uint8)
        opened = cv.morphologyEx(cleaned_mask, cv.MORPH_OPEN, kernel) > 127

        if np.sum(opened) == 0:
            break

        granulometric += opened

        kernel_size+=1
    
    hist_gran = cv.calcHist([granulometric], [0], None, [256], [0,256])


    display_granulometry(granulometric, hist_gran)
    # Count objects
    sizes = list()
    for size in range(40, 255):
        count = hist_gran[size, 0]/(size*size)        
        if count>0.9:
            sizes.append((size, math.floor(count)))

    for size, count in sizes:
        print(f"No. objects: {count} size: {size}:{size}")


def display_segmentation(orig, hue, hist, seg):
    plt.figure("Segmentation")
    
    plt.subplot(2,2,1)
    plt.imshow(orig)
    plt.title("Original Image")

    plt.subplot(2,2,2)
    plt.imshow(hue, cmap="jet")
    plt.title("Hue Image")
    plt.colorbar()

    plt.subplot(2,2,3)
    plt.plot(hist)
    plt.title("Hue Image Histogram")

    plt.subplot(2,2,4)
    plt.imshow(seg, cmap="jet")
    plt.title("Image Segmentation")
    plt.colorbar()

    plt.show()

def watershed(image, mask):
    kernel = np.ones((3,3), np.uint8)
    opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv.dilate(opening, kernel, iterations=3)

    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
    _, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg, sure_fg)

    ret, markers = cv.connectedComponents(sure_fg)
    markers = markers + 1 # watershed requires bg to be 1
    markers[unknown == 255] = 0
    old_markers = markers.copy()

    markers = cv.watershed(image, markers)
    boundary = (markers == -1).astype(np.uint8) * 255
    dilate_boundary = cv.dilate(boundary, kernel)
    binary_watershed = cv.subtract(mask, dilate_boundary)

    display_watershed(dist_transform, sure_fg, unknown, old_markers, boundary, binary_watershed)

    return binary_watershed

def display_watershed(dist_trans, sure_fg, unknown, markers, watershed_border, binary_watershed):
    plt.figure("Watershed", figsize=(12, 8))
    
    plt.subplot(2,3,1)
    plt.imshow(dist_trans, cmap="jet")
    plt.title("Distance Transform")

    plt.subplot(2,3,2)
    plt.imshow(sure_fg, cmap="jet")
    plt.title("Sure Foreground")

    plt.subplot(2,3,3)
    plt.imshow(unknown > 127, cmap="jet")
    plt.title("Unknown Region")
    plt.colorbar()

    plt.subplot(2,3,4)
    plt.imshow(markers, cmap="jet")
    plt.title("Markers")
    plt.colorbar()

    plt.subplot(2,3,5)
    plt.imshow(watershed_border > 127, cmap="jet")
    plt.title("Watershed Border")
    plt.colorbar()

    plt.subplot(2,3,6)
    plt.imshow(binary_watershed > 127, cmap="jet")
    plt.title("Binary Image with Watershed")
    plt.colorbar()

    plt.tight_layout()
    plt.show()

def display_coloring(watershed, coloring, cleaned):
    plt.figure("Coloring")

    plt.subplot(1,3,1)
    plt.imshow(watershed, cmap="jet")
    plt.title("Binary Image with Watershed")
    plt.colorbar()

    plt.subplot(1,3,2)
    plt.imshow(coloring, cmap="jet")
    plt.title("Region ident")
    plt.colorbar()

    plt.subplot(1,3,3)
    plt.imshow(cleaned, cmap="jet")
    plt.title("Result - Binary map")
    plt.colorbar()

    plt.show()

def display_granulometry(granulometry, hist):
    plt.figure("Granulometry")

    plt.subplot(1,2,1)
    plt.imshow(granulometry, cmap="jet")
    plt.title("Result - Granulometry")
    plt.colorbar()

    plt.subplot(1,2,2)
    plt.plot(hist)
    hist_plt = plt.title("Granul. Image Histogram")
    ax = plt.gca()
    ax.set_xlim([40, 80])
    ax.set_ylim([0,16000])
    plt.xlabel("Value")
    plt.ylabel("#")

    plt.show()


if __name__ == "__main__":
    image_path = os.path.join("data", "pvi_cv06_mince.jpg")
    process_image(image_path)
