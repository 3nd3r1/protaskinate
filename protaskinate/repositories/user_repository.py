"""protaskinate/repositories/user_repository.py"""

from typing import Optional

from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

from protaskinate.entities import User
from protaskinate.utils.database import db


class UserRepository:
    """Class representing a repository for users"""

    def get_all(self) -> list[User]:
        """Get all users"""
        sql = """SELECT id, username
                  FROM users"""
        result = db.session.execute(text(sql))
        rows = result.fetchall()
        return [User(id=row[0], username=row[1]) for row in rows]

    def get_by_username(self, username: str) -> Optional[User]:
        """Get a user from the repository by username"""
        sql = """SELECT id, username
                 FROM users WHERE username = :username"""
        result = db.session.execute(text(sql),
                                    {"username": username})
        row = result.fetchone()
        if row is None:
            return None
        return User(id=row[0], username=row[1])

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get a user from the repository by ID"""
        sql = """SELECT id, username
                 FROM users WHERE id = :id"""
        result = db.session.execute(text(sql),
                                    {"id": user_id})
        row = result.fetchone()
        if row is None:
            return None
        return User(id=row[0], username=row[1])

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

    def create(self, **kwargs) -> Optional[User]:
        """Create a new user"""
        required_fields = ["username", "password"]
        if not all(field in kwargs for field in required_fields):
            raise ValueError("Missing required fields")

        sql = """INSERT INTO users (username, password)
                 VALUES (:username, :password)
                 RETURNING id, username"""

        result = db.session.execute(text(sql),
                                    {"username": kwargs["username"],
                                     "password": generate_password_hash(kwargs["password"])})
        row = result.fetchone()
        db.session.commit()

        if row is None:
            return None
        return User(id=row[0], username=row[1])

user_repository = UserRepository()
