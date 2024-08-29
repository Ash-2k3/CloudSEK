from app import create_app, db
from app.models import User, Post, Comment

app = create_app()

def populate_users():
    """Create sample users."""
    users = [
        {'username': 'Ashwath', 'password': 'password123'},
        {'username': 'Kannan', 'password': 'pass123'},
        {'username': 'cloudSek', 'password': 'word@123'}
    ]
    for user_data in users:
        if not User.query.filter_by(username=user_data['username']).first():
            User.create_user(username=user_data['username'], password=user_data['password'])

def populate_posts():
    """Create sample posts."""
    users = User.query.all()
    for user in users:
        for i in range(3):  # Create 3 posts per user.
            Post.create_post(
                title=f"Post {i + 1} by {user.username}",
                content="This is a sample post content.",
                user_id=user.id
            )

def populate_comments():
    """Create sample comments."""
    posts = Post.query.all()
    users = User.query.all()
    for post in posts:
        for i in range(2):  # Create 2 comments per post.
            Comment.create_comment(
                post_id=post.id,
                user_id=users[i % len(users)].id,
                content=f"This is a comment {i + 1} on post {post.id}."
            )
    # db.session.commit()

def main():
    with app.app_context():
        db.drop_all()  # Clears the existing datastore.
        db.create_all()  # Create tables
        populate_users()
        populate_posts()
        populate_comments()
        print("Database populated with sample data.")

if __name__ == "__main__":
    main()
