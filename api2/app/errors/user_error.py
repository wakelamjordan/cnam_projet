class UserNotFoundError(Exception):
    """Exception levée lorsqu'aucun utilisateur n'est trouvé."""
    pass


class UserEmailDoesExist(Exception):
    """Exception levée lorsqu'aucun email existe déjà"""
    pass
