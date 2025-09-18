import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def preprocess(filepath: str) -> dict:
    """
    Transform to greyscale and create a histogram
    """
    image_data = cv2.imread(filepath)
    image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB) # First need to convert to RGB from loaded BGR (blue, green, red)
    greyscale = cv2.cvtColor(image_data, cv2.COLOR_RGB2GRAY) # Conversion for greyscale for easier histogram work (only one z-dimension) 
    histogram = cv2.calcHist([greyscale], [0], None, [256], [0,256])
    return {
        "hist": histogram,
        "img": image_data
    }


def main():
    folder = os.path.join("data")
    image_files = os.listdir(folder)
    
    data = [preprocess(os.path.join(folder,image)) for image in image_files] # saves histogram and image into an array

    images = plt.figure("Image comparison")
    histograms = plt.figure("Histogram comparison")

    dimension = len(data) # for plotting purposes

    for image_index, _ in enumerate(data): # creates a row for each image

        image_distances = [cv2.compareHist(data[image_index]["hist"], data[x]["hist"], cv2.HISTCMP_INTERSECT) for x, _ in enumerate(data)] # Calculate hist similarity to all other images (smaller = better -> hence descending order used later)
    
        np_image_distances = np.array(image_distances) # convert list to numpy for argsort (indice sort)

        indices = np.argsort(np_image_distances)[::-1] # get sorted indices in descending order

        # print(image_index, np_image_distances[indices])

        # Plots the row elements
        for index in range(len(indices)):
            plt.figure(images) # switch to image figure
            plt.subplot(dimension, dimension, (image_index*dimension)+index+1) # specifies the subplot of the figure (image_index*dimension=row, index+1=column)
            plt.imshow(data[indices[index]]["img"]) # indices[index] = n-th most similar image (starting with itself)
            plt.axis("off")

        for index in range(len(indices)):
            plt.figure(histograms)
            plt.subplot(dimension, dimension, (image_index*dimension)+index+1)
            plt.hist(data[indices[index]]["hist"])

    # Display plots
    images.show()
    histograms.show()

    input("Press enter to exit")


if __name__ == "__main__":
    main()