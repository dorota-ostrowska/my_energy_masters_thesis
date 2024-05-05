from flask import Blueprint, flash, jsonify, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from website.customized_tasks import (
    get_task_dry_laundry_outside,
    get_task_replace_bulbs,
    get_task_sleep_mode,
)

from .models import (
    Post,
    Client,
    Comment,
    Favourite,
    CustomizedChallenge,
    Challenge,
    Address,
)
from . import db
from .utils import get_next_id
from datetime import date, timedelta
from sqlalchemy import or_, text

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    if current_user.is_authenticated:
        return render_template("dashboard.html", user=current_user)
    return render_template("home.html")


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
    unlocked_challenges = (
        db.session.query(
            Challenge.name, Challenge.description, Challenge.customizing_function
        )
        .join(
            CustomizedChallenge,
            CustomizedChallenge.id_challenge == Challenge.id_challenge,
        )
        .join(Client, Client.id_client == CustomizedChallenge.id_client)
        .join(Address, Address.id_address == Client.id_clients_mailing_address)
        .filter(
            Client.id_client == id_client,
            or_(
                CustomizedChallenge.is_done == False,
                CustomizedChallenge.is_done.is_(None),
            ),
            CustomizedChallenge.start_date <= date.today(),
            CustomizedChallenge.end_date >= date.today(),
        )
        .all()
    )
    unlocked_challenges_customized: list[tuple[str, str]] = _customize_task_desciptions(
        unlocked_challenges
    )
    return unlocked_challenges_customized


def _get_locked_challenges(id_client: str) -> list[tuple[str, int]]:
    """
    Returns a list of tuples with names and IDs of locked challenges.
    """
    challenges_locked_query: str = f"""
        with challenges_started as (select c.name, c.id_challenge 
        from challenge as c
        inner join customizedchallenge as cc
        on cc.id_challenge = c.id_challenge	
        inner join client as cli
        on cli.id_client = cc.id_client
        where cli.id_client = {id_client})
        select c.name, c.id_challenge
        from challenge as c
        EXCEPT 
        select name, id_challenge from challenges_started
    """
    return db.session.execute(text(challenges_locked_query)).fetchall()


@views.route("/challenges")
@login_required
def challenges():
    """
    Displays all locked, available challenge names for logged in user
    and current, unfinished, unlocked task names and desciptions.
    Locked tasks have a deliberately hidden task description to arouse
    interest and create mystery.
    """
    return render_template(
        "challenges.html",
        challenges_locked=_get_locked_challenges(current_user.id_client),
        challenges_unlocked=_get_unlocked_challenges(current_user.id_client),
    )


def _customize_task_desciptions(
    challenges: list[tuple[str, str, str]]
) -> list[tuple[str, str]]:
    """
    Takes a list of tuples with names and template descriptions of challenges.
    Changes those templates to customized task descriptions.
    Argument 'challenges' contains list of tuples with name, description, customizing function
    of challenge.
    This function uses global() to call customizing function to change template to customized
    description.
    """
    challenges_customized = []
    for name, template, customizing_function in challenges:
        challenges_customized.append(
            (name, globals()[customizing_function](template, current_user))
        )
    return challenges_customized


@views.route("/home")
@views.route("/")
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
    customized_challenge = CustomizedChallenge(
        id_customized_challenge=get_next_id(
            db, CustomizedChallenge.id_customized_challenge
        ),
        id_client=current_user.id_client,
        id_challenge=id_challenge,
        is_done=False,
        points_scored=0,
        start_date=today,
        end_date=next_week,
    )
    db.session.add(customized_challenge)
    db.session.commit()


def _get_task_customized_desciption(id_challenge: int) -> list[tuple[str, str]]:
    """
    Gets a name and a customized description of fresh unlocked challenge.
    """
    fresh_unlocked_task = (
        Challenge.query.filter_by(id_challenge=id_challenge)
        .with_entities(
            Challenge.name, Challenge.description, Challenge.customizing_function
        )
        .first()
    )
    return _customize_task_desciptions(
        [
            (
                fresh_unlocked_task.name,
                fresh_unlocked_task.description,
                fresh_unlocked_task.customizing_function,
            )
        ]
    )


@views.route("/challenges/<id_challenge>")
@login_required
def try_challenge(id_challenge: int):
    """
    Creates a new record in CustomizedChallenge table.
    Displays a new unlocked task description.
    """
    _add_challenge_to_customized_challenge(id_challenge)
    name: str
    description: str
    name, description = _get_task_customized_desciption(id_challenge)[0]
    return render_template("new_task.html", task_name=name, task_desciption=description)


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
