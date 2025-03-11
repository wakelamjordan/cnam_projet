from datetime import datetime, timezone, date
from . import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, DateTime, ForeignKey
from typing import Optional
# from app.models.role_model import Role
from app.models.publication_model import Publication

aware_datetime = datetime.now(timezone.utc)


class User(Base):
    """
    Modèle représentant un utilisateur dans la base de données.

    Attributs:
        _email (str) : L'email de l'utilisateur, utilisé comme clé primaire.
        _password (str) : Le mot de passe de l'utilisateur.
        _firstname (Optional[str]) : Le prénom de l'utilisateur.
        _lastname (Optional[str]) : Le nom de famille de l'utilisateur.
        _birth_at (Optional[date]) : La date de naissance de l'utilisateur.
        _created_at (datetime) : La date et l'heure de création de l'utilisateur.
        _login_at (Optional[datetime]) : La date et l'heure de la dernière connexion de l'utilisateur.
        _role (Optional[str]) : Le rôle de l'utilisateur, lié à la table des rôles.

    Relations:
        role (Relationship) : Relation avec le modèle Role.
    """
    __tablename__ = 'user'

    _email: Mapped[str] = mapped_column("email", String(50), primary_key=True)
    _password: Mapped[str] = mapped_column("password", String(50))
    _firstname: Mapped[Optional[str]] = mapped_column("firstname")
    _lastname: Mapped[Optional[str]] = mapped_column("lastname")
    _birth_at: Mapped[Optional[date]] = mapped_column("birth_at")
    _created_at: Mapped[datetime] = mapped_column("created_at",
                                                  DateTime(timezone=True),
                                                  default=aware_datetime)
    _login_at: Mapped[Optional[datetime]] = mapped_column("login_at")

    _role: Mapped[Optional[str]] = mapped_column(ForeignKey("role.name"),
                                                 default='ROLE_USER')

    role: Mapped[Optional["Role"]] = relationship("Role",
                                                  back_populates="users")
    publications: Mapped[list["Publication"]] = relationship(
        "Publication", back_populates="author_email",
        cascade="save-update")  # Pas de suppression en cascade ici.

    # Rest of the methods...

    def __init__(self, email: str):
        """
        Initialise un nouvel utilisateur avec un email.

        Paramètres:
            email (str) : L'email de l'utilisateur.
        """
        self._email = email

    def __repr__(self):
        """
        Retourne une représentation sous forme de chaîne de l'objet utilisateur.

        Retourne:
            str : Représentation de l'utilisateur.
        """
        return (
            f'<User(email={self.get_email()},role={self.get_role()}, firstname={self.get_firstname()}, '
            f'lastname={self.get_lastname()}, birth_at={self.get_birth_at()}, '
            f'created_at={self.get_created_at()}, login_at={self.get_login_at()}, password={self.get_password()})>'
        )

    def to_dict(self):
        """
        Convertit les informations de l'utilisateur en dictionnaire.

        Retourne:
            dict : Un dictionnaire contenant les informations de l'utilisateur.
        """
        return {
            "email": self.get_email(),
            "role": self.get_role(),
            "firstname": self.get_firstname(),
            "lastname": self.get_lastname(),
            "birth_at": self.get_birth_at(),
            "created_at": self.get_created_at(),
            "login_at": self.get_login_at(),
            "password": self.get_password()
        }

    def to_dict_auth(self):
        """
        Convertit les informations d'authentification de l'utilisateur en dictionnaire.

        Retourne:
            dict : Un dictionnaire contenant les informations d'authentification de l'utilisateur.
        """
        return {
            "email": self.get_email(),
            "role": self.get_role(),
            "firstname": self.get_firstname(),
            "lastname": self.get_lastname(),
            "password": self.get_password()
        }

    def get_login_at(self) -> Optional[datetime]:
        """
        Retourne la date et l'heure de la dernière connexion de l'utilisateur.

        Retourne:
            Optional[datetime] : La date et l'heure de la dernière connexion.
        """
        return self._login_at

    def set_login_at(self) -> None:
        """
        Définit la date et l'heure de la dernière connexion de l'utilisateur à l'heure actuelle.
        """
        self._login_at = aware_datetime

    def get_role(self) -> Optional[str]:
        """
        Retourne le rôle de l'utilisateur.

        Retourne:
            Optional[str] : Le rôle de l'utilisateur.
        """
        return self._role

    def set_role(self, role: str) -> None:
        """
        Définit le rôle de l'utilisateur.

        Paramètres:
            role (str) : Le rôle à définir.
        """
        self._role = role

    def get_email(self) -> str:
        """
        Retourne l'email de l'utilisateur.

        Retourne:
            str : L'email de l'utilisateur.
        """
        return self._email

    def set_email(self, email: str) -> None:
        """
        Définit l'email de l'utilisateur.

        Paramètres:
            email (str) : L'email à définir.
        """
        self._email = email

    def get_password(self) -> str:
        """
        Retourne le mot de passe de l'utilisateur.

        Retourne:
            str : Le mot de passe de l'utilisateur.
        """
        return self._password

    def set_password(self, password: str) -> None:
        """
        Définit le mot de passe de l'utilisateur.

        Paramètres:
            password (str) : Le mot de passe à définir.
        """
        self._password = password

    def get_firstname(self) -> Optional[str]:
        """
        Retourne le prénom de l'utilisateur.

        Retourne:
            Optional[str] : Le prénom de l'utilisateur.
        """
        return self._firstname

    def set_firstname(self, firstname: str) -> None:
        """
        Définit le prénom de l'utilisateur.

        Paramètres:
            firstname (str) : Le prénom à définir.
        """
        self._firstname = firstname

    def get_lastname(self) -> Optional[str]:
        """
        Retourne le nom de famille de l'utilisateur.

        Retourne:
            Optional[str] : Le nom de famille de l'utilisateur.
        """
        return self._lastname

    def set_lastname(self, lastname: str) -> None:
        """
        Définit le nom de famille de l'utilisateur.

        Paramètres:
            lastname (str) : Le nom de famille à définir.
        """
        self._lastname = lastname

    def get_birth_at(self) -> Optional[date]:
        """
        Retourne la date de naissance de l'utilisateur.

        Retourne:
            Optional[date] : La date de naissance de l'utilisateur.
        """
        return self._birth_at

    def set_birth_at(self, birth_at: date) -> None:
        """
        Définit la date de naissance de l'utilisateur.

        Paramètres:
            birth_at (date) : La date de naissance à définir.
        """
        self._birth_at = birth_at

    def get_created_at(self) -> datetime:
        """
        Retourne la date et l'heure de création de l'utilisateur.

        Retourne:
            datetime : La date et l'heure de création de l'utilisateur.
        """
        return self._created_at
