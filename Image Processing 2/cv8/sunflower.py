import os
import cv2 as cv
import matplotlib.pyplot as plt
from skimage.feature import blob_log
from scipy.stats import entropy


THRESHOLD = 0.60

def load_template(path, display=True):
    """
    Load, calculate and normalize template hue histogram
    """
    template_bgr = cv.imread(path)
    template_rgb = cv.cvtColor(template_bgr, cv.COLOR_BGR2RGB)
    template_hue = cv.cvtColor(template_bgr, cv.COLOR_BGR2HSV)[:, :, 0]

    hist_hue = cv.calcHist([template_hue], [0], None, [180], [0,180])
    hist_hue = hist_hue / hist_hue.sum()


    if not display:
        return hist_hue
    
    plt.figure("Template")
    plt.subplot(1,2,1)
    plt.imshow(template_rgb)
    plt.title("Original")
    plt.subplot(1,2,2)
    plt.plot(hist_hue)
    plt.title("Hue histogram")
    plt.show()


def process_sunflowers(data_dir):
    """
    Work through sunflower images
    """
    template_path = os.path.join(data_dir, "pvi_cv08_sunflower_template.jpg")
    tmp_hist = load_template(template_path, display=False)

    # Parse paths
    img_dir = os.path.join(data_dir, "samples", "imgs")
    gt_dir = os.path.join(data_dir, "samples", "gt")
    images = os.listdir(img_dir)
    gts = os.listdir(gt_dir)
    for image in images:
        name, ext = os.path.splitext(image)
        gt_file = gts[gts.index(name+".txt")]

        image_path = os.path.join(img_dir, image)
        gt_path = os.path.join(gt_dir, gt_file)
        process(image_path, gt_path, tmp_hist, name)


def process(image_path, gt_path, tmp_hist, name):
    """
    Process sunflower image
    """
    image_bgr = cv.imread(image_path)
    image_gr = cv.cvtColor(image_bgr, cv.COLOR_BGR2GRAY)
    image_rgb = cv.cvtColor(image_bgr, cv.COLOR_BGR2RGB)
    image_hue = cv.cvtColor(image_bgr, cv.COLOR_BGR2HSV)[:,:,0]
    max_y, max_x = image_bgr.shape[:2]

    pred_im = image_rgb.copy()
    gt_im = image_rgb.copy()

    # Load GTs
    boxes = load_boxes(gt_path)
    draw_boxes(gt_im, boxes)

    # Find blobs
    blobs = blob_log(255-image_gr, min_sigma=1, overlap=0.5) # Requires inversion

    # display_found(image_rgb, blobs)

    pred_boxes = []
    for blob in blobs:
        y = blob[0]
        x = blob[1]
        sigma = 4*blob[2]

        # Calculating coords
        x1 = int(max(x-sigma/2, 0))
        x2 = int(min(x+sigma/2, max_x))
        y1 = int(max(y-sigma/2, 0))
        y2 = int(min(y+sigma/2, max_y))

        # Slicing the square
        square = image_hue[y1:y2, x1:x2]
        # Hist
        square_hist = cv.calcHist([square], [0], None, [180], [0,180])
        square_hist = square_hist / square_hist.sum()

        # Compare with template
        metric = entropy(square_hist+0.001, tmp_hist+0.001)
        print(metric)

        if metric > THRESHOLD:
            continue
        pred_boxes.append((x1,y1,x2,y2))


    calculate_metrics(boxes, pred_boxes, name)
    draw_boxes(pred_im, pred_boxes)
    display_blobs(pred_im, gt_im)

def calculate_metrics(gt_boxes, pred_boxes, name):
    """
    Calculate detection metrics
    """
    def iou(boxA, boxB):
        # Box coords
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        # Intersect
        interW = max(0, xB - xA)
        interH = max(0, yB - yA)
        interArea = interW * interH

        # Area    
        boxAArea = (boxA[2]-boxA[0]) * (boxA[3]-boxA[1])
        boxBArea = (boxB[2]-boxB[0]) * (boxB[3]-boxB[1])

        # IOU
        return interArea / float(boxAArea + boxBArea - interArea + 1e-10)

    # Save box index if found
    matched_gt = set()
    tp = 0
    for pred in pred_boxes:
        for i, gt in enumerate(gt_boxes):
            if i in matched_gt: # Skip already found
                continue
            if iou(pred, gt) >= 0.5:
                tp += 1
                matched_gt.add(i)
                break

    # Calculate the rest
    fp = len(pred_boxes) - tp
    fn = len(gt_boxes) - tp

    # Metric formulas
    precision = tp / (tp + fp + 1e-10)
    recall = tp / (tp + fn + 1e-10)

    # Print
    print(f"File: {name}")
    print(f"TP: {tp}, FP: {fp}, FN: {fn}")
    print(f"Precision: {precision:.3f}, Recall: {recall:.3f}")

def display_found(img_rgb, blobs):
    """
    Draw found blobs into image and display
    """
    result = img_rgb.copy()
    for blob in blobs:
        y = int(blob[0])
        x = int(blob[1])
        sigma = int(blob[2])
        cv.circle(result, (x,y), sigma, (255,0,0), 1)

    plt.imshow(result)
    plt.show()

def display_blobs(pred_im, gt_im):
    """
    Display detected sunflowers and ground truths
    """
    plt.figure("Blobs")

    plt.subplot(1,2,1)
    plt.imshow(pred_im)
    plt.title("Predictions")
    
    plt.subplot(1,2,2)
    plt.imshow(gt_im)
    plt.title("Ground Truth")

    plt.show()

def load_boxes(path):
    """
    Load ground truth
    """
    boxes = []
    with open(os.path.join(path)) as f:
        lines = f.read().splitlines()
        for line in lines:
            vec = [int(x) for x in line.split()] 
            boxes.append(vec)

    return boxes

def draw_boxes(image, boxes):
    """
    Draw boxes
    """
    for (x1, y1, x2, y2) in boxes:
        cv.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)


if __name__ == "__main__":
    data_dir = os.path.join("data")
    process_sunflowers(data_dir)