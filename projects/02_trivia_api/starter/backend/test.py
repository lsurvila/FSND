import unittest

from app import create_app
from db import db


class TriviaTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config_test')
        self.client = self.app.test_client
        with self.app.app_context():
            self.db = db
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.session.close()
            self.db.drop_all()

    def test_a(self):
        self.assertEqual(2, 4)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
