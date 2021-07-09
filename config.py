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
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 25
    MAIL_USE_TLS = 1
    MAIL_USERNAME = "1441721977"
    MAIL_PASSWORD = "xytewtosoqxtjdca"
    DEFAULT_MAIL_ADDR = 'developer.bowen@qq.com'
    ADMINS = ["bowendeng1997@163.com"]

    