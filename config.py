import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = b'alsfjostgosrih34387sd'

    UPLOAD_FOLDER = os.path.join(basedir, 'data', 'uploads')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'data', 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False