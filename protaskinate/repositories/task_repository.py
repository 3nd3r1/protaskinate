"""protaskinate/repositories/task_repository.py"""
from typing import Dict, Optional, Union

from sqlalchemy import text

from protaskinate.entities import Task
from protaskinate.repositories.comment_repository import \
    create_comment_from_row, AllFields as CommentAllFields
from protaskinate.repositories.repository import Repository
from protaskinate.utils.database import db

AllFields = ["id", "project_id", "creator_id", "title", "status", "priority", "created_at",
             "updated_at", "assignee_id", "deadline", "description"]
RequiredFields = ["project_id", "creator_id", "title", "status", "priority",
                  "created_at", "updated_at"]

def create_task_from_row(row) -> Task:
    """Helper function to create a Task entity from a database row"""
    return Task(id=row[0],
                project_id=row[1],
                creator_id=row[2],
                title=row[3],
                status=row[4],
                priority=row[5],
                created_at=row[6],
                updated_at=row[7],
                assignee_id=row[8],
                deadline=row[9],
                description=row[10])

class TaskRepository(Repository[Task]):
    """Task repository for managing tasks"""

    def __init__(self):
        super().__init__(table_name="tasks",
                         fields=AllFields,
                         required_fields=RequiredFields,
                         entity_creator=create_task_from_row)

    def get_join_comments(self, by_fields: Dict[str, Union[int, str]]) -> Optional[Task]:
        """Get a task by fields and join comments"""
        if not by_fields or any(key not in self._fields for key in by_fields):
            raise ValueError("Invalid by_fields")

        where_clause = " AND ".join(f"task.{key} = :{key}" for key in by_fields)
        fields = ", ".join(f"task.{field}" for field in self._fields)
        fields += ", "+", ".join(f"comment.{field}" for field in CommentAllFields)

        sql = f"""SELECT {fields}
                 FROM {self._table_name} task
                 LEFT JOIN comments comment ON task.id = comment.task_id
                 WHERE {where_clause}
                 ORDER BY comment.created_at"""

        result = db.session.execute(text(sql), by_fields)
        rows = result.fetchall()

        if not rows:
            return None

        task = self._entity_creator(rows[0])
        task.comments = []
        for row in rows:
            if row[len(self._fields)] and row[0] == task.id:
                comment = create_comment_from_row(row[len(self._fields):])
                task.comments.append(comment)

        return task


task_repository = TaskRepository()
