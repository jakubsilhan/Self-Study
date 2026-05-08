import os
from ultralytics import YOLO
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

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

    # Annotates images
    results = model(images, save=False)
    image_n = 0

    for result, image in zip(results,images):
        boxes = result.boxes.xyxy
        confidences = result.boxes.conf
        image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        plt.figure()
        for box, conf in zip(boxes, confidences):
            x1 = np.int32(box[0].item())
            y1 = np.int32(box[1].item())
            x2 = np.int32(box[2].item())
            y2 = np.int32(box[3].item())
            cv.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
            text_y = max(20, y1-10)
            cv.putText(image_rgb, f"{conf:.2f}", (x1, text_y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,255), 2)
        plt.imshow(image_rgb)
        plt.title(f"Image {image_n}")
        plt.show()
        image_n += 1


    
    print("Images processed!")