from ultralytics import YOLO

model = YOLO("yolov8n.pt")

CLASS_NAMES = model.names  # COCO class names


def detect(frame):
    results = model(frame)

    detections = []
    person_count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # 👇 only count humans
            if CLASS_NAMES[cls] == "person":
                person_count += 1

                detections.append({
                    "box": (x1, y1, x2, y2),
                    "confidence": conf,
                    "label": "person"
                })

    return detections, person_count