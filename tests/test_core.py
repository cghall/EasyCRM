import unittest

from app import app, db
from config import TestConfig
from app.core import Contact


class CoreTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.from_object(TestConfig)
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def setUp(self):
        self.app = app.test_client()

    def test_create_contact_route(self):
        rv = self.app.get('/contact/create')
        self.assertEquals(rv.status_code, 200)

    def test_create_contact_empty_data(self):
        data = {}
        rv = self.app.post('/contact/create', data=data)
        self.assertEquals(rv.status_code, 200)

    def test_create_contact_valid_form(self):
        data = {
            'first_name': 'test',
            'last_name': 'contact',
            'email': 'example@test.co.uk'
        }
        rv = self.app.post('/contact/create', data=data)
        self.assertEquals(rv.status_code, 200)
        c = Contact.query.filter_by(email=data['email']).all()
        self.assertEqual(len(c), 1)
        self.assertEqual(c[0].first_name, data['first_name'])
        self.assertEqual(c[0].last_name, data['last_name'])
        self.assertEqual(c[0].email, data['email'])

if __name__ == '__main__':
    unittest.main()
