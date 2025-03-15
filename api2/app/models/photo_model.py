from . import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey
from typing import Optional
# from app.models.publication_photo_model import PublicationPhoto


class Photo(Base):
    __tablename__ = 'photo'

    # Chemin d'accès à la photo (clé primaire)
    _path: Mapped[str] = mapped_column("path", String(50), primary_key=True)

    # Nom de la photo
    _name: Mapped[str] = mapped_column("name", String(50), unique=True)

    # Description de la photo
    _description: Mapped[str] = mapped_column("description", String(50))

    publication_photos: Mapped[list["PublicationPhoto"]] = relationship(
        "PublicationPhoto",
        back_populates="photo",
        cascade="all, delete-orphan")

    # _no: Mapped[Optional[int]] = mapped_column("no", nullable=True)

    # Relation avec PublicationPhoto : suppression des références dans PublicationPhoto si Photo est supprimée
    # publication_photo: Mapped[Optional["PublicationPhoto"]] = relationship(
    #     "PublicationPhoto",
    #     back_populates="photo",
    #     cascade="all, delete-orphan")

    def __init__(self, name: str = "", description: str = ""):
        """
        Initialise une instance de Photo.

        Args:
            path (str): Chemin d'accès à la photo.
            name (str, optional): Nom de la photo. Défaut à une chaîne vide.
            description (str, optional): Description de la photo. Défaut à une chaîne vide.
        """
        self._name = name
        self._description = description

    def __repr__(self) -> str:
        """
        Représentation textuelle de l'instance Photo.

        Returns:
            str: Représentation de la photo avec son chemin, nom et description.
        """
        return (f'<Photo(path={self.get_path()}, name={self.get_name()}, '
                f'description={self.get_description()})>')

    def to_dict(self) -> dict:
        """
        Convertit l'instance en dictionnaire.

        Returns:
            dict: Un dictionnaire contenant les attributs de l'instance Photo.
        """
        return {
            "path": self.get_path(),
            "name": self.get_name(),
            "description": self.get_description()
        }

    # Getters et Setters

    def get_path(self) -> str:
        """
        Retourne le chemin d'accès de la photo.

        Returns:
            str: Le chemin d'accès de la photo.
        """
        return self._path

    def set_path(self, path: str) -> None:
        """
        Modifie le chemin d'accès de la photo.

        Args:
            path (str): Le nouveau chemin d'accès de la photo.
        """
        self._path = path

    def get_name(self) -> str:
        """
        Retourne le nom de la photo.

        Returns:
            str: Le nom de la photo.
        """
        return self._name

    def set_name(self, name: str) -> None:
        """
        Modifie le nom de la photo.

        Args:
            name (str): Le nouveau nom de la photo.
        """
        self._name = name

    def get_description(self) -> str:
        """
        Retourne la description de la photo.

        Returns:
            str: La description de la photo.
        """
        return self._description

    def set_description(self, description: str) -> None:
        """
        Modifie la description de la photo.

        Args:
            description (str): La nouvelle description de la photo.
        """
        self._description = description
