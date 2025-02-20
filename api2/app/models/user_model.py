from datetime import datetime, timezone, date
from . import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime
from typing import Optional

# Définir l'heure actuelle UTC pour l'initialisation des dates
aware_datetime = datetime.now(timezone.utc)


class User(Base):
    """
    Modèle SQLAlchemy représentant un utilisateur dans la base de données.

    Cette classe définit les champs de l'utilisateur ainsi que les méthodes pour 
    manipuler ces données, telles que l'accès et la modification des attributs.

    Attributs:
        _email (str) : L'email unique de l'utilisateur (clé primaire).
        _password (str) : Le mot de passe de l'utilisateur.
        _firstname (str, optional) : Le prénom de l'utilisateur.
        _lastname (str, optional) : Le nom de famille de l'utilisateur.
        _birth_at (date, optional) : La date de naissance de l'utilisateur.
        _created_at (datetime) : La date de création du compte de l'utilisateur.
        _login_at (datetime, optional) : La dernière date de connexion de l'utilisateur.
    """

    __tablename__ = 'user'

    # Définition des colonnes de la table
    _email: Mapped[str] = mapped_column("email", String(50), primary_key=True)
    _password: Mapped[str] = mapped_column("password", String(50))
    _firstname: Mapped[Optional[str]] = mapped_column("firstname")
    _lastname: Mapped[Optional[str]] = mapped_column("lastname")
    _birth_at: Mapped[Optional[date]] = mapped_column("birth_at")
    _created_at: Mapped[datetime] = mapped_column("created_at",
                                                  DateTime(timezone=True),
                                                  default=aware_datetime)
    _login_at: Mapped[Optional[datetime]] = mapped_column("login_at")

    def __init__(self, email: str):
        """
        Constructeur de la classe User.

        Paramètre:
            email (str) : L'email de l'utilisateur.

        Initialise les attributs de l'utilisateur avec l'email donné.
        """
        self._email = email

    def __repr__(self):
        """
        Représentation en chaîne de caractères de l'utilisateur.

        Retourne une chaîne masquant le mot de passe et montrant seulement les informations publiques
        comme l'email, le prénom, le nom, la date de naissance, la date de création et de connexion.

        Retourne:
            str : La représentation en chaîne de l'objet User.
        """
        return f'<("email"={self.get_email()}, "password"="*******", "firstname"={self.get_firstname()}, "lastname"={self.get_lastname()}, "birth_at"={self.get_birth_at()}, "created_at"={self.get_created_at()}, "login_at"={self.get_login_at()})>'

    def to_dict(self):
        """
        Convertit l'objet User en un dictionnaire.

        Retourne un dictionnaire représentant l'utilisateur, avec des clés comme 'email', 'firstname', 
        'lastname', etc., et leurs valeurs respectives.

        Retourne:
            dict : Le dictionnaire avec les informations de l'utilisateur.
        """
        return {
            "email": self.get_email(),
            "firstname": self.get_firstname(),
            "lastname": self.get_lastname(),
            "birth_at": self.get_birth_at(),
            "created_at": self.get_created_at(),
            "login_at": self.get_login_at()
        }

    # Méthodes d'accès aux attributs privés

    def get_email(self):
        """
        Retourne l'email de l'utilisateur.

        Retourne:
            str : L'email de l'utilisateur.
        """
        return self._email

    def get_password(self):
        """
        Retourne le mot de passe de l'utilisateur.

        Retourne:
            str : Le mot de passe de l'utilisateur.
        """
        return self._password

    def set_password(self, password: str):
        """
        Définit le mot de passe de l'utilisateur.

        Paramètre:
            password (str) : Le nouveau mot de passe à définir.

        Cette méthode permet de changer le mot de passe de l'utilisateur.
        """
        self._password = password
        return

    def get_firstname(self):
        """
        Retourne le prénom de l'utilisateur.

        Retourne:
            str : Le prénom de l'utilisateur, ou None si non défini.
        """
        return self._firstname

    def get_lastname(self):
        """
        Retourne le nom de l'utilisateur.

        Retourne:
            str : Le nom de l'utilisateur, ou None si non défini.
        """
        return self._lastname

    def get_birth_at(self):
        """
        Retourne la date de naissance de l'utilisateur.

        Retourne:
            date : La date de naissance de l'utilisateur, ou None si non défini.
        """
        return self._birth_at

    def get_created_at(self):
        """
        Retourne la date de création du compte de l'utilisateur.

        Retourne:
            datetime : La date de création du compte de l'utilisateur.
        """
        return self._created_at

    def get_login_at(self):
        """
        Retourne la dernière date de connexion de l'utilisateur.

        Retourne:
            datetime : La dernière date de connexion de l'utilisateur, ou None si non défini.
        """
        return self._login_at
