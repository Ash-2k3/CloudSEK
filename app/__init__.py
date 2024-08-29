"""
Initializes the Flask application, configures extensions, and sets up routes.
"""

from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


# Extensions
db = SQLAlchemy() # SQLAlchemy instance for database interactions
jwt = JWTManager() # JWTManager instance for handling JSON Web Tokens (JWT)


def create_app(config_class=Config):
    """
    Application factory function to create and configure the Flask app.

    Args:
        config_class (class): The configuration class to use for setting up the app.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints for routes
    from app.models import User, Post, Comment
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app