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

    def test_login(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sign In' in response.get_data(as_text=True))

    def test_unknown_user(self):
        # try to log in with unknown user
        response = self.client.post('/auth/login', data={
            'username': USERNAME,
            'password': PASSWORD
        })
        self.assertEqual(response.status_code, 302)
        with self.client.session_transaction() as session:
            self.assertTrue(('message', 'Invalid username or password.') in session['_flashes'])

    def test_known_user(self):
        user = User(username=USERNAME,
                    password_hash=generate_password_hash(PASSWORD),
                    role_id=1)

        db.session.add(user)
        db.session.commit()

        response = self.client.post('/auth/login', data={
            'username': USERNAME,
            'password': PASSWORD
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue('/index' in response.get_data(as_text=True))
        with self.client.session_transaction() as session:
            self.assertTrue(('message', 'Successfully signed in.') in session['_flashes'])

    def test_registration_no_login(self):
        # try to view register endpoint without being logged in
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/auth/login?next=%2Fauth%2Fregister' in response.get_data(as_text=True))
        with self.client.session_transaction() as session:
            self.assertTrue(('message', 'Please log in to access this page.') in session['_flashes'])
