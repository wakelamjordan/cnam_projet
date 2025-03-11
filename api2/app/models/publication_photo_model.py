from . import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey
from typing import Optional


class PublicationPhoto(Base):
    __tablename__ = 'publication_photo'

    _photo: Mapped[str] = mapped_column("photo",
                                        ForeignKey("photo.path"),
                                        primary_key=True)

    _no: Mapped[Optional[int]] = mapped_column("no", nullable=True)

    _publication: Mapped[str] = mapped_column("publication",
                                              String(100),
                                              ForeignKey("publication.title"),
                                              primary_key=True)
    photo: Mapped["Photo"] = relationship("Photo",
                                          back_populates="publication_photos")

    publication: Mapped["Publication"] = relationship(
        "Publication", back_populates="publication_photos")

    def __init__(self, photo: str, publication: str, no: Optional[int] = None):
        """
        Initialise une nouvelle instance de PublicationPhoto.

        Args:
            photo (str): Le chemin de la photo.
            publication (str): Le titre de la publication associée.
            no (Optional[int], optional): Le numéro de la photo. Par défaut None.
        """
        self._photo = photo
        self._publication = publication
        self._no = no

    def __repr__(self) -> str:
        """
        Retourne une représentation sous forme de chaîne de l'objet PublicationPhoto.

        Returns:
            str: Une représentation sous forme de chaîne de l'objet PublicationPhoto.
        """
        return (
            f'<PublicationPhoto(photo={self.get_photo()}, publication={self.get_publication()}, '
            f'no={self.get_no()})>')

    def to_dict(self) -> dict:
        """
        Convertit les informations de la photo de publication en dictionnaire.

        Returns:
            dict: Un dictionnaire contenant les informations de la photo de publication.
        """
        return {
            "photo": self.get_photo(),
            "publication": self.get_publication(),
            "no": self.get_no()
        }

    # Getters et Setters

    def get_photo(self) -> str:
        """
        Retourne le chemin de la photo.

        Returns:
            str: Le chemin de la photo.
        """
        return self._photo

    def set_photo(self, photo: str) -> None:
        """
        Définit le chemin de la photo.

        Args:
            photo (str): Le chemin de la photo à définir.
        """
        self._photo = photo

    def get_publication(self) -> str:
        """
        Retourne le titre de la publication associée.

        Returns:
            str: Le titre de la publication.
        """
        return self._publication

    def set_publication(self, publication: str) -> None:
        """
        Définit le titre de la publication associée.

        Args:
            publication (str): Le titre de la publication à définir.
        """
        self._publication = publication

    def get_no(self) -> Optional[int]:
        """
        Retourne le numéro de la photo.

        Returns:
            Optional[int]: Le numéro de la photo, ou None si non défini.
        """
        return self._no

    def set_no(self, no: Optional[int]) -> None:
        """
        Définit le numéro de la photo.

        Args:
            no (Optional[int]): Le numéro de la photo à définir.
        """
        self._no = no
