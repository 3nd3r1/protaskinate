"""protaskinate/services/task_service.py"""

from typing import List

from protaskinate.entities import Task
from protaskinate.repositories import task_repository


class TaskService:
    """Class representing a service for tasks"""
    def get_all(self) -> List[Task]:
        """Get all tasks"""
        return task_repository.get_all()

    def update(self, task_id: int, **kwargs):
        """Update the task"""
        task_repository.update(task_id, **kwargs)

task_service = TaskService()
