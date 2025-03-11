class PublicationTitleDoesExist(Exception):
    """
    Exception levée lorsque le titre de la publication existe déjà.

    Cette exception est levée lorsque l'application tente de créer une publication
    avec un titre qui existe déjà dans la base de données.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Your title already exists!"):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "Your title already exists!".
        """
        self.message = message
        super().__init__(self.message)


class PublicationSlugDoesExist(Exception):
    """
    Exception levée lorsque le slug de la publication existe déjà.

    Cette exception est levée lorsque l'application tente de créer une publication
    avec un slug qui existe déjà dans la base de données.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Your slug already exists!"):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "Your slug already exists!".
        """
        self.message = message
        super().__init__(self.message)


class PublicationDoesExist(Exception):
    """
    Exception levée lorsque la publication existe déjà.

    Cette exception est levée lorsque l'application tente de créer une publication
    qui existe déjà dans la base de données.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Your publication already exists!"):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "Your publication already exists!".
        """
        self.message = message
        super().__init__(self.message)


class PublicationCopyAlreadyExist(Exception):
    """
    Exception levée lorsque la copie de la publication existe déjà.

    Cette exception est levée lorsque l'application tente de créer une copie d'une publication
    qui existe déjà dans la base de données.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Your publication copy already exists!"):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "Your publication copy already exists!".
        """
        self.message = message
        super().__init__(self.message)


class DataNotValid(Exception):
    """
    Exception levée lorsque les données ne sont pas valides.

    Cette exception est levée lorsque l'application tente de traiter des données
    qui ne respectent pas les critères de validation.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Data not valid!"):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "Data not valid!".
        """
        self.message = message
        super().__init__(self.message)


class PublicationNotExist(Exception):
    """
    Exception levée lorsque la publication n'existe pas.

    Cette exception est levée lorsque l'application tente de récupérer une publication
    qui n'existe pas dans la base de données.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Publication does not exist!"):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "Publication does not exist!".
        """
        self.message = message
        super().__init__(self.message)


class PublicationIsOnLine(Exception):
    """
    Exception levée lorsque la publication est en ligne.

    Cette exception est levée lorsque l'application tente de supprimer une publication
    qui est actuellement en ligne.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(
        self,
        message="The publication cannot be deleted because it is currently online."
    ):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "The publication cannot be deleted because it is currently online.".
        """
        self.message = message
        super().__init__(self.message)


class PublicationNotCategory(Exception):
    """
    Exception levée lorsque la publication n'a pas de catégorie.

    Cette exception est levée lorsque l'application tente de mettre une publication en ligne
    qui n'a pas de catégorie associée.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(
        self,
        message="The publication cannot be online because it does not have a category."
    ):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "The publication cannot be online because it does not have a category.".
        """
        self.message = message
        super().__init__(self.message)


class PublicationDataNotValid(Exception):
    """
    Exception levée lorsque les données de la publication ne sont pas valides.

    Cette exception est levée lorsque l'application tente de traiter des données de publication
    qui ne respectent pas les critères de validation.

    Attributes:
        message (str): Le message d'erreur associé à l'exception.
    """

    def __init__(self, message="Publication data not valid!"):
        """
        Initialise l'exception avec un message personnalisé.

        Args:
            message (str): Le message d'erreur associé à l'exception. Par défaut "Publication data not valid!".
        """
        self.message = message
        super().__init__(self.message)
