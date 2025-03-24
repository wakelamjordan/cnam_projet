class CategoryNotExist(Exception):
    """
    Exception levée lorsque la catégorie n'existe pas.

    Cette exception est levée lorsque l'application tente de récupérer ou de manipuler une catégorie
    qui n'existe pas dans la base de données.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Category does not exist!"):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "Category does not exist!".
        """
        self.message = message
        super().__init__(self.message)


class CategoryAlreadyExist(Exception):
    """
    Exception levée lorsque la catégorie existe déjà.

    Cette exception est levée lorsque l'application tente d'insérer une catégorie
    qui existe déjà dans la base de données.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Category already exists"):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "Category already exists".
        """
        super().__init__(message)


class CategoryNotValid(Exception):
    """
    Exception levée lorsque la catégorie n'est pas valide.

    Cette exception est levée lorsque les données de la catégorie ne répondent pas aux critères de validation.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message='Your category doesn\'t valid!'):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "Your category doesn't valid!".
        """
        self.message = message
        super().__init__(self.message)


class CategoryHavePublication(Exception):
    """
    Exception levée lorsque la catégorie a des publications associées.

    Cette exception est levée lorsque l'application tente de supprimer une catégorie
    qui a des publications associées.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(
            self,
            message='This category can\'t be deleted he had Publication.'):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "This category can't be deleted he had Publication.".
        """
        self.message = message
        super().__init__(self.message)


class CategoryHaveSub(Exception):
    """
    Exception levée lorsque la catégorie a des sous-catégories.

    Cette exception est levée lorsque l'application tente de supprimer une catégorie
    qui a des sous-catégories associées.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(
            self,
            message='This category can\'t be deleted he had sub-category.'):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "This category can't be deleted he had sub-category.".
        """
        self.message = message
        super().__init__(self.message)
