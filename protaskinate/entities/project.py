"""protaskinate/entities/project.py"""

from dataclasses import dataclass
from enum import Enum

from protaskinate.utils.validation import validate_enum


class ProjectRole(Enum):
    """Enumeration representing the role of a user in a project"""
    READER = "reader"
    WRITER = "writer"
    ADMIN = "admin"

@dataclass
class Project:
    """Class representing a project"""
    id: int
    name: str
    creator_id: int

    def __post_init__(self):
        if not isinstance(self.id, int):
            raise ValueError(f"Invalid id: {self.id}")

        if not isinstance(self.name, str):
            raise ValueError(f"Invalid name: {self.name}")

        if not isinstance(self.creator_id, int):
            raise ValueError(f"Invalid creator_id: {self.creator_id}")

@dataclass
class ProjectWithRole(Project):
    """Class representing a project with the current user's role"""
    role: ProjectRole

    def __post_init__(self):
        self.role = validate_enum(self.role, ProjectRole, "role")
