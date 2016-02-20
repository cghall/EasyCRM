from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import BaseConfig
from app.extensions import bcrypt, login_manager

app = Flask(__name__)
app.config.from_object(BaseConfig)

db = SQLAlchemy(app)
bcrypt.init_app(app)
login_manager.init_app(app)

from app.auth.controller import auth
from app.core.controller import core
app.register_blueprint(auth)
app.register_blueprint(core)

db.create_all()
