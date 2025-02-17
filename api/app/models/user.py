# Importation des modules nécessaires pour la définition du modèle
from sqlalchemy import Column, Integer, String, text, Date, DateTime  # Pour définir les colonnes et types dans la table
from app.database import Base  # Import de la classe Base pour le mapping ORM
import datetime


# Définition du modèle User
class User(Base):
    """
    Classe représentant le modèle User dans la base de données.

    Hérite de Base, qui est utilisée par SQLAlchemy pour le mapping ORM.
    Cette classe est associée à la table "users".
    """

    # Nom de la table associée à ce modèle
    __tablename__ = 'user'

    # Définition des colonnes de la table
    # id = Column(Integer, primary_key=True)  # Colonne pour l'ID, clé primaire
    email = Column(String(50),
                   primary_key=True)  # Colonne pour l'email, doit être unique
    firstName = Column(String(50))  # Colonne pour le nom, doit être unique
    lastName = Column(String(50))
    firstName = Column(String(50))
    birthAt = Column(Date)
    createdAt = Column(DateTime)
    loginAt = Column(DateTime)

    def __init__(self,
                 email,
                 firstName=None,
                 lastName=None,
                 birthAt=None,
                 createdAt=datetime.datetime.now(),
                 loginAt=None):
        """
        Constructeur pour initialiser un objet User.

        Arguments :
        ----------
        name : str, facultatif
            Le nom de l'utilisateur.
        email : str, facultatif
            L'email de l'utilisateur.
        """
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.firstName = firstName
        self.birthAt = birthAt
        self.createdAt = createdAt
        self.loginAt = loginAt

    def __repr__(self):
        """
        Méthode spéciale pour représenter un objet User sous forme de chaîne.

        Retour :
        -------
        str : Une chaîne lisible représentant l'utilisateur.
        """
        return f" email='{self.email}', firstName='{self.firstName}', lastName='{self.lastName}', birthAt='{self.birthAt}', createdAt='{self.createdAt}',loginAt='{self.loginAt}')>"

    def to_dict(self):
        """
        Convertit un objet User en dictionnaire.

        Retour :
        -------
        dict : Un dictionnaire contenant les informations de l'utilisateur.
        """
        return {
            'email': self.email,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'birthAt': self.birthAt,
            'createdAt': self.createdAt,
            'loginAt': self.loginAt
        }

    def getBirthAt(self):
        return self.birthAt

    def setBirthAt(self, birthAt):
        self.birthAt = birthAt

    def getLoginAt(self):
        return self.loginAt

    # def to_list(result):
    #     """
    #     Convertit un objet User en liste.

    #     Retour :
    #     -------
    #     list : Une liste contenant les informations de l'utilisateur.
    #     """
    #     data = []
    #     for row in result:
    #         data.append({'id': row.id, 'name': row.name, 'email': row.email})
    #     return data
