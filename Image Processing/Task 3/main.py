import cv2
import numpy as np
import math

'''
Image matrices are [y,x,z], but all the other formats are saved as [x,y]
'''

def rotate_image(filename: str, rotation: int):
    orig_image = cv2.imread(filename) # [y,x,z]
    
    # Shape
    height, width = orig_image.shape[:2] # First two values (y, x)

    # Original center
    orig_center = np.array([width//2, height//2]) # // full number division [x, y]

    # Degree to radian conversion
    rotation = rotation%360
    rad = math.radians(rotation)

    # Rotation matrix
    rotation_matrix = np.array([
        [np.cos(rad), -np.sin(rad)],
        [np.sin(rad), np.cos(rad)]
    ])

    # dimensions
    orig_dim = np.array([[width, height]]*2) # -> [2,2] [[width,height],[width,height]]
    new_dim = np.abs(rotation_matrix*orig_dim).sum(axis=0)

    # Inversion rotation matrix
    inv_rotation_matrix = np.linalg.inv(rotation_matrix)

    # New image center
    new_center = new_dim//2 # [x,y]

    # New image initialization
    new_image = np.zeros((int(new_dim[1]), int(new_dim[0]),3), dtype=np.uint8) # [y,x,z]

    # Rotation pixel wise
    for i in range(new_image.shape[0]): # rows
        for j in range(new_image.shape[1]): # columns
            # Calculating the cords in original image
            original_cords = np.dot(inv_rotation_matrix, np.array([j-new_center[0], i-new_center[1]])) # [x, y]
            x, y = original_cords + orig_center

            # Transfering color from original image cords to new image cords
            if 0<=x<width and 0<=y<height:
                new_image[i,j,:] = orig_image[int(y),int(x),:] 
    return new_image

if __name__ == "__main__":
    rotated_image = rotate_image("./data/cv03_robot.bmp", 90)
    cv2.imshow("Rotated image", rotated_image)
    cv2.waitKey(0)