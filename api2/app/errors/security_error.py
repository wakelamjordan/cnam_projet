class LoginError(Exception):
    """
    Exception levée lorsque les informations de connexion sont invalides.

    Cette exception est levée lorsque l'application tente de se connecter avec un email
    ou un mot de passe incorrect.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(
        self,
        message="Invalid email or password. Please check your credentials and try again."
    ):
        self.message = message
        super().__init__(self.message)


class AccessDenied(Exception):
    """
    Exception levée lorsque l'accès à une ressource est refusé.

    Cette exception est levée lorsque l'utilisateur n'a pas les permissions nécessaires
    pour accéder à une ressource ou effectuer une action spécifique.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Access Denied"):
        self.message = message
        super().__init__(self.message)
