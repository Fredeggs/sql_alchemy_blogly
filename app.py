from crypt import methods
from distutils.log import debug
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
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


@app.route("/posts/<post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    first = post.user.first_name
    last = post.user.last_name
    time = post.created_at
    return render_template(
        "post.html", post=post, first_name=first, last_name=last, time=time, tags=tags
    )


@app.route("/<user_id>/posts/new")
def show_add_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new-post.html", user=user, tags=tags)


@app.route("/<user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    title = request.form["title"]
    content = request.form["content"]
    tag_ids = request.form.getlist("included-tags")
    tags = [Tag.query.get_or_404(tag_id) for tag_id in tag_ids]
    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    new_post.tags.extend(tags)
    db.session.commit()

    return redirect(f"/posts/{new_post.id}")


@app.route("/posts/<post_id>/edit")
def show_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit-post.html", post=post, tags=tags)


@app.route("/posts/<post_id>/edit", methods=["POST"])
def edit_post(post_id):
    new_title = request.form["title"]
    new_content = request.form["content"]
    tag_ids = request.form.getlist("included-tags")
    new_tags = [Tag.query.get(tag_id) for tag_id in tag_ids]
    edited_post = Post.query.get_or_404(post_id)
    edited_post.title = new_title
    edited_post.content = new_content

    old_tags = edited_post.tags
    for tag in old_tags:
        for rel in tag.post_tag:
            print(rel.post_id)
            print(post_id)
            if int(rel.post_id) == int(post_id):
                db.session.delete(rel)
    db.session.commit()

    edited_post.tags.extend(new_tags)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/{post.user_id}")


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
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")


@app.route("/tags")
def show_tags():
    tags = Tag.query.all()
    return render_template("all-tags.html", tags=tags)


@app.route("/tags/<tag_id>")
def tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts_with_tag = tag.posts
    return render_template("tag-details.html", tag=tag, posts=posts_with_tag)


@app.route("/tags/new")
def show_add_tag():
    return render_template("new-tag.html")


@app.route("/tags/new", methods=["POST"])
def create_tag():
    name = request.form["tag-name"]
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")


@app.route("/tags/<tag_id>/edit")
def show_edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit-tag.html", tag=tag)


@app.route("/tags/<tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    new_name = request.form["tag-name"]
    tag = Tag.query.get_or_404(tag_id)
    tag.name = new_name
    db.session.commit()
    return redirect(f"/tags/{tag.id}")


@app.route("/tags/<tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")
