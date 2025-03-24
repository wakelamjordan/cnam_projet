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
    password = Column(String(50), nullable=False)
    firstname = Column(
        String(50), nullable=False,
        default="non renseigné")  # Colonne pour le nom, doit être unique
    lastname = Column(String(50), nullable=False, default="non renseigné")
    birthat = Column(Date)
    createdat = Column(DateTime)
    loginat = Column(DateTime)

    def __init__(self,
                 email,
                 firstname=None,
                 lastname=None,
                 birthat=None,
                 createdat=datetime.datetime.now(),
                 loginat=None,
                 password=None):
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
        self.firstname = firstname
        self.lastname = lastname
        self.birthat = birthat
        self.createdat = createdat
        self.loginat = loginat
        self.password = password

    def __repr__(self):
        """
        Méthode spéciale pour représenter un objet User sous forme de chaîne.

        Retour :
        -------
        str : Une chaîne lisible représentant l'utilisateur.
        """
        return f"<(email='{self.email}',password='{self.password}', firstName='{self.firstname}', lastName='{self.lastname}', birthAt='{self.birthat}', createdAt='{self.createdat}',loginAt='{self.loginat}')>"

    def to_dict(self):
        """
        Convertit un objet User en dictionnaire.

        Retour :
        -------
        dict : Un dictionnaire contenant les informations de l'utilisateur.
        """
        return {
            'email': self.email,
            'password': self.password,
            'firstName': self.firstname,
            'lastName': self.lastname,
            'birthAt': self.birthat,
            'createdAt': self.createdat,
            'loginAt': self.loginat
        }

    def getEmail(self):
        return self.email

    def getPassword(self):
        return self.password

    def getFirstName(self):
        return self.firstname

    def getLastName(self):
        return self.lastname

    def getBirthAt(self):
        return self.birthat

    def getCreatedAt(self):
        return self.createdat

    def getLoginAt(self):
        return self.loginat

    def setPassword(self, password):
        self.password = password

    def setFirstName(self, firstname):
        self.firstname = firstname

    def setLastName(self, lastname):
        self.lastname = lastname

    def setBirthAt(self, birthat):
        self.birthat = birthat

    def setCreatedAt(self, createdat):
        self.createdat = createdat

    def setLoginAt(self, loginat):
        self.loginat = loginat

    # def getLoginAt(self):
    #     return self.loginAt

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
