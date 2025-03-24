class ResultEmpty(Exception):

    def __init__(self, message: str = "No found error!"):
        self.message = message
        super().__init__(self.message)


class EntryUnavailableError(Exception):

    def __init__(self,
                 message: str = "One or more provided entries already exist."):
        super().__init__(message)


class InvalidEntryError(Exception):

    def __init__(self, message: str = "Data is incomplete or invalid!"):
        super().__init__(message)
