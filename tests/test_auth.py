import unittest

from flask import url_for
from flask_login import current_user

from config import AuthTestConfig
from app.auth import User
from app import create_app
from app.database import db


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(AuthTestConfig)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        db.app = self.app
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_route(self):
        rv = self.client.get(url_for('auth.login'))
        self.assertEquals(rv.status_code, 200)

    def test_add_user_with_password_hashing(self):
        user = User.create(username='test@gmail.com', password='mysecret', first_name='chris', last_name='hall')
        self.assertEqual(user.username, 'test@gmail.com')
        self.assertNotEqual(user.password, 'mysecret', 'Password not hashed')
        self.assertTrue(user.is_correct_password('mysecret'))
        self.assertEqual(user.first_name, 'chris')
        self.assertEqual(user.last_name, 'hall')

    def test_valid_login_submit(self):
        with self.client:
            user = User.create(username='right@gmail.com', password='mysecret', first_name='chris', last_name='hall')
            form_data = {
                'username': 'right@gmail.com',
                'password': 'mysecret'
            }
            rv = self.client.post(url_for('auth.login'), data=form_data, follow_redirects=True)
            self.assertEquals(rv.status_code, 200)
            self.assertTrue(user.is_authenticated())
            self.assertEquals(current_user.id, user.id)
            rv = self.client.get('contact/create')
            self.assertEquals(rv.status_code, 200)

    def test_incorrect_password_display_message(self):
        User.create(username='wrong@gmail.com', password='mysecret', first_name='chris', last_name='hall')
        form_data = {
            'username': 'wrong@gmail.com',
            'password': 'wrongpassword'
        }
        rv = self.client.post(url_for('auth.login'), data=form_data, follow_redirects=True)
        self.assertEquals(rv.status_code, 200)
        self.assertTrue('Invalid password' in rv.data)

    # When we are not logged in trying access login_required pages should yield 401
    def test_login_required(self):
        rv = self.client.get('/')
        self.assertEquals(rv.status_code, 401)
        rv = self.client.get('/contact/create')
        self.assertEquals(rv.status_code, 401)
