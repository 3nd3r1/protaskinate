"""protaskinate/entities/project.py"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from protaskinate.entities.user import User
from protaskinate.utils.validation import validate_enum, validate_type


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
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None

    def __post_init__(self):
        validate_type(self.id, int, "id")
        validate_type(self.name, str, "name")
        validate_type(self.creator_id, int, "creator_id")
        validate_type(self.created_at, datetime, "created_at")
        validate_type(self.updated_at, datetime, "updated_at")
        validate_type(self.description, str, "description", allow_none=True)


@dataclass
class ProjectWithRole:
    """Class representing a project with the current user's role"""
    project: Project
    role: ProjectRole

    def __post_init__(self):
        validate_type(self.project, Project, "project")
        self.role = validate_enum(self.role, ProjectRole, "role")

@dataclass
class ProjectUser:
    """Class representing a user in a project"""
    user: User
    role: ProjectRole

    def __post_init__(self):
        validate_type(self.user, User, "user")
        self.role = validate_enum(self.role, ProjectRole, "role")
