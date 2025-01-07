import cv2
import random
from datetime import datetime
from app.utils.model_utils import YOLOModel, DeepSortTracker
from app.utils.db_utils import MongoDBHandler


class DetectionService:
    def __init__(self, model_path, db_config):
        """
        Initializes the DetectionService with YOLO model, DeepSort tracker, and database handler.

        Args:
            model_path (str): Path to the YOLO model.
            db_config (dict): Configuration for the MongoDB connection.
        """
        self.model = YOLOModel(model_path)
        self.tracker = DeepSortTracker()
        self.db_handler = MongoDBHandler(db_config)
        self.track_info = {}
        self.serial_number = 1
        self.class_names = self.model.class_names

    def process_frame(self, frame, frame_number, fps):
        """
        Process a single video frame: detect objects, track them, and update the database.

        Args:
            frame (numpy.ndarray): The current video frame.
            frame_number (int): The current frame number.
            fps (float): Frames per second of the video.

        Returns:
            numpy.ndarray: Processed frame with detections and tracking annotations.
        """
        result_img, detections, _ = self.model.predict_objects(frame, conf=0.5)
        tracks = self.tracker.track_objects(detections, result_img)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            x1, y1, x2, y2 = map(int, track.to_tlbr())
            detected_class = (
                self.class_names[track.det_class]
                if track.det_class is not None
                else "unknown"
            )
            elapsed_time = frame_number / fps

            if track_id not in self.track_info:
                # New track
                self.track_info[track_id] = {
                    "serial_number": self.serial_number,
                    "gender": detected_class,
                    "start_time": current_time,
                    "time_spent": 0,
                    "last_seen": current_time,
                }
                self.serial_number += 1

            # Update track info
            self.track_info[track_id]["time_spent"] = elapsed_time
            self.track_info[track_id]["last_seen"] = current_time

            # Store or update in the database
            self.db_handler.update_or_insert(
                collection_name="tracking_data",
                document_id=str(track_id),
                data=self.track_info[track_id],
            )

            # Annotate frame
            cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                result_img,
                f"ID {track_id} {detected_class}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

        return result_img
