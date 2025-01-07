from flask import Blueprint, request, jsonify
from app.services.video_processing import process_rtsp_stream

rtsp_blueprint = Blueprint("rtsp", __name__)


@rtsp_blueprint.route("/start", methods=["POST"])
def start_rtsp():
    """
    Start processing an RTSP stream.

    Request Body:
    {
        "rtsp_url": "rtsp://username:password@ip:port/path"
    }

    Returns:
        JSON response indicating success or failure.
    """
    data = request.get_json()
    rtsp_url = data.get("rtsp_url")

    if not rtsp_url:
        return jsonify({"error": "RTSP URL is required"}), 400

    try:
        process_rtsp_stream(rtsp_url)
        return jsonify({"message": "RTSP stream processing started"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
