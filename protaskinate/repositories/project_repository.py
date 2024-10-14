"""protaskinate/repositories/project_repository.py"""
from typing import Any, List, Optional

from sqlalchemy import Row, text

from protaskinate.entities.project import (Project, ProjectRole, ProjectUser,
                                           ProjectWithRole)
from protaskinate.repositories.repository import Repository
from protaskinate.repositories.user_repository import \
    AllFields as AllUserFields
from protaskinate.repositories.user_repository import create_user_from_row
from protaskinate.utils.database import db

AllFields = ["id", "name", "creator_id", "created_at", "updated_at", "description"]
RequiredFields = ["name", "creator_id", "created_at", "updated_at"]

def create_project_from_row(row: Row[Any]) -> Project:
    """Helper function to create a Project entity from a database row"""
    return Project(id=row[0], name=row[1], creator_id=row[2], created_at=row[3],
                   updated_at=row[4], description=row[5])

def create_project_with_role_from_row(row: Row[Any]) -> ProjectWithRole:
    """Helper function to create a ProjectWithRole entity from a database row"""
    return ProjectWithRole(project=create_project_from_row(row),
                           role=ProjectRole(row[len(AllFields)]))

def create_project_user_from_row(row: Row[Any]) -> ProjectUser:
    """Helper function to create a ProjectUser entity from a database row"""
    return ProjectUser(user=create_user_from_row(row), role=ProjectRole(row[len(AllUserFields)]))

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

    def get_all_users_by_project(self, project_id: int) -> List[ProjectUser]:
        """Get all users and roles in a project"""
        user_fields = ", ".join(f"u.{field}" for field in AllUserFields)
        sql = f"""SELECT {user_fields}, up.role
                 FROM users u
                 JOIN user_projects up ON u.id = up.user_id
                 WHERE up.project_id = :project_id"""

        result = db.session.execute(text(sql), {"project_id": project_id})
        rows = result.fetchall()

        return [create_project_user_from_row(row) for row in rows]

    def update_user_role(self, project_id: int, user_id: int, role: ProjectRole) -> None:
        """Update the role of a user in a project"""
        sql = """UPDATE user_projects
                  SET role = :role
                  WHERE project_id = :project_id AND user_id = :user_id"""

        db.session.execute(text(sql), {"role": role.value, "project_id": project_id,
                                       "user_id": user_id})
        db.session.commit()

    def create_project_user(self, project_id: int, user_id: int,
                            role: ProjectRole) -> Optional[ProjectUser]:
        """Add a user to a project"""
        user_fields = ", ".join(f"u.{field}" for field in AllUserFields)

        sql = f"""WITH new AS (
                    INSERT INTO user_projects (project_id, user_id, role)
                    VALUES (:project_id, :user_id, :role)
                    RETURNING user_id, project_id, role
                 )
                 SELECT {user_fields}, new.role
                 FROM new new
                 JOIN users u ON u.id = new.user_id"""

        result = db.session.execute(text(sql), {"project_id": project_id, "user_id": user_id,
                                                "role": role.value})
        row = result.fetchone()
        db.session.commit()
        if row is None:
            return None

        return create_project_user_from_row(row)

project_repository = ProjectRepository()
