"""protaskinate/entities/activity_log.py"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TypedDict

from protaskinate.utils.validation import validate_enum, validate_type


class ActivityLogAction(Enum):
    """Enumeration representing the action of an activity log"""

    CREATE_TASK = "create_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    UPDATE_PROJECT = "update_project"

class NewActivityLog(TypedDict):
    """Type representing the data required to create a new activity log"""

    user_id: int
    project_id: int
    created_at: datetime
    action: ActivityLogAction

@dataclass
class ActivityLog:
    """Class representing an activity log"""

    id: int
    user_id: int
    project_id: int
    created_at: datetime
    action: ActivityLogAction

    def __post_init__(self):
        validate_type(self.id, int, "id")
        validate_type(self.user_id, int, "user_id")
        validate_type(self.project_id, int, "project_id")
        validate_type(self.created_at, datetime, "created_at")
        self.action = validate_enum(self.action, ActivityLogAction, "action")
