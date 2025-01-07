from deep_sort_realtime.deepsort_tracker import DeepSort

# Initialize DeepSort tracker
tracker = DeepSort(max_age=30, max_cosine_distance=0.3)


def track_objects(detections, frame):
    """
    Track detected objects in the frame.

    Args:
        detections (list): List of detected objects.
        frame (np.array): The video frame.

    Returns:
        list: Updated tracking data.
    """
    deepsort_detections = [
        {
            "bbox": [
                d["bbox"][0],
                d["bbox"][1],
                d["bbox"][2] - d["bbox"][0],
                d["bbox"][3] - d["bbox"][1],
            ],
            "confidence": d["confidence"],
            "class_id": d["label"],
        }
        for d in detections
    ]
    return tracker.update_tracks(deepsort_detections, frame=frame)
