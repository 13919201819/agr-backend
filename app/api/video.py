from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import cv2
import app.services.stream_manager as sm
import time

router = APIRouter()

def generate_frames():
    while sm.camera_running:
        with sm.lock:
            frame = sm.latest_frame

        if frame is None:
            time.sleep(0.03)
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

        time.sleep(0.03)

@router.get("/video")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )