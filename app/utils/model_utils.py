from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2


class YOLOModel:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.class_names = self.model.names  # Retrieve class names from the model

    def predict_objects(self, img, conf=0.3):
        """Perform object detection on an image."""
        results = self.model.predict(img, conf=conf)

        # Check if results are valid
        if len(results) == 0 or len(results[0].boxes) == 0:
            return (
                img,
                [],
                [],
            )  # Return empty detections and boxes if no objects are found

        detections, boxes = [], []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = (
                    int(box.xyxy[0][0]),
                    int(box.xyxy[0][1]),
                    int(box.xyxy[0][2]),
                    int(box.xyxy[0][3]),
                )
                class_id, confidence = int(box.cls[0]), box.conf[0]
                detections.append([[x1, y1, x2 - x1, y2 - y1], confidence, class_id])
                boxes.append((x1, y1, x2, y2))
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(
                    img,
                    f"{self.class_names[class_id]}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (255, 0, 0),
                    1,
                )
        return img, detections, boxes


class DeepSortTracker:
    def __init__(self):
        self.tracker = DeepSort()

    def track_objects(self, detections, frame):
        return self.tracker.update_tracks(detections, frame)
