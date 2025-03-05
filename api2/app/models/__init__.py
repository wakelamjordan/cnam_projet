from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from flask import current_app


# Définition de la classe de base pour SQLAlchemy
class Base(DeclarativeBase):
    """
    Classe de base pour tous les modèles SQLAlchemy.

    Cette classe sert de base pour tous les modèles SQLAlchemy dans le projet.  
    Elle permet à SQLAlchemy de savoir où il doit chercher les classes de modèles
    lorsqu'il tente de créer les tables en base de données.
    """
    pass


def get_engine():
    """
    Crée et retourne un moteur de base de données connecté à l'URI définie dans les configurations de Flask.

    Cette fonction utilise la configuration de l'application Flask pour créer un moteur
    SQLAlchemy. Le moteur est utilisé pour se connecter à la base de données spécifiée
    dans la configuration.

    Retourne:
        engine (Engine) : Une instance du moteur SQLAlchemy connectée à la base de données.
    """
    engine = create_engine(
        current_app.config['SQLALCHEMY_DATABASE_URI'], echo=True
    )  # echo=True active l'affichage des requêtes SQL pour le débogage
    return engine


def init_db():
    """
    Initialise la base de données en créant toutes les tables définies dans les modèles SQLAlchemy.

    Cette fonction crée les tables en appelant `Base.metadata.create_all()` sur l'engine SQLAlchemy.
    Elle s'assure que la structure de la base de données correspond aux modèles définis.

    Utilisation :
        Appeler cette fonction au démarrage de l'application pour créer la base de données.

    Exemple :
        init_db()
    """
    engine = get_engine()  # Récupère le moteur de la base de données
    from .user_model import User  # Importation du modèle User pour qu'il soit enregistré dans la base
    from .role_model import Role
    from .token_model import Token
    Base.metadata.create_all(
        engine)  # Crée toutes les tables des modèles SQLAlchemy


def get_db():
    engine = get_engine()  # Récupère l'engine de la base de données
    Session = sessionmaker(
        bind=engine)  # Crée la classe Session liée à l'engine
    session = Session()  # Crée une instance de session
    try:
        yield session  # Fournit la session pour une utilisation dans le gestionnaire de contexte
    finally:
        session.close()  # Ferme la session une fois l'opération terminée
