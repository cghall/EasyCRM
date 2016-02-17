from wtforms_alchemy import ModelForm

from app.core.models import Contact


class CreateContact(ModelForm):
    class Meta:
        model = Contact