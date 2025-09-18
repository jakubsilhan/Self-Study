import numpy as np
import cv2 as cv

def prepare_reference(filename: str):
    """
    Prepares a normalized hue histogram of the target to be tracked
    """
    reference = cv.imread(filename)
    # cap = cv.VideoCapture("./data/cv02_hrnecek.mp4")

    # Reference image to HSV
    hsv_ref = cv.cvtColor(reference, cv.COLOR_BGR2HSV)

    # Masking
    # Focus on the most likely important pixels ignore low saturation and dark pixels
    mask = cv.inRange(hsv_ref,
                      np.array((0.,60., 32.)),
                      np.array((180., 255., 255)))
    
    # Histogram of hue channel
    roi_hist = cv.calcHist([hsv_ref],
                           [0], mask,
                           [180],
                           [0,180])
    
    # Normalizes histogram to range 0-255
    cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)

    return roi_hist

def tracking(filename: str, roi_hist):
    """
    Uses the hue histogram of the target to track it using the camshift algorithm
    """
    # Initialization of video capture
    cap = cv.VideoCapture(filename)

    ret, frame = cap.read()
    if not ret:
        print("Failed to read video")
        cap.release()
        exit()

    # Initial tracking window
    x, y, width, height = 0, 0, 100, 100
    track_window = (x, y, width, height)

    # Set termination criteria: 10 iterations or at least 1 pt move (how many iterations for each frame)
    term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)

    while True:
        # Read the frame
        ret, frame = cap.read()
        if not ret:
            break

        # Frame to HSV
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Backprojection of histogram onto current frame (highlights areas that resemble the histogram - grayscale, brighter = more similar)
        dst = cv.calcBackProject([hsv], [0], roi_hist, [0,180], 1) # frame, channel(hue),target,range,scale

        # Apply camshift to get the new location of the target in current frame
        ret2, track_window = cv.CamShift(dst, track_window, term_crit)

        # Draw it on image
        pts = cv.boxPoints(ret2)
        pts = np.int0(pts) # float to int

        # Draw the tracking window
        Result = cv.polylines(frame,
                              [pts],
                              True,
                              (0, 255, 255),
                              2)
        
        cv.imshow('Camshift', Result)

        # Set ESC key as the exit button
        k = cv.waitKey(30) & 0xff

        if k == 27:
            break

    # Release the cap object
    cap.release()

    # Close all opened windows
    cv.destroyAllWindows()



if __name__ == "__main__":
    roi_hist = prepare_reference("./data/cv02_vzor_hrnecek.bmp")
    tracking("./data/cv02_hrnecek.mp4", roi_hist)
