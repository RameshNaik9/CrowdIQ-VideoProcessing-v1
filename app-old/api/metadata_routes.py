from flask import Blueprint, jsonify
from app.utils.db import get_all_metadata

metadata_blueprint = Blueprint("metadata", __name__)


@metadata_blueprint.route("/", methods=["GET"])
def get_metadata():
    """
    Fetch all metadata from the database.

    Returns:
        JSON response containing metadata.
    """
    try:
        data = get_all_metadata()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
