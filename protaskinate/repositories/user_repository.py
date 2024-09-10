"""protaskinate/repositories/user_repository.py"""

from typing import Optional

from sqlalchemy import text
from werkzeug.security import check_password_hash

from protaskinate.entities import User
from protaskinate.utils.database import db


class UserRepository:
    """Class representing a repository for users"""

    def get_by_username(self, username: str) -> Optional[User]:
        """Get a user from the repository by username"""
        sql = """SELECT id, username
                 FROM users WHERE username = :username"""
        result = db.session.execute(text(sql),
                                    {"username": username})
        row = result.fetchone()
        if row is None:
            return None
        return User(user_id=row[0], username=row[1])

    def verify_password(self, username: str, password: str) -> bool:
        """Verify a password against a password hash"""
        sql = """SELECT password
                 FROM users WHERE username = :username"""
        result = db.session.execute(text(sql),
                                    {"username": username})
        row = result.fetchone()
        if row is None:
            return False
        return check_password_hash(row[0], password)

user_repository = UserRepository()
