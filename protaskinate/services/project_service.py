"""protaskinate/services/project_service.py"""

from typing import List, Optional

from protaskinate.entities.project import (
    Project,
    ProjectRole,
    ProjectUser,
    ProjectWithRole,
)
from protaskinate.repositories import project_repository
from protaskinate.services import task_service


class ProjectService:
    """Class representing a service for projects"""

    def get_all(self) -> List[Project]:
        """Get all projects"""
        return project_repository.get_all()

    def get_all_by_user_with_role(self, user_id: int) -> List[ProjectWithRole]:
        """Get all user projects with their roles"""
        return project_repository.get_all_by_user_and_roles_with_role(
            user_id, [ProjectRole.READER, ProjectRole.WRITER, ProjectRole.ADMIN]
        )

    def get_all_users_in_project(self, project_id: int) -> List[ProjectUser]:
        """Get all users in a project"""
        return project_repository.get_all_users_by_project(project_id)

    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by id"""
        return project_repository.get({"id": project_id})

    def get_user_role(self, user_id: int, project_id: int) -> Optional[ProjectRole]:
        """Get the role of a user in a project"""
        return project_repository.get_user_role(user_id, project_id)

    def delete(self, project_id: int) -> None:
        """Delete a project"""
        return project_repository.delete({"id": project_id})

    def create(self, **kwargs) -> Optional[Project]:
        """Create a project"""
        return project_repository.create(kwargs)

    def add_user(
        self, project_id: int, user_id: int, role: ProjectRole
    ) -> Optional[ProjectUser]:
        """Add a user to a project"""
        return project_repository.create_project_user(project_id, user_id, role)

    def update_user_role(
        self, project_id: int, user_id: int, role: ProjectRole
    ) -> None:
        """Update the role of a user in a project"""
        return project_repository.update_user_role(project_id, user_id, role)

    def check_user_read_access(self, user_id: int, project_id: int) -> bool:
        """Check if a user has read-access to a project"""
        return project_repository.get_user_role(user_id, project_id) in [
            ProjectRole.READER,
            ProjectRole.WRITER,
            ProjectRole.ADMIN,
        ]

    def check_user_write_access(self, user_id: int, project_id: int) -> bool:
        """Check if a user has write-access to a project"""
        return project_repository.get_user_role(user_id, project_id) in [
            ProjectRole.WRITER,
            ProjectRole.ADMIN,
        ]

    def check_user_update_access(self, user_id: int, project_id: int) -> bool:
        """Check if a user has update-access to a project"""
        return (
            project_repository.get_user_role(user_id, project_id) == ProjectRole.ADMIN
        )

    def check_user_task_update_access(
        self, user_id: int, project_id: int, task_id: int
    ) -> bool:
        """Check if a user has update-access to a task"""
        user_project_role = project_repository.get_user_role(user_id, project_id)
        if user_project_role == ProjectRole.ADMIN:
            return True

        task = task_service.get_by_id_and_project(task_id, project_id)
        if not task or task.project_id != project_id:
            return False

        if user_project_role == ProjectRole.WRITER and task.creator_id == user_id:
            return True

        return False


project_service = ProjectService()
