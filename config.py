from this_app import app
# Enable Flask's debugging features. Should be False in production
import os
app.DEBUG = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'guess-it'
TESTING = False
Debug = False

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postre:admin@localhost/shopping_list'