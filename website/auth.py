"""
A view.
Authorization to MyEnergy service - login and register functions.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Client
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    View function for handling user login.

    If the request method is POST, the function attempts to log in the user
    using the provided username and password. If the username exists and the
    password is correct, the user is logged in and redirected to the dashboard.
    If the password is incorrect, an error message is flashed. If the username
    does not exist, another error message is flashed.

    If the request method is GET, the function renders the login page.

    Returns:
        If the user is logged in successfully, redirects to the dashboard.
        Otherwise, renders the login page.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        client = Client.query.filter_by(username=username).first()
        if client:
            if check_password_hash(client.password, password):
                flash("Logged in!", category="success")
                login_user(client, remember=True)
                return redirect(url_for("home.client_logged_in"))
            else:
                flash("Password is incorrect.", category="error")
        else:
            flash("Username doesn't exist.", category="error")
    return render_template("login.html", user=current_user)


@auth.route("/register", methods=["GET", "POST"])
def register():
    """
    View function for user registration.

    If the request method is POST, the function attempts to register a new user
    using the provided registration data. If the data is valid, a new client
    is created, and the user is logged in, then redirected to the questionnaire page.
    If there are validation errors, error messages are flashed to the user.

    If the request method is GET, the function renders the registration form.

    Returns:
        If the user is registered successfully, redirects to the questionnaire page.
        Otherwise, renders the registration form with error messages.
    """
    if request.method == "POST":
        id_client = request.form.get("id_client")
        pesel = request.form.get("pesel")
        username = request.form.get("username")
        email = request.form.get("email")
        password_1 = request.form.get("password1")
        password_2 = request.form.get("password2")

        client = (
            Client.query.filter_by(id_client=id_client).filter_by(pesel=pesel).first()
        )
        error = validate_registration_data(
            client, username, email, password_1, password_2
        )
        if error:
            flash(error, category="error")
        else:
            client_is_created = create_client(client, username, email, password_1)
            if client_is_created:
                login_user(client, remember=True)
                return redirect(url_for("challange.questionnaire"))
    return render_template("register.html", user=current_user)


def validate_registration_data(
    client, username, email, password_1, password_2
) -> str | None:
    """
    Validate registration data.

    Args:
        client: An instance of the Client model.
        username: The username for the new client from register form.
        email: The email address for the new client from register form.
        password_1: The first password entered during registration.
        password_2: The second password entered during registration.

    Returns:
        An error message if there's a validation error, otherwise None.
    """
    if not client:
        return "Your meter is not smart, there is no data in our system."
    elif client and client.username:
        return "You already have an account, try to log in."
    elif Client.query.filter_by(email=email).first():
        return "Email is already in use."
    elif Client.query.filter_by(username=username).first():
        return "Username is already in use, try again with another username."
    elif password_1 != password_2:
        return "Passwords don't match."
    elif len(username) < 6:
        return "Your username is too short."
    elif len(password_1) < 8:
        return "Your password is too short, use at least 8 characters."
    return None


def create_client(client: Client, username: str, email: str, password: str) -> bool:
    """
    Function to create a new client.

    Args:
        client: An instance of the Client model representing the client to be created.
        username: The username for the new client from register form.
        email: The email address for the new client from register form.
        password: The password for the new client from register form.

    Returns:
        A boolean indicating whether the client creation was successful or not.
        Returns True if the client was successfully created, False otherwise.
    """
    try:
        client.username = username
        client.email = email
        client.password = str(generate_password_hash(password, method="sha256"))
        db.session.commit()
        return True
    except Exception:
        return False


@auth.route("/logout")
@login_required
def logout():
    """
    View function for handling user logout.

    Logs out the current user if they are logged in and redirects them to the home page.

    Returns:
        Redirects the user to the home page after logging them out.
    """
    logout_user()
    return redirect(url_for("home.display_home"))
