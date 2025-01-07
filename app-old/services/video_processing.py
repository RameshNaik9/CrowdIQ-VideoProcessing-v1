from app.utils.video_stream import process_stream
from app.utils.db import save_metadata
import cv2
from ultralytics import YOLO

# Load age and gender models
face_net = cv2.dnn.readNet(
    "models/opencv_face_detector_uint8.pb", "models/opencv_face_detector.pbtxt"
)
age_net = cv2.dnn.readNet("models/age_net.caffemodel", "models/age_deploy.prototxt")
gender_net = cv2.dnn.readNet(
    "models/gender_net.caffemodel", "models/gender_deploy.prototxt"
)

# Load YOLO model
yolo_model = YOLO("models/yolov8_v1.pt")
import cv2
from app.services.detection import detect_objects
from app.services.tracking import track_objects
from app.services.metadata import extract_metadata
from app.utils.db import save_metadata
from app.utils.logger import get_logger

logger = get_logger(__name__)


def process_frame(frame, frame_number, fps, source_id):
    """
    Process a single frame to detect, track, and extract metadata.

    Args:
        frame (np.array): Video frame.
        frame_number (int): Frame number in the video.
        fps (float): Frames per second of the video.
        source_id (str): Identifier for the video source (e.g., RTSP URL).

    Returns:
        np.array: Processed frame with detection and tracking annotations.
    """
    logger.info(f"Processing frame {frame_number}...")

    # Perform object detection
    detections = detect_objects(frame)

    # Track objects
    tracks = track_objects(detections, frame)

    # Extract metadata
    metadata = extract_metadata(tracks, frame_number, fps, source_id)

    # Save metadata to the database
    save_metadata(metadata)

    # Annotate frame with metadata
    annotated_frame = annotate_frame(frame, tracks)

    return annotated_frame


def annotate_frame(frame, tracks):
    """
    Annotate the video frame with tracking and metadata information.

    Args:
        frame (np.array): Video frame.
        tracks (list): List of tracked objects.

    Returns:
        np.array: Annotated frame.
    """
    for track in tracks:
        if not track.is_confirmed():
            continue

        x1, y1, x2, y2 = map(int, track.to_tlbr())
        label = f"{track.det_class} ({track.track_id})"

        # Draw bounding box and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
        )

    return frame
