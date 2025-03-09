from datetime import datetime, timezone
from . import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey
from typing import Optional, List
# from app.models.role_model import Role


class Category(Base):
    """
    Représente une catégorie qui peut contenir des sous-catégories 
    (relation Many-to-One auto-référencée).
    Chaque catégorie peut être liée à un rôle.
    """

    __tablename__ = 'category'

    # Clé primaire : Nom unique de la catégorie
    _name: Mapped[str] = mapped_column("name", String(50), primary_key=True)

    # URL associée à la catégorie
    _url: Mapped[str] = mapped_column("url", String(50))

    # Numéro optionnel pour ordonner les catégories
    _no: Mapped[Optional[int]] = mapped_column("no")

    # Clé étrangère optionnelle : Référence au parent (catégorie parente)
    _parent: Mapped[Optional[str]] = mapped_column("parent",
                                                   String(50),
                                                   ForeignKey("category.name"),
                                                   nullable=True)

    # Clé étrangère optionnelle : Référence à un rôle
    _role: Mapped[Optional[str]] = mapped_column(ForeignKey("role.name"),
                                                 nullable=True)

    # Relation avec le rôle (Many-to-One)
    role: Mapped[Optional["Role"]] = relationship("Role",
                                                  back_populates="categories")

    # Relation avec la catégorie parente (Many-to-One)
    parent: Mapped[Optional["Category"]] = relationship(
        "Category", back_populates="children", remote_side="Category._name")

    # Relation avec les sous-catégories (One-to-Many) sans suppression automatique
    children: Mapped[List["Category"]] = relationship("Category",
                                                      back_populates="parent")

    def __init__(self,
                 name: str,
                 url: str,
                 no: Optional[int] = None,
                 parent: Optional[str] = None,
                 role: Optional[str] = None):
        """
        Initialise une nouvelle catégorie.

        :param name: Nom de la catégorie.
        :param url: URL associée à la catégorie.
        :param no: Numéro optionnel pour ordonner les catégories.
        :param parent: Nom de la catégorie parente (si applicable).
        :param role: Nom du rôle associé (si applicable).
        """
        self._name = name
        self._url = url
        self._no = no
        self._parent = parent
        self._role = role

    def __repr__(self) -> str:
        """
        Représentation textuelle de l'objet Category.

        :return: Chaîne représentant la catégorie.
        """
        return f'<Category(name={self._name}, parent={self._parent}, role={self._role})>'

    def to_dict(self) -> dict:
        """
        Convertit la catégorie en dictionnaire.

        :return: Dictionnaire contenant les données de la catégorie.
        """
        return {
            "name": self._name,
            "url": self._url,
            "no": self._no,
            "parent": self._parent,
            "role": self._role
        }

    # GETTERS

    def get_name(self) -> str:
        """Retourne le nom de la catégorie."""
        return self._name

    def get_url(self) -> str:
        """Retourne l'URL de la catégorie."""
        return self._url

    def get_no(self) -> Optional[int]:
        """Retourne le numéro de la catégorie (s'il existe)."""
        return self._no

    def get_parent(self) -> Optional[str]:
        """Retourne le nom de la catégorie parente (s'il y en a une)."""
        return self._parent

    def get_role(self) -> Optional[str]:
        """Retourne le rôle associé à la catégorie."""
        return self._role

    # SETTERS

    def set_name(self, name: str) -> None:
        """Définit le nom de la catégorie."""
        self._name = name

    def set_url(self, url: str) -> None:
        """Définit l'URL de la catégorie."""
        self._url = url

    def set_no(self, no: Optional[int]) -> None:
        """Définit le numéro de la catégorie."""
        self._no = no

    def set_parent(self, parent: Optional[str]) -> None:
        """Définit la catégorie parente."""
        self._parent = parent

    def set_role(self, role: Optional[str]) -> None:
        """Définit le rôle associé à la catégorie."""
        self._role = role
