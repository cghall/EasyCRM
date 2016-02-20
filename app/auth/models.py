from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.core import Base
from app.extensions import bcrypt


class User(Base):

    __tablename__ = 'user'

    username = db.Column(db.String(128), nullable=False)
    _password = db.Column(db.String(192), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext, 8)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)
