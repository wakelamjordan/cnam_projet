from . import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String
from typing import Optional, List
from app.models.category_model import Category
from app.models.user_model import User


class Role(Base):
    """
    Modèle représentant un rôle.

    Attributes:
        _name (str): Nom unique du rôle (clé primaire).
        users (Optional[List[User]]): Liste des utilisateurs associés à ce rôle.
        categories (Optional[List[Category]]): Liste des catégories associées à ce rôle.
    """

    __tablename__ = 'role'

    _name: Mapped[str] = mapped_column("name", String(50), primary_key=True)

    users: Mapped[Optional[List["User"]]] = relationship("User",
                                                         back_populates="role")

    categories: Mapped[Optional[List["Category"]]] = relationship(
        "Category", back_populates="role")

    def __init__(self, name: str):
        """
        Initialise un rôle.

        Args:
            name (str): Nom unique du rôle.
        """
        self._name = name

    def __repr__(self) -> str:
        """
        Représentation sous forme de chaîne de l'objet Role.

        Returns:
            str: Représentation textuelle du rôle.
        """
        return f'<Role(name={self.get_name()})>'

    def to_dict(self) -> dict:
        """
        Convertit l'objet Role en dictionnaire.

        Returns:
            dict: Dictionnaire contenant les informations du rôle.
        """
        return {"name": self._name}

    # Getters
    def get_name(self) -> str:
        """
        Retourne le nom du rôle.

        Returns:
            str: Nom du rôle.
        """
        return self._name

    def get_users(self) -> Optional[List["User"]]:
        """
        Retourne la liste des utilisateurs associés à ce rôle.

        Returns:
            Optional[List[User]]: Liste des utilisateurs ou None.
        """
        return self.users

    def get_categories(self) -> Optional[List["Category"]]:
        """
        Retourne la liste des catégories associées à ce rôle.

        Returns:
            Optional[List[Category]]: Liste des catégories ou None.
        """
        return self.categories

    # Setters
    def set_name(self, name: str) -> None:
        """
        Définit le nom du rôle.

        Args:
            name (str): Nouveau nom du rôle.
        """
        self._name = name
