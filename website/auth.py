from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Client
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func
from .utils import get_next_id

HOME_VIEW = "views.home"
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        client = Client.query.filter_by(username=username).first()
        if client:
            if check_password_hash(client.password, password):
                flash("Logged in!", category="success")
                login_user(client, remember=True)
                return redirect(url_for("views.client_logged_in"))
            else:
                flash("Password is incorrect.", category="error")
        else:
            flash("Username doesn\'t exist.", category="error")
    return render_template("login.html", user=current_user)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        surname = request.form.get("surname")
        username = request.form.get("username")
        pesel = request.form.get("pesel")
        password_1 = request.form.get("password1")
        password_2 = request.form.get("password2")

        if Client.query.filter_by(email=email).first():
            flash("Email is already in use, you have an account.", category="error")
        elif Client.query.filter_by(username=username).first():
            flash("Username is already in use, try again.", category="error")
        elif Client.query.filter_by(pesel=pesel).first():
            flash("PESEL is already in use, you have an account.", category="error")
        elif password_1 != password_2:
            flash("Passwords don\'t match.", category="error")
        elif len(username) < 6:
            flash("Your username is too short.", category="error")
        elif len(password_1) < 8:
            flash("Your password is too short, use at least 8 characters.", category="error")
        else:
            new_client = Client(
                id_client=get_next_id(db, Client.id_client),
                username=username,
                name=name,
                surname=surname,
                pesel=pesel,
                address_id_address=0,
                email=email,
                password=str(generate_password_hash(password_1, method="sha256")),
            )
            db.session.add(new_client)
            db.session.commit()
            login_user(new_client, remember=True)
            flash(f"{username} client created!")
            return redirect(url_for(HOME_VIEW))
    return render_template("register.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(HOME_VIEW))
