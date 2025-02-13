"""
Module __init__: Create and configure the Flask application.
"""

import os
from flask import Flask
from .views import main_blueprint


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    if os.environ.get("CONFIG_TYPE") == "config.TestingConfig":
        app.config["SECRET_KEY"] = "secret"
    else:
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    # Register blueprint (routes)
    app.register_blueprint(main_blueprint)

    return app


if __name__ == "__main__":
    # Only run the server if you execute this file directly.
    flask_app = create_app()
    flask_app.run(debug=True)
