import cv2
import numpy as np


def resize_frame(frame, scale=0.65):
    """
    Resize a video frame by a given scale.

    Args:
        frame (np.array): The original video frame.
        scale (float): The scale factor for resizing.

    Returns:
        np.array: The resized video frame.
    """
    height, width = frame.shape[:2]
    new_width = int(width * scale)
    new_height = int(height * scale)
    return cv2.resize(frame, (new_width, new_height))


def read_rtsp_stream(rtsp_url):
    """
    Reads frames from an RTSP stream.

    Args:
        rtsp_url (str): The RTSP stream URL.

    Yields:
        np.array: A frame from the RTSP stream.
    """
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        raise ValueError(f"Unable to open RTSP stream: {rtsp_url}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        yield frame

    cap.release()


def encode_frame_to_bytes(frame):
    """
    Encode a video frame to bytes for streaming.

    Args:
        frame (np.array): The video frame.

    Returns:
        bytes: Encoded frame as bytes.
    """
    _, buffer = cv2.imencode(".jpg", frame)
    return buffer.tobytes()
