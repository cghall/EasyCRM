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
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))


class Organisation(Base):

    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(80))
    address = db.Column(db.Text(180))

    contacts = db.relationship('Contact', backref='organisation')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

