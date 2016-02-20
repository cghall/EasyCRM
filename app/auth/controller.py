from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user

from app.auth.forms import LoginForm
from app.auth.models import User
from app.extensions import login_manager
from app import db

auth = Blueprint('auth', __name__, template_folder='templates/auth')

@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        form.user.authenticated = True
        db.session.add(form.user)
        db.session.commit()
        login_user(form.user)
    return render_template('auth/login.html', form=form)