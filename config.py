import os

class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'msu'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/msu'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

    S3_BUCKET = os.environ.get('S3_BUCKET')

class DevConfig(Config):
    db_user = 'postgres'
    db_pass = 'postgres'
    db_host = 'localhost'
    db_name = 'msu_dev'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
                                db_user, db_pass, db_host, db_name)

class TestConfig(Config):
    TESTING = True

    db_user = 'postgres'
    db_pass = 'postgres'
    db_host = 'localhost'
    db_name = 'msu_test'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
                                db_user, db_pass, db_host, db_name)

class ProdConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

configs = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
}
