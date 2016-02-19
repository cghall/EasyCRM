from flask import Blueprint, request, render_template, url_for, redirect

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
            return redirect(url_for('core.view_contact', id=contact.id))
    return render_template('core/create_contact.html', form=form, fields=form.data.keys())


@core.route('/contact/<id>')
def view_contact(id):
    form = CreateContact(request.form)
    contact = Contact.query.filter_by(id=id).first()
    return render_template('core/view_contact.html', record=contact, fields=form.data.keys())
