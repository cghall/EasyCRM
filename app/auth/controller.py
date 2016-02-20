from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user

from app.auth.forms import LoginForm
from app.auth.models import User
from app.extensions import login_manager


auth = Blueprint('auth', __name__, template_folder='templates/auth')

@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user)
            return redirect(url_for('core.home'))
        else:
            error = 'Invalid username/password'
    return render_template('auth/login.html', form=form, error=error)