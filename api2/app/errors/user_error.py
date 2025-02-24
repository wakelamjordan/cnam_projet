class UserNotFoundError(Exception):
    """Exception levée lorsqu'aucun utilisateur n'est trouvé."""


class UserEmailDoesExist(Exception):
    """Exception levée lorsqu'aucun email existe déjà"""


class UserEmailNotValide(Exception):
    """Exception levée quand un email n'es pas valide"""

    def __init__(self, message="Email not valid"):
        self.message = message
        super().__init__(self.message)
