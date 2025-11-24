import cv2 as cv
import numpy as np

class Camshift:
    def __init__(self, template_path):
        self._load_template(template_path)
        self.is_first = True


    def _load_template(self, path):
        """Loads template and converts it into roi histogram"""
        temp_bgr = cv.imread(path)
        # Size
        height, width = np.floor_divide(temp_bgr.shape[:2], 2)
        # Hist
        temp_hue = cv.cvtColor(temp_bgr, cv.COLOR_BGR2HSV)[:,:,0]
        roi_hist = cv.calcHist([temp_hue], [0], None, [180], [0,180])
        roi_hist = roi_hist / roi_hist.sum()
        self.roi_hist = roi_hist.ravel()
        self.shape = (height, width)

    def detect_object(self, frame):
        """Detects object in image and returns a bounding box"""
        if self.is_first:
            return self._first_frame(frame)
        
        return self._other_frames(frame)

    def _first_frame(self, frame):
        """Finds region of interest in first frame"""
        frame_hue = cv.cvtColor(frame, cv.COLOR_BGR2HSV)[:,:,0]
        # Probability map
        back_projection = self.roi_hist[frame_hue]
        # Absolute centroid
        self.roi = self._zeroth_moment(back_projection)
        return self._create_box()
    
    def _other_frames(self, frame):
        """Moves region of interest"""
        frame_hue = cv.cvtColor(frame, cv.COLOR_BGR2HSV)[:,:,0]
        # Probability map
        back_projection = self.roi_hist[frame_hue]
        # Limiting to previous roi
        x1,y1,x2,y2 = self.prev_cords
        back_projection = back_projection[y1:y2, x1:x2]
        # roi relative centroid
        tmp_x, tmp_y = self._zeroth_moment(back_projection)
        # Movement of absolute centroid
        x_t = int(x1+tmp_x)
        y_t = int(y1+tmp_y)
        self.roi = (x_t, y_t)
        return self._create_box()


    def _zeroth_moment(self, back_projection):
        """Finds centroid of backprojection"""
        y, x = np.indices(back_projection.shape)
        total = back_projection.sum()
        x_t = (x * back_projection).sum() / total
        y_t = (y * back_projection).sum() / total
        return x_t, y_t

    def _create_box(self):
        """Creates a bounded box coords around roi"""
        h, w = self.shape
        x_t, y_t = self.roi

        x1 = abs(int(x_t-w))
        x2 = abs(int(x_t+w))
        y1 = abs(int(y_t-h))
        y2 = abs(int(y_t+h))

        self.prev_cords = (x1,y1,x2,y2)
        return (x1, y1, x2, y2)

        
