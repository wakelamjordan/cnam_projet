from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from typing import Optional
from datetime import datetime, timezone

aware_datetime = datetime.now(timezone.utc)


class Publication(Base):
    """
    Modèle représentant une publication.

    Attributes:
        _title (str): Le titre de la publication.
        _slug (str): Le slug unique de la publication.
        _description (str): La description de la publication.
        _content (str): Le contenu de la publication.
        _on_line (bool): Indique si la publication est en ligne.
        _created_at (datetime): La date de création de la publication.
        _updated_at (Optional[datetime]): La date de la dernière mise à jour de la publication.
        _revision (bool): Indique si la publication est en révision.
        _author_email (Optional[str]): L'email de l'auteur de la publication.
        _category (Optional[str]): La catégorie de la publication.
    """
    __tablename__ = "publication"

    _title: Mapped[str] = mapped_column('title', String(100), primary_key=True)
    _slug: Mapped[str] = mapped_column('slug', String(50), unique=True)
    _description: Mapped[str] = mapped_column('description', String(200))
    _content: Mapped[str] = mapped_column('content', String())
    _on_line: Mapped[bool] = mapped_column('on_line', Boolean(), default=False)
    _created_at: Mapped[datetime] = mapped_column("created_at",
                                                  DateTime(timezone=True),
                                                  default=aware_datetime)
    _updated_at: Mapped[Optional[datetime]] = mapped_column("updated_at")
    _revision: Mapped[bool] = mapped_column('revision',
                                            Boolean(),
                                            default=False)
    _author_email: Mapped[Optional[str]] = mapped_column(
        'author_email', String(50), ForeignKey("user.email"), nullable=True)
    _category: Mapped[Optional[str]] = mapped_column(
        'category', ForeignKey("category.name"))

    author_email: Mapped["User"] = relationship("User",
                                                back_populates="publications")
    home_page_contents: Mapped[list[
        Optional["HomePageContent"]]] = relationship(
            "HomePageContent", back_populates="publication")
    events: Mapped[list[Optional["PublicationEvent"]]] = relationship(
        "PublicationEvent", back_populates="publication")
    publication_photos: Mapped[list[
        Optional["PublicationPhoto"]]] = relationship(
            "PublicationPhoto",
            back_populates="publication",
            cascade="all, delete-orphan")
    category: Mapped[Optional["Category"]] = relationship(
        "Category", back_populates="publications")

    def __init__(self,
                 title: str,
                 slug: str,
                 description: str,
                 content: str,
                 on_line: bool = False,
                 revision: bool = False,
                 author_email: str = None,
                 category: Optional[str] = None):
        """
        Initialise une nouvelle instance de Publication.

        Args:
            title (str): Le titre de la publication.
            slug (str): Le slug de la publication.
            description (str): La description de la publication.
            content (str): Le contenu de la publication.
            on_line (bool, optional): Indique si la publication est en ligne. Par défaut False.
            revision (bool, optional): Indique si la publication est en révision. Par défaut False.
            author_email (str, optional): L'email de l'auteur de la publication. Par défaut None.
            category (Optional[str], optional): La catégorie de la publication. Par défaut None.
        """
        self._title = title
        self._slug = slug
        self._description = description
        self._content = content
        self._revision = revision
        if revision:
            on_line = False
        self._on_line = on_line
        self._author_email = author_email
        self._category = category

    def __repr__(self):
        """
        Retourne une représentation sous forme de chaîne de l'objet publication.

        Returns:
            str: Une représentation sous forme de chaîne de l'objet publication.
        """
        return f'<Publication(title={self.get_title()}, slug={self.get_slug()}, author={self.get_author_email()})>'

    def to_dict(self) -> dict:
        """
        Convertit les informations de la publication en dictionnaire.

        Returns:
            dict: Un dictionnaire contenant les informations de la publication.
        """
        return {
            "title": self.get_title(),
            "slug": self.get_slug(),
            "description": self.get_description(),
            "content": self.get_content(),
            "on_line": self.get_on_line(),
            "revision": self.get_revision(),
            "author_email": self.get_author_email(),
            "category": self.get_category(),
            "created_at": self.get_created_at(),
            "updated_at": self.get_updated_at()
        }

    def get_created_at(self) -> datetime:
        """
        Retourne la date de création de la publication.

        Returns:
            datetime: La date de création de la publication.
        """
        return self._created_at

    def get_updated_at(self) -> Optional[datetime]:
        """
        Retourne la date de la dernière mise à jour de la publication.

        Returns:
            Optional[datetime]: La date de la dernière mise à jour de la publication, ou None si non définie.
        """
        return self._updated_at

    def get_title(self) -> str:
        """
        Retourne le titre de la publication.

        Returns:
            str: Le titre de la publication.
        """
        return self._title

    def set_title(self, title: str) -> None:
        """
        Définit le titre de la publication.

        Args:
            title (str): Le titre à définir.
        """
        self._title = title

    def set_updated_at(self) -> None:
        """
        Met à jour la date de la dernière mise à jour de la publication avec la date et l'heure actuelles.
        """
        self._updated_at = aware_datetime

    def get_slug(self) -> str:
        """
        Retourne le slug de la publication.

        Returns:
            str: Le slug de la publication.
        """
        return self._slug

    def set_slug(self, slug: str) -> None:
        """
        Définit le slug de la publication.

        Args:
            slug (str): Le slug à définir.
        """
        self._slug = slug

    def get_description(self) -> str:
        """
        Retourne la description de la publication.

        Returns:
            str: La description de la publication.
        """
        return self._description

    def set_description(self, description: str) -> None:
        """
        Définit la description de la publication.

        Args:
            description (str): La description à définir.
        """
        self._description = description

    def get_content(self) -> str:
        """
        Retourne le contenu de la publication.

        Returns:
            str: Le contenu de la publication.
        """
        return self._content

    def set_content(self, content: str) -> None:
        """
        Définit le contenu de la publication.

        Args:
            content (str): Le contenu à définir.
        """
        self._content = content

    def get_on_line(self) -> bool:
        """
        Retourne l'état en ligne de la publication.

        Returns:
            bool: True si la publication est en ligne, sinon False.
        """
        return self._on_line

    def set_on_line(self, on_line: bool) -> None:
        """
        Définit l'état en ligne de la publication.

        Args:
            on_line (bool): L'état à définir.
        """
        self._on_line = on_line

    def get_revision(self) -> bool:
        """
        Retourne l'état de révision de la publication.

        Returns:
            bool: True si la publication est en révision, sinon False.
        """
        return self._revision

    def set_revision(self, revision: bool) -> None:
        """
        Définit l'état de révision de la publication.

        Args:
            revision (bool): L'état à définir.
        """
        self._revision = revision

    def get_author_email(self) -> Optional[str]:
        """
        Retourne l'email de l'auteur de la publication.

        Returns:
            Optional[str]: L'email de l'auteur, ou None si non défini.
        """
        return self._author_email

    def set_author_email(self, author_email: Optional[str]) -> None:
        """
        Définit l'email de l'auteur de la publication.

        Args:
            author_email (Optional[str]): L'email à définir.
        """
        self._author_email = author_email

    def get_category(self) -> Optional[str]:
        """
        Retourne la catégorie de la publication.

        Returns:
            Optional[str]: La catégorie de la publication, ou None si non définie.
        """
        return self._category

    def set_category(self, category: Optional[str]) -> None:
        """
        Définit la catégorie de la publication.

        Args:
            category (Optional[str]): La catégorie à définir.
        """
        self._category = category
