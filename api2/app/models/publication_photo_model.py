from . import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey


class PublicationPhoto(Base):
    """
    Modèle représentant l'association entre une publication et une photo.

    Attributes:
        publication (str): L'identifiant de la publication.
        photo (str): Le chemin de la photo associée.
    """
    __tablename__ = 'publication_photo'

    _publication: Mapped[str] = mapped_column(String(100),
                                              ForeignKey("publication.title"),
                                              primary_key=True)
    _photo: Mapped[str] = mapped_column(String(50),
                                        ForeignKey("photo.path"),
                                        primary_key=True)

    def __init__(self, publication: str, photo: str):
        """
        Initialise une instance de PublicationPhoto.

        Args:
            publication (str): L'identifiant de la publication.
            photo (str): Le chemin de la photo associée.
        """
        self._publication = publication
        self._photo = photo

    def __repr__(self):
        return f'<PublicationPhoto(publication={self._publication}, photo={self._photo})>'

    def to_dict(self) -> dict:
        """
        Convertit l'instance en dictionnaire.

        Returns:
            dict: Un dictionnaire contenant les attributs de l'instance.
        """
        return {"publication": self._publication, "photo": self._photo}

    def get_publication(self) -> str:
        """
        Retourne l'identifiant de la publication.

        Returns:
            str: L'identifiant de la publication.
        """
        return self._publication

    def set_publication(self, publication: str) -> None:
        """
        Modifie l'identifiant de la publication.

        Args:
            publication (str): Le nouvel identifiant de la publication.
        """
        self._publication = publication

    def get_photo(self) -> str:
        """
        Retourne le chemin de la photo.

        Returns:
            str: Le chemin de la photo.
        """
        return self.photo

    def set_photo(self, photo: str) -> None:
        """
        Modifie le chemin de la photo.

        Args:
            photo (str): Le nouveau chemin de la photo.
        """
        self._photo = photo
