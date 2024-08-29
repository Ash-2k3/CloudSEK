from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config.from_object(Config)

# Extensions
db = SQLAlchemy()
jwt = JWTManager()

from app.models import User, Post, Comment
from app.routes import bp as routes_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(routes_bp)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app