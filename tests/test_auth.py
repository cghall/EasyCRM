import unittest

from app import app, db
from config import TestConfig
from app.auth import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_user(self):
        user = User(name='test', password='mysecret')
        db.session.add(user)
        db.session.commit()
        queried_user = User.query.filter_by(name='test').first()
        assert queried_user.name == 'test'
        assert queried_user.password == 'mysecret'
