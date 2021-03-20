import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAX_CONTENT_LENGTH = 1024 * 1024 * 5  # max 5 MB file
    UPLOAD_EXTENSIONS = ['.pdf']
