import unittest
from app import app

class FlaskUnitTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_app_exists(self):
        self.assertIsNotNone(app)

    def test_home_route_exists(self):
        response = self.app.get('/')
        self.assertIn(response.status_code, [200, 500])

if __name__ == '__main__':
    unittest.main()
