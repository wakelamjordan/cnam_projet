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
        Initialise un nouvel utilisateur avec un email.

        Paramètres:
            email (str) : L'adresse email de l'utilisateur.
        """
        self._email = email

    def __repr__(self):
        """
        Retourne une représentation textuelle de l'objet User.

        Cette représentation masque le mot de passe et affiche uniquement les
        informations publiques de l'utilisateur.

        Retourne:
            str : Représentation en chaîne de l'utilisateur.
        """
        return f'<User(email={self.get_email()}, firstname={self.get_firstname()}, lastname={self.get_lastname()}, birth_at={self.get_birth_at()}, created_at={self.get_created_at()}, login_at={self.get_login_at()})>'

    def to_dict(self):
        """
        Convertit l'objet User en dictionnaire.

        Retourne:
            dict : Un dictionnaire contenant les informations de l'utilisateur.
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

    def get_email(self) -> str:
        """
        Retourne l'email de l'utilisateur.

        Retourne:
            str : L'adresse email de l'utilisateur.
        """
        return self._email

    def get_password(self) -> str:
        """
        Retourne le mot de passe de l'utilisateur.

        Retourne:
            str : Le mot de passe de l'utilisateur.
        """
        return self._password

    def set_password(self, password: str) -> None:
        """
        Modifie le mot de passe de l'utilisateur.

        Paramètres:
            password (str) : Le nouveau mot de passe.
        """
        self._password = password

    def get_firstname(self) -> Optional[str]:
        """
        Retourne le prénom de l'utilisateur.

        Retourne:
            Optional[str] : Le prénom de l'utilisateur, ou None s'il n'est pas défini.
        """
        return self._firstname

    def set_firstname(self, firstname: str) -> None:
        """
        Modifie le prénom de l'utilisateur.

        Paramètres:
            firstname (str) : Le nouveau prénom de l'utilisateur.
        """
        self._firstname = firstname

    def get_lastname(self) -> Optional[str]:
        """
        Retourne le nom de famille de l'utilisateur.

        Retourne:
            Optional[str] : Le nom de famille de l'utilisateur, ou None s'il n'est pas défini.
        """
        return self._lastname

    def set_lastname(self, lastname: str) -> None:
        """
        Modifie le nom de famille de l'utilisateur.

        Paramètres:
            lastname (str) : Le nouveau nom de famille de l'utilisateur.
        """
        self._lastname = lastname

    def get_birth_at(self) -> Optional[date]:
        """
        Retourne la date de naissance de l'utilisateur.

        Retourne:
            Optional[date] : La date de naissance de l'utilisateur, ou None si non définie.
        """
        return self._birth_at

    def set_birth_at(self, birth_at: date) -> None:
        """
        Modifie la date de naissance de l'utilisateur.

        Paramètres:
            birth_at (date) : La nouvelle date de naissance de l'utilisateur.
        """
        self._birth_at = birth_at

    def get_created_at(self) -> datetime:
        """
        Retourne la date de création du compte de l'utilisateur.

        Retourne:
            datetime : La date de création du compte.
        """
        return self._created_at

    def get_login_at(self) -> Optional[datetime]:
        """
        Retourne la dernière date de connexion de l'utilisateur.

        Retourne:
            Optional[datetime] : La dernière date de connexion, ou None si non définie.
        """
        return self._login_at
