from flask import Blueprint, render_template
from flask_login import login_required, current_user


home = Blueprint("home", __name__)


@home.route("/")
@home.route("/home")
def display_home():
    if current_user.is_authenticated:
        return render_template("dashboard.html", user=current_user)
    return render_template("home.html")


@home.route("/")
@home.route("/home")
@login_required
def client_logged_in():
    return render_template("dashboard.html", user=current_user)
