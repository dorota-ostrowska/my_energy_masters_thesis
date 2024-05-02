from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from website.customized_tasks import get_task_dry_laundry_outside, get_task_replace_bulbs, get_task_sleep_mode

from .models import Post, Client, Comment, Favourite, CustomizedChallange, Challange
from . import db
from .utils import get_next_id
from datetime import date, timedelta
from sqlalchemy import text

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


@views.route("/challanges")
@login_required
def challanges():
    """
    Displays all available challanges for logged in user.
    """
    challanges_not_unlocked_query = f"""
        with challanges_started as (select c.name, c.id_challange 
        from challange as c
        inner join customizedchallange as cc
        on cc.id_challange = c.id_challange	
        inner join client as cli
        on cli.id_client = cc.id_client
        where cli.id_client = {current_user.id_client})
        select c.name, c.id_challange
        from challange as c
        EXCEPT 
        select name, id_challange from challanges_started
    """
    challanges_not_unlocked = db.session.execute(text(challanges_not_unlocked_query)).fetchall()
    unfinished_challanges_query = f"""
        select c.name, c.description, c.customizing_function
        from challange as c
        inner join customizedchallange as cc
        on cc.id_challange = c.id_challange	
        inner join client as cli
        on cli.id_client = cc.id_client
        inner join address as a
        on a.id_address = cli.id_clients_mailing_address
        where cli.id_client = {current_user.id_client}
        and (cc.is_done is false or cc.is_done is null)
        and '{date.today()}' between cc.start_date and cc.end_date;
    """
    unfinished_challanges = db.session.execute(text(unfinished_challanges_query)).fetchall()

    unfinished_challanges_customized = _customize_task_desciptions(unfinished_challanges)
    return render_template("challanges.html", 
                           challanges_not_unlocked=challanges_not_unlocked,
                           unfinished_challanges=unfinished_challanges_customized)

def _customize_task_desciptions(challanges):
    """
    challanges - list[tuple] - name, description, customizing function
    """
    challanges_customized = []
    for name, template, customizing_function in challanges:
        challanges_customized.append((name, globals()[customizing_function](template, current_user)))
    return challanges_customized


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


@views.route("/challanges/<id_challange>")
@login_required
def try_challange(id_challange):
    today: date = date.today()
    next_week: date = today + timedelta(days=7)
    customized_challange = CustomizedChallange(
        id_customized_challange = get_next_id(db, CustomizedChallange.id_customized_challange),
        id_client = current_user.id_client,
        id_challange = id_challange,
        is_done = False,
        points_scored = 0,
        start_date = today,
        end_date = next_week,
    ) 
    db.session.add(customized_challange)
    db.session.commit()
    unlocked_task_query = f"""
        select c.name, c.description, c.customizing_function
        from challange as c
        where c.id_challange = {id_challange}
    """
    unlocked_task = db.session.execute(text(unlocked_task_query)).fetchall()
    task_desciption = _customize_task_desciptions(unlocked_task)[0][1]
    return render_template(
        "new_task.html", customized_challange=customized_challange, task_desciption=task_desciption)

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


@views.route("/forum/like/<id_post>", methods=["POST"])
@login_required
def like(id_post):
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
