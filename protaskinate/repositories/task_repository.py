"""protaskinate/repositories/task_repository.py"""


from typing import List, Literal

from sqlalchemy import text

from protaskinate.entities import Task
from protaskinate.utils.database import db


class TaskRepository:
    """Class representing a repository for tasks"""

    def get_all(self,
                order_by_fields: List[Literal["title", "created_at", "priority"]] | None = None,
                reverse: list[bool] | None = None) -> List[Task]:
        """Get all tasks from the repository"""
        if order_by_fields is None or reverse is None:
            order_by_fields = ["created_at"]
            reverse = [True]

        allowed_attributes = ["title", "created_at", "priority"]
        order_clause = ", ".join(
                f"{field} {'DESC' if reverse else ''}"
                for field, reverse in zip(order_by_fields, reverse)
                if field in allowed_attributes)

        sql = f"""SELECT id, title, status, creator_id, created_at, priority
                 FROM tasks ORDER BY {order_clause}"""

        result = db.session.execute(text(sql))
        row = result.fetchall()
        return [Task(id=row[0],
                     title=row[1],
                     status=row[2],
                     creator_id=row[3],
                     created_at=row[4],
                     priority=row[5]) for row in row]

    def update(self, task_id: int, **kwargs):
        """Update the task in the repository"""
        allowed_attributes = ["title", "status", "priority"]
        filtered_kwargs = {key: value for key, value in kwargs.items() if key in allowed_attributes}
        set_clause = ", ".join(f"{key} = :{key}" for key in filtered_kwargs.keys())
        sql = f"""
            UPDATE tasks
            SET {set_clause}
            WHERE id = :task_id
        """
        db.session.execute(text(sql), {"task_id": task_id, **filtered_kwargs})
        db.session.commit()

task_repository = TaskRepository()
