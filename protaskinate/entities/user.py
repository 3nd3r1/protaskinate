"""protaskinate/entities/user.py"""


class User:
    """Class representing a user"""

    def __init__(self, user_id: int, username: str):
        self.id = user_id
        self.username = username
