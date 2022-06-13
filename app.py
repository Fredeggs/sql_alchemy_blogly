from crypt import methods
from distutils.log import debug
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "chickens123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def list_users():
    all_users = User.query.all()
    return render_template("users.html", users=all_users)


@app.route("/add-user")
def add_user():
    return render_template("new-user.html")


@app.route("/add-user", methods=["POST"])
def create_user():
    first = request.form["first"]
    last = request.form["last"]
    image = request.form["image"]
    if image == "":
        image = "https://thumbs.dreamstime.com/b/default-avatar-profile-image-vector-social-media-user-icon-potrait-182347582.jpg"

    new_user = User(first_name=first, last_name=last, image_url=image)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/{new_user.id}")


@app.route("/<user_id>")
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template("user-details.html", user=user, posts=posts)


@app.route("/<user_id>/posts/<post_id>")
def show_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", user=user, post=post)


@app.route("/<user_id>/posts/new")
def show_add_post(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("new-post.html", user=user)


@app.route("/<user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/{user_id}/posts/{new_post.id}")


@app.route("/<user_id>/edit-user")
def show_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)


@app.route("/<user_id>/edit-user", methods=["POST"])
def edit_user(user_id):
    first = request.form["first"]
    last = request.form["last"]
    image = request.form["image"]
    if image == "":
        image = "https://thumbs.dreamstime.com/b/default-avatar-profile-image-vector-social-media-user-icon-potrait-182347582.jpg"

    edited_user = User.query.get_or_404(user_id)
    edited_user.first_name = first
    edited_user.last_name = last
    edited_user.image_url = image
    db.session.commit()
    return redirect(f"/{user_id}")


@app.route("/<user_id>/delete-user", methods=["POST"])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")
