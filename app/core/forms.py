from flask_wtf import Form
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class CreateContact(Form):

    first_name = StringField('First Name', [DataRequired(message='First Name is required.')])
    last_name = StringField('Last Name', [DataRequired(message='Last Name is required.')])
    email = EmailField('Email', [DataRequired(message='Email is required.')])
