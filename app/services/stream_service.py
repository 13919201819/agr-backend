import cv2
import threading
from app.services import stream_manager
from app.services.detection_service import detect
from app.db.supabase import supabase
from datetime import datetime
from app.services.logging_service import log_detection
import time

def camera_loop(stream_url, stream_id):
    cap = cv2.VideoCapture(stream_url)
    stream_manager.camera_running = True

    print(f"🚀 Camera started for stream: {stream_id}")

    last_log_time = 0
    drone_id = stream_id  # 🔥 TEMP (later replace with real drone_id)

    while stream_manager.camera_running:
        ret, frame = cap.read()
        if not ret:
            print(f"⚠️ Frame read failed")
            break

        detections, count = detect(frame)

        # 🎯 DRAW BOXES
        for d in detections:
            x1, y1, x2, y2 = d["box"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Human", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # 🧠 CROWD DENSITY
        if count < 5:
            density, color = "LOW", (0, 255, 0)
        elif count < 15:
            density, color = "MEDIUM", (0, 255, 255)
        else:
            density, color = "HIGH", (0, 0, 255)

        # 🚨 ALERTS
        alerts = []

        if count > 15:
            alerts.append("HIGH CROWD 🚨")

        if count > 30:
            alerts.append("OVERCROWDING 🚨")

        # 📊 DISPLAY
        cv2.putText(frame, f"Humans: {count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.putText(frame, f"Density: {density}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # 🚨 DISPLAY ALERTS
        for i, alert in enumerate(alerts):
            cv2.putText(frame, alert, (20, 120 + i * 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # 💾 LOG TO DB (every 5 sec)
        current_time = time.time()
        if current_time - last_log_time > 5:
            log_detection(drone_id, count, density)
            last_log_time = current_time

        # ✅ SHARE FRAME WITH VIDEO
        with stream_manager.lock:
            stream_manager.latest_frame = frame.copy()

    cap.release()
    stream_manager.camera_running = False
    stream_manager.latest_frame = None

    print(f"🛑 Camera stopped for stream: {stream_id}")

# def camera_loop(stream_url, stream_id):
#     """Single camera loop — captures, detects, stores latest frame"""
#     cap = cv2.VideoCapture(stream_url)
#     stream_manager.camera_running = True
#     print(f"🚀 Camera started for stream: {stream_id}")

#     while stream_manager.camera_running:
#         ret, frame = cap.read()
#         if not ret:
#             print(f"⚠️ Frame read failed")
#             break

#         detections, count = detect(frame)

#         # Draw boxes
#         for d in detections:
#             x1, y1, x2, y2 = d["box"]
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.putText(frame, "Human", (x1, y1 - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

#         # Crowd density
#         if count < 5:
#             density, color = "LOW", (0, 255, 0)
#         elif count < 15:
#             density, color = "MEDIUM", (0, 255, 255)
#         else:
#             density, color = "HIGH", (0, 0, 255)

#         cv2.putText(frame, f"Humans: {count}", (20, 40),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#         cv2.putText(frame, f"Density: {density}", (20, 80),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

#         # ✅ Store latest frame for video feed
#         with stream_manager.lock:
#             stream_manager.latest_frame = frame.copy()

#     cap.release()
#     stream_manager.camera_running = False
#     stream_manager.latest_frame = None
#     print(f"🛑 Camera stopped for stream: {stream_id}")


def start_camera(stream_url, stream_id):
    t = threading.Thread(target=camera_loop, args=(stream_url, stream_id), daemon=True)
    stream_manager.camera_thread = t
    t.start()


def stop_camera():
    stream_manager.camera_running = False
    if stream_manager.camera_thread:
        stream_manager.camera_thread.join(timeout=3)
    stream_manager.camera_thread = None
    stream_manager.active_streams.clear()
    print("✅ Camera fully stopped")