"""protaskinate/services/activity_log_service.py"""

from datetime import datetime
from typing import List, Optional, TypedDict
from typing_extensions import Unpack, NotRequired

from protaskinate.entities.activity_log import ActivityLog, ActivityLogAction
from protaskinate.repositories import activity_log_repository


class NewActivityLog(TypedDict):
    """Type representing the data required to create a new activity log"""

    user_id: int
    project_id: int
    action: ActivityLogAction
    created_at: NotRequired[datetime]


class ActivityLogService:
    """Activity log service"""

    def get_all_by_project(self, project_id: int) -> List[ActivityLog]:
        """Get all activity logs by project"""
        return activity_log_repository.get_all({"project_id": project_id}, ["created_at"], [True])


    def create_log(self, **kwargs: Unpack[NewActivityLog]) -> Optional[ActivityLog]:
        """Create a new activity log"""
        return activity_log_repository.create(
            {
                "user_id": kwargs["user_id"],
                "project_id": kwargs["project_id"],
                "created_at": (
                    kwargs["created_at"].isoformat()
                    if "created_at" in kwargs
                    else datetime.now().isoformat()
                ),
                "action": kwargs["action"].value,
            }
        )

activity_log_service = ActivityLogService()
