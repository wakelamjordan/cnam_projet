class UserNotFoundError(Exception):
    """
    Exception levée lorsqu'aucun utilisateur n'est trouvé.

    Cette exception est levée lorsque l'application tente de récupérer un utilisateur
    qui n'existe pas dans la base de données.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="User not found!"):
        self.message = message
        super().__init__(self.message)


class UserEmailDoesExist(Exception):
    """
    Exception levée lorsqu'un email existe déjà.

    Cette exception est levée lorsque l'application tente de créer un utilisateur
    avec un email qui est déjà enregistré dans la base de données.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Email does exist"):
        self.message = message
        super().__init__(self.message)


class UserEmailNotValide(Exception):
    """
    Exception levée lorsqu'un email n'est pas valide.

    Cette exception est levée lorsque l'application tente de valider un email
    qui ne respecte pas le format attendu.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Email not valid"):
        self.message = message
        super().__init__(self.message)


class UserPasswordNotValid(Exception):
    """
    Exception levée lorsqu'un mot de passe n'est pas valide.

    Cette exception est levée lorsque l'application tente de valider un mot de passe
    qui ne respecte pas les critères de sécurité définis.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Password not valid"):
        self.message = message
        super().__init__(self.message)


class UserDataIncomplete(Exception):
    """
    Exception levée lorsque les données utilisateur sont incomplètes.

    Cette exception est levée lorsque l'application tente de traiter des données utilisateur
    qui ne contiennent pas toutes les informations requises.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Data incomplete"):
        self.message = message
        super().__init__(self.message)
