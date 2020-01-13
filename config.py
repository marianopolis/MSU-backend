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

    # For use in file handling. See msu/files.py.
    S3_BUCKET_IMAGES = os.environ.get('S3_BUCKET_IMAGES')
    S3_BUCKET_FILES = os.environ.get('S3_BUCKET_FILES')

    # Calendar to access from the calendar tab, and
    # service account that has read access to that calendar.
    # Calendar ID can be a gmail address.
    GOOGLE_CALENDAR_ID = os.environ.get('GOOGLE_CALENDAR_ID')
    GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')

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
