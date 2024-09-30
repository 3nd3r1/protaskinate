"""protaskinate/repositories/project_repository.py"""

from typing import List, Optional
from sqlalchemy import text
from protaskinate.utils.database import db
from protaskinate.entities import Project


class ProjectRepository:
    """Class representing a repository for projects"""

    def get_all(self) -> List[Project]:
        """Get all projects"""
        sql = "SELECT id, name, creator_id FROM projects"

        result = db.session.execute(text(sql))
        rows = result.fetchall()

        return [Project(id=row[0], name=row[1], creator_id=row[2]) for row in rows]

    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by id"""
        sql = "SELECT id, name, creator_id FROM projects WHERE id = :project_id"

        result = db.session.execute(text(sql), {"project_id": project_id})
        row = result.fetchone()

        if row is None:
            return None
        return Project(id=row[0], name=row[1], creator_id=row[2])

project_repository = ProjectRepository()
