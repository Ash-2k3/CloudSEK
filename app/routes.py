from flask import request, jsonify
from app import app, db
from app.models import Post, Comment

@app.route('/')
def index_page():
           return 'Hello World'

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400
    new_post = Post(title=title, content=content)
    db.session.add(new_post)
    db.session.commit()
    print(new_post.id)
    return jsonify({'id': new_post.id, 'title': new_post.title, 'content': new_post.content}), 201

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
def add_comment(post_id):
    data = request.get_json()
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    post = Post.query.get_or_404(post_id)
    new_comment = Comment(post_id=post_id, content=content)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'id': new_comment.id, 'content': new_comment.content, 'created_at': new_comment.created_at}), 201
