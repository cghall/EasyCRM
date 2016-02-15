from flask import Blueprint, request, render_template, flash, redirect, url_for, session

from app.auth.forms import LoginForm
from app.auth.models import User


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.name.data).first()
        if user and form.data.password == user.password:
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            return redirect(url_for('auth.home'))
        flash('Wrong email or password')
    return render_template('auth/login.html', form=form)