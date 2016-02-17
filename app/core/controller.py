from flask import Blueprint, request, render_template

from app import db
from app.core.forms import CreateContact
from app.core.models import Contact

core = Blueprint('core', __name__, template_folder='templates/core')


@core.route('/contact/create', methods=['GET', 'POST'])
def create_contact():
    form = CreateContact(request.form)
    if request.method == 'POST':
        if form.validate():
            contact = Contact(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
            db.session.add(contact)
            db.session.commit()
    return render_template('core/contact.html', form=form, fields=form.data.keys())
