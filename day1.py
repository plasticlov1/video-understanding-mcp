import os
import cv2

video = cv2.VideoCapture("clip.mp4")
fps = int(video.get(cv2.CAP_PROP_FPS))
count = 0

os.makedirs("frames",exist_ok=True)

while True:
    success,frame = video.read()
    if not success:
        break
    if count % fps ==0:
        sec = count // fps 
        cv2.imwrite(f"frames/frame_{sec}.png",frame)
    count +=1

video.release()
print(f"抽帧完成，共{count // fps}秒，帧图片在frames文件夹里")