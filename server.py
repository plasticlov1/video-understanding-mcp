import cv2
import base64
import numpy as np
import requests
import tempfile
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("video-watcher")

def frame_diff(frame1,frame2):
            diff = cv2.absdiff(frame1,frame2)
            return np.mean(diff)

@mcp.tool()
def watch_video(url: str) ->list:
    #从URL下载视频到临时文件
    r = requests.get(url)
    tmp = tempfile.NamedTemporaryFile(suffix=".mp4",delete=False)
    tmp.write(r.content)
    tmp.close()
    path = tmp.name

    video = cv2.VideoCapture(path)
    fps = int(video.get(cv2.CAP_PROP_FPS))

    frame_count = 0
    prev_frame = None
    frame_b64 =[]


    while True:
        success,frame = video.read()
        if not success:
            break
        if prev_frame is not None:
            diff = frame_diff(prev_frame,frame)
            if diff >= 30 or frame_count % (fps * 3)==0:
                _,buf = cv2.imencode(".jpg",frame)
                b64 = base64.b64encode(buf).decode("utf-8")
                frame_b64.append(b64)
        prev_frame = frame
        frame_count+=1
    video.release()
    return frame_b64

if __name__ =="__main__":
    import uvicorn
    app = mcp.sse_app()
    uvicorn.run(app,host="0.0.0.0",port=8000)