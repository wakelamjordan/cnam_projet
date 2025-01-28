import os


class configDev:
    # DEBUG = True
    # TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cnam_projet.db'
    # SECRET_KEY = 'your-secret-key'


config = {
    'dev': configDev,
}
