import cv2
from app.services.detection import detect_objects
from app.services.tracking import track_objects
from app.services.metadata import extract_metadata
from app.utils.db import save_metadata


def process_stream(source, is_rtsp=True):
    """
    Process video streams or files.

    Args:
        source: RTSP URL or video file.
        is_rtsp (bool): Flag indicating RTSP or file.
    """
    cap = cv2.VideoCapture(source if is_rtsp else source.stream)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detections = detect_objects(frame)
        tracks = track_objects(detections, frame)
        metadata = extract_metadata(tracks)
        save_metadata(metadata)

    cap.release()
    cv2.destroyAllWindows()
