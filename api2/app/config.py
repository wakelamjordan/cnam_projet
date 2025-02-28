from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


class Config:
    """
    Configuration de base pour l'application.

    Cette classe définit les paramètres de configuration par défaut pour l'application,
    y compris l'URI de la base de données, le mode de test et la clé secrète pour JWT.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): URI de la base de données SQLAlchemy.
        TESTING (bool): Indique si l'application est en mode test.
        JWT_SECRET_KEY (str): Clé secrète utilisée pour signer les tokens JWT.
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///exemple.db"
    TESTING = False
    JWT_SECRET_KEY = 'super-secret'


class Test_config(Config):
    """
    Configuration spécifique aux tests.

    Cette classe hérite de la classe `Config` et redéfinit certains paramètres
    pour les besoins des tests, notamment l'URI de la base de données et le mode de test.

    Attributes:
        TESTING (bool): Indique si l'application est en mode test.
        SQLALCHEMY_DATABASE_URI (str): URI de la base de données SQLAlchemy utilisée pour les tests.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test/test.db"
