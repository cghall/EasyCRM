from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.auth import User

def populate_db():
    """
    Adds fake data to the database.
    """
    admin = User(username='test@gmail.com', password='kkwi5140', first_name='chris', last_name='hall')
    db.session.add(admin)
    db.session.commit()