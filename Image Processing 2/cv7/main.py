import os
import cv2 as cv
import numpy as np

"""
Text processing based on vector projection
"""
def text_processing(path):
    # Load main
    text_bgr = cv.imread(os.path.join(path, "pvi_cv07_text.bmp"))
    text_gr = cv.cvtColor(text_bgr, cv.COLOR_BGR2GRAY)
    _, bw = cv.threshold(text_gr, 128, 1, cv.THRESH_BINARY_INV)
    binary = (bw>0).astype(np.uint8)
    
    # Load letters
    template_dir = os.path.join(path, "dir_znaky")
    templates = load_templates(template_dir)
    print(templates)

    # Region coloring
    num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(binary, connectivity=8)

    # Assign char to each region
    char_regions = []
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        cut_char = binary[y:y+h, x:x+w]
        feature_vec = feature_vector_calculation(cut_char)

        # Compare with each template and get closest char
        best_char = None
        best_dist = float('inf')
        for char, temp_vec in templates.items():
            d = np.linalg.norm(feature_vec - temp_vec) # euclid distance
            if d < best_dist:
                best_dist = d
                best_char = str(char)
        char_regions.append((x, y, best_char, best_dist))
        
    # Print translated text
    text_out = ""
    for x, y, letter, _ in char_regions:
        text_out += letter

    print("Rozpoznaný text")
    print(text_out)

def load_templates(template_dir):
    templates = {}
    for filename in os.listdir(template_dir):
        name, ext = os.path.splitext(filename)

        key = name.upper()
        # Convert to gray
        img_bgr = cv.imread(os.path.join(template_dir, filename))
        img_gr = cv.cvtColor(img_bgr, cv.COLOR_BGR2GRAY) 
        if img_gr is None:
            continue

        # Segment
        _, bw = cv.threshold(img_gr, 128, 1, cv.THRESH_BINARY_INV)

        # Calculate feature vector via projection
        fv = feature_vector_calculation(bw)
        templates[key] = fv
    return templates

def feature_vector_calculation(binary):
    # Horizontal projection (sum pixels for each column)
    horizontal = np.sum(binary, axis=1)
    # Vertical projection (sum pixels for each row)
    vertical = np.sum(binary, axis=0)

    feature_vector = np.concatenate((horizontal, vertical))
    return feature_vector

"""
Image processing using Haarcascade
"""
def image_processing(root_path):
    # Load data
    image_bgr = cv.imread(os.path.join(root_path, "pvi_cv07_people.jpg"))
    image_rgb = cv.cvtColor(image_bgr, cv.COLOR_BGR2RGB)
    image_gr = cv.cvtColor(image_bgr, cv.COLOR_BGR2GRAY) 

    # Load ground truth
    boxes = []
    with open(os.path.join(root_path, "pvi_cv07_boxes_01.txt")) as f:
        lines = f.read().splitlines()
        for line in lines:
            vec = [int(x) for x in line.split()] 
            boxes.append(vec)

    # Draw ground truth
    for (x, y, w, h) in boxes:
        cv.rectangle(image_bgr, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Detect faces
    faceCascade = cv.CascadeClassifier(os.path.join(root_path, "pvi_cv07_haarcascade_frontalface_default.xml"))
    faces = faceCascade.detectMultiScale(image_gr, scaleFactor=1.4, minNeighbors=5, minSize=(30,30), flags=cv.CASCADE_SCALE_IMAGE)

    # Draw predictions
    for (x, y, w, h) in faces:
        cv.rectangle(image_bgr, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display
    cv.imshow("Image processing", image_bgr)
    cv.waitKey()

    # Calculate detection metrics
    calculate_metrics(boxes, faces)


def calculate_metrics(boxes, faces):
    # Calculate detection metrics
    true_positive = 0
    for box in boxes:
        for face in faces:
            iou = get_iou(box, face)
            if iou < 0.5:
                continue
            true_positive += 1

    false_positive = len(faces)-true_positive #  all found - real found
    false_negative = len(boxes)-true_positive # real - real found
    true_negative = 0

    # Metric calculation
    accuracy = (true_positive+true_negative)/(true_positive+true_negative+false_positive+false_negative)
    precision = true_positive/(true_positive+false_positive)
    recall = true_positive/(true_positive+false_negative)

    print(f"Accuracy: {accuracy}\nPrecision: {precision}\nRecall: {recall}")

def get_iou(ground, pred):
    # Calculation of area of overlap
    x1 = max(ground[0], pred[0])
    y1 = max(ground[1], pred[1])
    x2 = min(ground[0]+ground[2], pred[0]+pred[2])
    y2 = min(ground[1]+ground[3], pred[1]+pred[3])

    intersect = max(0, x2-x1)*max(0, y2-y1)

    ref = ground[2]*ground[3]
    rec = pred[2]*pred[3]
    union = ref+rec-intersect

    return intersect/union


if __name__ =="__main__":
    text_path = os.path.join("text")
    text_processing(text_path)

    image_path = os.path.join("faces")
    image_processing(image_path)