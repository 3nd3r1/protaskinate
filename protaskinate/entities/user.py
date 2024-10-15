"""protaskinate/entities/user.py"""

from dataclasses import dataclass

from flask_login import UserMixin


@dataclass
class User(UserMixin):
    """Class representing a user"""

    id: int
    username: str

    def __post_init__(self):
        if not isinstance(self.id, int):
            raise ValueError(f"Invalid id: {self.id}")

        if not isinstance(self.username, str):
            raise ValueError(f"Invalid username: {self.username}")
