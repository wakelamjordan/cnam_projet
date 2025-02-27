class RoleNotFoundError(Exception):
    """Exception levée lorsqu'aucun utilisateur n'est trouvé."""

    def __init__(self, message="User not found!"):
        self.message = message
        super().__init__(self.message)


class RoleDoesExist(Exception):
    """Exception levée lorsqu'aucun email existe déjà"""

    def __init__(self, message="Email does exist"):
        self.message = message
        super().__init__(self.message)


class RoleNotValide(Exception):
    """Exception levée quand un email n'es pas valide"""

    def __init__(self, message="Email not valid"):
        self.message = message
        super().__init__(self.message)
