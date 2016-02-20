from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('Username', [DataRequired(message='Enter your Username')])
    password = PasswordField('Password', [DataRequired(message='Enter your Password')])
