import io
import picamera
import threading
import asyncio
import time
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse

app = FastAPI()

class CameraStream:
    def __init__(self):
        self.frame = None
        self.thread = threading.Thread(target=self._capture_frames, daemon=True)
        self.thread.start()

    def _capture_frames(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 30
            camera.start_preview()
            time.sleep(2)
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True, resize=(640,480)):
                stream.seek(0)
                self.frame = stream.read()
                stream.seek(0)
                stream.truncate()

camera_stream = CameraStream()

@app.get('/video_feed')
async def video_feed():
    async def generate():
        while True:
            frame = camera_stream.frame
            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                await asyncio.sleep(0.1)

    return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)