import os


class BaseConfig(object):
    """Standard configuration options"""
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
    WTF_CSRF_ENABLED = False
    DATABASE_CONNECT_OPTIONS = {}
    THREADS_PER_PAGE = 2
    SECRET_KEY = "secret"
    BCRYPT_LOG_ROUNDS = 12


class TestConfig(BaseConfig):
    """Configuration for general testing"""
    TESTING = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True
    BCRYPT_LOG_ROUNDS = 4


class AuthTestConfig(TestConfig):
    """For testing authentication we want to require login to check validation works"""
    LOGIN_DISABLED = False
