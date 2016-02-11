from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)

db = SQLAlchemy(app)
db.create_all()


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
