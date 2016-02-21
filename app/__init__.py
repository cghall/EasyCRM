from flask import Flask

from config import BaseConfig
from app.extensions import bcrypt, login_manager
from app.database import db
from app.core import core as core_blueprint
from app.auth import auth as auth_blueprint


def create_app(config=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    bcrypt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(core_blueprint)
