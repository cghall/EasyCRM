from wtforms_alchemy import ModelForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.core.models import Contact, Organisation


def available_organisations():
    return Organisation.query.all()


class CreateOrganisation(ModelForm):
    class Meta:
        model = Organisation


class CreateContact(ModelForm):
    class Meta:
        model = Contact

    org_id = QuerySelectField('Organisation', query_factory=available_organisations, get_label='name')
