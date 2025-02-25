class LoginError(Exception):

    def __init__(
        self,
        message="Invalid email or password. Please check your credentials and try again."
    ):
        self.message = message
        super().__init__(self.message)
