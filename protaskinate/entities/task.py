"""protaskinate/entities/task.py"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

from protaskinate.entities.comment import Comment
from protaskinate.utils.validation import validate_enum, validate_type


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
    project_id: int
    creator_id: int
    title: str
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
    assignee_id: Optional[int] = None
    deadline: Optional[datetime] = None
    description: Optional[str] = None

    def __post_init__(self):
        validate_type(self.id, int, "id")
        validate_type(self.project_id, int, "project_id")
        validate_type(self.creator_id, int, "creator_id")
        validate_type(self.title, str, "title")
        self.status = validate_enum(self.status, TaskStatus, "status")
        self.priority = validate_enum(self.priority, TaskPriority, "priority")
        validate_type(self.created_at, datetime, "created_at")
        validate_type(self.updated_at, datetime, "updated_at")
        validate_type(self.assignee_id, int, "assignee_id", allow_none=True)
        validate_type(self.deadline, datetime, "deadline", allow_none=True)
        validate_type(self.description, str, "description", allow_none=True)
