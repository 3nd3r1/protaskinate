"""protaskinate/repositories/project_repository.py"""
from protaskinate.entities import Project
from protaskinate.repositories.repository import Repository

AllFields = ["id", "name", "creator_id"]
RequiredFields = ["name", "creator_id"]

def create_project_from_row(row) -> Project:
    """Helper function to create a Project entity from a database row"""
    return Project(id=row[0], name=row[1], creator_id=row[2])

class ProjectRepository(Repository[Project]):
    """Task repository for managing projects"""

    def __init__(self):
        super().__init__(table_name="projects",
                         fields=AllFields,
                         required_fields=RequiredFields,
                         entity_creator=create_project_from_row)

project_repository = ProjectRepository()
