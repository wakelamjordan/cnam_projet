from datetime import datetime, timezone, date
from . import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime
from typing import Optional

aware_datetime = datetime.now(timezone.utc)


class User(Base):
    __tablename__ = 'user'

    email: Mapped[str] = mapped_column(String(50), primary_key=True)
    password: Mapped[str] = mapped_column(String(50))
    firstname: Mapped[Optional[str]] = mapped_column()
    lastname: Mapped[Optional[str]] = mapped_column()
    birth_at: Mapped[Optional[date]]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=aware_datetime)
    login_at: Mapped[Optional[datetime]] = mapped_column()

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<("email"={self.email}, "password"={self.password}, "firstname"={self.firstname}, "lastname"={self.lastname} "birth_at"={self.birth_at}, "created_at"={self.created_at}, "login_at"={self.login_at})>'
