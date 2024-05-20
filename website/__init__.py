"""
Website initialization module.

This module initializes the Flask application, configures database connection, and registers blueprints for different parts of the website.

Functions:
    create_app: Creates and configures the Flask application.

Attributes:
    app (Flask): The Flask application instance.
    db (SQLAlchemy): The SQLAlchemy database instance.

This module sets up the Flask application, including secret key configuration, database connection, and registration of blueprints for various parts of the website, such as home, authentication, forum, and challenge functionalities.

The `create_app` function initializes the Flask app, registers blueprints, creates necessary database tables, configures login manager, and loads user information.

It also provides access to the `app` and `db` objects, representing the Flask application instance and the SQLAlchemy database instance respectively, which can be used throughout the website.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json
from website.secret import FLASK_KEY

app = Flask(__name__)
app.secret_key = FLASK_KEY
with open("./appconfig.json", "r") as file:
    json_data: dict = json.load(file)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{json_data['user']}:{json_data['password']}@{json_data['host']}/{json_data['database']}"
)
db = SQLAlchemy(app)


def create_app():
    from .home import home
    from .auth import auth
    from .forum import forum
    from .challenge import challenge

    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/user")
    app.register_blueprint(forum, url_prefix="/forum")
    app.register_blueprint(challenge, url_prefix="/challenge")

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import Client

    @login_manager.user_loader
    def load_client(id_client):
        return Client.query.get(int(id_client))

    return app
