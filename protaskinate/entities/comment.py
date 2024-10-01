"""protaskinate/entities/comment.py"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Comment:
    """Class representing a comment"""
    id: int
    task_id: int
    creator_id: int
    created_at: datetime
    content: str

    def __post_init__(self):
        if not isinstance(self.id, int):
            raise ValueError(f"Invalid id: {self.id}")

        if not isinstance(self.task_id, int):
            raise ValueError(f"Invalid task_id: {self.task_id}")

        if not isinstance(self.creator_id, int):
            raise ValueError(f"Invalid creator_id: {self.creator_id}")

        if not isinstance(self.created_at, datetime):
            raise ValueError(f"Invalid created_at: {self.created_at}")

        if not isinstance(self.content, str):
            raise ValueError(f"Invalid content: {self.content}")
