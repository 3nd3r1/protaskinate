"""protaskinate/repositories/task_repository.py"""


from typing import List, Literal, Optional

from sqlalchemy import text

from protaskinate.entities import Task
from protaskinate.utils.database import db


class TaskRepository:
    """Class representing a repository for tasks"""

    def get_all(self,
                order_by_fields: Optional[List[Literal["title", "created_at", "priority"]]],
                reverse: Optional[list[bool]]) -> List[Task]:
        """Get all tasks from the repository"""
        if order_by_fields is None or reverse is None:
            order_by_fields = ["created_at"]
            reverse = [True]

        allowed_attributes = ["title", "created_at", "priority"]
        order_clause = ", ".join(
                f"{field} {'DESC' if reverse else ''}"
                for field, reverse in zip(order_by_fields, reverse)
                if field in allowed_attributes)

        sql = f"""SELECT id, title, status, creator_id, created_at, priority, assignee_id, deadline
                 FROM tasks ORDER BY {order_clause}"""

        result = db.session.execute(text(sql))
        row = result.fetchall()
        return [Task(id=row[0],
                     title=row[1],
                     status=row[2],
                     creator_id=row[3],
                     created_at=row[4],
                     priority=row[5],
                     assignee_id=row[6],
                     deadline=row[7]) for row in row]

    def update(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update the task in the repository"""
        allowed_attributes = ["title", "status", "priority", "assignee_id"]
        filtered_kwargs = {key: value for key, value in kwargs.items() if key in allowed_attributes}
        if not filtered_kwargs:
            return None

        set_clause = ", ".join(f"{key} = :{key}" for key in filtered_kwargs.keys())

        sql = f"""
            UPDATE tasks
            SET {set_clause}
            WHERE id = :task_id
            RETURNING id, title, status, creator_id, created_at, priority, assignee_id, deadline
        """

        result = db.session.execute(text(sql), {"task_id": task_id, **filtered_kwargs})
        row = result.fetchone()
        db.session.commit()
        if row is None:
            return None
        return Task(id=row[0],
                    title=row[1],
                    status=row[2],
                    creator_id=row[3],
                    created_at=row[4],
                    priority=row[5],
                    assignee_id=row[6],
                    deadline=row[7])

    def create(self, **kwargs) -> Optional[Task]:
        """Create a new task"""
        required_attributes = ["title", "status", "creator_id",
                               "created_at", "priority", "assignee_id", "deadline"]
        if not all(key in kwargs for key in required_attributes):
            raise ValueError("Missing required attributes")

        sql = """
            INSERT INTO tasks (title, status, creator_id, created_at, priority, assignee_id, deadline)
            VALUES (:title, :status, :creator_id, :created_at, :priority, :assignee_id, :deadline)
            RETURNING id, title, status, creator_id, created_at, priority, assignee_id, deadline
        """

        result = db.session.execute(text(sql), kwargs)
        row = result.fetchone()
        db.session.commit()

        if row is None:
            return None
        return Task(id=row[0],
                    title=row[1],
                    status=row[2],
                    creator_id=row[3],
                    created_at=row[4],
                    priority=row[5],
                    assignee_id=row[6],
                    deadline=row[7])

task_repository = TaskRepository()
