"""protaskinate/repositories/task_repository.py"""


from typing import List

from sqlalchemy import text

from protaskinate.entities import Task
from protaskinate.utils.database import db


class TaskRepository:
    """Class representing a repository for tasks"""

    def get_all(self) -> List[Task]:
        """Get all tasks from the repository"""
        sql = """SELECT id, title, status, creator_id
                 FROM tasks"""
        result = db.session.execute(text(sql))
        row = result.fetchall()
        return [Task(task_id=row[0], title=row[1], status=row[2], creator_id=row[3]) for row in row]

    def update(self, task_id: int, **kwargs):
        """Update the task in the repository"""
        allowed_attributes = ["title", "status"]
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
