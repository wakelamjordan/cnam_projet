from datetime import datetime, timezone
from . import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime

aware_datetime = datetime.now(timezone.utc)


class Token(Base):
    """
    Represents a token entity in the database.

    Attributes:
        _token (str): The unique token string, serving as the primary key.
        _created_at (datetime): The timestamp when the token was created.
    """
    __tablename__ = 'token'

    _token: Mapped[str] = mapped_column("token", String(200), primary_key=True)
    _created_at: Mapped[datetime] = mapped_column("created_at",
                                                  DateTime(timezone=True),
                                                  default=aware_datetime)

    def __init__(self, token: str):
        """
        Initializes a Token instance.

        Args:
            token (str): The token string.
        """
        self._token = token

    def __repr__(self) -> str:
        """
        Returns a string representation of the Token instance.

        Returns:
            str: A string representation of the token and its creation timestamp.
        """
        return (
            f'<Token(token={self.get_token()}, created_at={self.get_created_at()})>'
        )

    def to_dict(self) -> dict:
        """
        Converts the Token instance to a dictionary.

        Returns:
            dict: A dictionary containing the token and its creation timestamp.
        """
        return {"token": self.get_token(), "created_at": self.get_created_at()}

    def get_token(self) -> str:
        """
        Retrieves the token string.

        Returns:
            str: The token string.
        """
        return self._token

    def set_token(self, token: str) -> None:
        """
        Sets a new token value.

        Args:
            token (str): The new token value.
        """
        self._token = token

    def get_created_at(self) -> datetime:
        """
        Retrieves the creation timestamp of the token.

        Returns:
            datetime: The timestamp when the token was created.
        """
        return self._created_at
