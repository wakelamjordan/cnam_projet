from . import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey, INTEGER


class PublicationEvent(Base):
    """
    Modèle représentant l'association entre une publication et un événement.
    
    Attributes:
        _publication (str): Clé étrangère pointant vers une publication.
        _id (int): Clé étrangère pointant vers un événement.
    """

    __tablename__ = 'publication_event'

    _publication: Mapped[str] = mapped_column(String(100),
                                              ForeignKey("publication.title"),
                                              primary_key=True)
    _id: Mapped[int] = mapped_column("id",
                                     INTEGER,
                                     ForeignKey("event.id"),
                                     primary_key=True)

    def __init__(self, publication: str, event_id: int):
        """
        Initialise une instance de PublicationEvent.

        Args:
            publication (str): Le titre de la publication associée.
            event_id (int): L'ID de l'événement associé.
        """
        self._publication = publication
        self._id = event_id

    def __repr__(self):
        """
        Retourne une représentation textuelle de l'instance.

        Returns:
            str: Représentation de l'objet PublicationEvent.
        """
        return (
            f'<PublicationEvent(publication={self._publication}, id={self._id})>'
        )

    def to_dict(self) -> dict:
        """
        Convertit l'instance en dictionnaire.

        Returns:
            dict: Dictionnaire représentant l'instance.
        """
        return {"publication": self._publication, "id": self._id}

    def get_publication(self) -> str:
        """
        Récupère le titre de la publication.

        Returns:
            str: Le titre de la publication.
        """
        return self._publication

    def set_publication(self, publication: str) -> None:
        """
        Définit le titre de la publication.

        Args:
            publication (str): Le nouveau titre de la publication.
        """
        self._publication = publication

    def get_id(self) -> int:
        """
        Récupère l'ID de l'événement.

        Returns:
            int: L'ID de l'événement.
        """
        return self._id

    def set_id(self, event_id: int) -> None:
        """
        Définit l'ID de l'événement.

        Args:
            event_id (int): Le nouvel ID de l'événement.
        """
        self._id = event_id
