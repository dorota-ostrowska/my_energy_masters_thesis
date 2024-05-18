"""
A view.
User's challenges.
"""

import random
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from website.customized_tasks import (
    get_task_dry_laundry_outside,
    get_task_replace_bulbs,
    get_task_sleep_mode,
)
from website.game.badges import all_badges

from .models import (
    Client,
    CustomizedChallenge,
    Challenge,
)
from . import db
from .utils import get_next_id
from datetime import date, timedelta
from sqlalchemy import or_


challenge = Blueprint("challenge", __name__)


def _get_unlocked_challenges(id_client: int) -> list[Challenge]:
    """
    Retrieve unlocked challenges for a given client.

    Args:
        id_client (int): The ID of the client.

    Returns:
        list[Challenge]: A list of unlocked Challenge objects for the client.

    This function queries the database to retrieve challenges that are unlocked for the given client.
    It checks if the client has any customized challenges that are not marked as done and are within
    the start and end date range. The unlocked challenges are returned as a list of Challenge objects.
    """
    return (
        db.session.query(Challenge)
        .join(
            CustomizedChallenge,
            CustomizedChallenge.id_challenge == Challenge.id_challenge,
        )
        .join(Client, Client.id_client == CustomizedChallenge.id_client)
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


def _get_locked_challenges(id_client: int) -> list[Challenge]:
    """
    Retrieve locked challenges for a given client.

    Args:
        id_client (int): The ID of the client.

    Returns:
        list[Challenge]: A list of locked Challenge objects for the client.

    This function retrieves challenges that the client has not started yet. It first gets the IDs of
    challenges that the client has already started, then retrieves challenges that the client has not
    started by excluding those IDs. The locked challenges are returned as a list of Challenge objects.
    """
    challenges_started = (
        db.session.query(CustomizedChallenge.id_challenge)
        .join(Client, Client.id_client == CustomizedChallenge.id_client)
        .filter(Client.id_client == id_client)
        .all()
    )
    challenges_started_ids = [row[0] for row in challenges_started]
    locked_challenges = (
        db.session.query(Challenge)
        .filter(~Challenge.id_challenge.in_(challenges_started_ids))
        .all()
    )
    return locked_challenges


@challenge.route("/")
@login_required
def display_challenges():
    """
    If the user hasn't completed the questionnaire regarding the number of rooms
    or residents, they are redirected to the questionnaire page.
    If the user is not a member of any challenge, they are redirected to the game story page.

    Returns:
        rendered_template: HTML template displaying the challenges and tasks for the user.
            The template includes:
                - Locked challenges with deliberately hidden task descriptions to arouse interest.
                - Unlocked challenges with task names and descriptions customized for the user.

    Raises:
        Redirect: If the user hasn't completed the questionnaire or is not a member of any challenge,
            they are redirected to the respective pages.

    """
    logged_in_user = Client.query.filter_by(id_client=current_user.id_client).first()
    if not logged_in_user.number_of_rooms or not logged_in_user.number_of_residents:
        return redirect(url_for("challenge.questionnaire"))
    elif not logged_in_user.member_of_challenge:
        return redirect(url_for("challenge.game_story"))
    return render_template(
        "challenge.html",
        challenges_locked=_get_locked_challenges(current_user.id_client),
        challenges_unlocked=_customize_task_desciptions(
            _get_unlocked_challenges(current_user.id_client),
        ),
    )


def _customize_task_desciptions(
    challenges: list[Challenge],
) -> list[tuple[Challenge, str]]:
    """
    Customize task descriptions for the given challenges.

    Args:
        challenges (list[Challenge]): A list of Challenge objects representing the challenges.

    Returns:
        list[tuple[Challenge, str]]: A list of tuples containing Challenge objects and their
            customized descriptions.

    This function takes a list of Challenge objects and customizes their descriptions based
    on the user's current state or profile. It iterates through each challenge and applies
    a customizing function to modify the description. The customized descriptions, along
    with their corresponding Challenge objects, are stored in tuples and returned as a list.
    """
    challenges_customized = []
    if isinstance(challenges, list):
        for challenge in challenges:
            custom_description = globals()[challenge.customizing_function](
                challenge.description, current_user
            )
            challenges_customized.append((challenge, custom_description))
    else:
        custom_description = globals()[challenges.customizing_function](
            challenges.description, current_user
        )
        challenges_customized.append((challenges, custom_description))
    return challenges_customized


def _add_challenge_to_customized_challenge(id_challenge: int) -> None:
    """
    Adds the specified challenge to the CustomizedChallenge table for the current user.

    This function is typically called after the user clicks 'try' on a challenge.
    It creates a new entry in the CustomizedChallenge table, associating the challenge
    with the current user and setting the start date to today and the end date to a week from today.

    Args:
        id_challenge (int): The ID of the challenge to be added to the CustomizedChallenge table.
    """
    today: date = date.today()
    next_week: date = today + timedelta(days=8)
    next_month: date = today + timedelta(days=31)
    challenge_type = get_challenge_type(id_challenge)
    if challenge_type == "S":
        end_date = next_week
    else:
        end_date = next_month
    challenge_exists = CustomizedChallenge.query.filter_by(id_challenge=id_challenge, id_client=current_user.id_client).first()
    if challenge_exists:
        return
    customized_challenge = CustomizedChallenge(
        id_customized_challenge=get_next_id(
            db, CustomizedChallenge.id_customized_challenge
        ),
        id_client=current_user.id_client,
        id_challenge=id_challenge,
        is_done=False,
        points_scored=0,
        start_date=today,
        end_date=end_date,
    )
    db.session.add(customized_challenge)
    db.session.commit()


def _get_challenge_by_id(id_challenge: int) -> Challenge:
    """
    Retrieves the details of a challenge by its ID.

    Args:
        id_challenge (int): The ID of the challenge to retrieve details for.

    Returns:
        Challenge: An instance of the Challenge model.
    """
    return (
        Challenge.query.filter_by(id_challenge=id_challenge)
        .with_entities(
            Challenge.name, Challenge.description, Challenge.customizing_function
        )
        .first()
    )


@challenge.route("/<id_challenge>")
@login_required
def try_challenge(id_challenge: int):
    """
    Handles the user's attempt to try a challenge.

    This function creates a new record in the CustomizedChallenge table
    for the specified challenge ID, indicating that the user is attempting
    the challenge. It then retrieves and displays the description of a new
    unlocked task associated with the challenge.

    Args:
        id_challenge (int): The ID of the challenge the user wants to try.

    Returns:
        rendered_template: HTML template displaying the new task description
            along with details of the challenge.
    """
    _add_challenge_to_customized_challenge(id_challenge)
    challenge, task_desciption = _customize_task_desciptions(
        _get_challenge_by_id(id_challenge)
    )[0]
    return render_template(
        "new_task.html", challenge=challenge, task_desciption=task_desciption
    )


@challenge.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():
    """
    Handles the questionnaire form submission.

    If the request method is POST, the function attempts to retrieve
    the number of rooms and residents entered by the user. If any value
    entered is not an integer, it flashes an error message.

    The function then updates the user's profile with the entered values
    for the number of rooms and residents and commits the changes to the
    database.

    If the request method is GET, the function renders the questionnaire
    template, passing the current user's information.

    Returns:
        rendered_template: HTML template displaying the questionnaire form
            for the user to fill out.
    """
    if request.method == "POST":
        try:
            number_of_rooms = int(request.form.get("number_of_rooms"))
            number_of_residents = int(request.form.get("number_of_residents"))
        except ValueError:
            flash("You entered a wrong value.", category="error")
        user = Client.query.filter_by(id_client=current_user.id_client).first()
        user.number_of_rooms = number_of_rooms
        user.number_of_residents = number_of_residents
        db.session.commit()
        return redirect(url_for("home.client_logged_in"))
    return render_template("questionnaire.html", user=current_user)


@challenge.route("/game-story", methods=["GET", "POST"])
@login_required
def game_story():
    """
    Displays either challenges or the main game story window, depending on the user's participation status.

    If the request method is POST and the user enrolls in a challenge, it updates the user's profile
    to indicate their participation and redirects to the page displaying challenges.

    If the request method is GET, it reads the main game story from a text file and renders the game story template,
    passing the story content.

    Returns:
        rendered_template: HTML template displaying either the challenges or the main game story window.
    """
    if request.method == "POST":
        user = Client.query.filter_by(id_client=current_user.id_client).first()
        user.member_of_challenge = True
        db.session.commit()
        return redirect(url_for("challenge.display_challenges"))
    with open("website/game/main_story.txt", "r", encoding="utf-8") as file:
        story = file.read()
    return render_template("game_story.html", story=story)


@challenge.route("/finish-challenge/<id_challenge>", methods=["POST"])
@login_required
def finish_challenge(id_challenge):
    """
    Mark the challenge as finished for the current user.
    """
    customized_challenge = CustomizedChallenge.query.filter_by(
        id_client=current_user.id_client, id_challenge=id_challenge
    ).first()
    client = Client.query.filter_by(
        id_client=current_user.id_client
    ).first()
    if customized_challenge:
        customized_challenge.is_done = True
        ch_type: str = get_challenge_type(customized_challenge.id_challenge)
        random_badge = get_random_badge(ch_type)
        customized_challenge.points_scored = random_badge.points
        client.points = client.points + random_badge.points
        db.session.commit()
        flash("Challenge finished successfully!", "success")
        return redirect(url_for('challenge.congratulations', badge_name=random_badge.name))
    else:
        flash("Challenge not found or not started.", "error")
    return redirect(url_for("challenge.display_challenges"))


@challenge.route("/congratulations/<badge_name>")
@login_required
def congratulations(badge_name):
    """
    Display the congratulations page with the earned badge.
    """
    points = 0
    pic = ""
    for badge in all_badges:
        if badge.name == badge_name:
            points = badge.points
            pic = badge.picture
            break
    return render_template("congratulations.html", badge_name=badge_name, points = points, pic = pic, username=current_user.username)


@challenge.route("/resign-challenge/<int:id_challenge>", methods=["POST"])
@login_required
def resign_challenge(id_challenge):
    """
    Resign from the challenge for the current user.
    """
    customized_challenge = CustomizedChallenge.query.filter_by(
        id_client=current_user.id_client, id_challenge=id_challenge
    ).first()
    if customized_challenge:
        db.session.delete(customized_challenge)
        db.session.commit()
        flash("Resigned from challenge successfully.", "success")
    else:
        flash("Challenge not found or not started.", "error")
    return redirect(url_for("challenge.display_challenges"))


def get_random_badge(ch_type: str):
    if ch_type not in ["S", "B"]:
        raise ValueError("Challenge type must be either 'S' or 'B'")
    if ch_type == "S":
        weights = [badge.randomness_small_challenge for badge in all_badges]
    else:
        weights = [badge.randomness_big_challenge for badge in all_badges]
    selected_badge = random.choices(all_badges, weights=weights, k=1)[0]
    return selected_badge

def get_challenge_type(id_challenge: int) -> str:
    challenge = Challenge.query.filter_by(id_challenge=id_challenge).first()
    return challenge.type_small_big
