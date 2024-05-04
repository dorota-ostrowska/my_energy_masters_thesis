from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import login_required, current_user, logout_user

from website.customized_tasks import get_task_dry_laundry_outside, get_task_replace_bulbs, get_task_sleep_mode

from .models import Post, Client, Comment, Favourite, CustomizedChallange, Challange, Address
from . import db
from .utils import get_next_id
from datetime import date, timedelta
from sqlalchemy import text

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    logout_user()
    return render_template("home.html", user=current_user)


@views.route("/forum")
@login_required
def forum():
    """
    Displays all posts.
    """
    posts = Post.query.all()
    return render_template("forum.html", user=current_user, posts=posts)


def _get_unlocked_challenges(id_client: str) -> list[tuple[str, str]]:
    """
    Returns a list of tuples with names and customized descriptions of challenges
    to display them on a website.
    """
    unfinished_challanges_query: str = f"""
        select c.name, c.description, c.customizing_function
        from challange as c
        inner join customizedchallange as cc
        on cc.id_challange = c.id_challange	
        inner join client as cli
        on cli.id_client = cc.id_client
        inner join address as a
        on a.id_address = cli.id_clients_mailing_address
        where cli.id_client = {id_client}
        and (cc.is_done is false or cc.is_done is null)
        and '{date.today()}' between cc.start_date and cc.end_date;
    """
    unlocked_challanges: list[tuple[str, str, str]] = db.session.execute(text(unfinished_challanges_query)).fetchall()
    unlocked_challanges_customized: list[tuple[str, str]] = _customize_task_desciptions(unlocked_challanges)
    return unlocked_challanges_customized
    

def _get_locked_challanges(id_client: str) -> list[tuple[str, int]]:
    """
    Returns a list of tuples with names and IDs of locked challanges.
    """
    challanges_locked_query: str = f"""
        with challanges_started as (select c.name, c.id_challange 
        from challange as c
        inner join customizedchallange as cc
        on cc.id_challange = c.id_challange	
        inner join client as cli
        on cli.id_client = cc.id_client
        where cli.id_client = {id_client})
        select c.name, c.id_challange
        from challange as c
        EXCEPT 
        select name, id_challange from challanges_started
    """
    return db.session.execute(text(challanges_locked_query)).fetchall()


@views.route("/challanges")
@login_required
def challanges():
    """
    Displays all locked, available challenge names for logged in user 
    and current, unfinished, unlocked task names and desciptions.
    Locked tasks have a deliberately hidden task description to arouse 
    interest and create mystery.
    """
    return render_template("challanges.html", 
                           challanges_locked=_get_locked_challanges(current_user.id_client),
                           challanges_unlocked=_get_unlocked_challenges(current_user.id_client)
                           )


def _customize_task_desciptions(challenges: list[tuple[str, str, str]]) -> list[tuple[str, str]]:
    """
    Takes a list of tuples with names and template descriptions of challenges.
    Changes those templates to customized task descriptions.
    Argument 'challenges' contains list of tuples with name, description, customizing function 
    of challenge. 
    This function uses global() to call customizing function to change template to customized
    description.
    """
    challanges_customized = []
    for name, template, customizing_function in challenges:
        challanges_customized.append((name, globals()[customizing_function](template, current_user)))
    return challanges_customized


@views.route("/dashboard")
@login_required
def client_logged_in():
    return render_template("dashboard.html", user=current_user)


@views.route("/forum/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    """
    Creates a new post in database and next redirects user to a view of all posts.
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
            return redirect(url_for("views.forum"))
    return render_template("create_post.html", user=current_user)


def _add_challenge_to_customized_challenge(id_challenge: int) -> None:
    """
    It is called after clicking 'try' by user on a challenge.
    Adds the challenge to the customizedchallenge table.
    """
    today: date = date.today()
    next_week: date = today + timedelta(days=7)
    customized_challange = CustomizedChallange(
        id_customized_challange = get_next_id(db, CustomizedChallange.id_customized_challange),
        id_client = current_user.id_client,
        id_challange = id_challenge,
        is_done = False,
        points_scored = 0,
        start_date = today,
        end_date = next_week,
    ) 
    db.session.add(customized_challange)
    db.session.commit()   


def _get_task_customized_desciption(id_challenge: int) -> list[tuple[str, str]]:
    """
    Gets a name and a customized description of fresh unlocked challange.
    """
    fresh_unlocked_task = (
        Challange.query
        .filter_by(id_challange=id_challenge)
        .with_entities(Challange.name, Challange.description, Challange.customizing_function)
        .first()
    )
    return _customize_task_desciptions([(fresh_unlocked_task.name, fresh_unlocked_task.description, fresh_unlocked_task.customizing_function)])


@views.route("/challanges/<id_challange>")
@login_required
def try_challange(id_challange: int):
    """
    Creates a new record in CustomizedChallenge table.
    Displays a new unlocked task description.
    """
    _add_challenge_to_customized_challenge(id_challange)
    name: str
    description: str
    name, description = _get_task_customized_desciption(id_challange)[0]
    return render_template(
        "new_task.html", task_name=name, task_desciption=description)


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
