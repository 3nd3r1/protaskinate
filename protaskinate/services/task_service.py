"""protaskinate/services/task_service.py"""

from typing import List, Literal, Optional

from protaskinate.entities import Task
from protaskinate.repositories import task_repository


class TaskService:
    """Class representing a service for tasks"""
    def get_all(self,
                order_by_fields: Optional[list[Literal["title", "created_at", "priority"]]],
                reverse: Optional[list[bool]]) -> List[Task]:
        """Get all tasks"""
        return task_repository.get_all(order_by_fields, reverse)

    def update(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update the task"""
        return task_repository.update(task_id, **kwargs)

    def create(self, **kwargs) -> Optional[Task]:
        """Create a task"""
        return task_repository.create(**kwargs)

task_service = TaskService()
