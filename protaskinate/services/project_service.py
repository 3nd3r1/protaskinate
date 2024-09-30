"""protaskinate/services/project_service.py"""

from typing import List, Optional
from protaskinate.entities.project import Project
from protaskinate.repositories import project_repository


class ProjectService:
    """Class representing a service for projects"""

    def get_all(self) -> List[Project]:
        """Get all projects"""
        return project_repository.get_all()

    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by id"""
        return project_repository.get_by_id(project_id)

project_service = ProjectService()
