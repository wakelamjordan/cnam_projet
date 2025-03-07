from . import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String


class PublicationPhoto(Base):
    __tablename__ = 'publication_photo'

    _name: Mapped[str] = mapped_column("name", String(50), primary_key=True)

    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return (f'<PublicationPhoto(name={self.get_name()})>')

    def to_dict(self) -> dict:
        return {"name": self._name}

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name
