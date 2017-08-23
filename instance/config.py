#from this_app import app
# Enable Flask's debugging features. Should be False in production
import os

PSQL = 'postgresql://postgres:admin@localhost/shopping_list'


class Config(object):
    WTF_CSRF_ENABLED = True
    CSRF_ENABLED = True
    SECRET_KEY = 'guess-it'
    TESTING = False
    DEBUG = False
    #SQLALCHEMY_DATABASE_URI = os.environ['postgresql://postgres:admin@localhost/shopping_list']
    SQLALCHEMY_DATABASE_URI = PSQL

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    #DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    #DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/shopping_list'
    DEBUG = True

app_config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'staging':StagingConfig,
    'production':ProductionConfig,
}