from . import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey
from typing import Optional


class HomePageContent(Base):
    """
    Modèle représentant un élément du contenu de la page d'accueil.

    Chaque élément contient un nom, un identifiant unique, une description,
    et une référence à une publication associée. Cette classe représente
    un lien vers une publication existante.

    Attributes:
        _name (str): Nom de l'élément.
        _element (str): Identifiant unique de l'élément.
        _description (str): Description de l'élément.
        _publication (Optional[str]): Référence à une publication existante.
        publication (Optional[Publication]): Relation avec la publication associée.
    """

    __tablename__ = 'home_page_content'

    # Nom unique de l'élément (clé primaire)
    _name: Mapped[str] = mapped_column("name", String(20), primary_key=True)

    # Identifiant unique de l'élément (doit être unique)
    _element: Mapped[str] = mapped_column("element", String(20), unique=True)

    # Description de l'élément
    _description: Mapped[str] = mapped_column("description", String(200))

    # Clé étrangère : Référence à la publication associée (optionnelle)
    _publication: Mapped[Optional[str]] = mapped_column(
        "publication",
        String(100),
        ForeignKey("publication.title"),
        nullable=True)

    # Relation avec la publication associée
    publication: Mapped[Optional["Publication"]] = relationship(
        "Publication", back_populates="home_page_contents")

    def __init__(self,
                 name: str,
                 element: str,
                 description: str,
                 publication: Optional[str] = None):
        """
        Initialise une instance de HomePageContent.

        Args:
            name (str): Nom de l'élément.
            element (str): Identifiant unique de l'élément.
            description (str): Description de l'élément.
            publication (Optional[str]): Référence à une publication existante. (facultatif)
        """
        self._name = name
        self._element = element
        self._description = description
        self._publication = publication

    def __repr__(self) -> str:
        """
        Retourne une représentation sous forme de chaîne de l'objet HomePageContent.

        Returns:
            str: Une chaîne représentant l'élément du contenu de la page d'accueil.
        """
        return f'<HomePageContent(name={self._name}, element={self._element})>'

    def to_dict(self) -> dict:
        """
        Convertit l'instance en dictionnaire.

        Returns:
            dict: Un dictionnaire contenant les attributs de l'instance.
        """
        return {
            "name": self._name,
            "element": self._element,
            "description": self._description,
            "publication": self._publication
        }

    # GETTERS

    def get_name(self) -> str:
        """
        Retourne le nom de l'élément.

        Returns:
            str: Le nom de l'élément.
        """
        return self._name

    def get_element(self) -> str:
        """
        Retourne l'identifiant unique de l'élément.

        Returns:
            str: L'identifiant unique de l'élément.
        """
        return self._element

    def get_description(self) -> str:
        """
        Retourne la description de l'élément.

        Returns:
            str: La description de l'élément.
        """
        return self._description

    def get_publication(self) -> Optional[str]:
        """
        Retourne la référence à la publication associée.

        Returns:
            Optional[str]: La référence à la publication, ou None si aucune.
        """
        return self._publication

    # SETTERS

    def set_name(self, name: str) -> None:
        """
        Modifie le nom de l'élément.

        Args:
            name (str): Le nouveau nom de l'élément.
        """
        self._name = name

    def set_element(self, element: str) -> None:
        """
        Modifie l'identifiant unique de l'élément.

        Args:
            element (str): Le nouvel identifiant unique de l'élément.
        """
        self._element = element

    def set_description(self, description: str) -> None:
        """
        Modifie la description de l'élément.

        Args:
            description (str): La nouvelle description de l'élément.
        """
        self._description = description

    def set_publication(self, publication: Optional[str]) -> None:
        """
        Modifie la référence à la publication associée.

        Args:
            publication (Optional[str]): La nouvelle référence à la publication, ou None si aucune.
        """
        self._publication = publication
