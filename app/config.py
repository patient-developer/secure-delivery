import os


class Config(object):
    # TODO Check for availability of environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY')
