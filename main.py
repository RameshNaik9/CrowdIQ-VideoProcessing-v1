from flask import Flask, request, jsonify
from flask_cors import CORS
from app.services.detection_service import DetectionService
from app.services.video_service import VideoService
from config.config import DATABASE_CONFIG, MODEL_PATH
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize services
detection_service = DetectionService(MODEL_PATH, DATABASE_CONFIG)
video_service = VideoService(detection_service)


@app.route("/")
def index():
    """Health check endpoint."""
    return jsonify({"message": "CrowdIQ Video Processing Microservice is running."})


@app.route("/api/process/rtsp", methods=["POST"])
def process_rtsp():
    """
    Start processing an RTSP stream.

    Request Body:
    {
        "rtsp_url": "rtsp://username:password@ip:port/path"
    }

    Returns:
        JSON response with processing status.
    """
    data = request.get_json()
    rtsp_url = data.get("rtsp_url")
    if not rtsp_url:
        return jsonify({"error": "RTSP URL is required."}), 400

    try:
        video_service.process_video(rtsp_url, None)
        return jsonify({"message": "RTSP stream processing started."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/process/upload", methods=["POST"])
def process_upload():
    """
    Endpoint to process an uploaded video file.

    Request:
        Multipart form-data with the video file.

    Returns:
        JSON response with processing status.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400

    video_file = request.files["file"]
    if video_file.filename == "":
        return jsonify({"error": "No selected file."}), 400

    try:
        # Save the uploaded video
        video_path = f"./data/uploads/{video_file.filename}"
        video_file.save(video_path)

        # Call the process_video method
        output_path = f"./data/processed/{video_file.filename}"
        video_service.process_video(video_path, output_path)

        return jsonify({"message": "Uploaded video processing started."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/metadata", methods=["GET"])
def get_metadata():
    """
    Retrieve all metadata from the database.

    Returns:
        JSON response with metadata.
    """
    try:
        from app.utils.db_utils import MongoDBHandler

        db_handler = MongoDBHandler(DATABASE_CONFIG)
        metadata = db_handler.get_all_metadata()
        return jsonify({"metadata": metadata}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
