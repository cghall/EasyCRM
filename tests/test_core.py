import unittest

from sqlite3 import IntegrityError

from app import app, db
from config import TestConfig
from app.core import Contact, Organisation


class CoreTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_404(self):
        response = self.app.get('/nopagehere')
        assert response.status_code == 404
        assert 'EasyCRM: Page not found' in response.data

    def test_add_contact(self):
        dummy_first_name = 'test'
        dummy_last_name = 'contact'
        dummy_email = 'test@unittest.com'
        contact = Contact(first_name=dummy_first_name, last_name=dummy_last_name, email=dummy_email)
        db.session.add(contact)
        db.session.commit()
        queried_contact = Contact.query.filter_by(first_name='test').first()
        assert queried_contact.first_name == dummy_first_name
        assert queried_contact.last_name == dummy_last_name
        assert queried_contact.email == dummy_email
        # Check error raised if not nullable fields left blank
        incomplete_contact = Contact(first_name=dummy_first_name)
        self.assertRaises(IntegrityError, db.session.add(incomplete_contact))

    def test_add_org(self):
        dummy_org_name = 'big business'
        org = Organisation(org_name=dummy_org_name)
        db.session.add(org)
        db.session.commit()
        queried_org = Organisation.query.filter_by(org_name=dummy_org_name).first()
        assert queried_org.org_name == dummy_org_name

    def test_contact_org_relationship(self):
        dummy_first_name = 'test'
        dummy_last_name = 'contact'
        dummy_email = 'test@unittest.com'
        contact = Contact(first_name=dummy_first_name, last_name=dummy_last_name, email=dummy_email)
        dummy_org_name = 'big business'
        org = Organisation(org_name=dummy_org_name)
        contact.org_id = org.id
        db.session.add(contact)
        db.session.add(org)

if __name__ == '__main__':
    unittest.main()
