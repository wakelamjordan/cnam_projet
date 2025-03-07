from . import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String


class Photo(Base):
    __tablename__ = 'Photo'

    _path: Mapped[str] = mapped_column("path", String(50), primary_key=True)
    _name: Mapped[str] = mapped_column("name", String(50))
    _description: Mapped[str] = mapped_column("description", String(50))

    def __init__(self, path: str, name: str = "", description: str = ""):
        self._path = path
        self._name = name
        self._description = description

    def __repr__(self):
        return (f'<Photo(path={self.get_path()}, name={self.get_name()}, '
                f'description={self.get_description()})>')

    def to_dict(self) -> dict:
        return {
            "path": self.get_path(),
            "name": self.get_name(),
            "description": self.get_description()
        }

    # Getters and Setters for path
    def get_path(self) -> str:
        return self._path

    def set_path(self, path: str) -> None:
        self._path = path

    # Getters and Setters for name
    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    # Getters and Setters for description
    def get_description(self) -> str:
        return self._description

    def set_description(self, description: str) -> None:
        self._description = description
