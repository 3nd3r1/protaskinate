"""protaskinate/entities/task.py"""

from enum import Enum

class TaskStatus(Enum):
    """Enumeration representing the status of a task"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task:
    """Class representing a task"""

    def __init__(self, task_id: int, status: TaskStatus, title: str, creator_id: int):
        self.id = task_id
        self.title = title
        self.status = status
        self.creator_id = creator_id
