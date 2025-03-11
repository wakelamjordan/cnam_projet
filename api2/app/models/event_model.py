from . import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, INTEGER, DateTime
from datetime import datetime, timezone, date
# from app.models.publication_event_model import PublicationEvent

aware_datetime = datetime.now(timezone.utc)


class Event(Base):
    """
    Modèle représentant un événement.

    Attributes:
        _id (int): Identifiant unique de l'événement.
        _title (str): Titre de l'événement.
        _event_at (datetime): Date et heure de l'événement.
        _description (str): Description de l'événement.
    """
    __tablename__ = 'event'

    _id: Mapped[int] = mapped_column("id",
                                     INTEGER,
                                     autoincrement=True,
                                     primary_key=True)
    _title: Mapped[str] = mapped_column("title", String(100))
    _event_at: Mapped[datetime] = mapped_column("event_at",
                                                DateTime(timezone=True),
                                                default=aware_datetime)
    _description: Mapped[str] = mapped_column("description", String(200))

    publication: Mapped["PublicationEvent"] = relationship(
        "PublicationEvent",
        back_populates="event",
        cascade="all, delete-orphan")

    def __init__(self, title: str, event_at: datetime, description: str):
        """
        Initialise une instance d'Event.

        Args:
            title (str): Titre de l'événement.
            event_at (datetime): Date et heure de l'événement.
            description (str): Description de l'événement.
        """
        self._title = title
        self._event_at = event_at
        self._description = description

    def __repr__(self):
        return (f'<Event(title={self._title}, event_at={self._event_at})>')

    def to_dict(self) -> dict:
        """
        Convertit l'instance en dictionnaire.

        Returns:
            dict: Un dictionnaire contenant les attributs de l'événement.
        """
        return {
            "id": self._id,
            "title": self._title,
            "event_at": self._event_at.isoformat() if self._event_at else None,
            "description": self._description
        }

    def get_id(self) -> int:
        """
        Retourne l'identifiant de l'événement.

        Returns:
            int: L'identifiant unique de l'événement.
        """
        return self._id

    def get_title(self) -> str:
        """
        Retourne le titre de l'événement.

        Returns:
            str: Le titre de l'événement.
        """
        return self._title

    def set_title(self, title: str) -> None:
        """
        Modifie le titre de l'événement.

        Args:
            title (str): Le nouveau titre de l'événement.
        """
        self._title = title

    def get_event_at(self) -> datetime:
        """
        Retourne la date et l'heure de l'événement.

        Returns:
            datetime: La date et l'heure de l'événement.
        """
        return self._event_at

    def set_event_at(self, event_at: datetime) -> None:
        """
        Modifie la date et l'heure de l'événement.

        Args:
            event_at (datetime): La nouvelle date et heure de l'événement.
        """
        self._event_at = event_at

    def get_description(self) -> str:
        """
        Retourne la description de l'événement.

        Returns:
            str: La description de l'événement.
        """
        return self._description

    def set_description(self, description: str) -> None:
        """
        Modifie la description de l'événement.

        Args:
            description (str): La nouvelle description de l'événement.
        """
        self._description = description
