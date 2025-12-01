import os
from ultralytics import YOLO
import cv2 as cv

TEST_DIR = os.path.join("data", "test")
MODEL = os.path.join("runs", "detect", "train", "weights", "best.pt")

if __name__ == "__main__":
    images = []
    # Load images
    for image in os.listdir(TEST_DIR):
        img_path = os.path.join(TEST_DIR, image)
        image = cv.imread(img_path)

        images.append(image)

    model = YOLO(MODEL)

    # for image in images:
    results = model(images, save=True)
    
    print("Images processed!")