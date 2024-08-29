"""
SQLAlchemy models for the Post-Comment Service.
"""

from datetime import datetime
from . import db  # Importing the db object from __init__.py
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List


class User(db.Model):
    """
    User model represents a registered user in the system.
    
    Attributes:
        id (int): User id of the user;
            Primary key, unique identifier for each user.
        username (str): Unique username of the user.
        password_hash (str): Hashed password for secure authentication.
        
    Relationships:
        posts: One-to-many relationship with the Post model to link  users to their posts.
        comments: One-to-many relationship with the Comment model tio link users to their comments.
    """
    
    id = db.Column(db.Integer, primary_key=True)  # Primary key.
    username = db.Column(db.String(80), unique=True, nullable=False)  # User's username.
    password_hash = db.Column(db.String(128), nullable=False)  # Hashed password for the user.

    posts = db.relationship('Post', backref='author', lazy=True)  # One-to-many relationship with Post.
    comments = db.relationship('Comment', backref='author', lazy=True)  # One-to-many relationship with Comment.

    def set_password(self, password: str):
        """
        Set the password for the user by hashing the provided password.
        
        Args:
            password (str): The raw password provided by the user.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check the provided password against the stored hashed password.

        Args:
            password (str): The raw password provided for authentication.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create_user(username: str, password: str) -> "User":
        """
        Create and save a new user with the given username and password.
        
        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.
            
        Returns:
            User: The newly created user object.
        """
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user


class Post(db.Model):
    """
    Post model represents a Post created by a user.

    Attributes:
        id (int): Post id of the Post;
            Primary key, unique identifier for each post.
        title (str): Title of the post.
        content (str): Content/body of the post.
        created_at (datetime): Timestamp when the post was created.
        user_id (int): User id of the user who created the post;
            Foreign key linking the post to the author (User model).
        
    Relationships:
        comments: One-to-many relationship with the Comment model to link posts to their comments.
    """
    
    id = db.Column(db.Integer, primary_key=True)  # Primary key.
    title = db.Column(db.String(100), nullable=False)  # Title of the post
    content = db.Column(db.Text, nullable=False)  # Main content of the post
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of post creation
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking to User

    # One-to-many relationship with Comment
    comments = db.relationship('Comment', backref='post', lazy=True) 

    @staticmethod
    def create_post(title, content, user_id) -> "Post":
        """
        Create and save a new post with the given title, content, and user ID.

        Args:
            title (str): The title of the post.
            content (str): The content of the post.
            user_id (int): The Id of the user creating the post.

        Returns:
            Post: The newly created post object.
        """
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def get_all_posts() -> List['Post']:
        """
        Retrieve all posts from the database.

        Returns:
            list: A list of all Post objects.
        """
        posts = Post.query.all()
        return posts

    @staticmethod
    def get_post_by_id(post_id) -> 'Post':
        """
        Retrieve a single post by its ID.
        
        Args:
            post_id (int): The ID of the post to retrieve.

        Returns:
            Post: The Post object with the specified ID.
        """
        post = Post.query.get(post_id)
        return post


class Comment(db.Model):
    """
    Comment model represents a comment made by a user on a post.
    
    Attributes:
        id (int): Id of the Comment made by a user;
            Primary key, unique identifier for each comment.
        post_id (int): Id of the Post to which comment belongs;
            Foreign key linking the comment to the post (Post model).
        user_id (int): ID of the User who made the comment;
            Foreign key linking the comment to the author (User model).
        content (str): Content/body of the comment.
        created_at (datetime): Timestamp when the comment was created.
    """
    
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # Foreign key linking to Post.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking to User.
    content = db.Column(db.Text, nullable=False)  # Content of the comment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of comment creation.

    @staticmethod
    def create_comment(post_id, user_id, content) -> 'Post':
        """
        Create and save a new comment with the given post Id, user Id, and content.
        
        Args:
            post_id (int): The ID of the post being commented on.
            user_id (int): The Id of the user making the comment.
            content (str): The content of the comment.
            
        Returns:
            Comment: The newly created comment object.
        """
        comment = Comment(post_id=post_id, user_id=user_id, content=content)
        db.session.add(comment)
        db.session.commit()
        return comment
