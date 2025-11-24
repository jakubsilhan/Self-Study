import os
import cv2 as cv
from segmentation import segment_video
from background_subtraction import BackgroundSubtraction
from camshift import Camshift

def run_processing(path, output_path):

    # Get segments
    segments = segment_video(path)

    # Initialize capture and detector
    cap = cv.VideoCapture(path)
    template_path = os.path.join("data", "pvi_cv10_vzor_pomeranc.bmp")
    current_frame = 0

    # Prepare video writer
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter(output_path, fourcc, 10.0, (frame_width, frame_height))    

    # Cycle through segments
    for segment_idx, (start, end) in enumerate(segments):
        while current_frame < start:
            cap.read()
            current_frame += 1

        if segment_idx == 1:
            detector = Camshift(template_path)
        else:
            detector = BackgroundSubtraction(threshold=40)

        for frame_idx in range(start, end + 1):
            ret, frame = cap.read()
            if not ret:
                break

            current_frame += 1
            
            # Detect and display bounding box
            result = detector.detect_object(frame)
            if result is not None:
                x1, y1, x2, y2 = result
                cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Write info
            cv.putText(frame, f"Segment:{segment_idx+1}", (10,30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 1)

            # Write to output
            out.write(frame)

    cap.release()
    out.release()

if __name__ == "__main__":
    video_path = os.path.join("data", "pvi_cv10_video_in.mp4")
    output_path = os.path.join("edited_video.avi")
    run_processing(video_path, output_path)