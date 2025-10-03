import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from .infrastructure.database import db, migrate
from .presentation.api import register_blueprints
from .config import Config

def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}}) # Allow frontend to access API

    # Swagger/Flasgger setup
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    Swagger(app, config=swagger_config)

    # Register API blueprints
    register_blueprints(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
