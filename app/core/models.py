from sqlalchemy_utils import EmailType, ChoiceType
from sqlalchemy.exc import IntegrityError

from app.database import db


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Contact(Base):

    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(EmailType, nullable=False)
    mobile = db.Column(db.Integer)
    role = db.Column(db.String(60))

    org_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    activities = db.relationship('Activity', backref='contact')

    @staticmethod
    def create(**kwargs):
        c = Contact(**kwargs)
        db.session.add(c)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return c


class Organisation(Base):
    TYPE_CHOICE = [
        ('charity', 'Charity'),
        ('funder', 'Funder'),
        ('other', 'Other')
    ]

    name = db.Column(db.String(100), nullable=False)
    type = db.Column(ChoiceType(TYPE_CHOICE), nullable=False)
    address = db.Column(db.Text(180))

    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    contacts = db.relationship('Contact', backref='organisation')
    activities = db.relationship('Activity', backref='contact_lookup')

    @staticmethod
    def create(**kwargs):
        o = Organisation(**kwargs)
        db.session.add(o)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return o


class Project(Base):
    STATUS_CHOICE = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(ChoiceType(STATUS_CHOICE), nullable=False)

    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    org_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))

    activities = db.relationship('Activity', backref='project')
    invoices = db.relationship('Invoice', backref='project')


class Invoice(Base):

    issue_date = db.Column(db.Date)
    amount = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, default=False)

    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))


class Activity(Base):

    subject = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.Text)

    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    org_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
