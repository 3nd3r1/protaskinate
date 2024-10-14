"""protaskinate/repositories/project_repository.py"""
from typing import Any, List, Optional

from sqlalchemy import Row, text

from protaskinate.entities.project import Project, ProjectRole, ProjectWithRole
from protaskinate.repositories.repository import Repository
from protaskinate.utils.database import db

AllFields = ["id", "name", "creator_id", "created_at", "updated_at", "description"]
RequiredFields = ["name", "creator_id", "created_at", "updated_at"]

def create_project_from_row(row: Row[Any]) -> Project:
    """Helper function to create a Project entity from a database row"""
    return Project(id=row[0], name=row[1], creator_id=row[2], created_at=row[3],
                   updated_at=row[4], description=row[5])

def create_project_with_role_from_row(row: Row[Any]) -> ProjectWithRole:
    """Helper function to create a ProjectWithRole entity from a database row"""
    return ProjectWithRole(project=create_project_from_row(row), role=ProjectRole(row[6]))

class ProjectRepository(Repository[Project]):
    """Task repository for managing projects"""

    def __init__(self):
        super().__init__(table_name="projects",
                         fields=AllFields,
                         required_fields=RequiredFields,
                         entity_creator=create_project_from_row)

    def get_all_by_user_and_roles_with_role(self, user_id: int,
                                            roles: List[ProjectRole]
                                            ) -> List[ProjectWithRole]:
        """Get all projects and roles of a single user filtered by roles"""
        fields = ", ".join(f"project.{field}" for field in self._fields)
        roles_tuple = tuple(role.value for role in roles)

        sql = f"""SELECT {fields}, up.role
                  FROM {self._table_name} project
                  JOIN user_projects up ON project.id = up.project_id
                  WHERE up.user_id = :user_id AND up.role IN :roles"""

        result = db.session.execute(text(sql), {"user_id": user_id, "roles": roles_tuple})
        rows = result.fetchall()

        return [create_project_with_role_from_row(row) for row in rows]

    def get_user_role(self, user_id: int, project_id: int) -> Optional[ProjectRole]:
        """Get the role of a user in a project"""

        sql = f"""SELECT up.role
                  FROM {self._table_name} project
                  JOIN user_projects up ON project.id = up.project_id
                  WHERE up.user_id = :user_id AND project.id = :project_id"""

        result = db.session.execute(text(sql), {"user_id": user_id, "project_id": project_id})
        row = result.fetchone()

        if row is None:
            return None
        return ProjectRole(row[0])

project_repository = ProjectRepository()
