import re
from app.errors.user_error import UserEmailNotValide


class User_validator:
    _regex: re = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    def validate_email(self, word: str) -> None:
        if not re.fullmatch(self._regex, word):
            raise UserEmailNotValide
