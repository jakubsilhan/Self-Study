import cv2 as cv
import numpy as np

THRESHOLD = 0.3
MIN_SEGMENT_LENGTH= 5

def calculate_corell(frame1, frame2):
    """Calculates correllation of hists between frames"""
    h1 = cv.calcHist([frame1], [0], None, [256], [0,256])
    h2 = cv.calcHist([frame2], [0], None, [256], [0,256])
    return cv.compareHist(h1, h2, cv.HISTCMP_CORREL)

def segment_video(path):
    """Segments video into separate scenes"""
    cap = cv.VideoCapture(path)
    segments = []
    frame_idx = 0
    segment_start = 0
    prev_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if prev_frame is not None:
            corell = calculate_corell(prev_frame, frame)

            if corell < THRESHOLD:
                if frame_idx - segment_start >= MIN_SEGMENT_LENGTH:
                    segments.append((segment_start, frame_idx-1))
                    segment_start = frame_idx
        
        prev_frame = frame.copy()
        frame_idx += 1
    
    # Add last segment
    if frame_idx - segment_start >= MIN_SEGMENT_LENGTH:
        segments.append((segment_start, frame_idx-1))

    cap.release()
    return segments