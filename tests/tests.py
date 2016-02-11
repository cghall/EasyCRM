import unittest

from app import app, db
from config import TestConfig


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

if __name__ == '__main__':
    unittest.main()
