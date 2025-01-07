from ultralytics import YOLO

# Load YOLO model
model = YOLO("models/yolov8_v1.pt")


def detect_objects(frame):
    """
    Perform object detection on a frame.

    Args:
        frame (np.array): Video frame.

    Returns:
        list: Detected objects with bounding boxes and labels.
    """
    results = model.predict(frame, conf=0.3)
    detections = []

    for result in results:
        for box in result.boxes:
            detections.append(
                {
                    "bbox": box.xyxy[0].tolist(),
                    "confidence": box.conf[0].item(),
                    "label": model.names[int(box.cls[0])],
                }
            )

    return detections
