from flask import Blueprint, flash, render_template, request
from flask_login import login_required, current_user
from .models import Post
from . import db
from .utils import get_next_id

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

@views.route("/dashboard")
@login_required
def client_logged_in():
    return render_template("dashboard.html", user=current_user)

@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        post_content = request.form.get("text")
        if not post_content:
            flash("Post cannot be empty!", category="error")
        else:
            post = Post(
                text=post_content,
                author=current_user.id_client,
                id_post=get_next_id(db, Post.id_post)
                )
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category="success")
    return render_template("create_post.html", user=current_user)
    