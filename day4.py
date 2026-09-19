import os
import numpy as np
import cv2

saved = 0
frame_count = 0

video = cv2.VideoCapture("clip.mp4")
fps = int(video.get(cv2.CAP_PROP_FPS))

os.makedirs("frames",exist_ok=True)

def frame_diff(frame1,frame2):
            diff = cv2.absdiff(frame1,frame2)
            return np.mean(diff)

prev_frame=None

while True:
    success,frame = video.read()
    if not success:
        break
    frame = cv2.rotate(frame,cv2.ROTATE_90_COUNTERCLOCKWISE)
    if prev_frame is not None:
        diff = frame_diff(prev_frame,frame)
        if diff >=30 or (frame_count % (fps*3)==0):
            cv2.imwrite(f"frames/frame_{saved}.png",frame)
            saved +=1
    prev_frame = frame
    frame_count +=1

video.release()
print(f"智能抽帧已完成，保留了{saved}帧")

#帧差很小的被跳过了 无论帧差多少 每隔N秒至少保留一帧

