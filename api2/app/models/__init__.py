from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from flask import current_app  # Permet d'accéder à l'app actuelle dans le contexte


# Définition de la base de données
class Base(DeclarativeBase):
    pass


# Crée l'engine globalement (accessible par tous)
def get_engine():
    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'],
                           echo=True)
    return engine


# Fonction pour initialiser la base de données
def init_db():
    engine = get_engine()  # Utilisation de la fonction pour obtenir l'engine
    Session = sessionmaker(bind=engine)  # Crée la session
    from .user_model import User
    Base.metadata.create_all(engine)  # Crée toutes les tables


# Fonction pour obtenir la session
def get_db():
    engine = get_engine()  # Récupère l'engine depuis `get_engine()`
    Session = sessionmaker(bind=engine)  # Crée la session
    session = Session()  # Crée la session
    try:
        yield session  # Utilisation de la session dans le contexte
    finally:
        session.close()  # Ferme la session quand elle n'est plus utilisée
