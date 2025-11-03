import os
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import easyocr

def process_spz(path):
    # Load image
    im_bgr = cv.imread(os.path.join(path, "pvi_cv08_spz.png"))
    im_gr = cv.cvtColor(im_bgr, cv.COLOR_BGR2GRAY)
    im_rgb = cv.cvtColor(im_bgr, cv.COLOR_BGR2RGB)

    # Segmentation
    _, bw = cv.threshold(im_gr, 180, 255, cv.THRESH_BINARY_INV)
    # bw = cv.adaptiveThreshold(im_gr, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 35, 15)

    # Morphology
    # Close to fill inner
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
    closed = cv.morphologyEx(bw, cv.MORPH_CLOSE, kernel)

    # Open to remove letters
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (17,17))
    morph = cv.morphologyEx(closed, cv.MORPH_OPEN, kernel)

    # Harris edge detect
    fl_morph = morph
    dst = cv.cornerHarris(fl_morph, blockSize=7, ksize=15, k=0.1)
    dst = cv.dilate(dst, None)
    img_corners = im_rgb.copy()
    img_corners[dst>0.01*dst.max()] = [255, 0, 0]

    display_process(im_rgb, bw, morph, img_corners)

    # Create a rectangle to get angle
    corners = np.argwhere(dst > 0.01*dst.max())
    rect = cv.minAreaRect(corners[:, [1, 0]])
    center, (w, h), angle = rect

    # Normalize angle [-90, 90]
    if w < h:
        angle = 90+angle

    if angle > 90:
        angle -= 180
    elif angle < -90:
        angle += 180

    print(f"Angle: {angle}")
    # Rotation
    (h_im, w_im) = im_rgb.shape[:2]
    M = cv.getRotationMatrix2D(center, angle, 1.0)
    shift_x = 100 
    M[0,2] += shift_x
    rotated = cv.warpAffine(im_rgb, M, (h_im, w_im))
    
    # Text recognition
    reader = easyocr.Reader(['en'])
    result = reader.readtext(rotated)

    # Write text
    full_text = ''
    for (bbox, text, prob) in result:
        full_text += text
        full_text += " "

    cv.putText(rotated, full_text, (int(0), int(50)), cv.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)
    plt.imshow(rotated)
    plt.show()

def display_process(im_rgb, thresholded, morph, img_corners):
    plt.figure("Processing steps")
    plt.subplot(2,2,1)
    plt.imshow(im_rgb)
    plt.title("Orig. Im")

    plt.subplot(2,2,2)
    plt.imshow(thresholded, cmap="jet")
    plt.title("Bin. Im.")
    plt.colorbar()

    plt.subplot(2,2,3)
    plt.imshow(morph, cmap="jet")
    plt.title("Bin. Im. - Result")
    plt.colorbar()

    plt.subplot(2,2,4)
    plt.imshow(img_corners)
    plt.title("Im. + Harris")

    plt.show()

if __name__ == "__main__":
    data_dir = os.path.join("data")
    process_spz(data_dir)