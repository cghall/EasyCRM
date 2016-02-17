from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)

db = SQLAlchemy(app)

from app.auth.controller import auth
from app.core.controller import core
app.register_blueprint(auth)
app.register_blueprint(core)

db.create_all()
