import re
from app.errors.user_error import UserEmailNotValide


class User_validator:
    """
    Classe utilitaire pour valider les informations des utilisateurs.

    Attributs:
        _regex (re.Pattern) : Expression régulière utilisée pour valider les adresses email.
    """

    _regex: re.Pattern = re.compile(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')

    def validate_email(self, word: str) -> None:
        """
        Valide une adresse email.

        Paramètres:
            word (str) : L'adresse email à valider.

        Lève:
            UserEmailNotValide : Si l'adresse email n'est pas valide.
        """
        if not re.fullmatch(self._regex, word):
            raise UserEmailNotValide()
