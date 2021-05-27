import unittest

import config
from app import create_app, db
from app.auth.models import Role


class FlaskTestClientCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config.TESTING)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
