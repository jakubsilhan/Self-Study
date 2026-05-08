import os, shutil, yaml
import xml.etree.ElementTree as ET

DATASET_NAME = "dataset"
SOURCE_DIR = os.path.join("data")
DIR_NAME = os.path.join("prepared_data")
ANNOTATION = os.path.join("annotations.xml")

def prepare():
    target_dir = os.path.join(DIR_NAME)
    os.makedirs(target_dir, exist_ok=True)

    # Features
    images_dir = os.path.join(target_dir, "images")
    if not os.path.exists(images_dir):
        prepare_images(images_dir)

    # Labels
    labels_dir = os.path.join(target_dir, "labels")
    if not os.path.exists(labels_dir):
        prepare_labels(labels_dir)

    # Dataset file
    prepare_dataset_file()

def prepare_images(images_dir):
    source_images = os.path.join(SOURCE_DIR, "images")
    shutil.copytree(source_images, images_dir)

def prepare_labels(labels_dir):
    os.makedirs(labels_dir, exist_ok=True)
    tree = ET.parse(ANNOTATION)

    root = tree.getroot()

    for image in root.findall("image"):
        image_id = image.get("id")
        name = image.get("name")
        width = int(image.get("width"))
        height = int(image.get("height"))

        name = name.split("/")[1]
        name = name.split(".")[0]
        label_file = os.path.join(labels_dir, f"{name}.txt")

        lines = []

        for box in image.findall("box"):
            label = box.get("label")
            xtl = float(box.get("xtl"))
            ytl = float(box.get("ytl"))
            xbr = float(box.get("xbr"))
            ybr = float(box.get("ybr"))

            x_center = ((xtl + xbr) / 2) / width
            y_center = ((ytl + ybr) / 2) / height
            w = (xbr - xtl) / width
            h = (ybr - ytl) / height

            line = f"0 {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}"
            lines.append(line)

        with open(label_file, "w") as f:
            f.write("\n".join(lines))

def prepare_dataset_file():
    classes = ["strawberry"]
    yolo_dataset = {
        "path": DIR_NAME,
        "train": "images",
        "val": "images",
        "names": {i: name for i, name in enumerate(classes)}
    }

    with open(f"{DATASET_NAME}.yml", "w") as f:
        yaml.dump(yolo_dataset, f, sort_keys=False)

if __name__ == "__main__":
    prepare()