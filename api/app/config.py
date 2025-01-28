import os  # Permet d'interagir avec le système d'exploitation (variables d'environnement, chemins de fichiers)


# Configuration pour l'environnement de développement
class configDev:
    """
    Configuration pour l'environnement de développement.

    Attributs :
    ----------
    SQLALCHEMY_DATABASE_URI : str
        URL de connexion pour la base de données utilisée par SQLAlchemy.
        Ici, une base de données SQLite locale.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cnam_projet.db'


# Dictionnaire centralisant les configurations selon l'environnement
config = {
    'dev': configDev,  # Configuration pour l'environnement "dev"
}
