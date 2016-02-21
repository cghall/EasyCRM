from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.exc import IntegrityError

from app.database import db
from app.core import Base
from app.extensions import bcrypt


class User(Base):

    __tablename__ = 'user'

    username = db.Column(db.String(128), nullable=False)
    _password = db.Column(db.String(192), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    @staticmethod
    def create(**kwargs):
        u = User(**kwargs)
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def is_active(self):
        return self.active

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)
