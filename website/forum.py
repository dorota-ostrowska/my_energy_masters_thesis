"""
A view.
Forum of MyEnergy users. They can create posts, comment and like.
"""

from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from .models import (
    Post,
    Client,
    Comment,
    Favourite,
)
from . import db
from .utils import get_next_id

forum = Blueprint("forum", __name__)


@forum.route("/")
@login_required
def display_forum():
    """
    Displays all posts in the forum.

    Returns:
        Rendered HTML template displaying all posts.
    """
    posts = Post.query.all()
    return render_template("forum.html", user=current_user, posts=posts)


@forum.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    """
    Handles creation of a new post.

    If the request method is POST, it attempts to create a new post using the provided data.
    If successful, it adds the post to the database and redirects to the forum page.

    Returns:
        If the post is successfully created, redirects to the forum page.
        Otherwise, renders the create post form.
    """
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
            return redirect(url_for("forum.display_forum"))
    return render_template("create_post.html", user=current_user)


@forum.route("/delete-post/<id_post>")
@login_required
def delete_post(id_post):
    """
    Deletes a post.

    Args:
        id_post: The ID of the post to delete.

    Returns:
        Redirects to the forum page after deleting the post.
    """
    post = Post.query.filter_by(id_post=id_post).first()
    if not post:
        flash("Post doesn't exist.", category="error")
    elif current_user.id_client != post.id_author:
        flash("You don't have permission to delete this post.", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.", category="success")
    return redirect(url_for("forum.display_forum"))


@forum.route("/<username>")
@login_required
def display_posts(username):
    """
    Displays posts authored by a specific user.

    Args:
        username: Username of the user whose posts are to be displayed.

    Returns:
        If the user exists, renders HTML template displaying posts authored by the user.
        If the user does not exist, flashes an error message and redirects to the forum page.
    """
    client = Client.query.filter_by(username=username).first()
    if not client:
        flash("No user with that username exists.", category="error")
        return redirect(url_for("forum.display_forum"))
    posts = client.posts
    return render_template(
        "posts.html", user=current_user, posts=posts, username=username
    )


@forum.route("/create-comment/<id_post>", methods=["POST"])
@login_required
def create_comment(id_post):
    """
    Handles creation of a comment on a post.

    If the request method is POST, it attempts to create a new comment on the specified post.
    If successful, adds the comment to the database and redirects to the forum page.

    Returns:
        If the comment is successfully created, redirects to the forum page.
        Otherwise, redirects to the forum page.
    """
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
    return redirect(url_for("forum.display_forum"))


@forum.route("/delete-comment/<id_comment>")
@login_required
def delete_comment(id_comment):
    """
    Deletes a comment.

    Args:
        id_comment: ID of the comment to be deleted.

    Returns:
        Redirects to the forum page after deleting the comment.
    """
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
    return redirect(url_for("forum.display_forum"))


@forum.route("/like/<id_post>", methods=["POST"])
@login_required
def like(id_post):
    """
    Handles liking/unliking a post.

    If the post exists, adds or removes a like by the current user.
    Returns a JSON response with information about the post's likes.

    Returns:
        JSON response containing post likes information.
    """
    post = Post.query.filter_by(id_post=id_post).first()
    like = Favourite.query.filter_by(
        id_author=current_user.id_client, id_post=id_post
    ).first()
    if not post:
        return jsonify({"error": "Post does not exist."}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Favourite(
            id_author=current_user.id_client,
            id_post=id_post,
            id_like=get_next_id(db, Favourite.id_like),
        )
        db.session.add(like)
        db.session.commit()
    return jsonify(
        {
            "likes": len(post.likes),
            "liked": current_user.id_client in map(lambda x: x.id_author, post.likes),
        }
    )
