import cv2
import numpy as np

images = {
    "./data/cv04_f01.bmp": "./data/cv04_e01.bmp",
    "./data/cv04_f02.bmp": "./data/cv04_e02.bmp"
}

for img_path, etal_path in images.items():
    # Read images and their characteristics
    image = cv2.imread(img_path)
    etalon = cv2.imread(etal_path)
    width, height, depth = image.shape

    # max intensity value
    c = 255

    # Copy of image to correct
    corrected = image.copy()

    # Replace zeros with ones to avoid divison errors
    safe_etalon = np.where(etalon == 0, 1, etalon)

    # Pixel by pixel brightness correction
    for y in range(0,width):
        for x in range(0, height):
            for z in range(0, depth):
                # Calculate brightness correction
                corrected[y,x,z] = (c*image[y,x,z])/(safe_etalon[y,x,z])

    # Prepare both images
    display = np.concatenate([image, corrected], axis=1)

    # Display both images
    cv2.imshow("Corrected images", display)

cv2.waitKey(0)