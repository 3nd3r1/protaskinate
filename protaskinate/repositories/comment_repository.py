"""protaskinate/repositories/comment_repository.py"""
from protaskinate.entities import Comment
from protaskinate.repositories.repository import Repository

AllFields = ["id", "task_id", "creator_id", "created_at", "content"]
RequiredFields = ["task_id", "creator_id", "created_at", "content"]

def create_comment_from_row(row) -> Comment:
    """Helper function to create a Comment entity from a database row"""
    return Comment(id=row[0],
                   task_id=row[1],
                   creator_id=row[2],
                   created_at=row[3],
                   content=row[4])

class CommentRepository(Repository[Comment]):
    """Comment repository for managing tasks"""

    def __init__(self):
        super().__init__(table_name="comments",
                         fields=AllFields,
                         required_fields=RequiredFields,
                         entity_creator=create_comment_from_row)

comment_repository = CommentRepository()
