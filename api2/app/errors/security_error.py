class LoginError(Exception):
    """
    Exception raised when login information is invalid.

    This exception is triggered when the application attempts to authenticate with
    an incorrect email or password.

    Attributes:
        message (str): The error message associated with the exception.
    """

    def __init__(
        self,
        message="Invalid email or password. Please check your credentials and try again."
    ):
        self.message = message
        super().__init__(self.message)


class AccessDenied(Exception):
    """
    Exception raised when access to a resource is denied.

    This exception is triggered when a user lacks the necessary permissions
    to access a resource or perform a specific action.

    Attributes:
        message (str): The error message associated with the exception.
    """

    def __init__(self, message="Access Denied"):
        self.message = message
        super().__init__(self.message)


class TokenAlreadyUsed(Exception):
    """
    Exception raised when a token has already been used.

    This exception is triggered when a token is attempted to be used more than once.

    Attributes:
        message (str): The error message associated with the exception.
    """

    def __init__(self, message="Token already used."):
        self.message = message
        super().__init__(self.message)
