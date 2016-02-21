from wtforms_alchemy import ModelForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import Form

from app.core.models import Contact, Organisation


class CreateContact(ModelForm):
    class Meta:
        model = Contact


class CreateOrganisation(Form):

    name = StringField('Organisation Name', [DataRequired()])
    type = SelectField('Organisation Type', choices=Organisation.TYPE_CHOICE)
    address = TextAreaField('Address')
