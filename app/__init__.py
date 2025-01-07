import os
import logging


# Set up logging
def setup_logging():
    """
    Configure the logging for the application.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


setup_logging()

# Import the services and utilities
from app.services.detection_service import DetectionService
from app.services.video_service import VideoService
from app.utils.db_utils import MongoDBHandler
from app.utils.video_utils import resize_frame, read_rtsp_stream, encode_frame_to_bytes
from app.utils.model_utils import YOLOModel, DeepSortTracker
