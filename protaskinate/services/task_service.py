"""protaskinate/services/task_service.py"""

from typing import Dict, List, Optional

from protaskinate.entities import Task
from protaskinate.entities.task import TaskStatus
from protaskinate.repositories import task_repository


class TaskService:
    """Class representing a service for tasks"""

    def get_all_by_project(
        self,
        project_id: int,
        order_by_fields: Optional[List[str]] = None,
        reverse: Optional[List[bool]] = None,
    ) -> List[Task]:
        """Get all tasks by project"""
        return task_repository.get_all(
            {"project_id": project_id}, order_by_fields, reverse
        )

    def get_by_id_and_project(self, task_id: int, project_id: int) -> Optional[Task]:
        """Get task by ID and project"""
        return task_repository.get({"id": task_id, "project_id": project_id})

    def count_by_assignee_grouped_by_status(
        self, assignee_id: int
    ) -> Dict[TaskStatus, int]:
        """Get all tasks assigned to a user grouped by status"""
        return task_repository.count_by_assignee_grouped_by_status(assignee_id)

    def update(self, task_id: int, project_id: int, **kwargs) -> Optional[Task]:
        """Update the task"""
        return task_repository.update({"id": task_id, "project_id": project_id}, kwargs)

    def create(self, **kwargs) -> Optional[Task]:
        """Create a task"""
        return task_repository.create(kwargs)

    def delete(self, task_id: int, project_id: int) -> None:
        """Delete a task"""
        return task_repository.delete({"id": task_id, "project_id": project_id})


task_service = TaskService()
