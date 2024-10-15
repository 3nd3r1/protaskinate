"""protaskinate/repositories/activity_log_repository.py"""

from protaskinate.entities.activity_log import ActivityLog
from protaskinate.repositories.repository import Repository


AllFields = ["id", "user_id", "project_id", "created_at", "action"]
RequiredFields = ["user_id", "project_id", "created_at", "action"]


def create_activity_log_from_row(row) -> ActivityLog:
    """Helper function to create an ActivityLog entity from a database row"""
    return ActivityLog(
        id=row[0], user_id=row[1], project_id=row[2], created_at=row[3], action=row[4]
    )


class ActivityLogRepository(Repository[ActivityLog]):
    """ActivityLog repository for managing activity logs"""

    def __init__(self):
        super().__init__(
            table_name="activity_logs",
            fields=AllFields,
            required_fields=RequiredFields,
            entity_creator=create_activity_log_from_row,
        )


activity_log_repository = ActivityLogRepository()
