from flask import request, jsonify
from app import app, db
from app.models import Post, Comment, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


@app.route('/')
def index_page():
           return 'Hello World'

@app.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Checking if user is valid. -- TODO: Create a middleware.
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"msg": "User not found, token might be invalid"}), 401

    new_post = Post(
        title=data.get('title'),
        content=data.get('content'),
        user_id=current_user_id
    )

    db.session.add(new_post)
    db.session.commit()

    return jsonify({"msg": "Post created successfully"}), 201

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at,
        'comments': [{'id': comment.id, 'content': comment.content, 'created_at': comment.created_at} for comment in post.comments]
    })

@app.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found, token might be invalid"}), 401

    post = Post.query.get_or_404(post_id)

    new_comment = Comment(
        content=data.get('content'),
        post_id=post.id,
        user_id=user_id
    )

    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"msg": "Comment added successfully"}), 201

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200
