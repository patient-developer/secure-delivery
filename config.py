import os, ast

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEVELOPMENT = 'development'
TESTING = 'testing'
PRODUCTION = 'production'
DEFAULT = 'default'


class Config(object):
    # TODO Check for availability of environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = ast.literal_eval(os.environ.get('MAIL_USE_TLS').title())
    MAIL_USE_SSL = ast.literal_eval(os.environ.get('MAIL_USE_SSL').title())
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = [os.environ.get('MAIL_USERNAME')]

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


class TestingConfig(Config):
    WTF_CSRF_ENABLED = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


config = {
    DEVELOPMENT: DevelopmentConfig,
    TESTING: TestingConfig,
    PRODUCTION: ProductionConfig,

    DEFAULT: DevelopmentConfig
}
