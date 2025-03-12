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

    def __init__(self, message="Category already exists"):
        super().__init__(message)


class CategoryNotValid(Exception):

    def __init__(self, message='Your category doesn\'t valid!'):
        self.message = message
        super().__init__(self.message)


class CategoryHavePublication(Exception):

    def __init__(
            self,
            message='This category can\'t be deleted he had Publication.'):
        self.message = message
        super().__init__(self.message)


class CategoryHaveSub(Exception):

    def __init__(
            self,
            message='This category can\'t be deleted he had sub-category.'):
        self.message = message
        super().__init__(self.message)
