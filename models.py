from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import table, func

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """A User for the Blogly app"""

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image={u.image_url}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(
        db.String(200),
        default="https://thumbs.dreamstime.com/b/default-avatar-profile-image-vector-social-media-user-icon-potrait-182347582.jpg",
    )

    post = db.relationship("Post", backref="user", cascade="all, delete-orphan")


class Post(db.Model):
    """A Post for the Blogly app"""

    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    tags = db.relationship("Tag", secondary="posts_tags", backref="posts")


class Tag(db.Model):
    """A Tag pertaining to Posts in the Blogly app"""

    __tablename__ = "tags"

    def __repr__(self):
        t = self
        return f"<Tag id={t.id}, name={t.name}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), unique=True)


class PostTag(db.Model):

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    tag = db.relationship("Tag", backref="post_tag")
    post = db.relationship("Post", backref="post_tag")
