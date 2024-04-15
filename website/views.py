from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")

@views.route("/dashboard")
@login_required
def client_logged_in():
    return render_template("dashboard.html", name=current_user.username)
    