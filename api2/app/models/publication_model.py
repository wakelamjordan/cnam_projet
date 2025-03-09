from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey
from typing import Optional
from app.models.user_model import User


class Publication(Base):
    __tablename__ = "publication"

    _title: Mapped[str] = mapped_column('title', String(100), primary_key=True)
    _slug: Mapped[str] = mapped_column('slug', String(50), unique=True)
    _description: Mapped[str] = mapped_column('description', String(200))
    _content: Mapped[str] = mapped_column('content', String())
    _on_line: Mapped[bool] = mapped_column('on_line', Boolean(), default=False)
    _revision: Mapped[bool] = mapped_column('revision',
                                            Boolean(),
                                            default=False)
    _author_email: Mapped[str] = mapped_column('author_email', String(50),
                                               ForeignKey("user.email"))
    _category: Mapped[Optional[str]] = mapped_column('category', String(50))

    author: Mapped["User"] = relationship("User",
                                          back_populates="publications")

    def __init__(self,
                 title: str,
                 slug: str,
                 description: str,
                 content: str,
                 on_line: bool = False,
                 revision: bool = False,
                 author_email: str = None,
                 category: Optional[str] = None):
        self._title = title
        self._slug = slug
        self._description = description
        self._content = content
        self._on_line = on_line
        self._revision = revision
        self._author_email = author_email
        self._category = category

    def __repr__(self):
        """
        Retourne une représentation sous forme de chaîne de l'objet publication.
        """
        return f'<Publication(title={self.get_title()}, slug={self.get_slug()}, author={self.get_author_email()})>'

    def to_dict(self):
        """
        Convertit les informations de la publication en dictionnaire.

        Retourne:
            dict : Un dictionnaire contenant les informations de la publication.
        """
        return {
            "title": self.get_title(),
            "slug": self.get_slug(),
            "description": self.get_description(),
            "content": self.get_content(),
            "on_line": self.get_on_line(),
            "revision": self.get_revision(),
            "author_email": self.get_author_email(),
            "category": self.get_category()
        }

    # Getter and Setter for title
    def get_title(self) -> str:
        """
        Retourne le titre de la publication.

        Retourne:
            str : Le titre de la publication.
        """
        return self._title

    def set_title(self, title: str) -> None:
        """
        Définit le titre de la publication.

        Paramètres:
            title (str) : Le titre à définir.
        """
        self._title = title

    # Getter and Setter for slug
    def get_slug(self) -> str:
        """
        Retourne le slug de la publication.

        Retourne:
            str : Le slug de la publication.
        """
        return self._slug

    def set_slug(self, slug: str) -> None:
        """
        Définit le slug de la publication.

        Paramètres:
            slug (str) : Le slug à définir.
        """
        self._slug = slug

    # Getter and Setter for description
    def get_description(self) -> str:
        """
        Retourne la description de la publication.

        Retourne:
            str : La description de la publication.
        """
        return self._description

    def set_description(self, description: str) -> None:
        """
        Définit la description de la publication.

        Paramètres:
            description (str) : La description à définir.
        """
        self._description = description

    # Getter and Setter for content
    def get_content(self) -> str:
        """
        Retourne le contenu de la publication.

        Retourne:
            str : Le contenu de la publication.
        """
        return self._content

    def set_content(self, content: str) -> None:
        """
        Définit le contenu de la publication.

        Paramètres:
            content (str) : Le contenu à définir.
        """
        self._content = content

    # Getter and Setter for on_line
    def get_on_line(self) -> bool:
        """
        Retourne l'état en ligne de la publication.

        Retourne:
            bool : True si la publication est en ligne, sinon False.
        """
        return self._on_line

    def set_on_line(self, on_line: bool) -> None:
        """
        Définit l'état en ligne de la publication.

        Paramètres:
            on_line (bool) : L'état à définir.
        """
        self._on_line = on_line

    # Getter and Setter for revision
    def get_revision(self) -> bool:
        """
        Retourne l'état de révision de la publication.

        Retourne:
            bool : True si la publication est en révision, sinon False.
        """
        return self._revision

    def set_revision(self, revision: bool) -> None:
        """
        Définit l'état de révision de la publication.

        Paramètres:
            revision (bool) : L'état à définir.
        """
        self._revision = revision

    # Getter and Setter for author_email
    def get_author_email(self) -> str:
        """
        Retourne l'email de l'auteur de la publication.

        Retourne:
            str : L'email de l'auteur.
        """
        return self._author_email

    def set_author_email(self, author_email: str) -> None:
        """
        Définit l'email de l'auteur de la publication.

        Paramètres:
            author_email (str) : L'email à définir.
        """
        self._author_email = author_email

    # Getter and Setter for category
    def get_category(self) -> Optional[str]:
        """
        Retourne la catégorie de la publication.

        Retourne:
            Optional[str] : La catégorie de la publication ou None.
        """
        return self._category

    def set_category(self, category: Optional[str]) -> None:
        """
        Définit la catégorie de la publication.

        Paramètres:
            category (Optional[str]) : La catégorie à définir.
        """
        self._category = category
