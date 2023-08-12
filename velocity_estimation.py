
import cv2
import argparse
import numpy as np
from time import sleep
import time

def get_background(file_path):
    cap = cv2.VideoCapture(file_path)
    frame_indices = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=50)
    frames = []
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        frames.append(frame)
    median_frame = np.median(frames, axis=0).astype(np.uint8)
    return median_frame


cap = cv2.VideoCapture('17.mp4')

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
save_name = "outputs/a.mp4"
out = cv2.VideoWriter(
    save_name,
    cv2.VideoWriter_fourcc(*'mp4v'), 7.5, 
    (frame_width, frame_height)
)

background = get_background('17.mp4')
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
frame_count = 0
consecutive_frame = 4

sleep(5)

iter = 0

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frame_count += 1
        orig_frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if frame_count % consecutive_frame == 0 or frame_count == 1:
            frame_diff_list = []
        frame_diff = cv2.absdiff(gray, background)
        ret, thres = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
        dilate_frame = cv2.dilate(thres, None, iterations=2)
        frame_diff_list.append(dilate_frame)
        if len(frame_diff_list) == consecutive_frame:
            sum_frames = sum(frame_diff_list)
            start = time.time()
            contours, hierarchy = cv2.findContours(sum_frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for i, cnt in enumerate(contours):
                cv2.drawContours(frame, contours, i, (0, 0, 255), 3)
            for contour in contours:
                if cv2.contourArea(contour) < 5000 and cv2.contourArea(contour) > 1000:
                    iter += 1
                    #continue
                    (x, y, w, h) = cv2.boundingRect(contour)
                    
                    if iter == 1:
                        prev = y
                        dist = h
                    if y == dist:
                        end = time.time()
                        print(dist/(start-end))
                    
                        
# =============================================================================
#                     print(x, dist)
# =============================================================================
                    cv2.rectangle(orig_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
            cv2.imshow('Detected Objects', orig_frame)
            out.write(orig_frame)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
    else:
        break
cap.release()
cv2.destroyAllWindows()
