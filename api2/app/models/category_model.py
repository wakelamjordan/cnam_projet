from datetime import datetime, timezone
from . import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, Integer
from typing import Optional, List
# from app.models.role_model import Role


class Category(Base):
    """
    Représente une catégorie qui peut contenir des sous-catégories
    (relation Many-to-One auto-référencée).
    Chaque catégorie peut être liée à un rôle.

    Attributes:
        _name (str): Nom unique de la catégorie.
        _url (Optional[str]): URL associée à la catégorie.
        _no (Optional[int]): Numéro optionnel pour ordonner les catégories.
        _parent (Optional[str]): Référence à la catégorie parente.
        _role (Optional[str]): Référence à un rôle associé.
        role (Optional[Role]): Relation avec le rôle associé.
        parent (Optional[Category]): Relation avec la catégorie parente.
        children (List[Category]): Relation avec les sous-catégories.
        publications (List[Publication]): Relation avec les publications associées.
    """

    __tablename__ = 'category'

    # Clé primaire : Nom unique de la catégorie
    _name: Mapped[str] = mapped_column("name", String(50), primary_key=True)

    # URL associée à la catégorie
    _url: Mapped[Optional[str]] = mapped_column("url",
                                                String(50),
                                                nullable=True)

    # Numéro optionnel pour ordonner les catégories
    _no: Mapped[Optional[int]] = mapped_column("no")

    # Clé étrangère optionnelle : Référence au parent (catégorie parente)
    _parent: Mapped[Optional[str]] = mapped_column("parent",
                                                   String(50),
                                                   ForeignKey("category.name"),
                                                   nullable=True)

    # Clé étrangère optionnelle : Référence à un rôle
    _role: Mapped[Optional[str]] = mapped_column('role',
                                                 ForeignKey("role.name"),
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

    publications: Mapped[List["Publication"]] = relationship(
        "Publication", back_populates="category", cascade="save-update")

    def __init__(self, name: str):
        """
        Initialise une nouvelle catégorie.

        Args:
            name (str): Nom de la catégorie.
        """
        self._name = name

    def __repr__(self) -> str:
        """
        Retourne une représentation sous forme de chaîne de l'objet Category.

        Returns:
            str: Chaîne représentant la catégorie.
        """
        return f'<Category(name={self._name}, parent={self._parent}, role={self._role})>'

    def to_dict(self) -> dict:
        """
        Convertit la catégorie en dictionnaire.

        Returns:
            dict: Dictionnaire contenant les données de la catégorie.
        """
        return {
            "name": self._name,
            "url": self._url,
            "no": self._no,
            "parent": self._parent,
            "role": self._role
        }

    def get_publications(self) -> List["Publication"]:
        """
        Retourne les publications associées à la catégorie.

        Returns:
            List[Publication]: Liste des publications associées.
        """
        return self.publications

    # GETTERS

    def get_name(self) -> str:
        """
        Retourne le nom de la catégorie.

        Returns:
            str: Le nom de la catégorie.
        """
        return self._name

    def get_url(self) -> Optional[str]:
        """
        Retourne l'URL de la catégorie.

        Returns:
            Optional[str]: L'URL de la catégorie, ou None si non définie.
        """
        return self._url

    def get_no(self) -> Optional[int]:
        """
        Retourne le numéro de la catégorie (s'il existe).

        Returns:
            Optional[int]: Le numéro de la catégorie, ou None si non défini.
        """
        return self._no

    def get_parent(self) -> Optional[str]:
        """
        Retourne le nom de la catégorie parente (s'il y en a une).

        Returns:
            Optional[str]: Le nom de la catégorie parente, ou None si non définie.
        """
        return self._parent

    def get_role(self) -> Optional[str]:
        """
        Retourne le rôle associé à la catégorie.

        Returns:
            Optional[str]: Le rôle associé à la catégorie, ou None si non défini.
        """
        return self._role

    # SETTERS

    def set_name(self, name: str) -> None:
        """
        Définit le nom de la catégorie.

        Args:
            name (str): Le nouveau nom de la catégorie.
        """
        self._name = name

    def set_url(self, url: str) -> None:
        """
        Définit l'URL de la catégorie.

        Args:
            url (str): La nouvelle URL de la catégorie.
        """
        self._url = url

    def set_no(self, no: Optional[int]) -> None:
        """
        Définit le numéro de la catégorie.

        Args:
            no (Optional[int]): Le nouveau numéro de la catégorie.
        """
        if no is not None and not isinstance(no, int):
            raise ValueError("No Field should be integer.")
        self._no = no

    def set_parent(self, parent: Optional[str]) -> None:
        """
        Définit la catégorie parente.

        Args:
            parent (Optional[str]): Le nom de la nouvelle catégorie parente.
        """
        self._parent = parent

    def set_role(self, role: Optional[str]) -> None:
        """
        Définit le rôle associé à la catégorie.

        Args:
            role (Optional[str]): Le nouveau rôle associé à la catégorie.
        """
        self._role = role
