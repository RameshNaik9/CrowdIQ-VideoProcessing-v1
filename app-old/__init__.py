from flask import Flask
from flask_cors import CORS


def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    from app.api.rtsp_routes import rtsp_blueprint
    from app.api.upload_routes import upload_blueprint
    from app.api.metadata_routes import metadata_blueprint

    app.register_blueprint(rtsp_blueprint, url_prefix="/api/rtsp")
    app.register_blueprint(upload_blueprint, url_prefix="/api/upload")
    app.register_blueprint(metadata_blueprint, url_prefix="/api/metadata")

    return app
