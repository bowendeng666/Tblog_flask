import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #app basic config
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess" #SECRET_KEY is used to protect web forms against a nasty attack of CSRF
    POSTS_PER_PAGE = 10

    #config database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or  'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #config mail server
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    