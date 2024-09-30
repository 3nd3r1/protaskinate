"""protaskinate/entities/task.py"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    """Enumeration representing the status of a task"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskPriority(Enum):
    """Enumeration representing the priority of a task"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

    def as_int(self):
        """Return the integer value of the priority"""
        if self == TaskPriority.LOW:
            return 0
        if self == TaskPriority.MEDIUM:
            return 1
        if self == TaskPriority.HIGH:
            return 2
        return 3

    def __lt__(self, other):
        return self.as_int() < other.as_int()

    def __le__(self, other):
        return self.as_int() <= other.as_int()

    def __gt__(self, other):
        return self.as_int() > other.as_int()

    def __ge__(self, other):
        return self.as_int() >= other.as_int()

@dataclass
class Task:
    """Class representing a task"""
    id: int
    title: str
    status: TaskStatus
    creator_id: int
    created_at: datetime
    priority: TaskPriority
    assignee_id: Optional[int]
    deadline: Optional[datetime]
    project_id: int

    def __post_init__(self):
        if not isinstance(self.id, int):
            raise ValueError(f"Invalid id: {self.id}")

        if not isinstance(self.title, str):
            raise ValueError(f"Invalid title: {self.title}")

        if not isinstance(self.status, TaskStatus):
            try:
                self.status = TaskStatus(self.status)
            except ValueError as exc:
                raise ValueError(f"Invalid status: {self.status}") from exc

        if not isinstance(self.creator_id, int):
            raise ValueError(f"Invalid creator_id: {self.creator_id}")

        if not isinstance(self.created_at, datetime):
            raise ValueError(f"Invalid created_at: {self.created_at}")

        if not isinstance(self.priority, TaskPriority):
            try:
                self.priority = TaskPriority(self.priority)
            except ValueError as exc:
                raise ValueError(f"Invalid priority: {self.priority}") from exc

        if not isinstance(self.assignee_id, int) and self.assignee_id is not None:
            raise ValueError(f"Invalid assignee_id: {self.assignee_id}")

        if not isinstance(self.deadline, datetime) and self.deadline is not None:
            raise ValueError(f"Invalid deadline: {self.deadline}")

        if not isinstance(self.project_id, int):
            raise ValueError(f"Invalid project_id: {self.project_id}")
