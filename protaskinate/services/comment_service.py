"""protaskinate/services/comment_service.py"""

from typing import Optional

from protaskinate.entities import Comment
from protaskinate.repositories import comment_repository


class CommentService:
    """Comment service that interacts with the repository"""
    def create(self, **kwargs) -> Optional[Comment]:
        """Create a comment"""
        return comment_repository.create(kwargs)

    def delete(self, comment_id: int, task_id: int) -> None:
        """Delete a comment"""
        return comment_repository.delete({"id": comment_id, "task_id": task_id})

comment_service = CommentService()
