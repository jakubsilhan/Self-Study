import os
from enum import Enum
import cv2 as cv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

ORG = (20,100) 
FONT = cv.FONT_HERSHEY_SIMPLEX
FONTSCALE = 1
COLORT = (0,0,0)
THICKNESS = 2

class Color(Enum):
    BILA=0
    SEDA=1
    CERNA=2
    CERVENA=3
    ZELENA=4
    MODRA=5
    ZLUTA=6
    ORANZOVA=7
    FIALOVA=8
    RUZOVA=9
    HNEDA=10 

def pixel_color(pixel) -> Color:
    """
    Returns the color of the pixel
    """
    Hue = pixel[0]
    Saturation = pixel[1]
    Value = pixel[2]
    if Saturation < 30:
        if Value > 240:
            return Color.BILA
        if Value < 15:
            return Color.CERNA
        else:
            return Color.SEDA

    if Hue < 15 or Hue >= 170:
        return Color.CERVENA
    elif 40 <= Hue and Hue <80:
        return Color.ZELENA
    elif 80 <= Hue and Hue < 135:
        return Color.MODRA
    elif 25 <= Hue and Hue < 35:
        return Color.ZLUTA
    elif 10 <= Hue and Hue <25:
        return Color.ORANZOVA
    elif 135 <= Hue and Hue < 170:
        if Saturation < 175:
            return Color.RUZOVA
        return Color.FIALOVA
    else:
        return Color.CERNA

def image_distribution(bgr_im) -> defaultdict:
    """
    Calculates color distribution in the image
    """
    colors = defaultdict(int)

    # Acumulates color counts
    hsv_im = cv.cvtColor(bgr_im, cv.COLOR_BGR2HSV)
    height, width = hsv_im.shape[:2]
    for y in range(height):
        for x in range(width):
            colors[pixel_color(hsv_im[y,x,:])] +=1
    
    return colors

def grid_colors(image, grid_size):
    """
    Splits image into a square grid and assigns color to each square
    """
    bgr_im = cv.imread(image)
    rgb_im = cv.cvtColor(bgr_im, cv.COLOR_BGR2RGB)

    # Calculate image split
    height, width = bgr_im.shape[:2]
    square_h = round(height/grid_size)
    square_w = round(width/grid_size)
    
    # Initialize result image
    result_im = np.zeros([height, width, 3], dtype=np.int32)

    for y in range(0, grid_size):
        for x in range(0, grid_size):
            # Prepare image conversions for square
            square_im = bgr_im[y*square_h:(y+1)*square_h, x*square_w:(x+1)*square_w,:]
            square_im_rgb = cv.cvtColor(square_im, cv.COLOR_BGR2RGB)

            # Calculate most common color
            dist = image_distribution(square_im)
            top_color = sorted(dist.items(), key=lambda x: x[1], reverse=True)[:1]
            color_t = str(top_color[0][0].name)
            
            # Write color into image
            if color_t == 'CERNA':
                anot_im = cv.putText(square_im_rgb, color_t, ORG, FONT, FONTSCALE, (255,255,255), THICKNESS, cv.LINE_AA)
            else:
                anot_im = cv.putText(square_im_rgb, color_t, ORG, FONT, FONTSCALE, COLORT, THICKNESS, cv.LINE_AA)
            
            # Write square into result image
            result_im[y*square_h:(y+1)*square_h, x*square_w:(x+1)*square_w,:] = anot_im

    return result_im


def most_common(image):
    """
    Finds the top3 colors in the image
    """
    # Prepare image
    bgr_im  = cv.imread(image)
    rgb_im = cv.cvtColor(bgr_im, cv.COLOR_BGR2RGB)
    height, width = bgr_im.shape[:2]
    total = height*width

    # Calculate top 3 colors
    distribution = image_distribution(bgr_im=bgr_im)
    top3 = sorted(distribution.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Write top 3 colors
    fontscale = 0.4
    thickness = 2
    orgx = 10
    orgy = 10
    for color, count in top3:
        text = str(color.name) + ": " +str(round(count/total*100, 2)) + "%"
        im = cv.putText(rgb_im, text, (orgx, orgy+30), FONT, fontscale, (0,255,0), thickness, cv.LINE_AA)
        orgy+=30
    return im

if __name__ == "__main__":
    image = os.path.join("data", "cv02_01.bmp")
    im = grid_colors(image, 3)
    plt.imshow(im)
    plt.show()

    image1 = os.path.join("data", "cv01_u01.jpg")
    image1 = most_common(image1)
    plt.subplot(1,3,1)
    plt.imshow(image1)

    image2 = os.path.join("data", "cv01_u02.jpg")
    image2 = most_common(image2)
    plt.subplot(1,3,2)
    plt.imshow(image2)

    image3 = os.path.join("data", "cv01_u03.jpg")
    image3 = most_common(image3)
    plt.subplot(1,3,3)
    plt.imshow(image3)

    plt.show()
    