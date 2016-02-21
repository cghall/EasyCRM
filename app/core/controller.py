from flask import request, render_template, url_for, redirect
from flask_login import login_required

from app.core.forms import CreateContact, CreateOrganisation
from app.core.models import Contact, Organisation
from . import core


@core.route('/')
@login_required
def home():
    return render_template('core/home.html')


@core.route('/contact/create', methods=['GET', 'POST'])
@login_required
def create_contact():
    form = CreateContact(request.form)
    if request.method == 'POST':
        if form.validate():
            contact = Contact.create(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
            return redirect(url_for('core.view_contact', id=contact.id))
    return render_template('core/create_contact.html', form=form, fields=form.data.keys())


@core.route('/contact/<id>')
@login_required
def view_contact(id):
    contact = Contact.query.filter_by(id=id).first()
    columns = [el.name for el in Contact.__table__.columns]
    return render_template('core/view_contact.html', columns=columns, record=contact)


@core.route('/organisation/create', methods=['GET', 'POST'])
@login_required
def create_organisation():
    form = CreateOrganisation(request.form)
    if request.method == 'POST':
        if form.validate():
            org = Organisation.create(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
            return redirect(url_for('core.view_contact', id=org.id))
    return render_template('core/create_contact.html', form=form, fields=form.data.keys())