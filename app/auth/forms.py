from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .models import User


class LoginForm(Form):
    username = StringField('Username', [DataRequired(message='Enter your Username')])
    password = PasswordField('Password', [DataRequired(message='Enter your Password')])

    def validate_password(form, field):
        try:
            user = User.query.filter(User.username == form.username.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Invalid user")
        if user is None:
            raise ValidationError("Invalid user")
        if not user.is_correct_password(form.password.data):
            raise ValidationError("Invalid password")
        form.user = user
        return True