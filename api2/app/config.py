import os


class Config:
    """Configuration de base"""
    SQLALCHEMY_DATABASE_URI = "sqlite:///exemple.db"
    TESTING = False


class Test_config(Config):
    """Configuration spécifique aux tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test/test.db"
