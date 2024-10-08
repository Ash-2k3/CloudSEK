"""
Defines API routes of the App.
"""

from flask import request, jsonify, Blueprint
from app.models import Post, Comment, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


bp = Blueprint('routes', __name__)

@bp.route('/')
def index_page():
    return 'Hello World'

@bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    """
    Create a new post with the provided data. Requires authentication.

    Returns:
        Response: JSON response indicating the success or failure of the post creation.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Checking if user is valid. -- TODO: Create a middleware.
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found, token might be invalid"}), 401

    new_post = Post.create_post(
        title=data.get('title'),
        content=data.get('content'),
        user_id=current_user_id
    )

    return jsonify({"msg": "Post created successfully"}), 201

@bp.route('/posts', methods=['GET'])
@bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id = None):
    """
    Retrieve posts. If a post ID is provided, retrieve that specific post; otherwise, retrieve all posts.

    Args:
        post_id (Optional[int]): The ID of the post to retrieve. If None, retrieve all posts.

    Returns:
        Response: JSON response containing the post(s) data.
    """
    if not post_id:
        posts = Post.get_all_posts()
        return jsonify([
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'comments': [
                    {
                        'id': comment.id,
                        'content': comment.content,
                        'created_at': comment.created_at,
                        'author_id': comment.user_id
                    } for comment in post.comments
                ]
            } for post in posts
        ])
    else:
        post = Post.get_post_by_id(post_id)
        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'comments': [{'id': comment.id, 'content': comment.content, 'created_at': comment.created_at, 'author_id': comment.user_id} for comment in post.comments]
        })

@bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    """
    Create a new comment for the specified post. Requires authentication.

    Returns:
        Response: JSON response indicating the success or failure of the comment creation.
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    user = User.query.get(user_id) # TODO - Create a validation method
    if not user:
        return jsonify({"msg": "User not found, token might be invalid"}), 401

    post = Post.query.get_or_404(post_id) # TODO - Create a validation method

    new_comment = Comment.create_comment(
        post_id=post.id,
        user_id=user_id,
        content=data.get('content'),
    )

    return jsonify({"msg": "Comment added successfully"}), 201

@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user with the provided username and password.

    Returns:
        Response: JSON response indicating the success or failure of the user registration.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password: # TODO - Create Validation Checks
        return jsonify({"msg": "Username and password required"}), 400

    if User.query.filter_by(username=username).first(): # TODO - Create Validation Checks
        return jsonify({"msg": "Username already exists"}), 400

    user = User.create_user(
        username,
        password
    )

    return jsonify({"msg": "User registered successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user and return an access token.

    Returns:
        Response: JSON response containing the access token or an error message.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first() # TODO - Create a validation check

    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200
