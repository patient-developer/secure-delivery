import io
import unittest

from werkzeug.security import generate_password_hash

from app import create_app, db
from app.auth.models import Role, User
import config

USERNAME = 'luke.skywalker'
PASSWORD = 'may-the-force-be-with-you'


class FlaskTestClientCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config.TESTING)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_upload_non_pdf_file(self):
        user = User(username=USERNAME,
                    password_hash=generate_password_hash(PASSWORD),
                    role_id=1)

        db.session.add(user)
        db.session.commit()

        self.client.post('/auth/login', data={
            'username': USERNAME,
            'password': PASSWORD
        })

        response = self.client.post('/delivery/send-mail', data={
            'file': (io.BytesIO(b'Hello World!'), 'non-pdf-file.dat'),
            'email_recipient': 'hello@world'
        })

        with self.client.session_transaction() as session:
            self.assertTrue(('message', 'Invalid email address.') in session['_flashes'])
