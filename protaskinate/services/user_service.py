"""protaskinate/services/user_service.py"""

from typing import List, Optional

from werkzeug.security import generate_password_hash

from protaskinate.entities import User
from protaskinate.repositories import user_repository


class UserService:
    """Class representing a service for users"""
    def login(self, username: str, password: str) -> Optional[User]:
        """Login a user"""
        if user_repository.verify_password(username, password):
            return user_repository.get({"username": username})
        return None

    def get_all(self) -> List[User]:
        """Get all users"""
        return user_repository.get_all()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        return user_repository.get({"id": user_id})

    def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        return user_repository.get({"username": username})

    def register(self, username: str, password: str) -> Optional[User]:
        """Register a user"""
        return user_repository.create(username=username, password=generate_password_hash(password))

user_service = UserService()
