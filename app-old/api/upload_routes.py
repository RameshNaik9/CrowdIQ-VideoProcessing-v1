from flask import Blueprint, request, jsonify
from app.services.video_processing import process_uploaded_video

upload_blueprint = Blueprint("upload", __name__)


@upload_blueprint.route("/process", methods=["POST"])
def process_video():
    """
    Process an uploaded video file.

    Request:
        Multipart form with a video file.

    Returns:
        JSON response indicating success or failure.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        process_uploaded_video(file)
        return jsonify({"message": "Video file processing started"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
