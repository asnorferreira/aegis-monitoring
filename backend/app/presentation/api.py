from .auth_controller import auth_bp
from .structure_controller import structure_bp

def register_blueprints(app):
    """Registers all API blueprints with the Flask app."""
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(structure_bp, url_prefix='/api/structures')
