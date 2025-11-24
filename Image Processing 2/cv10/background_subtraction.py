import numpy as np
import cv2 as cv

class BackgroundSubtraction:
    def __init__(self, threshold = 25):
        self.threshold = threshold
        self.background = None

    def initialize_background(self, frame):
        """Initializes background"""
        self.background = frame.astype(np.float32)

    def get_foreground_mask(self, frame):
        """Returns a mask of foreground"""
        if self.background is None:
            self.initialize_background(frame)
            return np.zeros(frame.shape[:2], dtype=np.uint8)
        
        # Frame coloring
        bg_uint8 = self.background.astype(np.uint8)
        gr_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gr_bg = cv.cvtColor(bg_uint8, cv.COLOR_BGR2GRAY)

        # Frame subtraction
        diff = cv.absdiff(gr_bg, gr_frame)

        # Mask extraction
        _, mask = cv.threshold(diff, self.threshold, 255, cv.THRESH_BINARY)

        # Noise filtering
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

        return mask

    def detect_object(self, frame):
        """Detects object and return bounded box"""
        mask = self.get_foreground_mask(frame)

        y_coords, x_coords = np.where(mask > 0)

        if len(x_coords) < 20:
            return None

        x_min = int(np.min(x_coords))
        x_max = int(np.max(x_coords))
        y_min = int(np.min(y_coords))
        y_max = int(np.max(y_coords))


        return (x_min, y_min, x_max, y_max)
