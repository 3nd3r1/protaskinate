"""protaskinate/entities/project.py"""

from dataclasses import dataclass


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
