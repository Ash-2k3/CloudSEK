from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'cloudSEK-intern-task'

# Extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

from app.models import User, Post, Comment  # Importing models after db is initialized
from app import routes

# This ensures that the tables are created when the application starts
with app.app_context():
    db.create_all()