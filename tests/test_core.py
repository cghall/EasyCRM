import unittest

from flask import url_for

from config import TestConfig
from app import create_app
from app.database import db
from app.auth import User
from app.core import Contact


class CoreTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        db.app = self.app
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page_route(self):
         with self.client:
            user = User(username='right@gmail.com', password='mysecret', first_name='chris', last_name='hall')
            db.session.add(user)
            db.session.commit()
            form_data = {
                'username': 'right@gmail.com',
                'password': 'mysecret'
            }
            self.client.post(url_for('auth.login'), data=form_data, follow_redirects=True)
            rv = self.client.get('/')
            self.assertEquals(rv.status_code, 200)

    def test_create_contact_route(self):
        rv = self.client.get('/contact/create')
        self.assertEquals(rv.status_code, 200)

    def test_create_contact_empty_data(self):
        data = {}
        rv = self.client.post('/contact/create', data=data)
        self.assertEquals(rv.status_code, 200)

    def test_create_contact_valid_form(self):
        data = {
            'first_name': 'test',
            'last_name': 'contact',
            'email': 'example@test.co.uk'
        }
        rv = self.client.post('/contact/create', data=data)
        self.assertEquals(rv.status_code, 302)
        c = Contact.query.filter_by(email=data['email']).all()
        self.assertEqual(len(c), 1)
        self.assertEqual(c[0].first_name, data['first_name'])
        self.assertEqual(c[0].last_name, data['last_name'])
        self.assertEqual(c[0].email, data['email'])

    def test_create_contact_email_validation(self):
        data = {
            'first_name': 'test',
            'last_name': 'contact',
            'email': 'notanemailaddress'
        }
        rv = self.client.post('/contact/create', data=data)
        self.assertEqual(rv.status_code, 200)
        c = Contact.query.filter_by(email=data['email']).all()
        self.assertEqual(len(c), 0)

    def test_view_contact_route(self):
        data = {
            'first_name': 'test',
            'last_name': 'contact',
            'email': 'example@test.co.uk'
        }
        self.client.post('/contact/create', data=data)
        c = Contact.query.filter_by(email=data['email']).first()
        rv = self.client.get('/contact/{}'.format(c.id))
        self.assertEquals(rv.status_code, 200)

if __name__ == '__main__':
    unittest.main()