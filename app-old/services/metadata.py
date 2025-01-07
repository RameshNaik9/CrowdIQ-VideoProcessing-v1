from datetime import datetime


def extract_metadata(tracks, frame_number, fps, source_id):
    """
    Extract metadata such as gender, age, and time spent from tracks.

    Args:
        tracks (list): List of tracked objects.
        frame_number (int): Current frame number.
        fps (float): Frames per second of the video.
        source_id (str): Identifier for the video source (e.g., RTSP URL).

    Returns:
        list: Metadata for each tracked object.
    """
    metadata = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for track in tracks:
        if not track.is_confirmed():
            continue

        elapsed_time = frame_number / fps

        metadata.append(
            {
                "serial_number": track.track_id,
                "label": track.det_class,
                "time_spent": elapsed_time,
                "start_frame": track.start_frame,
                "first_appearance_time": current_time,
                "last_appearance_time": current_time,
                "source_id": source_id,
            }
        )

    return metadata
