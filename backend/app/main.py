import os
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from .infrastructure.database import db, migrate
from .presentation.api import register_blueprints
from .config import config_by_name

def create_app():
    """Application factory."""
    app = Flask(__name__)
    
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config_by_name[env])

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Configuração do Swagger
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

    register_blueprints(app)

    return app