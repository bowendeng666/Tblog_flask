import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    #app basic config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super encrypted key' #SECRET_KEY is used to protect web forms against a nasty attack of CSRF
    POSTS_PER_PAGE = 10
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    #config database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1) if os.environ.get('DATABASE_URL') else  'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #config mail server
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    DEFAULT_MAIL_ADDR = os.environ.get('DEFAULT_MAIL_ADDR')
    ADMINS = ["bowendeng1997@163.com"]

    #config redis server
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'



