import re
from app.errors.user_error import UserEmailNotValide, UserPasswordNotValid


class User_validator:
    """
    Classe utilitaire pour valider les informations des utilisateurs.

    Cette classe fournit des méthodes statiques pour valider les adresses email
    et les mots de passe des utilisateurs selon des critères spécifiques.
    """

    @staticmethod
    def validate_email(word: str) -> None:
        """
        Valide une adresse email.

        Paramètres:
            word (str) : L'adresse email à valider.

        Lève:
            UserEmailNotValide : Si l'adresse email n'est pas valide.
        """
        _regex: re.Pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
        if not re.fullmatch(_regex, word):
            raise UserEmailNotValide()

    @staticmethod
    def validate_psw(psw: str) -> None:
        """
        Valide un mot de passe.

        Paramètres:
            psw (str) : Le mot de passe à valider.

        Lève:
            UserPasswordNotValid : Si le mot de passe n'est pas valide.

        Le mot de passe doit contenir au moins :
        - 12 caractères
        - Une lettre majuscule
        - Une lettre minuscule
        - Un chiffre
        - Un caractère spécial
        """
        _regex_psw: re.Pattern = re.compile(
            r"^(?=.*\d)(?=.*[a-zA-Z])(?=.*[!\"#$%&'()*+,-.\/:;<=>?@[\]^_{}|~`]).{12,}$"
        )
        if not re.fullmatch(_regex_psw, psw):
            raise UserPasswordNotValid()
