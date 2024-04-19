from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, Client, Comment
from . import db
from .utils import get_next_id

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


@views.route("/forum")
@login_required
def forum():
    posts = Post.query.all()
    return render_template("forum.html", user=current_user, posts=posts)


@views.route("/dashboard")
@login_required
def client_logged_in():
    return render_template("dashboard.html", user=current_user)


@views.route("/forum/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        post_content = request.form.get("text")
        if not post_content:
            flash("Post cannot be empty!", category="error")
        else:
            post = Post(
                text=post_content,
                id_author=current_user.id_client,
                id_post=get_next_id(db, Post.id_post),
            )
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category="success")
            return redirect(url_for("views.forum"))
    return render_template("create_post.html", user=current_user)


@views.route("/forum/delete-post/<id_post>")
@login_required
def delete_post(id_post):
    post = Post.query.filter_by(id_post=id_post).first()
    if not post:
        flash("Post doesn't exist.", category="error")
    elif current_user.id_client != post.id_author:
        flash("You don't have permission to delete this post.", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.", category="success")
    return redirect(url_for("views.forum"))


@views.route("/forum/<username>")
@login_required
def posts(username):
    client = Client.query.filter_by(username=username).first()
    if not client:
        flash("No user with that username exists.", category="error")
        return redirect(url_for("views.forum"))
    posts = client.posts
    return render_template(
        "posts.html", user=current_user, posts=posts, username=username
    )


@views.route("/forum/create-comment/<id_post>", methods=["POST"])
@login_required
def create_comment(id_post):
    text = request.form.get("text")
    if not text:
        flash("Comment cannot be empty.", category="error")
    else:
        post = Post.query.filter_by(id_post=id_post)
        if post:
            comment = Comment(
                text=text,
                id_author=current_user.id_client,
                id_post=id_post,
                id_comment=get_next_id(db, Comment.id_comment),
            )
            db.session.add(comment)
            db.session.commit()
        else:
            flash("Post doesn't exist.", category="error")
    return redirect(url_for("views.forum"))


@views.route("/forum/delete-comment/<id_comment>")
@login_required
def delete_comment(id_comment):
    comment = Comment.query.filter_by(id_comment=id_comment).first()
    if not comment:
        flash("Comment does not exist.", category="error")
    elif (
        current_user.id_client != comment.id_author
        and current_user.id_client != comment.comments_under_post.id_author
    ):
        flash("You do not have permission to delete this comment.", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for("views.forum"))
