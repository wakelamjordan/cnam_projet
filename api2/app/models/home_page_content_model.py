from . import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey


class HomePageContent(Base):
    """
    Modèle représentant un élément du contenu de la page d'accueil.

    Attributes:
        _name (str): Nom de l'élément.
        _element (str): Identifiant unique de l'élément.
        _description (str): Description de l'élément.
        _publication (str): Référence à une publication existante.
    """
    __tablename__ = 'home_page_content'

    _name: Mapped[str] = mapped_column("name", String(20), primary_key=True)
    _element: Mapped[str] = mapped_column("element", String(20), unique=True)
    _description: Mapped[str] = mapped_column("description", String(200))
    _publication: Mapped[str] = mapped_column("publication", String(200),
                                              ForeignKey("publication.title"))

    def __init__(self, name: str, element: str, description: str,
                 publication: str):
        """
        Initialise une instance de HomePageContent.

        Args:
            name (str): Nom de l'élément.
            element (str): Identifiant unique de l'élément.
            description (str): Description de l'élément.
            publication (str): Référence à une publication existante.
        """
        self._name = name
        self._element = element
        self._description = description
        self._publication = publication

    def __repr__(self):
        return (
            f'<HomePageContent(name={self._name}, element={self._element})>')

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

    def get_name(self) -> str:
        """
        Retourne le nom de l'élément.

        Returns:
            str: Le nom de l'élément.
        """
        return self._name

    def set_name(self, name: str) -> None:
        """
        Modifie le nom de l'élément.

        Args:
            name (str): Le nouveau nom de l'élément.
        """
        self._name = name

    def get_element(self) -> str:
        """
        Retourne l'identifiant unique de l'élément.

        Returns:
            str: L'identifiant unique de l'élément.
        """
        return self._element

    def set_element(self, element: str) -> None:
        """
        Modifie l'identifiant unique de l'élément.

        Args:
            element (str): Le nouvel identifiant de l'élément.
        """
        self._element = element

    def get_description(self) -> str:
        """
        Retourne la description de l'élément.

        Returns:
            str: La description de l'élément.
        """
        return self._description

    def set_description(self, description: str) -> None:
        """
        Modifie la description de l'élément.

        Args:
            description (str): La nouvelle description de l'élément.
        """
        self._description = description

    def get_publication(self) -> str:
        """
        Retourne la référence à la publication associée.

        Returns:
            str: La référence à la publication.
        """
        return self._publication

    def set_publication(self, publication: str) -> None:
        """
        Modifie la référence à la publication associée.

        Args:
            publication (str): La nouvelle référence à la publication.
        """
        self._publication = publication
