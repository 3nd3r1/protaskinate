"""protaskinate/repositories/user_repository.py"""

from sqlalchemy import text
from werkzeug.security import check_password_hash

from protaskinate.entities import User
from protaskinate.repositories.repository import Repository
from protaskinate.utils.database import db

AllFields = ["id", "username", "password"]
RequiredFields = ["username", "password"]


def create_user_from_row(row) -> User:
    """Helper function to create a User entity from a database row"""
    return User(id=row[0], username=row[1])


class UserRepository(Repository[User]):
    """User repository for managing users"""

    def __init__(self):
        super().__init__(
            table_name="users",
            fields=AllFields,
            required_fields=RequiredFields,
            entity_creator=create_user_from_row,
        )

    def verify_password(self, username: str, password: str) -> bool:
        """Verify a password against a password hash"""
        sql = f"""SELECT password
                 FROM {self._table_name} WHERE username = :username"""
        result = db.session.execute(text(sql), {"username": username})
        row = result.fetchone()

        if row is None:
            return False
        return check_password_hash(row[0], password)


user_repository = UserRepository()
