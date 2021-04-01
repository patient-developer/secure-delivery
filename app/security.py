import string
import secrets
import os

ALPHABET = string.ascii_letters + string.digits


def get_password():
    while True:
        password = ''.join(secrets.choice(ALPHABET) for i in range(int(os.getenv('PASSWORD_LENGTH'))))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= int(os.getenv('PASSWORD_DIGITS_COUNT'))):
            return password
