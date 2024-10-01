"""protaskinate/services/task_service.py"""

from typing import List, Optional

from protaskinate.entities import Task
from protaskinate.repositories import task_repository


class TaskService:
    """Class representing a service for tasks"""
    def get_all_by_project(self,
                project_id: int,
                order_by_fields: Optional[List[str]],
                reverse: Optional[List[bool]]) -> List[Task]:
        """Get all tasks by project"""
        return task_repository.get_all({"project_id": project_id}, order_by_fields, reverse)

    def get_by_id_and_project(self, task_id: int, project_id: int) -> Optional[Task]:
        """Get task by ID"""
        return task_repository.get({"id": task_id, "project_id": project_id})

    def update(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update the task"""
        return task_repository.update(task_id, **kwargs)

    def create(self, **kwargs) -> Optional[Task]:
        """Create a task"""
        return task_repository.create(**kwargs)

    def delete(self, task_id: int) -> None:
        """Delete a task"""
        return task_repository.delete(task_id)

task_service = TaskService()
