"""protaskinate/services/task_service.py"""

from typing import List, Literal

from protaskinate.entities import Task
from protaskinate.repositories import task_repository


class TaskService:
    """Class representing a service for tasks"""
    def get_all(self,
                order_by_fields: list[Literal["title", "created_at", "priority"]] | None = None,
                reverse: list[bool] | None = None) -> List[Task]:
        """Get all tasks"""
        return task_repository.get_all(order_by_fields, reverse)

    def update(self, task_id: int, **kwargs):
        """Update the task"""
        task_repository.update(task_id, **kwargs)

    def create(self, **kwargs):
        """Create a task"""
        task_repository.create(**kwargs)

task_service = TaskService()
