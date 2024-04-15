from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import json
from typing import Dict

app = Flask(__name__)
app.secret_key = "super secret key"
with open("./appconfig.json", "r") as file:
    json_data: Dict = json.load(file)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{json_data["user"]}:{json_data["password"]}@{json_data["host"]}/{json_data["database"]}"
# db.init_app(app)
db = SQLAlchemy(app)

def create_app():
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

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
