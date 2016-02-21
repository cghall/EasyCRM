from sqlalchemy_utils import EmailType

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

    def __init__(self, first_name=None, last_name=None, email=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


class Organisation(Base):

    org_name = db.Column(db.String(100), nullable=False)
    contacts = db.relationship('Contact', backref='organisation')

    def __init__(self, org_name=None):
        self.org_name = org_name