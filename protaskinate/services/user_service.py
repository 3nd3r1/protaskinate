"""protaskinate/services/user_service.py"""

from typing import List, Optional

from protaskinate.entities import User
from protaskinate.repositories import user_repository


class UserService:
    """Class representing a service for users"""
    def login(self, username: str, password: str) -> Optional[User]:
        """Login a user"""
        if user_repository.verify_password(username, password):
            return user_repository.get_by_username(username)
        return None

    def get_all(self) -> List[User]:
        """Get all users"""
        return user_repository.get_all()

user_service = UserService()
