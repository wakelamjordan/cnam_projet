from . import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey
from typing import Optional
from app.models.photo_model import Photo


class PublicationPhoto(Base):
    """
    Modèle représentant l'association entre une publication et une photo.

    Attributes:
        _publication (str): L'identifiant de la publication associée.
        _photo (str): Le chemin de la photo associée.
        photo (Photo): La photo liée à la publication, récupérée via la relation.
    """
    __tablename__ = 'publication_photo'

    # Clé étrangère pointant vers la publication
    _publication: Mapped[str] = mapped_column(String(100),
                                              ForeignKey("publication.title"),
                                              primary_key=True)

    # Clé étrangère pointant vers la photo
    _photo: Mapped[str] = mapped_column(String(50),
                                        ForeignKey("photo.path"),
                                        primary_key=True)

    # Relation avec la table Photo
    photo: Mapped[Optional["Photo"]] = relationship("Photo")

    def __init__(self, publication: str, photo: str):
        """
        Initialise une instance de PublicationPhoto.

        Args:
            publication (str): L'identifiant de la publication associée.
            photo (str): Le chemin de la photo associée à la publication.
        """
        self._publication = publication
        self._photo = photo

    def __repr__(self) -> str:
        """
        Représentation textuelle de l'instance PublicationPhoto.

        Returns:
            str: Représentation de l'association publication-photo.
        """
        return f'<PublicationPhoto(publication={self._publication}, photo={self._photo})>'

    def to_dict(self) -> dict:
        """
        Convertit l'instance en dictionnaire.

        Returns:
            dict: Un dictionnaire contenant les attributs de l'instance PublicationPhoto.
        """
        return {"publication": self._publication, "photo": self._photo}

    def get_publication(self) -> str:
        """
        Retourne l'identifiant de la publication associée.

        Returns:
            str: L'identifiant de la publication.
        """
        return self._publication

    def set_publication(self, publication: str) -> None:
        """
        Modifie l'identifiant de la publication associée.

        Args:
            publication (str): Le nouvel identifiant de la publication.
        """
        self._publication = publication

    def get_photo(self) -> str:
        """
        Retourne le chemin de la photo associée.

        Returns:
            str: Le chemin de la photo.
        """
        return self._photo

    def set_photo(self, photo: str) -> None:
        """
        Modifie le chemin de la photo associée.

        Args:
            photo (str): Le nouveau chemin de la photo.
        """
        self._photo = photo
