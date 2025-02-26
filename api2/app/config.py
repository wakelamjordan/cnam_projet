from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    # app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


class Config:
    """Configuration de base"""
    SQLALCHEMY_DATABASE_URI = "sqlite:///exemple.db"
    TESTING = False
    JWT_SECRET_KEY = 'super-secret'


class Test_config(Config):
    """Configuration spécifique aux tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test/test.db"
