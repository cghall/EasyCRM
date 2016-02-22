import unittest

from config import TestConfig
from app import create_app
from app.database import db
from app.core import Contact, Organisation


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
        org_data = {
            'name': 'test charity',
            'type': 'charity',
            'address': '1 My Road, London'
        }
        o = Organisation.create(**org_data)
        data = {
            'first_name': 'test',
            'last_name': 'contact',
            'email': 'example@test.co.uk',
            'org_id': o.id
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
        org_data = {
            'name': 'test charity',
            'type': 'charity',
            'address': '1 My Road, London'
        }
        o = Organisation.create(**org_data)
        con_data = {
            'first_name': 'test',
            'last_name': 'contact',
            'email': 'example@test.co.uk',
            'org_id': o.id
        }
        self.client.post('/contact/create', data=con_data)
        c = Contact.query.filter_by(email=con_data['email']).first()
        rv = self.client.get('/contact/{}'.format(c.id))
        self.assertEquals(rv.status_code, 200)

    def test_create_organisation_route(self):
        rv = self.client.get('/organisation/create')
        self.assertEquals(rv.status_code, 200)

    def test_create_organisation_valid_form(self):
        data = {
            'name': 'test charity',
            'type': 'charity',
            'address': '1 My Road, London'
        }
        rv = self.client.post('/organisation/create', data=data)
        self.assertEquals(rv.status_code, 302)
        o = Organisation.query.filter_by(name=data['name']).all()
        self.assertEqual(len(o), 1)
        self.assertEqual(o[0].name, data['name'])
        self.assertEqual(o[0].type, data['type'])
        self.assertEqual(o[0].address, data['address'])

    def test_contact_organisation_relationship(self):
        test_org_name = 'Test Organisation'
        test_org = Organisation.create(name=test_org_name, type='charity')
        test_contact = Contact.create(first_name='test', last_name='contact', email='example@test.co.uk',
                                      org_id=test_org.id)
        self.assertEquals(test_org.id, test_contact.org_id)
        self.assertEquals(len(test_org.contacts), 1)
        self.assertEquals(test_contact.organisation.name, test_org_name)


if __name__ == '__main__':
    unittest.main()