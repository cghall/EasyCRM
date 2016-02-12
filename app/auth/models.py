from app import db
from app.core import Base


class User(Base):

    __tablename__ = 'user'

    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(192), nullable=False)
