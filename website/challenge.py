"""
A view.
User's challenges.
"""
from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from website.customized_tasks import (
    get_task_dry_laundry_outside,
    get_task_replace_bulbs,
    get_task_sleep_mode,
)

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
        challenges_unlocked=_customize_task_desciptions(_get_unlocked_challenges(current_user.id_client),
    ))


def _customize_task_desciptions(challenges: list[Challenge]) -> list[tuple[Challenge, str]]:
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
    for challenge in challenges:
        custom_description = globals()[challenge.customizing_function](
            challenge.description, current_user
        )
        challenges_customized.append((challenge, custom_description))
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


@challenge.route("/<id_challenge>")
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


@challenge.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():
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
    If user takes part in challenge, it displays challenges,
    if user does not, it displays a window with a main history and possibility to
    enroll to challenge.
    """
    if request.method == "POST":
        user = Client.query.filter_by(id_client=current_user.id_client).first()
        user.member_of_challenge = True
        db.session.commit()
        return redirect(url_for("challenge.display_challenges"))
    with open("website/game/main_story.txt", "r", encoding="utf-8") as file:
        story = file.read()
    return render_template("game_story.html", story=story)
