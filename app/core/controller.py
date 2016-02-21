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
            print form.data
            contact = Contact.create(**form.data)
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
            org = Organisation.create(name=form.name.data, type=form.type.data, address=form.address.data)
            return redirect(url_for('core.view_organisation', id=org.id))
    return render_template('core/create_organisation.html', form=form)


@core.route('/organisation/<id>')
@login_required
def view_organisation(id):
    org = Organisation.query.filter_by(id=id).first()
    return render_template('core/view_organisation.html', organisation=org)