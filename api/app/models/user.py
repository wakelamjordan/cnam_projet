# Importation des modules nécessaires pour la définition du modèle
from sqlalchemy import Column, Integer, String, text  # Pour définir les colonnes et types dans la table
from app.database import Base # Import de la classe Base pour le mapping ORM


# Définition du modèle User
class User(Base):
    """
    Classe représentant le modèle User dans la base de données.

    Hérite de Base, qui est utilisée par SQLAlchemy pour le mapping ORM.
    Cette classe est associée à la table "users".
    """

    # Nom de la table associée à ce modèle
    __tablename__ = 'users'

    # Définition des colonnes de la table
    id = Column(Integer, primary_key=True)  # Colonne pour l'ID, clé primaire
    name = Column(String(50),
                  unique=True)  # Colonne pour le nom, doit être unique
    email = Column(String(120),
                   unique=True)  # Colonne pour l'email, doit être unique

    def __init__(self, name=None, email=None):
        """
        Constructeur pour initialiser un objet User.

        Arguments :
        ----------
        name : str, facultatif
            Le nom de l'utilisateur.
        email : str, facultatif
            L'email de l'utilisateur.
        """
        self.name = name
        self.email = email

    def __repr__(self):
        """
        Méthode spéciale pour représenter un objet User sous forme de chaîne.

        Retour :
        -------
        str : Une chaîne lisible représentant l'utilisateur.
        """
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

    def to_dict(self):
        """
        Convertit un objet User en dictionnaire.

        Retour :
        -------
        dict : Un dictionnaire contenant les informations de l'utilisateur.
        """
        return {'id': self.id, 'name': self.name, 'email': self.email}
    
    def to_list(result):
        """
        Convertit un objet User en liste.

        Retour :
        -------
        list : Une liste contenant les informations de l'utilisateur.
        """
        data=[]
        for row in result:
            data.append({'id': row.id, 'name': row.name, 'email': row.email})
        return data


