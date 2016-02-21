from flask import request, render_template, redirect, url_for
from flask_login import login_user

from app.auth.forms import LoginForm
from app.auth.models import User
from app.extensions import login_manager
from . import auth
from app.database import db


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        form.user.authenticated = True
        db.session.add(form.user)
        db.session.commit()
        login_user(form.user)
        return redirect(url_for('core.home'))
    return render_template('auth/login.html', form=form)

